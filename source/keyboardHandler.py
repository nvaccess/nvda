#keyboardHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Keyboard support"""

import locale
import winUser
import ctypes
import time
import vkCodes
import speech
from keyUtils import key, keyName, sendKey, localizedKeyLabels
import scriptHandler
import globalVars
from logHandler import log
import queueHandler
import config
import _winreg
import api
import winInputHook
import watchdog

keyUpIgnoreSet=set()
passKeyThroughCount=-1 #If 0 or higher then key downs and key ups will be passed straight through
NVDAModifierKey=None
usedNVDAModifierKey=False
lastNVDAModifierKey=None
lastNVDAModifierKeyTime=None
unpauseByShiftUp=False

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
			queueHandler.queueFunction(queueHandler.eventQueue,speech.speakMessage,_("caps lock %s")%(_("on") if toggleState else _("off")))
	elif vkCode==winUser.VK_NUMLOCK:
			queueHandler.queueFunction(queueHandler.eventQueue,speech.speakMessage,_("num lock %s")%(_("on") if toggleState else _("off")))
	elif vkCode==winUser.VK_SCROLL:
			queueHandler.queueFunction(queueHandler.eventQueue,speech.speakMessage,_("scroll lock %s")%(_("on") if toggleState else _("off")))

def speakKeyboardLayout(layout):
	try:
		s = hex(winUser.LOWORD(layout))[2:].rjust(8, "0")
		key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Control\\Keyboard Layouts\\"+ s)
	except:
		s = hex(winUser.HIWORD(layout))[2:].rjust(8, "0")
		key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Control\\Keyboard Layouts\\"+ s)
	try:
		s = _winreg.QueryValueEx(key, "Layout Display Name")[0]
	except:
		s=None
	if s is not None and isinstance(s,basestring):
		buf=ctypes.create_unicode_buffer(256)
		ctypes.windll.shlwapi.SHLoadIndirectString(s,buf,256,None)
		s=buf.value
	else:
		s = _winreg.QueryValueEx(key, "Layout Text")[0]
	key.Close()
	queueHandler.queueFunction(queueHandler.eventQueue,speech.speakMessage,_("%s keyboard layout")%s)

