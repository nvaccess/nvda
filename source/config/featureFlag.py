# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Manages NVDA configuration.
Provides utility classes to make handling featureFlags easier.
"""

import enum
from typing import (
	Optional,
)
from configobj.validate import (
	ValidateError,
	VdtParamError,
)
from logHandler import log


class FeatureFlagValue(enum.Enum):
	""" The explicit DEFAULT option allows developers to differentiate between a value set that happens to be
	the current default, and a value that has been returned to the "default" explicitly.
	"""
	DEFAULT = enum.auto()
	DISABLED = enum.auto()
	ENABLED = enum.auto()


class FeatureFlag:
	"""A FeatureFlag is a boolean flag that can be enabled, disabled or left at its default state.
	NVDA logic only cares about the effective Enabled/Disabled dichotomy.
	The default option allows users to explicitly enable, disable, or defer to the NVDA default behaviour.
	This allows for the default behaviour to change, without affecting a users explicit choice to enable, or
	disable.
	"""
	def __init__(self, value: FeatureFlagValue, behaviorOfDefault: FeatureFlagValue):
		self.value = value
		assert behaviorOfDefault != FeatureFlagValue.DEFAULT
		self.behaviorOfDefault = behaviorOfDefault

	def __bool__(self) -> bool:
		return (
			self.value == FeatureFlagValue.ENABLED
			or (
				self.value == FeatureFlagValue.DEFAULT
				and self.behaviorOfDefault == FeatureFlagValue.ENABLED
			)
		)

	def __str__(self):
		"""So that the value can be saved to the ini file."""
		return self.value.name


def _validateConfig_featureFlag(value: Optional[str], behaviorOfDefault: str) -> FeatureFlag:
	""" Used in conjunction with configObj.Validator
	param value: The value to be validated / converted to a FeatureFlag object.
	Expected: "enabled", "disabled", "default"
	param behaviorOfDefault: Required, the default behavior of the flag, should be "enabled" or "disabled".
	"""
	log.debug(f"Validating feature flag: {value}, behaviorOfDefault: {behaviorOfDefault}")
	if not isinstance(behaviorOfDefault, str):
		raise ValidateError(
			'Spec Error: behaviorOfDefault must be specified as a valid FeatureFlagValue string'
			f" (got type {type(behaviorOfDefault)} with value: {behaviorOfDefault})"
		)
	try:
		behaviorOfDefault = FeatureFlagValue[behaviorOfDefault.upper()]
	except KeyError:
		raise ValidateError(
			"Spec Error: behaviorOfDefault must be specified as a valid FeatureFlagValue string"
			f" (got {behaviorOfDefault})"
		)
	if behaviorOfDefault == FeatureFlagValue.DEFAULT:
		raise ValidateError("Spec Error: behaviorOfDefault must not be 'default'")

	if not isinstance(value, str):
		raise ValidateError(
			'Expected a featureFlag value in the form of a string. EG "disabled", "enabled", or "default".'
			f" Got {type(value)} with value: {value} instead."
		)
	try:
		value = FeatureFlagValue[value.upper()]
	except KeyError:
		raise ValidateError(
			"FeatureFlag value must be specified as a valid FeatureFlagValue value string."
			f" (got value: {value})"
		)
	return FeatureFlag(value, behaviorOfDefault)


def _transformSpec_AddFeatureFlagDefault(specString: str, **kwargs) -> str:
	""" Ensure that default is specified for featureFlag used in configSpec.
	Param examples based on the following spec string in configSpec:
		loadChromiumVBufOnBusyState = featureFlag(behaviorOfDefault="enabled")
	@param specString: EG 'featureFlag(behaviorOfDefault="enabled")'
	@param kwargs: EG {'behaviorOfDefault': 'enabled'}
	@return 'featureFlag(behaviorOfDefault="enabled", default="default")'
	@remarks Manually specifying 'default' in the configSpec string (for featureFlag) will result in a
		VdtParamError. Param 'behaviorOfDefault' must be supplied.
	"""
	usage = 'Usage: featureFlag(behaviorOfDefault="enabled"|"disabled")'
	if "default=" in specString:
		raise VdtParamError(
			name_or_msg=f"Param 'default' not expected. {usage}",
			value=specString
		)
	behaviorOfDefaultKey = "behaviorOfDefault"
	if behaviorOfDefaultKey not in kwargs:
		raise VdtParamError(
			name_or_msg=f"Param '{behaviorOfDefaultKey}' missing. {usage}",
			value=specString
		)
	behaviorOfDefaultVal = kwargs[behaviorOfDefaultKey]
	if not isinstance(behaviorOfDefaultVal, str):
		raise VdtParamError(
			name_or_msg=(
				f"Param '{behaviorOfDefaultKey}' should have a string value"
				f" but got {type(behaviorOfDefaultVal)}. {usage}"),
			value=specString
		)
	behaviorOfDefaultVal = behaviorOfDefaultVal.lower()
	if behaviorOfDefaultVal not in ['enabled', 'disabled']:
		raise VdtParamError(
			name_or_msg=(
				f"Param '{behaviorOfDefaultKey}' should be either 'enabled' or 'disabled'"
				f" but was {behaviorOfDefaultVal}. {usage}"
			),
			value=specString
		)
	if len(kwargs) != 1:
		raise VdtParamError(
			name_or_msg=(
				f"Unexpected number of params."
				f" Got {kwargs}. {usage}"
			),
			value=specString
		)
	# ensure there is the expected default
	return f'featureFlag({behaviorOfDefaultKey}="{behaviorOfDefaultVal}", default="default")'
