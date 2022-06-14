import unittest

import configobj
import configobj.validate

from config import featureFlag
from config.featureFlag import (
	FeatureFlag,
	FeatureFlagValues,
)


class Config_FeatureFlag_specTransform(unittest.TestCase):

	def test_defaultGetsAdded(self):
		self.assertEqual(
			featureFlag._transformSpec_AddFeatureFlagDefault(
				'featureFlag(behaviorOfDefault="disabled")',
				behaviorOfDefault="disabled"
			),
			'featureFlag(behaviorOfDefault="disabled", default="default")'
		)

	def test_behaviorOfDefaultGetsKept(self):
		self.assertEqual(
			featureFlag._transformSpec_AddFeatureFlagDefault(
				'featureFlag(behaviorOfDefault="enabled")',
				behaviorOfDefault="enabled"
			),
			'featureFlag(behaviorOfDefault="enabled", default="default")'
		)

	def test_paramDefaultIsError(self):
		with self.assertRaises(configobj.validate.VdtParamError):
			featureFlag._transformSpec_AddFeatureFlagDefault(
				'featureFlag(behaviorOfDefault="disabled", default="enabled")',
				behaviorOfDefault="disabled"
			)

	def test_behaviorOfDefaultMissingIsError(self):
		with self.assertRaises(configobj.validate.VdtParamError):
			featureFlag._transformSpec_AddFeatureFlagDefault(
				'featureFlag()',
			)

	def test_behaviorOfDefaultTypeMustBeStr(self):
		with self.assertRaises(configobj.validate.VdtParamError):
			featureFlag._transformSpec_AddFeatureFlagDefault(
				'featureFlag(behaviorOfDefault=True)',
				behaviorOfDefault=True
			)

	def test_tooManyParamsIsError(self):
		with self.assertRaises(configobj.validate.VdtParamError):
			featureFlag._transformSpec_AddFeatureFlagDefault(
				'featureFlag(behaviorOfDefault="enabled", someOther=True)',
				behaviorOfDefault=True,
				someOther=True
			)


class Config_FeatureFlag_validateFeatureFlag(unittest.TestCase):

	def assertFeatureFlagState(
			self,
			flag: FeatureFlag,
			value: FeatureFlagValues,
			behaviorOfDefault: FeatureFlagValues,
			calculatedValue: bool
	):
		self.assertEqual(bool(flag), calculatedValue)
		self.assertEqual(flag.value, value)
		self.assertEqual(flag.behaviorOfDefault, behaviorOfDefault)
		self.assertEqual(
			str(flag),  # conversion to string required to save to config.
			value.name.upper()
		)

	def test_enabled_lower(self):
		flag = featureFlag._validateConfig_featureFlag(
			"enabled",
			behaviorOfDefault="disabled"
		)
		self.assertFeatureFlagState(
			flag,
			value=FeatureFlagValues.ENABLED,
			behaviorOfDefault=FeatureFlagValues.DISABLED,
			calculatedValue=True
		)

	def test_enabled_upper(self):
		flag = featureFlag._validateConfig_featureFlag(
			"ENABLED",
			behaviorOfDefault="disabled"
		)
		self.assertFeatureFlagState(
			flag,
			value=FeatureFlagValues.ENABLED,
			behaviorOfDefault=FeatureFlagValues.DISABLED,
			calculatedValue=True
		)

	def test_disabled_lower(self):
		flag = featureFlag._validateConfig_featureFlag(
			"disabled",
			behaviorOfDefault="enabled"
		)
		self.assertFeatureFlagState(
			flag,
			value=FeatureFlagValues.DISABLED,
			behaviorOfDefault=FeatureFlagValues.ENABLED,
			calculatedValue=False
		)

	def test_disabled_upper(self):
		flag = featureFlag._validateConfig_featureFlag(
			"DISABLED",
			behaviorOfDefault="enabled"
		)
		self.assertFeatureFlagState(
			flag,
			value=FeatureFlagValues.DISABLED,
			behaviorOfDefault=FeatureFlagValues.ENABLED,
			calculatedValue=False
		)

	def test_default_lower(self):
		flag = featureFlag._validateConfig_featureFlag(
			"default",
			behaviorOfDefault="enabled"
		)
		self.assertFeatureFlagState(
			flag,
			value=FeatureFlagValues.DEFAULT,
			behaviorOfDefault=FeatureFlagValues.ENABLED,
			calculatedValue=True
		)

	def test_default_upper(self):
		flag = featureFlag._validateConfig_featureFlag(
			"DEFAULT",
			behaviorOfDefault="enabled"
		)
		self.assertFeatureFlagState(
			flag,
			value=FeatureFlagValues.DEFAULT,
			behaviorOfDefault=FeatureFlagValues.ENABLED,
			calculatedValue=True
		)

	def test_empty_defaultsToDisabled(self):
		with self.assertRaises(configobj.validate.ValidateError):
			featureFlag._validateConfig_featureFlag(
				"",  # Given our usage of ConfigObj, this situation is unexpected.
				behaviorOfDefault="disabled"
			)

	def test_None_defaultsToDisabled(self):
		with self.assertRaises(configobj.validate.ValidateError):
			featureFlag._validateConfig_featureFlag(
				None,  # Given our usage of ConfigObj, this situation is unexpected.
				behaviorOfDefault="disabled"
			)
