#mathPlayer.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2014 NV Access Limited

"""Support for math interaction using MathPlayer 2014.
"""

import re
import comtypes.client
from comtypes import COMError
from comtypes.gen.MathPlayer import MPInterface, IMathSpeech, IMathNavigation, IMathBraille
from NVDAObjects.window import Window
import controlTypes
import speech
import characterProcessing
from keyboardHandler import KeyboardInputGesture
import ui
import eventHandler
import api
from logHandler import log
import textInfos
import braille
import virtualBuffers

_initResult = None
_mpSpeech = None
_mpNavigation = None
_mpBraille = None

def ensureInit():
	"""Initialize MathPlayer if it hasn't been initialized already.
	@return: Whether MathPlayer is available.
	@rtype: bool
	"""
	global _initResult, _mpSpeech, _mpNavigation, _mpBraille
	if _initResult is not None:
		return _initResult
	try:
		_mpSpeech = comtypes.client.CreateObject(MPInterface, interface=IMathSpeech)
		_mpNavigation = _mpSpeech.QueryInterface(IMathNavigation)
		_mpBraille = _mpSpeech.QueryInterface(IMathBraille)
		_initResult = True
	except:
		log.warning("MathPlayer 2014 not available")
		_initResult = False
	return _initResult

RE_MP_SPEECH_PAUSE = re.compile(r" *[.,](?! $) *")
def _processMpSpeech(text):
	# MathPlayer with speech tags set to none uses full stop and comma for pauses
	# with inconsistent surrounding space.
	# Full stop doesn't work with eSpeak and probably other synths because
	# they require a capital letter after a full stop to treat it as a sentence ending.
	# There must be a space after but not before either mark for some synths to honour it.
	# Therefore, fix spaces and change most full stops to commas.
	return RE_MP_SPEECH_PAUSE.sub(", ", text)

def getSpeechForMathMl(mathMl):
	ensureInit()
	_mpSpeech.SetMathML(mathMl)
	return (speech.SymbolLevelCommand(characterProcessing.SYMLVL_NONE),
		_processMpSpeech(_mpSpeech.GetSpokenText()),
		speech.SymbolLevelCommand(None))

def getBrailleForMathMl(mathMl):
	ensureInit()
	_mpSpeech.SetMathML(mathMl)
	_mpBraille.SetBrailleWidth(braille.handler.displaySize)
	return _mpBraille.GetBraille()

class MathNVDAObject(Window):
	"""A fake NVDAObject which is focused while interacting with math.
	"""

	role = controlTypes.ROLE_MATH
	# Override the window name.
	name = None
	# Any tree interceptor should not apply here.
	treeInterceptor = None

	def __init__(self, parent=None, mathMl=None):
		ensureInit()
		self.parent = parent
		super(MathNVDAObject, self).__init__(windowHandle=parent.windowHandle)
		_mpSpeech.SetMathML(mathMl)

	def reportFocus(self):
		super(MathNVDAObject, self).reportFocus()
		speech.speakText(_processMpSpeech(_mpSpeech.GetSpokenText()),
			symbolLevel=characterProcessing.SYMLVL_NONE)

	def getBrailleRegions(self, review=False):
		yield braille.NVDAObjectRegion(self, appendText=" ")
		region = braille.Region()
		region.focusToHardLeft = True
		_mpBraille.SetBrailleWidth(braille.handler.displaySize)
		region.rawText = _mpBraille.GetBraille()
		yield region

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
		speech.speakText(_processMpSpeech(text),
			symbolLevel=characterProcessing.SYMLVL_NONE)

	def script_exit(self, gesture):
		eventHandler.executeEvent("gainFocus", self.parent)
	# Translators: Describes a command.
	script_exit.__doc__ = _("Exit math interaction")

	__gestures = {
		"kb:escape": "exit",
	}

def interactWithMath(info):
	info.expand(textInfos.UNIT_CHARACTER)
	for item in reversed(info.getTextWithFields()):
		if not isinstance(item, textInfos.FieldCommand) or item.command != "controlStart":
			continue
		field = item.field
		if field.get("role") != controlTypes.ROLE_MATH:
			continue
		try:
			mathMl = info.getMathMl(field)
		except (NotImplementedError, AttributeError, ValueError):
			continue
		focus = api.getFocusObject()
		ti = focus.treeInterceptor
		if isinstance(ti, virtualBuffers.VirtualBuffer):
			# Normally, when entering browse mode from a descendant (e.g. dialog),
			# we want the cursor to move to the focus (#3145).
			# However, we don't want this for math, as math isn't focusable.
			ti._enteringFromOutside = True
		eventHandler.executeEvent("gainFocus",
			MathNVDAObject(parent=focus, mathMl=mathMl))
		return
	# Translators: Reported when the user attempts math interaction
	# with something that isn't math.
	ui.message(_("Not math"))
