# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2021-2026 NV Access Limited, Cyrille Bougot, Leonard de Ruijter

"""Unit tests for the speech module."""

import gettext
import typing
import unittest

import config
from characterProcessing import processSpeechSymbol
from controlTypes import OutputReason, Role, State
from speech import (
	_getSpellingCharAddCapNotification,
	_getSpellingSpeechAddCharMode,
	_getSpellingSpeechWithoutCharMode,
	cancelSpeech,
	pauseSpeech,
	speechCanceled,
	post_speechPaused,
)
from speech.commands import (
	BeepCommand,
	CharacterModeCommand,
	EndUtteranceCommand,
	LangChangeCommand,
	PitchCommand,
)
from speech.speech import _shouldSpeakContentFirst
from textInfos import ControlField

from .extensionPointTestHelpers import actionTester


class Test_getSpellingSpeechAddCharMode(unittest.TestCase):
	def test_symbolNamesAtStartAndEnd(self):
		# Spelling ¡hola!
		seq = (
			c
			for c in [
				"inverted exclamation point",
				EndUtteranceCommand(),
				"h",
				EndUtteranceCommand(),
				"o",
				EndUtteranceCommand(),
				"l",
				EndUtteranceCommand(),
				"a",
				EndUtteranceCommand(),
				"bang",
				EndUtteranceCommand(),
			]
		)
		expected = repr(
			[
				"inverted exclamation point",
				EndUtteranceCommand(),
				CharacterModeCommand(True),
				"h",
				EndUtteranceCommand(),
				"o",
				EndUtteranceCommand(),
				"l",
				EndUtteranceCommand(),
				"a",
				EndUtteranceCommand(),
				CharacterModeCommand(False),
				"bang",
				EndUtteranceCommand(),
			],
		)
		output = _getSpellingSpeechAddCharMode(seq)
		self.assertEqual(repr(list(output)), expected)

	def test_manySymbolNamesInARow(self):
		# Spelling a...b
		seq = (
			c
			for c in [
				"a",
				EndUtteranceCommand(),
				"dot",
				EndUtteranceCommand(),
				"dot",
				EndUtteranceCommand(),
				"dot",
				EndUtteranceCommand(),
				"b",
				EndUtteranceCommand(),
			]
		)
		expected = repr(
			[
				CharacterModeCommand(True),
				"a",
				EndUtteranceCommand(),
				CharacterModeCommand(False),
				"dot",
				EndUtteranceCommand(),
				"dot",
				EndUtteranceCommand(),
				"dot",
				EndUtteranceCommand(),
				CharacterModeCommand(True),
				"b",
				EndUtteranceCommand(),
				CharacterModeCommand(False),
			],
		)
		output = _getSpellingSpeechAddCharMode(seq)
		self.assertEqual(repr(list(output)), expected)


class Translation_Fake(gettext.NullTranslations):
	originalTranslationFunction: gettext.NullTranslations
	translationResults: typing.Dict[str, str]

	def __init__(self, originalTranslationFunction: gettext.NullTranslations):
		self.originalTranslationFunction = originalTranslationFunction
		self.translationResults = {}
		super().__init__()

	def gettext(self, msg: str) -> str:
		if msg in self.translationResults:
			return self.translationResults[msg]
		return self.originalTranslationFunction.gettext(msg)


