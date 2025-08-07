# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2017-2023 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""Upgrade speech dict files"""

from typing import Any
import globalVars
import os
import api
import glob
from logHandler import log
from NVDAState import WritePaths


def __getattr__(attrName: str) -> Any:
	"""Module level `__getattr__` used to preserve backward compatibility."""
	import NVDAState

	if NVDAState._allowDeprecatedAPI():
		if attrName == "speechDictsPath":
			log.warning(
				"speechDictHandler.dictFormatUpgrade.speechDictsPath is deprecated, "
				"instead use NVDAState.WritePaths.speechDictsDir",
				stack_info=True,
			)
			return WritePaths.speechDictsDir

		if attrName == "voiceDictsPath":
			log.warning(
				"speechDictHandler.dictFormatUpgrade.voiceDictsPath is deprecated, "
				"instead use NVDAState.WritePaths.voiceDictsDir",
				stack_info=True,
			)
			return WritePaths.voiceDictsDir

		if attrName == "voiceDictsBackupPath":
			log.warning(
				"speechDictHandler.dictFormatUpgrade.voiceDictsBackupPath is deprecated, "
				"instead use NVDAState.WritePaths.voiceDictsBackupDir",
				stack_info=True,
			)
			return WritePaths.voiceDictsBackupDir

	raise AttributeError(f"module {repr(__name__)} has no attribute {repr(attrName)}")


def createVoiceDictFileName(synthName, voiceName):
	"""Creates a filename used for the voice dictionary files.
	this is in the format synthName-voiceName.dic
	"""
	fileNameFormat = "{synth}-{voice}.dic"
	return fileNameFormat.format(
		synth=synthName,
		voice=api.filterFileName(voiceName),
	)


def doAnyUpgrades(synth):
	"""Do any upgrades required for the synth passed in."""
	if globalVars.appArgs.launcher:
		# When running from the launcher we don't upgrade dicts because the user may decide not to install this version,
		# and the dict location may not be compatible with the already installed version. See #7688
		# We allow the upgrade when secure arg is present so that dictionaries work on secure screens.
		return

	# We know the transform required for Espeak, so try regardless of
	# the synth currently set.
	_doEspeakDictUpgrade()

	if synth.name == "espeak":
		# nothing more we can do until a different synth is used
		return

	# for any other synth, we can only do the backup and move if the synth
	# is loaded, because we need the synth name
	# For these synths, no name change is required so we dont pass in a name
	# mapping.
	_doSynthVoiceDictBackupAndMove(synth.name)


def _doSynthVoiceDictBackupAndMove(synthName, oldFileNameToNewFileNameList=None):
	"""Move all files for the synth to the backup dir for each file in the backup
	dir copy it to the synthvoice dir using the new name if it we have one.
	"""
	import shutil

	if not os.path.isdir(WritePaths.voiceDictsDir):
		os.makedirs(WritePaths.voiceDictsDir)
	if not os.path.isdir(WritePaths.voiceDictsBackupDir):
		os.makedirs(WritePaths.voiceDictsBackupDir)

	newDictPath = os.path.join(WritePaths.voiceDictsDir, synthName)
	needsUpgrade = not os.path.isdir(newDictPath)
	if needsUpgrade:
		log.info("Upgrading voice dictionaries for %s" % synthName)

		# always make the new directory, this prevents the upgrade from
		# occuring more than once.
		os.makedirs(newDictPath)

		# look for files that need to be upgraded  in the old voice
		# dicts diectory
		voiceDictGlob = os.path.join(
			WritePaths.speechDictsDir,
			"{synthName}*".format(synthName=synthName),
		)
		log.debug("voiceDictGlob: %s" % voiceDictGlob)

		for actualPath in glob.glob(voiceDictGlob):
			log.debug("processing file: %s" % actualPath)
			# files will be copied here before we modify them so as to avoid
			# any data loss.
			shutil.copy(actualPath, WritePaths.voiceDictsBackupDir)

			actualBasename = os.path.basename(actualPath)
			log.debug("basename: %s" % actualBasename)

			renameTo = actualBasename
			if oldFileNameToNewFileNameList:
				for oldFname, newFname in oldFileNameToNewFileNameList:
					if oldFname == actualBasename:
						log.debug(
							"renaming {} to {} and moving to {}".format(
								actualPath,
								newFname,
								newDictPath,
							),
						)
						renameTo = newFname
						break
			shutil.move(actualPath, os.path.join(newDictPath, renameTo))


def _doEspeakDictUpgrade():
	synthName = "espeak"

	def getNextVoice():
		for ID, (oldName, newName) in espeakNameChanges.items():
			yield (
				createVoiceDictFileName(synthName, oldName),
				createVoiceDictFileName(synthName, newName),
			)

	_doSynthVoiceDictBackupAndMove(synthName, list(getNextVoice()))


