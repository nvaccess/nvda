#keyboardHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Keyboard support"""

import winUser
import time
import pyHook
import nvwh
import debug
import speech
from keyUtils import key, keyName
import scriptHandler
import globalVars
import queueHandler
import config
import locale

keyUpIgnoreSet=set()
passKeyThroughCount=-1 #If 0 or higher then key downs and key ups will be passed straight through
insertDown=False
word=""
hookManager=None


def passNextKeyThrough():
	global passKeyThroughCount
	if passKeyThroughCount==-1:
		passKeyThroughCount=0

#Internal functions for key presses

@nvwh.userKeyCallbackType
def internal_keyDownEvent(keyInfo):
	"""Event called by pyHook when it receives a keyDown. It sees if there is a script tied to this key and if so executes it. It also handles the speaking of characters, words and command keys.
"""
	global insertDown, passKeyThroughCount
	vkName=pyHook.HookConstants.IDToName(keyInfo.vkCode)
	if passKeyThroughCount>=0:
		passKeyThroughCount+=1
		return True
	try:
		if keyInfo.injected:
			return True
		globalVars.keyCounter+=1
		if not speech.beenCanceled:
			queueHandler.queueFunction(queueHandler.interactiveQueue,speech.cancelSpeech)
		if keyInfo.vkCode in [winUser.VK_CONTROL,winUser.VK_LCONTROL,winUser.VK_RCONTROL,winUser.VK_SHIFT,winUser.VK_LSHIFT,winUser.VK_RSHIFT,winUser.VK_MENU,winUser.VK_LMENU,winUser.VK_RMENU,winUser.VK_LWIN,winUser.VK_RWIN]:
			return True
		if (vkName=="Insert"): #and (keyInfo.extended==0):
			insertDown=True
			return False
		modifierList=[]
		if insertDown:
			modifierList.append("Insert")
		if winUser.getKeyState(winUser.VK_CONTROL)&32768:
			modifierList.append("Control")
		if winUser.getKeyState(winUser.VK_SHIFT)&32768:
			modifierList.append("Shift")
		if winUser.getKeyState(winUser.VK_MENU)&32768:
			modifierList.append("Alt")
		if winUser.getKeyState(winUser.VK_LWIN)&32768:
			modifierList.append("Win")
		if winUser.getKeyState(winUser.VK_RWIN)&32768:
			modifierList.append("Win")
		if len(modifierList) > 0:
			modifiers=frozenset(modifierList)
		else:
			modifiers=None
		mainKey=vkName
		if keyInfo.extended==1:
			mainKey="Extended%s"%mainKey
		keyPress=(modifiers,mainKey)
		debug.writeMessage("key press: %s"%keyName(keyPress))
		if mainKey=="Capital":
			capState=bool(not winUser.getKeyState(winUser.VK_CAPITAL)&1)
			queueHandler.queueFunction(queueHandler.interactiveQueue,speech.speakMessage,_("caps lock %s")%(_("on") if capState else _("off")))
		elif mainKey=="ExtendedNumlock":
			numState=bool(not winUser.getKeyState(winUser.VK_NUMLOCK)&1)
			queueHandler.queueFunction(queueHandler.interactiveQueue,speech.speakMessage,_("num lock %s")%(_("on") if numState else _("off")))
		script=scriptHandler.findScript(keyPress)
		if script:
			scriptName=scriptHandler.getScriptName(script)
			scriptLocation=scriptHandler.getScriptLocation(script)
			scriptDescription=scriptHandler.getScriptDescription(script)
			if globalVars.keyboardHelp and scriptName!="keyboardHelp":
				queueHandler.queueFunction(queueHandler.interactiveQueue,speech.speakMessage,"%s"%scriptName.replace('_',' '))
				queueHandler.queueFunction(queueHandler.interactiveQueue,speech.speakMessage,_("Description: %s")%scriptDescription)
				queueHandler.queueFunction(queueHandler.interactiveQueue,speech.speakMessage,_("Location: %s")%scriptLocation)
			else:
				queueHandler.queueFunction(queueHandler.interactiveQueue,script,keyPress)
		if script or globalVars.keyboardHelp:
			keyUpIgnoreSet.add((vkName,keyInfo.extended))
			return False
		else:
			return True
	except:
		debug.writeException("keyboardHandler.internal_keyDownEvent")
		speech.speakMessage("Error in keyboardHandler.internal_keyDownEvent",wait=True)
		return True

@nvwh.userKeyCallbackType
def internal_keyUpEvent(keyInfo):
	"""Event that pyHook calls when it receives keyUps"""
	global insertDown, passKeyThroughCount
	try:
		vkName=pyHook.HookConstants.IDToName(keyInfo.vkCode)
		if keyInfo.injected:
			return True
		elif passKeyThroughCount>=1:
			passKeyThroughCount-=1
			if passKeyThroughCount==0:
				passKeyThroughCount=-1
			return True
		elif (vkName,keyInfo.extended) in keyUpIgnoreSet:
			keyUpIgnoreSet.remove((vkName,keyInfo.extended))
			return False
		elif keyInfo.vkCode in [winUser.VK_CONTROL,winUser.VK_LCONTROL,winUser.VK_RCONTROL,winUser.VK_SHIFT,winUser.VK_LSHIFT,winUser.VK_RSHIFT,winUser.VK_MENU,winUser.VK_LMENU,winUser.VK_RMENU,winUser.VK_LWIN,winUser.VK_RWIN]:
			return True
		elif (vkName=="Insert"): #and (keyInfo.extended==0):
			insertDown=False
			return False
		else:
			return True
	except:
		debug.writeException("keyboardHandler.internal_keyUpEvent")
		speech.speakMessage("Error in keyboardHandler.internal_keyUpEvent",wait=True)
		return True

@nvwh.userCharCallbackType
def internal_typeCharacterEvent(ch):
	queueHandler.queueFunction(queueHandler.interactiveQueue,speech.speakTypedCharacters,unichr(ch))

#Register internal key press event with  operating system

def initialize():
	"""Initialises keyboard support."""
	global hookManager
	nvwh.setUserKeyUpCallback(internal_keyUpEvent)
	nvwh.setUserKeyDownCallback(internal_keyDownEvent)
	nvwh.setUserCharCallback(internal_typeCharacterEvent)
	nvwh.registerKeyHook()
	nvwh.registerCharHook()

def pumpAll():
	nvwh.pumpCharQueue()

def terminate():
	nvwh.unregisterCharHook()
	nvwh.unregisterKeyHook()
