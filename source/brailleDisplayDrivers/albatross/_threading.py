# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023 NV Access Limited, Burman's Computer and Education Ltd.

"""Threads for Tivomatic Caiku Albatross braille display driver.
Classes:
- L{ReadThread}; manages reconnection retries and works as a trigger
for read operations excluding initial connection establishment
- L{RepeatedTimer}; timer to check periodically if data needs to be sent
to display to keep connection. If display gets nothing within approximately
2 seconds, it falls back to "wait for connection" state.
"""

import ctypes
import serial

from ctypes import byref
from ctypes.wintypes import DWORD
from logHandler import log
from serial.win32 import (
	ERROR_IO_PENDING,
	EV_RXCHAR,
	GetLastError,
	SetCommMask,
)
from threading import (
	Event,
	Thread,
	Timer,
)
from typing import Callable

from .constants import KC_INTERVAL


class ReadThread(Thread):
	"""Controls most of read operations and tries to reconnect when needed."""

	def __init__(
			self,
			readFunction: Callable[[], None],
			disableFunction: Callable[[], None],
			event: Event,
			dev: serial.Serial,
			*args,
			**kwargs
	):
		"""Constructor.
		@param readFunction: Handles read operations and reconnection.
		@param disableFunction: Called on connection failure.
		@param event: Exit thread when set.
		@param dev: Port object.
		"""
		super().__init__(*args, **kwargs)
		self._readFunction = readFunction
		self._disableFunction = disableFunction
		self._event = event
		self._dev = dev

	def run(self):
		data = dwEvtMask = DWORD()
		log.debug(f"{self.name} started")
		while not self._event.isSet():
			# Try to reconnect if port is not open
			if not self._dev.is_open:
				log.debug(
					f"Calling {self._readFunction.__name__}, port {self._dev.name} not open"
				)
				self._readFunction()
				if not self._dev.is_open:
					log.debug(
						f"Sleepin {KC_INTERVAL} seconds, port {self._dev.name} not open"
					)
					self._event.wait(KC_INTERVAL)
					continue
			# If any of I/O function fails, it should not crash the thread.
			try:
				if not SetCommMask(self._dev._port_handle, EV_RXCHAR):
					# Exiting
					if self._event.isSet():
						break
					self._disableFunction()
					log.debug("SetCommMask failed")
					continue
				result = ctypes.windll.kernel32.WaitCommEvent(
					self._dev._port_handle,
					byref(dwEvtMask),
					byref(self._dev._overlapped_read)
				)
				if not result and GetLastError() != ERROR_IO_PENDING:
					if self._event.isSet():
						break
					self._disableFunction()
					log.debug("WaitCommEvent failed")
					continue
				result = ctypes.windll.kernel32.GetOverlappedResult(
					self._dev._port_handle,
					byref(self._dev._overlapped_read),
					byref(data),
					True
				)
				if result:
					log.debug(f"Calling function {self._readFunction.__name__} for read")
					self._readFunction()
				else:
					if self._event.isSet():
						break
					log.debug(f"GetOverLappedResult failed {ctypes.WinError()}")
					self._disableFunction()
			# Considering situation where "albatross_read" thread is about to read
			# but writing to display fails during it - or vice versa - AttributeError
			# or TypeError might raise.
			except (OSError, AttributeError, TypeError):
				if self._event.isSet():
					break
				else:
					self._disableFunction()
					log.debug("", exc_info=True)
		log.debug(f"Exiting {self.name}")


class RepeatedTimer:
	"""Repeating timer.
	Timer is used to check if data needs to be sent to display to keep
	connected.
	"""

	def __init__(
			self,
			interval: float,
			feedFunction: Callable[[], None]
	):
		"""Constructor.
		@param interval: Checking frequency
		@param feedFunction: feeds display with data if needed
		"""
		self._interval = interval
		self._timer = Timer(self._interval, self._run)
		self._feedFunction = feedFunction
		self.is_running = False
		self.start()

	def _run(self):
		self.is_running = False
		self.start()
		self._feedFunction()

	def start(self):
		if not self.is_running:
			self._timer = Timer(self._interval, self._run)
			self._timer.start()
			self.is_running = True

	def stop(self):
		self._timer.cancel()
		self.is_running = False
