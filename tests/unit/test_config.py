# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022-2025 NV Access Limited, Cyrille Bougot, Leonard de Ruijter

from collections.abc import Callable, Generator
import enum
import typing
import unittest
from unittest.mock import MagicMock, patch
import io

import configobj
import configobj.validate
from pycaw.constants import DEVICE_STATE

from config import (
	AggregatedSection,
	ConfigManager,
	featureFlag,
)
from config.featureFlag import (
	FeatureFlag,
)
from config.featureFlagEnums import (
	getAvailableEnums,
	BoolFlag,
)
from config.profileUpgradeSteps import (
	_friendlyNameToEndpointId,
	_upgradeConfigFrom_8_to_9_lineIndent,
	_upgradeConfigFrom_8_to_9_cellBorders,
	_upgradeConfigFrom_8_to_9_showMessages,
	_upgradeConfigFrom_8_to_9_tetherTo,
	upgradeConfigFrom_9_to_10,
	upgradeConfigFrom_11_to_12,
	upgradeConfigFrom_13_to_14,
	upgradeConfigFrom_16_to_17,
	upgradeConfigFrom_17_to_18,
	upgradeConfigFrom_18_to_19,
)
from config.configFlags import (
	NVDAKey,
	ShowMessages,
	ReportLineIndentation,
	ReportCellBorders,
	TetherTo,
	OutputMode,
	ReportSpellingErrors,
)
from utils.displayString import (
	DisplayStringEnum,
)
from utils.mmdevice import AudioOutputDevice


class Config_FeatureFlagEnums_getAvailableEnums(unittest.TestCase):
	def test_knownEnumsReturned(self):
		self.assertTrue(
			set(getAvailableEnums()).issuperset(
				{
					("BoolFlag", BoolFlag),
				},
			),
		)

	def test_allEnumsHaveDefault(self):
		noDefault = []
		for name, klass in getAvailableEnums():
			if not hasattr(klass, "DEFAULT"):
				noDefault.append((name, klass))
		self.assertEqual(noDefault, [])


class Config_FeatureFlag_specTransform(unittest.TestCase):
	def test_defaultGetsAdded(self):
		self.assertEqual(
			featureFlag._transformSpec_AddFeatureFlagDefault(
				'featureFlag(behaviorOfDefault="disabled", optionsEnum="BoolFlag")',
				behaviorOfDefault="disabled",
				optionsEnum="BoolFlag",
				# note: configObj treats param 'default' specially, it isn't passed through as a kwarg.
			),
			'_featureFlag(optionsEnum="BoolFlag", behaviorOfDefault="DISABLED", default="DEFAULT")',
		)

	def test_behaviorOfDefaultGetsKept(self):
		self.assertEqual(
			featureFlag._transformSpec_AddFeatureFlagDefault(
				'featureFlag(behaviorOfDefault="enabled", optionsEnum="BoolFlag")',
				behaviorOfDefault="enabled",
				optionsEnum="BoolFlag",
			),
			'_featureFlag(optionsEnum="BoolFlag", behaviorOfDefault="ENABLED", default="DEFAULT")',
		)

	def test_paramDefaultIsError(self):
		with self.assertRaises(configobj.validate.VdtParamError):
			featureFlag._transformSpec_AddFeatureFlagDefault(
				'featureFlag(behaviorOfDefault="disabled", optionsEnum="BoolFlag", default="enabled")',
				behaviorOfDefault="disabled",
				optionsEnum="BoolFlag",
				# note: configObj treats param 'default' specially, it isn't passed through as a kwarg.
			)

	def test_behaviorOfDefaultMissingIsError(self):
		with self.assertRaises(configobj.validate.VdtParamError):
			featureFlag._transformSpec_AddFeatureFlagDefault(
				'featureFlag(optionsEnum="BoolFlag")',
				optionsEnum="BoolFlag",
			)

	def test_optionsEnumMissingIsError(self):
		with self.assertRaises(configobj.validate.VdtParamError):
			featureFlag._transformSpec_AddFeatureFlagDefault(
				'featureFlag(behaviorOfDefault="enabled")',
				behaviorOfDefault="enabled",
			)

	def test_argsMissingIsError(self):
		with self.assertRaises(configobj.validate.VdtParamError):
			featureFlag._transformSpec_AddFeatureFlagDefault(
				"featureFlag()",
			)

	def test_behaviorOfDefaultTypeMustBeStr(self):
		with self.assertRaises(configobj.validate.VdtParamError):
			featureFlag._transformSpec_AddFeatureFlagDefault(
				'featureFlag(behaviorOfDefault=True, optionsEnum="BoolFlag")',
				behaviorOfDefault=True,
				optionsEnum="BoolFlag",
			)

	def test_tooManyParamsIsError(self):
		with self.assertRaises(configobj.validate.VdtParamError):
			featureFlag._transformSpec_AddFeatureFlagDefault(
				'featureFlag(behaviorOfDefault="enabled", optionsEnum="BoolFlag", someOther=True)',
				behaviorOfDefault="enabled",
				optionsEnum="BoolFlag",
				someOther=True,
			)

	def test_optionsEnumMustBeKnown(self):
		with self.assertRaises(configobj.validate.VdtParamError):
			featureFlag._transformSpec_AddFeatureFlagDefault(
				'featureFlag(behaviorOfDefault="enabled", optionsEnum="UnknownEnumClass", someOther=True)',
				behaviorOfDefault="enabled",
				optionsEnum="UnknownEnumClass",
				someOther=True,
			)


