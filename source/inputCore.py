#inputCore.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010 James Teh <jamie@jantrid.net>

"""Core framework for handling input from the user.
Every piece of input from the user (e.g. a key press) is represented by an L{InputGesture}.
The singleton L{InputManager} (L{manager}) manages functionality related to input from the user.
For example, it is used to execute gestures and handle input help.
"""

import sys
import os
import itertools
import weakref
import configobj
import sayAllHandler
import baseObject
import scriptHandler
import queueHandler
import api
import speech
import characterProcessing
import config
import watchdog
from logHandler import log
import globalVars
import languageHandler
import controlTypes

#: Script category for emulated keyboard keys.
# Translators: The name of a category of NVDA commands.
SCRCAT_KBEMU = _("Emulated system keyboard keys")
#: Script category for miscellaneous commands.
# Translators: The name of a category of NVDA commands.
SCRCAT_MISC = _("Miscellaneous")
#: Script category for Browse Mode  commands.
# Translators: The name of a category of NVDA commands.
SCRCAT_BROWSEMODE = _("Browse mode")

class NoInputGestureAction(LookupError):
	"""Informs that there is no action to execute for a gesture.
	"""

class InputGesture(baseObject.AutoPropertyObject):
	"""A single gesture of input from the user.
	For example, this could be a key press on a keyboard or Braille display or a click of the mouse.
	At the very least, subclasses must implement L{_get_identifiers} and L{_get_displayName}.
	"""
	cachePropertiesByDefault = True

	#: indicates that sayAll was running before this gesture
	#: @type: bool
	wasInSayAll=False

	#: Indicates that while in Input Help Mode, this gesture should be handled as if Input Help mode was currently off.
	#: @type: bool
	bypassInputHelp=False

	def _get_identifiers(self):
		"""The identifier(s) which will be used in input gesture maps to represent this gesture.
		These identifiers will be looked up in order until a match is found.
		A single identifier should take the form: C{source:id}
		where C{source} is a few characters representing the source of this gesture
		and C{id} is the specific gesture.
		If C{id} consists of multiple items with indeterminate order,
		they should be separated by a + sign and they should be in Python set order.
		Also, the entire identifier should be in lower case.
		An example identifier is: C{kb(desktop):nvda+1}
		Subclasses must implement this method.
		@return: One or more identifiers which uniquely identify this gesture.
		@rtype: list or tuple of str
		"""
		raise NotImplementedError

	def _get_logIdentifier(self):
		"""A single identifier which will be logged for this gesture.
		This identifier should be usable in input gesture maps, but should be as readable as possible to the user.
		For example, it might sort key names in a particular order
		and it might contain mixed case.
		This is in contrast to L{identifiers}, which must be normalized.
		The base implementation returns the first identifier from L{identifiers}.
		"""
		return self.identifiers[0]

	def _get_displayName(self):
		"""The name of this gesture as presented to the user.
		Subclasses must implement this method.
		@return: The display name.
		@rtype: str
		"""
		return self.getDisplayTextForIdentifier(self.identifiers[0])[1]

	#: Whether this gesture should be reported when reporting of command gestures is enabled.
	#: @type: bool
	shouldReportAsCommand = True

	#: whether this gesture represents a character being typed (i.e. not a potential command)
	#: @type bool
	isCharacter=False

	SPEECHEFFECT_CANCEL = "cancel"
	SPEECHEFFECT_PAUSE = "pause"
	SPEECHEFFECT_RESUME = "resume"
	#: The effect on speech when this gesture is executed; one of the SPEECHEFFECT_* constants or C{None}.
	speechEffectWhenExecuted = SPEECHEFFECT_CANCEL

	#: Whether this gesture is only a modifier, in which case it will not search for a script to execute.
	#: @type: bool
	isModifier = False

	def reportExtra(self):
		"""Report any extra information about this gesture to the user.
		This is called just after command gestures are reported.
		For example, it could be used to report toggle states.
		"""

	def _get_script(self):
		"""The script bound to this input gesture.
		@return: The script to be executed.
		@rtype: script function
		"""
		self.script=scriptHandler.findScript(self)
		return self.script

	def send(self):
		"""Send this gesture to the operating system.
		This is not possible for all sources.
		@raise NotImplementedError: If the source does not support sending of gestures.
		"""
		raise NotImplementedError

	def _get_scriptableObject(self):
		"""An object which contains scripts specific to this  gesture or type of gesture.
		This object will be searched for scripts before any other object when handling this gesture.
		@return: The gesture specific scriptable object or C{None} if there is none.
		@rtype: L{baseObject.ScriptableObject}
		"""
		return None

	@classmethod
	def getDisplayTextForIdentifier(cls, identifier):
		"""Get the text to be presented to the user describing a given gesture identifier.
		This should only be called for gesture identifiers associated with this class.
		Most callers will want L{inputCore.getDisplayTextForIdentifier} instead.
		The display text consists of two strings:
		the gesture's source (e.g. "laptop keyboard")
		and the specific gesture (e.g. "alt+tab").
		@param identifier: The normalized gesture identifier in question.
		@type identifier: basestring
		@return: A tuple of (source, specificGesture).
		@rtype: tuple of (basestring, basestring)
		@raise Exception: If no display text can be determined.
		"""
		raise NotImplementedError

