#brailleDisplayDrivers/papenmeier_serial.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2012-2017 Tobias Platen, Halim Sahin, Ali-Riza Ciftcioglu, NV Access Limited, Davy Kager
#Author: Tobias Platen (nvda@lists.thm.de)
#minor changes by Halim Sahin (nvda@lists.thm.de), Ali-Riza Ciftcioglu <aliminator83@googlemail.com>, James Teh and Davy Kager
#used braille port selection code from braillenote driver

from collections import OrderedDict
import time
from typing import List, Optional

import wx
import braille
import hwPortUtils
from logHandler import log
from baseObject import ScriptableObject
import inputCore
import serial

#Control Flow
STX = 0x02 #Start of Text
ETX = 0x03 #End of Text

KEY_CHECK_INTERVAL = 10
TIMEOUT = 0.5

def brl_auto_id() -> bytes:
	"""send auto id command to braille display"""
	#send a bad packet to the braille display
	return bytes([STX, ord(b'S'), 0x0, 0x0, 0x0, 0x0, ETX])

def brl_out(offset: int, data: List[int]) -> bytes:
	"""send data to braille display
		@param offset: Must be positive.
	"""
	d2 = len(data)+7
	ret = bytearray([
		STX,
		ord(b'S')
	])
	ret.extend(offset.to_bytes(2, "big", signed=False))
	ret.extend(d2.to_bytes(2, "big", signed=False))
	ret.extend(data)
	ret.append(ETX)
	return bytes(ret)

def brl_poll(dev: serial.Serial) -> bytes:
	"""read data from braille display, used by keypress handler"""
	if dev.in_waiting < 10: return b""
	ret = dev.read(dev.in_waiting)
	if ret[0] == STX and ret[9] == ETX:
		return ret
	return b""

class BrailleDisplayDriver(braille.BrailleDisplayDriver, ScriptableObject):
	"""papenmeier_serial braille display driver.
	"""
	name = "papenmeier_serial"
	# Translators: Names of braille displays.
	description = _("Papenmeier BRAILLEX older models")

	@classmethod
	def check(cls):
		"""should return false if there is a missing dependency"""
		return True

	@classmethod
	def getPossiblePorts(cls):
		ports = OrderedDict()
		for p in hwPortUtils.listComPorts():
			# Translators: Name of a serial communications port
			ports[p["port"]] = _("Serial: {portName}").format(portName=p["friendlyName"])
		return ports

	def initTable(self):
		"""do not use braille builtin table"""
		table = [1] * self.numCells
		self._dev.write(brl_out(512+self._offsetHorizontal, table))

	def __init__(self, port):
		"""Initializes braille display driver"""
		super(BrailleDisplayDriver, self).__init__()
		self.numCells = 0
		self._lastkey = ''
		self._dev = None
		self._repeatcount = 0
		self._port = (port)
		log.info("papenmeier_serial using port "+self._port)
		#try to connect to braille display
		for baud in (19200, 38400):
			if(self._dev is None):
				self._dev = serial.Serial(self._port, baudrate = baud, timeout=TIMEOUT, writeTimeout=TIMEOUT)
				self._dev.write(brl_auto_id())
				if (baud == 19200): time.sleep(0.2)
				else: time.sleep(0.03)
				displaytype = brl_poll(self._dev)
				dic = -1
				if len(displaytype) == 10 and displaytype[0] == STX and displaytype[1] == ord(b'I'):
					dic = displaytype[2]
					self._eab = (baud == 38400)
				if(dic == -1):
					self._dev.close()
					self._dev=None

		#set parameters for display
		if(dic == 2):
			self.numCells = 40
			self._offsetHorizontal = 0
			self._keymap = ['l1', 'l2', 'left', 'up', 'r2', 'dn', 'right', 'r1', 'reportf']
		elif(dic == 1):
			self._offsetHorizontal = 0
			self.numCells = 40
		elif(dic == 3):
			self.numCells = 80
			self._offsetHorizontal = 22
			self._keymap = ['l1', 'l2', 'r2', 'reportf', 'up', 'left', 'r1', 'right', 'dn', 'left2', 'up2', 'dn2', 'right2']
		elif(dic == 6):
			self.numCells = 80
			self._offsetHorizontal = 0
		elif(dic == 66):#//BRAILLEX EL 80
			self._offsetHorizontal = 2
			self.numCells = 80
		elif(dic == 67):
			self._offsetHorizontal = 20
			self.numCells = 80
		elif(dic == 64):
			self._offsetHorizontal = 13
			self.numCells = 40
		elif(dic == 65):
			self._offsetHorizontal = 13
			self.numCells = 66
		elif(dic == 68):
			self._offsetHorizontal = 0
			self.numCells = 40
		elif(dic==69):
			self._offsetHorizontal = 0
			self.numCells = 32
		elif(dic==70):
			self._offsetHorizontal = 0
			self.numCells = 20
		else:
			raise Exception("No or unknown braille display found")
		#initialize display
		self.initTable()
		#start keyCheckTimer
		self._decodedkeys = []
		self._keyCheckTimer = wx.PyTimer(self._handleKeyPresses)
		self._keyCheckTimer.Start(KEY_CHECK_INTERVAL)

	def terminate(self):
		"""free resources"""
		super(BrailleDisplayDriver, self).terminate()
		try:
			if(self._dev!=None):
				self._dev.close()
				self._dev = None
				self._keyCheckTimer.Stop()
				self._keyCheckTimer = None
		except:
			pass

	def display(self, cells: List[int]):
		"""write data to braille display"""
		if(self._dev!=None):
			try:
				self._dev.write(brl_out(self._offsetHorizontal, cells))
			except:
				self._dev = None
		
	def executeGesture(self,gesture):
		"""execute a gesture"""
		#here you can add other gesture types
		try:
			if gesture.id: inputCore.manager.executeGesture(gesture)
		except inputCore.NoInputGestureAction:
			pass

	def _handleKeyPresses(self): #called by the keycheck timer
		"""if a button was pressed an input gesture is executed"""
		if(self._dev!=None):
			data = brl_poll(self._dev)
			if len(data) == 10 and data[1] == ord(b'K'):
				pos = (data[2] << 8) + data[3]
				pos = (pos-768) // 3
				pressed = data[6]
				keys = data[8]
				self._repeatcount = 0
				self.executeGesture(InputGesture(pos, pressed, keys, self))
			elif(len(data) == 0):
				if(self._repeatcount==50):
					if(len(self._lastkey)): self.executeGesture(InputGesture(None, None, None, self))
					self._repeatcount = 0
				else:
					self._repeatcount += 1

	#global gestures
	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"braille_scrollBack": ("br(papenmeier_serial):left",),
			"braille_scrollForward": ("br(papenmeier_serial):right",),
			"braille_previousLine": ("br(papenmeier_serial):up",),
			"braille_nextLine": ("br(papenmeier_serial):dn",),
			"braille_routeTo": ("br(papenmeier_serial):route",),
			"braille_reportFormatting": ("br(papenmeier_serial):upperRouting",),

			"braille_toggleTether": ("br(papenmeier_serial):r2",),
			"review_currentCharacter": ("br(papenmeier_serial):l1",),
			"review_activate": ("br(papenmeier_serial):l2",),
			"reportFormatting": ("br(papenmeier_serial):reportf",),

			"navigatorObject_previous": ("br(papenmeier_serial):left2", "br(papenmeier_serial):r1,left"),
			"navigatorObject_next": ("br(papenmeier_serial):right2", "br(papenmeier_serial):r1,right"),
			"navigatorObject_parent": ("br(papenmeier_serial):up2", "br(papenmeier_serial):r1,up"),
			"navigatorObject_firstChild": ("br(papenmeier_serial):dn2", "br(papenmeier_serial):r1,dn"),

			"title": ("br(papenmeier_serial):l1,up",),
			"reportStatusLine": ("br(papenmeier_serial):l2,dn",),
		}
	})