class Test_getSpellingCharAddCapNotification(unittest.TestCase):
	translationsFake: Translation_Fake

	@classmethod
	def setUpClass(cls):
		# Initialize fake translation,
		# providing translation installed by `languageHandler` as an original one.
		# To retrieve it we just get an gettext instance bound to the `_` function.
		orig_translation = _.__self__
		cls.translationsFake = Translation_Fake(orig_translation)
		cls.translationsFake.install()

	@classmethod
	def tearDownClass(cls):
		cls.translationsFake.originalTranslationFunction.install()

	def tearDown(self) -> None:
		self.translationsFake.translationResults.clear()

	def test_noNotifications(self):
		expected = repr(
			[
				"A",
			],
		)
		output = _getSpellingCharAddCapNotification(
			speakCharAs="A",
			sayCapForCapitals=False,
			capPitchChange=0,
			beepForCapitals=False,
		)
		self.assertEqual(repr(list(output)), expected)

	def test_pitchNotifications(self):
		expected = repr(
			[
				PitchCommand(offset=30),
				"A",
				PitchCommand(),
			],
		)
		output = _getSpellingCharAddCapNotification(
			speakCharAs="A",
			sayCapForCapitals=False,
			capPitchChange=30,
			beepForCapitals=False,
		)
		self.assertEqual(repr(list(output)), expected)

	def test_beepNotifications(self):
		expected = repr(
			[
				BeepCommand(2000, 50, left=50, right=50),
				"A",
			],
		)
		output = _getSpellingCharAddCapNotification(
			speakCharAs="A",
			sayCapForCapitals=False,
			capPitchChange=0,
			beepForCapitals=True,
		)
		self.assertEqual(repr(list(output)), expected)

	def test_capNotifications(self):
		expected = repr(
			[
				"cap ",
				"A",
			],
		)
		output = _getSpellingCharAddCapNotification(
			speakCharAs="A",
			sayCapForCapitals=True,
			capPitchChange=0,
			beepForCapitals=False,
		)
		self.assertEqual(repr(list(output)), expected)

	def test_capNotificationsWithPlaceHolderBefore(self):
		self.translationsFake.translationResults["cap %s"] = "%s cap"
		expected = repr(["A", " cap"])  # for English this would be "cap A"
		output = _getSpellingCharAddCapNotification(
			speakCharAs="A",
			sayCapForCapitals=True,
			capPitchChange=0,
			beepForCapitals=False,
		)
		self.assertEqual(repr(list(output)), expected)

	def test_normalizedNotifications(self):
		expected = repr(
			[
				"A",
				" normalized",
			],
		)
		output = _getSpellingCharAddCapNotification(
			speakCharAs="A",
			sayCapForCapitals=False,
			capPitchChange=0,
			beepForCapitals=False,
			reportNormalized=True,
		)
		self.assertEqual(repr(list(output)), expected)

	def test_allNotifications(self):
		expected = repr(
			[
				PitchCommand(offset=30),
				BeepCommand(2000, 50, left=50, right=50),
				"cap ",
				"A",
				" normalized",
				PitchCommand(),
			],
		)
		output = _getSpellingCharAddCapNotification(
			speakCharAs="A",
			sayCapForCapitals=True,
			capPitchChange=30,
			beepForCapitals=True,
			reportNormalized=True,
		)
		self.assertEqual(repr(list(output)), expected)