class GlobalGestureMap(object):
	"""Maps gestures to scripts anywhere in NVDA.
	This is used to allow users and locales to bind gestures in addition to those bound by individual scriptable objects.
	Map entries will most often be loaded from a file using the L{load} method.
	See that method for details of the file format.
	"""

	def __init__(self, entries=None):
		"""Constructor.
		@param entries: Initial entries to add; see L{update} for the format.
		@type entries: mapping of str to mapping
		"""
		self._map = {}
		#: Indicates that the last load or update contained an error.
		#: @type: bool
		self.lastUpdateContainedError = False
		#: The file name for this gesture map, if any.
		#: @type: basestring
		self.fileName = None
		if entries:
			self.update(entries)

	def clear(self):
		"""Clear this map.
		"""
		self._map.clear()
		self.lastUpdateContainedError = False

	def add(self, gesture, module, className, script,replace=False):
		"""Add a gesture mapping.
		@param gesture: The gesture identifier.
		@type gesture: str
		@param module: The name of the Python module containing the target script.
		@type module: str
		@param className: The name of the class in L{module} containing the target script.
		@type className: str
		@param script: The name of the target script
			or C{None} to unbind the gesture for this class.
		@type script: str
		@param replace: if true replaces all existing bindings for this gesture with the given script, otherwise only appends this binding.
		@type replace: boolean
		"""
		gesture = normalizeGestureIdentifier(gesture)
		try:
			scripts = self._map[gesture]
		except KeyError:
			scripts = self._map[gesture] = []
		if replace:
			del scripts[:]
		scripts.append((module, className, script))

	def load(self, filename):
		"""Load map entries from a file.
		The file is an ini file.
		Each section contains entries for a particular scriptable object class.
		The section name must be the full Python module and class name.
		The key of each entry is the script name and the value is a comma separated list of one or more gestures.
		If the script name is "None", the gesture will be unbound for this class.
		For example, the following binds the "a" key to move to the next heading in virtual buffers
		and removes the default "h" binding::
			[virtualBuffers.VirtualBuffer]
			nextHeading = kb:a
			None = kb:h
		@param filename: The name of the file to load.
		@type: str
		"""
		self.fileName = filename
		try:
			conf = configobj.ConfigObj(filename, file_error=True, encoding="UTF-8")
		except (configobj.ConfigObjError,UnicodeDecodeError), e:
			log.warning("Error in gesture map '%s': %s"%(filename, e))
			self.lastUpdateContainedError = True
			return
		self.update(conf)

	def update(self, entries):
		"""Add multiple map entries.
		C{entries} must be a mapping of mappings.
		Each inner mapping contains entries for a particular scriptable object class.
		The key in the outer mapping must be the full Python module and class name.
		The key of each entry in the inner mappings is the script name and the value is a list of one or more gestures.
		If the script name is C{None}, the gesture will be unbound for this class.
		For example, the following binds the "a" key to move to the next heading in virtual buffers
		and removes the default "h" binding::
			{
				"virtualBuffers.VirtualBuffer": {
					"nextHeading": "kb:a",
					None: "kb:h",
				}
			}
		@param entries: The items to add.
		@type entries: mapping of str to mapping
		"""
		self.lastUpdateContainedError = False
		for locationName, location in entries.iteritems():
			try:
				module, className = locationName.rsplit(".", 1)
			except:
				log.error("Invalid module/class specification: %s" % locationName)
				self.lastUpdateContainedError = True
				continue
			for script, gestures in location.iteritems():
				if script == "None":
					script = None
				if gestures == "":
					gestures = ()
				elif isinstance(gestures, basestring):
					gestures = [gestures]
				for gesture in gestures:
					try:
						self.add(gesture, module, className, script)
					except:
						log.error("Invalid gesture: %s" % gesture)
						self.lastUpdateContainedError = True
						continue

	def getScriptsForGesture(self, gesture):
		"""Get the scripts associated with a particular gesture.
		@param gesture: The gesture identifier.
		@type gesture: str
		@return: The Python class and script name for each script;
			the script name may be C{None} indicating that the gesture should be unbound for this class.
		@rtype: generator of (class, str)
		"""
		try:
			scripts = self._map[gesture]
		except KeyError:
			return
		for moduleName, className, scriptName in scripts:
			try:
				module = sys.modules[moduleName]
			except KeyError:
				continue
			try:
				cls = getattr(module, className)
			except AttributeError:
				continue
			yield cls, scriptName

	def getScriptsForAllGestures(self):
		"""Get all of the scripts and their gestures.
		@return: The Python class, gesture and script name for each mapping;
			the script name may be C{None} indicating that the gesture should be unbound for this class.
		@rtype: generator of (class, str, str)
		"""
		for gesture in self._map:
			for cls, scriptName in self.getScriptsForGesture(gesture):
				yield cls, gesture, scriptName

	def remove(self, gesture, module, className, script):
		"""Remove a gesture mapping.
		@param gesture: The gesture identifier.
		@type gesture: str
		@param module: The name of the Python module containing the target script.
		@type module: str
		@param className: The name of the class in L{module} containing the target script.
		@type className: str
		@param script: The name of the target script.
		@type script: str
		@raise ValueError: If the requested mapping does not exist.
		"""
		gesture = normalizeGestureIdentifier(gesture)
		try:
			scripts = self._map[gesture]
		except KeyError:
			raise ValueError("Mapping not found")
		scripts.remove((module, className, script))

	def save(self):
		"""Save this gesture map to disk.
		@precondition: L{load} must have been called.
		"""
		if globalVars.appArgs.secure:
			return
		if not self.fileName:
			raise ValueError("No file name")
		out = configobj.ConfigObj(encoding="UTF-8")
		out.filename = self.fileName

		for gesture, scripts in self._map.iteritems():
			for module, className, script in scripts:
				key = "%s.%s" % (module, className)
				try:
					outSect = out[key]
				except KeyError:
					out[key] = {}
					outSect = out[key]
				if script is None:
					script = "None"
				try:
					outVal = outSect[script]
				except KeyError:
					# Write the first value as a string so configobj doesn't output a comma if there's only one value.
					outVal = outSect[script] = gesture
				else:
					if isinstance(outVal, list):
						outVal.append(gesture)
					else:
						outSect[script] = [outVal, gesture]

		out.write()

