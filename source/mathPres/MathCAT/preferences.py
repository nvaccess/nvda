# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2025 NV Access Limited, Neil Soiffer, Ryan McCleary
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from enum import Enum
import os

import config
import languageHandler
import yaml
from logHandler import log
from NVDAState import ReadPaths, WritePaths
from utils.displayString import DisplayStringStrEnum

import libmathcat_py as libmathcat
from .rulesUtils import getRulesFiles


class ImpairmentOption(DisplayStringStrEnum):
	LEARNING_DISABILITY = "LearningDisability"
	BLINDNESS = "Blindness"
	LOW_VISION = "LowVision"

	@property
	def _displayStringLabels(self) -> dict["ImpairmentOption", str]:
		return {
			# Translators: Learning disabilities includes dyslexia and ADHD
			# category of impairment that MathCAT supports: people with learning disabilities
			self.LEARNING_DISABILITY: pgettext("math", "Learning disabilities"),
			# Translators: category of impairment that MathCAT supports: people who are blind
			self.BLINDNESS: pgettext("math", "Blindness"),
			# Translators: category of impairment that MathCAT supports: people who have low vision
			self.LOW_VISION: pgettext("math", "Low vision"),
		}


class DecimalSeparatorOption(DisplayStringStrEnum):
	AUTO = "Auto"
	DOT = "."
	COMMA = ","
	CUSTOM = "Custom"

	@property
	def _displayStringLabels(self) -> dict["DecimalSeparatorOption", str]:
		return {
			# Translators: options for decimal separator -- "Auto" = automatically pick the choice based on the language
			self.AUTO: pgettext("math", "Automatic"),
			# options for decimal separator -- use "."  (and use ", " for block separators)
			self.DOT: ".",
			# options for decimal separator -- use ","  (and use ". " for block separators)
			self.COMMA: ",",
			# Translators: options for decimal separator -- "Custom" = user sets it
			#   Currently there is no UI for how it is done yet, but eventually there will be a dialog that pops up to set it
			self.CUSTOM: pgettext("math", "Custom"),
		}


class VerbosityOption(DisplayStringStrEnum):
	TERSE = "Terse"
	MEDIUM = "Medium"
	VERBOSE = "Verbose"

	@property
	def _displayStringLabels(self) -> dict["VerbosityOption", str]:
		return {
			# Translators: options for speech verbosity -- "terse" = use less words
			self.TERSE: pgettext("math", "Terse"),
			# Translators: options for speech verbosity -- "medium" = try to be neither too terse nor too verbose
			self.MEDIUM: pgettext("math", "Medium"),
			# Translators: options for speech verbosity -- "verbose" = use more words
			self.VERBOSE: pgettext("math", "Verbose"),
		}


class ChemistryOption(DisplayStringStrEnum):
	SPELL_OUT = "SpellOut"
	OFF = "Off"

	@property
	def _displayStringLabels(self) -> dict["ChemistryOption", str]:
		return {
			# Translators: values for chemistry options with example speech in parenthesis
			self.SPELL_OUT: pgettext("math", "Spell it out (H 2 O)"),
			# Translators: values for chemistry options with example speech in parenthesis (never interpret as chemistry)
			self.OFF: pgettext("math", "Off (H sub 2 O)"),
		}


class NavModeOption(DisplayStringStrEnum):
	ENHANCED = "Enhanced"
	SIMPLE = "Simple"
	CHARACTER = "Character"

	@property
	def _displayStringLabels(self) -> dict["NavModeOption", str]:
		return {
			# Translators: names of different modes of navigation. "Enhanced" mode understands math structure
			self.ENHANCED: pgettext("math", "Enhanced"),
			# Translators: "Simple" walks by character expect for things like fractions, roots, and scripts
			self.SIMPLE: pgettext("math", "Simple"),
			# Translators: "Character" moves around by character, automatically moving into fractions, etc
			self.CHARACTER: pgettext("math", "Character"),
		}


class NavVerbosityOption(DisplayStringStrEnum):
	TERSE = "Terse"
	MEDIUM = "Medium"
	VERBOSE = "Verbose"

	@property
	def _displayStringLabels(self) -> dict["NavVerbosityOption", str]:
		return {
			# Translators: options for navigation verbosity -- "terse" = use less words
			self.TERSE: pgettext("math", "Terse"),
			# Translators: options for navigation verbosity -- "medium" = try to be nether too terse nor too verbose words
			self.MEDIUM: pgettext("math", "Medium"),
			# Translators: options for navigation verbosity -- "verbose" = use more words
			self.VERBOSE: pgettext("math", "Verbose"),
		}