class Config_FeatureFlag_validateFeatureFlag(unittest.TestCase):
	def assertFeatureFlagState(
		self,
		flag: FeatureFlag,
		enumType: typing.Type,
		value: enum.Enum,
		behaviorOfDefault: enum.Enum,
		calculatedValue: bool,
	) -> None:
		self.assertIsInstance(flag.value, enumType, msg="Wrong enum type created")
		self.assertIsInstance(value, enumType, msg="Test error: wrong enum type for checking value")
		self.assertIsInstance(
			behaviorOfDefault,
			enumType,
			msg="Test error: wrong enum type for checking behaviorOfDefault",
		)

		self.assertEqual(bool(flag), calculatedValue, msg="Calculated value for behaviour is unexpected")
		self.assertEqual(flag.value, value, msg="Flag value is unexpected")
		self.assertEqual(
			flag.behaviorOfDefault,
			behaviorOfDefault,
			msg="Flag behaviorOfDefault value is unexpected",
		)
		self.assertEqual(
			str(flag),  # conversion to string required to save to config.
			value.name.upper(),
			msg="Flag string conversion not as expected",
		)

	def test_enabled_lower(self):
		flag = featureFlag._validateConfig_featureFlag(
			"enabled",
			behaviorOfDefault="disabled",
			optionsEnum=BoolFlag.__name__,
		)
		self.assertFeatureFlagState(
			flag,
			enumType=BoolFlag,
			value=BoolFlag.ENABLED,
			behaviorOfDefault=BoolFlag.DISABLED,
			calculatedValue=True,
		)

	def test_enabled_upper(self):
		flag = featureFlag._validateConfig_featureFlag(
			"ENABLED",
			behaviorOfDefault="disabled",
			optionsEnum=BoolFlag.__name__,
		)
		self.assertFeatureFlagState(
			flag,
			enumType=BoolFlag,
			value=BoolFlag.ENABLED,
			behaviorOfDefault=BoolFlag.DISABLED,
			calculatedValue=True,
		)

	def test_disabled_lower(self):
		flag = featureFlag._validateConfig_featureFlag(
			"disabled",
			behaviorOfDefault="enabled",
			optionsEnum=BoolFlag.__name__,
		)
		self.assertFeatureFlagState(
			flag,
			enumType=BoolFlag,
			value=BoolFlag.DISABLED,
			behaviorOfDefault=BoolFlag.ENABLED,
			calculatedValue=False,
		)

	def test_disabled_upper(self):
		flag = featureFlag._validateConfig_featureFlag(
			"DISABLED",
			behaviorOfDefault="enabled",
			optionsEnum=BoolFlag.__name__,
		)
		self.assertFeatureFlagState(
			flag,
			enumType=BoolFlag,
			value=BoolFlag.DISABLED,
			behaviorOfDefault=BoolFlag.ENABLED,
			calculatedValue=False,
		)

	def test_default_lower(self):
		flag = featureFlag._validateConfig_featureFlag(
			"default",
			behaviorOfDefault="enabled",
			optionsEnum=BoolFlag.__name__,
		)
		self.assertFeatureFlagState(
			flag,
			enumType=BoolFlag,
			value=BoolFlag.DEFAULT,
			behaviorOfDefault=BoolFlag.ENABLED,
			calculatedValue=True,
		)

	def test_default_upper(self):
		flag = featureFlag._validateConfig_featureFlag(
			"DEFAULT",
			behaviorOfDefault="enabled",
			optionsEnum=BoolFlag.__name__,
		)
		self.assertFeatureFlagState(
			flag,
			enumType=BoolFlag,
			value=BoolFlag.DEFAULT,
			behaviorOfDefault=BoolFlag.ENABLED,
			calculatedValue=True,
		)

	def test_empty_raises(self):
		with self.assertRaises(configobj.validate.ValidateError):
			featureFlag._validateConfig_featureFlag(
				"",  # Given our usage of ConfigObj, this situation is unexpected.
				behaviorOfDefault="disabled",
				optionsEnum=BoolFlag.__name__,
			)

	def test_None_raises(self):
		with self.assertRaises(configobj.validate.ValidateError):
			featureFlag._validateConfig_featureFlag(
				None,  # Given our usage of ConfigObj, this situation is unexpected.
				behaviorOfDefault="disabled",
				optionsEnum=BoolFlag.__name__,
			)

	def test_invalid_raises(self):
		with self.assertRaises(configobj.validate.ValidateError):
			featureFlag._validateConfig_featureFlag(
				"invalid",  # must be a valid member of BoolFlag
				behaviorOfDefault="disabled",
				optionsEnum=BoolFlag.__name__,
			)


class Config_FeatureFlag_with_BoolFlag(unittest.TestCase):
	def test_Enabled_DisabledByDefault(self):
		f = FeatureFlag(value=BoolFlag.ENABLED, behaviorOfDefault=BoolFlag.DISABLED)
		self.assertEqual(True, bool(f))
		self.assertEqual(BoolFlag.ENABLED, f.calculated())
		self.assertTrue(f == BoolFlag.ENABLED)  # overloaded operator ==
		self.assertEqual(f.enumClassType, BoolFlag)

	def test_Enabled_EnabledByDefault(self):
		f = FeatureFlag(value=BoolFlag.ENABLED, behaviorOfDefault=BoolFlag.ENABLED)
		self.assertEqual(True, bool(f))
		self.assertEqual(BoolFlag.ENABLED, f.calculated())
		self.assertTrue(f == BoolFlag.ENABLED)  # overloaded operator ==
		self.assertEqual(f.enumClassType, BoolFlag)

	def test_Disabled_DisabledByDefault(self):
		f = FeatureFlag(value=BoolFlag.DISABLED, behaviorOfDefault=BoolFlag.DISABLED)
		self.assertEqual(False, bool(f))
		self.assertEqual(BoolFlag.DISABLED, f.calculated())
		self.assertTrue(f == BoolFlag.DISABLED)  # overloaded operator ==
		self.assertEqual(f.enumClassType, BoolFlag)

	def test_Disabled_EnabledByDefault(self):
		f = FeatureFlag(value=BoolFlag.DISABLED, behaviorOfDefault=BoolFlag.ENABLED)
		self.assertEqual(False, bool(f))
		self.assertEqual(BoolFlag.DISABLED, f.calculated())
		self.assertTrue(f == BoolFlag.DISABLED)  # overloaded operator ==
		self.assertEqual(f.enumClassType, BoolFlag)

	def test_Default_EnabledByDefault(self):
		f = FeatureFlag(value=BoolFlag.DEFAULT, behaviorOfDefault=BoolFlag.ENABLED)
		self.assertEqual(True, bool(f))
		self.assertEqual(BoolFlag.ENABLED, f.calculated())
		self.assertTrue(f == BoolFlag.ENABLED)  # overloaded operator ==
		self.assertEqual(f.enumClassType, BoolFlag)

	def test_Default_DisabledByDefault(self):
		f = FeatureFlag(value=BoolFlag.DEFAULT, behaviorOfDefault=BoolFlag.DISABLED)
		self.assertEqual(False, bool(f))
		self.assertEqual(BoolFlag.DISABLED, f.calculated())
		self.assertTrue(f == BoolFlag.DISABLED)  # overloaded operator ==
		self.assertEqual(f.enumClassType, BoolFlag)

	def test_DefaultBehaviorOfDefault_Raises(self):
		with self.assertRaises(AssertionError):
			FeatureFlag(value=BoolFlag.DEFAULT, behaviorOfDefault=BoolFlag.DEFAULT)


