# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2025 NV Access Limited, Neil Soiffer, Ryan McCleary
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from enum import Enum
import os

import config
import yaml
from logHandler import log
from NVDAState import WritePaths

import libmathcat_py as libmathcat
from .rulesUtils import getRulesFiles


class SpeechOptions(Enum):
	DecimalSeparator = ("Auto", ".", ",", "Custom")
	Impairment = ("LearningDisability", "Blindness", "LowVision")
	Verbosity = ("Terse", "Medium", "Verbose")
	SubjectArea = ("General",)
	Chemistry = ("SpellOut", "Off")


class NavigationOptions(Enum):
	NavMode = ("Enhanced", "Simple", "Character")
	NavVerbosity = ("Terse", "Medium", "Verbose")
	CopyAs = ("MathML", "LaTeX", "ASCIIMath", "Speech")


class BrailleOptions(Enum):
	BrailleNavHighlight = ("Off", "FirstChar", "EndPoints", "All")


# two constants to scale "PauseFactor"
# these work out so that a slider that goes [0,14] has value ~100 at 7 and ~1000 at 14
class PauseFactor(Enum):
	SCALE: float = 9.5
	LOG_BASE: float = 1.4


def pathToUserPreferencesFolder() -> str:
	"""Returns the path to the folder where user preferences are stored."""
	# the user preferences file is stored at: C:\Users\<user-name>AppData\Roaming\MathCAT\prefs.yaml
	return os.path.join(os.path.expandvars("%APPDATA%"), "MathCAT")


def pathToUserPreferences() -> str:
	"""Returns the full path to the user preferences file."""
	# the user preferences file is stored at: C:\Users\<user-name>AppData\Roaming\MathCAT\prefs.yaml
	return os.path.join(pathToUserPreferencesFolder(), "prefs.yaml")


def pathToBrailleFolder() -> str:
	r"""Returns the full path to the Braille rules folder.
		The Braille rules are stored in:
	MathCAT\Rules\Braille, relative to the location of this file.

	:return: Absolute path to the Braille folder as a string.
	"""
	return os.path.join(
		WritePaths.mathCATDir,
		"Rules",
		"Braille",
	)


def getBrailleCodes() -> list[str]:
	"""Initializes and populates the braille code choice control with available braille codes.

	Scans the braille codes folder for valid directories containing rules files, and adds them
	to the braille code dropdown in the dialog.
	"""
	brailleFolderPath: str = pathToBrailleFolder()
	resultBrailleCodes = []
	for brailleCode in os.listdir(brailleFolderPath):
		pathToBrailleCode: str = os.path.join(brailleFolderPath, brailleCode)
		if os.path.isdir(pathToBrailleCode):
			if len(getRulesFiles(pathToBrailleCode, None)) > 0:
				resultBrailleCodes.append(brailleCode)
	return resultBrailleCodes


def toNVDAConfigKey(key: str) -> str:
	"""Converts a key for MathCAT's preferences (UpperCamelCase) to a
	key for NVDA's configobj-based configuration (lowerCamelCase).
	Some special cases, such as 'LaTex' and 'UEB' are handled separately.
	"""
	# First, we handle special cases separately.
	if key == "UEB" or key == "LaTeX" or key == "":
		return key
	else:
		return key[0].lower() + key[1:]


type PreferencesDict = dict[str, dict[str, int | str | bool]]


