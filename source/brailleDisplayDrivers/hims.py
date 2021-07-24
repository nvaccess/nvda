# -*- coding: UTF-8 -*-
#brailleDisplayDrivers/hims.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010-2018 Gianluca Casalino, NV Access Limited, Babbage B.V., Leonard de Ruijter, Bram Duvigneau
from typing import List

import serial
from io import BytesIO
import hwIo
import braille
from logHandler import log
from collections import OrderedDict
import inputCore
import brailleInput
from baseObject import AutoPropertyObject
import time
import bdDetect

BAUD_RATE = 115200
PARITY = serial.PARITY_NONE

class Model(AutoPropertyObject):
	"""Extend from this base class to define model specific behavior."""
	#: Two bytes device identifier, used in the protocol to identify the device
	#: @type: bytes
	deviceId = b""
	#: A generic name that identifies the model/series, used in gesture identifiers
	#: @type: string
	name = ""
	#: Number of braille cells
	#: @type: int
	numCells = 0 #0 means undefined, needs to be requested for
	#: The USB VID and PID for this model in the form VID_xxxx&PID_xxxx
	#: @type: string
	usbId = ""
	#: The bluetooth prefix used by devices of this specific model
	#: @type: string
	bluetoothPrefix = ""

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
			0x10<<8: "f4",
			0x20<<8: "leftSideScroll",
			0x40<<8: "rightSideScroll",
		})

class BrailleSense(Model):
	name = "Braille Sense"
	usbId = "VID_045E&PID_930A"
	bluetoothPrefix = "BrailleSense"
	numCells = 0 # Either 18 or 32

	def _get_keys(self):
		keys = super(BrailleSense, self)._get_keys()
		keys.update({
			0x01<<16: "leftSideScrollUp",
			0x02<<16: "leftSideScrollDown",
			0x04<<16: "rightSideScrollUp",
			0x08<<16: "rightSideScrollDown",
		})
		return keys

class BrailleEdge(Model):
	deviceId = b"\x42\x45" # BE
	name = "Braille Edge"
	usbId = "VID_045E&PID_930B"
	bluetoothPrefix = "BrailleEDGE"
	numCells = 40

	def _get_keys(self):
		keys = super(BrailleEdge, self)._get_keys()
		keys.update({
			0x01<<16: "leftSideScrollUp",
			0x02<<16: "rightSideScrollUp",
			0x04<<16: "rightSideScrollDown",
			0x08<<16: "leftSideScrollDown",
			0x10<<16: "f5",
			0x20<<16: "f6",
			0x40<<16: "f7",
			0x80<<16: "f8",
			0x01<<24: "leftSideUpArrow",
			0x02<<24: "leftSideDownArrow",
			0x04<<24: "leftSideLeftArrow",
			0x08<<24: "leftSideRightArrow",
			0x10<<24: "rightSideUpArrow",
			0x20<<24: "rightSideDownArrow",
			0x40<<24: "rightSideLeftArrow",
			0x80<<24: "rightSideRightArrow",
		})
		return keys

class BrailleSense2S(BrailleSense):
	"""Braille Sense with one scroll key on both sides.
	Also referred to as Braille Sense Classic."""
	name = "Braille Sense Classic"
	deviceId = b"\x42\x53" # BS

class BrailleSense4S(BrailleSense):
	deviceId = b"\x4c\x58" # LX

class SmartBeetle(BrailleSense4S):
	"""Subclass for Smart Beetle device, which has the same identifier as the Braille Sense with 4 scroll keys.
	However, it is distinguishable by the number of cells.
	Furthermore, the key codes for f2 and f4 are swapped, and it has only two scroll keys.
	"""
	numCells=14
	bluetoothPrefix = "SmartBeetle(b)"
	name = "Smart Beetle"

	def _get_keys(self):
		keys = Model._get_keys(self)
		keys.update({
			0x04<<8: "f4",
			0x10<<8: "f2",
			0x04<<16: "leftSideScroll",
			0x08<<16: "rightSideScroll",
		})
		return keys

