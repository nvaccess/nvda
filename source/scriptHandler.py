# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2007-2023 NV Access Limited, Babbage B.V., Julien Cochuyt, Leonard de Ruijter, Cyrille Bougot
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from typing import (
	Callable,
	Generator,
	Iterator,
	List,
	Optional,
	Tuple,
)
import time
import weakref
import types
import config
import NVDAObjects
from speech import sayAll
import api
import queueHandler
from logHandler import log
import inputCore
import globalPluginHandler
import braille
import vision
import baseObject


_ScriptFunctionT = Callable[["inputCore.InputGesture"], None]
_ScriptFilterT = Callable[
	[
		Optional[_ScriptFunctionT],
		"NVDAObjects.NVDAObject",
		"inputCore.InputGesture"
	],
	Optional[_ScriptFunctionT]
]

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
	func = lambda gesture: inputCore.manager.emulateGesture(emuGesture)  # noqa: E731
	func.__name__ = "script_%s" % scriptName
	func.__doc__ = _("Emulates pressing %s on the system keyboard") % emuGesture.displayName
	return func


def _getObjScript(
		obj: "NVDAObjects.NVDAObject",
		gesture: "inputCore.InputGesture",
		globalMapScripts: List["inputCore.InputGestureScriptT"],
) -> Optional[_ScriptFunctionT]:
	"""
	@param globalMapScripts: An ordered list of scripts.
	The list is ordered by resolution priority,
	the first map in the list should be used to resolve the script first.
	"""
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

	try:
		# Search the object itself for in-built bindings.
		return obj.getScript(gesture)
	except Exception:  # Prevent a faulty add-on from breaking script handling altogether (#5446)
		log.exception()


def getGlobalMapScripts(gesture: "inputCore.InputGesture") -> List["inputCore.InputGestureScriptT"]:
	"""
	@returns: An ordered list of scripts.
	The list is ordered by resolution priority,
	the first map in the list should be used to resolve scripts first.
	"""
	globalMapScripts: List["inputCore.InputGestureScriptT"] = []
	globalMaps = [inputCore.manager.userGestureMap, inputCore.manager.localeGestureMap]
	globalMap = braille.handler.display.gestureMap if braille.handler and braille.handler.display else None
	if globalMap:
		globalMaps.append(globalMap)
	for globalMap in globalMaps:
		for identifier in gesture.normalizedIdentifiers:
			globalMapScripts.extend(globalMap.getScriptsForGesture(identifier))
	return globalMapScripts


def findScript(gesture: "inputCore.InputGesture") -> Optional[_ScriptFunctionT]:
	from utils.security import getSafeScripts
	from winAPI.sessionTracking import isLockScreenModeActive
	foundScript = _findScript(gesture)
	if (
		foundScript is not None
		and isLockScreenModeActive()
		and foundScript not in getSafeScripts()
	):
		return None
	return foundScript


def _findScript(gesture: "inputCore.InputGesture") -> Optional[_ScriptFunctionT]:
	focus = api.getFocusObject()
	if not focus:
		return None

	globalMapScripts = getGlobalMapScripts(gesture)

	for obj, filterFunc in _yieldObjectsForFindScript(gesture):
		if obj:
			func = _getObjScript(obj, gesture, globalMapScripts)
			if filterFunc is not None:
				func = filterFunc(func, obj, gesture)
			if func:
				return func

	return None


def _getTreeModeInterceptorScript(
		func: Optional[_ScriptFunctionT],
		obj: "NVDAObjects.NVDAObject",
		gesture: "inputCore.InputGesture",
) -> Optional[_ScriptFunctionT]:
	"""
	A filtering function used with _yieldObjectsForFindScript, to ensure a tree interceptor
	should propagate scripts and therefore handle the input gesture.
	"""
	from browseMode import BrowseModeTreeInterceptor
	if isinstance(obj, BrowseModeTreeInterceptor):
		func = obj.getAlternativeScript(gesture, func)
	if func and (not obj.passThrough or getattr(func, "ignoreTreeInterceptorPassThrough", False)):
		return func
	return None


def _getFocusAncestorScript(
		func: Optional[_ScriptFunctionT],
		obj: "NVDAObjects.NVDAObject",
		gesture: "inputCore.InputGesture",
) -> Optional[_ScriptFunctionT]:
	"""
	A filtering function used with _yieldObjectsForFindScript, to ensure a focus ancestor
	should propagate scripts and therefore handle the input gesture.
	"""
	if func and getattr(func, 'canPropagate', False):
		return func
	return None


