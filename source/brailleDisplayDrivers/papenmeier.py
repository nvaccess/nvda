#brailleDisplayDrivers/papenmeier.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2012-2017 Tobias Platen, Halim Sahin, Ali-Riza Ciftcioglu, NV Access Limited, Davy Kager
#Author: Tobias Platen (nvda@lists.thm.de)
#minor changes by Halim Sahin (nvda@lists.thm.de), Ali-Riza Ciftcioglu <aliminator83@googlemail.com>, James Teh and Davy Kager

import time
from typing import List, Union, Tuple, Optional

import wx
import braille
from logHandler import log

import inputCore
import brailleInput
import keyboardHandler

try:
	import ftdi2
except:
	ftdi2 = None
#for bluetooth
import hwPortUtils
import serial

#for brxcom
import ctypes
import winreg

#for scripting
from baseObject import ScriptableObject

#timer intervalls used by the driver
KEY_CHECK_INTERVAL = 50
BLUETOOTH_INTERVAL = 5000

#Control Flow
STX = 0x02 #Start of Text
ETX = 0x03 #End of Text

#Control Messages
AUTOID = 0x42
BRAILLE = 0x43

#Timeout for bluetooth
BLUETOOTH_TIMEOUT = 0.2

def brl_auto_id() -> bytes:
	"""send auto id command to braille display"""
	# device will respond with a message that allows identification of the display
	return bytes([
		STX, AUTOID, 0x50, 0x50, ETX
	])

def _swapDotBits(d: int) -> List[int]:
	# swap dot bits
	d2 = 0
	if(d & 1): d2|=128
	if(d & 2): d2|=64
	if(d & 4): d2|=32
	if(d & 8): d2|=16
	if(d & 16): d2|=8
	if(d & 32): d2|=4
	if(d & 64): d2|=2
	if(d & 128): d2|=1
	a = 0x30|(d2 & 0x0F)
	b = 0x30|(d2 >> 4)
	return [b, a]

def brl_out(data: List[int], nrk: int, nlk: int, nv: int) -> bytes:
	"""write data to braille cell with nv vertical cells, nrk cells right and nlk cells left
	some papenmeier displays have vertical cells, other displays have dummy cells with keys
	"""
	d2 = len(data) + nv + 2 * nlk + 2 * nrk
	ret = bytearray([
		STX,  # STX
		BRAILLE,  # COMMAND BRAILLE
		# write length to stream
		0x50 | (d2 >> 4),  # big end
		0x50 | (d2 & 0x0F),  # little end
	])

	# fill dummy bytes
	dummyByteCount = (
			2 * nv  # left
			+ 4 * nlk  # vertical
	)
	ret.extend([0x30] * dummyByteCount)

	for d in data:
		ret.extend(_swapDotBits(d))

	#fill dummy bytes on (right)
	ret.extend([0x30] * 4 * nrk)

	#ETX
	ret.append(ETX)
	return bytes(ret)

def brl_poll(dev: serial.Serial) -> bytes:
	"""read sequence from braille display"""
	if dev.inWaiting() > 3:
		status = bytearray(dev.read(4))
		if status[0] == STX:  # first char must be an STX
			if status[1] in [ord(b'K'), ord(b'L')]:
				length = 2 * (((status[2] - 0x50) << 4) + status[3] - 0x50) + 1
			else:
				length = 6
			status.extend(dev.read(length))
			if status[-1] == ETX:
				return bytes(status[1:-1])  # strip STX and ETX
	return b""


