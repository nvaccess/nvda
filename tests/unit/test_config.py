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


class Config_FeatureFlagEnums_getAvailableEnums(unittest.TestCase):

	def test_knownEnumsReturned(self):
		self.assertEqual(
			dict(getAvailableEnums()),
			{
				"BoolFlag": BoolFlag,
			}
		)


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
