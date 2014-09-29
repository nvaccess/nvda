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
	global speechProvider, brailleProvider, presentationProvider
	if speech:
		speechProvider = provider
	if braille:
		brailleProvider = provider
	if interaction:
		interactionProvider = provider

def ensureInit():
	pass