class CustomEnum(DisplayStringEnum):
	DEFAULT = enum.auto()
	ALWAYS = enum.auto()
	WHEN_REQUIRED = enum.auto()
	NEVER = enum.auto()

	def _displayStringLabels(self) -> typing.Dict[enum.Enum, str]:
		return {}


class Config_FeatureFlag_with_CustomEnum(unittest.TestCase):
	def test_CustomEnum_boolRaises(self):
		f = FeatureFlag(value=CustomEnum.ALWAYS, behaviorOfDefault=CustomEnum.NEVER)
		with self.assertRaises(NotImplementedError):
			bool(f)

	def test_CustomEnum_equalsOp(self):
		always = FeatureFlag(value=CustomEnum.ALWAYS, behaviorOfDefault=CustomEnum.NEVER)

		alsoAlways = FeatureFlag(value=CustomEnum.ALWAYS, behaviorOfDefault=CustomEnum.NEVER)
		whenRequired = FeatureFlag(value=CustomEnum.WHEN_REQUIRED, behaviorOfDefault=CustomEnum.NEVER)
		defaultAlways = FeatureFlag(value=CustomEnum.DEFAULT, behaviorOfDefault=CustomEnum.ALWAYS)
		defaultNever = FeatureFlag(value=CustomEnum.DEFAULT, behaviorOfDefault=CustomEnum.NEVER)

		self.assertFalse(always.isDefault())
		self.assertTrue(defaultAlways.isDefault())

		# overloaded operator == accepts enum or featureFlag
		self.assertTrue(always == CustomEnum.ALWAYS)
		self.assertTrue(always == alsoAlways)
		self.assertTrue(whenRequired == CustomEnum.WHEN_REQUIRED)
		self.assertTrue(whenRequired != alsoAlways)
		self.assertTrue(defaultAlways == CustomEnum.ALWAYS)
		self.assertTrue(defaultAlways == always)
		self.assertTrue(defaultNever == CustomEnum.NEVER)


def _loadProfile(configString: str) -> configobj.ConfigObj:
	fn = io.StringIO(configString)
	profile = configobj.ConfigObj(fn, indent_type="\t", encoding="UTF-8", file_error=False)
	# Python converts \r\n to \n when reading files in Windows, so ConfigObj can't determine
	# the true line ending.
	profile.newlines = "\r\n"
	return profile


class Config_profileUpgradeSteps__upgradeConfigFrom_8_to_9_lineIndent(unittest.TestCase):
	def test_DefaultProfile_Unmodified(self):
		"""Document formatting Line indentation reporting option not modified in default profile."""

		configString = "[documentFormatting]"
		profile = _loadProfile(configString)
		_upgradeConfigFrom_8_to_9_lineIndent(profile)
		with self.assertRaises(KeyError):
			profile["documentFormatting"]["reportLineIndentation"]
		with self.assertRaises(KeyError):
			profile["documentFormatting"]["reportLineIndentationWithTones"]

	def test_DefaultProfile_LineIndentationRestoredToOff(self):
		"""Document formatting Line indentation reporting option explicitely restored to off in default profile
		after having previously selected speech and tones.
		"""

		configString = """
[documentFormatting]
	reportLineIndentation = False
	reportLineIndentationWithTones = False
"""
		profile = _loadProfile(configString)
		_upgradeConfigFrom_8_to_9_lineIndent(profile)
		self.assertEqual(
			profile["documentFormatting"]["reportLineIndentation"],
			ReportLineIndentation.OFF.value,
		)
		with self.assertRaises(KeyError):
			profile["documentFormatting"]["reportLineIndentationWithTones"]

	def test_DefaultProfile_LineIndentationSpeech(self):
		"""Document formatting Line indentation reporting option set to Speech in default profile."""

		configString = """
[documentFormatting]
	reportLineIndentation = True
"""
		profile = _loadProfile(configString)
		_upgradeConfigFrom_8_to_9_lineIndent(profile)
		self.assertEqual(
			profile["documentFormatting"]["reportLineIndentation"],
			ReportLineIndentation.SPEECH.value,
		)
		with self.assertRaises(KeyError):
			profile["documentFormatting"]["reportLineIndentationWithTones"]

	def test_DefaultProfile_LineIndentationTones(self):
		"""Document formatting Line indentation reporting option set to tones in default profile."""

		configString = """
[documentFormatting]
	reportLineIndentationWithTones = True
"""
		profile = _loadProfile(configString)
		_upgradeConfigFrom_8_to_9_lineIndent(profile)
		self.assertEqual(
			profile["documentFormatting"]["reportLineIndentation"],
			ReportLineIndentation.TONES.value,
		)
		with self.assertRaises(KeyError):
			profile["documentFormatting"]["reportLineIndentationWithTones"]

	def test_DefaultProfile_LineIndentationSpeechAndTones(self):
		"""Document formatting Line indentation reporting option set to Speech and tones in default profile."""

		configString = """
[documentFormatting]
	reportLineIndentation = True
	reportLineIndentationWithTones = True
"""
		profile = _loadProfile(configString)
		_upgradeConfigFrom_8_to_9_lineIndent(profile)
		self.assertEqual(
			profile["documentFormatting"]["reportLineIndentation"],
			ReportLineIndentation.SPEECH_AND_TONES.value,
		)
		with self.assertRaises(KeyError):
			profile["documentFormatting"]["reportLineIndentationWithTones"]