class InputManager(baseObject.AutoPropertyObject):
	"""Manages functionality related to input from the user.
	Input includes key presses on the keyboard, as well as key presses on Braille displays, etc.
	"""

	#: a modifier gesture was just executed while sayAll was running
	#: @type: bool
	lastModifierWasInSayAll=False

	def __init__(self):
		#: The function to call when capturing gestures.
		#: If it returns C{False}, normal execution will be prevented.
		#: @type: callable
		self._captureFunc = None
		#: The gestures mapped for the NVDA locale.
		#: @type: L{GlobalGestureMap}
		self.localeGestureMap = GlobalGestureMap()
		#: The gestures mapped by the user.
		#: @type: L{GlobalGestureMap}
		self.userGestureMap = GlobalGestureMap()
		self.loadLocaleGestureMap()
		self.loadUserGestureMap()

	def executeGesture(self, gesture):
		"""Perform the action associated with a gesture.
		@param gesture: The gesture to execute.
		@type gesture: L{InputGesture}
		@raise NoInputGestureAction: If there is no action to perform.
		"""
		if watchdog.isAttemptingRecovery:
			# The core is dead, so don't try to perform an action.
			# This lets gestures pass through unhindered where possible,
			# as well as stopping a flood of actions when the core revives.
			raise NoInputGestureAction

		script = gesture.script
		focus = api.getFocusObject()
		if focus.sleepMode is focus.SLEEP_FULL or (focus.sleepMode and not getattr(script, 'allowInSleepMode', False)):
			raise NoInputGestureAction

		wasInSayAll=False
		if gesture.isModifier:
			if not self.lastModifierWasInSayAll:
				wasInSayAll=self.lastModifierWasInSayAll=sayAllHandler.isRunning()
		elif self.lastModifierWasInSayAll:
			wasInSayAll=True
			self.lastModifierWasInSayAll=False
		else:
			wasInSayAll=sayAllHandler.isRunning()
		if wasInSayAll:
			gesture.wasInSayAll=True

		speechEffect = gesture.speechEffectWhenExecuted
		if speechEffect == gesture.SPEECHEFFECT_CANCEL:
			queueHandler.queueFunction(queueHandler.eventQueue, speech.cancelSpeech)
		elif speechEffect in (gesture.SPEECHEFFECT_PAUSE, gesture.SPEECHEFFECT_RESUME):
			queueHandler.queueFunction(queueHandler.eventQueue, speech.pauseSpeech, speechEffect == gesture.SPEECHEFFECT_PAUSE)

		if log.isEnabledFor(log.IO) and not gesture.isModifier:
			log.io("Input: %s" % gesture.logIdentifier)

		if self._captureFunc:
			try:
				if self._captureFunc(gesture) is False:
					return
			except:
				log.error("Error in capture function, disabling", exc_info=True)
				self._captureFunc = None

		if gesture.isModifier:
			raise NoInputGestureAction

		if config.conf["keyboard"]["speakCommandKeys"] and gesture.shouldReportAsCommand:
			queueHandler.queueFunction(queueHandler.eventQueue, speech.speakMessage, gesture.displayName)

		gesture.reportExtra()

		# #2953: if an intercepted command Script (script that sends a gesture) is queued
		# then queue all following gestures (that don't have a script) with a fake script so that they remain in order.
		if not script and scriptHandler._numIncompleteInterceptedCommandScripts:
			script=lambda gesture: gesture.send()


		if script:
			scriptHandler.queueScript(script, gesture)
			return

		raise NoInputGestureAction

	def _get_isInputHelpActive(self):
		"""Whether input help is enabled, wherein the function of each key pressed by the user is reported but not executed.
		@rtype: bool
		"""
		return self._captureFunc == self._inputHelpCaptor

	def _set_isInputHelpActive(self, enable):
		if enable:
			self._captureFunc = self._inputHelpCaptor
		elif self.isInputHelpActive:
			self._captureFunc = None

	def _inputHelpCaptor(self, gesture):
		bypass = gesture.bypassInputHelp or getattr(gesture.script, "bypassInputHelp", False)
		queueHandler.queueFunction(queueHandler.eventQueue, self._handleInputHelp, gesture, onlyLog=bypass)
		return bypass

	def _handleInputHelp(self, gesture, onlyLog=False):
		textList = [gesture.displayName]
		script = gesture.script
		runScript = False
		logMsg = "Input help: gesture %s"%gesture.logIdentifier
		if script:
			scriptName = scriptHandler.getScriptName(script)
			logMsg+=", bound to script %s" % scriptName
			scriptLocation = scriptHandler.getScriptLocation(script)
			if scriptLocation:
				logMsg += " on %s" % scriptLocation
			if scriptName == "toggleInputHelp":
				runScript = True
			else:
				desc = script.__doc__
				if desc:
					textList.append(desc)

		log.info(logMsg)
		if onlyLog:
			return

		import braille
		braille.handler.message("\t\t".join(textList))
		# Punctuation must be spoken for the gesture name (the first chunk) so that punctuation keys are spoken.
		speech.speakText(textList[0], reason=controlTypes.REASON_MESSAGE, symbolLevel=characterProcessing.SYMLVL_ALL)
		for text in textList[1:]:
			speech.speakMessage(text)

		if runScript:
			script(gesture)

	def loadUserGestureMap(self):
		self.userGestureMap.clear()
		try:
			self.userGestureMap.load(os.path.join(globalVars.appArgs.configPath, "gestures.ini"))
		except IOError:
			log.debugWarning("No user gesture map")

	def loadLocaleGestureMap(self):
		self.localeGestureMap.clear()
		lang = languageHandler.getLanguage()
		try:
			self.localeGestureMap.load(os.path.join("locale", lang, "gestures.ini"))
		except IOError:
			try:
				self.localeGestureMap.load(os.path.join("locale", lang.split('_')[0], "gestures.ini"))
			except IOError:
				log.debugWarning("No locale gesture map for language %s" % lang)

	def emulateGesture(self, gesture):
		"""Convenience method to emulate a gesture.
		First, an attempt will be made to execute the gesture using L{executeGesture}.
		If that fails, the gesture will be sent to the operating system if possible using L{InputGesture.send}.
		@param gesture: The gesture to execute.
		@type gesture: L{InputGesture}
		"""
		try:
			return self.executeGesture(gesture)
		except NoInputGestureAction:
			pass
		try:
			gesture.send()
		except NotImplementedError:
			pass

	def getAllGestureMappings(self, obj=None, ancestors=None):
		if not obj:
			obj = api.getFocusObject()
			ancestors = api.getFocusAncestors()
		return _AllGestureMappingsRetriever(obj, ancestors).results

