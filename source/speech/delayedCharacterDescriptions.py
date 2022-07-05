# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022 NV Access Limited, David CM.

import config
import textInfos
from core import callLater
from synthDriverHandler import getSynth

characterDescriptionTimer = None


class _DelayedCharacterDescriptionTextInfo(textInfos._SupportsGetTextWithFields):
	"""
	Used to preserve data from a TextInfo object.
	"""

	def __init__(self, origTextInfo: textInfos._SupportsGetTextWithFields):
		self.text = origTextInfo.text
		self._fields = origTextInfo.getTextWithFields({})

	def getTextWithFields(self, formatConfig=None):
		return self._fields


def cancelDelayedCharacterDescription() -> None:
	"""
	Stops the timer used for delayed character descriptions.
	Should be called when a new sentence is sent or the user cancels the speech,
	e.g, by pressing control key.
	If this function is called and no delayed character description is pending, it will have no effect.
	"""
	global characterDescriptionTimer
	if characterDescriptionTimer and characterDescriptionTimer.IsRunning():
		characterDescriptionTimer.Stop()
		characterDescriptionTimer = None


def _speakDelayedCharacterDescription(info: _DelayedCharacterDescriptionTextInfo) -> None:
	"""
	Should be called from a timer after a delay.
	Will check if a character description is available for a locale, then speak it.
	"""
	if info.text.strip() == "":
		return
	from .speech import getCharDescListFromText, _spellTextWithFields, getCurrentLanguage
	curLang = getCurrentLanguage()
	if config.conf['speech']['autoLanguageSwitching']:
		for command in info.getTextWithFields():
			if isinstance(command, textInfos.FieldCommand) and command.command == "formatChange":
				curLang = command.field.get('language', curLang)
	_, description = getCharDescListFromText(info.text, locale=curLang)[0]
	if description:
		_spellTextWithFields(info, useCharacterDescriptions=True)


def startDelayedCharacterDescriptionSpeaking(info: textInfos.TextInfo) -> None:
	"""
	Will set the timer to speak a delayed character description.
	Creates a copy of required information from the TextInfo.
	Requires delayed character descriptions being enabled.
	"""
	global characterDescriptionTimer
	if config.conf["speech"][getSynth().name]["delayedCharacterDescriptions"]:
		cancelDelayedCharacterDescription()
		characterDescriptionTimer = callLater(
			config.conf["speech"][getSynth().name]["delayedCharacterDescriptionsTimeoutMs"],
			_speakDelayedCharacterDescription,
			_DelayedCharacterDescriptionTextInfo(info)
		)