class Test_getSpellingSpeechWithoutCharMode(unittest.TestCase):
	def setUp(self):
		config.conf["speech"]["autoLanguageSwitching"] = False

	def tearDown(self):
		# Restore default value
		config.conf["speech"]["autoLanguageSwitching"] = config.conf.getConfigValidation(
			["speech", "autoLanguageSwitching"],
		).default

	def test_simpleSpelling(self):
		expected = repr(
			[
				"a",
				EndUtteranceCommand(),
				"b",
				EndUtteranceCommand(),
				"c",
				EndUtteranceCommand(),
			],
		)
		output = _getSpellingSpeechWithoutCharMode(
			text="abc",
			locale=None,
			useCharacterDescriptions=False,
			sayCapForCapitals=False,
			capPitchChange=0,
			beepForCapitals=False,
		)
		self.assertEqual(repr(list(output)), expected)

	def test_cap(self):
		expected = repr(
			[
				PitchCommand(offset=30),
				BeepCommand(2000, 50, left=50, right=50),
				"cap ",
				"A",
				PitchCommand(),
				EndUtteranceCommand(),
			],
		)
		output = _getSpellingSpeechWithoutCharMode(
			text="A",
			locale=None,
			useCharacterDescriptions=False,
			sayCapForCapitals=True,
			capPitchChange=30,
			beepForCapitals=True,
		)
		self.assertEqual(repr(list(output)), expected)

	def test_characterMode(self):
		expected = repr(
			[
				"Alfa",
				EndUtteranceCommand(),
			],
		)
		output = _getSpellingSpeechWithoutCharMode(
			text="a",
			locale="en",
			useCharacterDescriptions=True,
			sayCapForCapitals=False,
			capPitchChange=0,
			beepForCapitals=False,
		)
		self.assertEqual(repr(list(output)), expected)

	def test_blank(self):
		expected = repr(
			[
				"blank",
			],
		)
		output = _getSpellingSpeechWithoutCharMode(
			text="",
			locale=None,
			useCharacterDescriptions=False,
			sayCapForCapitals=False,
			capPitchChange=0,
			beepForCapitals=False,
		)
		self.assertEqual(repr(list(output)), expected)

	def test_onlySpaces(self):
		expected = repr(
			[
				"space",
				EndUtteranceCommand(),
				"tab",
				EndUtteranceCommand(),
			],
		)
		output = _getSpellingSpeechWithoutCharMode(
			text=" \t",
			locale=None,
			useCharacterDescriptions=False,
			sayCapForCapitals=False,
			capPitchChange=0,
			beepForCapitals=False,
		)
		self.assertEqual(repr(list(output)), expected)

	def test_trimRightSpace(self):
		expected = repr(
			[
				"a",
				EndUtteranceCommand(),
			],
		)
		output = _getSpellingSpeechWithoutCharMode(
			text="a   ",
			locale=None,
			useCharacterDescriptions=False,
			sayCapForCapitals=False,
			capPitchChange=0,
			beepForCapitals=False,
		)
		self.assertEqual(repr(list(output)), expected)

	def test_symbol(self):
		expected = repr(
			[
				"bang",
				EndUtteranceCommand(),
			],
		)
		output = _getSpellingSpeechWithoutCharMode(
			text="!",
			locale=None,
			useCharacterDescriptions=False,
			sayCapForCapitals=False,
			capPitchChange=0,
			beepForCapitals=False,
		)
		self.assertEqual(repr(list(output)), expected)

	def test_languageDetection(self):
		config.conf["speech"]["autoLanguageSwitching"] = True
		expected = repr(
			[
				LangChangeCommand("fr_FR"),
				"a",
				EndUtteranceCommand(),
			],
		)
		output = _getSpellingSpeechWithoutCharMode(
			text="a",
			locale="fr_FR",
			useCharacterDescriptions=False,
			sayCapForCapitals=False,
			capPitchChange=0,
			beepForCapitals=False,
		)
		self.assertEqual(repr(list(output)), expected)

	def test_ligature_normalizeOff(self):
		expected = repr(
			[
				"ĳ",
				EndUtteranceCommand(),
			],
		)
		output = _getSpellingSpeechWithoutCharMode(
			text="ĳ",
			locale=None,
			useCharacterDescriptions=False,
			sayCapForCapitals=False,
			capPitchChange=0,
			beepForCapitals=False,
			unicodeNormalization=False,
			reportNormalizedForCharacterNavigation=False,
		)
		self.assertEqual(repr(list(output)), expected)

	def test_ligature_normalizeOnDontReport(self):
		expected = repr(
			[
				"i j",
				EndUtteranceCommand(),
			],
		)
		output = _getSpellingSpeechWithoutCharMode(
			text="ĳ",
			locale=None,
			useCharacterDescriptions=False,
			sayCapForCapitals=False,
			capPitchChange=0,
			beepForCapitals=False,
			unicodeNormalization=True,
			reportNormalizedForCharacterNavigation=False,
		)
		self.assertEqual(repr(list(output)), expected)

	def test_ligature_normalizeOnReport(self):
		expected = repr(
			[
				"i j",
				" normalized",
				EndUtteranceCommand(),
			],
		)
		output = _getSpellingSpeechWithoutCharMode(
			text="ĳ",
			locale=None,
			useCharacterDescriptions=False,
			sayCapForCapitals=False,
			capPitchChange=0,
			beepForCapitals=False,
			unicodeNormalization=True,
			reportNormalizedForCharacterNavigation=True,
		)
		self.assertEqual(repr(list(output)), expected)

	def test_decomposed_normalizeOff(self):
		expected = repr(
			[
				"E",
				EndUtteranceCommand(),
				"́",
				EndUtteranceCommand(),
			],
		)
		output = _getSpellingSpeechWithoutCharMode(
			text="É",
			locale=None,
			useCharacterDescriptions=False,
			sayCapForCapitals=False,
			capPitchChange=0,
			beepForCapitals=False,
			unicodeNormalization=False,
			reportNormalizedForCharacterNavigation=False,
		)
		self.assertEqual(repr(list(output)), expected)

	def test_decomposed_normalizeOnDontReport(self):
		expected = repr(
			[
				"É",
				EndUtteranceCommand(),
			],
		)
		output = _getSpellingSpeechWithoutCharMode(
			text="É",
			locale=None,
			useCharacterDescriptions=False,
			sayCapForCapitals=False,
			capPitchChange=0,
			beepForCapitals=False,
			unicodeNormalization=True,
			reportNormalizedForCharacterNavigation=False,
		)
		self.assertEqual(repr(list(output)), expected)

	def test_decomposed_normalizeOnReport(self):
		expected = repr(
			[
				"É",
				" normalized",
				EndUtteranceCommand(),
			],
		)
		output = _getSpellingSpeechWithoutCharMode(
			text="É",
			locale=None,
			useCharacterDescriptions=False,
			sayCapForCapitals=False,
			capPitchChange=0,
			beepForCapitals=False,
			unicodeNormalization=True,
			reportNormalizedForCharacterNavigation=True,
		)
		self.assertEqual(repr(list(output)), expected)

	def test_decomposedBindingToSpace(self):
		# Note, with this test string, no normalization occurs at all.
		# Yet we need to test this explicitly because splitAtCharacterBoundaries treats
		# space plus acute as one character.
		text = " ́"
		expected = repr(
			[
				"space",
				EndUtteranceCommand(),
				"́",
				EndUtteranceCommand(),
			],
		)
		output1 = _getSpellingSpeechWithoutCharMode(
			text=text,
			locale=None,
			useCharacterDescriptions=False,
			sayCapForCapitals=False,
			capPitchChange=0,
			beepForCapitals=False,
			unicodeNormalization=False,
			reportNormalizedForCharacterNavigation=False,
		)
		self.assertEqual(repr(list(output1)), expected)
		output2 = _getSpellingSpeechWithoutCharMode(
			text=text,
			locale=None,
			useCharacterDescriptions=False,
			sayCapForCapitals=False,
			capPitchChange=0,
			beepForCapitals=False,
			unicodeNormalization=True,
			reportNormalizedForCharacterNavigation=False,
		)
		self.assertEqual(repr(list(output2)), expected)
		output3 = _getSpellingSpeechWithoutCharMode(
			text=text,
			locale=None,
			useCharacterDescriptions=False,
			sayCapForCapitals=False,
			capPitchChange=0,
			beepForCapitals=False,
			unicodeNormalization=True,
			reportNormalizedForCharacterNavigation=True,
		)
		self.assertEqual(repr(list(output3)), expected)

	def test_normalizedInSymbolDict_normalizeOff(self):
		expected = repr(
			[
				"·",
				EndUtteranceCommand(),
			],
		)
		output = _getSpellingSpeechWithoutCharMode(
			text="·",
			locale="en",
			useCharacterDescriptions=False,
			sayCapForCapitals=False,
			capPitchChange=0,
			beepForCapitals=False,
			unicodeNormalization=False,
			reportNormalizedForCharacterNavigation=False,
		)
		self.assertEqual(repr(list(output)), expected)

	def test_normalizedInSymbolDict_normalizeOnDontReport(self):
		expected = repr(
			[
				processSpeechSymbol("en", "·"),
				EndUtteranceCommand(),
			],
		)
		output = _getSpellingSpeechWithoutCharMode(
			text="·",
			locale="en",
			useCharacterDescriptions=False,
			sayCapForCapitals=False,
			capPitchChange=0,
			beepForCapitals=False,
			unicodeNormalization=True,
			reportNormalizedForCharacterNavigation=False,
		)
		self.assertEqual(repr(list(output)), expected)

	def test_normalizedInSymbolDict_normalizeOnReport(self):
		expected = repr(
			[
				processSpeechSymbol("en", "·"),
				" normalized",
				EndUtteranceCommand(),
			],
		)
		output = _getSpellingSpeechWithoutCharMode(
			text="·",
			locale="en",
			useCharacterDescriptions=False,
			sayCapForCapitals=False,
			capPitchChange=0,
			beepForCapitals=False,
			unicodeNormalization=True,
			reportNormalizedForCharacterNavigation=True,
		)
		self.assertEqual(repr(list(output)), expected)