class BrailleDisplayDriver(braille.BrailleDisplayDriver, ScriptableObject):
	"""papenmeier braille display driver.
	"""
	_dev: serial.Serial
	name = "papenmeier"
	# Translators: Names of braille displays.
	description = _("Papenmeier BRAILLEX newer models")

	@classmethod
	def check(cls):
		"""should return false if there is a missing dependency"""
		return True

	def connectBrxCom(self):#connect to brxcom server (provided by papenmeier)
		try:
			with winreg.OpenKey(
					winreg.HKEY_LOCAL_MACHINE,
					r"SOFTWARE\FHP\BrxCom"
			) as brxcomkey:
				value, vtype = winreg.QueryValueEx(brxcomkey, "InstallPath")
				assert vtype == winreg.REG_SZ # value is of type: str
			self._brxnvda = ctypes.cdll.LoadLibrary(value + r"\brxnvda.dll")
			if self._brxnvda.brxnvda_init(value + r"\BrxCom.dll"):
				self._baud=1 #prevent bluetooth from connecting
				self.numCells=self._brxnvda.brxnvda_numCells()
				self._voffset=self._brxnvda.brxnvda_numVertCells()
				log.info("Found Braille Display connected via BRXCom")
				self.startTimer()
				return None
		except:
			log.debugWarning("BRXCom is not installed")
			self._brxnvda = None

	def connectBluetooth(self):
		"""try to connect to bluetooth device first, bluetooth is only supported on Braillex Trio"""
		if(self._baud == 0 and self._dev is None):
			for portInfo in sorted(hwPortUtils.listComPorts(onlyAvailable=True), key=lambda item: "bluetoothName" in item):
				port = portInfo["port"]
				hwID = portInfo["hardwareID"]
				if "bluetoothName" in portInfo:
					if portInfo["bluetoothName"][0:14] == "braillex trio " or  portInfo["bluetoothName"][0:13] == "braillex live":
						try:
							self._dev = serial.Serial(port, baudrate = 57600,timeout = BLUETOOTH_TIMEOUT, writeTimeout = BLUETOOTH_TIMEOUT)
							log.info("connectBluetooth success")
						except:
							log.debugWarning("connectBluetooth failed")

	def connectUSB(self, devlist: List[bytes]):
		"""try to connect to usb device,is triggered when BRXCOM is not installed and bluetooth
connection could not be established"""
		try:
			self._dev = ftdi2.open_ex(devlist[0])
			self._dev.set_baud_rate(self._baud)
			self._dev.inWaiting = self._dev.get_queue_status
			log.info("connectUSB success")
		except:
			log.debugWarning("connectUSB failed")

	def __init__(self):
		"""initialize driver"""
		super(BrailleDisplayDriver, self).__init__()
		self.numCells = 0
		self._nlk = 0
		self._nrk = 0
		self.decodedkeys = []
		self._baud = 0
		self._dev = None
		self._proto = None
		devlist: List[bytes] = []
		self.connectBrxCom()
		if(self._baud == 1): return #brxcom is running, skip bluetooth and USB

		#try to connect to usb device,
		#if no usb device is found there may be a bluetooth device
		if ftdi2:
			devlist = ftdi2.list_devices()
		if(len(devlist)==0):
			self.connectBluetooth()
		elif ftdi2:
			self._baud = 57600
			self.connectUSB(devlist)
		if(self._dev is not None):
			try:
				#request type of braille display
				self._dev.write(brl_auto_id())
				time.sleep(0.05)# wait 50 ms in order to get response for further actions
				autoid: bytes = brl_poll(self._dev)
				if autoid == b'':
					#no response, assume a Trio is connected
					self._baud = 115200
					self._dev.set_baud_rate(self._baud)
					self._dev.purge()
					self._dev.read(self._dev.inWaiting())
					#request type of braille display twice because of baudrate change
					self._dev.write(brl_auto_id())
					self._dev.write(brl_auto_id())
					time.sleep(0.05)# wait 50 ms in order to get response for further actions
					autoid = brl_poll(self._dev)
				if len(autoid) != 8:
					return
				else:
					if(autoid[3] == 0x35 and autoid[4] == 0x38):#EL80s
						self.numCells = 80
						self._nlk = 1
						self._nrk = 1
						self._proto = 'A'
						self._voffset = 0
						log.info("Found EL80s")
					elif(autoid[3]==0x35 and autoid[4]==0x3A):#EL70s
						self.numCells = 70
						self._nlk = 1
						self._nrk = 1
						self._proto = 'A'
						self._voffset = 0
						log.info("Found EL70s")
					elif(autoid[3]==0x35 and autoid[4]==0x35):#EL40s
						self.numCells = 40
						self._nlk = 1
						self._nrk = 1
						self._proto = 'A'
						self._voffset = 0
						log.info("Found EL40s")
					elif(autoid[3] == 0x35 and autoid[4] == 0x37):#EL66s
						self.numCells = 66
						self._nlk = 1
						self._nrk = 1
						self._proto = 'A'
						self._voffset = 0
						log.info("Found EL66s")
					elif(autoid[3] == 0x35 and autoid[4] == 0x3E):#EL20c
						self.numCells = 20
						self._nlk = 1
						self._nrk = 1
						self._proto = 'A'
						self._voffset = 0
						log.info("Found EL20c")
					elif(autoid[3] == 0x35 and autoid[4] == 0x3F):#EL40c
						self.numCells = 40
						self._nlk = 1
						self._nrk = 1
						self._proto = 'A'
						self._voffset = 0
						log.info("Found EL40c")
					elif(autoid[3] == 0x36 and autoid[4] == 0x30):#EL60c
						self.numCells = 60
						self._nlk = 1
						self._nrk = 1
						self._proto = 'A'
						self._voffset = 0
						log.info("Found EL60c")
					elif(autoid[3] == 0x36 and autoid[4] == 0x31):#EL80c
						self.numCells = 80
						self._nlk = 1
						self._nrk = 1
						self._proto = 'A'
						self._voffset = 0
						log.info("Found EL80c")
					elif(autoid[3] == 0x35 and autoid[4] == 0x3b):#EL2D80s
						self.numCells = 80
						self._nlk = 1
						self._nrk = 1
						self._proto = 'A'
						self._voffset = 20
						log.info("Found EL2D80s")
					elif(autoid[3] == 0x35 and autoid[4] == 0x39):#trio
						self.numCells = 40
						self._proto = 'B'
						self._voffset = 0
						log.info("Found trio")
					elif(autoid[3] == 0x36 and autoid[4] == 0x34):#live20
						self.numCells = 20
						self._proto = 'B'
						self._voffset = 0
						log.info("Found live 20")
					elif(autoid[3] == 0x36 and autoid[4] == 0x33):#live+
						self.numCells = 40
						self._proto = 'B'
						self._voffset = 0
						log.info("Found live+")
					elif(autoid[3] == 0x36 and autoid[4] == 0x32):#live
						self.numCells = 40
						self._proto = 'B'
						self._voffset = 0
						log.info("Found live")
					else:
						log.debugWarning('UNKNOWN BRAILLE')

			except:
				log.debugWarning('BROKEN PIPE - THIS SHOULD NEVER HAPPEN')
		if(self.numCells == 0): raise Exception('no device found')

		#start keycheck timer
		self.startTimer()
		self.initmapping()

	def startTimer(self):
		"""start timers used by this driver"""
		self._keyCheckTimer = wx.PyTimer(self._handleKeyPresses)
		self._keyCheckTimer.Start(KEY_CHECK_INTERVAL)
		#the keycheck timer polls the braille display for keypresses
		self._bluetoothTimer = wx.PyTimer(self.connectBluetooth)
		self._bluetoothTimer.Start(BLUETOOTH_INTERVAL)
		#the bluetooth timer tries to reconnect if the bluetooth connection is lost

	def stopTimer(self):
		"""stop all timers"""
		try:
			self._keyCheckTimer.Stop()
			self._bluetoothTimer.Stop()
		except:
			pass

		self._keyCheckTimer = None
		self._bluetoothTimer = None

	def initmapping(self):
		if(self._proto == 'A'):
			self._keynamesrepeat = {20: 'up2', 21: 'up', 22: 'dn', 23: 'dn2', 24: 'right', 25: 'left', 26: 'right2', 27: 'left2'}
			x = self.numCells * 2 + 4
			self._keynames = {x+28: 'r1', x+29: 'r2', 20: 'up2', 21: 'up', 22: 'dn', 23: 'dn2', 24: 'right', 25: 'left', 26: 'right2', 27: 'left2', 28: 'l1', 29: 'l2'}
		else:
			self._keynamesrepeat = {16: 'left2', 17: 'right2', 18: 'left', 19: 'right', 20: 'dn2', 21: 'dn', 22: 'up', 23: 'up2'}
			x = self.numCells * 2
			self._keynames = {16: 'left2', 17: 'right2', 18: 'left', 19: 'right', 20: 'dn2', 21: 'dn', 22: 'up', 23: 'up2', x+38: 'r2', x+39: 'r1', 30: 'l2', 31: 'l1'}
			self._dotNames={32: 'd6', 1: 'd1', 2: 'd2', 4: 'd3', 8: 'd4', 64: 'd7', 128: 'd8', 16: 'd5'}
			self._thumbs = {1:"rt", 2:"space", 4:"lt"}

	def terminate(self):
		"""free resources used by this driver"""
		try:
			super(BrailleDisplayDriver, self).terminate()
			self.stopTimer()
			if(self._dev is not None): self._dev.close()
			self._dev=None
			if(self._brxnvda): self._brxnvda.brxnvda_close()
		except:
			self._dev=None

	def display(self, cells: List[int]):
		"""write to braille display"""
		if(self._brxnvda):
			newcells = bytes(cells)
			self._brxnvda.brxnvda_sendToDisplay(newcells)
			return
		if(self._dev is None): return
		try:
			self._dev.write(brl_out(cells, self._nlk, self._nrk, self._voffset))
		except:
			self._dev.close()
			self._dev=None

	def executeGesture(self,gesture):
		"""executes a gesture"""
		if gesture.id or (gesture.dots or gesture.space): inputCore.manager.executeGesture(gesture)

	def _handleKeyPresses(self):
		"""handles key presses and performs a gesture"""
		try:
			if(self._brxnvda):
				k: int = self._brxnvda.brxnvda_keyIndex()
				if(k!=-1):
					self.executeGesture(InputGesture(k,self))
				return
			if(self._dev is None and self._baud>0):
				try:
					devlist: List[bytes] = ftdi2.list_devices()
					if(len(devlist)>0):
						self.connectUSB(devlist)
				except:
					return
			s: bytes = brl_poll(self._dev)
			if s:
				self._repeatcount=0
				ig = InputGesture(s,self)
				self.executeGesture(ig)
			else:
				if(len(self.decodedkeys)):
					ig = InputGesture(None,self)
					self.executeGesture(ig)
		except:
			if(self._dev!=None): self._dev.close()
			self._dev=None

	#global gestures
	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"braille_scrollBack": ("br(papenmeier):left",),
			"braille_scrollForward": ("br(papenmeier):right",),
			"braille_previousLine": ("br(papenmeier):up",),
			"braille_nextLine": ("br(papenmeier):dn",),
			"braille_routeTo": ("br(papenmeier):route",),
			"braille_reportFormatting": ("br(papenmeier):upperRouting",),

			"braille_toggleTether": ("br(papenmeier):r2",),
			"review_currentCharacter": ("br(papenmeier):l1",),
			"review_activate": ("br(papenmeier):l2",),

			"navigatorObject_previous": ("br(papenmeier):left2",),
			"navigatorObject_next": ("br(papenmeier):right2",),
			"navigatorObject_parent": ("br(papenmeier):up2",),
			"navigatorObject_firstChild": ("br(papenmeier):dn2",),

			"title": ("br(papenmeier):l1,up",),
			"reportStatusLine": ("br(papenmeier):l2,dn",),
			"kb:alt": ("br(papenmeier):lt+d3",),
			"kb:control": ("br(papenmeier):lt+d2",),
			"kb:escape": ("br(papenmeier):space+d7",),
			"kb:control+escape": ("br(papenmeier):lt+d1+d2+d3+d4+d5+d6",),
			"kb:tab": ("br(papenmeier):space+d3+d7",),
			"kb:upArrow": ("br(papenmeier):space+d2",),
			"kb:downArrow": ("br(papenmeier):space+d5",),
			"kb:leftArrow": ("br(papenmeier):space+d1",),
			"kb:rightArrow": ("br(papenmeier):space+d4",),
		}
	})

