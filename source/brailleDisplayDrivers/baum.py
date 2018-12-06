# -*- coding: UTF-8 -*-
#brailleDisplayDrivers/baum.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010-2017 NV Access Limited, Babbage B.V.

import time
from collections import OrderedDict
from cStringIO import StringIO
import braille
import inputCore
from logHandler import log
import brailleInput
import bdDetect
import hwIo

TIMEOUT = 0.2
BAUD_RATE = 19200

ESCAPE = "\x1b"

BAUM_DISPLAY_DATA = "\x01"
BAUM_CELL_COUNT = "\x01"
BAUM_REQUEST_INFO = "\x02"
BAUM_PROTOCOL_ONOFF = "\x15"
BAUM_COMMUNICATION_CHANNEL = "\x16"
BAUM_POWERDOWN = "\x17"
BAUM_ROUTING_KEYS = "\x22"
BAUM_DISPLAY_KEYS = "\x24"
BAUM_ROUTING_KEY = "\x27"
BAUM_BRAILLE_KEYS = "\x33"
BAUM_JOYSTICK_KEYS = "\x34"
BAUM_DEVICE_ID = "\x84"
BAUM_SERIAL_NUMBER = "\x8A"

BAUM_RSP_LENGTHS = {
	BAUM_CELL_COUNT: 1,
	BAUM_POWERDOWN: 1,
	BAUM_COMMUNICATION_CHANNEL: 1,
	BAUM_DISPLAY_KEYS: 1,
	BAUM_ROUTING_KEY: 1,
	BAUM_BRAILLE_KEYS: 2,
	BAUM_JOYSTICK_KEYS: 1,
	BAUM_DEVICE_ID: 16,
	BAUM_SERIAL_NUMBER: 8,
}

KEY_NAMES = {
	BAUM_ROUTING_KEYS: None,
	BAUM_ROUTING_KEY: None,
	BAUM_DISPLAY_KEYS: ("d1", "d2", "d3", "d4", "d5", "d6"),
	BAUM_BRAILLE_KEYS: ("b9", "b10", "b11", None, "c1", "c2", "c3", "c4", # byte 1
		"b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8"), # byte 2
	BAUM_JOYSTICK_KEYS: ("up", "left", "down", "right", "select"),
}