class MathCATUserPreferences:
	_prefs: PreferencesDict

	@staticmethod
	def defaults() -> PreferencesDict:
		def defaultValue(path: tuple[str]) -> str | int | bool:
			return config.conf.getConfigValidation(path).default

		return {
			"Speech": {
				"Impairment": defaultValue(("speech", "impairment")),
				"Language": defaultValue(("speech", "language")),
				"Verbosity": defaultValue(("speech", "verbosity")),
				"MathRate": defaultValue(("speech", "mathRate")),
				"PauseFactor": defaultValue(("speech", "pauseFactor")),
				"SpeechSound": defaultValue(("speech", "speechSound")),
				"SpeechStyle": defaultValue(("speech", "speechStyle")),
				"SubjectArea": defaultValue(("speech", "subjectArea")),
				"Chemistry": defaultValue(("speech", "chemistry")),
			},
			"Navigation": {
				"NavMode": defaultValue(("navigation", "navMode")),
				"ResetNavMode": defaultValue(("navigation", "resetNavMode")),
				"Overview": defaultValue(("navigation", "overview")),
				"ResetOverview": defaultValue(("navigation", "resetOverview")),
				"NavVerbosity": defaultValue(("navigation", "navVerbosity")),
				"AutoZoomOut": defaultValue(("navigation", "autoZoomOut")),
				"CopyAs": defaultValue(("navigation", "copyAs")),
			},
			"Braille": {
				"BrailleNavHighlight": defaultValue(("braille", "brailleNavHighlight")),
				"BrailleCode": defaultValue(("braille", "brailleCode")),
			},
		}

	def __init__(
		self,
		prefs: PreferencesDict,
	) -> None:
		self._prefs = prefs
		self._validateAll()

	@staticmethod
	def fromNVDAConfig() -> "MathCATUserPreferences":
		prefs: PreferencesDict = MathCATUserPreferences.defaults()
		mathConf = config.conf["math"]
		for key1 in prefs:
			for key2 in prefs[key1]:
				convertedKey1 = toNVDAConfigKey(key1)
				convertedKey2 = toNVDAConfigKey(key2)
				try:
					prefs[key1][key2] = mathConf[convertedKey1][convertedKey2]
				except Exception:
					log.warning(
						f"Could not access math.{convertedKey1}.{convertedKey2} configuration; using MathCAT default.",
					)
		return MathCATUserPreferences(prefs)

	def save(self) -> None:
		"""Writes the current user preferences to a file and updates special settings.

		Sets the language preference through the native library, ensures the preferences
		folder exists, and saves the preferences to disk.
		"""
		# Language is special because it is set elsewhere by SetPreference which overrides the user_prefs -- so set it here

		try:
			libmathcat.SetPreference("Language", self._prefs["Speech"]["Language"])
		except Exception as e:
			log.exception(
				f'Error in trying to set MathCAT "Language" preference to "{self._prefs["Speech"]["Language"]}": {e}',
			)
		if not os.path.exists(pathToUserPreferencesFolder()):
			# create a folder for the user preferences
			os.mkdir(pathToUserPreferencesFolder())
		with open(pathToUserPreferences(), "w", encoding="utf-8") as f:
			# write values to the user preferences file, NOT the default
			yaml.dump(self._prefs, stream=f, allow_unicode=True)

	def _validateAll(self):
		"""Validates all user preferences, ensuring each is present and valid.

		If a preference is missing or invalid, it is reset to its default value.
		Validation covers speech, navigation, and braille settings.
		"""
		#  Speech.Impairment
		# Default value: Blindness
		# Valid values: LearningDisability, LowVision, Blindness
		self._validate(
			"Speech",
			"Impairment",
			["LearningDisability", "LowVision", "Blindness"],
			"Blindness",
		)
		# Speech.Language
		# Default value: en
		# Valid values: any known language code and sub-code -- could be en-uk, etc
		self._validate("Speech", "Language", [], "en")
		# Speech.Verbosity
		# Default value: Medium
		# Valid values: Terse, Medium, Verbose
		self._validate("Speech", "Verbosity", ["Terse", "Medium", "Verbose"], "Medium")
		# Speech.MathRate
		# Default value: 100
		# Valid values: integers in the interval [0, 200]; change from text speech rate (%)
		self._validateInt("Speech", "MathRate", [0, 200], 100)
		# Speech.PauseFactor: 100
		# Default value: 100
		# Valid values: integers in the interval [0, 1000]
		self._validateInt("Speech", "PauseFactor", [0, 1000], 100)
		# Speech.SpeechSound
		# Default value: None
		# Valid values: None, Beep -- make a sound when starting / ending math speech
		self._validate("Speech", "SpeechSound", ["None", "Beep"], "None")
		# Speech.SpeechStyle
		# Default value: ClearSpeak
		# Valid values: Any known speech style (falls back to ClearSpeak)
		self._validate("Speech", "SpeechStyle", [], "ClearSpeak")
		# Speech.SubjectArea
		# Default value: General
		# Not yet implemented in MathCAT
		self._validate("Speech", "SubjectArea", [], "General")
		# Speech.Chemistry
		# Default value: SpellOut
		# Valid values: SpellOut (H 2 O), AsCompound (Water), Off (H sub 2 O)
		self._validate("Speech", "Chemistry", ["SpellOut", "Off"], "SpellOut")

		# Navigation:

		# Navigation.NavMode
		# Default value: Enhanced
		# Valid values: Enhanced, Simple, Character
		self._validate("Navigation", "NavMode", ["Enhanced", "Simple", "Character"], "Enhanced")
		# Navigation.ResetNavMode
		# Default value: false
		# Valid values: true, false; remember previous value and use it
		self._validate("Navigation", "ResetNavMode", [False, True], False)
		# Navigation.Overview
		# Default value: false
		# Valid values: true, false; speak the expression or give a description/overview
		self._validate("Navigation", "Overview", [False, True], False)
		# Navigation.ResetOverview
		# Default value: true
		# Valid values: true, false; remember previous value and use it
		self._validate("Navigation", "ResetOverview", [False, True], True)
		# Navigation.NavVerbosity
		# Default value: Medium
		# Valid values: Terse, Medium, Full (words to say for nav command)
		self._validate("Navigation", "NavVerbosity", ["Terse", "Medium", "Full"], "Medium")
		# Navigation.AutoZoomOut
		# Default value: true
		# Valid values: true, false; Auto zoom out of 2D exprs (use shift-arrow to force zoom out if unchecked)
		self._validate("Navigation", "AutoZoomOut", [False, True], True)
		# Navigation.CopyAs
		# Default value: MathML
		# Valid values: MathML, LaTeX, ASCIIMath, Speech
		self._validate("Navigation", "CopyAs", ["MathML", "LaTeX", "ASCIIMath", "Speech"], "MathML")

		# Braille

		# Braille.BrailleNavHighlight
		# Default value: EndPoints
		# Valid values: Highlight with dots 7 & 8 the current nav node -- values are Off, FirstChar, EndPoints, All
		self._validate(
			"Braille",
			"BrailleNavHighlight",
			["Off", "FirstChar", "EndPoints", "All"],
			"EndPoints",
		)
		# Braille.BrailleCode
		# Default value: "Nemeth"
		# Valid values: Any supported braille code (currently Nemeth, UEB, CMU, Vietnam)
		self._validate("Braille", "BrailleCode", [], "Nemeth")

	def _validate(
		self,
		key1: str,
		key2: str,
		validValues: list[str | bool],
		defaultValue: str | bool,
	) -> None:
		"""Validates that a preference value is in a list of valid options or non-empty if no list is given.

		If the value is missing or invalid, sets it to the default.

		:param key1: The first-level key in the preferences dictionary.
		:param key2: The second-level key in the preferences dictionary.
		:param validValues: A list of valid values; if empty, any non-empty value is valid.
		:param defaultValue: The default value to set if validation fails.
		"""
		try:
			if validValues == []:
				# any value is valid
				if self._prefs[key1][key2] != "":
					return

			else:
				# any value in the list is valid
				if self._prefs[key1][key2] in validValues:
					return
		except Exception as e:
			log.exception(f"MathCAT: An exception occurred in validate: {e}")
			# the preferences entry does not exist
		if key1 not in self._prefs:
			self._prefs[key1] = {key2: defaultValue}
		else:
			self._prefs[key1][key2] = defaultValue

	def _validateInt(
		self,
		key1: str,
		key2: str,
		validValues: list[int],
		defaultValue: int,
	) -> None:
		"""Validates that an integer preference is within a specified range.

		If the value is missing or out of bounds, sets it to the default.

		:param key1: The first-level key in the preferences dictionary.
		:param key2: The second-level key in the preferences dictionary.
		:param validValues: A list with two integers [min, max] representing valid bounds.
		:param defaultValue: The default value to set if validation fails.
		"""
		try:
			# any value between lower and upper bounds is valid
			if (
				int(self._prefs[key1][key2]) >= validValues[0]
				and int(self._prefs[key1][key2]) <= validValues[1]
			):
				return
		except Exception as e:
			log.exception(f"MathCAT: An exception occurred in validateInt: {e}")
		# the preferences entry does not exist
		if key1 not in self._prefs:
			self._prefs[key1] = {key2: defaultValue}
		else:
			self._prefs[key1][key2] = defaultValue
