#scriptHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import time
import weakref
import inspect
import config
import speech
import sayAllHandler
import appModuleHandler
import api
import queueHandler
from logHandler import log
import inputCore
import globalPluginHandler
import braille

_numScriptsQueued=0 #Number of scripts that are queued to be executed
#: Number of scripts that send their gestures on that are queued to be executed or are currently being executed.
_numIncompleteInterceptedCommandScripts=0
_lastScriptTime=0 #Time in MS of when the last script was executed
_lastScriptRef=None #Holds a weakref to the last script that was executed
_lastScriptCount=0 #The amount of times the last script was repeated
_isScriptRunning=False

def _makeKbEmulateScript(scriptName):
	import keyboardHandler
	keyName = scriptName[3:]
	emuGesture = keyboardHandler.KeyboardInputGesture.fromName(keyName)
	func = lambda gesture: inputCore.manager.emulateGesture(emuGesture)
	if isinstance(scriptName, unicode):
		# __name__ must be str; i.e. can't be unicode.
		scriptName = scriptName.encode("mbcs")
	func.__name__ = "script_%s" % scriptName
	func.__doc__ = _("Emulates pressing %s on the system keyboard") % keyName
	return func

def _getObjScript(obj, gesture, globalMapScripts):
	# Search the scripts from the global gesture maps.
	for cls, scriptName in globalMapScripts:
		if isinstance(obj, cls):
			if scriptName is None:
				# The global map specified that no script should execute for this gesture and object.
				return None
			if scriptName.startswith("kb:"):
				# Emulate a key press.
				return _makeKbEmulateScript(scriptName)
			try:
				return getattr(obj, "script_%s" % scriptName)
			except AttributeError:
				pass

	# Search the object itself for in-built bindings.
	return obj.getScript(gesture)

def findScript(gesture):
	focus = api.getFocusObject()
	if not focus:
		return None

	# Import late to avoid circular import.
	# We need to import this here because this might be the first import of this module
	# and it might be needed by global maps.
	import globalCommands

	globalMapScripts = []
	globalMaps = [inputCore.manager.userGestureMap, inputCore.manager.localeGestureMap]
	globalMap = braille.handler.display.gestureMap
	if globalMap:
		globalMaps.append(globalMap)
	for globalMap in globalMaps:
		for identifier in gesture.identifiers:
			globalMapScripts.extend(globalMap.getScriptsForGesture(identifier))

	# Gesture specific scriptable object.
	obj = gesture.scriptableObject
	if obj:
		func = _getObjScript(obj, gesture, globalMapScripts)
		if func:
			return func

	# Global plugin level.
	for plugin in globalPluginHandler.runningPlugins:
		func = _getObjScript(plugin, gesture, globalMapScripts)
		if func:
			return func

	# App module level.
	app = focus.appModule
	if app:
		func = _getObjScript(app, gesture, globalMapScripts)
		if func:
			return func

	# Tree interceptor level.
	treeInterceptor = focus.treeInterceptor
	if treeInterceptor and treeInterceptor.isReady:
		func = _getObjScript(treeInterceptor, gesture, globalMapScripts)
		from browseMode import BrowseModeTreeInterceptor
		if isinstance(treeInterceptor,BrowseModeTreeInterceptor):
			func=treeInterceptor.getAlternativeScript(gesture,func)
		if func and (not treeInterceptor.passThrough or getattr(func,"ignoreTreeInterceptorPassThrough",False)):
			return func

	# NVDAObject level.
	func = _getObjScript(focus, gesture, globalMapScripts)
	if func:
		return func
	for obj in reversed(api.getFocusAncestors()):
		func = _getObjScript(obj, gesture, globalMapScripts)
		if func and getattr(func, 'canPropagate', False): 
			return func

	# Global commands.
	func = _getObjScript(globalCommands.commands, gesture, globalMapScripts)
	if func:
		return func

	return None

def getScriptName(script):
	return script.__name__[7:]