class Config_profileUpgradeSteps_upgradeConfigFrom_8_to_9_cellBorders(unittest.TestCase):
	def _checkOldKeysRemoved(self, profile: configobj.ConfigObj) -> None:
		with self.assertRaises(KeyError):
			profile["documentFormatting"]["reportBorderStyle"]
		with self.assertRaises(KeyError):
			profile["documentFormatting"]["reportBorderColor"]

	def test_DefaultProfile_Unmodified(self):
		"""Document formatting Cell borders option not modified in default profile."""

		configString = "[documentFormatting]"
		profile = _loadProfile(configString)
		_upgradeConfigFrom_8_to_9_cellBorders(profile)
		with self.assertRaises(KeyError):
			profile["documentFormatting"]["reportCellBorders"]
		self._checkOldKeysRemoved(profile)

	def test_DefaultProfile_CellBordersStyle(self):
		"""Document formatting Cell borders option set on style in default profile."""

		configString = """
[documentFormatting]
	reportBorderStyle = True
"""
		profile = _loadProfile(configString)
		_upgradeConfigFrom_8_to_9_cellBorders(profile)
		self.assertEqual(profile["documentFormatting"]["reportCellBorders"], ReportCellBorders.STYLE.value)
		self._checkOldKeysRemoved(profile)

	def test_DefaultProfile_CellBordersColorAndStyle(self):
		"""Document formatting Cell borders option set on Both color and style in default profile."""

		configString = """
[documentFormatting]
	reportBorderStyle = True
	reportBorderColor = True
"""
		profile = _loadProfile(configString)
		_upgradeConfigFrom_8_to_9_cellBorders(profile)
		self.assertEqual(
			profile["documentFormatting"]["reportCellBorders"],
			ReportCellBorders.COLOR_AND_STYLE.value,
		)
		self._checkOldKeysRemoved(profile)

	def test_DefaultProfile_CellBordersRestoreOff(self):
		"""Document formatting Cell borders option explicitely restored to Off after having been set
		on Both color and style in default profile.
		"""

		configString = """
[documentFormatting]
	reportBorderStyle = False
	reportBorderColor = False
"""
		profile = _loadProfile(configString)
		_upgradeConfigFrom_8_to_9_cellBorders(profile)
		self.assertEqual(profile["documentFormatting"]["reportCellBorders"], ReportCellBorders.OFF.value)
		self._checkOldKeysRemoved(profile)

	def test_ManualProfile_CellBordersColorAndStyle(self):
		"""Document formatting Cell borders option set on:
		- Both color and style in manually activated profile
		- Style in default profile
		when manually activated profile is activated on top of default profile.
		Thus the configuration for manually activated profile only specifies the reportBorderColor key
		since reportBorderStyle is the same as default profile.
		"""

		# Note that this config is not possible in default profile
		configString = """
[documentFormatting]
	reportBorderColor = True
"""
		profile = _loadProfile(configString)
		_upgradeConfigFrom_8_to_9_cellBorders(profile)
		self.assertEqual(
			profile["documentFormatting"]["reportCellBorders"],
			ReportCellBorders.COLOR_AND_STYLE.value,
		)
		self._checkOldKeysRemoved(profile)


class Config_profileUpgradeSteps_upgradeConfigFrom_8_to_9_showMessages(unittest.TestCase):
	def _checkOldKeyRemoved(self, profile: configobj.ConfigObj) -> None:
		with self.assertRaises(KeyError):
			profile["braille"]["noMessageTimeout"]

	def test_DefaultProfile_Unmodified(self):
		"""Braille Show message and Message timeout option not modified in default profile."""

		configString = "[braille]"
		profile = _loadProfile(configString)
		_upgradeConfigFrom_8_to_9_showMessages(profile)
		self._checkOldKeyRemoved(profile)
		with self.assertRaises(KeyError):
			profile["braille"]["showMessages"]
		with self.assertRaises(KeyError):
			profile["braille"]["messageTimeout"]

	def test_DefaultProfile_ShowMessageDisabled(self):
		"""Braille Show message option set to Disabled in default profile."""

		configString = """
[braille]
	messageTimeout = 0
"""
		profile = _loadProfile(configString)
		_upgradeConfigFrom_8_to_9_showMessages(profile)
		self._checkOldKeyRemoved(profile)
		self.assertEqual(profile["braille"]["showMessages"], ShowMessages.DISABLED.value)
		with self.assertRaises(KeyError):
			profile["braille"]["messageTimeout"]

	def test_DefaultProfile_ShowMessageIndefinitely(self):
		"""Braille Show message option set to Show indefinitely in default profile."""

		configString = """
[braille]
	noMessageTimeout = True
"""
		profile = _loadProfile(configString)
		_upgradeConfigFrom_8_to_9_showMessages(profile)
		self._checkOldKeyRemoved(profile)
		self.assertEqual(profile["braille"]["showMessages"], ShowMessages.SHOW_INDEFINITELY.value)
		with self.assertRaises(KeyError):
			profile["braille"]["messageTimeout"]

	def test_DefaultProfile_ShowMessageRestoreUseTimeout(self):
		"""Braille Show message option explicitely restored to Use timeout in default profile
		after having been set to Show indefinitely.
		"""

		configString = """
[braille]
	noMessageTimeout = False
"""
		profile = _loadProfile(configString)
		_upgradeConfigFrom_8_to_9_showMessages(profile)
		self._checkOldKeyRemoved(profile)
		self.assertEqual(profile["braille"]["showMessages"], ShowMessages.USE_TIMEOUT.value)
		with self.assertRaises(KeyError):
			profile["braille"]["messageTimeout"]

	def test_DefaultProfile_UseTimeout1s(self):
		"""Braille Message timeout option set to 1 second in default profile."""

		configString = """
[braille]
	messageTimeout = 1
"""
		profile = _loadProfile(configString)
		_upgradeConfigFrom_8_to_9_showMessages(profile)
		self._checkOldKeyRemoved(profile)
		with self.assertRaises(KeyError):
			profile["braille"]["showMessages"]
		self.assertEqual(profile["braille"]["messageTimeout"], "1")

	def test_DefaultProfile_RestoreUseTimeout4s(self):
		"""Braille Message timeout option explicitely restored to 4 second (default value) in default profile
		after having been set to a different value.
		"""

		configString = """
[braille]
	messageTimeout = 4
"""
		profile = _loadProfile(configString)
		_upgradeConfigFrom_8_to_9_showMessages(profile)
		self._checkOldKeyRemoved(profile)
		with self.assertRaises(KeyError):
			profile["braille"]["showMessages"]
		self.assertEqual(profile["braille"]["messageTimeout"], "4")


