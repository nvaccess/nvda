#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2011 Sebastian Kruber <sebastian.kruber@hedo.de>

# Parts of this code are inherited from the baum braille driver
# written by James Teh <jamie@jantrid.net>

# This file represents the braille display driver for
# hedo ProfiLine USB, a product from hedo Reha-Technik GmbH
# see www.hedo.de for more details

import time
import wx
import serial
import braille
import inputCore
import hwPortUtils
from logHandler import log

HEDO_TIMEOUT = 0.2
HEDO_BAUDRATE = 19200
HEDO_READ_INTERVAL = 50
HEDO_ACK = 0x7E
HEDO_INIT = 0x01
HEDO_CR_BEGIN = 0x20
HEDO_CR_END = 0x6F
HEDO_RELEASE_OFFSET = 0x80
HEDO_CELL_COUNT = 80
HEDO_STATUS_CELL_COUNT = 4

HEDO_KEYMAP = {
	0x04: "K1",
	0x03: "K2", # K2 or B1
	0x08: "K3",
	0x07: "B2",
	0x0B: "B3",
	0x0F: "B4",
	0x13: "B5",
	0x17: "B6",
	0x1B: "B7",
	0x1F: "B8",
}

HEDO_USB_IDS = frozenset((
	"VID_0403&PID_DE59", # Hedo ProfiLine
	"VID_0403&PID_DE58", # Hedo MobiLine
))

class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	name = "hedoProfiLine"
	description = "hedo ProfiLine USB"

	numCells = HEDO_CELL_COUNT

	@classmethod
	def check(cls):
		return True

	def __init__(self):
		super(BrailleDisplayDriver, self).__init__()

		for portInfo in hwPortUtils.listComPorts(onlyAvailable=True):
			port = portInfo["port"]
			hwID = portInfo["hardwareID"]
			#log.info("Found port {port} with hardwareID {hwID}".format(port=port, hwID=hwID))
			if not hwID.startswith(r"FTDIBUS\COMPORT"):
				continue
			try:
				usbID = hwID.split("&", 1)[1]
			except IndexError:
				continue
			if usbID not in HEDO_USB_IDS:
				continue
			# At this point, a port bound to this display has been found.
			# Try talking to the display.
			try:
				self._ser = serial.Serial(port, baudrate=HEDO_BAUDRATE, timeout=HEDO_TIMEOUT, writeTimeout=HEDO_TIMEOUT, parity=serial.PARITY_ODD, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE)
			except serial.SerialException:
				continue

			# Prepare a blank line
			cells = chr(HEDO_INIT) + chr(0) * (HEDO_CELL_COUNT + HEDO_STATUS_CELL_COUNT)

			# Send the blank line twice
			self._ser.write(cells)
			self._ser.flush()
			self._ser.write(cells)
			self._ser.flush()

			# Read out the input buffer
			ackS = self._ser.read(2)
			if chr(HEDO_ACK) in ackS:
				log.info("Found hedo ProfiLine connected via {port}".format(port=port))
				break

		else:
			raise RuntimeError("No hedo display found")
		
		self._readTimer = wx.PyTimer(self.handleResponses)
		self._readTimer.Start(HEDO_READ_INTERVAL)

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

	def display(self, cells):
		# every transmitted line consists of the preamble HEDO_INIT, the statusCells and the Cells
		line = chr(HEDO_INIT) + chr(0) * HEDO_STATUS_CELL_COUNT + "".join(chr(cell) for cell in cells)

		# cells will be padded up to 1 + numStatusCells + numCells.
		expectedLength = 1 + HEDO_STATUS_CELL_COUNT + HEDO_CELL_COUNT
		line += chr(0) * (expectedLength - len(line))

		self._ser.write(line)

	def handleResponses(self, wait=False):
		while wait or self._ser.inWaiting():
			data = self._ser.read(1)
			if data:
				# do not handle acknowledge bytes
				if data != chr(HEDO_ACK):
					self.handleData(ord(data))
			wait = False

	def handleData(self, data):

		if data >= HEDO_CR_BEGIN and data <= HEDO_CR_END:
			# Routing key is pressed
			try:
				inputCore.manager.executeGesture(InputGestureRouting(data - HEDO_CR_BEGIN))
			except inputCore.NoInputGestureAction:
				log.debug("No Action for routing command")
				pass

		elif data >= (HEDO_CR_BEGIN + HEDO_RELEASE_OFFSET) and data <= (HEDO_CR_END + HEDO_RELEASE_OFFSET):
			# Routing key is released
			return

		elif data in HEDO_KEYMAP:
			# A key is pressed
			# log.debug("Key " + HEDO_KEYMAP[data] + " pressed")
			self._keysDown.add(HEDO_KEYMAP[data])
			self._ignoreKeyReleases = False

		elif data > HEDO_RELEASE_OFFSET and (data - HEDO_RELEASE_OFFSET) in HEDO_KEYMAP:
			# A key is released
			# log.debug("Key " + str(self._keysDown) + " released")
			if self._ignoreKeyReleases == False:
				keys = "+".join(self._keysDown)
				self._ignoreKeyReleases = True
				self._keysDown = set()
				try:
					inputCore.manager.executeGesture(InputGestureKeys(keys))
				except inputCore.NoInputGestureAction:
					log.debug("No Action for keys {keys}".format(keys=keys))
					pass

		# else:
		#	log.debug("Key " + hex(data) + " not identified")

	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"braille_scrollBack": ("br(hedoProfiLine):K1",),
			"braille_toggleTether": ("br(hedoProfiLine):K2",),
			"braille_scrollForward": ("br(hedoProfiLine):K3",),
			"braille_previousLine": ("br(hedoProfiLine):B2",),
			"braille_nextLine": ("br(hedoProfiLine):B5",),
			"sayAll": ("br(hedoProfiLine):B6",),
			"braille_routeTo": ("br(hedoProfiLine):routing",),
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