def internal_keyDownEvent(vkCode,scanCode,extended,injected):
	"""Event called by keyHook when it receives a keyDown. It sees if there is a script tied to this key and if so executes it. It also handles the speaking of characters, words and command keys.
"""
	try:
		global NVDAModifierKey, usedNVDAModifierKey, lastNVDAModifierKey, lastNVDAModifierKeyTime, passKeyThroughCount, unpauseByShiftUp 
		if watchdog.isAttemptingRecovery:
			# The core is dead, so let keys pass through unhindered.
			return True
		focusObject=api.getFocusObject()
		focusAppModule=focusObject.appModule
		if focusAppModule and focusAppModule.selfVoicing:
			return True
		#Injected keys should be ignored
		if injected:
			return True
		if passKeyThroughCount>=0:
			passKeyThroughCount+=1
			return True
		#pass the volume controlling keys
		if extended and vkCode >= winUser.VK_VOLUME_MUTE and vkCode <= winUser.VK_VOLUME_UP: return True
		vkName=vkCodes.byCode.get(vkCode,"").lower()
		vkChar=ctypes.windll.user32.MapVirtualKeyW(vkCode,winUser.MAPVK_VK_TO_CHAR)
		if vkName.startswith('oem') or not vkName:
			if 32<vkCode<128:
				vkName=unichr(vkCode).lower()
			elif 32<vkChar<128:
				vkName=unichr(vkChar).lower()
		if vkCode in (winUser.VK_CONTROL,winUser.VK_LCONTROL,winUser.VK_RCONTROL,winUser.VK_SHIFT,winUser.VK_LSHIFT,winUser.VK_RSHIFT):
			if speech.isPaused:
				unpauseByShiftUp=True
			else:
				queueHandler.queueFunction(queueHandler.eventQueue,speech.pauseSpeech,True)
		else:
			unpauseByShiftUp=False
			globalVars.keyCounter+=1
			queueHandler.queueFunction(queueHandler.eventQueue,speech.cancelSpeech)
		if lastNVDAModifierKey and (vkCode,extended)==lastNVDAModifierKey:
			lastNVDAModifierKey=None
			if (time.time()-lastNVDAModifierKeyTime)<0.5:
				speakToggleKey(vkCode)
				return True
		lastNVDAModifierKey=None
		if isNVDAModifierKey(vkCode,extended):
			NVDAModifierKey=(vkCode,extended)
			if not globalVars.keyboardHelp:
				return False
		if not globalVars.keyboardHelp and vkCode in [winUser.VK_CONTROL,winUser.VK_LCONTROL,winUser.VK_RCONTROL,winUser.VK_SHIFT,winUser.VK_LSHIFT,winUser.VK_RSHIFT,winUser.VK_MENU,winUser.VK_LMENU,winUser.VK_RMENU,winUser.VK_LWIN,winUser.VK_RWIN]:
			return True
		modifierList=[]
		if NVDAModifierKey:
			modifierList.append("nvda")
		if not vkCode in [winUser.VK_CONTROL,winUser.VK_LCONTROL,winUser.VK_RCONTROL] and winUser.getKeyState(winUser.VK_CONTROL)&32768:
			modifierList.append("control")
		if not vkCode in [winUser.VK_SHIFT,winUser.VK_LSHIFT,winUser.VK_RSHIFT] and winUser.getKeyState(winUser.VK_SHIFT)&32768:
			modifierList.append("shift")
		if not vkCode in [winUser.VK_MENU,winUser.VK_LMENU,winUser.VK_RMENU] and winUser.getKeyState(winUser.VK_MENU)&32768:
			modifierList.append("alt")
		if not vkCode in [winUser.VK_LWIN,winUser.VK_RWIN] and winUser.getKeyState(winUser.VK_LWIN)&32768:
			modifierList.append("win")
		if not vkCode in [winUser.VK_LWIN,winUser.VK_RWIN] and winUser.getKeyState(winUser.VK_RWIN)&32768:
			modifierList.append("win")
		if len(modifierList) > 0:
			modifiers=frozenset(modifierList)
		else:
			modifiers=None
		mainKey=vkName
		if not mainKey:
			mainKey=winUser.getKeyNameText(scanCode,extended)
		if extended==1:
			mainKey="extended%s"%mainKey
		keyPress=(modifiers,mainKey)
		if log.isEnabledFor(log.IO): log.io("key press: %s"%keyName(keyPress))
		speakCommandKeys=config.conf["keyboard"]["speakCommandKeys"]
		if globalVars.keyboardHelp or speakCommandKeys:
			labelList = []
			if modifiers:
				for mod in modifiers: 
					if localizedKeyLabels.has_key(mod): 
						labelList.append(localizedKeyLabels[mod]) 
					else: 
						labelList.append(mod)
			if not isNVDAModifierKey(vkCode,extended):
				ch=ctypes.windll.user32.MapVirtualKeyW(vkCode,winUser.MAPVK_VK_TO_CHAR)
				if localizedKeyLabels.has_key(keyPress[1]):
					labelList.append(localizedKeyLabels[keyPress[1]])
				elif ch>=32 and not mainKey.startswith('numpad') and not mainKey in ('extendeddivide', 'multiply', 'subtract', 'add', 'extendedreturn', 'decimal'):
					labelList.append(unichr(ch))
				else:
					labelList.append(keyPress[1])
			if not speakCommandKeys or (speakCommandKeys and (
				# An alphanumeric key has a label of only 1 character.
				# Therefore, a command key either has a label longer than 1 character (except space)...
				(labelList[-1]!="space" and len(labelList[-1])>1)
				# or it has modifiers other than shift; e.g. control+f is a command key, but shift+f is not.
				or (modifiers and modifiers!=frozenset(("shift",)))
			)):
				queueHandler.queueFunction(queueHandler.eventQueue,speech.speakMessage,"+".join(labelList))
		if not globalVars.keyboardHelp and (mainKey in ('extendeddivide', 'multiply', 'subtract', 'add', 'extendedreturn')) and (bool(winUser.getKeyState(winUser.VK_NUMLOCK)&1)):
			return True
		script=scriptHandler.findScript(keyPress)
		if script:
			scriptName=scriptHandler.getScriptName(script)
			if globalVars.keyboardHelp and scriptName!="keyboardHelp":
				brailleTextList=[]
				brailleTextList.append("+".join(labelList))
				scriptDescription = scriptHandler.getScriptDescription(script)
				if scriptDescription:
					brailleTextList.append(scriptDescription)
					queueHandler.queueFunction(queueHandler.eventQueue,speech.speakMessage,_("Description: %s")%scriptDescription)
				scriptLocation=scriptHandler.getScriptLocation(script)
				brailleTextList.append(scriptLocation)
				queueHandler.queueFunction(queueHandler.eventQueue,speech.speakMessage,_("Location: %s")%scriptLocation)
				import braille
				braille.handler.message("\t\t".join(brailleTextList))
			else:
				scriptHandler.queueScript(script,keyPress)
		if script or globalVars.keyboardHelp:
			keyUpIgnoreSet.add((vkCode,extended))
			if NVDAModifierKey:
				usedNVDAModifierKey=True 
			return False
		else:
			speakToggleKey(vkCode)
			return True
	except:
		log.error("internal_keyDownEvent", exc_info=True)
		speech.speakMessage(_("Error in keyboardHandler.internal_keyDownEvent"))
		return True