class Config_profileUpgradeSteps_upgradeConfigFrom_8_to_9_tetherTo(unittest.TestCase):
	def _checkOldKeyRemoved(self, profile: configobj.ConfigObj) -> None:
		with self.assertRaises(KeyError):
			profile["braille"]["autoTether"]

	def test_DefaultProfile_Unmodified(self):
		"""Braille Tether Braille option not modified in default profile."""

		configString = "[braille]"
		profile = _loadProfile(configString)
		_upgradeConfigFrom_8_to_9_tetherTo(profile)
		with self.assertRaises(KeyError):
			profile["braille"]["autoTether"]
		with self.assertRaises(KeyError):
			profile["braille"]["tetherTo"]

	def test_DefaultProfile_TetherToFocus(self):
		"""Braille Tether Braille option set on Focus in default profile."""

		configString = """
[braille]
	autoTether = False
"""
		profile = _loadProfile(configString)
		_upgradeConfigFrom_8_to_9_tetherTo(profile)
		self._checkOldKeyRemoved(profile)
		self.assertEqual(profile["braille"]["tetherTo"], TetherTo.FOCUS.value)

	def test_DefaultProfile_TetherToReview(self):
		"""Braille Tether Braille option set on Review in default profile."""

		configString = """
[braille]
	tetherTo = review
	autoTether = False
"""
		profile = _loadProfile(configString)
		_upgradeConfigFrom_8_to_9_tetherTo(profile)
		self._checkOldKeyRemoved(profile)
		self.assertEqual(profile["braille"]["tetherTo"], TetherTo.REVIEW.value)

	def test_DefaultProfile_TetherToRestoreAuto(self):
		"""Braille Tether Braille option explicitely restored on Automatic in default profile,
		after having been set on Review."""

		configString = """
[braille]
	tetherTo = focus
	autoTether = True
"""
		profile = _loadProfile(configString)
		_upgradeConfigFrom_8_to_9_tetherTo(profile)
		self._checkOldKeyRemoved(profile)
		self.assertEqual(profile["braille"]["tetherTo"], TetherTo.AUTO.value)

	def test_ManualProfile_TetherToReview(self):
		"""Braille Tether Braille option set on:
		- Review in manually activated profile
		- Focus in default profile
		when manually activated profile is activated on top of default profile.
		Thus the configuration for manually activated profile only specifies tetherTo key
		since autoTether is the same as default profile.
		"""

		# Note that this config is not possible in default profile
		configString = """
[braille]
	tetherTo = review
"""
		profile = _loadProfile(configString)
		_upgradeConfigFrom_8_to_9_tetherTo(profile)
		self._checkOldKeyRemoved(profile)
		self.assertEqual(profile["braille"]["tetherTo"], TetherTo.REVIEW.value)


class Config_profileUpgradeSteps_upgradeConfigFrom_9_to_10(unittest.TestCase):
	def _checkOldKeyRemoved(self, profile: configobj.ConfigObj) -> None:
		with self.assertRaises(KeyError):
			profile["keyboard"]["useCapsLockAsNVDAModifierKey"]
		with self.assertRaises(KeyError):
			profile["keyboard"]["useNumpadInsertAsNVDAModifierKey"]
		with self.assertRaises(KeyError):
			profile["keyboard"]["useExtendedInsertAsNVDAModifierKey"]

	def test_DefaultProfile_Unmodified(self):
		"""Keyboard settings, NVDA Modifiers Keys option not modified in default profile."""

		configString = "[keyboard]"
		profile = _loadProfile(configString)
		upgradeConfigFrom_9_to_10(profile)
		self._checkOldKeyRemoved(profile)
		with self.assertRaises(KeyError):
			profile["keyboard"]["NVDAModifierKeys"]

	def test_DefaultProfile_setCapsLockTrue(self):
		"""Keyboard settings, Caps Lock enabled as NVDA Modifier key in default profile; other keys remain enabled
		(default).
		"""

		configString = """
[keyboard]
	useCapsLockAsNVDAModifierKey = True
"""
		profile = _loadProfile(configString)
		upgradeConfigFrom_9_to_10(profile)
		self._checkOldKeyRemoved(profile)
		self.assertEqual(
			profile["keyboard"]["NVDAModifierKeys"],
			NVDAKey.CAPS_LOCK.value | NVDAKey.NUMPAD_INSERT.value | NVDAKey.EXTENDED_INSERT.value,
		)

	def test_DefaultProfile_setCapsLockTrueOtherFalse(self):
		"""Keyboard settings, Caps Lock enabled as NVDA Modifier key in default profile; other keys disabled."""

		configString = """
[keyboard]
	useCapsLockAsNVDAModifierKey = True
	useNumpadInsertAsNVDAModifierKey = False
	useExtendedInsertAsNVDAModifierKey = False
"""
		profile = _loadProfile(configString)
		upgradeConfigFrom_9_to_10(profile)
		self._checkOldKeyRemoved(profile)
		self.assertEqual(
			profile["keyboard"]["NVDAModifierKeys"],
			NVDAKey.CAPS_LOCK.value,
		)

	def test_ManualProfile_setNumpadInsertFalseExtendedInsertFalse(self):
		"""Keyboard settings, NVDA Modifier keys option set on:
		- numpad insert and extended insert explicitely disabled in the manual profile, while caps lock was still
		enabled in default profile
		- caps lock explicitely disabled in the default profile afterwards

		Thus the configuration for manually activated profile only explicitely disables numpad insert and
		extended insert since caps lock enabled was inherited from default profile.

		See issue #14527 for full description.
		"""

		# Note that this config is not possible in default profile using only NVDA GUI options, i.e. not using
		# Python console or manually editing nvda.ini.
		configString = """
[keyboard]
	useNumpadInsertAsNVDAModifierKey = False
	useExtendedInsertAsNVDAModifierKey = False
"""
		profile = _loadProfile(configString)
		upgradeConfigFrom_9_to_10(profile)
		self._checkOldKeyRemoved(profile)
		# Check that Caps Lock is restored to avoid having no NVDA modifier key at all.
		self.assertEqual(
			profile["keyboard"]["NVDAModifierKeys"],
			NVDAKey.CAPS_LOCK.value,
		)


