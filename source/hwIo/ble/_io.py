# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Dot Incorporated, Bram Duvigneau
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
import time
from itertools import count, takewhile
from queue import Empty, Queue
from threading import Event, Thread
from typing import Callable, Iterator
import weakref

from asyncioEventLoop import runCoroutine
from ..base import _isDebug, IoBase
from ..ioThread import IoThread
from logHandler import log

import bleak
from bleak.backends.device import BLEDevice
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.winrt.client import WinRTClientArgs

CONNECT_TIMEOUT_SECONDS: int = 2
WINRT_CLIENT_ARGS = WinRTClientArgs(use_cached_services=True)


def queueReader(
	queue: Queue[bytes],
	onReceive: Callable[[bytes], None],
	stopEvent: Event,
	ioThread: IoThread,
) -> None:
	while True:
		try:
			if stopEvent.is_set():
				log.debug("Reader thread got stop event")
				break
			try:
				data: bytes = queue.get(timeout=0.2)
			except Empty:
				continue

			def apc(_x: int = 0):
				return onReceive(data)

			ioThread.queueAsApc(apc)
			queue.task_done()
		except Exception:
			log.error("Reader thread got exception", exc_info=True)


def sliced(data: bytes, n: int) -> Iterator[bytes]:
	"""Split data into chunks of size n (last chunk may be smaller)."""
	return takewhile(len, (data[i : i + n] for i in count(0, n)))


