# brailleDisplayDrivers/nattiqbraille.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2020 NV Access Limited, Mohammed Noman - Nattiq Technologies


import serial
import braille
import inputCore
from logHandler import log
import hwIo

BAUD_RATE = 10000000
INIT_TAG = b"0"
RESET_TAG = b"reset"
# Initialization response id
INIT_RESP = 0
# Keys response id
ROUTE_RESP = 1
UP_KEY_RESP = 2
DOWN_KEY_RESP = 3
RIGHT_KEY_RESP = 4
LEFT_KEY_RESP = 5
# Keys pressed id
UP_KEY_PRESS = 1
DOWN_KEY_PRESS = 2
RIGHT_KEY_PRESS = 3
LEFT_KEY_PRESS = 4


class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	name = "nattiqbraille"
	# Translators: Names of braille displays
	description = _("Nattiq nBraille")
	isThreadSafe = True

	@classmethod
	def getManualPorts(cls):
		return braille.getSerialPorts()

	def __init__(self, port="auto"):
		super(BrailleDisplayDriver, self).__init__()
		self._serial = None
		for portType, portId, port, portInfo in self._getTryPorts(port):
			log.debug("Checking port %s for a Nattiq nBraille", port)
			try:
				self._serial = hwIo.Serial(
					port, baudrate=BAUD_RATE, timeout=self.timeout, writeTimeout=self.timeout,
					parity=serial.PARITY_NONE, onReceive=self._onReceive
				)
			except EnvironmentError:
				log.debugWarning("", exc_info=True)
				continue
			# Check for cell information
			if self._describe():
				log.debug("Nattiq nBraille found on %s with %d cells", port, self.numCells)
				break
			else:
				self._serial.close()
		else:
			raise RuntimeError("Can't find a Nattiq nBraille device (port = %s)" % port)

	def terminate(self):
		try:
			super(BrailleDisplayDriver, self).terminate()
		finally:
			self._serial.write(RESET_TAG)
			self._serial.close()
			self._serial = None

	def _describe(self):
		self.numCells = 0
		log.debug("Writing reset tag")
		self._serial.write(RESET_TAG)
		self._serial.waitForRead(self.timeout * 10)
		log.debug("Writing init tag")
		self._serial.write(INIT_TAG)
		self._serial.waitForRead(self.timeout * 10)
		# If a valid response was received, _onReceive will have set numCells.
		if self.numCells:
			return True
		log.debug("Not a Nattiq nBraille")
		return False

	def _onReceive(self, command):
		if int(command) == INIT_RESP:
			CELLS_NUM = self._serial.read(2)
			self.numCells = int(CELLS_NUM)
		elif int(command) == ROUTE_RESP:
			ROUTE_KEY = self._serial.read(2)
			inputCore.manager.executeGesture(RoutingInputGesture(int(ROUTE_KEY)))
		elif int(command) == UP_KEY_RESP:
			inputCore.manager.executeGesture(InputGestureKeys(UP_KEY_PRESS))
			log.debug("Up Key Pressed")
		elif int(command) == DOWN_KEY_RESP:
			inputCore.manager.executeGesture(InputGestureKeys(DOWN_KEY_PRESS))
			log.debug("Down Key Pressed")
		elif int(command) == RIGHT_KEY_RESP:
			inputCore.manager.executeGesture(InputGestureKeys(RIGHT_KEY_PRESS))
			log.debug("Right Key Pressed")
		elif int(command) == LEFT_KEY_RESP:
			inputCore.manager.executeGesture(InputGestureKeys(LEFT_KEY_PRESS))
			log.debug("Left Key Pressed")

	def display(self, cells):
		cells = "-".join(str(cell) for cell in cells)
		log.debug(cells)
		self._serial.write(cells.encode())

	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"braille_scrollBack": ("br(nattiqbraille):tback",),
			"braille_routeTo": ("br(nattiqbraille):routing",),
			"braille_scrollForward": ("br(nattiqbraille):tadvance",),
			"braille_previousLine": ("br(nattiqbraille):tprevious",),
			"braille_nextLine": ("br(nattiqbraille):tnext",),
		},
	})


class InputGestureKeys(braille.BrailleDisplayGesture):
	source = BrailleDisplayDriver.name

	def __init__(self, keys):
		super(InputGestureKeys, self).__init__()
		if keys == UP_KEY_PRESS:
			self.id = "tback"
		elif keys == DOWN_KEY_PRESS:
			self.id = "tadvance"
		elif keys == RIGHT_KEY_PRESS:
			self.id = "tnext"
		elif keys == LEFT_KEY_PRESS:
			self.id = "tprevious"


class RoutingInputGesture(braille.BrailleDisplayGesture):
	source = BrailleDisplayDriver.name

	def __init__(self, routingIndex):
		super(RoutingInputGesture, self).__init__()
		self.routingIndex = routingIndex
		self.id = "routing"
