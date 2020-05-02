# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2019 NV Access Limited

"""Classes used to represent settings for Drivers and other AutoSettings instances

	Naming of these classes is historical, kept for backwards compatibility purposes.
"""

from typing import Optional
from baseObject import AutoPropertyObject


class DriverSetting(AutoPropertyObject):
	"""As a base class, represents a setting to be shown in GUI and saved to config.

	GUI representation is a string selection GUI control, a wx.Choice control.

	Used for synthesizer or braille display setting such as voice, variant or dot firmness as
	well as for settings in Vision Providers
	"""
	id: str
	displayName: str
	displayNameWithAccelerator: str
	availableInSettingsRing: bool
	defaultVal: object
	useConfig: bool

	#: Type information for _get_configSpec
	configSpec: str

	def _get_configSpec(self):
		"""Returns the configuration specification of this particular setting for config file validator.
		@rtype: str
		"""
		return "string(default={defaultVal})".format(defaultVal=self.defaultVal)

	def __init__(
			self,
			id: str,
			displayNameWithAccelerator: str,
			availableInSettingsRing: bool = False,
			defaultVal: object = None,
			displayName: Optional[str] = None,
			useConfig: bool = True
	):
		"""
		@param id: internal identifier of the setting
		@param displayNameWithAccelerator: the localized string shown in voice or braille settings dialog
		@param availableInSettingsRing: Will this option be available in a settings ring?
		@param defaultVal: Specifies the default value for a driver setting.
		@param displayName: the localized string used in synth settings ring or
			None to use displayNameWithAccelerator
		@param useConfig: Whether the value of this option is loaded from and saved to NVDA's configuration.
			Set this to C{False} if the driver deals with loading and saving.
		"""
		self.id = id
		self.displayNameWithAccelerator = displayNameWithAccelerator
		if not displayName:
			# Strip accelerator from displayNameWithAccelerator.
			displayName = displayNameWithAccelerator.replace("&", "")
		self.displayName = displayName
		self.availableInSettingsRing = availableInSettingsRing
		self.defaultVal = defaultVal
		self.useConfig = useConfig


class NumericDriverSetting(DriverSetting):
	"""Represents a numeric driver setting such as rate, volume, pitch or dot firmness.
	GUI representation is a slider control.
	"""

	defaultVal: int

	def _get_configSpec(self):
		return "integer(default={defaultVal},min={minVal},max={maxVal})".format(
			defaultVal=self.defaultVal, minVal=self.minVal, maxVal=self.maxVal)

	def __init__(
			self,
			id,
			displayNameWithAccelerator,
			availableInSettingsRing=False,
			defaultVal: int = 50,
			minVal: int = 0,
			maxVal: int = 100,
			minStep: int = 1,
			normalStep: int = 5,
			largeStep: int = 10,
			displayName: Optional[str] = None,
			useConfig: bool = True):
		"""
		@param defaultVal: Specifies the default value for a numeric driver setting.
		@param minVal: Specifies the minimum valid value for a numeric driver setting.
		@param maxVal: Specifies the maximum valid value for a numeric driver setting.
		@param minStep: Specifies the minimum step between valid values for each numeric setting.
			For example, if L{minStep} is set to 10, setting values can only be multiples of 10; 10, 20, 30, etc.
		@param normalStep: Specifies the step between values that a user will normally prefer.
			This is used in the settings ring.
		@param largeStep: Specifies the step between values if a large adjustment is desired.
			This is used for pageUp/pageDown on sliders in the Voice Settings dialog.
		@note: If necessary, the step values will be normalised so that L{minStep} <= L{normalStep} <= L{largeStep}.
		"""
		super(NumericDriverSetting, self).__init__(
			id,
			displayNameWithAccelerator,
			availableInSettingsRing=availableInSettingsRing,
			defaultVal=defaultVal,
			displayName=displayName,
			useConfig=useConfig
		)
		self.minVal = minVal
		self.maxVal = max(maxVal, self.defaultVal)
		self.minStep = minStep
		self.normalStep = max(normalStep, minStep)
		self.largeStep = max(largeStep, self.normalStep)


class BooleanDriverSetting(DriverSetting):
	"""Represents a boolean driver setting such as rate boost or automatic time sync.
	GUI representation is a wx.Checkbox
	"""
	defaultVal: bool

	def __init__(
			self,
			id: str,
			displayNameWithAccelerator: str,
			availableInSettingsRing: bool = False,
			displayName: Optional[str] = None,
			defaultVal: bool = False,
			useConfig: bool = True
	):
		"""
		@param defaultVal: Specifies the default value for a boolean driver setting.
		"""
		super(BooleanDriverSetting, self).__init__(
			id,
			displayNameWithAccelerator,
			availableInSettingsRing=availableInSettingsRing,
			defaultVal=defaultVal,
			displayName=displayName,
			useConfig=useConfig
		)

	def _get_configSpec(self):
		defaultVal = repr(self.defaultVal) if self.defaultVal is not None else self.defaultVal
		return "boolean(default={defaultVal})".format(defaultVal=defaultVal)
