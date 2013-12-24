# -*- coding: UTF-8 -*-
#brailleDisplayDrivers/baum.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010-2013 NV Access Limited

import os
import time
from collections import OrderedDict
import _winreg
import itertools
import wx
import serial
import braille
import inputCore
from logHandler import log
import brailleInput
import bdDetect

TIMEOUT = 0.2
BAUD_RATE = 19200
READ_INTERVAL = 50

ESCAPE = "\x1b"

BAUM_DISPLAY_DATA = "\x01"
BAUM_CELL_COUNT = "\x01"
BAUM_PROTOCOL_ONOFF = "\x15"
BAUM_COMMUNICATION_CHANNEL = "\x16"
BAUM_POWERDOWN = "\x17"
BAUM_ROUTING_KEYS = "\x22"
BAUM_DISPLAY_KEYS = "\x24"
BAUM_BRAILLE_KEYS = "\x33"
BAUM_JOYSTICK_KEYS = "\x34"
BAUM_DEVICE_ID = "\x84"
BAUM_SERIAL_NUMBER = "\x8A"

BAUM_RSP_LENGTHS = {
	BAUM_CELL_COUNT: 1,
	BAUM_POWERDOWN: 1,
	BAUM_COMMUNICATION_CHANNEL: 1,
	BAUM_DISPLAY_KEYS: 1,
	BAUM_BRAILLE_KEYS: 2,
	BAUM_JOYSTICK_KEYS: 1,
	BAUM_DEVICE_ID: 16,
	BAUM_SERIAL_NUMBER: 8,
}

KEY_NAMES = {
	BAUM_ROUTING_KEYS: None,
	BAUM_DISPLAY_KEYS: ("d1", "d2", "d3", "d4", "d5", "d6"),
	BAUM_BRAILLE_KEYS: ("b9", "b10", "b11", None, "c1", "c2", "c3", "c4", # byte 1
		"b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8"), # byte 2
	BAUM_JOYSTICK_KEYS: ("up", "left", "down", "right", "select"),
}

