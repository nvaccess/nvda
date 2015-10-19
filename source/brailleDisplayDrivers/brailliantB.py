#brailleDisplayDrivers/brailliantB.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2012-2015 NV Access Limited

import os
import time
import _winreg
import itertools
import wx
import serial
import hwPortUtils
import braille
import inputCore
from logHandler import log
import brailleInput

TIMEOUT = 0.2
BAUD_RATE = 115200
PARITY = serial.PARITY_EVEN
READ_INTERVAL = 50

HEADER = "\x1b"
MSG_INIT = "\x00"
MSG_INIT_RESP = "\x01"
MSG_DISPLAY = "\x02"
MSG_KEY_DOWN = "\x05"
MSG_KEY_UP = "\x06"

KEY_NAMES = {
	# Braille keyboard.
	2: "dot1",
	3: "dot2",
	4: "dot3",
	5: "dot4",
	6: "dot5",
	7: "dot6",
	8: "dot7",
	9: "dot8",
	10: "space",
	# Command keys.
	11: "c1",
	12: "c2",
	13: "c3",
	14: "c4",
	15: "c5",
	16: "c6",
	# Thumb keys.
	17: "up",
	18: "left",
	19: "right",
	20: "down",
}
FIRST_ROUTING_KEY = 80
DOT1_KEY = 2
DOT8_KEY = 9
SPACE_KEY = 10

def _getPorts():
	# USB.
	try:
		rootKey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Enum\USB\Vid_1c71&Pid_c005")
	except WindowsError:
		# A display has never been connected via USB.
		pass
	else:
		with rootKey:
			for index in itertools.count():
				try:
					keyName = _winreg.EnumKey(rootKey, index)
				except WindowsError:
					break
				try:
					with _winreg.OpenKey(rootKey, os.path.join(keyName, "Device Parameters")) as paramsKey:
						yield "USB", _winreg.QueryValueEx(paramsKey, "PortName")[0]
				except WindowsError:
					continue

	# Bluetooth.
	for portInfo in hwPortUtils.listComPorts(onlyAvailable=True):
		try:
			btName = portInfo["bluetoothName"]
		except KeyError:
			continue
		if btName.startswith("Brailliant B") or btName == "Brailliant 80":
			yield "bluetooth", portInfo["port"]

