#mathPres/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2014 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Framework for presentation of math.
Three types of presentation are supported: speech, braille and interaction.
All of these accept MathML markup.
Plugins can register their own implementation for any or all of these
using L{registerProvider}.
"""

from NVDAObjects.window import Window
import controlTypes
import api
import virtualBuffers
import eventHandler
from logHandler import log

class MathPresentationProvider(object):
	"""Implements presentation of math content.
	A single provider does not need to implement all presentation types.
	"""

	def getSpeechForMathMl(self, mathMl):
		"""Get speech output for specified MathML markup.
		@param mathMl: The MathML markup.
		@type mathMl: basestring
		@return: A speech sequence.
		@rtype: list of unicode and/or L{speech.SpeechCommand}
		"""
		raise NotImplementedError

	def getBrailleForMathMl(self, mathMl):
		"""Get braille output for specified MathML markup.
		@param mathMl: The MathML markup.
		@type mathMl: basestring
		@return: A string of Unicode braille.
		@rtype: unicode
		"""
		raise NotImplementedError

	def interactWithMathMl(self, mathMl):
		"""Begin interaction with specified MathML markup.
		@param mathMl: The MathML markup.
		"""
		raise NotImplementedError

speechProvider = None
brailleProvider = None
interactionProvider = None

def registerProvider(provider, speech=False, braille=False, interaction=False):
	"""Register a math presentation provider.
	@param provider: The provider to register.
	@type provider: L{MathPresentationProvider}
	@param speech: Whether this provider supports speech output.
	@type speech: bool
	@param braille: Whether this provider supports braille output.
	@type braille: bool
	@param interaction: Whether this provider supports interaction.
	@type interaction: bool
	"""
	global speechProvider, brailleProvider, interactionProvider
	if speech:
		speechProvider = provider
	if braille:
		brailleProvider = provider
	if interaction:
		interactionProvider = provider

def ensureInit():
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
	Subclasses can bind commands to itneract with the content
	and produce speech and braille output as they wish.
	To begin interaction, call L{setFocus}.
	Pressing escape exits interaction.
	"""

	role = controlTypes.ROLE_MATH
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
