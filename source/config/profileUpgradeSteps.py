# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2016-2022 NV Access Limited, Bill Dengler, Cyrille Bougot, Łukasz Golonka
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
Contains upgrade steps for the NVDA configuration files. These steps are run to ensure that a configuration file
complies with the latest schema (@see configSpec.py).

To add a new step (after modifying the schema and incrementing the schema version number) add a new method to this
module. The method name should be in the form "upgradeConfigFrom_X_to_Y" where X is the previous schema version, and Y
is the current schema version. The argument profile will be a configobj.ConfigObj object. The function should ensure 
that no information is lost, while updating the ConfigObj to meet the requirements of the new schema.
"""

from logHandler import log
from config.configFlags import ReportTableHeaders
from typing import (
	Dict,
)
import configobj.validate


def upgradeConfigFrom_0_to_1(profile):
	# Schema has been modified to set a new minimum blink rate
	# The blink rate could previously be set to zero to disable blinking (while still 
	# having a cursor)
	try:
		blinkRate = int(profile["braille"]["cursorBlinkRate"])
	except KeyError:
		# Setting does not exist, no need for upgrade of this setting
		log.debug("No cursorBlinkRate, no action taken.")
	else:
		newMinBlinkRate = 200
		if blinkRate < newMinBlinkRate:
			profile["braille"]["cursorBlinkRate"] = newMinBlinkRate
			if blinkRate < 1:
				profile["braille"]["cursorBlink"] = False


def upgradeConfigFrom_1_to_2(profile):
	# Schema has been modified to split cursor shape into focus and review shapes
	# Previously, the same cursor shape was used for focus and review
	try:
		cursorShape = int(profile["braille"]["cursorShape"])
	except KeyError:
		# Setting does not exist, no need for upgrade of this setting
		log.debug("No cursorShape, no action taken.")
	else:
		del profile["braille"]["cursorShape"]
		profile["braille"]["cursorShapeFocus"] = cursorShape


def upgradeConfigFrom_2_to_3(profile):
	# The winConsoleSpeakPasswords option has been moved to the terminals section of the config.
	try:
		speakPasswords = profile["UIA"]["winConsoleSpeakPasswords"]
	except KeyError:
		# Setting does not exist, no need for upgrade of this setting
		log.debug("winConsoleSpeakPasswords not present, no action taken.")
	else:
		del profile["UIA"]["winConsoleSpeakPasswords"]
		if "terminals" not in profile:
			profile["terminals"] = {}
		profile["terminals"]["speakPasswords"] = speakPasswords


def upgradeConfigFrom_3_to_4(profile):
	"Reporting of superscripts and subscripts can now be configured separately to font attributes."
	try:
		profile['documentFormatting']['reportSuperscriptsAndSubscripts'] = (
			profile['documentFormatting']['reportFontAttributes']
		)
	except KeyError:
		# Setting does not exist, no need for upgrade of this setting
		log.debug("reportFontAttributes not present, no action taken.")


def upgradeConfigFrom_4_to_5(profile):
	""" reporting details has become enabled by default.
	Discard aria-details setting, ensure users are aware of the setting.
	The setting was used while the feature was in development.
	Prevented reporting 'has details' with no way to report the details.
	"""
	try:
		del profile['annotations']['reportDetails']
	except KeyError:
		# Setting does not exist, no need for upgrade of this setting
		log.debug("reportDetails not present, no action taken.")


def upgradeConfigFrom_5_to_6(profile: dict):
	"""
	useInMSWordWhenAvailable in UIA section has been replaced with allowInMSWord multichoice.
	"""
	try:
		useInMSWord: str = profile['UIA']['useInMSWordWhenAvailable']
		del profile['UIA']['useInMSWordWhenAvailable']
	except KeyError:
		useInMSWord = False
	if configobj.validate.is_boolean(useInMSWord):
		from . import AllowUiaInMSWord
		profile['UIA']['allowInMSWord'] = AllowUiaInMSWord.ALWAYS.value


def upgradeConfigFrom_6_to_7(profile: Dict[str, str]) -> None:
	"""
	Selective UIA registration check box has been replaced with event registration multi choice.
	If the user has explicitly enabled selective UIA event registration, set
	the new eventRegistration preference to selective.
	Otherwise, the default value, auto, will be used.
	"""
	try:
		selectiveEventRegistration: str = profile['UIA']['selectiveEventRegistration']
		del profile['UIA']['selectiveEventRegistration']
	except KeyError:
		selectiveEventRegistration = False
	if configobj.validate.is_boolean(selectiveEventRegistration):
		profile['UIA']['eventRegistration'] = "selective"


def upgradeConfigFrom_7_to_8(profile: Dict[str, str]) -> None:
	"""
	In Document formatting settings, "Row/column headers" check box has been replaced with "Headers" combobox.
	"""
	try:
		reportTableHeaders: str = profile['documentFormatting']['reportTableHeaders']
	except KeyError:
		# Setting does not exist, no need for upgrade of this setting
		log.debug("reportTableHeaders not present, no action taken.")
	else:
		if configobj.validate.is_boolean(reportTableHeaders):
			profile['documentFormatting']['reportTableHeaders'] = ReportTableHeaders.ROWS_AND_COLUMNS.value
		else:
			profile['documentFormatting']['reportTableHeaders'] = ReportTableHeaders.OFF.value