class CopyAsOption(DisplayStringStrEnum):
	MATHML = "MathML"
	LATEX = "LaTeX"
	ASCIIMATH = "ASCIIMath"
	SPEECH = "Speech"

	@property
	def _displayStringLabels(self) -> dict["CopyAsOption", str]:
		return {
			# Translators: options for Copy expression to clipboard as -- "MathML"
			self.MATHML: pgettext("math", "MathML"),
			# Translators: options for Copy math to clipboard as -- "LaTeX"
			self.LATEX: pgettext("math", "LaTeX"),
			# Translators: options for Copy math to clipboard as -- "ASCIIMath"
			self.ASCIIMATH: pgettext("math", "ASCIIMath"),
			# Translators: options for Copy math to clipboard as -- speech text
			self.SPEECH: pgettext("math", "Speech"),
		}


class BrailleNavHighlightOption(DisplayStringStrEnum):
	OFF = "Off"
	FIRST_CHAR = "FirstChar"
	ENDPOINTS = "EndPoints"
	ALL = "All"

	@property
	def _displayStringLabels(self) -> dict["BrailleNavHighlightOption", str]:
		return {
			# Translators: Math option for using dots 7 and 8: don't highlight
			self.OFF: pgettext("math", "Off"),
			# Translators: Math option for using dots 7 and 8:
			# only the first character of the current navigation node uses dots 7 & 8
			self.FIRST_CHAR: pgettext("math", "First character"),
			# Translators: Math option for using dots 7 and 8:
			# only the first and last character of the current navigation node uses dots 7 & 8
			self.ENDPOINTS: pgettext("math", "Endpoints"),
			# Translators: Math option for using dots 7 and 8:
			# all the characters for the current navigation node use dots 7 & 8
			self.ALL: pgettext("math", "All"),
		}


class SpeechStyleOption(DisplayStringStrEnum):
	CLEAR_SPEAK = "ClearSpeak"
	SIMPLE_SPEAK = "SimpleSpeak"
	LITERAL_SPEAK = "LiteralSpeak"

	@property
	def _displayStringLabels(self) -> dict["SpeechStyleOption", str]:
		return {
			# Translators: ClearSpeak is a speech style developed by ETS for use on high-stakes tests such as the SAT
			self.CLEAR_SPEAK: pgettext("math", "ClearSpeak"),
			# Translators: SimpleSpeak is a speech style that tries to minimize speech by speaking simple expressions without bracketing words
			self.SIMPLE_SPEAK: pgettext("math", "SimpleSpeak"),
			# Translators: LiteralSpeak is a speech style with no language-specific rules that reads math character by character
			self.LITERAL_SPEAK: pgettext("math", "LiteralSpeak"),
		}


# two constants to scale "PauseFactor"
# these work out so that a slider that goes [0,14] has value ~100 at 7 and ~1000 at 14
class PauseFactor(Enum):
	SCALE: float = 9.5
	LOG_BASE: float = 1.4


def pathToUserPreferences() -> str:
	"""Returns the full path to the user preferences file."""
	return os.path.join(WritePaths.configDir, "mathcat.yaml")


