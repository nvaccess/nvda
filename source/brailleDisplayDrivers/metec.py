import controlTypes
import braille
import brailleInput
import queueHandler
from logHandler import log
from ctypes import *
import time
import threading
import wx
import config
import speech
import NVDAObjects
import api
import textInfos
import inputCore
import socket
import ui
import unicodedata


class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	name = "metec"
	description = "Metec Virtual Braille Device"

	@classmethod
	def check(cls):
		return True

	def __init__(self):
		super(BrailleDisplayDriver,self).__init__()
		self._numCells = 20
		self._lock = threading.Lock()
		self._sock = None

		self._keyTimer = wx.PyTimer(self._readKeys)
		self._keyTimer.Start(200)

		self._connectTimer = wx.PyTimer(self._tryconnect)
		self._connectTimer.Start(1000)



	def _tryconnect(self):
		if self._sock is None:
			try:
				log.info("try connect")
				self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self._sock.settimeout(2)
				self._sock.connect(("127.0.0.1", 2018))
				self._sock.settimeout(0.1)
				log.info("connected")

				# Since MVBD version 106
				data = "{cmd}{l0}{l1}{s}".format( cmd=chr(29), l0=chr(1), l1=chr(0), s=chr(2) )
				self._sock.send( data )
				log.info("TcpIpClientRouteIdentifier is NVDA (2)")

				# Since MVBD version 124
				data = "{cmd}{l0}{l1}{mask0}{mask1}{mask2}{mask3}{enabled}".format( cmd=chr(56), l0=chr(5),l1=chr(0),   mask0=chr(64), mask1=chr(0), mask2=chr(0), mask3=chr(0),   enabled=chr(1) )
				self._sock.send( data )
				log.info("Register for Gesture Events")

			except:
				log.info("ERROR connect")
				self._sock.close()
				self._sock = None




	def terminate(self):
		super(BrailleDisplayDriver, self).terminate()
		
		if not self._sock is None:
			self._sock.close()
			self._sock = None

		if not self._keyTimer is None:
			self._keyTimer.Stop()
			self._keyTimer = None

		if not self._connectTimer is None:
			self._connectTimer.Stop()
			self._connectTimer = None




	def _get_numCells(self):
		return self._numCells


	def display(self, cells):
		if self._sock is None: return

		s = "".join(chr(cell) for cell in cells)
		self._SendBrailleString(1, s)






	def _SendBrailleString(self, cmd, s):
		if self._sock is None: return

		# LittleEndian
		#s = s.encode('cp1252')
		l=len(s)
		l0 = (l >> 0 ) & 0xFF
		l1 = (l >> 8 ) & 0xFF
		data = "{cmd}{l0}{l1}{s}".format( cmd=chr(cmd), l0=chr(l0),l1=chr(l1),  s=s )

		with self._lock:
			try:
				self._sock.send( data )
			except:
				log.info("ERROR write")
				self._sock = None








	def _readKeys(self):
		if self._sock is None: return

		try:
			buf = self._sock.recv(4)
			msg = ord(buf[0])

			if msg == 1:
				buf = self._sock.recv(1)
				self._numCells = ord(buf[0])

			elif msg == 30:
				buf = self._sock.recv(4)
					
				b0 = ord(buf[0])
				b1 = ord(buf[1])
				b2 = ord(buf[2])
				b3 = ord(buf[3])
				inputCore.manager.executeGesture( InputGesture(b0,b1,b2,b3) )

		except socket.timeout:
			pass

		except Exception as e:
			log.info( "ERROR _readKeys %s" % e )








#-------key-mapping-------------------------------------------------------------
	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"braille_routeTo": ("br(MVBD):b0",),
			"braille_scrollBack": ("br(MVBD):b1",),
			"braille_scrollForward": ("br(MVBD):b2",),
			"braille_previousLine": ("br(MVBD):b3",),
			"braille_nextLine": ("br(MVBD):b4",),
			"braille_toggleTether": ("br(MVBD):b5",),


			"review_previousWord": ("br(MVBD):b11",),
			"review_previousLine": ("br(MVBD):b12",),
			"review_nextWord": ("br(MVBD):b13",),
			"review_top": ("br(MVBD):b14",),
			"review_currentWord": ("br(MVBD):b15",),

			"kb:leftArrow": ("br(MVBD):b21",),
			"kb:upArrow": ("br(MVBD):b22",),
			"kb:rightArrow": ("br(MVBD):b23",),
			"kb:downArrow": ("br(MVBD):b24",),
			"kb:home": ("br(MVBD):b25",),
			"kb:end": ("br(MVBD):b26",),
			"kb:control+home": ("br(MVBD):b27",),
			"kb:control+end": ("br(MVBD):b28",),
			"kb:control+leftArrow": ("br(MVBD):b29",),
			"kb:control+rightArrow": ("br(MVBD):b30",),
			"kb:control+escape": ("br(MVBD):b32",),
			"kb:control+a": ("br(MVBD):b33",),
			"kb:control+c": ("br(MVBD):b34",),
			"kb:control+v": ("br(MVBD):b35",),
			"kb:windows": ("br(MVBD):b36",),
			"kb:windows+d": ("br(MVBD):b37",),
			"kb:windows+q": ("br(MVBD):b38",),
			"kb:tab": ("br(MVBD):b39",),
			"kb:shift+tab": ("br(MVBD):b40",),
			"kb:alt+tab": ("br(MVBD):b41",),
			"kb:escape": ("br(MVBD):b42",),
			"kb:enter": ("br(MVBD):b43",),
			"kb:backspace": ("br(MVBD):b44",),
			"kb:delete": ("br(MVBD):b45",),


			"activateGeneralSettingsDialog": ("br(MVBD):b51",),
			"activateSynthesizerDialog": ("br(MVBD):b52",),
			"activateVoiceDialog": ("br(MVBD):b53",),
			"activateKeyboardSettingsDialog": ("br(MVBD):b54",),
			"activateObjectPresentationDialog": ("br(MVBD):b55",),
			"activateBrowseModeDialog": ("br(MVBD):b56",),
			"activateDocumentFormattingDialog": ("br(MVBD):b57",),


			"say_battery_status": ("br(MVBD):b61",),
			"showGui": ("br(MVBD):b62",),
			"title": ("br(MVBD):b63",),
			"dateTime": ("br(MVBD):b64",),
			"sayAll": ("br(MVBD):b65",),
			"reportCurrentLine": ("br(MVBD):b66",),
			"quit": ("br(MVBD):b67",),
			"toggleCurrentAppSleepMode": ("br(MVBD):b68",),


			"leftMouseClick": ("br(MVBD):b81",),
			"rightMouseClick": ("br(MVBD):b82",),
			"toggleLeftMouseButton": ("br(MVBD):b83",),
			"toggleRightMouseButton": ("br(MVBD):b84",),
			"moveMouseToNavigatorObject": ("br(MVBD):b85",),
			"moveNavigatorObjectToMouse": ("br(MVBD):b86",),




		}
	})






class InputGesture(braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture):

	source = BrailleDisplayDriver.name

	def __init__(self, b0,b1,b2,b3):
		super(InputGesture, self).__init__()
		
		self.id = ""
		if b0 != 0xFF: self.id = "b" + str(b0)
		if b1 != 0xFF: self.routingIndex = b1
		if b2 != 0xFF: self.dots = b2
		if b3 != 0xFF: self.space = b3

		#log.info("id: " + self.id)


