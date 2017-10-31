# -*- coding: UTF-8 -*-
#brailleDisplayDrivers/hims.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010-2017 Gianluca Casalino, NV Access Limited, Babbage B.V., Leonard de Ruijter, Bram Duvigneau

import _winreg
import serial
from cStringIO import StringIO
import itertools
import os
import hwPortUtils
import hwIo
import braille
from logHandler import log
from collections import OrderedDict
import inputCore
import brailleInput
from baseObject import AutoPropertyObject

TIMEOUT = 0.2
BAUD_RATE = 115200
PARITY = serial.PARITY_NONE

class Model(AutoPropertyObject):
	# Two bytes device identifier, used in the protocol to identify the device
	deviceId = None
	# user readable name for the device
	name = ""
	numCells = 0 #0 means undefined, needs to be requested for

	def __init__(self, display):
		self._display = display

	def _get_keys(self):
		"""Basic keymap

		This returns a basic keymap with sensible defaults for all devices.
		Subclasses should override or extend this method to add model specific keys, 
		or relabel keys. Even if a key isn't available on all devices, add it here
		if it would make sense for most devices.

		The Hims protocol uses a 4 bytes value for key identification.
		Bit shifting is used to make clear what byte is used for what key.
		For example: 0x001 represents a key code that will be received in the first byte,
		0x001<<8 represents a key code that will be received in the second byte, etc.
		"""
		return OrderedDict({
			# Braille keyboard, not used for SyncBraille
			0x01:"dot1",
			0x02:"dot2",
			0x04:"dot3",
			0x08:"dot4",
			0x10:"dot5",
			0x20:"dot6",
			0x40:"dot7",
			0x80:"dot8",
			0x01<<8: "space",
			0x02<<8: "f1",
			0x04<<8: "f2",
			0x08<<8: "f3",
			0x10<<8: "f4"
		})

class BrailleSense(Model):
	name = "Braille Sense"
	usbId = "VID_045E&PID_930A"
	bluetoothPrefix = "BrailleSense"
	numCells = 0 # Either 18 or 32

class BrailleEdge(Model):
	deviceId="\x42\x45" # BE
	name = "Braille Edge"
	usbId = "VID_045E&PID_930B"
	bluetoothPrefix = "BrailleEDGE"
	numCells = 40

	def _get_keys(self):
		keys = super(BrailleEdge, self)._get_keys()
		keys.update({
			0x01<<16: "leftScrollUp",
			0x02<<16: "rightScrollUp",
			0x04<<16: "rightScrollDown",
			0x08<<16: "leftScrollDown",
			0x10<<16: "f5",
			0x20<<16: "f6",
			0x40<<16: "f7",
			0x80<<16: "f8",
			0x01<<24: "leftUpArrow",
			0x02<<24: "leftDownArrow",
			0x04<<24: "leftLeftArrow",
			0x08<<24: "leftRightArrow",
			0x10<<24: "rightUpArrow",
			0x20<<24: "rightDownArrow",
			0x40<<24: "rightLeftArrow",
			0x80<<24: "rightRightArrow",
		})
		return keys

class BrailleSense2S(BrailleSense):
	"""Braille Sense with one scroll key on both sides.
	Also referred to as Braille Sense Classic."""

	name = "Braille Sense"
	deviceId="\x42\x53" # BS

	def _get_keys(self):
		keys = super(BrailleSense2S, self)._get_keys()
		keys.update({
			0x20<<8: "leftScroll",
			0x40<<8: "rightScroll",
		})
		return keys

class BrailleSense4S(BrailleSense):
	deviceId="\x4c\x58" # LX

	def _get_keys(self):
		keys = super(BrailleSense4S, self)._get_keys()
		keys.update({
			0x01<<16: "leftScrollUp",
			0x02<<16: "leftScrollDown",
			0x04<<16: "rightScrollUp",
			0x08<<16: "rightScrollDown",
		})
		return keys

class SmartBeetle(BrailleSense4S):
	"""Subclass for Smart Beetle device, which has the same identifier as the Braille Sense with 4 scroll keys.
	However, it is distinguishable by the number of cells.
	Furthermore, the key codes for f2 and f4 are swapped, and it has only two scroll keys.
	"""
	numCells=14
	bluetoothPrefix = "SmartBeetle"
	name = "Smart Beetle"

	def _get_keys(self):
		keys = Model._get_keys(self)
		keys.update({
			0x04<<8: "f4",
			0x10<<8: "f2",
			0x04<<16: "leftScroll",
			0x08<<16: "rightScroll",
			# Once in a while, a Beetle sends the wrong key codes for left and right scroll.
			0x20<<8: "leftScroll",
			0x40<<8: "rightScroll",
		})
		return keys