class SpeechExtensionPoints(unittest.TestCase):
	def test_speechCanceledExtensionPoint(self):
		with actionTester(
			self,
			speechCanceled,
		):
			cancelSpeech()

	def test_post_speechPausedExtensionPoint(self):
		with actionTester(self, post_speechPaused, switch=True):
			pauseSpeech(True)

		with actionTester(self, post_speechPaused, switch=False):
			pauseSpeech(False)


class _ShouldSpeakContentFirstBase(unittest.TestCase):
	"""Base class providing helper methods for _shouldSpeakContentFirst tests."""

	def _makeAttrs(
		self,
		role: Role = Role.BUTTON,
		states=None,
	) -> ControlField:
		"""Create a minimal ControlField with the given properties."""
		attrs = ControlField()
		attrs["role"] = role
		if states:
			attrs["states"] = states
		else:
			attrs["states"] = set()
		return attrs

	def _call(
		self,
		reason: OutputReason,
		role: Role = Role.BUTTON,
		presCat: str = ControlField.PRESCAT_SINGLELINE,
		tableID: str | None = None,
		states: set[State] | None = None,
	) -> bool:
		attrs = self._makeAttrs(role=role, states=states)
		return _shouldSpeakContentFirst(
			reason=reason,
			role=role,
			presCat=presCat,
			attrs=attrs,
			tableID=tableID,
			states=states or set(),
		)


