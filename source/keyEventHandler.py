#keyEventHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import win32api
import Queue
import pyHook
import debug
import audio

queue_keys=Queue.Queue(1000)
keyUpIgnoreSet=set()
keyPressIgnoreSet=set()
controlDown=False
shiftDown=False
altDown=False
insertDown=False
winDown=False
extendedWinDown=False

ignoreNextKeyPress = False

def key(name):
	l = name.split("+")
	if len(l) >= 2:
		s=set()
		for m in l[0:-1]:
			m="%s%s"%(m[0].upper(),m[1:])
			s.add(m)
		modifiers = frozenset(s)
	else:
		modifiers = None
	if len(l[-1])==1:
		l[-1]=l[-1].upper()
	return (modifiers, l[-1])

def sendKey(keyPress):
	global keyPressIgnoreSet
	keyList=[]
	#Process modifier keys
	if keyPress[0] is not None:
		for modifier in keyPress[0]:
			if (modifier=="Alt") and altDown:
				continue
			elif (modifier=="Control") and controlDown:
				continue
			elif (modifier=="Shift") and shiftDown:
				continue
			elif (modifier=="Win") and winDown:
				continue
			elif (modifier=="ExtendedWin") and extendedWinDown:
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
	#Send key down events for these keys
	debug.writeMessage("send key: %s"%keyList)
	for key in keyList:
		win32api.keybd_event(key[0],0,key[1],0)
	#Send key up events for the keys in reverse order
	keyList.reverse()
	for key in keyList:
		win32api.keybd_event(key[0],0,key[1]+2,0)

#Internal functions for key presses

def internal_keyDownEvent(event):
	global controlDown, shiftDown, altDown, insertDown, extendedInsertDown, winDown, extendedWinDown, ignoreNextKeyPress, ignoreKeyCounter
	try:
		if event.Injected:
			return True
		try:
			queue_keys.put_nowait((None, "SilenceSpeech"))
		except Queue.Empty:
			debug.writeError("internal_keyDownEvent: no room in queue")
		if (event.Key=="Insert") and (event.Extended==0):
			insertDown=True
			return True
		if (event.Key=="Lcontrol") or (event.Key=="Rcontrol"):
			controlDown=True
			return True
		if (event.Key=="Lshift") or (event.Key=="Rshift"):
			shiftDown=True
			return True
		if (event.Key=="Lmenu") or (event.Key=="Rmenu"):
			altDown=True
			return True
		if ((event.Key=="Lwin") or (event.Key=="Rwin")) and (event.Extended==0):
			winDown=True
			return True
		if ((event.Key=="Lwin") or (event.Key=="Rwin")) and (event.Extended==1):
			extendedWinDown=True
			return True
		modifierList=[]
		if insertDown is True:
			modifierList.append("Insert")
		if controlDown is True:
			modifierList.append("Control")
		if shiftDown is True:
			modifierList.append("Shift")
		if altDown is True:
			modifierList.append("Alt")
		if winDown is True:
			modifierList.append("Win")
		if extendedWinDown is True:
			modifierList.append("ExtendedWin")
		if len(modifierList) > 0:
			modifiers=frozenset(modifierList)
		else:
			modifiers=None
		keyName=event.Key
		if event.Extended==1:
			keyName="Extended%s"%keyName
		keyPress=(modifiers,keyName)
		debug.writeMessage("key press: %s %s"%keyPress)
		if keyPress in keyPressIgnoreSet:
			keyPressIgnoreSet.remove(keyPress)
			keyUpIgnoreSet.add((event.Key,event.Extended))
			return True
		if altDown and (event.KeyID==pyHook.HookConstants.vk_to_id['VK_TAB']):
			return True
		try:
			queue_keys.put_nowait(keyPress)
		except Queue.Empty:
			debug.writeError("internal_keyDownEvent: no room in queue")
			return True
		keyUpIgnoreSet.add((event.Key,event.Extended))
		return False
	except:
		audio.speakMessage("Error in keyEventHandler.internal_keyPressEvent")
		debug.writeException("keyEventHandler.internal_keyDownEvent")

def internal_keyUpEvent(event):
	global controlDown, shiftDown, altDown, insertDown, winDown, extendedWinDown, ignoreNextKeyPress, ignoreKeyCounter
	if event.Injected:
		return True
	if (event.Key=="Lcontrol") or (event.Key=="Rcontrol"):
		controlDown=False
		return True
	elif (event.Key=="Lshift") or (event.Key=="Rshift"):
		shiftDown=False
		return True
	elif (event.Key=="Lmenu") or (event.Key=="Rmenu"):
		altDown = False
		return True
	elif (event.Key=="Insert") and (event.Extended==0):
		insertDown = False
		return True
	elif ((event.Key=="Lwin") or (event.Key=="Rwin")) and (event.Extended==0):
		winDown = False
		return True
	elif ((event.Key=="Lwin") or (event.Key=="Rwin")) and (event.Extended==1):
		extendedWinDown = False
		return True
	if (event.Key,event.Extended) in keyUpIgnoreSet:
		keyUpIgnoreSet.remove((event.Key,event.Extended))
		return False
	return True

#Register internal key press event with  operating system

def initialize():
	hookManager=pyHook.HookManager()
	hookManager.KeyDown=internal_keyDownEvent
	hookManager.KeyUp=internal_keyUpEvent
	hookManager.HookKeyboard()

