# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2014-2022 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Framework for presentation of math.
Three types of presentation are supported: speech, braille and interaction.
All of these accept MathML markup.
Plugins can register their own implementation for any or all of these
using L{registerProvider}.
"""

import re
import typing
from typing import List, Optional, Union

from NVDAObjects.window import Window
import controlTypes
import api
import virtualBuffers
import eventHandler
from logHandler import log
import ui
import textInfos

if typing.TYPE_CHECKING:
	from speech.commands import SpeechCommand  # noqa F401: type-checking only


class MathPresentationProvider(object):
	"""Implements presentation of math content.
	A single provider does not need to implement all presentation types.
	"""

	def getSpeechForMathMl(self, mathMl: str) -> List[Union[str, "SpeechCommand"]]:
		"""Get speech output for specified MathML markup.
		@param mathMl: The MathML markup.
		@return: A speech sequence.
		"""
		raise NotImplementedError

	def getBrailleForMathMl(self, mathMl: str) -> str:
		"""Get braille output for specified MathML markup.
		@param mathMl: The MathML markup.
		@return: A string of Unicode braille.
		"""
		raise NotImplementedError

	def interactWithMathMl(self, mathMl: str) -> None:
		"""Begin interaction with specified MathML markup.
		@param mathMl: The MathML markup.
		"""
		raise NotImplementedError


speechProvider: Optional[MathPresentationProvider] = None
brailleProvider: Optional[MathPresentationProvider] = None
interactionProvider: Optional[MathPresentationProvider] = None


def registerProvider(
		provider: MathPresentationProvider,
		speech: bool = False,
		braille: bool = False,
		interaction: bool = False,
):
	"""Register a math presentation provider.
	@param provider: The provider to register.
	@param speech: Whether this provider supports speech output.
	@param braille: Whether this provider supports braille output.
	@param interaction: Whether this provider supports interaction.
	"""
	global speechProvider, brailleProvider, interactionProvider
	if speech:
		speechProvider = provider
	if braille:
		brailleProvider = provider
	if interaction:
		interactionProvider = provider


def initialize() -> None:
	# Register builtin providers if a plugin hasn't registered others.
	if not speechProvider or not brailleProvider or not interactionProvider:
		from . import mathPlayer
		try:
			provider = mathPlayer.MathPlayer()
		except:
			log.warning("MathPlayer 4 not available")
		else:
			registerProvider(provider, speech=not speechProvider,
				braille=not brailleProvider, interaction=not interactionProvider)


class MathInteractionNVDAObject(Window):
	"""Base class for a fake NVDAObject which can be focused while interacting with math.
	Subclasses can bind commands to interact with the content
	and produce speech and braille output as they wish.
	To begin interaction, call L{setFocus}.
	Pressing escape exits interaction.
	"""

	role = controlTypes.Role.MATH
	# Override the window name.
	name = None
	# Any tree interceptor should not apply here.
	treeInterceptor = None

	def __init__(self, provider=None, mathMl=None):
		self.parent = parent = api.getFocusObject()
		self.provider = provider
		super(MathInteractionNVDAObject, self).__init__(windowHandle=parent.windowHandle)

	def setFocus(self):
		ti = self.parent.treeInterceptor
		if isinstance(ti, virtualBuffers.VirtualBuffer):
			# Normally, when entering browse mode from a descendant (e.g. dialog),
			# we want the cursor to move to the focus (#3145).
			# However, we don't want this for math, as math isn't focusable.
			ti._enteringFromOutside = True
		eventHandler.executeEvent("gainFocus", self)

	def script_exit(self, gesture):
		eventHandler.executeEvent("gainFocus", self.parent)
	# Translators: Describes a command.
	script_exit.__doc__ = _("Exit math interaction")

	__gestures = {
		"kb:escape": "exit",
	}

RE_STRIP_XML_PREFIX = re.compile(r"^.*?(?=<(?:\w+:)?math[ >])")
def stripExtraneousXml(xml):
	"""Strip extraneous XML from MathML.
	This is needed where retrieving MathML produces more than just the math tag.
	Currently, this strips anything before the opening of the math tag.
	"""
	return RE_STRIP_XML_PREFIX.sub("", xml)


def getMathMlFromTextInfo(pos: textInfos.TextInfo) -> Optional[str]:
	"""Get MathML (if any) at the start of a TextInfo.
	@param pos: The TextInfo in question.
	@return: The MathML or C{None} if there is no math.
	"""
	pos = pos.copy()
	pos.expand(textInfos.UNIT_CHARACTER)
	for item in reversed(pos.getTextWithFields()):
		if not isinstance(item, textInfos.FieldCommand) or item.command != "controlStart":
			continue
		field = item.field
		if field.get("role") != controlTypes.Role.MATH:
			continue
		try:
			return pos.getMathMl(field)
		except (NotImplementedError, LookupError):
			continue
	return None


def interactWithMathMl(mathMl: str) -> None:
	"""Begin interaction with specified MathML markup, reporting any errors to the user.
	This is intended to be called from scripts.
	If interaction isn't supported, this will be reported to the user.
	The script should return after calling this function.
	@param mathMl: The MathML markup.
	"""
	if not interactionProvider:
		# Translators: Reported when the user attempts math interaction
		# but math interaction is not supported.
		ui.message(_("Math interaction not supported."))
		return
	return interactionProvider.interactWithMathMl(mathMl)


RE_MATH_LANG = re.compile(r"""<math.*? xml:lang=["']([^"']+)["'].*?>""")
def getLanguageFromMath(mathMl):
	"""Get the language specified in a math tag.
	@return: The language or C{None} if unspeicifed.
	@rtype: str
	"""
	m = RE_MATH_LANG.search(mathMl)
	if m:
		return m.group(1)
	return None

RE_MATH_APPEND = re.compile(r"(<math[^>]*)>")
def insertLanguageIntoMath(mathMl, language):
	"""Insert the specified language into a math tag.
	"""
	return RE_MATH_APPEND.sub(r'\1 xml:lang="%s">' % language, mathMl, count=1)
