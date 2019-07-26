# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2017 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""Upgrade speech dict files
"""

import globalVars
import os
import api
import glob
from logHandler import log
from .speechDictVars import speechDictsPath

voiceDictsPath = os.path.join(speechDictsPath, r"voiceDicts.v1")
voiceDictsBackupPath = os.path.join(speechDictsPath, r"voiceDictsBackup.v0")

def createVoiceDictFileName(synthName, voiceName):
	""" Creates a filename used for the voice dictionary files.
	this is in the format synthName-voiceName.dic
	"""
	fileNameFormat = u"{synth}-{voice}.dic"
	return fileNameFormat.format(
			synth = synthName,
			voice = api.filterFileName(voiceName)
			)

def doAnyUpgrades(synth):
	""" Do any upgrades required for the synth passed in.
	"""
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
	""" Move all files for the synth to the backup dir for each file in the backup
	dir copy it to the synthvoice dir using the new name if it we have one.
	"""
	import shutil
	
	if not os.path.isdir(voiceDictsPath):
		os.makedirs(voiceDictsPath)
	if not os.path.isdir(voiceDictsBackupPath):
		os.makedirs(voiceDictsBackupPath)
	
	newDictPath = os.path.join(voiceDictsPath,synthName)
	needsUpgrade = not os.path.isdir(newDictPath)
	if needsUpgrade:
		log.info("Upgrading voice dictionaries for %s"%synthName)

		# always make the new directory, this prevents the upgrade from
		# occuring more than once.
		os.makedirs(newDictPath)

		# look for files that need to be upgraded  in the old voice 
		# dicts diectory
		voiceDictGlob=os.path.join(
				speechDictsPath,
				r"{synthName}*".format(synthName=synthName)
				)
		log.debug("voiceDictGlob: %s"%voiceDictGlob)

		for actualPath in glob.glob(voiceDictGlob):
			log.debug("processing file: %s" % actualPath)
			# files will be copied here before we modify them so as to avoid
			# any data loss.
			shutil.copy(actualPath, voiceDictsBackupPath)
			
			actualBasename = os.path.basename(actualPath)
			log.debug("basename: %s" % actualBasename)
			
			renameTo = actualBasename
			if oldFileNameToNewFileNameList:
				for oldFname, newFname in oldFileNameToNewFileNameList:
					if oldFname == actualBasename:
						log.debug("renaming {} to {} and moving to {}".format(
							actualPath,
							newFname,
							newDictPath
							))
						renameTo = newFname
						break
			shutil.move(actualPath, os.path.join(newDictPath, renameTo))

def _doEspeakDictUpgrade():
	synthName = "espeak"
	def getNextVoice():
		for ID, (oldName, newName) in espeakNameChanges.items():
			yield (
					createVoiceDictFileName(synthName, oldName),
					createVoiceDictFileName(synthName, newName)
					)
	_doSynthVoiceDictBackupAndMove(synthName, list(getNextVoice()))

# the ID maped to old and new names for voices in espeak-ng
# "old" used in NVDA 2017.3 "new" in NVDA 2017.4
espeakNameChanges = {
	"af": [u"afrikaans", u"Afrikaans"],
	"am": [u"amharic", u"Amharic"],
	"an": [u"aragonese", u"Aragonese"],
	"ar": [u"arabic", u"Arabic"],
	"as": [u"assamese", u"Assamese"],
	"az": [u"azerbaijani", u"Azerbaijani"],
	"bg": [u"bulgarian", u"Bulgarian"],
	"bn": [u"bengali", u"Bengali"],
	"bs": [u"bosnian", u"Bosnian"],
	"ca": [u"catalan", u"Catalan"],
	"cmn": [u"Mandarin", u"Chinese (Mandarin)"],
	"cs": [u"czech", u"Czech"],
	"cy": [u"welsh", u"Welsh"],
	"da": [u"danish", u"Danish"],
	"de": [u"german", u"German"],
	"el": [u"greek", u"Greek"],
	"en-029": [u"en-westindies", u"English (Caribbean)"],
	"en": [u"english", u"English (Great Britain)"],
	"en-gb-scotland": [u"en-scottish", u"English (Scotland)"],
	"en-gb-x-gbclan": [u"english-north", u"English (Lancaster)"],
	"en-gb-x-gbcwmd": [u"english_wmids", u"English (West Midlands)"],
	"en-gb-x-rp": [u"english_rp", u"English (Received Pronunciation)"],
	"en-us": [u"english-us", u"English (America)"],
	"eo": [u"esperanto", u"Esperanto"],
	"es": [u"spanish", u"Spanish (Spain)"],
	"es-419": [u"spanish-latin-am", u"Spanish (Latin America)"],
	"et": [u"estonian", u"Estonian"],
	"eu": [u"basque", u"Basque"],
	"fa": [u"Persian+English-UK", u"Persian"],
	"fa-latn": [u"persian-pinglish", u"Persian (Pinglish)"],
	"fi": [u"finnish", u"Finnish"],
	"fr-be": [u"french-Belgium", u"French (Belgium)"],
	"fr": [u"french", u"French (France)"],
	"ga": [u"irish-gaeilge", u"Gaelic (Irish)"],
	"gd": [u"scottish-gaelic", u"Gaelic (Scottish)"],
	"gn": [u"guarani", u"Guarani"],
	"grc": [u"greek-ancient", u"Greek (Ancient)"],
	"gu": [u"gujarati", u"Gujarati"],
	"hi": [u"hindi", u"Hindi"],
	"hr": [u"croatian", u"Croatian"],
	"hu": [u"hungarian", u"Hungarian"],
	"hy": [u"armenian", u"Armenian (East Armenia)"],
	"hy-arevmda": [u"armenian-west", u"Armenian (West Armenia)"],
	"ia": [u"interlingua", u"Interlingua"],
	"id": [u"indonesian", u"Indonesian"],
	"is": [u"icelandic", u"Icelandic"],
	"it": [u"italian", u"Italian"],
	"ja": [u"japanese","Japanese"], # Used to have ID 'jp'
	"jbo": [u"lojban", u"Lojban"],
	"ka": [u"georgian", u"Georgian"],
	"kl": [u"greenlandic", u"Greenlandic"],
	"kn": [u"kannada", u"Kannada"],
	"ko": [u"Korean", u"Korean"],
	"ku": [u"kurdish", u"Kurdish"],
	"ky": [u"kyrgyz", u"Kyrgyz"],
	"la": [u"latin", u"Latin"],
	"lfn": [u"lingua_franca_nova", u"Lingua Franca Nova"],
	"lt": [u"lithuanian", u"Lithuanian"],
	"lv": [u"latvian", u"Latvian"],
	"mk": [u"macedonian", u"Macedonian"],
	"ml": [u"malayalam", u"Malayalam"],
	"mr": [u"marathi", u"Marathi"],
	"ms": [u"malay", u"Malay"],
	"mt": [u"maltese", u"Maltese"],
	"my": [u"burmese", u"Burmese"],
	"nci": [u"nahuatl-classical", u"Nahuatl (Classical)"],
	"ne": [u"nepali", u"Nepali"],
	"nl": [u"dutch", u"Dutch"],
	"nb": [u"norwegian", u"Norwegian Bokmål"], # Used to have ID "no"
	"om": [u"oromo", u"Oromo"],
	"or": [u"oriya", u"Oriya"],
	"pa": [u"punjabi", u"Punjabi"],
	"pap": [u"papiamento", u"Papiamento"],
	"pl": [u"polish", u"Polish"],
	"pt": [u"portugal", u"Portuguese (Portugal)"], # Used to have ID "pt-pt"
	"pt-br": [u"brazil", u"Portuguese (Brazil)"],
	"ro": [u"romanian", u"Romanian"],
	"ru": [u"russian", u"Russian"],
	"si": [u"sinhala", u"Sinhala"],
	"sk": [u"slovak", u"Slovak"],
	"sl": [u"slovenian", u"Slovenian"],
	"sq": [u"albanian", u"Albanian"],
	"sr": [u"serbian", u"Serbian"],
	"sv": [u"swedish", u"Swedish"],
	"sw": [u"swahili", u"Swahili"],
	"ta": [u"tamil", u"Tamil"],
	"te": [u"telugu", u"Telugu"],
	"tn": [u"setswana", u"Setswana"],
	"tr": [u"turkish", u"Turkish"],
	"tt": [u"tatar", u"Tatar"],
	"ur": [u"urdu", u"Urdu"],
	"vi": [u"vietnam", u"Vietnamese (Northern)"],
	"vi-vn-x-central": [u"vietnam_hue", u"Vietnamese (Central)"],
	"vi-vn-x-south": [u"vietnam_sgn", u"Vietnamese (Southern)"],
	"yue": [u"cantonese", u"Chinese (Cantonese)"],
}