class BrailleSenseQ(BrailleSense4S):
	deviceId = b"\x51\x58" # QX
	name = "Braille Sense QWERTY"
	numCells = 32

class BrailleSenseQX(BrailleSenseQ):
	"""Special identifier to support QWERTY input"""
	deviceId = b"\x53\x58" # SX

class SyncBraille(Model):
	name = "SyncBraille"
	usbId = "VID_0403&PID_6001"

	def _get_keys(self):
		return OrderedDict({
			0x10<<8: "leftSideScrollUp",
			0x20<<8: "rightSideScrollUp",
			0x40<<8: "rightSideScrollDown",
			0x80<<8: "leftSideScrollDown",
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
	SyncBraille,
)]

class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	name = "hims"
	# Translators: The name of a series of braille displays.
	description = _("HIMS Braille Sense/Braille EDGE/Smart Beetle/Sync Braille series")
	isThreadSafe = True
	timeout = 0.2

	@classmethod
	def getManualPorts(cls):
		return braille.getSerialPorts(filterFunc=lambda info: "bluetoothName" in info)

	def __init__(self, port="auto"):
		super(BrailleDisplayDriver, self).__init__()
		self.numCells = 0
		self._model = None

		for match in self._getTryPorts(port):
			portType, portId, port, portInfo = match
			self.isBulk = portType==bdDetect.KEY_CUSTOM
			# Try talking to the display.
			try:
				if self.isBulk:
					# onReceiveSize based on max packet size according to USB endpoint information.
					self._dev = hwIo.Bulk(port, 0, 1, self._onReceive, onReceiveSize=64)
				else:
					self._dev = hwIo.Serial(port, baudrate=BAUD_RATE, parity=PARITY, timeout=self.timeout, writeTimeout=self.timeout, onReceive=self._onReceive)
			except EnvironmentError:
				log.debugWarning("", exc_info=True)
				continue
			for i in range(3):
				self._sendCellCountRequest()
				# Wait for an expected response.
				if self.isBulk:
					# Hims Bulk devices sometimes present themselves to the system while not yet ready.
					# For example, when switching the connection mode toggle on the Braille EDGE from Bluetooth to USB,
					# the USB device is connected but not yet ready.
					# Wait ten times the timeout, which is ugly, but effective.
					self._dev.waitForRead(self.timeout*10)
				else:
					self._dev.waitForRead(self.timeout)
				if self.numCells:
					break
			if not self.numCells:
				log.debugWarning("No response from potential Hims display")
				self._dev.close()
				continue
			self._sendIdentificationRequests(match)
			if self._model:
				# A display responded.
				log.info("Found {device} connected via {type} ({port})".format(
					device=self._model.name, type=portType, port=port))
				break

			self._dev.close()
		else:
			raise RuntimeError("No Hims display found")

	def display(self, cells: List[int]):
		# cells will already be padded up to numCells.
		cellBytes = bytes(cells)
		self._sendPacket(b"\xfc", b"\x01", cellBytes)

	def _sendCellCountRequest(self):
		log.debug("Sending cell count request...")
		self._sendPacket(b"\xfb", b"\x01", bytes(32)) # send 32 null bytes

	def _sendIdentificationRequests(self, match: bdDetect.DeviceMatch):
		log.debug("Considering sending identification requests for device %s"%str(match))
		if match.type==bdDetect.KEY_CUSTOM: # USB Bulk
			matchedModelsMap = [
				modelTuple for modelTuple in modelMap if(
					modelTuple[1].usbId == match.id
				)
			]
		elif "bluetoothName" in match.deviceInfo: # Bluetooth
			matchedModelsMap = [
				modelTuple for modelTuple in modelMap if(
					modelTuple[1].bluetoothPrefix
					and match.id.startswith(modelTuple[1].bluetoothPrefix)
				)
			]
		else: # The only serial device we support which is not bluetooth, is a Sync Braille
			self._model = SyncBraille()
			log.debug("Use %s as model without sending an additional identification request"%self._model.name)
			return
		if not matchedModelsMap:
			log.debugWarning("The provided device match to send identification requests didn't yield any results")
			matchedModelsMap = modelMap
		if len(matchedModelsMap) == 1:
			modelCls = matchedModelsMap[0][1]
			numCells = self.numCells or modelCls.numCells
			if numCells:
				# There is only one model matching the criteria, and we have the proper number of cells.
				# There's no point in sending an identification request at all, just use this model
				log.debug("Use %s as model without sending an additional identification request"%modelCls.name)
				self._model = modelCls()
				self.numCells = numCells
				return
		self._model = None
		for modelId, cls in matchedModelsMap:
			log.debug("Sending request for id %r" % modelId)

			self._dev.write(b"".join([
				b"\x1c",
				modelId,
				b"\x1f"
			]))
			self._dev.waitForRead(self.timeout)
			if self._model:
				log.debug("%s model has been set"%self._model.name)
				break

	def _handleIdentification(self, recvId: bytes):
		modelCls = None
		models = [
			modelCls for modelId, modelCls in modelMap if(
				modelId == recvId
			)
		]
		log.debug("Identification received, id %s" % recvId)
		if not models:
			raise ValueError("Device identification ID unknown in model map")
		if len(models)==1:
			modelCls = models[0]
			self.numCells=self.numCells or modelCls.numCells
			log.debug("There is an exact match, %s found with %d cells"%(modelCls.name,self.numCells))
		elif len(models)>1:
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
			self._model = modelCls()

	def _handlePacket(self, packet: bytes):
		mode = packet[1]
		if mode == 0x00: # Cursor routing
			routingIndex = packet[3]
			try:
				inputCore.manager.executeGesture(RoutingInputGesture(routingIndex))
			except inputCore.NoInputGestureAction:
				pass
		elif mode == 0x01: # Braille input or function key
			if not self._model:
				return
			_keys = int.from_bytes(packet[4:8], "little", signed=False)
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
		elif mode == 0x02: # Cell count
			self.numCells = packet[3]

	def _onReceive(self, data: bytes):
		if self.isBulk:
			# data contains the entire packet.
			stream = BytesIO(data)
			firstByte:bytes = data[0:1]
			stream.seek(1)
		else:
			firstByte = data
			# data only contained the first byte. Read the rest from the device.
			stream = self._dev
		if firstByte == b"\x1c":
			# A device is identifying itself
			deviceId: bytes = stream.read(2)
			# When a device identifies itself, the packets ends with 0x1f
			assert stream.read(1) == b"\x1f"
			self._handleIdentification(deviceId)
		elif firstByte == b"\xfa":
			# Command packets are ten bytes long
			packet = firstByte + stream.read(9)
			assert packet[2] == 0x01 # Fixed value
			CHECKSUM_INDEX = 8
			checksum: int = packet[CHECKSUM_INDEX]
			assert packet[9] == 0xfb # Command End
			calcCheckSum: int = 0xff & sum(
				c for index, c in enumerate(packet) if(
					index != CHECKSUM_INDEX)
			)
			assert(calcCheckSum == checksum)
			self._handlePacket(packet)
		else:
			log.debug("Unknown first byte received: 0x%x"%ord(firstByte))
			return

	def _sendPacket(
			self,
			packetType: bytes,
			mode: bytes,
			data1: bytes,
			data2: bytes = b""
	):
		d1Len = len(data1)
		d2Len = len(data2)
		# Construct the packet
		packet: List[bytes] = [
			# Packet start
			packetType * 2,
			# Mode
			mode, # Always "\x01" according to the spec
			# Data block 1 start
			b"\xf0",
			# Data block 1 length
			d1Len.to_bytes(length=2, byteorder="little", signed=False),
			# Data block 1
			data1,
			# Data block 1 end
			b"\xf1",
			# Data block 2 is currently not used, but it is part of the spec
			# Data block 2 start
			b"\xf2",
			# Data block 1 length
			d2Len.to_bytes(length=2, byteorder="little", signed=False),
			# Data block 2
			data2,
			# Data block 2 end
			b"\xf3",
			# Reserved bytes
			b"\x00" * 4,
			# Reserved space for checksum
			# Note that the checksum has the -3rd position in the final packet bytearray,
			# whereas it has the -2nd position in the packet list
			b"\x00",
			# Packet end
			b"\xfd" * 2,
		]
		packetB = bytearray(b"".join(packet))
		#  checksum is the 3rd index from the end because 'packet end' takes up
		# two bytes and 'packetB' is a bytearray
		checksumIndexInPacketB: int = -3
		checksum: int = 0xff & sum(packetB)
		packetB[checksumIndexInPacketB] = checksum

		# check that the packet is the size we expect:
		ptLen = len(packetType)
		assert(ptLen == 1)
		mLen = len(mode)
		assert(mLen == 1)
		packetLength = ptLen*2 + mLen + 1 + 2 + d1Len + 1 + 1 + 2 + d2Len + 1 + 4 + 1 + 2
		assert(len(packetB) == packetLength)

		self._dev.write(bytes(packetB))

	def terminate(self):
		try:
			super(BrailleDisplayDriver, self).terminate()
		finally:
			# We must sleep before closing the port as not doing this can leave the display in a bad state where it can not be re-initialized.
			time.sleep(self.timeout)
			# Make sure the device gets closed.
			# If it doesn't, we may not be able to re-open it later.
			self._dev.close()

	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
					"braille_routeTo": (
				"br(hims):routing",
			),
			"braille_scrollBack": (
				"br(hims):leftSideScrollUp",
				"br(hims):rightSideScrollUp",
				"br(hims):leftSideScroll",
			),
			"braille_scrollForward": (
				"br(hims):leftSideScrollDown",
				"br(hims):rightSideScrollDown",
				"br(hims):rightSideScroll",
			),
			"braille_previousLine": (
				"br(hims):leftSideScrollUp+rightSideScrollUp",
			),
			"braille_nextLine": (
				"br(hims):leftSideScrollDown+rightSideScrollDown",
			),
			"review_previousLine": (
				"br(hims):rightSideUpArrow",
			),
			"review_nextLine": (
				"br(hims):rightSideDownArrow",
			),
			"review_previousCharacter": (
				"br(hims):rightSideLeftArrow",
			),
			"review_nextCharacter": (
				"br(hims):rightSideRightArrow",
			),
			"braille_toFocus": (
				"br(hims):leftSideScrollUp+leftSideScrollDown",
				"br(hims):rightSideScrollUp+rightSideScrollDown",
				"br(hims):leftSideScroll+rightSideScroll",
			),
			"kb:control": (
				"br(hims.smartbeetle):f1",
				"br(hims.brailleedge):f3",
			),
			"kb:windows": (
				"br(hims.smartbeetle):f2",
				"br(hims):f7",
			),
			"kb:alt": (
				"br(hims):dot1+dot3+dot4+space",
				"br(hims.smartbeetle):f3",
				"br(hims):f2",
				"br(hims.brailleedge):f4",
			),
			"kb:shift": (
				"br(hims):f5",
			),
			"kb:insert": (
				"br(hims):dot2+dot4+space",
				"br(hims):f6",
			),
			"kb:applications": (
				"br(hims):dot1+dot2+dot3+dot4+space",
				"br(hims):f8",
			),
			"kb:capsLock": (
				"br(hims):dot1+dot3+dot6+space",
			),
			"kb:tab": (
				"br(hims):dot4+dot5+space",
				"br(hims):f3",
				"br(hims.brailleedge):f2",
			),
			"kb:shift+alt+tab": (
				"br(hims):f2+f3+f1",
			),
			"kb:alt+tab": (
				"br(hims):f2+f3",
			),
			"kb:shift+tab": (
				"br(hims):dot1+dot2+space",
			),
			"kb:end": (
				"br(hims):dot4+dot6+space",
			),
			"kb:control+end": (
				"br(hims):dot4+dot5+dot6+space",
			),
			"kb:home": (
				"br(hims):dot1+dot3+space",
				"br(hims.smartbeetle):f4",
			),
			"kb:control+home": (
				"br(hims):dot1+dot2+dot3+space",
			),
			"kb:alt+f4": (
				"br(hims):dot1+dot3+dot5+dot6+space",
			),
			"kb:leftArrow": (
				"br(hims):dot3+space",
				"br(hims):leftSideLeftArrow",
			),
			"kb:control+shift+leftArrow": (
				"br(hims):dot2+dot8+space+f1",
			),
			"kb:control+leftArrow": (
				"br(hims):dot2+space",
			),
			"kb:shift+alt+leftArrow": (
				"br(hims):dot2+dot7+f1",
			),
			"kb:alt+leftArrow": (
				"br(hims):dot2+dot7",
			),
			"kb:rightArrow": (
				"br(hims):dot6+space",
				"br(hims):leftSideRightArrow",
			),
			"kb:control+shift+rightArrow": (
				"br(hims):dot5+dot8+space+f1",
			),
			"kb:control+rightArrow": (
				"br(hims):dot5+space",
			),
			"kb:shift+alt+rightArrow": (
				"br(hims):dot5+dot7+f1",
			),
			"kb:alt+rightArrow": (
				"br(hims):dot5+dot7",
			),
			"kb:pageUp": (
				"br(hims):dot1+dot2+dot6+space",
			),
			"kb:control+pageUp": (
				"br(hims):dot1+dot2+dot6+dot8+space",
			),
			"kb:upArrow": (
				"br(hims):dot1+space",
				"br(hims):leftSideUpArrow",
			),
			"kb:control+shift+upArrow": (
				"br(hims):dot2+dot3+dot8+space+f1",
			),
			"kb:control+upArrow": (
				"br(hims):dot2+dot3+space",
			),
			"kb:shift+alt+upArrow": (
				"br(hims):dot2+dot3+dot7+f1",
			),
			"kb:alt+upArrow": (
				"br(hims):dot2+dot3+dot7",
			),
			"kb:shift+upArrow": (
				"br(hims):leftSideScrollDown+space",
			),
			"kb:pageDown": (
				"br(hims):dot3+dot4+dot5+space",
			),
			"kb:control+pageDown": (
				"br(hims):dot3+dot4+dot5+dot8+space",
			),
			"kb:downArrow": (
				"br(hims):dot4+space",
				"br(hims):leftSideDownArrow",
			),
			"kb:control+shift+downArrow": (
				"br(hims):dot5+dot6+dot8+space+f1",
			),
			"kb:control+downArrow": (
				"br(hims):dot5+dot6+space",
			),
			"kb:shift+alt+downArrow": (
				"br(hims):dot5+dot6+dot7+f1",
			),
			"kb:alt+downArrow": (
				"br(hims):dot5+dot6+dot7",
			),
			"kb:shift+downArrow": (
				"br(hims):space+rightSideScrollDown",
			),
			"kb:escape": (
				"br(hims):dot1+dot5+space",
				"br(hims):f4",
				"br(hims.brailleedge):f1",
			),
			"kb:delete": (
				"br(hims):dot1+dot3+dot5+space",
				"br(hims):dot1+dot4+dot5+space",
			),
			"kb:f1": (
				"br(hims):dot1+dot2+dot5+space",
			),
			"kb:f3": (
				"br(hims):dot1+dot4+dot8+space",
			),
			"kb:f4": (
				"br(hims):dot7+f3",
			),
			"kb:windows+b": (
				"br(hims):dot1+dot2+f1",
			),
			"kb:windows+d": (
				"br(hims):dot1+dot4+dot5+f1",
			),
			"kb:control+insert": (
				"br(hims.smartbeetle):f1+rightSideScroll",
			),
			"kb:alt+insert": (
				"br(hims.smartbeetle):f3+rightSideScroll",
			),
		}
	})

class KeyInputGesture(braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture):

	source = BrailleDisplayDriver.name

	def __init__(self, model, keys):
		super(KeyInputGesture, self).__init__()
		# Model identifiers should not contain spaces.
		self.model=model.name.replace(" ", "")
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
