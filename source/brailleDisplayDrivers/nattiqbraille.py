# brailleDisplayDrivers/nattiqbraille.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2011-2020


import serial
import braille
import inputCore
from logHandler import log
import hwIo

BAUD_RATE = 10000000
TIMEOUT = 0.3
INIT_TAG = "0"


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
					self._serial = hwIo.Serial(port, baudrate=BAUD_RATE, timeout=0.3, writeTimeout=0.3, parity=serial.PARITY_NONE, onReceive=self._onReceive)
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
				self._serial.write("reset".encode())
				self._serial.close()
				self._serial = None

        def _describe(self):
			self.numCells = 0
			log.debug("Writing reset tag")
			self._serial.write("reset".encode())
			self._serial.waitForRead(3)
			log.debug("Writing init tag")
			self._serial.write(INIT_TAG)
			self._serial.waitForRead(3)
			# If a valid response was received, _onReceive will have set numCells.
			if self.numCells:
					return True
			log.debug("Not a Nattiq nBraille")
			return False
        
        def _onReceive(self, command):
			if int(command) == 0:
				arg = self._serial.read(2)
				self.numCells = int(arg)
			elif int(command) == 2:     
				inputCore.manager.executeGesture(InputGestureKeys(1))
				self._serial.waitForRead(1)
				arg = self._serial.read(2)   
            elif int(command) == 3:  
				inputCore.manager.executeGesture(InputGestureKeys(2))
				self._serial.waitForRead(1)
				arg = self._serial.read(2)
            elif int(command) == 4:
				inputCore.manager.executeGesture(InputGestureKeys(3))
				self._serial.waitForRead(1)
				arg = self._serial.read(2) 
            elif int(command) == 5:
				inputCore.manager.executeGesture(InputGestureKeys(4))
				self._serial.waitForRead(1)
				arg = self._serial.read(2)
            elif int(command) == 1:
				arg = self._serial.read(2)
				try:
					inputCore.manager.executeGesture(RoutingInputGesture(int(arg)))
				except ValueError:
					pass

		def _dispatch(self, command, arg):
			return
	
		def display(self, cells):
			cells = "-".join(str(cell) for cell in cells)
			log.debug(cells)
			self._serial.write(cells)

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
		if keys == 1:
			self.id = "tback"
		elif keys == 2:
			self.id = "tadvance"    
		elif keys == 3:
			self.id = "tnext"    
		elif keys == 4:
			self.id = "tprevious"    

class RoutingInputGesture(braille.BrailleDisplayGesture):
	source = BrailleDisplayDriver.name
	def __init__(self, routingIndex):
		super(RoutingInputGesture, self).__init__()
		self.routingIndex = routingIndex
		self.id = "routing"