# the ID maped to old and new names for voices in espeak-ng
# "old" used in NVDA 2017.3 "new" in NVDA 2017.4
espeakNameChanges = {
	"af": ["afrikaans", "Afrikaans"],
	"am": ["amharic", "Amharic"],
	"an": ["aragonese", "Aragonese"],
	"ar": ["arabic", "Arabic"],
	"as": ["assamese", "Assamese"],
	"az": ["azerbaijani", "Azerbaijani"],
	"bg": ["bulgarian", "Bulgarian"],
	"bn": ["bengali", "Bengali"],
	"bs": ["bosnian", "Bosnian"],
	"ca": ["catalan", "Catalan"],
	"cmn": ["Mandarin", "Chinese (Mandarin)"],
	"cs": ["czech", "Czech"],
	"cy": ["welsh", "Welsh"],
	"da": ["danish", "Danish"],
	"de": ["german", "German"],
	"el": ["greek", "Greek"],
	"en-029": ["en-westindies", "English (Caribbean)"],
	"en": ["english", "English (Great Britain)"],
	"en-gb-scotland": ["en-scottish", "English (Scotland)"],
	"en-gb-x-gbclan": ["english-north", "English (Lancaster)"],
	"en-gb-x-gbcwmd": ["english_wmids", "English (West Midlands)"],
	"en-gb-x-rp": ["english_rp", "English (Received Pronunciation)"],
	"en-us": ["english-us", "English (America)"],
	"eo": ["esperanto", "Esperanto"],
	"es": ["spanish", "Spanish (Spain)"],
	"es-419": ["spanish-latin-am", "Spanish (Latin America)"],
	"et": ["estonian", "Estonian"],
	"eu": ["basque", "Basque"],
	"fa": ["Persian+English-UK", "Persian"],
	"fa-latn": ["persian-pinglish", "Persian (Pinglish)"],
	"fi": ["finnish", "Finnish"],
	"fr-be": ["french-Belgium", "French (Belgium)"],
	"fr": ["french", "French (France)"],
	"ga": ["irish-gaeilge", "Gaelic (Irish)"],
	"gd": ["scottish-gaelic", "Gaelic (Scottish)"],
	"gn": ["guarani", "Guarani"],
	"grc": ["greek-ancient", "Greek (Ancient)"],
	"gu": ["gujarati", "Gujarati"],
	"hi": ["hindi", "Hindi"],
	"hr": ["croatian", "Croatian"],
	"hu": ["hungarian", "Hungarian"],
	"hy": ["armenian", "Armenian (East Armenia)"],
	"hy-arevmda": ["armenian-west", "Armenian (West Armenia)"],
	"ia": ["interlingua", "Interlingua"],
	"id": ["indonesian", "Indonesian"],
	"is": ["icelandic", "Icelandic"],
	"it": ["italian", "Italian"],
	"ja": ["japanese", "Japanese"],  # Used to have ID 'jp'
	"jbo": ["lojban", "Lojban"],
	"ka": ["georgian", "Georgian"],
	"kl": ["greenlandic", "Greenlandic"],
	"kn": ["kannada", "Kannada"],
	"ko": ["Korean", "Korean"],
	"ku": ["kurdish", "Kurdish"],
	"ky": ["kyrgyz", "Kyrgyz"],
	"la": ["latin", "Latin"],
	"lfn": ["lingua_franca_nova", "Lingua Franca Nova"],
	"lt": ["lithuanian", "Lithuanian"],
	"lv": ["latvian", "Latvian"],
	"mk": ["macedonian", "Macedonian"],
	"ml": ["malayalam", "Malayalam"],
	"mr": ["marathi", "Marathi"],
	"ms": ["malay", "Malay"],
	"mt": ["maltese", "Maltese"],
	"my": ["burmese", "Burmese"],
	"nci": ["nahuatl-classical", "Nahuatl (Classical)"],
	"ne": ["nepali", "Nepali"],
	"nl": ["dutch", "Dutch"],
	"nb": ["norwegian", "Norwegian Bokmål"],  # Used to have ID "no"
	"om": ["oromo", "Oromo"],
	"or": ["oriya", "Oriya"],
	"pa": ["punjabi", "Punjabi"],
	"pap": ["papiamento", "Papiamento"],
	"pl": ["polish", "Polish"],
	"pt": ["portugal", "Portuguese (Portugal)"],  # Used to have ID "pt-pt"
	"pt-br": ["brazil", "Portuguese (Brazil)"],
	"ro": ["romanian", "Romanian"],
	"ru": ["russian", "Russian"],
	"si": ["sinhala", "Sinhala"],
	"sk": ["slovak", "Slovak"],
	"sl": ["slovenian", "Slovenian"],
	"sq": ["albanian", "Albanian"],
	"sr": ["serbian", "Serbian"],
	"sv": ["swedish", "Swedish"],
	"sw": ["swahili", "Swahili"],
	"ta": ["tamil", "Tamil"],
	"te": ["telugu", "Telugu"],
	"tn": ["setswana", "Setswana"],
	"tr": ["turkish", "Turkish"],
	"tt": ["tatar", "Tatar"],
	"ur": ["urdu", "Urdu"],
	"vi": ["vietnam", "Vietnamese (Northern)"],
	"vi-vn-x-central": ["vietnam_hue", "Vietnamese (Central)"],
	"vi-vn-x-south": ["vietnam_sgn", "Vietnamese (Southern)"],
	"yue": ["cantonese", "Chinese (Cantonese)"],
}
