#keyboardHandler.py
#$Rev$
#$Date$
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
import api
import globalVars
import core
import config


keyUpIgnoreSet=set()
keyPressIgnoreSet=set()
insertDown=False
word=""

ignoreNextKeyPress = False

def key(name):
	"""Converts a string representation of a keyPress in to a set of modifiers and a key (which is NVDA's internal key representation).
@param name: keyPress name to convert
@type name: string
@returns: the internal key representation 
"""
	l = name.split("+")
	for num in range(len(l)):
		t=l[num]
		if len(t)>1:
			t="%s%s"%(t[0].upper(),t[1:])
		elif len(t)==1:
			t=t[0].upper()
		l[num]=t
	if len(l) >= 2:
		s=set()
		for m in l[0:-1]:
			s.add(m)
		modifiers = frozenset(s)
	else:
		modifiers = None
	return (modifiers, l[-1])

def keyName(keyPress):
	"""Converts an internal key press to a printable name
@param keyPress: a keyPress
@type keyPress: key
"""
	keyName=""
	for k in list(keyPress[0] if isinstance(keyPress[0],frozenset) else [])+[keyPress[1]]:
		keyName+="+%s"%k
	return keyName[1:]

def sendKey(keyPress):
	"""Sends a key press through to the operating system.
@param keyPress: the key to send
@type keyPress: NVDA internal key
"""
	debug.writeMessage("keyboardHandler.sendKey: %s"%keyName(keyPress))
	global keyPressIgnoreSet
	keyList=[]
	#Process modifier keys
	if keyPress[0] is not None:
		for modifier in keyPress[0]:
			if (modifier=="Alt") and (winUser.getKeyState(winUser.VK_MENU)&32768):
				continue
			elif (modifier=="Control") and (winUser.getKeyState(winUser.VK_CONTROL)&32768):
				continue
			elif (modifier=="Shift") and (winUser.getKeyState(winUser.VK_SHIFT)&32768):
				continue
			elif (modifier=="Win") and ((winUser.getKeyState(winUser.VK_LWIN)&32768) or (winUser.getKeyState(winUser.VK_RWIN)&32768)):
				continue
			elif (modifier=="Insert") and insertDown:
				continue
			if modifier[0:8]=="Extended":
				extended=1
				modifier=modifier[8:]
			else:
				extended=0
			if modifier=="Alt":
				modifier="Menu"
			if modifier=="Win":
				modifier="Lwin"
			modifier=modifier.upper()
			keyID=pyHook.HookConstants.VKeyToID("VK_%s"%modifier)
			keyList.append((keyID,extended))
	#Process normal key
	if keyPress[1] is not None:
		k=keyPress[1]
		if k[0:8]=="Extended":
			extended=1
			k=k[8:]
		else:
			extended=0
		k=k.upper()
		if len(k)==1:
			keyID=ord(k)
		else:
			keyID=pyHook.HookConstants.VKeyToID("VK_%s"%k)
		keyList.append((keyID,extended))
	if (keyList is None) or (len(keyList)==0):
		return
	#Send key up for any keys that are already down
	for k in filter(lambda x: winUser.getKeyState(x[0])&32768,keyList):
		winUser.keybd_event(k[0],0,k[1]+2,0)
	#Send key down events for these keys
	for k in keyList:
		winUser.keybd_event(k[0],0,k[1],0)
	#Send key up events for the keys in reverse order
	keyList.reverse()
	for k in keyList:
		winUser.keybd_event(k[0],0,k[1]+2,0)
	time.sleep(0.001)

#Internal functions for key presses

def internal_keyDownEvent(event):
	"""Event called by pyHook when it receives a keyDown. It sees if there is a script tied to this key and if so executes it. It also handles the speaking of characters, words and command keys.
"""
	global insertDown, ignoreNextKeyPress, word
	try:
		if event.Injected:
			return True
		globalVars.keyCounter+=1
		core.executeFunction(core.EXEC_SPEECH,audio.cancel)
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
			core.executeFunction(core.EXEC_SPEECH,audio.speakMessage,_("caps lock %s")%(_("on") if capState else _("off")))
		elif mainKey=="ExtendedNumlock":
			numState=bool(not winUser.getKeyState(winUser.VK_NUMLOCK)&1)
			core.executeFunction(core.EXEC_SPEECH,audio.speakMessage,_("num lock %s")%(_("on") if numState else _("off")))

		core.executeFunction(core.EXEC_KEYBOARD,speakKey,keyPress,event.Ascii)
		if api.keyHasScript(keyPress):
			core.executeFunction(core.EXEC_KEYBOARD,api.executeScript,keyPress)
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
		if api.isTypingProtected():
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