def brl_decode_trio(keys: bytes)->List[int]:
	"""decode routing keys on Trio"""
	if keys[0] == ord(b'K'):  # KEYSTATE CHANGED EVENT on Trio, not Braille keys
		keys = keys[3:]
		i = 0
		j = []
		for k in keys:
			a = k & 0x0F
			#convert bitstream to list of indexes
			if(a & 1): j.append(i+3)
			if(a & 2): j.append(i+2)
			if(a & 4): j.append(i+1)
			if(a & 8): j.append(i)
			i +=4
		return j
	return []

def brl_decode_keys_A(data: bytes, start: int, voffset: int) -> List[int]:
	"""decode routing keys non Trio devices"""
	n = start #key index iterator
	j = []
	shift = 0
	for i, value in enumerate(data):
		if(i%2==0):
			a = value & 0x0F  # n+4,n+3
			b = data[i+1] & 0x0F  # n+2,n+1
			#convert bitstream to list of indexes
			if(n > 26): shift=voffset
			if(b & 1): j.append(n+0-shift)
			if(b & 2): j.append(n+1-shift)
			if(b & 4): j.append(n+2-shift)
			if(b & 8): j.append(n+3-shift)
			if(a & 1): j.append(n+4-shift)
			if(a & 2): j.append(n+5-shift)
			if(a & 4): j.append(n+6-shift)
			if(a & 8): j.append(n+7-shift)
			n+=8
	return j

