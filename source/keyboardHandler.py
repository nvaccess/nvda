#keyboardHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import winUser
import time
import pyHook
import debug
import winUser
import audio
import api
import globalVars
from constants import *
import NVDAThreads

keyUpIgnoreSet=set()
keyPressIgnoreSet=set()
insertDown=False

ignoreNextKeyPress = False

def key(name):
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

def sendKey(keyPress):
	global keyPressIgnoreSet
	keyList=[]
	#Process modifier keys
	if keyPress[0] is not None:
		for modifier in keyPress[0]:
			if (modifier=="Alt") and (winUser.getKeyState(VK_MENU)&32768):
				continue
			elif (modifier=="Control") and (winUser.getKeyState(VK_CONTROL)&32768):
				continue
			elif (modifier=="Shift") and (winUser.getKeyState(VK_SHIFT)&32768):
				continue
			elif (modifier=="Win") and ((winUser.getKeyState(VK_LWIN)&32768) or (winUser.getKeyState(VK_RWIN)&32768)):
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
		key=keyPress[1]
		if key[0:8]=="Extended":
			extended=1
			key=key[8:]
		else:
			extended=0
		key=key.upper()
		if len(key)==1:
			keyID=ord(key)
		else:
			keyID=pyHook.HookConstants.VKeyToID("VK_%s"%key)
		keyList.append((keyID,extended))
	if (keyList is None) or (len(keyList)==0):
		return
	#Send key up for any keys that are already down
	for key in filter(lambda x: winUser.getKeyState(x[0])&32768,keyList):
		winUser.keybd_event(key[0],0,key[1]+2,0)
	#Send key down events for these keys
	for key in keyList:
		winUser.keybd_event(key[0],0,key[1],0)
	#Send key up events for the keys in reverse order
	keyList.reverse()
	for key in keyList:
		winUser.keybd_event(key[0],0,key[1]+2,0)
	time.sleep(0.1)

#Internal functions for key presses

def internal_keyDownEvent(event):
	global insertDown, ignoreNextKeyPress
	try:
		if event.Injected:
			return True
		globalVars.keyCounter+=1
		NVDAThreads.executeFunction(audio.cancel)
		if event.KeyID in [VK_CONTROL,VK_LCONTROL,VK_RCONTROL,VK_SHIFT,VK_LSHIFT,VK_RSHIFT,VK_MENU,VK_LMENU,VK_RMENU,VK_LWIN,VK_RWIN]:
			return True
		if (event.Key=="Insert") and (event.Extended==0):
			insertDown=True
			return False
		modifierList=[]
		if insertDown:
			modifierList.append("Insert")
		if winUser.getKeyState(VK_CONTROL)&32768:
			modifierList.append("Control")
		if winUser.getKeyState(VK_SHIFT)&32768:
			modifierList.append("Shift")
		if winUser.getKeyState(VK_MENU)&32768:
			modifierList.append("Alt")
		if winUser.getKeyState(VK_LWIN)&32768:
			modifierList.append("Win")
		if winUser.getKeyState(VK_RWIN)&32768:
			modifierList.append("Win")
		if len(modifierList) > 0:
			modifiers=frozenset(modifierList)
		else:
			modifiers=None
		keyName=event.Key
		if event.Extended==1:
			keyName="Extended%s"%keyName
		keyPress=(modifiers,keyName)
		if keyPress in keyPressIgnoreSet:
			keyPressIgnoreSet.remove(keyPress)
			keyUpIgnoreSet.add((event.Key,event.Extended))
			return True
		debug.writeMessage("key press: %s"%str(keyPress))
		if api.keyHasScript(keyPress):
			NVDAThreads.executeFunction(api.executeScript,keyPress)
			keyUpIgnoreSet.add((event.Key,event.Extended))
			return False
		else:
			return True
	except:
		debug.writeException("keyboardHandler.internal_keyDownEvent")
		audio.speakMessage("Error in keyboardHandler.internal_keyDownEvent",wait=True)
		return True

def internal_keyUpEvent(event):
	global insertDown, ignoreNextKeyPress
	try:
		if event.Injected:
			return True
		if event.KeyID in [VK_CONTROL,VK_LCONTROL,VK_RCONTROL,VK_SHIFT,VK_LSHIFT,VK_RSHIFT,VK_MENU,VK_LMENU,VK_RMENU,VK_LWIN,VK_RWIN]:
			return True
		elif (event.Key=="Insert") and (event.Extended==0):
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
	hookManager=pyHook.HookManager()
	hookManager.KeyDown=internal_keyDownEvent
	hookManager.KeyUp=internal_keyUpEvent
	hookManager.HookKeyboard()

