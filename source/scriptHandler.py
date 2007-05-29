#scriptHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import appModuleHandler
import virtualBuffers
import api

def findScript(keyPress):
		return findScript_appModuleLevel(keyPress)

def findScript_appModuleLevel(keyPress):
	focusObject=api.getFocusObject()
	if not focusObject:
		return None
	appModule=focusObject.appModule()
	func=appModule.getScript(keyPress) if appModule else None
	if func:
		nextFunc=lambda keyPress=keyPress: findScript_defaultAppModuleLevel(keyPress)
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
		nextFunc=lambda keyPress=keyPress: findScript_virtualBufferLevel(keyPress)
		script=lambda k: func(k,nextFunc)
		script.__name__=func.__name__
		script.__doc__=func.__doc__
		script.__module__=func.__module__
		return script
	return findScript_virtualBufferLevel(keyPress)

def findScript_virtualBufferLevel(keyPress):
	virtualBuffer=api.getFocusObject().virtualBuffer()
	if virtualBuffer and not api.isVirtualBufferPassThrough():
		func=virtualBuffer.getScript(keyPress)
		if func:
			nextFunc=lambda keyPress=keyPress: findScript_NVDAObjectLevel(keyPress)
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