def _yieldObjectsForFindScript(
		gesture: "inputCore.InputGesture"
) -> Generator[Tuple["NVDAObjects.NVDAObject", Optional[_ScriptFilterT]], None, None]:
	"""
	This generator is used to determine which NVDAObject to perform an input gesture on,
	in order of priority.
	For example, if the first yielded object has an associated script for the given gesture, findScript
	will use that script.
	@yields: A tuple, which includes
	 - an NVDAObject, to check if there is an associated script
	 - an optional function to handle any further filtering required after checking for an associated script
	"""
	# Import late to avoid circular import.
	# We need to import this here because this might be the first import of this module
	# and it might be needed by global maps.
	import globalCommands
	focus = api.getFocusObject()

	# Gesture specific scriptable object
	yield gesture.scriptableObject, None
	# Global plugins
	yield from ((p, None) for p in globalPluginHandler.runningPlugins)
	# App module
	yield focus.appModule, None

	# Braille display
	if (
		braille.handler
		and isinstance(braille.handler.display, baseObject.ScriptableObject)
	):
		yield braille.handler.display, None

	# Vision enhancement provider
	if vision.handler:
		for provider in vision.handler.getActiveProviderInstances():
			if isinstance(provider, baseObject.ScriptableObject):
				yield provider, None

	# Tree interceptor
	treeInterceptor = focus.treeInterceptor
	if treeInterceptor and treeInterceptor.isReady:
		yield treeInterceptor, _getTreeModeInterceptorScript

	# NVDAObject
	yield focus, None

	# Focus ancestors
	yield from ((a, _getFocusAncestorScript) for a in reversed(api.getFocusAncestors()))

	# Configuration profile activation scripts
	yield globalCommands.configProfileActivationCommands, None
	# Global commands
	yield globalCommands.commands, None


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
	gesture.executeScript(script)
	if _isInterceptedCommandScript(script):
		_numIncompleteInterceptedCommandScripts-=1

def queueScript(script,gesture):
	global _numScriptsQueued, _numIncompleteInterceptedCommandScripts
	_numScriptsQueued+=1
	if _isInterceptedCommandScript(script):
		_numIncompleteInterceptedCommandScripts+=1
	queueHandler.queueFunction(
		queueHandler.eventQueue,
		_queueScriptCallback,
		script,
		gesture,
		_immediate=getattr(gesture, "_immediate", True)
	)

def willSayAllResume(gesture):
	return (
		config.conf['keyboard']['allowSkimReadingInSayAll']
		and gesture.wasInSayAll
		and getattr(gesture.script, 'resumeSayAllMode', None) == sayAll.SayAllHandler.lastSayAllMode
	)

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
		resumeSayAllMode = sayAll.SayAllHandler.lastSayAllMode
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
	except:  # noqa: E722
		log.exception("error executing script: %s with gesture %r"%(script,gesture.displayName))
	finally:
		_isScriptRunning=False
		if resumeSayAllMode is not None:
			sayAll.SayAllHandler.readText(resumeSayAllMode)

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


def clearLastScript():
	"""Clears the variables that keeps track of the execution of duplicate scripts with in a certain amount of
	time, so that next script execution will always be detected as a first execution of this script.
	This function should only be called from the main thread.
	"""

	global _lastScriptTime, _lastScriptRef, _lastScriptCount
	_lastScriptTime = 0
	_lastScriptRef = None
	_lastScriptCount = 0


def getCurrentScript() -> Optional[_ScriptFunctionT]:
	if not _isScriptRunning:
		return None
	lastScriptRef = _lastScriptRef() if _lastScriptRef else None
	return lastScriptRef


def isScriptWaiting():
	return bool(_numScriptsQueued)

def script(
		description: str = "",
		category: Optional[str] = None,
		gesture: Optional[str] = None,
		gestures: Optional[Iterator[str]] = None,
		canPropagate: bool = False,
		bypassInputHelp: bool = False,
		allowInSleepMode: bool = False,
		resumeSayAllMode: Optional[int] = None,
		speakOnDemand: bool = False,
):
	"""Define metadata for a script.
	This function is to be used as a decorator to set metadata used by the scripting system and gesture editor.
	It can only decorate methods which have a name starting with "script_"
	:param description: A short translatable description of the script to be used in the gesture editor, etc.
	:param category: The category of the script displayed in the gesture editor.
	:param gesture: A gesture associated with this script.
	:param gestures: A collection of gestures associated with this script
	:param canPropagate: Whether this script should also apply when it belongs to a  focus ancestor object.
	:param bypassInputHelp: Whether this script should run when input help is active.
	:param allowInSleepMode: Whether this script should run when NVDA is in sleep mode.
	:param resumeSayAllMode: The say all mode that should be resumed when active before executing this script.
	One of the C{sayAll.CURSOR_*} constants.
	:param speakOnDemand: Whether this script should speak when NVDA speech mode is "on-demand"
	"""
	if gestures is None:
		gestures: List[str] = []
	else:
		# A tuple may have been used, however, the collection of gestures may need to be
		# extended (via append) with the value of the 'gesture' string (in-case both are provided in the
		# decorator).
		gestures: List[str] = list(gestures)

	def script_decorator(decoratedScript):
		# Decoratable scripts are functions, not bound instance methods.
		if not isinstance(decoratedScript, types.FunctionType):
			log.warning(
				"Using the script decorator is unsupported for %r" % decoratedScript,
				stack_info=True
			)
			return decoratedScript
		if not decoratedScript.__name__.startswith("script_"):
			log.warning(
				"Can't apply  script decorator to %r which name does not start with 'script_'" % decoratedScript.__name__,
				stack_info=True
			)
			return decoratedScript
		decoratedScript.__doc__ = description
		if category is not None:
			decoratedScript.category = category
		if gesture is not None:
			gestures.append(gesture)
		if gestures:
			decoratedScript.gestures = gestures
		decoratedScript.canPropagate = canPropagate
		decoratedScript.bypassInputHelp = bypassInputHelp
		if resumeSayAllMode is not None:
			decoratedScript.resumeSayAllMode = resumeSayAllMode
		decoratedScript.allowInSleepMode = allowInSleepMode
		decoratedScript.speakOnDemand = speakOnDemand
		return decoratedScript
	return script_decorator
