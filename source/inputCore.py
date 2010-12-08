#inputCore.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010 James Teh <jamie@jantrid.net>

import sys
import os
import itertools
from configobj import ConfigObj
import baseObject
import scriptHandler
import queueHandler
import api
import speech
import config
import watchdog
from logHandler import log
import globalVars
import languageHandler

"""Core framework for handling input from the user.
Every piece of input from the user (e.g. a key press) is represented by an L{InputGesture}.
The singleton L{InputManager} (L{manager}) manages functionality related to input from the user.
For example, it is used to execute gestures and handle input help.
"""

class NoInputGestureAction(LookupError):
	"""Informs that there is no action to execute for a gesture.
	"""

class InputGesture(baseObject.AutoPropertyObject):
	"""A single gesture of input from the user.
	For example, this could be a key press on a keyboard or Braille display or a click of the mouse.
	At the very least, subclasses must implement L{_get_identifiers} and L{_get_displayName}.
	"""
	cachePropertiesByDefault = True

	def _get_identifiers(self):
		"""The identifier(s) which will be used in input gesture maps to represent this gesture.
		These identifiers will be looked up in order until a match is found.
		A single identifier should take the form: C{source:id}
		where C{source} is a few characters representing the source of this gesture
		and C{id} is the specific gesture.
		An example identifier is: C{kb(desktop):NVDA+1}
		Subclasses must implement this method.
		@return: One or more identifiers which uniquely identify this gesture.
		@rtype: list or tuple of str
		"""
		raise NotImplementedError

	def _get_displayName(self):
		"""The name of this gesture as presented to the user.
		Subclasses must implement this method.
		@return: The display name.
		@rtype: str
		"""
		raise NotImplementedError

	#: Whether this gesture should be reported when reporting of command gestures is enabled.
	#: @type: bool
	shouldReportAsCommand = True

	SPEECHEFFECT_CANCEL = "cancel"
	SPEECHEFFECT_PAUSE = "pause"
	SPEECHEFFECT_RESUME = "resume"
	#: The effect on speech when this gesture is executed; one of the SPEECHEFFECT_* constants or C{None}.
	speechEffectWhenExecuted = SPEECHEFFECT_CANCEL

	#: Whether this gesture is only a modifier, in which case it will not search for a script to execute.
	#: @type: bool
	isModifier = False

	#: Whether this gesture should bypass input help.
	#: @type: bool
	bypassInputHelp = False

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
		return scriptHandler.findScript(self)

	def send(self):
		"""Send this gesture to the operating system.
		This is not possible for all sources.
		@raise NotImplementedError: If the source does not support sending of gestures.
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
		if entries:
			self.update(entries)

	def clear(self):
		"""Clear this map.
		"""
		self._map.clear()

	def add(self, gesture, module, className, script):
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
		"""
		gesture = normalizeGestureIdentifier(gesture)
		try:
			scripts = self._map[gesture]
		except KeyError:
			scripts = self._map[gesture] = []
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
		conf = ConfigObj(filename, file_error=True, encoding="UTF-8")
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
		for locationName, location in entries.iteritems():
			try:
				module, className = locationName.rsplit(".", 1)
			except:
				log.error("Invalid module/class specification: %s" % locationName)
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

class InputManager(baseObject.AutoPropertyObject):
	"""Manages functionality related to input from the user.
	Input includes key presses on the keyboard, as well as key presses on Braille displays, etc.
	"""

	def __init__(self):
		#: Whether input help is enabled, wherein the function of each key pressed by the user is reported but not executed.
		#: @type: bool
		self.isInputHelpActive = False
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
		app = api.getFocusObject().appModule
		if app and app.selfVoicing:
			raise NoInputGestureAction

		speechEffect = gesture.speechEffectWhenExecuted
		if speechEffect == gesture.SPEECHEFFECT_CANCEL:
			queueHandler.queueFunction(queueHandler.eventQueue, speech.cancelSpeech)
		elif speechEffect in (gesture.SPEECHEFFECT_PAUSE, gesture.SPEECHEFFECT_RESUME):
			queueHandler.queueFunction(queueHandler.eventQueue, speech.pauseSpeech, speechEffect == gesture.SPEECHEFFECT_PAUSE)

		if log.isEnabledFor(log.IO) and not gesture.isModifier:
			log.io("Input: %s" % gesture.identifiers[0])

		if self.isInputHelpActive and not gesture.bypassInputHelp:
			queueHandler.queueFunction(queueHandler.eventQueue, self._handleInputHelp, gesture)
			return

		if gesture.isModifier:
			raise NoInputGestureAction

		if config.conf["keyboard"]["speakCommandKeys"] and gesture.shouldReportAsCommand:
			queueHandler.queueFunction(queueHandler.eventQueue, speech.speakMessage, gesture.displayName)

		gesture.reportExtra()

		script = gesture.script
		if script:
			scriptHandler.queueScript(script, gesture)
			return

		raise NoInputGestureAction

	def _handleInputHelp(self, gesture):
		textList = [gesture.displayName]
		script = gesture.script
		runScript = False
		if script:
			scriptName = scriptHandler.getScriptName(script)
			scriptLocation = scriptHandler.getScriptLocation(script)
			logMsg = "Input help: gesture %s, bound to script %s" % (gesture.identifiers[0], scriptName)
			if scriptLocation:
				logMsg += " on %s" % scriptLocation
			log.info(logMsg)
			if scriptName == "toggleInputHelp":
				runScript = True
			else:
				desc = script.__doc__
				if desc:
					textList.append(desc)

		import braille
		braille.handler.message("\t\t".join(textList))
		# Punctuation must be spoken for the gesture name (the first chunk) so that punctuation keys are spoken.
		speech.speakText(textList[0], reason=speech.REASON_MESSAGE, expandPunctuation=True)
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

def normalizeGestureIdentifier(identifier):
	"""Normalize a gesture identifier so that it matches other identifiers for the same gesture.
	"""
	prefix, main = identifier.split(":", 1)
	main = main.split("+")
	# The order of all parts except the last doesn't matter as far as the user is concerned,
	# but we need them to be in a determinate order so they will match other gesture identifiers.
	# Rather than sorting, just use Python's set ordering.
	main = "+".join(itertools.chain(frozenset(main[:-1]), main[-1:]))
	return u"{0}:{1}".format(prefix, main).lower()

#: The singleton input manager instance.
#: @type: L{InputManager}
manager = InputManager()