def brl_decode_key_names_repeat(driver: BrailleDisplayDriver) -> List[str]:
	"""translate key names for protocol A with repeat"""
	driver._repeatcount+=1
	if(driver._repeatcount < 10):
		return []
	else:
		driver._repeatcount = 0
	dec = []
	for key in driver.decodedkeys:
		try:
			dec.append(driver._keynamesrepeat[key])
		except:
			pass
	return dec

def brl_decode_key_names(driver: BrailleDisplayDriver) -> List[str]:
	"""translate key names for protocol A"""
	dec = []
	keys = driver.decodedkeys
	for key in keys:
		try:
			dec.append(driver._keynames[key])
		except:
			pass
	return dec

def brl_join_keys(dec: List[str]) -> str:
	"""join key names with comma, this is used for key combinations"""
	if(len(dec) == 1): return dec[0]
	elif(len(dec) == 3 and dec[0] == dec[1]): return dec[0] + "," + dec[2]
	elif(len(dec) == 3 and dec[0] == dec[2]): return dec[0] + "," + dec[1]
	elif(len(dec) == 2): return dec[1] + "," + dec[0]
	else: return ''

def brl_keyname_decoded(key: int, rest: str) -> str:
	"""convert index used by brxcom to keyname"""
	if(key == 11 or key == 9): return 'l1' + rest
	elif(key == 12 or key == 10): return 'l2' + rest
	elif(key == 13 or key == 15): return 'r1' + rest
	elif(key == 14 or key == 16): return 'r2' + rest

	elif(key == 3): return 'up' + rest
	elif(key == 7): return 'dn' + rest
	elif(key == 1): return 'left' + rest
	elif(key == 5): return 'right' + rest

	elif(key == 4): return 'up2' + rest
	elif(key == 8): return 'dn2' + rest
	elif(key == 2): return 'left2' + rest
	elif(key == 6): return 'right2' + rest
	else: return ''