class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	name = "brailliantB"
	# Translators: The name of a series of braille displays.
	description = _("HumanWare Brailliant BI/B series")

	@classmethod
	def check(cls):
		try:
			next(_getPorts())
		except StopIteration:
			# No possible ports found.
			return False
		return True

	def __init__(self):
		super(BrailleDisplayDriver, self).__init__()
		self.numCells = 0

		for portType, port in _getPorts():
			# Try talking to the display.
			try:
				self._ser = serial.Serial(port, baudrate=BAUD_RATE, parity=PARITY, timeout=TIMEOUT, writeTimeout=TIMEOUT)
			except serial.SerialException:
				continue
			# This will cause the number of cells to be returned.
			self._sendMessage(MSG_INIT)
			# #5406: With the new USB driver, the first command is ignored after a reconnection.
			# Worse, if we don't receive a reply,
			# _handleResponses freezes for some reason despite the timeout.
			# Send the init message again just in case.
			self._sendMessage(MSG_INIT)
			self._handleResponses(wait=True)
			if not self.numCells:
				# HACK: When connected via bluetooth, the display sometimes reports communication not allowed on the first attempt.
				self._sendMessage(MSG_INIT)
				self._handleResponses(wait=True)
			if self.numCells:
				# A display responded.
				log.info("Found display with {cells} cells connected via {type} ({port})".format(
					cells=self.numCells, type=portType, port=port))
				break

		else:
			raise RuntimeError("No display found")

		self._readTimer = wx.PyTimer(self._handleResponses)
		self._readTimer.Start(READ_INTERVAL)
		self._keysDown = set()
		self._ignoreKeyReleases = False

	def terminate(self):
		try:
			super(BrailleDisplayDriver, self).terminate()
			self._readTimer.Stop()
			self._readTimer = None
		finally:
			# We absolutely must close the Serial object, as it does not have a destructor.
			# If we don't, we won't be able to re-open it later.
			self._ser.close()

	def _sendMessage(self, msgId, payload=""):
		if isinstance(payload, (int, bool)):
			payload = chr(payload)
		self._ser.write("{header}{id}{length}{payload}".format(
			header=HEADER, id=msgId,
			length=chr(len(payload)), payload=payload))

	def _handleResponses(self, wait=False):
		while wait or self._ser.inWaiting():
			msgId, payload = self._readPacket()
			if msgId:
				self._handleResponse(msgId, payload)
			wait = False

	def _readPacket(self):
		# Wait for the header.
		while True:
			char = self._ser.read(1)
			if char == HEADER:
				break
		msgId = self._ser.read(1)
		length = ord(self._ser.read(1))
		payload = self._ser.read(length)
		return msgId, payload

	def _handleResponse(self, msgId, payload):
		if msgId == MSG_INIT_RESP:
			if ord(payload[0]) != 0:
				# Communication not allowed.
				log.debugWarning("Display at %r reports communication not allowed" % self._ser.port)
				return
			self.numCells = ord(payload[2])

		elif msgId == MSG_KEY_DOWN:
			payload = ord(payload)
			self._keysDown.add(payload)
			# This begins a new key combination.
			self._ignoreKeyReleases = False

		elif msgId == MSG_KEY_UP:
			payload = ord(payload)
			if not self._ignoreKeyReleases and self._keysDown:
				try:
					inputCore.manager.executeGesture(InputGesture(self._keysDown))
				except inputCore.NoInputGestureAction:
					pass
				# Any further releases are just the rest of the keys in the combination being released,
				# so they should be ignored.
				self._ignoreKeyReleases = True
			self._keysDown.discard(payload)

		else:
			log.debugWarning("Unknown message: id {id!r}, payload {payload!r}".format(id=msgId, payload=payload))

	def display(self, cells):
		# cells will already be padded up to numCells.
		self._sendMessage(MSG_DISPLAY, "".join(chr(cell) for cell in cells))

	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"braille_scrollBack": ("br(brailliantB):left",),
			"braille_scrollForward": ("br(brailliantB):right",),
			"braille_previousLine": ("br(brailliantB):up",),
			"braille_nextLine": ("br(brailliantB):down",),
			"braille_routeTo": ("br(brailliantB):routing",),
			"braille_toggleTether": ("br(brailliantB):up+down",),
			"kb:upArrow": ("br(brailliantB):space+dot1",),
			"kb:downArrow": ("br(brailliantB):space+dot4",),
			"kb:leftArrow": ("br(brailliantB):space+dot3",),
			"kb:rightArrow": ("br(brailliantB):space+dot6",),
			"showGui": ("br(brailliantB):c1+c3+c4+c5",),
			"kb:shift+tab": ("br(brailliantB):space+dot1+dot3",),
			"kb:tab": ("br(brailliantB):space+dot4+dot6",),
			"kb:alt": ("br(brailliantB):space+dot1+dot3+dot4",),
			"kb:escape": ("br(brailliantB):space+dot1+dot5",),
			"kb:enter": ("br(brailliantB):dot8",),
			"kb:windows+d": ("br(brailliantB):c1+c4+c5",),
			"kb:windows": ("br(brailliantB):space+dot3+dot4",),
			"kb:alt+tab": ("br(brailliantB):space+dot2+dot3+dot4+dot5",),
			"sayAll": ("br(brailliantB):c1+c2+c3+c4+c5+c6",),
		},
	})

class InputGesture(braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture):

	source = BrailleDisplayDriver.name

	def __init__(self, keys):
		super(InputGesture, self).__init__()
		self.keyCodes = set(keys)

		self.keyNames = names = set()
		isBrailleInput = True
		for key in self.keyCodes:
			if isBrailleInput:
				if DOT1_KEY <= key <= DOT8_KEY:
					self.dots |= 1 << (key - DOT1_KEY)
				elif key == SPACE_KEY:
					self.space = True
				else:
					# This is not braille input.
					isBrailleInput = False
					self.dots = 0
					self.space = False
			if key >= FIRST_ROUTING_KEY:
				names.add("routing")
				self.routingIndex = key - FIRST_ROUTING_KEY
			else:
				try:
					names.add(KEY_NAMES[key])
				except KeyError:
					log.debugWarning("Unknown key with id %d" % key)

		self.id = "+".join(names)
