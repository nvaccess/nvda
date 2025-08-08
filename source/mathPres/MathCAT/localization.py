# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2025 NV Access Limited, Neil Soiffer, Ryan McCleary
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import glob
import os
from zipfile import ZipFile

import wx
from languageHandler import getLanguageDescription
from logHandler import log

from . import rulesUtils


def pathToLanguagesFolder() -> str:
	r"""Returns the full path to the Languages rules folder.
		The language rules are stored in:
	MathCAT\Rules\Languages, relative to the location of this file.

	:return: Absolute path to the Languages folder as a string.
	"""
	return os.path.join(
		os.path.dirname(os.path.abspath(__file__)),
		"..",
		"..",
		"..",
		"include",
		"nvda-mathcat",
		"assets",
		"Rules",
		"Languages",
	)

def getLanguages() -> tuple[list[str], list[str]]:
	"""Populate the language choice dropdown with available languages and their regional variants.

	This method scans the language folders and adds entries for each language and its
	regional dialects. Language folders use ISO 639-1 codes and regional variants use ISO 3166-1 alpha-2 codes.

	It also adds a special "Use Voice's Language (Auto)" option at the top.
	"""

	languageOptions: list[str] = []
	languageCodes: list[str] = []

	def addRegionalLanguages(subDir: str, language: str) -> list[str]:
		# the language variants are in folders named using ISO 3166-1 alpha-2
		# codes https://en.wikipedia.org/wiki/ISO_3166-2
		# check if there are language variants in the language folder
		if subDir != "SharedRules":
			# add to the listbox the text for this language variant together with the code
			regionalCode: str = language + "-" + subDir.upper()
			langDesc = getLanguageDescription(regionalCode)
			log.info(f"regionalCode: {regionalCode}, langDesc: {langDesc}")
			if langDesc is not None:
				languageOptions.append(f"{langDesc} ({regionalCode})")
			else:
				languageOptions.Append(f"{language} ({regionalCode})")
			languageCodes.append(regionalCode)
			return [os.path.basename(file) for file in glob.glob(os.path.join(subDir, "*_Rules.yaml"))]
		return []

	# Translators: menu item -- use the language of the voice chosen in the NVDA speech settings dialog
	# "Auto" == "Automatic" -- other items in menu are "English (en)", etc., so this matches that style
	languageOptions.append(pgettext("math", "Use Voice's Language (Auto)"))
	languageCodes.append("Auto")
	# populate the available language names in the dialog
	# the implemented languages are in folders named using the relevant ISO 639-1
	#   code https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
	languageDir: str = pathToLanguagesFolder()
	for language in os.listdir(languageDir):
		pathToLanguageDir: str = os.path.join(pathToLanguagesFolder(), language)
		if os.path.isdir(pathToLanguageDir):
			# only add this language if there is a xxx_Rules.yaml file
			if len(rulesUtils.getRulesFiles(pathToLanguageDir, addRegionalLanguages)) > 0:
				# add to the listbox the text for this language together with the code
				if language in languagesSet:
					languageOptions.append(getLanguageDescription(language) + " (" + language + ")")
				else:
					languageOptions.append(language + " (" + language + ")")
				languageCodes.append(language)
	return languageOptions, languageCodes


def getLanguageCode(langChoice: wx.Choice) -> str:
	"""Extract the language code from the selected language string in the UI.
		The selected language string is expected to contain the language code in parentheses,
	for example: "English (en)".
		:return: The language code extracted from the selection.
	"""
	langSelection: str = langChoice.GetStringSelection()
	langCode: str = langSelection[langSelection.find("(") + 1 : langSelection.find(")")]
	return langCode


