# -*- coding: UTF-8 -*-
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017 NV Access Limited, Coscell Kao, Babbage B.V.
from typing import List

import serial
import braille
import hwIo
from hwIo import intToByte
import time
import inputCore
from logHandler import log

BAUD_RATE = 9600
TIMEOUT = 0.5

# Tags sent by the SuperBraille
# Sent to identify the display and receive amount of cells this unit has
DESCRIBE_TAG = b"\xff\xff\x0a"
# Sent to request displaying of cells
DISPLAY_TAG = b"\xff\xff\x04\x00\x99\x00\x50\x00"

class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	name = "superBrl"
	# Translators: Names of braille displays.
	description = _("SuperBraille")
	isThreadSafe=True

	@classmethod
	def getManualPorts(cls):
		return braille.getSerialPorts()

	def __init__(self,port="Auto"):
		super(BrailleDisplayDriver, self).__init__()
		for portType, portId, port, portInfo in self._getTryPorts(port):
			try:
				self._dev = hwIo.Serial(port, baudrate=BAUD_RATE, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, timeout=TIMEOUT, writeTimeout=TIMEOUT, onReceive=self._onReceive)
			except EnvironmentError:
				log.debugWarning("", exc_info=True)
				continue

			# try to initialize the device and request number of cells
			self._dev.write(DESCRIBE_TAG)
			self._dev.waitForRead(TIMEOUT)
			# Check for cell information
			if self.numCells:
				# ok, it is a SuperBraille
				log.info("Found superBraille device, version %s"%self.version)
				break
			else:
				self._dev.close()
		else:
			raise RuntimeError("No SuperBraille found")

	def terminate(self):
		try:
			super(BrailleDisplayDriver, self).terminate()
		finally:
			# We must sleep before closing the COM port as not doing this can leave the display in a bad state where it can not be re-initialized
			time.sleep(TIMEOUT)
			self._dev.close()
			self._dev = None

	def _onReceive(self, data: bytes):
		# The only info this display ever sends is number of cells and the display version.
		# It sends 0x00, 0x05, number of cells, then version string of 8 bytes.
		if data != b'\x00':
			return
		data=self._dev.read(1)
		if data!= b'\x05':
			return
		self.numCells = ord(self._dev.read(1))
		self._dev.read(1)
		self.version=self._dev.read(8)

	def display(self, cells: List[int]):
		writeBytes: List[bytes] = [DISPLAY_TAG, ]
		for cell in cells:
			writeBytes.append(b"\x00")
			writeBytes.append(intToByte(cell))
		self._dev.write(b"".join(writeBytes))

	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"braille_scrollBack": ("kb:numpadMinus",),
			"braille_scrollForward": ("kb:numpadPlus",),
		},
	})

