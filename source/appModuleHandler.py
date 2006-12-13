"""Manages appModules.
@ivar current: holds the currently loaded appModule
@type current: appModule
"""
#appModules/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import re
import ctypes
import os
import sys
import debug
import audio
import winUser
import winKernel
from constants import *
from config import conf
from keyboardHandler import key

#This is here so that the appModules are able to import modules from the appModules dir themselves
__path__=['.\\appModules']

#Dictionary of windowHandle:appModule paires used to hold the currently running modules
runningTable={}
#variable to hold the default appModule instance
default=None

#regexp to collect the key and script from a line in a keyMap file 
re_keyScript=re.compile(r'^\s*(?P<key>[\w+]+)\s*=\s*(?P<script>[\w]+)\s*$')

def getAppName(window):
	"""Finds out the application name of the given window.
"""
	try:
		processID=winUser.getWindowThreadProcessID(winUser.getAncestor(window,GA_ROOTOWNER))
		procHandle=winKernel.openProcess(PROCESS_ALL_ACCESS,False,processID[0])
		buf=ctypes.create_unicode_buffer(1024)
		res=ctypes.windll.psapi.GetProcessImageFileNameW(procHandle,buf,1024)
		winKernel.closeHandle(procHandle)
		return os.path.splitext(buf.value.split('\\')[-1])[0].lower()
	except:
		return None

def moduleExists(name):
	return os.path.isfile('appModules/%s.py'%name)

def getKeyMapFileName(appName,layout):
	if os.path.isfile('appModules/%s_%s.kbd'%(appName,layout)):
		return 'appModules/%s_%s.kbd'%(appName,layout)
	elif layout!='desktop':
		return getKeyMapFileName(appName,'desktop')
	else:
		return None

def getActiveModule():
	appWindow=winUser.getAncestor(winUser.getForegroundWindow(),GA_ROOTOWNER)
	if runningTable.has_key(appWindow):
		return runningTable[appWindow]
	else:
		return default

def update():
	for w in filter(lambda x: not winUser.isWindow(x),runningTable):
		debug.writeMessage("appModuleHandler.update: removing module %s at %s"%(runningTable[w].__module__,w))
		del runningTable[w]
	appWindow=winUser.getAncestor(winUser.getForegroundWindow(),GA_ROOTOWNER)
	if not appWindow:
		return
	if not runningTable.has_key(appWindow):
		appName=getAppName(appWindow)
		if not appName:
			debug.writeError("appModuleHandler.loadModule: could not get application name from window %s (%s)"%(appWindow,winUser.getClassName(appWindow)))
		mod=fetchModule(appName,appWindow)
		if mod:
			mod._keyMap=default._keyMap.copy()
			loadKeyMap(appName,mod)
			runningTable[appWindow]=mod
			debug.writeMessage("appModuleHandler.update: loaded module %s"%appName)

def loadKeyMap(appName,mod):
	layout=conf["keyboard"]["keyboardLayout"]
	keyMapFileName=getKeyMapFileName(appName,layout)
	if not keyMapFileName:
		return False
	keyMapFile=open(keyMapFileName,'r')
	bindCount=0
	for line in filter(lambda x: not x.startswith('#') and not x.isspace(),keyMapFile.readlines()):
		m=re_keyScript.match(line)
		if m:
			try:
				mod._keyMap[key(m.group('key'))]=getattr(mod,"script_"+m.group('script'))
				bindCount+=1
			except:
				debug.writeException("appModuleHandler.loadKeyMap: error binding %s to %s in module %s"%(m.group('script'),m.group('key'),appName))
	debug.writeMessage("appModuleHandler.loadKeyMap: added %s bindings to module %s from file %s"%(bindCount,appName,keyMapFileName))
  	return True

def fetchModule(appName,appWindow):
	if not moduleExists(appName):
		return False
	try:
		mod=__import__(appName,globals(),locals(),[]).appModule(appWindow,winUser.getWindowThreadProcessID(appWindow))
	except:
		debug.writeException("appModuleHandler.loadModule: Error in appModule %s"%appName)
		audio.speakMessage("Error in appModule %s"%appName,wait=True)
		return None
	return mod

def initialize():
	global default
	default=fetchModule('_default',winUser.getDesktopWindow())
	if default:
		if loadKeyMap('_default',default):
			debug.writeMessage("appModuleHandler.initialize: loaded default module")
		else:
			audio.speakMessage("Could not load default module keyMap",wait=True)
			raise RuntimeError("appModuleHandler.initialize: could not load default module keymap")
	else:
		audio.speakMessage("Could not load default module ",wait=True)
		raise RuntimeError("appModuleHandler.initialize: could not load default module ")