class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	name = "baum"
	# Translators: Names of braille displays.
	description = _("Baum/HumanWare/APH/Orbit braille displays")
	isThreadSafe = True

	@classmethod
	def getManualPorts(cls):
		return braille.getSerialPorts()

	def __init__(self, port="auto"):
		super(BrailleDisplayDriver, self).__init__()
		self.numCells = 0
		self._deviceID = None

		for portType, portId, port, portInfo in self._getTryPorts(port):
			# At this point, a port bound to this display has been found.
			# Try talking to the display.
			self.isHid = portType == bdDetect.KEY_HID
			try:
				if self.isHid:
					self._dev = hwIo.Hid(port, onReceive=self._onReceive)
				else:
					self._dev = hwIo.Serial(port, baudrate=BAUD_RATE, timeout=TIMEOUT, writeTimeout=TIMEOUT, onReceive=self._onReceive)
			except EnvironmentError:
				log.debugWarning("", exc_info=True)
				continue
			if self.isHid:
				try:
					# It's essential to send protocol on for the Orbit Reader 20.
					self._sendRequest(BAUM_PROTOCOL_ONOFF, True)
				except EnvironmentError:
					# Pronto! and VarioUltra don't support BAUM_PROTOCOL_ONOFF.
					pass
				# Explicitly request device info.
				# Even where it's supported, BAUM_PROTOCOL_ONOFF doesn't always return device info.
				self._sendRequest(BAUM_REQUEST_INFO, 0)
			else: # Serial
				# If the protocol is already on, sending protocol on won't return anything.
				# First ensure it's off.
				self._sendRequest(BAUM_PROTOCOL_ONOFF, False)
				# This will cause the device id, serial number and number of cells to be returned.
				self._sendRequest(BAUM_PROTOCOL_ONOFF, True)
				# Send again in case the display misses the first one.
				self._sendRequest(BAUM_PROTOCOL_ONOFF, True)
			for i in xrange(3):
				# An expected response hasn't arrived yet, so wait for it.
				self._dev.waitForRead(TIMEOUT)
				if self.numCells and self._deviceID:
					break
			if self.numCells:
				# A display responded.
				log.info("Found {device} connected via {type} ({port})".format(
					device=self._deviceID, type=portType, port=port))
				break
			self._dev.close()

		else:
			raise RuntimeError("No Baum display found")

		self._keysDown = {}
		self._ignoreKeyReleases = False

	def terminate(self):
		try:
			super(BrailleDisplayDriver, self).terminate()
			try:
				self._sendRequest(BAUM_PROTOCOL_ONOFF, False)
			except EnvironmentError:
				# Some displays don't support BAUM_PROTOCOL_ONOFF.
				pass
		finally:
			# Make sure the device gets closed.
			# If it doesn't, we may not be able to re-open it later.
			self._dev.close()

	def _sendRequest(self, command, arg=""):
		if isinstance(arg, (int, bool)):
			arg = chr(arg)
		if self.isHid:
			self._dev.write(command + arg)
		else:
			self._dev.write("\x1b{command}{arg}".format(command=command,
				arg=arg.replace(ESCAPE, ESCAPE * 2)))

	def _onReceive(self, data):
		if self.isHid:
			# data contains the entire packet.
			stream = StringIO(data)
		else:
			if data != ESCAPE:
				log.debugWarning("Ignoring byte before escape: %r" % data)
				return
			# data only contained the escape. Read the rest from the device.
			stream = self._dev
		command = stream.read(1)
		length = BAUM_RSP_LENGTHS.get(command, 0)
		if command == BAUM_ROUTING_KEYS:
			length = 10 if self.numCells > 40 else 5
		arg = stream.read(length)
		if command == BAUM_DEVICE_ID and arg == "Refreshabraille ":
			# For most Baum devices, the argument is 16 bytes,
			# but it is 18 bytes for the Refreshabraille.
			arg += stream.read(2)
		self._handleResponse(command, arg)

	def _handleResponse(self, command, arg):
		if command == BAUM_CELL_COUNT:
			self.numCells = ord(arg)
		elif command == BAUM_DEVICE_ID:
			# Short ids can be padded with either nulls or spaces.
			self._deviceID = arg.rstrip("\0 ")
		elif command in KEY_NAMES:
			arg = sum(ord(byte) << offset * 8 for offset, byte in enumerate(arg))
			if arg < self._keysDown.get(command, 0):
				# Release.
				if not self._ignoreKeyReleases:
					# The first key released executes the key combination.
					try:
						inputCore.manager.executeGesture(InputGesture(self._deviceID, self._keysDown))
					except inputCore.NoInputGestureAction:
						pass
					# Any further releases are just the rest of the keys in the combination being released,
					# so they should be ignored.
					self._ignoreKeyReleases = True
			else:
				# Press.
				# This begins a new key combination.
				self._ignoreKeyReleases = False
			if arg > 0:
				self._keysDown[command] = arg
			elif command in self._keysDown:
				# All keys in this group have been released.
				# #3541: Remove this group so it doesn't count as a group with keys down.
				del self._keysDown[command]

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

	def __init__(self, model, keysDown):
		super(InputGesture, self).__init__()
		# Model identifiers should not contain spaces.
		if model:
			self.model = model.replace(" ", "")
			assert(self.model.isalnum())
		self.keysDown = dict(keysDown)

		self.keyNames = names = []
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
						names.append("routing")
						break
			elif group == BAUM_ROUTING_KEY:
				self.routingIndex = groupKeysDown - 1
				names.append("routing")
			else:
				for index, name in enumerate(KEY_NAMES[group]):
					if groupKeysDown & (1 << index):
						names.append(name)

		self.id = "+".join(names)
