#brailleDisplayDrivers/braillePen12.py
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

READ_INTERVAL = 50

BP12_KEYCALLBACKHANDLE = WINFUNCTYPE(None,c_ubyte,c_ubyte,c_ubyte,c_ubyte,c_ubyte,c_ubyte,c_ubyte,c_ubyte)



BP12_BRAILLE_KEYS = ("dot1", "dot2", "dot3", "dot4", "dot5", "dot6", "dot7", "dot8")
BP12_CONTROL_KEYS=("leftScroll","joyAction","joyLeft","joyUp","joyDown","joyRight","space", "rightScroll")

#Try to load BP12TI32.dll
try:
	BP12Lib=windll[r"brailleDisplayDrivers\BP12TI.dll"]
except:
	BP12Lib=None

def _findPorts():
	for portInfo in hwPortUtils.listComPorts(onlyAvailable=True):
		try:
			btName = portInfo["bluetoothName"]
		except KeyError:
			continue
		if btName.startswith("EL12-"):
			yield portInfo["port"]

class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	name = "braillePen12"
	description = _("BP12 and EL12 series")

	@classmethod
	def check(cls):
		return bool(BP12Lib)

	def __init__(self):
		super(BrailleDisplayDriver,self).__init__()
		self.numCells = 12
		
		
		for port in _findPorts():
		
			if not port:
				raise RuntimeError("No BP12 display found")
				continue
		
			portName=u"{port}".format(port=port)
			self._keyCallbackInst = BP12_KEYCALLBACKHANDLE(self._keyCallback)
			
			result=0
			
			try:
				result=BP12Lib.open(portName,self._keyCallbackInst)
			except:
				result=0
		
			if result >0:
				self._connectedState=True
				break
		else:
			raise RuntimeError("No BP12 display found")

	def terminate(self):
		super(BrailleDisplayDriver, self).terminate()
		try:
			BP12Lib.close()
		except:
			pass

	def handleResponses(self):
		pass
		
	def display(self, cells):
		try:
			arr="".join([chr(x) for x in cells])
			if self._connectedState==True:
				result=BP12Lib.sendBraille(0,len(cells),arr)
				if result<0:
					self._connectedState=False
		except:
			pass

	def _keyCallback(self, braille, system, coursor1, coursor2, coursor3, coursor4, coursor5, coursor6):
		if braille!=0 or system!=0 or coursor1!=0:
			try:
				inputCore.manager.executeGesture(InputGesture(braille, system, coursor1))
			except inputCore.NoInputGestureAction:
				pass
				
		return
		
	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"braille_scrollBack": ("br(braillePen12):leftScroll",),
			"braille_scrollForward": ("br(braillePen12):rightScroll",),
			"braille_routeTo": ("br(braillePen12):routing",),
			"kb:upArrow": ("br(braillePen12):joyUp",),
			"kb:downArrow": ("br(braillePen12):joyDown",),
			"kb:leftArrow": ("br(braillePen12):joyLeft",),
			"kb:rightArrow": ("br(braillePen12):joyRight",),
			"kb:enter": ("br(braillePen12):joyAction","br(braillePen12):space+dot8"),			
			"kb:backspace": ("br(braillePen12):space+dot7","br(braillePen12):space+dot1+dot2"),
			"kb:delete": ("br(braillePen12):space+dot1+dot4+dot5",),
			"kb:windows": ("br(braillePen12):space+dot3+dot4",),
			"kb:alt": ("br(braillePen12):space+dot1+dot3+dot4",),
			"kb:escape": ("br(braillePen12):space+dot1+dot5",),
			"braille_previousLine": ("br(braillePen12):joyUp+space",),
			"braille_nextLine": ("br(braillePen12):joyDown+space",),
			"kb:shift+tab": ("br(braillePen12):space+joyLeft",),
			"kb:tab": ("br(braillePen12):space+joyRight",),			
			"review_nextWord": ("br(braillePen12):space+dot5",),
			"review_previousWord": ("br(braillePen12):space+dot2",),
			"review_nextLine": ("br(braillePen12):space+dot4",),
			"review_previousLine": ("br(braillePen12):space+dot1",),
			"review_nextCharacter": ("br(braillePen12):space+dot6",),
			"review_previousCharacter": ("br(braillePen12):space+dot3",),
			"toggleInputHelp": ("br(braillePen12):space+dot3+dot6+dot7",),
			"braille_toggleTether": ("br(braillePen12):space+dot1+dot2+dot6",),
			"kb:home": ("br(braillePen12):space+dot2+dot3",),
			"kb:end": ("br(braillePen12):space+dot5+dot6",),
			"review_top": ("br(braillePen12):space+dot1+dot2+dot3",),			
			"review_bottom": ("br(braillePen12):space+dot4+dot5+dot6",),
			"sayAll": ("br(braillePen12):space+dot1+dot2+dot4+dot5+dot6",),
			"review_currentCharacter": ("br(braillePen12):space+dot3+dot6",),
			"review_currentWord": ("br(braillePen12):space+dot2+dot5",),
			"review_currentLine": ("br(braillePen12):space+dot1+dot4",),
			"dateTime": ("br(braillePen12):space+dot2+dot3+dot4",),
			"reportCurrentSelection": ("br(braillePen12):space+dot1+dot2+dot4+dot5+dot6+dot7",),
			"showGui": ("br(braillePen12):space+dot1+dot2+dot4+dot5",),
			"kb:alt+tab": ("br(braillePen12):space+dot1+dot3+dot5",),
			"say_battery_status": ("br(braillePen12):space+dot1+dot2+dot7",),
			"review_markStartForCopy": ("br(braillePen12):space+dot1+dot4+dot7",),
			"review_copy": ("br(braillePen12):space+dot1+dot4+dot8",),
			"reportClipboardText": ("br(braillePen12):space+dot1+dot2+dot3+dot6+dot8",),
			"kb:control+v": ("br(braillePen12):space+dot1+dot2+dot3+dot6+dot7",),
			"review_sayAll": ("br(braillePen12):space+dot1+dot3+dot4+dot5+dot6",),
			"reviewMode_next": ("br(braillePen12):space+joyRight+dot7",),
			"reviewMode_previous": ("br(braillePen12):space+joyLeft+dot7",),
			"review_activate": ("br(braillePen12):joyAction+space",),
			"title": ("br(braillePen12):space+dot2+dot3+dot4+dot5",),
			"reportCurrentFocus": ("br(braillePen12):space+dot1+dot2+dot4+dot7",),
			"reportStatusLine": ("br(braillePen12):space+dot2+dot3+dot4+dot7",),
			"speakForeground": ("br(braillePen12):space+dot1+dot2+dot4+dot5+dot7",),
			"toggleCaretMovesReviewCursor": ("br(braillePen12):joyAction+space+dot7",),
			"kb:control+leftArrow": ("br(braillePen12):space+joyLeft+dot8",),
			"kb:control+rightArrow": ("br(braillePen12):space+joyRight+dot8",),
			"kb:control+home": ("br(braillePen12):space+joyUp+dot8",),
			"kb:control+end": ("br(braillePen12):space+joyDown+dot8",),
		},
	})

class InputGesture(braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture):

	source = BrailleDisplayDriver.name

	def __init__(self, brailleKeys,controlKeys,routingKey):
		super(InputGesture, self).__init__()
		
		brailleKeysList=[BP12_BRAILLE_KEYS[num] for num in xrange(8) if (brailleKeys>>num)&1]
		controlKeysList=[BP12_CONTROL_KEYS[num] for num in xrange(8) if (controlKeys>>num)&1]
		routingKeyList = ["routing"]
		
		if routingKey==0:
			selectedKeys=controlKeysList+brailleKeysList
		else:
			selectedKeys=controlKeysList+brailleKeysList+routingKeyList
		
		self.id="+".join(set(selectedKeys))
		self.keys = set(selectedKeys)
			
		
		self.keyNames = names = set()
		
		if brailleKeys!=0 and controlKeys==0 and routingKey==0:
			self.dots =brailleKeys
		
		if brailleKeys==0 and controlKeys==64 and routingKey==0:
			self.space = True
			
		if routingKey !=0:
			self.routingIndex = routingKey -1
		
		log.info(self.id)
