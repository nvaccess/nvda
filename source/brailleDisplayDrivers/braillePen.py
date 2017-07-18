#brailleDisplayDrivers/braillePen.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2014 Harpo Sp. z o. o. <http://www.harpo.com.pl>

import braille
import queueHandler
from logHandler import log
from ctypes import *
from ctypes.wintypes import *
import time
import config
import inputCore
import hwPortUtils
import brailleInput
import wx
import hwIo

BAUD_RATE = 115200
TIMEOUT = 0.1

BP12_BRAILLE_KEYS = ("dot1", "dot2", "dot3", "dot4", "dot5", "dot6","dot7","dot8" )

def _findPorts():
	for portInfo in hwPortUtils.listComPorts(onlyAvailable=True):
		try:
			btName = portInfo["bluetoothName"]
		except KeyError:
			continue
		if btName.startswith("BraillePen") or btName.startswith("EasyLink"):
			yield portInfo["port"]

class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	name = "braillePen"
	# Translators: Names of braille displays.
	description = _("BraillePen Slim")
	isThreadSafe = True

	@classmethod
	def check(cls):
		return True

	def __init__(self):
		super(BrailleDisplayDriver, self).__init__()
		self.numCells = 0
		for port in _findPorts():
			try:
				self._dev = hwIo.Serial(port, baudrate=BAUD_RATE, timeout=TIMEOUT, writeTimeout=TIMEOUT, onReceive=self._serOnReceive)
			except EnvironmentError:
				log.info("BraillePen open port error")
				continue			
			break
		else:
			raise RuntimeError("BraillePen not found")
				
	def terminate(self):
		try:
			super(BrailleDisplayDriver, self).terminate()
		finally:
			self._dev.close()
		
	def _serOnReceive(self,data):
		braille=None
		command=None
		braille=data
		command=self._dev.read(1)
		self._serHandleResponse(braille, command)

	def _serHandleResponse(self,braille,command):		
		if braille is not None and command is not None:
			try:
				inputCore.manager.executeGesture(InputGesture(braille, command))
			except inputCore.NoInputGestureAction:
				pass
	
	def display(self, cells):
		pass

	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"kb:upArrow": ("br(braillePen):space+dot1",),
			"kb:downArrow": ("br(braillePen):space+dot4",),
			"kb:leftArrow": ("br(braillePen):space+dot3",),
			"kb:rightArrow": ("br(braillePen):space+dot6",),
			"kb:enter": ("br(braillePen):space+dot8"),			
			"kb:backspace": ("br(braillePen):space+dot7","br(braillePen):space+dot1+dot2"),
			"kb:delete": ("br(braillePen):space+dot1+dot4+dot5",),
			"kb:windows": ("br(braillePen):space+dot3+dot4",),
			"kb:alt": ("br(braillePen):space+dot1+dot3+dot4",),
			"kb:escape": ("br(braillePen):space+dot1+dot5",),
			"kb:shift+tab": ("br(braillePen):space+dot2+dot3+dot4+dot5+dot8",),
			"kb:tab": ("br(braillePen):space+dot2+dot3+dot4+dot5+dot7",),			
			"toggleInputHelp": ("br(braillePen):space+dot3+dot6+dot7",),
			"braille_toggleTether": ("br(braillePen):space+dot1+dot2+dot6",),
			"kb:home": ("br(braillePen):space+dot2+dot3",),
			"kb:end": ("br(braillePen):space+dot5+dot6",),
			"sayAll": ("br(braillePen):space+dot1+dot2+dot4+dot5+dot6",),
			"dateTime": ("br(braillePen):space+dot2+dot3+dot4",),
			"reportCurrentSelection": ("br(braillePen):space+dot1+dot2+dot4+dot5+dot6+dot7",),
			"showGui": ("br(braillePen):space+dot1+dot2+dot4+dot5",),
			"kb:alt+tab": ("br(braillePen):space+dot1+dot3+dot5",),
			"say_battery_status": ("br(braillePen):space+dot1+dot2+dot7",),
			"title": ("br(braillePen):space+dot2+dot3+dot4+dot5",),
			"reportCurrentFocus": ("br(braillePen):space+dot1+dot2+dot4+dot7",),
			"reportStatusLine": ("br(braillePen):space+dot2+dot3+dot4+dot7",),
			"speakForeground": ("br(braillePen):space+dot1+dot2+dot4+dot5+dot7",),
			"kb:control+leftArrow": ("br(braillePen):space+dot2",),
			"kb:control+rightArrow": ("br(braillePen):space+dot5",),
			"kb:control+home": ("br(braillePen):space+dot2+dot3+dot7",),
			"kb:control+end": ("br(braillePen):space+dot5+dot6+dot7",),
		},
	})

class InputGesture(braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture):

	source = BrailleDisplayDriver.name

	def __init__(self, brailleKeys,controlKeys):
		super(InputGesture, self).__init__()
		spaceKey=False
		brailleKeysExtended = ord(brailleKeys)
		controlKeysExtended = ord(controlKeys)
		if controlKeysExtended & 1 >0:
			spaceKey=True
		if controlKeysExtended & 2 >0:
			brailleKeysExtended = brailleKeysExtended | 0x40
		if controlKeysExtended & 4 >0:
			brailleKeysExtended = brailleKeysExtended | 0x80
		brailleKeysList=[BP12_BRAILLE_KEYS[num] for num in xrange(8) if (brailleKeysExtended>>num)&1]
		spaceKeyList = ["space"]
		if spaceKey:
			selectedKeys=spaceKeyList+brailleKeysList
		else:
			selectedKeys=brailleKeysList
		self.id="+".join(set(selectedKeys))
		self.keys = set(selectedKeys)
		self.keyNames = names = set()
		if brailleKeysExtended!=0 and spaceKey==False:
			self.dots =brailleKeysExtended		
		if brailleKeysExtended==0 and spaceKey==True:
			self.space = True
		log.info(self.id)
