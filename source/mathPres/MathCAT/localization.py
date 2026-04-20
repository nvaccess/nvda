# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2026 NV Access Limited, Neil Soiffer, Ryan McCleary
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from collections.abc import Callable
from dataclasses import dataclass
import glob
import os
from zipfile import ZipFile

import libmathcat_py as libmathcat
import wx

from languageHandler import getLanguageDescription
from logHandler import log
from NVDAState import ReadPaths

from . import rulesUtils


def getLanguageToUse() -> str:
	"""Get the language preference, falling back to English if it is Auto.

	:returns: The language string to use.
	"""
	mathCATLanguageSetting: str = "en"
	try:
		# ignore regional differences if the MathCAT language setting doesn't have it.
		mathCATLanguageSetting = libmathcat.GetPreference("Language")
	except Exception:
		log.exception()

	if mathCATLanguageSetting.casefold() == "auto":
		log.debugWarning("Math language 'Auto' is unsupported. Falling back to 'en'.")
		mathCATLanguageSetting = "en"
	return mathCATLanguageSetting


def pathToLanguagesFolder() -> str:
	r"""Returns the full path to the Languages rules folder.

	The language rules are stored in:
	..\..\..\include\nvda-mathcat\assets\Rules\Languages,
	relative to the location of this file.

	:return: Absolute path to the Languages folder as a string.
	"""
	return os.path.join(
		ReadPaths.mathCATDir,
		"Rules",
		"Languages",
	)


@dataclass
class LanguageInfo:
	"""Data class to hold information about a language, including its code and description."""

	code: str
	"""Language code in the form 'en-uk' or 'en'"""

	description: str
	"""Translated description. Falls back to the first part of the language code"""


def _createAddRegionalLanguagesFunction(languages: list[LanguageInfo]) -> Callable[[str, str], list[str]]:
	def addRegionalLanguages(subDir: str, language: str) -> list[str]:
		"""Add regional language variants and append them to the captured languages list.

		The closed-over ``languages`` list is modified in place.
		:param subDir: The subdirectory representing the regional variant.
		:param language: The base language code.
		:return: A list of rule files for the regional variant.
		"""
		# the language variants are in folders named using ISO 3166-1 alpha-2
		# codes https://en.wikipedia.org/wiki/ISO_3166-2
		# check if there are language variants in the language folder
		if subDir != "SharedRules":
			# add to the list the text for this language variant together with the code
			regionalCode: str = language + "-" + subDir.upper()
			langDesc = getLanguageDescription(regionalCode)
			# Translators: {lang} is the name of the language in that language,
			# and {code} is the code for that language variant,
			# e.g. "en-UK" for English (United Kingdom).
			optionString = pgettext("math", "{lang} ({code})")
			if langDesc is not None:
				languages.append(
					LanguageInfo(
						code=regionalCode,
						description=optionString.format(lang=langDesc, code=regionalCode),
					),
				)
			else:
				log.error(
					f"MathCAT: couldn't find description for language code {regionalCode}, using {language} as description",
				)
				languages.append(
					LanguageInfo(
						code=regionalCode,
						description=optionString.format(lang=language, code=regionalCode),
					),
				)
			return [os.path.basename(file) for file in glob.glob(os.path.join(subDir, "*_Rules.yaml"))]
		return []

	return addRegionalLanguages


def getLanguages() -> list[LanguageInfo]:
	"""Populate the language choice dropdown with available languages and their regional variants.

	This method scans the language folders and adds entries for each language and its
	regional dialects. Language folders use ISO 639-1 codes and regional variants use ISO 3166-1 alpha-2 codes.

	:return: A list of LanguageInfo objects representing the available languages.
	"""

	languages: list[LanguageInfo] = []
	addRegionalLanguages = _createAddRegionalLanguagesFunction(languages)

	# populate the available language names in the dialog
	# the implemented languages are in folders named using the relevant ISO 639-1
	# code https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
	languageDir: str = pathToLanguagesFolder()
	for language in os.listdir(languageDir):
		pathToLanguageDir: str = os.path.join(pathToLanguagesFolder(), language)
		if os.path.isdir(pathToLanguageDir):
			# only add this language if there is a xxx_Rules.yaml file
			if len(rulesUtils.getRulesFiles(pathToLanguageDir, addRegionalLanguages)) > 0:
				# add to the listbox the text for this language
				languageDesc = getLanguageDescription(language)
				if languageDesc is not None:
					languages.append(
						LanguageInfo(code=language, description=languageDesc),
					)
				else:
					log.error(
						f"MathCAT: couldn't find description for language code {language}, using code as description",
					)
					languages.append(
						LanguageInfo(code=language, description=language),
					)
	return languages


def getLanguageCode(langChoice: wx.Choice) -> str:
	"""Extract the language code from the selected language string in the UI.

	The selected language string is expected to contain the language code in parentheses,
	for example: "English (en)".

	:param langChoice: The language selection combo box.

	:return: The language code extracted from the selection.
	"""
	langSelection: str = langChoice.GetStringSelection()
	langCode: str = langSelection[langSelection.find("(") + 1 : langSelection.find(")")]
	return langCode


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
		zipFilePath: str = os.path.join(dir, mainLang, f"{mainLang}.zip")
		try:
			with ZipFile(zipFilePath, "r") as zipFile:
				allStyleFiles = [
					name.split("/")[-1] for name in zipFile.namelist() if name.endswith("_Rules.yaml")
				]
		except Exception as e:
			log.debugWarning(f"MathCAT: didn't find zip file {zipFilePath}. Error: {e}")
	allStyleFiles.sort()
	return allStyleFiles


def getSpeechStyles(languageCode: str) -> list[str]:
	"""Get all the speech styles for the current language.
	This sets the SpeechStyles dialog entry.

	:param languageCode: The code of the current language.

	:return: A list of speech styles for the given language.
	"""

	resultSpeechStyles = []
	if languageCode.casefold() == "auto":
		# Fall back to English
		log.debugWarning("Math language 'Auto' is not supported. Using 'en'.")
		languageCode = "en"
	languageCode = languageCode.replace("-", "\\")

	languagePath = pathToLanguagesFolder() + "\\"
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
