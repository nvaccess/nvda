# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2019 NV Access Limited

"""Classes used to represent settings for Drivers and other AutoSettings instances

	Naming of these classes is historical, kept for backwards compatibility purposes.
"""

from typing import Optional, ClassVar
from dataclasses import dataclass
from baseObject import AutoPropertyObject


@dataclass(eq=False)
class DriverSetting(AutoPropertyObject):
	"""As a base class, represents a setting to be shown in GUI and saved to config.

	GUI representation is a string selection GUI control, a wx.Choice control.

	Used for synthesizer or braille display setting such as voice, variant or dot firmness as
	well as for settings in Vision Providers
	"""
	#: Internal identifier of the setting.
	id: str
	#: The localized string shown in voice or braille settings dialog.
	displayNameWithAccelerator: str
	#: Will this option be available in a settings ring?
	availableInSettingsRing: bool = False
	#: Specifies the default value for a setting.
	defaultVal: Optional[object] = None
	#: The localized string used in synth settings ring or C{None} to use displayNameWithAccelerator.
	displayName: Optional[str] = None
	#: Whether the value of this option is loaded from and saved to NVDA's configuration.
	#: Set this to C{False} if L{AutoSettings} deals with loading and saving.
	useConfig: bool = True

	#: Type information for _get_configSpec
	configSpec: ClassVar[str]

	def _get_configSpec(self) -> str:
		"""Returns the configuration specification of this particular setting for config file validator.
		"""
		return f"string(default={self.defaultVal})"

	def __post_init__(self):
		if not self.displayName:
			# Strip accelerator from displayNameWithAccelerator.
			self.displayName = self.displayNameWithAccelerator.replace("&", "")


@dataclass(eq=False)
class NumericDriverSetting(DriverSetting):
	"""Represents a numeric driver setting such as rate, volume, pitch or dot firmness.
	GUI representation is a slider control.
	@note: If necessary, the step values will be normalised so that]
	L{minStep} <= L{normalStep} <= L{largeStep}.
	"""

	#: Specifies the default value for a numeric setting.
	defaultVal: int = 50
	#: Specifies the minimum valid value for a numeric setting.
	minVal: int = 0
	#: Specifies the maximum valid value for a numeric setting.
	maxVal: int = 100
	#: Specifies the minimum step between valid values for each numeric setting.
	#: For example, if L{minStep} is set to 10, setting values can only be multiples of 10; 10, 20, 30, etc.
	minStep: int = 1
	#: Specifies the step between values that a user will normally prefer.
	#: This is used in the settings ring.
	normalStep: int = 5
	#: Specifies the step between values if a large adjustment is desired.
	#: This is used for pageUp/pageDown on sliders.
	largeStep: int = 10

	def _get_configSpec(self):
		return f"integer(default={self.defaultVal},min={self.minVal},max={self.maxVal})"

	def __post_init__(self):
		super().__post_init__()
		self.normalStep = max(self.normalStep, self.minStep)
		self.largeStep = max(self.largeStep, self.normalStep)


@dataclass(eq=False)
class BooleanDriverSetting(DriverSetting):
	"""Represents a boolean driver setting such as rate boost or automatic time sync.
	GUI representation is a wx.Checkbox
	"""
	#: Specifies the default value for a boolean setting.
	defaultVal: bool = False

	def _get_configSpec(self):
		defaultVal = repr(self.defaultVal) if self.defaultVal is not None else self.defaultVal
		return f"boolean(default={defaultVal})"
