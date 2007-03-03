#keyboardHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Keyboard support"""

import winUser
import time
import pyHook
import debug
import audio
from keyUtils import key, keyName
import api
import scriptHandler
import globalVars
import queueHandler
import config


keyUpIgnoreSet=set()
keyPressIgnoreSet=set()
insertDown=False
word=""

ignoreNextKeyPress = False

def isTypingProtected():
	"""Checks to see if key echo should be suppressed because the focus is currently on an object that has its protected state set.
@returns: True if it should be suppressed, False otherwise.
@rtype: boolean
"""
	focusObject=api.getFocusObject()
	if focusObject and focusObject.isProtected:
		return True
	else:
		return False


#Internal functions for key presses

def internal_keyDownEvent(event):
	"""Event called by pyHook when it receives a keyDown. It sees if there is a script tied to this key and if so executes it. It also handles the speaking of characters, words and command keys.
"""
	global insertDown, ignoreNextKeyPress, word
	try:
		if event.Injected:
			return True
		globalVars.keyCounter+=1
		if not audio.beenCanceled:
			queueHandler.queueFunction(queueHandler.ID_SPEECH,audio.cancel)
		if event.KeyID in [winUser.VK_CONTROL,winUser.VK_LCONTROL,winUser.VK_RCONTROL,winUser.VK_SHIFT,winUser.VK_LSHIFT,winUser.VK_RSHIFT,winUser.VK_MENU,winUser.VK_LMENU,winUser.VK_RMENU,winUser.VK_LWIN,winUser.VK_RWIN]:
			return True
		if (event.Key=="Insert"): #and (event.Extended==0):
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
		mainKey=event.Key
		if event.Extended==1:
			mainKey="Extended%s"%mainKey
		keyPress=(modifiers,mainKey)
		if keyPress in keyPressIgnoreSet:
			keyPressIgnoreSet.remove(keyPress)
			keyUpIgnoreSet.add((event.Key,event.Extended))
			return True
		debug.writeMessage("key press: %s"%keyName(keyPress))
		if mainKey=="Capital":
			capState=bool(not winUser.getKeyState(winUser.VK_CAPITAL)&1)
			queueHandler.queueFunction(queueHandler.ID_SPEECH,audio.speakMessage,_("caps lock %s")%(_("on") if capState else _("off")))
		elif mainKey=="ExtendedNumlock":
			numState=bool(not winUser.getKeyState(winUser.VK_NUMLOCK)&1)
			queueHandler.queueFunction(queueHandler.ID_SPEECH,audio.speakMessage,_("num lock %s")%(_("on") if numState else _("off")))
		queueHandler.queueFunction(queueHandler.ID_SCRIPT,speakKey,keyPress,event.Ascii)
		script=scriptHandler.findScript(keyPress)
		if script:
			scriptName=scriptHandler.getScriptName(script)
			scriptLocation=scriptHandler.getScriptLocation(script)
			scriptDescription=scriptHandler.getScriptDescription(script)
			if globalVars.keyboardHelp and scriptName!="keyboardHelp":
				queueHandler.queueFunction(queueHandler.ID_SPEECH,audio.speakMessage,"%s"%scriptName.replace('_',' '))
				queueHandler.queueFunction(queueHandler.ID_SPEECH,audio.speakMessage,_("Description: %s")%scriptDescription)
				queueHandler.queueFunction(queueHandler.ID_SPEECH,audio.speakMessage,_("Location: %s")%scriptLocation)
			else:
				queueHandler.queueFunction(queueHandler.ID_SCRIPT,script,keyPress)
		if script or globalVars.keyboardHelp:
			keyUpIgnoreSet.add((event.Key,event.Extended))
			return False
		else:
			return True
	except:
		debug.writeException("keyboardHandler.internal_keyDownEvent")
		audio.speakMessage("Error in keyboardHandler.internal_keyDownEvent",wait=True)
		return True

def speakKey(keyPress,ascii):
	global word
	if ((keyPress[0] is None) or (keyPress[0]==frozenset(['Shift']))) and (ascii in range(33,128)):
		if isTypingProtected():
			char="*"
		else:
			char=chr(ascii)
		if config.conf["keyboard"]["speakTypedCharacters"]:
			audio.speakSymbol(char)
		if config.conf["keyboard"]["speakTypedWords"] and (((keyPress[1]>=ord('a')) and (ascii<=ord('z'))) or ((ascii>=ord('A')) and (ascii<=ord('Z')))):
			word+=char
		elif config.conf["keyboard"]["speakTypedWords"] and (len(word)>=1):
			audio.speakText(word)
			word=""
	else:
		if config.conf["keyboard"]["speakCommandKeys"]:
			keyList=[]
			if (keyPress[0] is not None) and (len(keyPress[0])>0):
				keyList+=keyPress[0]
			if ascii in range(33,128):
				keyList.append(chr(ascii))
			else:
				keyList.append(keyPress[1])
			label="+".join(keyList)
			audio.speakMessage(keyList)
		if config.conf["keyboard"]["speakTypedWords"] and (len(word)>=1):
			audio.speakMessage(word)
			word=""

def internal_keyUpEvent(event):
	"""Event that pyHook calls when it receives keyUps"""
	global insertDown, ignoreNextKeyPress
	try:
		if event.Injected:
			return True
		if event.KeyID in [winUser.VK_CONTROL,winUser.VK_LCONTROL,winUser.VK_RCONTROL,winUser.VK_SHIFT,winUser.VK_LSHIFT,winUser.VK_RSHIFT,winUser.VK_MENU,winUser.VK_LMENU,winUser.VK_RMENU,winUser.VK_LWIN,winUser.VK_RWIN]:
			return True
		elif (event.Key=="Insert"): #and (event.Extended==0):
			insertDown=False
			return False
		elif (event.Key,event.Extended) in keyUpIgnoreSet:
			keyUpIgnoreSet.remove((event.Key,event.Extended))
			return False
		else:
			return True
	except:
		debug.writeException("keyboardHandler.internal_keyUpEvent")
		audio.speakMessage("Error in keyboardHandler.internal_keyUpEvent",wait=True)
		return True

#Register internal key press event with  operating system

def initialize():
	"""Initialises keyboard support."""
	hookManager=pyHook.HookManager()
	hookManager.KeyDown=internal_keyDownEvent
	hookManager.KeyUp=internal_keyUpEvent
	hookManager.HookKeyboard()

