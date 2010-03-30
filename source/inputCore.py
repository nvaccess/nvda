#inputCore.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010 James Teh <jamie@jantrid.net>

import baseObject
import scriptHandler
import queueHandler
import api
import speech
import braille
import config
from logHandler import log

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
		# FIXME: Support other gesture types.
		import keyUtils
		return scriptHandler.findScript(keyUtils.key(self.keyName))

	def send(self):
		"""Send this gesture to the operating system.
		This is not possible for all sources.
		@raise NotImplementedError: If the source does not support sending of gestures.
		"""
		raise NotImplementedError

class InputManager(baseObject.AutoPropertyObject):
	"""Manages functionality related to input from the user.
	Input includes key presses on the keyboard, as well as key presses on Braille displays, etc.
	"""

	def __init__(self):
		#: Whether input help is enabled, wherein the function of each key pressed by the user is reported but not executed.
		#: @type: bool
		self.isInputHelpActive = False

	def executeGesture(self, gesture):
		"""Perform the action associated with a gesture.
		@param gesture: The gesture to execute.
		@type gesture: L{InputGesture}
		@raise NoInputGestureAction: If there is no action to perform.
		"""
		if api.getFocusObject().appModule.selfVoicing:
			raise NoInputGestureAction

		speechEffect = gesture.speechEffectWhenExecuted
		if speechEffect == gesture.SPEECHEFFECT_CANCEL:
			queueHandler.queueFunction(queueHandler.eventQueue, speech.cancelSpeech)
		elif speechEffect in (gesture.SPEECHEFFECT_PAUSE, gesture.SPEECHEFFECT_RESUME):
			queueHandler.queueFunction(queueHandler.eventQueue, speech.pauseSpeech, speechEffect == gesture.SPEECHEFFECT_PAUSE)

		if log.isEnabledFor(log.IO) and not gesture.isModifier:
			log.io("Input: %s" % gesture.mapKeys[0])

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
			if scriptName == "toggleInputHelp":
				runScript = True
			else:
				desc = scriptHandler.getScriptDescription(script)
				if desc:
					textList.append(desc)
				location = scriptHandler.getScriptLocation(script)
				if location:
					textList.append(_("Location: %s") % location)

		braille.handler.message("\t\t".join(textList))
		for text in textList:
			speech.speakMessage(text)

		if runScript:
			script(gesture)

#: The singleton input manager instance.
#: @type: L{InputManager}
manager = InputManager()
