#keyboardHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Keyboard support"""

import winUser
import ctypes
import time
import winsound
import pyHook
import nvwh
import debug
import speech
from keyUtils import key, keyName, sendKey
import scriptHandler
import globalVars
import queueHandler
import config
import locale

keyUpIgnoreSet=set()
passKeyThroughCount=-1 #If 0 or higher then key downs and key ups will be passed straight through
NVDAModifierKey=None
usedNVDAModifierKey=False
lastNVDAModifierKey=None
lastNVDAModifierKeyTime=None

def passNextKeyThrough():
	global passKeyThroughCount
	if passKeyThroughCount==-1:
		passKeyThroughCount=0

def isNVDAModifierKey(vkCode,extended):
	if config.conf["keyboard"]["useNumpadInsertAsNVDAModifierKey"] and vkCode==winUser.VK_INSERT and not extended:
		return True
	elif config.conf["keyboard"]["useExtendedInsertAsNVDAModifierKey"] and vkCode==winUser.VK_INSERT and extended:
		return True
	elif config.conf["keyboard"]["useCapsLockAsNVDAModifierKey"] and vkCode==winUser.VK_CAPITAL:
		return True
	else:
		return False

def speakToggleKey(vkCode):
	toggleState=bool(not winUser.getKeyState(vkCode)&1)
	if vkCode==winUser.VK_CAPITAL:
			queueHandler.queueFunction(queueHandler.interactiveQueue,speech.speakMessage,_("caps lock %s")%(_("on") if toggleState else _("off")))
	elif vkCode==winUser.VK_NUMLOCK:
			queueHandler.queueFunction(queueHandler.interactiveQueue,speech.speakMessage,_("num lock %s")%(_("on") if toggleState else _("off")))
	elif vkCode==winUser.VK_SCROLL:
			queueHandler.queueFunction(queueHandler.interactiveQueue,speech.speakMessage,_("scroll lock %s")%(_("on") if toggleState else _("off")))

@nvwh.userKeyCallbackType
def internal_keyDownEvent(keyInfo):
	"""Event called by pyHook when it receives a keyDown. It sees if there is a script tied to this key and if so executes it. It also handles the speaking of characters, words and command keys.
"""
	try:
		global NVDAModifierKey, usedNVDAModifierKey, lastNVDAModifierKey, lastNVDAModifierKeyTime, passKeyThroughCount
		#Injected keys should be ignored
		if keyInfo.injected:
			return True
		if passKeyThroughCount>=0:
			passKeyThroughCount+=1
			return True
		if not speech.beenCanceled:
			queueHandler.queueFunction(queueHandler.interactiveQueue,speech.cancelSpeech)
		vkName=pyHook.HookConstants.IDToName(keyInfo.vkCode)
		globalVars.keyCounter+=1
		if lastNVDAModifierKey and (keyInfo.vkCode,keyInfo.extended)==lastNVDAModifierKey:
			lastNVDAModifierKey=None
			if (time.time()-lastNVDAModifierKeyTime)<0.5:
				speakToggleKey(keyInfo.vkCode)
				return True
		lastNVDAModifierKey=None
		if isNVDAModifierKey(keyInfo.vkCode,keyInfo.extended):
			NVDAModifierKey=(keyInfo.vkCode,keyInfo.extended)
			return False
		if keyInfo.vkCode in [winUser.VK_CONTROL,winUser.VK_LCONTROL,winUser.VK_RCONTROL,winUser.VK_SHIFT,winUser.VK_LSHIFT,winUser.VK_RSHIFT,winUser.VK_MENU,winUser.VK_LMENU,winUser.VK_RMENU,winUser.VK_LWIN,winUser.VK_RWIN]:
			return True
		modifierList=[]
		if NVDAModifierKey:
			modifierList.append("NVDA")
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
		if globalVars.keyboardHelp or (config.conf["keyboard"]["speakCommandKeys"] and not ( not keyPress[0] and config.conf["keyboard"]["speakTypedCharacters"])):
			labelList=[]
			if keyPress[0] is not None:
				labelList.extend(keyPress[0])
			ch=ctypes.windll.user32.MapVirtualKeyW(keyInfo.vkCode,winUser.MAPVK_VK_TO_CHAR)
			if ch>32:
				labelList.append(unichr(ch))
			else:
				labelList.append(keyPress[1])
			queueHandler.queueFunction(queueHandler.interactiveQueue,speech.speakMessage,"+".join(labelList))
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
			keyUpIgnoreSet.add((keyInfo.vkCode,keyInfo.extended))
			if NVDAModifierKey:
				usedNVDAModifierKey=True 
			return False
		else:
			speakToggleKey(keyInfo.vkCode)
			return True
	except:
		debug.writeException("keyboardHandler.internal_keyDownEvent")
		speech.speakMessage("Error in keyboardHandler.internal_keyDownEvent",wait=True)
		return True

@nvwh.userKeyCallbackType
def internal_keyUpEvent(keyInfo):
	"""Event that pyHook calls when it receives keyUps"""
	try:
		global NVDAModifierKey, usedNVDAModifierKey, lastNVDAModifierKey, lastNVDAModifierKeyTime, passKeyThroughCount
		if keyInfo.injected:
			return True
		elif passKeyThroughCount>=1:
			passKeyThroughCount-=1
			if passKeyThroughCount==0:
				passKeyThroughCount=-1
			return True
		elif NVDAModifierKey and (keyInfo.vkCode,keyInfo.extended)==NVDAModifierKey:
			if not usedNVDAModifierKey:
				lastNVDAModifierKey=NVDAModifierKey
				lastNVDAModifierKeyTime=time.time()
			NVDAModifierKey=None
			usedNVDAModifierKey=False
			return False
		elif (keyInfo.vkCode,keyInfo.extended) in keyUpIgnoreSet:
			keyUpIgnoreSet.remove((keyInfo.vkCode,keyInfo.extended))
			return False
		elif keyInfo.vkCode in [winUser.VK_CONTROL,winUser.VK_LCONTROL,winUser.VK_RCONTROL,winUser.VK_SHIFT,winUser.VK_LSHIFT,winUser.VK_RSHIFT,winUser.VK_MENU,winUser.VK_LMENU,winUser.VK_RMENU,winUser.VK_LWIN,winUser.VK_RWIN]:
			return True
		else:
			return True
	except:
		debug.writeException("keyboardHandler.internal_keyUpEvent")
		speech.speakMessage("Error in keyboardHandler.internal_keyUpEvent",wait=True)
		return True

@nvwh.userCharCallbackType
def internal_typeCharacterEvent(ch):
	if ch>=32:
		queueHandler.queueFunction(queueHandler.eventQueue,speech.speakTypedCharacters,unichr(ch))

#Register internal key press event with  operating system

def initialize():
	"""Initialises keyboard support."""
	nvwh.setUserKeyUpCallback(internal_keyUpEvent)
	nvwh.setUserKeyDownCallback(internal_keyDownEvent)
	nvwh.setUserCharCallback(internal_typeCharacterEvent)
	nvwh.registerKeyHook()
	nvwh.registerCharHook()

def terminate():
	nvwh.unregisterCharHook()
	nvwh.unregisterKeyHook()