def internal_keyUpEvent(vkCode,scanCode,extended,injected):
	"""Event that pyHook calls when it receives keyUps"""
	try:
		global NVDAModifierKey, usedNVDAModifierKey, lastNVDAModifierKey, lastNVDAModifierKeyTime, passKeyThroughCount, unpauseByShiftUp 
		if watchdog.isAttemptingRecovery:
			# The core is dead, so let keys pass through unhindered.
			return True
		focusObject=api.getFocusObject()
		focusAppModule=focusObject.appModule
		if focusAppModule and focusAppModule.selfVoicing:
			return True
		lastPressedKeyTime=time.time()
		if injected:
			return True
		elif passKeyThroughCount>=1:
			passKeyThroughCount-=1
			if passKeyThroughCount==0:
				passKeyThroughCount=-1
			return True
		if unpauseByShiftUp and vkCode in (winUser.VK_SHIFT,winUser.VK_LSHIFT,winUser.VK_RSHIFT):
			queueHandler.queueFunction(queueHandler.eventQueue,speech.pauseSpeech,False)
			unpauseByShiftUp=False
		if NVDAModifierKey and (vkCode,extended)==NVDAModifierKey:
			if not usedNVDAModifierKey:
				lastNVDAModifierKey=NVDAModifierKey
				lastNVDAModifierKeyTime=time.time()
			NVDAModifierKey=None
			usedNVDAModifierKey=False
			return False
		elif (vkCode,extended) in keyUpIgnoreSet:
			keyUpIgnoreSet.remove((vkCode,extended))
			return False
		elif vkCode in [winUser.VK_CONTROL,winUser.VK_LCONTROL,winUser.VK_RCONTROL,winUser.VK_SHIFT,winUser.VK_LSHIFT,winUser.VK_RSHIFT,winUser.VK_MENU,winUser.VK_LMENU,winUser.VK_RMENU,winUser.VK_LWIN,winUser.VK_RWIN]:
			return True
	except:
		log.error("", exc=True)
		speech.speakMessage(_("Error in keyboardHandler.internal_keyUpEvent"))
	return True

#Register internal key press event with  operating system

def initialize():
	"""Initialises keyboard support."""
	winInputHook.initialize()
	winInputHook.setCallbacks(keyDown=internal_keyDownEvent,keyUp=internal_keyUpEvent)

def terminate():
	winInputHook.terminate()