def pathToBrailleFolder() -> str:
	r"""Returns the full path to the Braille rules folder.
		The Braille rules are stored in:
	MathCAT\Rules\Braille, relative to the location of this file.

	:return: Absolute path to the Braille folder as a string.
	"""
	return os.path.join(
		ReadPaths.mathCATDir,
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


def getAutoBrailleCode(
	availableCodes: list[str] | None = None,
	languageCode: str | None = None,
) -> str:
	"""
	Determine the automatic MathCAT Braille code to use based on the current
	or provided NVDA language.
	"""
	if not availableCodes:
		availableCodes = getBrailleCodes()
	if languageCode is None:
		languageCode = languageHandler.getLanguage()

	# de, nb, and nn should probably use Marburg when implemented upstream
	languagesToBrailleCodes: dict[str, str] = {
		"af": "UEB",
		"an": "CMU",
		"ca": "CMU",
		"da": "LaTeX",
		"de": "LaTeX",
		"en": "UEB",
		"es": "CMU",
		"fi": "ASCIIMath-fi",
		"ga": "UEB",
		"gl": "CMU",
		"mn": "UEB",
		"nb": "LaTeX",
		"nn": "LaTeX",
		"pt": "CMU",
		"ro": "UEB",
		"sv": "Swedish",
		"vi": "Vietnam",
	}

	res = languagesToBrailleCodes.get(languageCode.split("_")[0])
	if res and res in availableCodes:
		return res
	return "ASCIIMath"


def setEffectiveBrailleCode() -> None:
	"""
	Apply the effective Braille code to MathCAT at runtime, resolving auto
	if needed.
	"""
	try:
		brailleCodePref = config.conf["math"]["braille"]["brailleCode"]
		effectiveCode = getAutoBrailleCode() if brailleCodePref == "Auto" else brailleCodePref
		libmathcat.SetPreference("BrailleCode", effectiveCode)
	except Exception as e:
		log.debugWarning(
			f"MathCAT: failed to set BrailleCode preference: {e}",
			exc_info=True,
		)


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


def getSpeechStyleChoicesWithTranslations(languageCode: str) -> list[str]:
	"""Get speech style choices with translations for known styles.

	This function gets the available speech styles from MathCAT's localization system
	and provides translations for the core speech styles (ClearSpeak, SimpleSpeak, LiteralSpeak)
	while keeping language-specific styles untranslated.

	:param languageCode: The language code to get speech styles for
	:return: List of speech style display strings (some translated, some original)
	"""
	from . import localization

	rawStyles = localization.getSpeechStyles(languageCode)
	displayChoices = []

	knownStyleValues = [style.value for style in SpeechStyleOption]

	for style in rawStyles:
		if style in knownStyleValues:
			# Get translated version for known styles
			enumOption = SpeechStyleOption(style)
			displayChoices.append(enumOption.displayString)
		else:
			# Unknown style, use original name as fallback
			displayChoices.append(style)

	return displayChoices


def getSpeechStyleConfigValue(displayString: str) -> str:
	"""
	Convert a display string back to its config value.

	:param displayString: The display string from the UI selection
	:return: The config value to save for this speech style
	"""
	# Try to find matching enum first
	for style in SpeechStyleOption:
		if style.displayString == displayString:
			return style.value
	return displayString


class MathCATUserPreferences:
	_prefs: PreferencesDict

	@staticmethod
	def defaults() -> PreferencesDict:
		def defaultValue(path: tuple[str]) -> str | int | bool:
			return config.conf.getConfigValidation(("math",) + path).default

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

		setEffectiveBrailleCode()

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
			[option.value for option in ImpairmentOption],
			ImpairmentOption.BLINDNESS.value,
		)
		# Speech.Language
		# Default value: en
		# Valid values: any known language code and sub-code -- could be en-uk, etc
		self._validate("Speech", "Language", [], "en")
		# Speech.Verbosity
		# Default value: Medium
		# Valid values: Terse, Medium, Verbose
		self._validate(
			"Speech",
			"Verbosity",
			[option.value for option in VerbosityOption],
			VerbosityOption.MEDIUM.value,
		)
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
		self._validate(
			"Speech",
			"Chemistry",
			[option.value for option in ChemistryOption],
			ChemistryOption.SPELL_OUT.value,
		)

		# Navigation:

		# Navigation.NavMode
		# Default value: Enhanced
		# Valid values: Enhanced, Simple, Character
		self._validate(
			"Navigation",
			"NavMode",
			[option.value for option in NavModeOption],
			NavModeOption.ENHANCED.value,
		)
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
		# Valid values: Terse, Medium, Verbose (words to say for nav command)
		self._validate(
			"Navigation",
			"NavVerbosity",
			[option.value for option in NavVerbosityOption],
			NavVerbosityOption.MEDIUM.value,
		)
		# Navigation.AutoZoomOut
		# Default value: true
		# Valid values: true, false; Auto zoom out of 2D exprs (use shift-arrow to force zoom out if unchecked)
		self._validate("Navigation", "AutoZoomOut", [False, True], True)
		# Navigation.CopyAs
		# Default value: MathML
		# Valid values: MathML, LaTeX, ASCIIMath, Speech
		self._validate(
			"Navigation",
			"CopyAs",
			[option.value for option in CopyAsOption],
			CopyAsOption.MATHML.value,
		)

		# Braille

		# Braille.BrailleNavHighlight
		# Default value: EndPoints
		# Valid values: Highlight with dots 7 & 8 the current nav node -- values are Off, FirstChar, EndPoints, All
		self._validate(
			"Braille",
			"BrailleNavHighlight",
			[option.value for option in BrailleNavHighlightOption],
			BrailleNavHighlightOption.ENDPOINTS.value,
		)
		# Braille.BrailleCode
		# Default value: Auto
		# Valid values: Any supported braille code (for example Nemeth, UEB, CMU, Vietnam) or Auto
		self._validate("Braille", "BrailleCode", [], "Auto")

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