class Test_shouldSpeakContentFirst_FocusAndQuickNav(_ShouldSpeakContentFirstBase):
	"""FOCUS and QUICKNAV should always speak content first for non-container roles,
	regardless of the config setting.
	"""

	def setUp(self):
		self._original = config.conf["virtualBuffers"]["controlFieldReadingOrder"]

	def tearDown(self):
		config.conf["virtualBuffers"]["controlFieldReadingOrder"] = self._original

	def test_focus_button_alwaysContentFirst(self):
		"""FOCUS on a button should always speak content first, even with controlInfoFirst config."""
		config.conf["virtualBuffers"]["controlFieldReadingOrder"] = "controlInfoFirst"
		self.assertTrue(self._call(OutputReason.FOCUS, Role.BUTTON))

	def test_focus_button_alwaysContentFirst_withContentFirstConfig(self):
		"""FOCUS on a button should speak content first even when config is contentFirst."""
		config.conf["virtualBuffers"]["controlFieldReadingOrder"] = "contentFirst"
		self.assertTrue(self._call(OutputReason.FOCUS, Role.BUTTON))

	def test_quicknav_link_alwaysContentFirst(self):
		"""QUICKNAV on a link should always speak content first, regardless of config."""
		config.conf["virtualBuffers"]["controlFieldReadingOrder"] = "controlInfoFirst"
		self.assertTrue(self._call(OutputReason.QUICKNAV, Role.LINK))

	def test_quicknav_button_alwaysContentFirst(self):
		"""QUICKNAV on a button should always speak content first, regardless of config."""
		config.conf["virtualBuffers"]["controlFieldReadingOrder"] = "controlInfoFirst"
		self.assertTrue(self._call(OutputReason.QUICKNAV, Role.BUTTON))


