#scriptHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import time
import weakref
from keyUtils import sendKey
import appModuleHandler
import api
import queueHandler

_numScriptsQueued=0 #Number of scripts that are queued to be executed
_lastScriptTime=0 #Time in MS of when the last script was executed
_lastScriptRef=None #Holds a weakref to the last script that was executed
_lastScriptCount=0 #The amount of times the last script was repeated
_isScriptRunning=False

def findScript(keyPress):
		return findScript_appModuleLevel(keyPress)

def findScript_appModuleLevel(keyPress):
	focusObject=api.getFocusObject()
	if not focusObject:
		return None
	appModule=focusObject.appModule
	func=appModule.getScript(keyPress) if appModule else None
	if func:
		return func
	return findScript_defaultAppModuleLevel(keyPress)

def findScript_defaultAppModuleLevel(keyPress):
	default=appModuleHandler.default
	func=default.getScript(keyPress)
	if func:
		return func
	return findScript_virtualBufferLevel(keyPress)

def findScript_virtualBufferLevel(keyPress):
	virtualBuffer=api.getFocusObject().virtualBuffer
	if virtualBuffer and not virtualBuffer.passThrough:
		func=virtualBuffer.getScript(keyPress)
		if func:
			return func
	return findScript_NVDAObjectLevel(keyPress)

def findScript_NVDAObjectLevel(keyPress):
	focusObject=api.getFocusObject()
	func=focusObject.getScript(keyPress)
	if func:
		return func
	else:
		return None

def getScriptName(script):
	return script.__name__[7:]

def getScriptLocation(script):
	return script.__module__

def getScriptDescription(script):
	return script.__doc__

def _queueScriptCallback(script,keyPress):
	global _numScriptsQueued
	_numScriptsQueued-=1
	executeScript(script,keyPress)

def queueScript(script,keyPress):
	global _numScriptsQueued
	_numScriptsQueued+=1
	queueHandler.queueFunction(queueHandler.eventQueue,_queueScriptCallback,script,keyPress)

def executeScript(script,keyPress):
	"""Executes a given script (function) passing it the given keyPress.
	It also keeps track of the execution of duplicate scripts with in a certain amount of time, and counts how many times this happens.
	Use L{getLastScriptRepeateCount} to find out this count value.
	@param script: the function or method that should be executed. The function or method must take an argument of 'keyPress'.
	@type script: callable.
	@param keyPress: the key press that activated this script
	@type keyPress: an NVDA keyPress
	"""
	global _lastScriptTime, _lastScriptCount, _lastScriptRef, _isScriptRunning 
	lastScriptRef=_lastScriptRef() if _lastScriptRef else None
	#We don't allow the same script to be executed from with in itself, but we still should pass the key through
	if _isScriptRunning and lastScriptRef==script:
		return sendKey(keyPress)
	_isScriptRunning=True
	try:
		scriptTime=time.time()
		scriptRef=weakref.ref(script)
		if (scriptTime-_lastScriptTime)<=0.5 and script==lastScriptRef:
			_lastScriptCount+=1
		else:
			_lastScriptCount=0
		_lastScriptRef=scriptRef
		_lastScriptTime=scriptTime
		script(keyPress)
	finally:
		_isScriptRunning=False

def getLastScriptRepeateCount():
	"""The count of how many times the most recent script has been executed.
	This should only be called from with in a script.
	@returns: a value greater or equal to 0. If the script has not been repeated it is 0, if it has been repeated once its 1, and so forth.
	@rtype: integer
	"""
	if (time.time()-_lastScriptTime)>0.5:
		return 0
	else:
		return _lastScriptCount

def isScriptWaiting():
	return bool(_numScriptsQueued)