def getSpeechStyles(languageCode: str) -> list[str]:
	"""Get all the speech styles for the current language.
	This sets the SpeechStyles dialog entry.

	:param thisSpeechStyle: The speech style to set or highlight in the dialog.
	"""
	from speech import getCurrentLanguage

	def getSpeechStyleFromDirectory(dir: str, lang: str) -> list[str]:
		r"""Get the speech styles from any regional dialog, from the main language, dir and if there isn't from the zip file.
		The 'lang', if it has a region dialect, is of the form 'en\uk'
		The returned list is sorted alphabetically

		:param dir: The directory path to search for speech styles.
		:param lang: Language code which may include a regional dialect (e.g., 'en\uk').
		:return: A list of speech styles sorted alphabetically.
		"""
		# start with the regional dialect, then add on any (unique) styles in the main dir
		mainLang: str = lang.split("\\")[0]  # does the right thing even if there is no regional directory
		allStyleFiles: list[str] = []
		if lang.find("\\") >= 0:
			allStyleFiles: list[str] = [
				os.path.basename(name) for name in glob.glob(dir + lang + "\\*_Rules.yaml")
			]
		allStyleFiles.extend(
			[os.path.basename(name) for name in glob.glob(dir + mainLang + "\\*_Rules.yaml")],
		)
		allStyleFiles = list(set(allStyleFiles))  # make them unique
		if len(allStyleFiles) == 0:
			# look in the .zip file for the style files -- this will have regional variants, but also have that dir
			try:
				zipFilePath: str = dir + mainLang + "\\" + mainLang + ".zip"
				zipFile: ZipFile = ZipFile(zipFilePath, "r")  # file might not exist
				allStyleFiles = [
					name.split("/")[-1] for name in zipFile.namelist() if name.endswith("_Rules.yaml")
				]
			except Exception as e:
				log.debugWarning(f"MathCAT Dialog: didn't find zip file {zipFile}. Error: {e}")
		allStyleFiles.sort()
		return allStyleFiles

	resultSpeechStyles = []
	if languageCode == "Auto":
		# list the speech styles for the current voice rather than have none listed
		languageCode = getCurrentLanguage().lower().replace("_", "-")
	languageCode = languageCode.replace("-", "\\")

	languagePath = pathToLanguagesFolder() + "\\"
	# log.info(f"languagePath={languagePath}")
	# populate the m_choiceSpeechStyle choices
	allStyleFiles = [
		# remove "_Rules.yaml" from the list
		name[: name.find("_Rules.yaml")]
		for name in getSpeechStyleFromDirectory(languagePath, languageCode)
	]
	# There isn't a LiteralSpeak rules file since it has no language-specific rules. We add it at the end.
	# Translators: at the moment, do NOT translate this string as some code specifically looks for this name.
	allStyleFiles.append("LiteralSpeak")
	for name in allStyleFiles:
		resultSpeechStyles.append((name))
	return resultSpeechStyles


languagesSet = frozenset(
	[
		"aa",
		"ab",
		"af",
		"ak",
		"an",
		"ar",
		"as",
		"av",
		"ay",
		"az",
		"ba",
		"be",
		"bg",
		"bh",
		"bi",
		"bm",
		"bn",
		"bo",
		"bs",
		"ca",
		"ce",
		"ch",
		"co",
		"cr",
		"cs",
		"cu",
		"cv",
		"cy",
		"da",
		"de",
		"dv",
		"dz",
		"ee",
		"el",
		"en",
		"en-GB",
		"en-US",
		"eo",
		"es",
		"fa",
		"fi",
		"fj",
		"fo",
		"fr",
		"fy",
		"ga",
		"gd",
		"gl",
		"gn",
		"gu",
		"gv",
		"ha",
		"he",
		"hi",
		"ho",
		"hr",
		"ht",
		"hu",
		"hy",
		"hz",
		"ia",
		"id",
		"ig",
		"ii",
		"ik",
		"io",
		"is",
		"it",
		"iu",
		"ja",
		"jv",
		"ka",
		"kg",
		"ki",
		"kj",
		"kk",
		"km",
		"kn",
		"ko",
		"ks",
		"ku",
		"kv",
		"kw",
		"ky",
		"la",
		"lb",
		"lg",
		"li",
		"ln",
		"lo",
		"lt",
		"lv",
		"mg",
		"mh",
		"mk",
		"ml",
		"mn",
		"mo",
		"ms",
		"mt",
		"my",
		"na",
		"ne",
		"ng",
		"nl",
		"nn",
		"nr",
		"nv",
		"ny",
		"oc",
		"oj",
		"om",
		"os",
		"pa",
		"pi",
		"pl",
		"ps",
		"pt",
		"qu",
		"rm",
		"ro",
		"ru",
		"rw",
		"sa",
		"sc",
		"sd",
		"se",
		"sg",
		"sh",
		"si",
		"sk",
		"sl",
		"sm",
		"sn",
		"so",
		"sq",
		"sr",
		"ss",
		"st",
		"su",
		"sv",
		"sw",
		"ta",
		"tg",
		"th",
		"ti",
		"tk",
		"tl",
		"to",
		"tr",
		"ts",
		"tt",
		"tw",
		"ty",
		"ug",
		"uk",
		"ur",
		"uz",
		"ve",
		"vi",
		"vo",
		"wa",
		"wo",
		"xh",
		"yi",
		"yo",
		"za",
		"zh",
		"zh-HANS",
		"zh-HANT",
		"zh-TW",
		"zu",
	],
)
