# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2012-2020 NV Access Limited, Ulf Beckmann <beckmann@flusoft.de>
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

# A redesign was made for Python V3.7 in 2020
#
# This file represents the braille display driver for
# Seika3/5 V1.x/2.0, Seika80, a product from Nippon Telesoft
# see www.seika-braille.com for more details
# 24.07.2020 17:03

from typing import List
import wx
import serial
import braille
import inputCore
import hwPortUtils
from hwIo import intToByte
from logHandler import log

TIMEOUT = 0.2
BAUDRATE = 9600
READ_INTERVAL = 50
BUF_START = b"\xFF\xFF"

class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	name = "seika"
	# Translators: Names of braille displays.
	description = _("Seika Braille Displays")
	numCells = 0

	@classmethod
	def check(cls):
		return True
	def __init__(self):
		super(BrailleDisplayDriver, self).__init__()
		for portInfo in hwPortUtils.listComPorts(onlyAvailable=True):
			port = portInfo["port"]
			hwID = portInfo["hardwareID"]
			
			if not hwID.upper().startswith(r"USB\VID_10C4&PID_EA60"): # Seika USB to Serial, in XP it is lowercase, in Win7 uppercase
				continue
			# At this point, a port bound to this display has been found.
			# Try talking to the display.
			try:
				self._ser = serial.Serial(port, baudrate=BAUDRATE, timeout=TIMEOUT, writeTimeout=TIMEOUT, parity=serial.PARITY_ODD, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE)
			except serial.SerialException:
				continue
			log.debug("serial port open {port}".format(port=port))
			# get the version infos
			self._ser.write(BUF_START + b"\x1C")
			self._ser.flush()
			# Read out the input buffer
			versionS = self._ser.read(13)
			log.debug("receive {p}".format(p=versionS))
			if versionS.startswith(b"seika80"):
				log.info("Found Seika80 connected via {port} Version {versionS}".format(port=port, versionS=versionS))
				self.numCells = 80
				# data header for seika 80
				self.sendHeader = (BUF_START + b"s80").ljust(8, b"\x00")
				break
			if versionS.startswith(b"seika3"):
				log.info("Found Seika3/5 connected via {port} Version {versionS}".format(port=port, versionS=versionS))
				self.numCells = 40
				# data header for v3, v5
				self.sendHeader = (BUF_START + b"seika").ljust(8, b"\x00")
				break
			# is it a old Seika3?
			log.debug("test if it is a old Seika3")
			self._ser.write(BUF_START + b"\x0A")
			self._ser.flush()
			# Read out the input buffer
			versionS = self._ser.read(12)
			log.debug("receive {p}".format(p=versionS))
			if versionS.startswith(prefix=(
				b'\x00\x05(\x08v5.0\x01\x01\x01\x01',
				b'\x00\x05(\x08seika\x00'
			)):
				log.info("Found Seika3 old Version connected via {port} Version {versionS}".format(port=port, versionS=versionS))
				self.numCells = 40
				self.sendHeader = BUF_START + b"\x04\x00\x63\x00\x50\x00"
				break
			self._ser.close()
		else:
			raise RuntimeError("No SEIKA40/80 display found")
		self._readTimer = wx.PyTimer(self.handleResponses)
		self._readTimer.Start(READ_INTERVAL)

	def terminate(self):
		try:
			super(BrailleDisplayDriver, self).terminate()
			self._readTimer.Stop()
			self._readTimer = None
		finally:
			self._ser.close()

	def display(self, cells: List[int]):
		# every transmitted line consists of the preamble 'sendHeader' and the Cells
		if 80 == self.numCells:
			lineBytes: bytes = self.sendHeader + bytes(cells)
		elif 40 == self.numCells:
			cellData = (b"\x00" + intToByte(cell) for cell in cells)
			lineBytes = self.sendHeader + b"".join(cellData)
		else:
			log.error("Unsupported cell count")
			return
		self._ser.write(lineBytes)

	def handleResponses(self):
		if not self._ser.in_waiting:
			return
		key = 0
		keys = set()
		maxCellRead = self.numCells // 4  # for 80 maxCellRead is 20, for 40 cell maxCellRead is 10
		chars: bytes = self._ser.read(2)
		keytyp=1
		if not chars[0] & 0x60: # a cursorrouting block is expected
			chars: bytes = self._ser.read(maxCellRead)
			keytyp=2
		
		if keytyp == 1: # normal key
			if chars[0] & 1: # LEFT
				keys.add("left")
			if chars[0] & 4: # RIGHT
				keys.add("right")
			if chars[1] & 2: # B1 
				keys.add("b1")
			if chars[1] & 8:
				keys.add("b2")
			if chars[1] & 16:
				keys.add("b3")
			if chars[0] & 16:
				keys.add("b4")
			if chars[0] & 8:
				keys.add("b5")
			if chars[0] & 2:
				keys.add("b6")
			data= "+".join(keys)
			try:
				inputCore.manager.executeGesture(InputGestureKeys(data))
			except inputCore.NoInputGestureAction:
				log.debug("No Action for keys {keys}".format(keys=data))
				pass
		else:
			i = 0
			k = maxCellRead // 2
			while i < k:
				j = 0
				while j < 8:
					if chars[5+i] & (1<<j):
						key = i*8+j+1
						break
					j+=1
				i+=1
			if key: # Routing key is pressed
				try:
					inputCore.manager.executeGesture(InputGestureRouting(key-1))
				except inputCore.NoInputGestureAction:
					log.debug("No Action for routing command")
					pass

	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"braille_scrollBack": ("br(seika):left",),
			"braille_scrollForward": ("br(seika):right",),
			"braille_previousLine": ("br(seika):b3",),
			"braille_nextLine": ("br(seika):b4",),
			"braille_toggleTether": ("br(seika):b5",),
			"sayAll": ("br(seika):b6",),
			"kb:tab": ("br(seika):b1",),
			"kb:shift+tab": ("br(seika):b2",),
			"kb:alt+tab": ("br(seika):b1+b2",),
			"showGui": ("br(seika):left+right",),
			"braille_routeTo": ("br(seika):routing",),
		},
	})

class InputGestureKeys(braille.BrailleDisplayGesture):

	source = BrailleDisplayDriver.name
	def __init__(self, keys):
		super(InputGestureKeys, self).__init__()
		self.id = keys

class InputGestureRouting(braille.BrailleDisplayGesture):

	source = BrailleDisplayDriver.name

	def __init__(self, index):
		super(InputGestureRouting, self).__init__()

		self.id = "routing"
		self.routingIndex = index