class Test_shouldSpeakContentFirst_CaretWithControlInfoFirstConfig(_ShouldSpeakContentFirstBase):
	"""With controlFieldReadingOrder='controlInfoFirst' (default), CARET should NOT speak content first."""

	def setUp(self):
		self._original = config.conf["virtualBuffers"]["controlFieldReadingOrder"]
		config.conf["virtualBuffers"]["controlFieldReadingOrder"] = "controlInfoFirst"

	def tearDown(self):
		config.conf["virtualBuffers"]["controlFieldReadingOrder"] = self._original

	def test_caret_button_controlInfoFirst(self):
		"""CARET on a button with controlInfoFirst config should NOT speak content first."""
		self.assertFalse(self._call(OutputReason.CARET, Role.BUTTON))

	def test_caret_link_controlInfoFirst(self):
		"""CARET on a link with controlInfoFirst config should NOT speak content first."""
		self.assertFalse(self._call(OutputReason.CARET, Role.LINK))

	def test_caret_heading_controlInfoFirst(self):
		"""CARET on a heading with controlInfoFirst config should NOT speak content first."""
		self.assertFalse(self._call(OutputReason.CARET, Role.HEADING, presCat=ControlField.PRESCAT_SINGLELINE))

	def test_sayall_button_controlInfoFirst(self):
		"""SAYALL on a button with controlInfoFirst config should NOT speak content first."""
		self.assertFalse(self._call(OutputReason.SAYALL, Role.BUTTON))


class Test_shouldSpeakContentFirst_CaretWithContentFirstConfig(_ShouldSpeakContentFirstBase):
	"""With controlFieldReadingOrder='contentFirst', CARET should speak content first."""

	def setUp(self):
		self._original = config.conf["virtualBuffers"]["controlFieldReadingOrder"]
		config.conf["virtualBuffers"]["controlFieldReadingOrder"] = "contentFirst"

	def tearDown(self):
		config.conf["virtualBuffers"]["controlFieldReadingOrder"] = self._original

	def test_caret_button_contentFirst(self):
		"""CARET on a button with contentFirst config should speak content first."""
		self.assertTrue(self._call(OutputReason.CARET, Role.BUTTON))

	def test_caret_link_contentFirst(self):
		"""CARET on a link with contentFirst config should speak content first."""
		self.assertTrue(self._call(OutputReason.CARET, Role.LINK))

	def test_caret_heading_contentFirst(self):
		"""CARET on a heading with contentFirst config should speak content first."""
		self.assertTrue(self._call(OutputReason.CARET, Role.HEADING, presCat=ControlField.PRESCAT_SINGLELINE))

	def test_sayall_button_contentFirst(self):
		"""SAYALL on a button with contentFirst config should speak content first."""
		self.assertTrue(self._call(OutputReason.SAYALL, Role.BUTTON))

	def test_sayall_link_contentFirst(self):
		"""SAYALL on a link with contentFirst config should speak content first."""
		self.assertTrue(self._call(OutputReason.SAYALL, Role.LINK))


