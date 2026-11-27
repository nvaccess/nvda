# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2026 NV Access Limited, Leonard de Ruijter, Cary-rowen
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Handler for driver functionality that is global to synthesizers and braille displays."""

from autoSettingsUtils.autoSettings import AutoSettings


class Driver(AutoSettings):
	"""
	Abstract base class for drivers, such as speech synthesizer and braille display drivers.
	Abstract subclasses such as L{braille.display.driver.BrailleDisplayDriver} should set L{_configSection}.

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
		super().__init__()

	def terminate(self):
		"""Release driver resources without saving settings.

		Code managing this driver must call :meth:`saveSettings` before replacement or profile switching
		when changes should be kept. Overrides must call this method to unregister configuration save callbacks.
		The driver must not be used after termination.
		"""
		self._unregisterConfigSaveAction()

	def __repr__(self):
		return f"{self.__class__.__name__}({self.name!r})"

	@classmethod
	def check(cls):
		"""Determine whether this driver is available.
		The driver will be excluded from the list of available drivers if this method returns C{False}.
		For example, if a speech synthesizer requires installation and it is not installed, C{False} should be returned.
		@return: C{True} if this driver is available, C{False} if not.
		@rtype: bool
		"""
		return False

	# Impl for abstract methods in AutoSettings class
	@classmethod
	def getId(cls) -> str:
		return cls.name

	@classmethod
	def getDisplayName(cls) -> str:
		return cls.description

	@classmethod
	def _getConfigSection(cls) -> str:
		return cls._configSection