class Config_upgradeProfileSteps_upgradeProfileFrom_11_to_12(unittest.TestCase):
	def test_DefaultProfile_Unmodified(self):
		"""reportFontAttributes unmodified."""
		configString = "[documentFormatting]"
		profile = _loadProfile(configString)
		upgradeConfigFrom_11_to_12(profile)
		with self.assertRaises(KeyError):
			profile["documentFormatting"]["reportFontAttributes"]
		with self.assertRaises(KeyError):
			profile["documentFormatting"]["fontAttributeReporting"]

	def test_defaultProfile_reportFontAttributes_false(self):
		"""reportFontAttributes set to False."""
		configString = """
		[documentFormatting]
		reportFontAttributes = False
		"""
		profile = _loadProfile(configString)
		upgradeConfigFrom_11_to_12(profile)
		self.assertEqual(profile["documentFormatting"]["reportFontAttributes"], "False")
		self.assertEqual(profile["documentFormatting"]["fontAttributeReporting"], OutputMode.OFF.value)

	def test_defaultProfile_reportFontAttributes_true(self):
		"""reportFontAttributes set to True."""
		configString = """
		[documentFormatting]
		reportFontAttributes = True
		"""
		profile = _loadProfile(configString)
		upgradeConfigFrom_11_to_12(profile)
		self.assertEqual(profile["documentFormatting"]["reportFontAttributes"], "True")
		self.assertEqual(
			profile["documentFormatting"]["fontAttributeReporting"],
			OutputMode.SPEECH_AND_BRAILLE.value,
		)

	def test_defaultProfile_reportFontAttributes_invalid(self):
		"""reportFontAttributes set to a non-boolean value."""
		configString = """
		[documentFormatting]
		reportFontAttributes = notABool
		"""
		profile = _loadProfile(configString)
		upgradeConfigFrom_11_to_12(profile)
		self.assertEqual(profile["documentFormatting"]["reportFontAttributes"], "notABool")
		with self.assertRaises(KeyError):
			profile["documentFormatting"]["fontAttributeReporting"]


class Config_AggregatedSection_getitem(unittest.TestCase):
	def setUp(self):
		manager = MagicMock(ConfigManager())
		spec = MagicMock(configobj.ConfigObj())
		self.testSection = AggregatedSection(
			manager=manager,
			path=(),
			spec=spec,
			profiles=[],
		)

	def test_cached(self):
		self.testSection._cache["foo"] = "bar"
		self.assertEqual(self.testSection["foo"], "bar")

	def test_KeyError(self):
		self.testSection._cache["foo"] = KeyError
		with self.assertRaises(KeyError):
			self.testSection["foo"]


class Config_AggregatedSection_setitem(unittest.TestCase):
	def setUp(self):
		manager = MagicMock(ConfigManager())
		spec = MagicMock(configobj.ConfigObj())
		profile = MagicMock(configobj.ConfigObj())
		self.testSection = AggregatedSection(
			manager=manager,
			path=(),
			spec=spec,
			profiles=[profile],
		)

	def test_update_str(self):
		self.testSection._cache["foo"] = "bar"
		self.testSection["foo"] = "zoo"
		self.assertEqual(self.testSection["foo"], "zoo")

	def test_update_FeatureFlag_defaultValue_fromValueOfDefault(self):
		"""
		Documents bug raised in #14133,
		where the config did not update when changing from the value of the default to the default value
		"""
		valueOfDefaultFlag = FeatureFlag(value=CustomEnum.NEVER, behaviorOfDefault=CustomEnum.NEVER)
		defaultFlag = FeatureFlag(value=CustomEnum.DEFAULT, behaviorOfDefault=CustomEnum.NEVER)
		self.testSection["foo"] = defaultFlag
		self.assertIs(self.testSection["foo"], defaultFlag)
		self.testSection["foo"] = valueOfDefaultFlag
		self.assertIs(self.testSection["foo"], valueOfDefaultFlag)


class Config_AggregatedSection_pollution(unittest.TestCase):
	"""Ensure that config profiles don't get polluted with overridden values equal to the base config"""

	def setUp(self):
		manager = ConfigManager()
		spec = configobj.ConfigObj({"someBool": "boolean(default=True)"})
		self.baseConfig = configobj.ConfigObj({"someBool": True})
		self.profile = configobj.ConfigObj()
		self.testSection = AggregatedSection(
			manager=manager,
			path=(),
			spec=spec,
			profiles=[self.baseConfig, self.profile],
		)

	def test_updateToSameValue(self):
		self.testSection["someBool"] = True
		# Since we set someBool to its existing value, don't touch the profile.
		self.assertEqual(self.profile, {})

	def test_updateToDifferentValue(self):
		self.testSection["someBool"] = False
		# Since we set someBool to a different value, update the profile.
		self.assertEqual(self.profile, {"someBool": False})


_DevicesT: typing.TypeAlias = dict[DEVICE_STATE, list[AudioOutputDevice]]