class _AllGestureMappingsRetriever(object):

	def __init__(self, obj, ancestors):
		self.results = {}
		self.scriptInfo = {}
		self.handledGestures = set()

		self.addGlobalMap(manager.userGestureMap)
		self.addGlobalMap(manager.localeGestureMap)
		import braille
		gmap = braille.handler.display.gestureMap
		if gmap:
			self.addGlobalMap(gmap)

		# Global plugins.
		import globalPluginHandler
		for plugin in globalPluginHandler.runningPlugins:
			self.addObj(plugin)

		# App module.
		app = obj.appModule
		if app:
			self.addObj(app)

		# Tree interceptor.
		ti = obj.treeInterceptor
		if ti:
			self.addObj(ti)

		# NVDAObject.
		self.addObj(obj)
		for anc in reversed(ancestors):
			self.addObj(anc, isAncestor=True)

		# Global commands.
		import globalCommands
		self.addObj(globalCommands.commands)

	def addResult(self, scriptInfo):
		self.scriptInfo[scriptInfo.cls, scriptInfo.scriptName] = scriptInfo
		try:
			cat = self.results[scriptInfo.category]
		except KeyError:
			cat = self.results[scriptInfo.category] = {}
		cat[scriptInfo.displayName] = scriptInfo

	def addGlobalMap(self, gmap):
		for cls, gesture, scriptName in gmap.getScriptsForAllGestures():
			key = (cls, gesture)
			if key in self.handledGestures:
				continue
			self.handledGestures.add(key)
			if scriptName is None:
				# The global map specified that no script should execute for this gesture and object.
				continue
			try:
				scriptInfo = self.scriptInfo[cls, scriptName]
			except KeyError:
				if scriptName.startswith("kb:"):
					scriptInfo = self.makeKbEmuScriptInfo(cls, scriptName)
				else:
					try:
						script = getattr(cls, "script_%s" % scriptName)
					except AttributeError:
						continue
					scriptInfo = self.makeNormalScriptInfo(cls, scriptName, script)
					if not scriptInfo:
						continue
				self.addResult(scriptInfo)
			scriptInfo.gestures.append(gesture)

	def makeKbEmuScriptInfo(self, cls, scriptName):
		info = AllGesturesScriptInfo(cls, scriptName)
		info.category = SCRCAT_KBEMU
		info.displayName = scriptName[3:]
		return info

	def makeNormalScriptInfo(self, cls, scriptName, script):
		info = AllGesturesScriptInfo(cls, scriptName)
		info.category = self.getScriptCategory(cls, script)
		info.displayName = script.__doc__
		if not info.displayName:
			return None
		return info

	def getScriptCategory(self, cls, script):
		try:
			return script.category
		except AttributeError:
			pass
		try:
			return cls.scriptCategory
		except AttributeError:
			pass
		return SCRCAT_MISC

	def addObj(self, obj, isAncestor=False):
		scripts = {}
		for cls in obj.__class__.__mro__:
			for scriptName, script in cls.__dict__.iteritems():
				if not scriptName.startswith("script_"):
					continue
				if isAncestor and not getattr(script, "canPropagate", False):
					continue
				scriptName = scriptName[7:]
				try:
					scriptInfo = self.scriptInfo[cls, scriptName]
				except KeyError:
					scriptInfo = self.makeNormalScriptInfo(cls, scriptName, script)
					if not scriptInfo:
						continue
					self.addResult(scriptInfo)
				scripts[script] = scriptInfo
		for gesture, script in obj._gestureMap.iteritems():
			try:
				scriptInfo = scripts[script.__func__]
			except KeyError:
				continue
			key = (scriptInfo.cls, gesture)
			if key in self.handledGestures:
				continue
			self.handledGestures.add(key)
			scriptInfo.gestures.append(gesture)