class BrailleSenseQ(BrailleSense4S):
	deviceId="\x51\x58" # QX
	name = "Braille Sense QWERTY"
	numCells = 32

class BrailleSenseQX(BrailleSenseQ):
	"""Special identifier to support QWERTY input"""
	deviceId="\x53\x58" # SX

class SyncBraille(Model):
	name = "SyncBraille"
	usbId = "VID_0403&PID_6001"

	def _get_keys(self):
		return OrderedDict({
			0x10<<8: "leftScrollUp",
			0x20<<8: "rightScrollUp",
			0x40<<8: "rightScrollDown",
			0x80<<8: "leftScrollDown",
		})

modelMap = [(cls.deviceId,cls) for cls in (
	# The order of models in this list is important, as some models can simulate other models.
	# For example, the Braille Edge can report itself as a Braille Sense Classic
	BrailleSenseQX,
	BrailleSenseQ,
	BrailleEdge,
	SmartBeetle,
	BrailleSense4S,
	BrailleSense2S,
)]

USB_IDS_BULK={BrailleEdge.usbId,BrailleSense.usbId}

bluetoothPrefixes={modelCls.bluetoothPrefix for id, modelCls in modelMap if modelCls.bluetoothPrefix}

class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	name = "hims"
	# Translators: The name of a series of braille displays.
	description = _("HIMS Braille Sense/Braille EDGE/Smart Beetle/Sync Braille series")
	isThreadSafe = True

	@classmethod
	def check(cls):
		return True

	@classmethod
	def getPossiblePorts(cls):
		ports = OrderedDict()
		comPorts = list(hwPortUtils.listComPorts(onlyAvailable=True))
		try:
			next(cls._getAutoPorts(comPorts))
			ports.update((cls.AUTOMATIC_PORT,))
		except StopIteration:
			pass
		for portInfo in comPorts:
			# Translators: Name of a serial communications port.
			ports[portInfo["port"]] = _("Serial: {portName}").format(portName=portInfo["friendlyName"])
		return ports

	@classmethod
	def _getAutoPorts(cls, comPorts):
		# USB bulk
		for bulkId in USB_IDS_BULK:
			portType = "USB bulk"
			try:
				rootKey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Enum\USB\%s"%bulkId)
			except WindowsError:
				continue
			else:
				with rootKey:
					for index in itertools.count():
						try:
							keyName = _winreg.EnumKey(rootKey, index)
						except WindowsError:
							break
						try:
							with _winreg.OpenKey(rootKey, os.path.join(keyName, "Device Parameters")) as paramsKey:
								yield _winreg.QueryValueEx(paramsKey, "SymbolicName")[0], portType, bulkId
						except WindowsError:
							continue
		# Try bluetooth ports last.
		for portInfo in sorted(comPorts, key=lambda item: "bluetoothName" in item):
			port = portInfo["port"]
			hwID = portInfo["hardwareID"]
			if hwID.startswith(r"FTDIBUS\COMPORT"):
				# USB.
				portType = "USB serial"
				try:
					usbID = hwID.split("&", 1)[1]
				except IndexError:
					continue
				if usbID is not SyncBraille.usbId:
					continue
				yield portInfo['port'], portType, usbID
			elif "bluetoothName" in portInfo:
				# Bluetooth.
				portType = "bluetooth"
				btName = portInfo["bluetoothName"]
				for prefix in bluetoothPrefixes:
					if btName.startswith(prefix):
						btPrefix=prefix
						break
				else:
					btPrefix = None
				yield portInfo['port'], portType, btPrefix

	def __init__(self, port="auto"):
		super(BrailleDisplayDriver, self).__init__()
		self.numCells = 0
		self._model = None
		if port == "auto":
			tryPorts = self._getAutoPorts(hwPortUtils.listComPorts(onlyAvailable=True))
		else:
			tryPorts = ((port, "serial",None),)
		for port, portType, identifier in tryPorts:
			self.isBulk = portType.startswith("USB bulk")
			# Try talking to the display.
			try:
				if self.isBulk:
					self._dev = hwIo.Bulk(port, 0, 1, self._onReceive, writeSize=4, onReceiveSize=10)
				else:
					self._dev = hwIo.Serial(port, baudrate=BAUD_RATE, parity=PARITY, timeout=TIMEOUT, writeTimeout=TIMEOUT, onReceive=self._onReceive)
			except EnvironmentError:
				continue

			# Send a cell count request twice, since it seems that the first sent request doesn't come through
			self._sendCellCountRequest()
			self._sendCellCountRequest()
			for i in xrange(3):
				# An expected response hasn't arrived yet, so wait for it.
				self._dev.waitForRead(TIMEOUT)
				if self.numCells:
					break
			if not self.numCells:
				self._dev.close()
				continue
			if portType.startswith("USB serial"):
				self._model = SyncBraille(self)
			elif self.isBulk:
				self._sendIdentificationRequests(usbId=identifier)
			elif identifier:
				self._sendIdentificationRequests(bluetoothPrefix=identifier)
			else:
				self._sendIdentificationRequests()
			self._dev.waitForRead(TIMEOUT)
			if self._model:
				# A display responded.
				log.info("Found {device} connected via {type} ({port})".format(
					device=self._model.name, type=portType, port=port))
				break

			self._dev.close()
		else:
			raise RuntimeError("No Hims display found")

	def display(self, cells):
		# cells will already be padded up to numCells.
		self._sendPacket("\xfc","\x01","".join(chr(cell) for cell in cells))

	def _sendCellCountRequest(self):
		log.debug("Sending cell count request...")
		self._sendPacket("\xfb","\x01","\x00"*32)

	def _sendIdentificationRequests(self, usbId=None, bluetoothPrefix=None):
		log.debug("Considering sending identification requests: usbId=%s, bluetoothPrefix=%s"%(usbId,bluetoothPrefix))
		if usbId and not bluetoothPrefix:
			map=[modelTuple for modelTuple in modelMap if modelTuple[1].usbId==usbId]
		elif not usbId and bluetoothPrefix:
			map=[modelTuple for modelTuple in modelMap if modelTuple[1].bluetoothPrefix==bluetoothPrefix]
		elif usbId and bluetoothPrefix:
			map=[modelTuple for modelTuple in modelMap if modelTuple[1].usbId==usbId and modelCls.bluetoothPrefix==bluetoothPrefix]
		else: # not usbId and not bluetoothPrefix
			map=modelMap
		if not map:
			raise ValueError("The specified criteria to send identification requests didn't yield any results")
		if len(map)==1:
			modelCls = map[0][1]
			numCells = self.numCells or modelCls.numCells
			if numCells:
				# There is only one model matching the criteria, and we have the proper number of cells.
				# There's no point in sending an identification request at all, just use this model
				log.debug("Chose %s as model without sending an additional identification request"%modelCls.name)
				self._model = modelCls(self)
				self.numCells = numCells
				return
		self._model = None
		for id, cls in map:
			log.debug("Sending request for id %r"%id)
			self._dev.write("\x1c{id}\x1f".format(id=id))
			self._dev.waitForRead(TIMEOUT)
			if self._model:
				log.debug("%s model has been set"%self._model.name)
				break

	def _handleIdentification(self, id):
		modelCls = None
		models=[modelCls for modelId,modelCls in modelMap if modelId==id]
		log.debug("Identification received, id %s"%id)
		if not models:
			raise ValueError("Device identification ID unknown in model map")
		if len(models)==1:
			modelCls = models[0]
			self.numCells=self.numCells or modelCls.numCells
			log.debug("There is an exact match, %s found with %d cells"%(modelCls.name,self.numCells))
		if not self.numCells:
			self._sendCellCountRequest()
			self._dev.waitForRead(TIMEOUT)
		if self.numCells and len(models)>1:
			log.debug("Multiple models match: %s"%", ".join(modelCls.name for modelCls in models))
			try:
				modelCls = next(cls for cls in models if cls.numCells==self.numCells)
				log.debug("There is an exact match out of multiple models, %s found with %d cells"%(modelCls.name,self.numCells))
			except StopIteration:
				log.debugWarning("No exact model match found for the reported %d cells display"%self.numCells)
				try:
					modelCls = next(cls for cls in models if not cls.numCells)
				except StopIteration:
					modelCls = Model
		if modelCls:
			self._model = modelCls(self)

	def _handlePacket(self, packet):
		mode=packet[1]
		if mode=="\x00": # Cursor routing
			routingIndex = ord(packet[3])
			try:
				inputCore.manager.executeGesture(RoutingInputGesture(routingIndex))
			except inputCore.NoInputGestureAction:
				pass
		elif mode=="\x01": # Braille input or function key
			if not self._model:
				return
			_keys = sum(ord(packet[4+i])<<(i*8) for i in xrange(4))
			keys = set()
			for keyHex in self._model.keys:
				if _keys & keyHex:
					# This key is pressed
					_keys -= keyHex
					keys.add(keyHex)
					if _keys == 0:
						break
			if _keys:
				log.error("Unknown key(s) 0x%x received from Hims display"%_keys)
				return
			try:
				inputCore.manager.executeGesture(KeyInputGesture(self._model, keys))
			except inputCore.NoInputGestureAction:
				pass
		elif mode=="\x02": # Cell count
			self.numCells=ord(packet[3])

	def _onReceive(self, data):
		if self.isBulk:
			# data contains the entire packet.
			stream = StringIO(data)
			firstByte=data[0]
			stream.seek(1)
		else:
			firstByte = data
			# data only contained the first byte. Read the rest from the device.
			stream = self._dev
		if firstByte=="\x1c":
			# A device is identifying itself
			deviceId=stream.read(2)
			# When a device identifies itself, the packets ends with 0x1f
			assert stream.read(1) == "\x1f"
			self._handleIdentification(deviceId)
		elif firstByte=="\xfa":
			# Command packets are ten bytes long
			packet=firstByte+stream.read(9)
			assert packet[2] == "\x01" # Fixed value
			checksum=packet[8]
			assert packet[9] == "\xfb" # Command End
			assert(chr(sum(ord(c) for c in packet[0:8]+packet[9])&0xff)==checksum)
			self._handlePacket(packet)
		else:
			log.debug("Unknown first byte received: 0x%x"%ord(firstByte))
			return

	def _sendPacket(self, type, mode, data1, data2=""):
		packetLength = 2 + 1 + 1 + 2 + len(data1) + 1 + 1 + 2 + len(data2) + 1 + 4 + 1 + 2
		# Construct the packet
		packet=[
			# Packet start
			type*2,
			# Mode
			mode, # Always "\x01" according to the spec
			# Data block 1 start
			"\xf0",
			# Data block 1 length
			chr((len(data1)>>0)&0xff),
			chr((len(data1)>>8)&0xff),
			# Data block 1
			data1,
			# Data block 1 end
			"\xf1",
			# Data block 2 is currently not used, but it is part of the spec
			# Data block 2 start
			"\xf2",
			# Data block 1 length
			chr((len(data2)>>0)&0xff),
			chr((len(data2)>>8)&0xff),
			# Data block 2
			data2,
			# Data block 2 end
			"\xf3",
			# Reserved bytes
			"\x00"*4,
			# Reserved space for checksum
			"\x00",
			# Packet end
			"\xfd"*2,
		]
		packetStrWithoutCheksum="".join(s for s in packet)
		packet[-2]=chr(sum(ord(c) for c in packetStrWithoutCheksum)&0xff)
		packetStrWithCheksum="".join(s for s in packet)
		assert(len(packetStrWithCheksum)==packetLength)
		self._dev.write(packetStrWithCheksum)

	def terminate(self):
		try:
			super(BrailleDisplayDriver, self).terminate()
		finally:
			# Make sure the device gets closed.
			# If it doesn't, we may not be able to re-open it later.
			self._dev.close()

	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"kb:leftAlt": ("br(hims.braillesenseqwerty):dot1+dot3+dot4+space",),
			"kb:capsLock": ("br(hims.braillesenseqwerty):dot1+dot3+dot6+space",),
			"kb:tab": ("br(hims.braillesenseqwerty):dot4+dot5+space",),
			"kb:shift+alt+tab": ("br(hims.braillesenseqwerty):advance2+advance3+advance1",),
			"kb:alt+tab": ("br(hims.braillesenseqwerty):advance2+advance3",),
			"kb:shift+tab": ("br(hims.braillesenseqwerty):dot1+dot2+space",),
			"kb:end": ("br(hims.braillesenseqwerty):dot4+dot6+space",),
			"kb:control+end": ("br(hims.braillesenseqwerty):dot4+dot5+dot6+space",),
			"kb:home": ("br(hims.braillesenseqwerty):dot1+dot3+space",),
			"kb:control+home": ("br(hims.braillesenseqwerty):dot1+dot2+dot3+space",),
			"kb:leftArrow": ("br(hims.braillesenseqwerty):dot3+space",),
			"kb:control+shift+leftArrow": ("br(hims.braillesenseqwerty):dot2+dot8+space+advance1",),
			"kb:control+leftArrow": ("br(hims.braillesenseqwerty):dot2+space",),
			"kb:shift+alt+leftArrow": ("br(hims.braillesenseqwerty):dot2+dot7+advance1",),
			"kb:alt+leftArrow": ("br(hims.braillesenseqwerty):dot2+dot7",),
			"kb:rightArrow": ("br(hims.braillesenseqwerty):dot6+space",),
			"kb:control+shift+rightArrow": ("br(hims.braillesenseqwerty):dot5+dot8+space+advance1",),
			"kb:control+rightArrow": ("br(hims.braillesenseqwerty):dot5+space",),
			"kb:shift+alt+rightArrow": ("br(hims.braillesenseqwerty):dot5+dot7+advance1",),
			"kb:alt+rightArrow": ("br(hims.braillesenseqwerty):dot5+dot7",),
			"kb:pageUp": ("br(hims.braillesenseqwerty):dot1+dot2+dot6+space",),
			"kb:control+pageUp": ("br(hims.braillesenseqwerty):dot1+dot2+dot6+dot8+space",),
			"kb:upArrow": ("br(hims.braillesenseqwerty):dot1+space",),
			"kb:control+shift+upArrow": ("br(hims.braillesenseqwerty):dot2+dot3+dot8+space+advance1",),
			"kb:control+upArrow": ("br(hims.braillesenseqwerty):dot2+dot3+space",),
			"kb:shift+alt+upArrow": ("br(hims.braillesenseqwerty):dot2+dot3+dot7+advance1",),
			"kb:alt+upArrow": ("br(hims.braillesenseqwerty):dot2+dot3+dot7",),
			"kb:shift+upArrow": ("br(hims.braillesenseqwerty):leftSideScrollDown+space",),
			"kb:pageDown": ("br(hims.braillesenseqwerty):dot3+dot4+dot5+space",),
			"kb:control+pageDown": ("br(hims.braillesenseqwerty):dot3+dot4+dot5+dot8+space",),
			"kb:downArrow": ("br(hims.braillesenseqwerty):dot4+space",),
			"kb:control+shift+downArrow": ("br(hims.braillesenseqwerty):dot5+dot6+dot8+space+advance1",),
			"kb:control+downArrow": ("br(hims.braillesenseqwerty):dot5+dot6+space",),
			"kb:shift+alt+downArrow": ("br(hims.braillesenseqwerty):dot5+dot6+dot7+advance1",),
			"kb:alt+downArrow": ("br(hims.braillesenseqwerty):dot5+dot6+dot7",),
			"kb:shift+downArrow": ("br(hims.braillesenseqwerty):space+rightSideScrollDown",),
			"kb:escape": ("br(hims.braillesenseqwerty):dot1+dot5+space",),
			"kb:delete": ("br(hims.braillesenseqwerty):dot1+dot3+dot5+space",),
			"kb:f1": ("br(hims.braillesenseqwerty):dot1+dot2+dot5+space",),
			"kb:f3": ("br(hims.braillesenseqwerty):dot1+dot2+dot4+dot8",),
			"kb:f4": ("br(hims.braillesenseqwerty):dot7+advance3",),
			"kb:windows+b": ("br(hims.braillesenseqwerty):dot1+dot2+advance1",),
			"kb:windows+d": ("br(hims.braillesenseqwerty):dot1+dot4+dot5+advance1",),
			"braille_routeTo": ("br(hims):routing",),
			"braille_scrollBack": ("br(hims):leftScrollUp","br(hims):rightScrollUp","br(hims):leftScroll",),
			"braille_scrollForward": ("br(hims):leftScrollDown","br(hims):rightScrollDown","br(hims):rightScroll",),
			"review_previousLine": ("br(hims):rightUpArrow",),
			"review_nextLine": ("br(hims):rightDownArrow",),
			"review_previousCharacter": ("br(hims):rightLeftArrow",),
			"review_nextCharacter": ("br(hims):rightRightArrow",),
			"braille_toFocus": ("br(hims):leftScrollUp+leftScrollDown","br(hims):rightScrollUp+rightScrollDown","br(hims):leftScroll+rightScroll",),
		}
	})

class KeyInputGesture(braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture):

	source = BrailleDisplayDriver.name

	def __init__(self, model, keys):
		super(KeyInputGesture, self).__init__()
		self.model=model.name
		self.keys = keys
		self.keyNames = names = set()
		isBrailleInput = True
		for key in keys:
			if isBrailleInput:
				if 0xff & key:
					self.dots |= key
				elif model.keys.get(key)=="space":
					self.space = True
				else:
					# This is not braille input.
					isBrailleInput = False
					self.dots = 0
					self.space = False
			names.add(model.keys[key])

		self.id = "+".join(names)

class RoutingInputGesture(braille.BrailleDisplayGesture):

	source = BrailleDisplayDriver.name

	def __init__(self, routingINdex):
		super(RoutingInputGesture, self).__init__()
		self.routingIndex = routingINdex
		self.id = "routing"
