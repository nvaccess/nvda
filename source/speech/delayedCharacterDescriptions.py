# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022 NV Access Limited, David CM.

import config
import textInfos
from core import callLater
from synthDriverHandler import getSynth

characterDescriptionTimer = None


class _DelayedCharacterDescriptionTextInfo():
	"""
	this class is used to preserve the information of the old object that contain the text.
	It's useful to use with delayed descriptions.
	"""

	def __init__(self, origTextInfo: textInfos.TextInfo):
		self.text = origTextInfo.text
		self.fields = origTextInfo.getTextWithFields({})

	def getTextWithFields(self, _=None):
		return self.fields


def cancelDelayedCharacterDescription() -> None:
	"""
	Stops the timer used for delayed character descriptions.
	This should be called when a new sentence is sent or the user cancels the speech.
	e.g, by pressing control key.
	if a timer was set for a delayed description and it's running,
	this function will stop the timer and set it to None.
	if this function is called and no delayed character description is pending, it will have no effect.
	"""
	global characterDescriptionTimer
	if characterDescriptionTimer and characterDescriptionTimer.IsRunning():
		characterDescriptionTimer.Stop()
		characterDescriptionTimer = None


def _speakDelayedCharacterDescription(info: _DelayedCharacterDescriptionTextInfo) -> None:
	"""
	this is the function that will be called from the timer after N milliseconds.
	This function will check if a character description is available and then,
	speak it by using "spellTextInfo(..., useCharacterDescriptions=True)"
	"""
	if info.text.strip() == "":
		return
	from .speech import getCharDescListFromText, spellTextInfo, getCurrentLanguage
	curLang = getCurrentLanguage()
	if config.conf['speech']['autoLanguageSwitching']:
		for k in info.fields:
			if isinstance(k, textInfos.FieldCommand) and k.command == "formatChange":
				curLang = k.field.get('language', curLang)
	_, description = getCharDescListFromText(info.text, locale=curLang)[0]
	# We can't call spellTextInfo directly because we need to check if the description is available first.
	if description:
		spellTextInfo(info, useCharacterDescriptions=True)


def startDelayedCharacterDescriptionSpeaking(info: textInfos.TextInfo) -> None:
	"""
	this function will set the timer to speak the delaied character description.
	this will keep a copy of the needed fiels by spellTextInfo function, from the provided TextInfo.
	this function will check if the delayed character descriptions are enabled first.
	"""
	global characterDescriptionTimer
	if config.conf["speech"][getSynth().name]["delayedCharacterDescriptions"]:
		cancelDelayedCharacterDescription()
		characterDescriptionTimer = callLater(
			config.conf["speech"][getSynth().name]["delayedCharacterDescriptionsTimeoutMs"],
			_speakDelayedCharacterDescription,
			_DelayedCharacterDescriptionTextInfo(info)
		)