class AllGesturesScriptInfo(object):
	__slots__ = ("cls", "scriptName", "category", "displayName", "gestures")
	
	def __init__(self, cls, scriptName):
		self.cls = cls
		self.scriptName = scriptName
		self.gestures = []

	@property
	def moduleName(self):
		return self.cls.__module__

	@property
	def className(self):
		return self.cls.__name__

def normalizeGestureIdentifier(identifier):
	"""Normalize a gesture identifier so that it matches other identifiers for the same gesture.
	Any items separated by a + sign after the source are considered to be of indeterminate order
	and are reordered into Python set ordering.
	Then the entire identifier is converted to lower case.
	"""
	prefix, main = identifier.split(":", 1)
	main = main.split("+")
	# The order of the parts doesn't matter as far as the user is concerned,
	# but we need them to be in a determinate order so they will match other gesture identifiers.
	# We use Python's set ordering.
	main = "+".join(frozenset(main))
	return u"{0}:{1}".format(prefix, main).lower()

#: Maps registered source prefix strings to L{InputGesture} classes.
gestureSources = weakref.WeakValueDictionary()

def registerGestureSource(source, gestureCls):
	"""Register an input gesture class for a source prefix string.
	The specified gesture class will be used for queries regarding all gesture identifiers with the given source prefix.
	For example, if "kb" is registered with the C{KeyboardInputGesture} class,
	any queries for "kb:tab" or "kb(desktop):tab" will be directed to the C{KeyboardInputGesture} class.
	If there is no exact match for the source, any parenthesised portion is stripped.
	For example, for "br(baum):d1", if "br(baum)" isn't registered,
	"br" will be used if it is registered.
	This registration is used, for example, to get the display text for a gesture identifier.
	@param source: The source prefix for associated gesture identifiers.
	@type source: basestring
	@param gestureCls: The input gesture class.
	@type gestureCls: L{InputGesture}
	"""
	gestureSources[source] = gestureCls

