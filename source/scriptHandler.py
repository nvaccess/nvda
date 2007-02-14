#scriptHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import appModuleHandler
import virtualBuffers
import api

def findScript(keyPress):
		return findScript_appModuleLevel(keyPress)

def findScript_appModuleLevel(keyPress):
	appModule=appModuleHandler.getActiveModule()
	func=appModule.getScript(keyPress)
	if func:
		nextFunc=lambda k: findScript_defaultAppModuleLevel(k)
		script=lambda k: func(k,nextFunc)
		script.__name__=func.__name__
		script.__doc__=func.__doc__
		script.__module__=func.__module__
		return script
	return findScript_defaultAppModuleLevel(keyPress)

def findScript_defaultAppModuleLevel(keyPress):
	default=appModuleHandler.default
	func=default.getScript(keyPress)
	if func:
		nextFunc=lambda k: findScript_virtualBufferLevel(k)
		script=lambda k: func(k,nextFunc)
		script.__name__=func.__name__
		script.__doc__=func.__doc__
		script.__module__=func.__module__
		return script
	return findScript_virtualBufferLevel(keyPress)

def findScript_virtualBufferLevel(keyPress):
	focusObject=api.getFocusObject()
	virtualBuffer=virtualBuffers.getVirtualBuffer(focusObject)
	if virtualBuffer and not api.isVirtualBufferPassThrough():
		func=virtualBuffer.getScript(keyPress)
		if func:
			nextFunc=lambda k: findScript_NVDAObjectLevel(k)
			script=lambda k: func(k,nextFunc)
			script.__name__=func.__name__
			script.__doc__=func.__doc__
			script.__module__=func.__module__
			return script
	return findScript_NVDAObjectLevel(keyPress)

def findScript_NVDAObjectLevel(keyPress):
	focusObject=api.getFocusObject()
	func=focusObject.getScript(keyPress)
	if func:
		nextFunc=None
		script=lambda k: func(k,nextFunc)
		script.__name__=func.__name__
		script.__doc__=func.__doc__
		script.__module__=func.__module__
		return script
	else:
		return None

def getScriptName(script):
	return script.__name__[7:]

def getScriptLocation(script):
	return script.__module__

def getScriptDescription(script):
	return script.__doc__