class Ble(IoBase):
	"""I/O for Bluetooth Low Energy (BLE) devices

	This implementation expects a service/characteristic pair to send raw data to as a BLE command
	and receive raw data through a BLE notify on a service/characteristic pair.
	"""

	_client: bleak.BleakClient
	"The Bleak client to use for BLE communication"
	_writeServiceUuid: str
	"The service UUID to use for writing data to the peripheral, this should accept BLE commands"
	_writeCharacteristicUuid: str
	"The characteristic UUID to use for writing data to the peripheral, this should accept BLE commands"
	_readServiceUuid: str
	"The service UUID to use for reading data from the peripheral, this should generate BLE notifications"
	_readCharacteristicUuid: str
	"""The characteristic UUID to use for reading data from the peripheral,
	this should generate BLE notifications"""
	_onReceive: Callable[[bytes], None] | None
	"The callback to call when data is received"
	_queuedData: Queue[bytes | bytearray]
	"A queue of received data, this is processed by the onReceive handler"
	_readEvent: Event
	"An event that is set when data is received"
	_readerThread: Thread
	"Thread that processes the queue of read data"
	_stopReaderEvent: Event
	"Event that is set to stop the reader thread"
	_ioThreadRef: weakref.ReferenceType[IoThread]
	"Reference to the I/O thread"

	def __init__(
		self,
		device: BLEDevice | str,
		writeServiceUuid: str,
		writeCharacteristicUuid: str,
		readServiceUuid: str,
		readCharacteristicUuid: str,
		onReceive: Callable[[bytes], None],
		ioThread: IoThread | None = None,
	) -> None:
		if isinstance(device, str):
			# String address provided - Bleak will perform implicit discovery
			address = device
			log.info(f"Connecting to BLE device at address {address}")
			self._client = bleak.BleakClient(address, winrt=WINRT_CLIENT_ARGS)
		else:
			# BLEDevice object provided (preferred)
			log.info(f"Connecting to {device.name} ({device.address})")
			self._client = bleak.BleakClient(device, winrt=WINRT_CLIENT_ARGS)
		self._writeServiceUuid = writeServiceUuid
		self._writeCharacteristicUuid = writeCharacteristicUuid
		self._readServiceUuid = readServiceUuid
		self._readCharacteristicUuid = readCharacteristicUuid
		self._onReceive = onReceive
		if ioThread is None:
			from .. import bgThread as ioThread
		self._ioThreadRef = weakref.ref(ioThread)
		self._queuedData = Queue()
		self._readEvent = Event()
		self._stopReaderEvent = Event()
		self._readerThread = Thread(
			target=queueReader,
			args=(self._queuedData, self._onReceive, self._stopReaderEvent, ioThread),
			daemon=True,
		)
		self._readerThread.start()
		f = runCoroutine(self._initAndConnect())
		f.result()
		if f.exception():
			raise f.exception()
		self.waitForConnection(CONNECT_TIMEOUT_SECONDS)

	async def _initAndConnect(self) -> None:
		await self._client.connect()
		# Listen for notifications
		await self._client.start_notify(self._readCharacteristicUuid, self._notifyReceive)

	def waitForRead(self, timeout: int | float) -> bool:
		"""Wait for data to be received from the peripheral."""
		self._readEvent.clear()
		return self._readEvent.wait(timeout)

	def write(self, data: bytes):
		"""Write data to the connected BLE peripheral.

		Data is automatically split into MTU-sized chunks if needed.

		:param data: The data to write to the peripheral.
		:raises RuntimeError: If not connected or service/characteristic not found.
		"""
		if not self._client.is_connected:
			raise RuntimeError("Not connected to peripheral")
		service = self._client.services.get_service(self._writeServiceUuid)
		if not service:
			raise RuntimeError(f"Service {self._writeServiceUuid} not found")
		characteristic = service.get_characteristic(self._writeCharacteristicUuid)
		if not characteristic:
			raise RuntimeError(f"Characteristic {self._writeCharacteristicUuid} not found")
		if _isDebug():
			log.debug(f"Write: {data!r}")

		# Split the data into chunks that fit within the MTU
		for s in sliced(data, characteristic.max_write_without_response_size):
			f = runCoroutine(
				self._client.write_gatt_char(characteristic, s, response=False),
			)
			f.result()
			if f.exception():
				raise f.exception()

	def close(self) -> None:
		"""Disconnect the BLE peripheral and release resources."""
		if _isDebug():
			log.debug("Closing BLE connection")
		if self._client.is_connected:
			runCoroutine(self._client.disconnect()).result()
		self._queuedData.join()
		self._stopReaderEvent.set()
		self._readerThread.join()

		self._onReceive = None

	def __del__(self):
		"""Ensure the BLE connection is closed before object destruction."""
		try:
			self.close()
		except AttributeError:
			if _isDebug():
				log.debugWarning("Couldn't delete object gracefully", exc_info=True)

	def isConnected(self) -> bool:
		"""Check if the BLE peripheral is currently connected."""
		return self._client.is_connected

	def waitForConnection(self, maxWait: int | float):
		"""Wait for connection and service discovery.

		:param maxWait: Maximum time to wait in seconds.
		:raises RuntimeError: If connection not established within maxWait.
		"""
		numTries = 0
		sleepTime = 0.1

		while (sleepTime * numTries) < maxWait:
			if _isDebug():
				services = [
					(
						s.uuid,
						s.description,
					)
					for s in self._client.services.services.values()
				]
				log.debug(
					f"Waiting for connection, {numTries} tries, "
					f"is connected {self.isConnected()}, services {services}",
				)
			if self._client.is_connected and len(self._client.services.services) > 0:
				return
			time.sleep(sleepTime)
			numTries += 1
		raise RuntimeError("Connection timed out")

	def _notifyReceive(self, _char: BleakGATTCharacteristic, data: bytearray):
		if _isDebug():
			log.debug(f"Read: {data!r}")
		self._readEvent.set()
		self._queuedData.put(data)

	def read(self, num_bytes: int = 1) -> bytes:
		"""Not implemented for BLE.

		BLE communication uses a push model with notifications rather than polling reads.
		Data is received asynchronously via the onReceive callback provided during initialization.

		:raises NotImplementedError: Always, as BLE doesn't support synchronous reads
		"""
		raise NotImplementedError("BLE uses notification-based communication, not polling reads")