def _getGestureClsForIdentifier(identifier):
	"""Get the registered gesture class for an identifier.
	"""
	source = identifier.split(":", 1)[0]
	try:
		return gestureSources[source]
	except KeyError:
		pass
	genSource = source.split("(", 1)[0]
	if genSource:
		try:
			return gestureSources[genSource]
		except KeyError:
			pass
	raise LookupError("Gesture source not registered: %s" % source)

def getDisplayTextForGestureIdentifier(identifier):
	"""Get the text to be presented to the user describing a given gesture identifier.
	The display text consists of two strings:
	the gesture's source (e.g. "laptop keyboard")
	and the specific gesture (e.g. "alt+tab").
	@param identifier: The normalized gesture identifier in question.
	@type identifier: basestring
	@return: A tuple of (source, specificGesture).
	@rtype: tuple of (basestring, basestring)
	@raise LookupError: If no display text can be determined.
	"""
	gcls = _getGestureClsForIdentifier(identifier)
	try:
		return gcls.getDisplayTextForIdentifier(identifier)
	except:
		raise
		raise LookupError("Couldn't get display text for identifier: %s" % identifier)

#: The singleton input manager instance.
#: @type: L{InputManager}
manager = None

def initialize():
	"""Initializes input core, creating a global L{InputManager} singleton.
	"""
	global manager
	manager=InputManager()

def terminate():
	"""Terminates input core.
	"""
	global manager
	manager=None