class Test_shouldSpeakContentFirst_NeverContentFirstRoles(_ShouldSpeakContentFirstBase):
	"""Certain roles should never speak content first, regardless of config or reason."""

	def setUp(self):
		self._original = config.conf["virtualBuffers"]["controlFieldReadingOrder"]
		config.conf["virtualBuffers"]["controlFieldReadingOrder"] = "contentFirst"

	def tearDown(self):
		config.conf["virtualBuffers"]["controlFieldReadingOrder"] = self._original

	def test_editableText_neverContentFirst(self):
		"""EDITABLETEXT should never speak content first."""
		self.assertFalse(self._call(OutputReason.FOCUS, Role.EDITABLETEXT))

	def test_combobox_neverContentFirst(self):
		"""COMBOBOX should never speak content first."""
		self.assertFalse(self._call(OutputReason.FOCUS, Role.COMBOBOX))

	def test_treeview_neverContentFirst(self):
		"""TREEVIEW should never speak content first."""
		self.assertFalse(self._call(OutputReason.FOCUS, Role.TREEVIEW))

	def test_list_neverContentFirst(self):
		"""LIST should never speak content first."""
		self.assertFalse(self._call(OutputReason.FOCUS, Role.LIST))

	def test_landmark_neverContentFirst(self):
		"""LANDMARK should never speak content first."""
		self.assertFalse(self._call(OutputReason.QUICKNAV, Role.LANDMARK))

	def test_region_neverContentFirst(self):
		"""REGION should never speak content first."""
		self.assertFalse(self._call(OutputReason.QUICKNAV, Role.REGION))


class Test_shouldSpeakContentFirst_Containers(_ShouldSpeakContentFirstBase):
	"""Container controls should not speak content first, except articles."""

	def setUp(self):
		self._original = config.conf["virtualBuffers"]["controlFieldReadingOrder"]
		config.conf["virtualBuffers"]["controlFieldReadingOrder"] = "contentFirst"

	def tearDown(self):
		config.conf["virtualBuffers"]["controlFieldReadingOrder"] = self._original

	def test_container_notContentFirst(self):
		"""A generic container should not speak content first."""
		self.assertFalse(
			self._call(OutputReason.FOCUS, Role.GROUPING, presCat=ControlField.PRESCAT_CONTAINER),
		)

	def test_article_container_contentFirst(self):
		"""An article container should speak content first (#11103)."""
		self.assertTrue(
			self._call(OutputReason.QUICKNAV, Role.ARTICLE, presCat=ControlField.PRESCAT_CONTAINER),
		)


class Test_shouldSpeakContentFirst_Tables(_ShouldSpeakContentFirstBase):
	"""Controls inside tables (with a tableID) should not speak content first."""

	def setUp(self):
		self._original = config.conf["virtualBuffers"]["controlFieldReadingOrder"]
		config.conf["virtualBuffers"]["controlFieldReadingOrder"] = "contentFirst"

	def tearDown(self):
		config.conf["virtualBuffers"]["controlFieldReadingOrder"] = self._original

	def test_button_inTable_notContentFirst(self):
		"""A button inside a table should not speak content first."""
		self.assertFalse(self._call(OutputReason.FOCUS, Role.BUTTON, tableID="table1"))


class Test_shouldSpeakContentFirst_EditableState(_ShouldSpeakContentFirstBase):
	"""Controls with EDITABLE state should not speak content first."""

	def setUp(self):
		self._original = config.conf["virtualBuffers"]["controlFieldReadingOrder"]
		config.conf["virtualBuffers"]["controlFieldReadingOrder"] = "contentFirst"

	def tearDown(self):
		config.conf["virtualBuffers"]["controlFieldReadingOrder"] = self._original

	def test_editable_notContentFirst(self):
		"""A control with EDITABLE state should not speak content first."""
		self.assertFalse(
			self._call(OutputReason.FOCUS, Role.BUTTON, states={State.EDITABLE}),
		)


class Test_shouldSpeakContentFirst_UnknownReason(_ShouldSpeakContentFirstBase):
	"""An unhandled OutputReason should never speak content first."""

	def setUp(self):
		self._original = config.conf["virtualBuffers"]["controlFieldReadingOrder"]
		config.conf["virtualBuffers"]["controlFieldReadingOrder"] = "contentFirst"

	def tearDown(self):
		config.conf["virtualBuffers"]["controlFieldReadingOrder"] = self._original

	def test_onlycache_notContentFirst(self):
		"""ONLYCACHE reason should never speak content first."""
		self.assertFalse(self._call(OutputReason.ONLYCACHE, Role.BUTTON))