class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	name = "baum"
	# Translators: Names of braille displays.
	description = _("Baum/HumanWare/APH braille displays")

	@classmethod
	def check(cls):
		return (bdDetect.arePossibleDevicesForDriver(cls.name)
			or bool(cls.getManualPorts()))

	@classmethod
	def getManualPorts(cls):
		return braille.getSerialPorts()

	@classmethod
	def _getUsbPorts(cls, usbIds=None):
		if not usbIds:
			usbIds = bdDetect.getConnectedUsbDevicesForDriver(cls.name)
		try:
			rootKey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Enum\FTDIBUS")
		except WindowsError:
			return
		with rootKey:
			for index in itertools.count():
				try:
					keyName = _winreg.EnumKey(rootKey, index)
				except WindowsError:
					break
				usbId = "&".join(keyName.split("+", 2)[:2])
				if usbId not in usbIds:
					continue
				try:
					with _winreg.OpenKey(rootKey, os.path.join(keyName, "0000", "Device Parameters")) as paramsKey:
						yield _winreg.QueryValueEx(paramsKey, "PortName")[0]
				except WindowsError:
					continue

	def __init__(self, port=None):
		super(BrailleDisplayDriver, self).__init__()
		self.numCells = 0
		self._deviceID = None

		if isinstance(port, bdDetect.UsbDeviceMatch):
			tryPorts = ((p, "USB") for p in self._getUsbPorts(usbIds=(port.id,)))
		elif isinstance(port, bdDetect.BluetoothComPortMatch):
			tryPorts = ((port.port, "Bluetooth"),)
		else:
			tryPorts = ((port, "serial"),)
		for port, portType in tryPorts:
			# At this point, a port bound to this display has been found.
			# Try talking to the display.
			try:
				self._ser = serial.Serial(port, baudrate=BAUD_RATE, timeout=TIMEOUT, writeTimeout=TIMEOUT)
			except serial.SerialException:
				continue
			# This will cause the number of cells to be returned.
			self._sendRequest(BAUM_DISPLAY_DATA)
			# Send again in case the display misses the first one.
			self._sendRequest(BAUM_DISPLAY_DATA)
			# We just sent less bytes than we should,
			# so we need to send another request in order for the display to know the previous request is finished.
			self._sendRequest(BAUM_DEVICE_ID)
			self._handleResponses(wait=True)
			if self.numCells:
				# A display responded.
				if not self._deviceID:
					# Bah. The response to our device ID query hasn't arrived yet, so wait for it.
					self._handleResponses(wait=True)
				log.info("Found {device} connected via {type} ({port})".format(
					device=self._deviceID, type=portType, port=port))
				break

		else:
			raise RuntimeError("No Baum display found")

		self._readTimer = wx.PyTimer(self._handleResponses)
		self._readTimer.Start(READ_INTERVAL)
		self._keysDown = {}
		self._ignoreKeyReleases = False

	def terminate(self):
		try:
			super(BrailleDisplayDriver, self).terminate()
			self._readTimer.Stop()
			self._readTimer = None
			self._sendRequest(BAUM_PROTOCOL_ONOFF, False)
		finally:
			# We absolutely must close the Serial object, as it does not have a destructor.
			# If we don't, we won't be able to re-open it later.
			self._ser.close()

	def _sendRequest(self, command, arg=""):
		if isinstance(arg, (int, bool)):
			arg = chr(arg)
		self._ser.write("\x1b{command}{arg}".format(command=command,
			arg=arg.replace(ESCAPE, ESCAPE * 2)))

	def _handleResponses(self, wait=False):
		while wait or self._ser.inWaiting():
			command, arg = self._readPacket()
			if command:
				self._handleResponse(command, arg)
			wait = False

	def _readPacket(self):
		# Find the escape.
		chars = []
		escapeFound = False
		while True:
			char = self._ser.read(1)
			if char == ESCAPE:
				escapeFound = True
				break
			else:
				chars.append(char)
			if not self._ser.inWaiting():
				break
		if chars:
			log.debugWarning("Ignoring data before escape: %r" % "".join(chars))
		if not escapeFound:
			return None, None

		command = self._ser.read(1)
		length = BAUM_RSP_LENGTHS.get(command, 0)
		if command == BAUM_ROUTING_KEYS:
			length = 10 if self.numCells > 40 else 5
		arg = self._ser.read(length)
		return command, arg

	def _handleResponse(self, command, arg):
		if command == BAUM_CELL_COUNT:
			self.numCells = ord(arg)
		elif command == BAUM_DEVICE_ID:
			self._deviceID = arg

		elif command in KEY_NAMES:
			arg = sum(ord(byte) << offset * 8 for offset, byte in enumerate(arg))
			if arg < self._keysDown.get(command, 0):
				# Release.
				if not self._ignoreKeyReleases:
					# The first key released executes the key combination.
					try:
						inputCore.manager.executeGesture(InputGesture(self._keysDown))
					except inputCore.NoInputGestureAction:
						pass
					# Any further releases are just the rest of the keys in the combination being released,
					# so they should be ignored.
					self._ignoreKeyReleases = True
			else:
				# Press.
				# This begins a new key combination.
				self._ignoreKeyReleases = False
			self._keysDown[command] = arg

		elif command == BAUM_POWERDOWN:
			log.debug("Power down")
		elif command in (BAUM_COMMUNICATION_CHANNEL, BAUM_SERIAL_NUMBER):
			pass

		else:
			log.debugWarning("Unknown command {command!r}, arg {arg!r}".format(command=command, arg=arg))

	def display(self, cells):
		# cells will already be padded up to numCells.
		self._sendRequest(BAUM_DISPLAY_DATA, "".join(chr(cell) for cell in cells))

	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"braille_scrollBack": ("br(baum):d2",),
			"braille_scrollForward": ("br(baum):d5",),
			"braille_previousLine": ("br(baum):d1",),
			"braille_nextLine": ("br(baum):d3",),
			"braille_routeTo": ("br(baum):routing",),
			"kb:upArrow": ("br(baum):up",),
			"kb:downArrow": ("br(baum):down",),
			"kb:leftArrow": ("br(baum):left",),
			"kb:rightArrow": ("br(baum):right",),
			"kb:enter": ("br(baum):select",),
		},
	})

class InputGesture(braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture):

	source = BrailleDisplayDriver.name

	def __init__(self, keysDown):
		super(InputGesture, self).__init__()
		self.keysDown = dict(keysDown)

		self.keyNames = names = set()
		for group, groupKeysDown in keysDown.iteritems():
			if group == BAUM_BRAILLE_KEYS and len(keysDown) == 1 and not groupKeysDown & 0xfc:
				# This is braille input.
				# 0xfc covers command keys. The space bars are covered by 0x3.
				self.dots = groupKeysDown >> 8
				self.space = groupKeysDown & 0x3
			if group == BAUM_ROUTING_KEYS:
				for index in xrange(braille.handler.display.numCells):
					if groupKeysDown & (1 << index):
						self.routingIndex = index
						names.add("routing")
						break
			else:
				for index, name in enumerate(KEY_NAMES[group]):
					if groupKeysDown & (1 << index):
						names.add(name)

		self.id = "+".join(names)