class InputGesture(braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture):
	"""Input gesture for papenmeier displays"""
	source = BrailleDisplayDriver.name

	def __init__(self, keys: Optional[Union[bytes, int]], driver: BrailleDisplayDriver):
		"""create an input gesture and decode keys"""
		super(InputGesture, self).__init__()
		self.id=''

		if keys is None:
			self.id=brl_join_keys(brl_decode_key_names_repeat(driver))
			return

		if driver._baud != 1 and keys[0] == 'L':
			assert isinstance(keys, bytes)
			if (keys[3] - 48) >> 3:
				scancode = keys[5] - 48 << 4 | keys[6] - 48
				press = not keys[4] & 1
				ext = bool(keys[4] & 2)
				keyboardHandler.injectRawKeyboardInput(press,scancode,ext)
				return
			#get dots
			z = ord(b'0')
			b = keys[4] - z
			c = keys[5] - z
			d = keys[6] - z
			dots = c << 4 | d
			thumbs = b & 7
			if thumbs and dots: 
				names = set()
				names.update(driver._thumbs[1 << i] for i in range(3) if (1 << i) & thumbs)
				names.update(driver._dotNames[1 << i] for i in range(8)if (1 << i) & dots)
				self.id = "+".join(names)
				self.space = True
				self.dots = dots
			elif dots == 64:
				self.id = "d7"
			elif dots == 128:
				self.id = "d8"
			elif thumbs == 2: self.space = True
			else:self.dots = dots
			return

		if(driver._baud==1):#brxcom
			assert isinstance(keys, int)
			if(keys>255 and keys<512):
				self.routingIndex = keys-256-driver._voffset
				self.id = "route"
				return
			elif(keys>511 and keys <786):
				self.routingIndex = keys-512-driver._voffset
				self.id="upperRouting"
				return
			else:
				key1 = (keys & 0xFFFF0000) >> 16
				key2 = keys & 0x0000FFFF
				self.id=brl_keyname_decoded(key1, ',')+brl_keyname_decoded(key2, '')
				return

		if(driver._proto == 'A'):#non trio
			assert isinstance(keys, bytes)
			decodedkeys = brl_decode_keys_A(keys[3:], 4, driver._voffset*2)
		elif(driver._proto=='B'):#trio
			assert isinstance(keys, bytes)
			decodedkeys = brl_decode_trio(keys)
		else:
			decodedkeys: List[int] = []

		length = len(decodedkeys)
		if length == 1 and 32 <= decodedkeys[0] < 32 + driver.numCells * 2:
			#routing keys
			self.routingIndex = (decodedkeys[0] - 32) // 2
			self.id = "route"
			if(decodedkeys[0] % 2 == 1):
				self.id="upperRouting"
		#other keys
		elif length > 0 and length >= len(driver.decodedkeys):
			driver.decodedkeys.extend(decodedkeys)

		elif length == 0 and len(driver.decodedkeys) > 0:
			self.id=brl_join_keys(brl_decode_key_names(driver))
			driver.decodedkeys=[]
