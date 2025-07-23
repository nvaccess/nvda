import glob
import os
from collections.abc import Callable
from zipfile import ZipFile

import wx
from languageHandler import getLanguageDescription
from logHandler import log

from .MathCATPreferences import UserInterface


def getLanguages() -> list[str]:
	"""Populate the language choice dropdown with available languages and their regional variants.

	This method scans the language folders and adds entries for each language and its
	regional dialects. Language folders use ISO 639-1 codes and regional variants use ISO 3166-1 alpha-2 codes.

	It also adds a special "Use Voice's Language (Auto)" option at the top.
	"""

	languageOptions: list[str] = []

	def addRegionalLanguages(subDir: str, language: str) -> list[str]:
		# the language variants are in folders named using ISO 3166-1 alpha-2
		# codes https://en.wikipedia.org/wiki/ISO_3166-2
		# check if there are language variants in the language folder
		if subDir != "SharedRules":
			# add to the listbox the text for this language variant together with the code
			regionalCode: str = language + "-" + subDir.upper()
			langDesc = getLanguageDescription(regionalCode)
			if langDesc is not None:
				languageOptions.append(langDesc)
			else:
				languageOptions.Append(f"{language} ({regionalCode})")
			return [os.path.basename(file) for file in glob.glob(os.path.join(subDir, "*_Rules.yaml"))]
		return []

	# Translators: menu item -- use the language of the voice chosen in the NVDA speech settings dialog
	# "Auto" == "Automatic" -- other items in menu are "English (en)", etc., so this matches that style
	languageOptions.append(pgettext("math", "Use Voice's Language (Auto)"))
	# populate the available language names in the dialog
	# the implemented languages are in folders named using the relevant ISO 639-1
	#   code https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
	languageDir: str = UserInterface.pathToLanguagesFolder()
	for language in os.listdir(languageDir):
		pathToLanguageDir: str = os.path.join(UserInterface.pathToLanguagesFolder(), language)
		if os.path.isdir(pathToLanguageDir):
			# only add this language if there is a xxx_Rules.yaml file
			if len(getRulesFiles(pathToLanguageDir, addRegionalLanguages)) > 0:
				# add to the listbox the text for this language together with the code
				if language in languagesSet:
					languageOptions.append(getLanguageDescription(language) + " (" + language + ")")
				else:
					languageOptions.append(language + " (" + language + ")")
	return languageOptions


def getLanguageCode(langChoice: wx.Choice) -> str:
	"""Extract the language code from the selected language string in the UI.
		The selected language string is expected to contain the language code in parentheses,
	for example: "English (en)".
		:return: The language code extracted from the selection.
	"""
	langSelection: str = langChoice.GetStringSelection()
	langCode: str = langSelection[langSelection.find("(") + 1 : langSelection.find(")")]
	return langCode


def getRulesFiles(
	pathToDir: str,
	processSubDirs: Callable[[str, str], list[str]] | None,
) -> list[str]:
	"""Get the rule files from a directory, optionally processing subdirectories.
		Searches for files ending with '_Rules.yaml' in the specified directory.
	If no rule files are found, attempts to find them inside a corresponding ZIP archive,
	including checking any subdirectories inside the ZIP.
		:param pathToDir: Path to the directory to search for rule files.
	:param processSubDirs: Optional callable to process subdirectories. It should take the subdirectory name
		and the language code as arguments, returning a list of rule filenames found in that subdirectory.
	:return: A list of rule file names found either directly in the directory or inside the ZIP archive.
	"""
	language: str = os.path.basename(pathToDir)
	ruleFiles: list[str] = [
		os.path.basename(file) for file in glob.glob(os.path.join(pathToDir, "*_Rules.yaml"))
	]
	for dir in os.listdir(pathToDir):
		if os.path.isdir(os.path.join(pathToDir, dir)):
			if processSubDirs:
				ruleFiles.extend(processSubDirs(dir, language))
		if len(ruleFiles) == 0:
			# look in the .zip file for the style files, including regional subdirs -- it might not have been unzipped
			try:
				zip_file: ZipFile = ZipFile(f"{pathToDir}\\{language}.zip", "r")
				for file in zip_file.namelist():
					if file.endswith("_Rules.yaml"):
						ruleFiles.append(file)
					elif zip_file.getinfo(file).is_dir() and processSubDirs:
						ruleFiles.extend(processSubDirs(dir, language))
			except Exception as e:
				log.debugWarning(f"MathCAT Dialog: didn't find zip file {zip_file}. Error: {e}")
	return ruleFiles


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
