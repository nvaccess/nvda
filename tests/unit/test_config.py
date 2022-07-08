# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022 NV Access Limited
import enum
import typing
import unittest

import configobj
import configobj.validate

from config import featureFlag
from config.featureFlag import (
	FeatureFlag,
)
from config.featureFlagEnums import (
	getAvailableEnums,
	BoolFlag,
)
from utils.displayString import (
	DisplayStringEnum
)


class Config_FeatureFlagEnums_getAvailableEnums(unittest.TestCase):

	def test_knownEnumsReturned(self):
		self.assertTrue(
			set(getAvailableEnums()).issuperset({
				("BoolFlag", BoolFlag),
			}
		))

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
			'_featureFlag(optionsEnum="BoolFlag", behaviorOfDefault="DISABLED", default="DEFAULT")'
		)

	def test_behaviorOfDefaultGetsKept(self):
		self.assertEqual(
			featureFlag._transformSpec_AddFeatureFlagDefault(
				'featureFlag(behaviorOfDefault="enabled", optionsEnum="BoolFlag")',
				behaviorOfDefault="enabled",
				optionsEnum="BoolFlag",
			),
			'_featureFlag(optionsEnum="BoolFlag", behaviorOfDefault="ENABLED", default="DEFAULT")'
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
				'featureFlag()',
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
				someOther=True
			)

	def test_optionsEnumMustBeKnown(self):
		with self.assertRaises(configobj.validate.VdtParamError):
			featureFlag._transformSpec_AddFeatureFlagDefault(
				'featureFlag(behaviorOfDefault="enabled", optionsEnum="UnknownEnumClass", someOther=True)',
				behaviorOfDefault="enabled",
				optionsEnum="UnknownEnumClass",
				someOther=True
			)


class Config_FeatureFlag_validateFeatureFlag(unittest.TestCase):

	def assertFeatureFlagState(
			self,
			flag: FeatureFlag,
			enumType: typing.Type,
			value: enum.Enum,
			behaviorOfDefault: enum.Enum,
			calculatedValue: bool
	) -> None:
		self.assertIsInstance(flag.value, enumType, msg="Wrong enum type created")
		self.assertIsInstance(value, enumType, msg="Test error: wrong enum type for checking value")
		self.assertIsInstance(
			behaviorOfDefault,
			enumType,
			msg="Test error: wrong enum type for checking behaviorOfDefault"
		)

		self.assertEqual(bool(flag), calculatedValue, msg="Calculated value for behaviour is unexpected")
		self.assertEqual(flag.value, value, msg="Flag value is unexpected")
		self.assertEqual(
			flag.behaviorOfDefault,
			behaviorOfDefault,
			msg="Flag behaviorOfDefault value is unexpected"
		)
		self.assertEqual(
			str(flag),  # conversion to string required to save to config.
			value.name.upper(),
			msg="Flag string conversion not as expected"
		)

	def test_enabled_lower(self):
		flag = featureFlag._validateConfig_featureFlag(
			"enabled",
			behaviorOfDefault="disabled",
			optionsEnum=BoolFlag.__name__
		)
		self.assertFeatureFlagState(
			flag,
			enumType=BoolFlag,
			value=BoolFlag.ENABLED,
			behaviorOfDefault=BoolFlag.DISABLED,
			calculatedValue=True
		)

	def test_enabled_upper(self):
		flag = featureFlag._validateConfig_featureFlag(
			"ENABLED",
			behaviorOfDefault="disabled",
			optionsEnum=BoolFlag.__name__
		)
		self.assertFeatureFlagState(
			flag,
			enumType=BoolFlag,
			value=BoolFlag.ENABLED,
			behaviorOfDefault=BoolFlag.DISABLED,
			calculatedValue=True
		)

	def test_disabled_lower(self):
		flag = featureFlag._validateConfig_featureFlag(
			"disabled",
			behaviorOfDefault="enabled",
			optionsEnum=BoolFlag.__name__
		)
		self.assertFeatureFlagState(
			flag,
			enumType=BoolFlag,
			value=BoolFlag.DISABLED,
			behaviorOfDefault=BoolFlag.ENABLED,
			calculatedValue=False
		)

	def test_disabled_upper(self):
		flag = featureFlag._validateConfig_featureFlag(
			"DISABLED",
			behaviorOfDefault="enabled",
			optionsEnum=BoolFlag.__name__
		)
		self.assertFeatureFlagState(
			flag,
			enumType=BoolFlag,
			value=BoolFlag.DISABLED,
			behaviorOfDefault=BoolFlag.ENABLED,
			calculatedValue=False
		)

	def test_default_lower(self):
		flag = featureFlag._validateConfig_featureFlag(
			"default",
			behaviorOfDefault="enabled",
			optionsEnum=BoolFlag.__name__
		)
		self.assertFeatureFlagState(
			flag,
			enumType=BoolFlag,
			value=BoolFlag.DEFAULT,
			behaviorOfDefault=BoolFlag.ENABLED,
			calculatedValue=True
		)

	def test_default_upper(self):
		flag = featureFlag._validateConfig_featureFlag(
			"DEFAULT",
			behaviorOfDefault="enabled",
			optionsEnum=BoolFlag.__name__
		)
		self.assertFeatureFlagState(
			flag,
			enumType=BoolFlag,
			value=BoolFlag.DEFAULT,
			behaviorOfDefault=BoolFlag.ENABLED,
			calculatedValue=True
		)

	def test_empty_raises(self):
		with self.assertRaises(configobj.validate.ValidateError):
			featureFlag._validateConfig_featureFlag(
				"",  # Given our usage of ConfigObj, this situation is unexpected.
				behaviorOfDefault="disabled",
				optionsEnum=BoolFlag.__name__
			)

	def test_None_raises(self):
		with self.assertRaises(configobj.validate.ValidateError):
			featureFlag._validateConfig_featureFlag(
				None,  # Given our usage of ConfigObj, this situation is unexpected.
				behaviorOfDefault="disabled",
				optionsEnum=BoolFlag.__name__
			)

	def test_invalid_raises(self):
		with self.assertRaises(configobj.validate.ValidateError):
			featureFlag._validateConfig_featureFlag(
				"invalid",  # must be a valid member of BoolFlag
				behaviorOfDefault="disabled",
				optionsEnum=BoolFlag.__name__
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