def brl_keyname2(keys: int) -> str:
	"""returns keyname for key index on displays with eab"""
	if(keys & 4 == 4): return 'l1'
	if(keys & 8 == 8): return 'l2'
	if(keys & 16 == 16): return 'r1'
	if(keys & 32 == 32): return 'r2'
	return ''

def brl_keyname(keyindex: int, driver: BrailleDisplayDriver) -> str:
	"""returns keyname for key index"""
	if(driver._eab):
		if(keyindex==-255): return "left"
		if(keyindex==-254): return "left2"
		if(keyindex==-253): return "up"
		if(keyindex==-252): return "up2"
		if(keyindex==-251): return "right"
		if(keyindex==-250): return "right2"
		if(keyindex==-249): return "dn"
		if(keyindex==-248): return "dn2"
		return ''
	else:
		#display does not have an eab, so the display specific table is used
		keyindex = keyindex+255
		if(keyindex>=0 and keyindex<len(driver._keymap)):
			return driver._keymap[keyindex]
		else: return ''

class InputGesture(braille.BrailleDisplayGesture):
	"""input gesture class for papenmeier_serial displays used only by the driver"""

	source = BrailleDisplayDriver.name
	
	def __init__(
			self,
			keyindex: Optional[int],
			pressed: Optional[int],
			keys: Optional[int],
			driver: BrailleDisplayDriver
	):
		super(InputGesture, self).__init__()
		self.id = ''
		if(keyindex is None):
			self.id = driver._lastkey
			return
		if(pressed==1 and keyindex>=0):
			self.routingIndex = keyindex-driver._offsetHorizontal
			self.id = "route"
			if(keyindex>255):
				self.routingIndex -= 256
				self.id = "upperRouting"
		elif(pressed == 0):
			k: str = brl_keyname(keyindex, driver)
			if(driver._lastkey!=k):
				if(driver._lastkey!=''): self.id=driver._lastkey+','+k
			else:
				self.id = k
				if(len(driver._decodedkeys) and len(k)): self.id = driver._decodedkeys[0]+","+k
				elif(len(driver._decodedkeys)==1): self.id = driver._decodedkeys[0]
				elif(len(driver._decodedkeys)==2): self.id = driver._decodedkeys[0]+','+driver._decodedkeys[1]
				driver._decodedkeys = [] 
			driver._lastkey = ''
		else:
			if(driver._lastkey == ''): driver._lastkey=brl_keyname(keyindex, driver)
		keys2 = brl_keyname2(keys)
		if(len(keys2) and driver._eab): driver._decodedkeys += [keys2]