def getOutputDevicesFactory(
	devices: _DevicesT,
) -> Callable[[DEVICE_STATE], Generator[AudioOutputDevice]]:
	"""Create a callable that can be used to patch utils.mmdevice.getOutputDevices."""

	def getOutputDevices(stateMask: DEVICE_STATE, **kw) -> Generator[AudioOutputDevice]:
		yield from devices.get(stateMask, [])

	return getOutputDevices


class Config_ProfileUpgradeSteps_FriendlyNameToEndpointId(unittest.TestCase):
	DEFAULT_DEVICES: _DevicesT = {
		DEVICE_STATE.ACTIVE: [AudioOutputDevice("id1", "Device 1")],
		DEVICE_STATE.UNPLUGGED: [AudioOutputDevice("id2", "Device 2")],
		DEVICE_STATE.DISABLED: [AudioOutputDevice("id3", "Device 3")],
		DEVICE_STATE.NOTPRESENT: [AudioOutputDevice("id4", "Device 4")],
	}

	def test_noDuplicates(self):
		"""Test that mapping from a friendly name to an endpoint ID works as expected when there are no duplicate friendly names."""
		devices = self.DEFAULT_DEVICES
		for devicesState, devicesInState in devices.items():
			for device in devicesInState:
				with self.subTest(id=device.id, FriendlyName=device.friendlyName, state=devicesState):
					self.performTest(*device, devices)

	def test_orderOfPrecedence(self):
		"""Test that, when there are devices with duplicate names in different states, the one with the preferred state is returned."""
		FRIENDLY_NAME = "Device friendly name"
		devices: _DevicesT = {
			DEVICE_STATE.ACTIVE: [AudioOutputDevice("idA", FRIENDLY_NAME)],
			DEVICE_STATE.DISABLED: [AudioOutputDevice("idD", FRIENDLY_NAME)],
			DEVICE_STATE.NOTPRESENT: [AudioOutputDevice("idN", FRIENDLY_NAME)],
			DEVICE_STATE.UNPLUGGED: [AudioOutputDevice("idU", FRIENDLY_NAME)],
		}
		with self.subTest("Friendly name is active"):
			self.performTest(*devices[DEVICE_STATE.ACTIVE][0], devices)
		devices[DEVICE_STATE.ACTIVE].pop()
		with self.subTest("Friendly name is unplugged"):
			self.performTest(*devices[DEVICE_STATE.UNPLUGGED][0], devices)
		devices[DEVICE_STATE.UNPLUGGED].pop()
		with self.subTest("Friendly name is disabled"):
			self.performTest(*devices[DEVICE_STATE.DISABLED][0], devices)
		devices[DEVICE_STATE.DISABLED].pop()
		with self.subTest("Friendly name is notpresent"):
			self.performTest(*devices[DEVICE_STATE.NOTPRESENT][0], devices)
		devices[DEVICE_STATE.NOTPRESENT].pop()

	def test_nonexistant(self):
		"""Test that attempting a match for a friendly name that no device has returns None."""
		devices = self.DEFAULT_DEVICES
		self.performTest(friendlyName="Nonexistant", expectedId=None, devices=devices)

	def test_noDevices(self):
		"""Test that attempting a match for a friendly name that no device has returns None."""
		devices: _DevicesT = {}
		self.performTest(friendlyName="Anything", expectedId=None, devices=devices)

	def performTest(self, expectedId: str | None, friendlyName: str, devices: _DevicesT):
		"""Patch utils.mmdevice.getOutputDevices to return what we tell it, then test that friendlyNameToEndpointId returns the correct ID given a friendly name.
		The odd order of arguments is so you can directly unpack an AudioOutputDevice.
		"""
		with patch(
			"utils.mmdevice.getOutputDevices",
			autospec=True,
			side_effect=getOutputDevicesFactory(devices),
		):
			self.assertEqual(_friendlyNameToEndpointId(friendlyName), expectedId)


class Config_upgradeProfileSteps_upgradeProfileFrom_13_to_14(unittest.TestCase):
	def setUp(self):
		devices: _DevicesT = {
			DEVICE_STATE.ACTIVE: [AudioOutputDevice("id", "Friendly name")],
		}
		self._getOutputDevicesPatcher = patch(
			"utils.mmdevice.getOutputDevices",
			autospec=True,
			side_effect=getOutputDevicesFactory(devices),
		)
		self._getOutputDevicesPatcher.start()
		super().setUp()

	def tearDown(self):
		self._getOutputDevicesPatcher.stop()
		super().tearDown()

	def test_outputDeviceNotSet(self):
		"""Test that upgrading with no output device set works."""
		configString = ""
		profile = _loadProfile(configString)
		upgradeConfigFrom_13_to_14(profile)
		with self.assertRaises(KeyError):
			profile["speech"]["outputDevice"]
		with self.assertRaises(KeyError):
			profile["audio"]["outputDevice"]

	def test_outputDeviceFound(self):
		"""Test that upgrading the profile correctly creates the new key and value."""
		configString = """
		[speech]
			outputDevice=Friendly name
		"""
		profile = _loadProfile(configString)
		upgradeConfigFrom_13_to_14(profile)
		self.assertEqual(profile["audio"]["outputDevice"], "id")
		with self.assertRaises(KeyError):
			profile["speech"]["outputDevice"]

	def test_outputDeviceNotFound(self):
		"""Test that upgrading the profile with an unidentifiable device doesn't create a new entry."""
		configString = """
		[speech]
			outputDevice=Nonexistant device
		"""
		profile = _loadProfile(configString)
		upgradeConfigFrom_13_to_14(profile)
		with self.assertRaises(KeyError):
			profile["speech"]["outputDevice"]
		with self.assertRaises(KeyError):
			profile["audio"]["outputDevice"]


