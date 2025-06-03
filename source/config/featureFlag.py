# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Manages NVDA configuration.
Provides utility classes to make handling featureFlags easier.
"""

import enum
import typing

from . import featureFlagEnums
from .featureFlagEnums import (
	BoolFlag,
	FlagValueEnum,
)
from typing import (
	Union,
)
from configobj.validate import (
	ValidateError,
	VdtParamError,
)
from logHandler import log


class FeatureFlag:
	"""A FeatureFlag allows the selection of a preference for behavior or its default state.
	It's typically used to introduce a feature that isn't expected to handle all use-cases well
	when initially introduced.
	The feature can be disabled initially, some users can manually enable and try the feature
	giving feedback.
	Once developers have confidence in the feature, the default behavior is changed.
	This change in default behavior should not have any impact on users who have already tried the feature,
	and perhaps disagreed in principle with it (I.E. wished to disable the feature, not because it is buggy,
	but because even if it works perfectly it is not their preference).
	The default option allows users to explicitly defer to the NVDA default behaviour.
	The default behaviour can change, without affecting a user's preference.
	"""

	def __init__(
		self,
		value: FlagValueEnum,
		behaviorOfDefault: FlagValueEnum,
	):
		self.value = value
		self.enumClassType: typing.Type[FlagValueEnum] = type(value)
		assert self.enumClassType is type(behaviorOfDefault)
		assert behaviorOfDefault != value.DEFAULT
		self.behaviorOfDefault = behaviorOfDefault

	def __bool__(self) -> bool:
		if not isinstance(self.value, BoolFlag):
			raise NotImplementedError(
				"Only BoolFlag supported. For other types use explicit checks",
			)
		if self.isDefault():
			return bool(self.behaviorOfDefault)
		return bool(self.value)

	def isDefault(self) -> bool:
		return self.value == self.value.DEFAULT

	def calculated(self) -> FlagValueEnum:
		if self.isDefault():
			return self.behaviorOfDefault
		return self.value

	def __eq__(self, other: typing.Union["FeatureFlag", FlagValueEnum]):
		if isinstance(other, type(self.value)):
			other = FeatureFlag(other, behaviorOfDefault=self.behaviorOfDefault)
		if isinstance(other, FeatureFlag):
			return self.calculated() == other.calculated()
		return super().__eq__(other)

	def __str__(self) -> str:
		"""So that the value can be saved to the ini file."""
		return self.value.name


def _validateConfig_featureFlag(
	value: Union[str, FeatureFlag, None],
	optionsEnum: str,
	behaviorOfDefault: str,
) -> FeatureFlag:
	"""Used in conjunction with configObj.Validator
	param value: The value to be validated / converted to a FeatureFlag object.
	Expected: "enabled", "disabled", "default"
	param behaviorOfDefault: Required, the default behavior of the flag, should be "enabled" or "disabled".
	"""
	log.debug(
		f"Validating feature flag: {value}"
		f", optionsEnum: {optionsEnum}"
		f", behaviorOfDefault: {behaviorOfDefault}",
	)
	if not isinstance(optionsEnum, str):
		raise ValidateError(
			"Spec Error: optionsEnum must be specified as a string"
			f" (got type {type(optionsEnum)} with value: {optionsEnum})",
		)
	try:
		OptionsEnumClass = dict(featureFlagEnums.getAvailableEnums())[optionsEnum]
	except KeyError:
		raise ValidateError(
			"Spec Error: optionsEnum must be an enum defined in the config.featureFlagEnums module."
			f" (got {optionsEnum})",
		)

	if not isinstance(behaviorOfDefault, str):
		raise ValidateError(
			"Spec Error: behaviorOfDefault must be specified as a valid"
			f" {OptionsEnumClass.__qualname__} member string"
			f" (got type {type(behaviorOfDefault)} with value: {behaviorOfDefault})",
		)
	try:
		behaviorOfDefault = OptionsEnumClass[behaviorOfDefault.upper()]
	except KeyError:
		raise ValidateError(
			"Spec Error: behaviorOfDefault must be specified as a valid enum member string for enum class "
			f"{OptionsEnumClass.__qualname__} (got {behaviorOfDefault})",
		)
	if behaviorOfDefault == OptionsEnumClass.DEFAULT:
		raise ValidateError("Spec Error: behaviorOfDefault must not be 'default'/'DEFAULT'")

	if isinstance(value, FeatureFlag):
		return value

	if not isinstance(value, str):
		raise ValidateError(
			'Expected a featureFlag value in the form of a string. EG "disabled", "enabled", or "default".'
			f" Got {type(value)} with value: {value} instead.",
		)

	try:
		value = OptionsEnumClass[value.upper()]
	except KeyError:
		raise ValidateError(
			"FeatureFlag value must be specified as a valid enum member string for enum class "
			f"{OptionsEnumClass.__qualname__} (got {value})",
		)

	return FeatureFlag(value, behaviorOfDefault)


def _transformSpec_AddFeatureFlagDefault(specString: str, **kwargs) -> str:
	"""Ensure that default is specified for featureFlag used in configSpec.
	Param examples based on the following spec string in configSpec:
		loadChromiumVBufOnBusyState = featureFlag(behaviorOfDefault="enabled", optionsEnum="BoolFlag")
	@param specString: EG 'featureFlag(behaviorOfDefault="enabled", optionsEnum="BoolFlag")'
	@param kwargs: EG {'behaviorOfDefault': 'enabled', 'optionsEnum':'BoolFlag'}
	@return 'featureFlag(behaviorOfDefault="ENABLED", optionsEnum="BoolFlag", default="DEFAULT")'
	@remarks Manually specifying 'default' in the configSpec string (for featureFlag) will result in a
		VdtParamError. Required params:
		- 'behaviorOfDefault'
		- 'optionsEnum'
	"""
	usage = 'Usage: featureFlag(behaviorOfDefault="enabled"|"disabled", optionsEnum="BoolFlag")'
	if "default=" in specString:
		raise VdtParamError(
			name_or_msg=f"Param 'default' not expected. {usage}",
			value=specString,
		)

	optionsEnumKey = "optionsEnum"
	if optionsEnumKey not in kwargs:
		raise VdtParamError(
			name_or_msg=f"Param '{optionsEnumKey}' missing. {usage}",
			value=specString,
		)
	optionsEnumVal = kwargs[optionsEnumKey]
	if not isinstance(optionsEnumVal, str):
		raise VdtParamError(
			name_or_msg=(
				f"Param '{optionsEnumKey}' should have a string value but got {type(optionsEnumVal)}. {usage}"
			),
			value=specString,
		)
	availableEnums = dict(featureFlagEnums.getAvailableEnums())
	if optionsEnumVal not in availableEnums:
		raise VdtParamError(
			name_or_msg=(
				f"Param '{optionsEnumKey}' should be an enum defined in featureFlagEnums,"
				f" but was {optionsEnumVal}. Currently available: {availableEnums.keys()} "
			),
			value=specString,
		)
	OptionsEnumClass: enum.EnumMeta = availableEnums[optionsEnumVal]
	behaviorOfDefaultKey = "behaviorOfDefault"
	if behaviorOfDefaultKey not in kwargs:
		raise VdtParamError(
			name_or_msg=f"Param '{behaviorOfDefaultKey}' missing. {usage}",
			value=specString,
		)
	behaviorOfDefaultVal = kwargs[behaviorOfDefaultKey]
	if not isinstance(behaviorOfDefaultVal, str):
		raise VdtParamError(
			name_or_msg=(
				f"Param '{behaviorOfDefaultKey}' should have a string value"
				f" but got {type(behaviorOfDefaultVal)}. {usage}"
			),
			value=specString,
		)
	behaviorOfDefaultVal = behaviorOfDefaultVal.upper()
	try:
		OptionsEnumClass[behaviorOfDefaultVal]
	except KeyError:
		raise VdtParamError(
			name_or_msg=(
				f"Param '{behaviorOfDefaultKey}' should be one of: {[o.name for o in OptionsEnumClass]}"
				f" but was {behaviorOfDefaultVal}. {usage}"
			),
			value=specString,
		)
	if len(kwargs) != 2:
		raise VdtParamError(
			name_or_msg=(f"Unexpected number of params. Got {kwargs}. {usage}"),
			value=specString,
		)
	# ensure there is the expected default
	retString = (
		"_featureFlag("
		f'{optionsEnumKey}="{optionsEnumVal}"'
		f', {behaviorOfDefaultKey}="{behaviorOfDefaultVal}"'
		f', default="DEFAULT")'
	)
	return retString