def getScriptLocation(script):
	try:
		instance = script.__self__
	except AttributeError:
		# Not an instance method, so this must be a fake script.
		return None
	name=script.__name__
	for cls in instance.__class__.__mro__:
		if name in cls.__dict__:
			return "%s.%s"%(cls.__module__,cls.__name__)

def _isInterceptedCommandScript(script):
	return not getattr(script,'__doc__',None)

def _queueScriptCallback(script,gesture):
	global _numScriptsQueued, _numIncompleteInterceptedCommandScripts
	_numScriptsQueued-=1
	executeScript(script,gesture)
	if _isInterceptedCommandScript(script):
		_numIncompleteInterceptedCommandScripts-=1

def queueScript(script,gesture):
	global _numScriptsQueued, _numIncompleteInterceptedCommandScripts
	_numScriptsQueued+=1
	if _isInterceptedCommandScript(script):
		_numIncompleteInterceptedCommandScripts+=1
	queueHandler.queueFunction(queueHandler.eventQueue,_queueScriptCallback,script,gesture)

def willSayAllResume(gesture):
	return config.conf['keyboard']['allowSkimReadingInSayAll']and gesture.wasInSayAll and getattr(gesture.script,'resumeSayAllMode',None)==sayAllHandler.lastSayAllMode

def executeScript(script,gesture):
	"""Executes a given script (function) passing it the given gesture.
	It also keeps track of the execution of duplicate scripts with in a certain amount of time, and counts how many times this happens.
	Use L{getLastScriptRepeatCount} to find out this count value.
	@param script: the function or method that should be executed. The function or method must take an argument of 'gesture'. This must be the same value as gesture.script, but its passed in here purely for performance. 
	@type script: callable.
	@param gesture: the input gesture that activated this script
	@type gesture: L{inputCore.InputGesture}
	"""
	global _lastScriptTime, _lastScriptCount, _lastScriptRef, _isScriptRunning 
	lastScriptRef=_lastScriptRef() if _lastScriptRef else None
	#We don't allow the same script to be executed from with in itself, but we still should pass the key through
	scriptFunc=getattr(script,"__func__",script)
	if _isScriptRunning and lastScriptRef==scriptFunc:
		return gesture.send()
	_isScriptRunning=True
	resumeSayAllMode=None
	if willSayAllResume(gesture):
		resumeSayAllMode=sayAllHandler.lastSayAllMode
	try:
		scriptTime=time.time()
		scriptRef=weakref.ref(scriptFunc)
		if (scriptTime-_lastScriptTime)<=0.5 and scriptFunc==lastScriptRef:
			_lastScriptCount+=1
		else:
			_lastScriptCount=0
		_lastScriptRef=scriptRef
		_lastScriptTime=scriptTime
		script(gesture)
	except:
		log.exception("error executing script: %s with gesture %r"%(script,gesture.displayName))
	finally:
		_isScriptRunning=False
		if resumeSayAllMode is not None:
			sayAllHandler.readText(resumeSayAllMode)

def getLastScriptRepeatCount():
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

def isCurrentScript(scriptFunc):
	"""Finds out if the given script is equal to the script that L{isCurrentScript} is being called from.
	@param scriptFunc: the script retreaved from ScriptableObject.getScript(gesture)
	@type scriptFunc: Instance method
	@returns: True if they are equal, False otherwise
	@rtype: boolean
	"""
	try:
	 	givenFunc=getattr(scriptFunc.im_self.__class__,scriptFunc.__name__)
	except AttributeError:
		log.debugWarning("Could not get unbound method from given script",exc_info=True) 
		return False
	parentFrame=inspect.currentframe().f_back
	try:
		realObj=parentFrame.f_locals['self']
	except KeyError:
		log.debugWarning("Could not get self instance from parent frame instance method",exc_info=True)
		return False
	try:
		realFunc=getattr(realObj.__class__,parentFrame.f_code.co_name)
	except AttributeError:
		log.debugWarning("Could not get unbound method from parent frame instance",exc_info=True)
		return False
	return givenFunc==realFunc

