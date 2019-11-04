# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2006-2019 NV Access Limited, Leonard de Ruijter

"""Handler for driver functionality that is global to synthesizers and braille displays."""
from autoSettingsUtils.autoSettings import AutoSettings
from autoSettingsUtils.utils import (
	paramToPercent,
	percentToParam
)

# F401: the following imports, while unused in this file, are provided for backwards compatibility.
from autoSettingsUtils.driverSetting import (  # noqa: F401
	DriverSetting,
	BooleanDriverSetting,
	NumericDriverSetting,
	AutoPropertyObject,
)
from autoSettingsUtils.utils import (  # noqa: F401
	UnsupportedConfigParameterError,
	StringParameterInfo,
)


class Driver(AutoSettings):
	"""
	Abstract base class for drivers, such as speech synthesizer and braille display drivers.
	Abstract subclasses such as L{braille.BrailleDisplayDriver} should set L{_configSection}.

	At a minimum, drivers must set L{name} and L{description} and override the L{check} method.

	L{supportedSettings} should be set as appropriate for the settings supported by the driver.
	Each setting is retrieved and set using attributes named after the setting;
	e.g. the L{dotFirmness} attribute is used for the L{dotFirmness} setting.
	These will usually be properties.
	"""

	#: The name of the driver; must be the original module file name.
	#: @type: str
	name = ""
	#: A description of the driver.
	#: @type: str
	description = ""
	#: The configuration section where driver specific subsections should be saved.
	#: @type: str
	_configSection = ""

	def __init__(self):
		"""Initialize this driver.
		This method can also set default settings for the driver.
		@raise Exception: If an error occurs.
		@postcondition: This driver can be used.
		"""
		super(Driver, self).__init__()
		self._registerConfigSaveAction()

	def terminate(self, saveSettings: bool = True):
		"""Terminate this driver.
		This should be used for any required clean up.
		@param saveSettings: Whether settings should be saved on termination.
		@precondition: L{initialize} has been called.
		@postcondition: This driver can no longer be used.
		"""
		if saveSettings:
			self.saveSettings()
		self._unregisterConfigSaveAction()

	@classmethod
	def check(cls):
		"""Determine whether this driver is available.
		The driver will be excluded from the list of available drivers if this method returns C{False}.
		For example, if a speech synthesizer requires installation and it is not installed, C{False} should be returned.
		@return: C{True} if this driver is available, C{False} if not.
		@rtype: bool
		"""
		return False


	@classmethod
	def _paramToPercent(cls, current, min, max):
		"""Convert a raw parameter value to a percentage given the current, minimum and maximum raw values.
		@param current: The current value.
		@type current: int
		@param min: The minimum value.
		@type current: int
		@param max: The maximum value.
		@type max: int
		"""
		return paramToPercent(current, min, max)

	@classmethod
	def _percentToParam(cls, percent, min, max):
		"""Convert a percentage to a raw parameter value given the current percentage and the minimum and maximum raw parameter values.
		@param percent: The current percentage.
		@type percent: int
		@param min: The minimum raw parameter value.
		@type min: int
		@param max: The maximum raw parameter value.
		@type max: int
		"""
		return percentToParam(percent, min, max)

# Impl for abstract methods in AutoSettings class
	@classmethod
	def getId(cls) -> str:
		return cls.name

	@classmethod
	def getTranslatedName(cls) -> str:  # todo rename to getTranslatedName
		return cls.description

	@classmethod
	def _getConfigSection(cls) -> str:
		return cls._configSection
