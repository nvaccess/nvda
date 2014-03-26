#mathPlayer.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2014 NV Access Limited

"""Support for math interaction using MathPlayer 2014.
"""

import comtypes.client
from comtypes import COMError
from comtypes.gen.MathPlayer import MPInterface, IMathSpeech, IMathNavigation
from NVDAObjects.window import Window
import controlTypes
import speech
import characterProcessing
from keyboardHandler import KeyboardInputGesture
import ui
import eventHandler
import api
import characterProcessing
from logHandler import log

_initResult = None
_mpSpeech = None
_mpNavigation = None

def ensureInit():
	"""Initialize MathPlayer if it hasn't been initialized already.
	@return: Whether MathPlayer is available.
	@rtype: bool
	"""
	global _initResult, _mpSpeech, _mpNavigation
	if _initResult is not None:
		return _initResult
	try:
		_mpSpeech = comtypes.client.CreateObject(MPInterface, interface=IMathSpeech)
		_mpNavigation = _mpSpeech.QueryInterface(IMathNavigation)
		_initResult = True
	except:
		log.warning("MathPlayer 2014 not available")
		_initResult = False
	return _initResult

def getSpeechForMathMl(mathMl):
	ensureInit()
	_mpSpeech.SetMathML(mathMl)
	return (speech.SymbolLevelCommand(characterProcessing.SYMLVL_NONE),
		_mpSpeech.GetSpokenText(),
		speech.SymbolLevelCommand(None))

class MathNVDAObject(Window):
	"""A fake NVDAObject which is focused while interacting with math.
	"""

	role = controlTypes.ROLE_EQUATION
	# Override the window name.
	name = None
	# Any tree interceptor should not apply here.
	treeInterceptor = None

	def __init__(self, mathMl=None):
		ensureInit()
		parent = self.parent = api.getFocusObject()
		super(MathNVDAObject, self).__init__(windowHandle=parent.windowHandle)
		_mpSpeech.SetMathML(mathMl)

	def reportFocus(self):
		super(MathNVDAObject, self).reportFocus()
		speech.speakText(_mpSpeech.GetSpokenText(), symbolLevel=characterProcessing.SYMLVL_NONE)

	def getScript(self, gesture):
		# Pass most keys to MathPlayer. Pretty ugly.
		if isinstance(gesture, KeyboardInputGesture) and "NVDA" not in gesture.modifierNames and (
			gesture.mainKeyName in {
				"leftArrow", "rightArrow", "upArrow", "downArrow",
				"home", "end",
				"space", "backspace", "enter",
			}
			or len(gesture.mainKeyName) == 1
		):
			return self.script_navigate
		return super(MathNVDAObject, self).getScript(gesture)

	def script_navigate(self, gesture):
		modNames = gesture.modifierNames
		try:
			text = _mpNavigation.DoNavigateKeyPress(gesture.vkCode,
				"shift" in modNames, "control" in modNames, "alt" in modNames, False)
		except COMError:
			return
		speech.speakText(text, symbolLevel=characterProcessing.SYMLVL_NONE)

	def script_exit(self, gesture):
		eventHandler.executeEvent("gainFocus", self.parent)
	# Translators: Describes a command.
	script_exit.__doc__ = _("Exit math interaction")

	__gestures = {
		"kb:escape": "exit",
	}

def interactWithMath(info):
	try:
		mathMl = info.obj.getMathMlForEquation(info)
	except (NotImplementedError, AttributeError, ValueError):
		# Translators: Reported when the user attempts math interaction
		# with something that isn't math.
		ui.message(_("Not math"))
		return
	eventHandler.executeEvent("gainFocus",
		MathNVDAObject(mathMl=mathMl))