class Config_upgradeProfileSteps_upgradeProfileFrom_16_to_17(unittest.TestCase):
	def test_rename(self):
		v15Config = """
[remote]
	[[connections]]
		last_connected = nvdaremote:6837, 192.168.0.123:456
	[[controlserver]]
		autoconnect = True
		self_hosted = True
		connection_type = 0
		host = remote.example.com:1234
		port = 31415
		key = superSecurePassw0rd
	[[seen_motds]]
		nvdaremote.com:6837=7B502C3A1F48C8609AE212CDFB639DEE39673F5E
	[[trusted_certs]]
		sketchyServer.example.com:6837 = 64EC88CA00B268E5BA1A35678A1B5316D212F4F366B2477232534A8AECA37F3C
"""
		expectedV16Config = {
			"remote": {
				"connections": {
					"lastConnected": ["nvdaremote:6837", "192.168.0.123:456"],
				},
				"controlServer": {
					"autoconnect": "True",
					"selfHosted": "True",
					"connectionMode": "0",
					"host": "remote.example.com:1234",
					"port": "31415",
					"key": "superSecurePassw0rd",
				},
				"seenMOTDs": {
					"nvdaremote.com:6837": "7B502C3A1F48C8609AE212CDFB639DEE39673F5E",
				},
				"trustedCertificates": {
					"sketchyServer.example.com:6837": "64EC88CA00B268E5BA1A35678A1B5316D212F4F366B2477232534A8AECA37F3C",
				},
			},
		}
		conf = configobj.ConfigObj(io.StringIO(v15Config))
		upgradeConfigFrom_16_to_17(conf)
		actualV16Config = conf.dict()
		self.maxDiff = None
		self.assertEqual(expectedV16Config, actualV16Config)


class Config_upgradeProfileSteps_upgradeProfileFrom_17_to_18(unittest.TestCase):
	def test_noBrailleSection(self):
		"""Test upgrading when there is no braille section - should create the structure and add dotPad."""
		configString = ""
		profile = _loadProfile(configString)
		upgradeConfigFrom_17_to_18(profile)
		self.assertEqual(profile["braille"]["auto"]["excludedDisplays"], ["dotPad"])

	def test_noAutoSection(self):
		"""Test upgrading when braille section exists but no auto section - should create auto section and add dotPad."""
		configString = """
[braille]
	display = auto
"""
		profile = _loadProfile(configString)
		upgradeConfigFrom_17_to_18(profile)
		self.assertEqual(profile["braille"]["auto"]["excludedDisplays"], ["dotPad"])

	def test_noExcludedDisplaysKey(self):
		"""Test upgrading when auto section exists but no excludedDisplays key - should create key and add dotPad."""
		configString = """
[braille]
	display = auto
	[[auto]]
"""
		profile = _loadProfile(configString)
		upgradeConfigFrom_17_to_18(profile)
		self.assertEqual(profile["braille"]["auto"]["excludedDisplays"], ["dotPad"])

	def test_emptyExcludedDisplays(self):
		"""Test upgrading when excludedDisplays exists but is empty - should add dotPad."""
		configString = """
[braille]
	display = auto
	[[auto]]
		excludedDisplays =
"""
		profile = _loadProfile(configString)
		# Manually set to empty list to simulate the state after config parsing
		profile["braille"]["auto"]["excludedDisplays"] = []
		upgradeConfigFrom_17_to_18(profile)
		self.assertEqual(profile["braille"]["auto"]["excludedDisplays"], ["dotPad"])

	def test_existingExcludedDisplays(self):
		"""Test upgrading when excludedDisplays has other entries - should add dotPad to the list."""
		configString = """
[braille]
	display = auto
	[[auto]]
		excludedDisplays = hidBrailleStandard,
"""
		profile = _loadProfile(configString)
		upgradeConfigFrom_17_to_18(profile)
		expected = ["hidBrailleStandard", "dotPad"]
		self.assertEqual(profile["braille"]["auto"]["excludedDisplays"], expected)

	def test_dotPadAlreadyExcluded(self):
		"""Test upgrading when dotPad is already in excludedDisplays - should not add it again."""
		configString = """
[braille]
	display = auto
	[[auto]]
		excludedDisplays = dotPad, hidBrailleStandard
"""
		profile = _loadProfile(configString)
		upgradeConfigFrom_17_to_18(profile)
		expected = ["dotPad", "hidBrailleStandard"]
		self.assertEqual(profile["braille"]["auto"]["excludedDisplays"], expected)


class Config_upgradeProfileSteps_upgradeProfileFrom_18_to_19(unittest.TestCase):
	def test_DefaultProfile_Unmodified(self):
		"""reportSpellingErrors unmodified."""
		configString = "[documentFormatting]"
		profile = _loadProfile(configString)
		upgradeConfigFrom_18_to_19(profile)
		with self.assertRaises(KeyError):
			profile["documentFormatting"]["reportSpellingErrors"]
		with self.assertRaises(KeyError):
			profile["documentFormatting"]["reportSpellingErrors2"]

	def test_defaultProfile_reportSpellingErrors_false(self):
		"""reportSpellingErrors set to False."""
		configString = """
		[documentFormatting]
		reportSpellingErrors = False
		"""
		profile = _loadProfile(configString)
		upgradeConfigFrom_18_to_19(profile)
		with self.assertRaises(KeyError):
			profile["documentFormatting"]["reportSpellingErrors"]
		self.assertEqual(
			profile["documentFormatting"]["reportSpellingErrors2"],
			ReportSpellingErrors.OFF.value,
		)

	def test_defaultProfile_reportSpellingErrors_true(self):
		"""reportSpellingErrors set to True."""
		configString = """
		[documentFormatting]
		reportSpellingErrors = True
		"""
		profile = _loadProfile(configString)
		upgradeConfigFrom_18_to_19(profile)
		with self.assertRaises(KeyError):
			profile["documentFormatting"]["reportSpellingErrors"]
		self.assertEqual(
			profile["documentFormatting"]["reportSpellingErrors2"],
			ReportSpellingErrors.SPEECH.value,
		)

	def test_defaultProfile_reportSpellingErrors_invalid(self):
		"""reportSpellingErrors set to a non-boolean value."""
		configString = """
		[documentFormatting]
		reportSpellingErrors = notABool
		"""
		profile = _loadProfile(configString)
		upgradeConfigFrom_18_to_19(profile)
		self.assertEqual(profile["documentFormatting"]["reportSpellingErrors"], "notABool")
		with self.assertRaises(KeyError):
			profile["documentFormatting"]["reportSpellingErrors2"]
