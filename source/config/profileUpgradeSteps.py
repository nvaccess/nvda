# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2016-2025 NV Access Limited, Bill Dengler, Cyrille Bougot, Łukasz Golonka, Leonard de Ruijter, Cary-rowen
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

import os

import configobj.validate
from configobj import ConfigObj
from logHandler import log

from config.configFlags import (
	NVDAKey,
	OutputMode,
	ReportCellBorders,
	ReportLineIndentation,
	ReportSpellingErrors,
	ReportTableHeaders,
	ShowMessages,
	TetherTo,
	TypingEcho,
)


def upgradeConfigFrom_0_to_1(profile: ConfigObj) -> None:
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


def upgradeConfigFrom_1_to_2(profile: ConfigObj) -> None:
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


def upgradeConfigFrom_2_to_3(profile: ConfigObj) -> None:
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


def upgradeConfigFrom_3_to_4(profile: ConfigObj) -> None:
	"Reporting of superscripts and subscripts can now be configured separately to font attributes."
	try:
		profile["documentFormatting"]["reportSuperscriptsAndSubscripts"] = profile["documentFormatting"][
			"reportFontAttributes"
		]
	except KeyError:
		# Setting does not exist, no need for upgrade of this setting
		log.debug("reportFontAttributes not present, no action taken.")


def upgradeConfigFrom_4_to_5(profile: ConfigObj) -> None:
	"""reporting details has become enabled by default.
	Discard aria-details setting, ensure users are aware of the setting.
	The setting was used while the feature was in development.
	Prevented reporting 'has details' with no way to report the details.
	"""
	try:
		del profile["annotations"]["reportDetails"]
	except KeyError:
		# Setting does not exist, no need for upgrade of this setting
		log.debug("reportDetails not present, no action taken.")


def upgradeConfigFrom_5_to_6(profile: ConfigObj) -> None:
	"""
	useInMSWordWhenAvailable in UIA section has been replaced with allowInMSWord multichoice.
	"""
	try:
		useInMSWord: str = profile["UIA"]["useInMSWordWhenAvailable"]
		del profile["UIA"]["useInMSWordWhenAvailable"]
	except KeyError:
		useInMSWord = False
	if configobj.validate.is_boolean(useInMSWord):
		from . import AllowUiaInMSWord

		profile["UIA"]["allowInMSWord"] = AllowUiaInMSWord.ALWAYS.value


def upgradeConfigFrom_6_to_7(profile: ConfigObj) -> None:
	"""
	Selective UIA registration check box has been replaced with event registration multi choice.
	If the user has explicitly enabled selective UIA event registration, set
	the new eventRegistration preference to selective.
	Otherwise, the default value, auto, will be used.
	"""
	try:
		selectiveEventRegistration: str = profile["UIA"]["selectiveEventRegistration"]
		del profile["UIA"]["selectiveEventRegistration"]
	except KeyError:
		selectiveEventRegistration = False
	if configobj.validate.is_boolean(selectiveEventRegistration):
		profile["UIA"]["eventRegistration"] = "selective"


def upgradeConfigFrom_7_to_8(profile: ConfigObj) -> None:
	"""
	In Document formatting settings, "Row/column headers" check box has been replaced with "Headers" combobox.
	"""
	try:
		reportTableHeaders: str = profile["documentFormatting"]["reportTableHeaders"]
	except KeyError:
		# Setting does not exist, no need for upgrade of this setting
		log.debug("reportTableHeaders not present, no action taken.")
	else:
		if configobj.validate.is_boolean(reportTableHeaders):
			profile["documentFormatting"]["reportTableHeaders"] = ReportTableHeaders.ROWS_AND_COLUMNS.value
		else:
			profile["documentFormatting"]["reportTableHeaders"] = ReportTableHeaders.OFF.value


def upgradeConfigFrom_8_to_9(profile: ConfigObj) -> None:
	"""
	In NVDA config, when various values were controlling a single combobox in the settings window, these values
	have been replaced by a single value.
	The following settings are upgraded:
	- Line indentation (in Document formatting settings)
	- Cell borders (in Document formatting settings)
	- Show messages (in Braille settings)
	- Tether to (in Braille settings)
	"""

	_upgradeConfigFrom_8_to_9_lineIndent(profile)
	_upgradeConfigFrom_8_to_9_cellBorders(profile)
	_upgradeConfigFrom_8_to_9_showMessages(profile)
	_upgradeConfigFrom_8_to_9_tetherTo(profile)


def _upgradeConfigFrom_8_to_9_lineIndent(profile: ConfigObj) -> None:
	anySettingInConfig = False
	try:
		reportLineIndent: str = profile["documentFormatting"]["reportLineIndentation"]
		anySettingInConfig = True
	except KeyError:
		reportLineIndent = False
	try:
		reportLineIndentWithTones: str = profile["documentFormatting"]["reportLineIndentationWithTones"]
		del profile["documentFormatting"]["reportLineIndentationWithTones"]
		anySettingInConfig = True
	except KeyError:
		reportLineIndentWithTones = False
	if anySettingInConfig:
		if configobj.validate.is_boolean(reportLineIndent):
			if configobj.validate.is_boolean(reportLineIndentWithTones):
				profile["documentFormatting"]["reportLineIndentation"] = (
					ReportLineIndentation.SPEECH_AND_TONES.value
				)
			else:
				profile["documentFormatting"]["reportLineIndentation"] = ReportLineIndentation.SPEECH.value
		else:
			if configobj.validate.is_boolean(reportLineIndentWithTones):
				profile["documentFormatting"]["reportLineIndentation"] = ReportLineIndentation.TONES.value
			else:
				profile["documentFormatting"]["reportLineIndentation"] = ReportLineIndentation.OFF.value
	else:
		log.debug("reportLineIndentation and reportLineIndentationWithTones not present, no action taken.")


def _upgradeConfigFrom_8_to_9_cellBorders(profile: ConfigObj) -> None:
	anySettingInConfig = False
	try:
		reportBorderStyle: str = profile["documentFormatting"]["reportBorderStyle"]
		del profile["documentFormatting"]["reportBorderStyle"]
		anySettingInConfig = True
		reportBorderStyleMissing = False
	except KeyError:
		reportBorderStyle = False
		reportBorderStyleMissing = True
	try:
		reportBorderColor: str = profile["documentFormatting"]["reportBorderColor"]
		del profile["documentFormatting"]["reportBorderColor"]
		anySettingInConfig = True
	except KeyError:
		reportBorderColor = False
	if anySettingInConfig:
		if configobj.validate.is_boolean(reportBorderStyle):
			if configobj.validate.is_boolean(reportBorderColor):
				profile["documentFormatting"]["reportCellBorders"] = ReportCellBorders.COLOR_AND_STYLE.value
			else:
				profile["documentFormatting"]["reportCellBorders"] = ReportCellBorders.STYLE.value
		elif configobj.validate.is_boolean(reportBorderColor) and reportBorderStyleMissing:
			# In default profile, this config cannot be set.
			# However in a non-default profile you can get this config if:
			# - default profile is set with "Cell borders" on "styles"
			# - the other profile is set with "Cell borders" on "Both colors and styles"
			profile["documentFormatting"]["reportCellBorders"] = ReportCellBorders.COLOR_AND_STYLE.value
		else:
			profile["documentFormatting"]["reportCellBorders"] = ReportCellBorders.OFF.value
	else:
		log.debug("reportBorderStyle and reportBorderColor not present, no action taken.")


def _upgradeConfigFrom_8_to_9_showMessages(profile: ConfigObj) -> None:
	upgradeNeeded = False
	try:
		noMessageTimeout: str = profile["braille"]["noMessageTimeout"]
	except KeyError:
		noMessageTimeoutVal = False  # Default value
	else:
		del profile["braille"]["noMessageTimeout"]
		noMessageTimeoutVal = configobj.validate.is_boolean(noMessageTimeout)
		upgradeNeeded = True
	try:
		messageTimeout: str = profile["braille"]["messageTimeout"]
	except KeyError:
		messageTimeoutVal = 4  # Default value
	else:
		messageTimeoutVal = configobj.validate.is_integer(messageTimeout)
		if messageTimeoutVal == 0:
			del profile["braille"]["messageTimeout"]
			upgradeNeeded = True

	if upgradeNeeded:
		if messageTimeoutVal == 0:
			profile["braille"]["showMessages"] = ShowMessages.DISABLED.value
			if noMessageTimeoutVal:
				# Invalid config with noMessageTimeout=True and messageTimeout=0." is possible (if set manually by a user)
				# and it actually leads to disabled messages.
				# So we fix it with ShowMessages.DISABLED but also issue a warning.
				log.debugWarning(
					"Invalid config found: noMessageTimeout=True and messageTimeout=0."
					" Fixing it with setting showMessages on DISABLE.",
				)
		else:
			if noMessageTimeoutVal:
				profile["braille"]["showMessages"] = ShowMessages.SHOW_INDEFINITELY.value
			else:
				profile["braille"]["showMessages"] = ShowMessages.USE_TIMEOUT.value
	else:
		log.debug("messageTimeout >= 1 or not present and noMessageTimeout not present, no action taken.")


def _upgradeConfigFrom_8_to_9_tetherTo(profile: ConfigObj) -> None:
	try:
		autoTether: str = profile["braille"]["autoTether"]
		isAutoTetherMissing = False
	except KeyError:
		autoTether: str = "True"
		isAutoTetherMissing = True
	else:
		del profile["braille"]["autoTether"]
	try:
		tetherTo: str = profile["braille"]["tetherTo"]
		isTetherToMissing = False
	except KeyError:
		tetherTo: str = TetherTo.FOCUS.value
		isTetherToMissing = True

	autoTetherVal = configobj.validate.is_boolean(autoTether)
	tetherToVal = configobj.validate.is_string(tetherTo)
	if isAutoTetherMissing and isTetherToMissing:
		log.debug("autoTether and tetherTo not present in config, no action taken.")
	elif isAutoTetherMissing:
		# It is not possible to get tetherTo without having autoTether in default profile's config.
		# This is possible in a non-default config in case "Tether to" option is not set to "Automatically" (e.g.
		# "Review") and the current profile has this option set to "Focus".
		# In this case, tetherTo keeps the same value.
		log.debug(
			"autoTether not present in config but tetherTo present, no action taken (keeping tetherTo value).",
		)
	elif isTetherToMissing:
		if autoTetherVal:
			profile["braille"]["tetherTo"] = TetherTo.AUTO.value
		else:
			profile["braille"]["tetherTo"] = TetherTo.FOCUS.value
	else:  # both values present in config
		if autoTetherVal:
			profile["braille"]["tetherTo"] = TetherTo.AUTO.value
		else:
			profile["braille"]["tetherTo"] = tetherToVal


def upgradeConfigFrom_9_to_10(profile: ConfigObj) -> None:
	"""In NVDA config, use only one value to store NVDA keys rather than 3 distinct values."""

	anySettingInConfig = False
	try:
		capsLock: str = profile["keyboard"]["useCapsLockAsNVDAModifierKey"]
		del profile["keyboard"]["useCapsLockAsNVDAModifierKey"]
		anySettingInConfig = True
	except KeyError:
		capsLock = False
	try:
		numpadInsert: str = profile["keyboard"]["useNumpadInsertAsNVDAModifierKey"]
		del profile["keyboard"]["useNumpadInsertAsNVDAModifierKey"]
		anySettingInConfig = True
	except KeyError:
		numpadInsert = True
	try:
		extendedInsert: str = profile["keyboard"]["useExtendedInsertAsNVDAModifierKey"]
		del profile["keyboard"]["useExtendedInsertAsNVDAModifierKey"]
		anySettingInConfig = True
	except KeyError:
		extendedInsert = True
	if anySettingInConfig:
		val = 0
		if configobj.validate.is_boolean(capsLock):
			val |= NVDAKey.CAPS_LOCK.value
		if configobj.validate.is_boolean(numpadInsert):
			val |= NVDAKey.NUMPAD_INSERT.value
		if configobj.validate.is_boolean(extendedInsert):
			val |= NVDAKey.EXTENDED_INSERT.value
		if val == 0:
			# val may be 0 if:
			# 1: The default profile has caps lock enabled and the currently upgraded profile has ext insert and
			# numpad insert disabled. In the current profile's config this leads to:
			# - useNumpadInsertAsNVDAModifierKey = False
			# - useExtendedInsertAsNVDAModifierKey = False
			# - useCapsLockAsNVDAModifierKey not present (True inherited from default config)
			# (see issue #14527 for full description)
			# or
			# 2: Someone did disabled all 3 possible NVDA key in config manually, e.g. modifying nvda.ini or via the
			# Python console.
			# Thus we consider case 1 which is the only use case reachable by the user via NVDA's GUI.
			log.debug(
				"No True value for any of 'use*AsNVDAModifierKey',"
				" restore caps lock (only possible case via NVDA's GUI).",
			)
			val = NVDAKey.CAPS_LOCK.value
		profile["keyboard"]["NVDAModifierKeys"] = val
	else:
		log.debug("use*AsNVDAModifierKey values not present, no action taken.")


def upgradeConfigFrom_10_to_11(profile: ConfigObj) -> None:
	"""Remove the enableHidBrailleSupport braille config flag in favor of an auto detect exclusion."""
	# Config spec entry was:
	# enableHidBrailleSupport = integer(0, 2, default=0)  # 0:Use default/recommended value (yes), 1:yes, 2:no
	try:
		hidSetting: str = profile["braille"]["enableHidBrailleSupport"]
		del profile["braille"]["enableHidBrailleSupport"]
	except KeyError:
		log.debug("enableHidBrailleSupport not present in config, no action taken.")
		return
	if configobj.validate.is_integer(hidSetting) == 2:  # HID standard support disabled
		if "braille" not in profile:
			profile["braille"] = {}
		if "auto" not in profile["braille"]:
			profile["braille"]["auto"] = {}
		if "excludedDisplays" not in profile["braille"]["auto"]:
			profile["braille"]["auto"]["excludedDisplays"] = []
		profile["braille"]["auto"]["excludedDisplays"] += ["hidBrailleStandard"]
		log.debug(
			"hidBrailleStandard added to braille display auto detection excluded displays. "
			f"List is now: {profile['braille']['auto']['excludedDisplays']}",
		)


def upgradeConfigFrom_11_to_12(profile: ConfigObj) -> None:
	"""Add a new key, documentFormatting.fontAttributeReporting, which allows users to select between speech and/or braille, and base it on documentFormatting.reportFontAttributes."""
	try:
		reportFontAttributes: bool = profile["documentFormatting"].as_bool("reportFontAttributes")
	except KeyError:
		log.debug("reportFontAttributes not present in config, no action taken.")
		return
	except ValueError:
		log.error("reportFontAttributes is not a boolean, no action taken.")
		return
	profile["documentFormatting"]["fontAttributeReporting"] = (
		OutputMode.SPEECH_AND_BRAILLE if reportFontAttributes else OutputMode.OFF
	)
	log.debug(
		f"documentFormatting.fontAttributeReporting added with value {profile['documentFormatting']['fontAttributeReporting']}.",
	)


def upgradeConfigFrom_12_to_13(profile: ConfigObj) -> None:
	"""
	If the includeCldr speech config flag is set in a profile,
	enable the cldr dictionary in the speechSymbols list.
	"""
	try:
		setting: bool = profile["speech"].as_bool("includeCLDR")
	except KeyError:
		log.debug("includeCLDR not present in config, no action taken.")
		return
	except ValueError:
		log.error("includeCLDR is not a boolean, no action taken.")
		return
	profile["speech"]["symbolDictionaries"] = ["cldr"] if setting else []
	log.debug(
		f"Handled cldr value of {setting!r}. List is now: {profile['speech']['symbolDictionaries']}",
	)


def upgradeConfigFrom_13_to_14(profile: ConfigObj):
	"""Set [audio][outputDevice] to the endpointID of [speech][outputDevice], and delete the latter."""
	try:
		friendlyName = profile["speech"]["outputDevice"]
	except KeyError:
		log.debug("Output device not present in config. Taking no action.")
		return
	if friendlyName == "default":
		log.debug("Output device is set to default. Not writing a new value to config.")
	elif endpointId := _friendlyNameToEndpointId(friendlyName):
		log.debug(
			f"Best match for device with {friendlyName=} has {endpointId=}. Writing new value to config.",
		)
		if "audio" not in profile:
			profile["audio"] = {}
		profile["audio"]["outputDevice"] = endpointId
	else:
		log.debug(
			f"Could not find an audio output device with {friendlyName=}. Not writing a new value to config.",
		)
	log.debug("Deleting old config value.")
	del profile["speech"]["outputDevice"]


def _friendlyNameToEndpointId(friendlyName: str) -> str | None:
	"""Convert a device friendly name to an endpoint ID string.

	Since friendly names are not unique, there may be many devices on one system with the same friendly name.
	As the order of devices in an IMMEndpointEnumerator is arbitrary, we cannot assume that the first device with a matching friendly name is the device the user wants.
	We also can't guarantee that the device the user has selected is active, so we need to retrieve devices by state, in order from most to least preferable.
	It is probably a safe bet that the device the user wants to use is either active or unplugged.
	Thus, the preference order for states is:
	1. ACTIVE- The audio adapter that connects to the endpoint device is present and enabled.
	   In addition, if the endpoint device plugs into a jack on the adapter, then the endpoint device is plugged in.
	2. UNPLUGGED - The audio adapter that contains the jack for the endpoint device is present and enabled, but the endpoint device is not plugged into the jack.
	3. DISABLED - The user has disabled the device in the Windows multimedia control panel.
	4. NOTPRESENT - The audio adapter that connects to the endpoint device has been removed from the system, or the user has disabled the adapter device in Device Manager.
	Within a state, if there is more than one device with the selected friendly name, we use the first one.

	:param friendlyName: Friendly name of the device to search for.
	:return: Endpoint ID string of the best match device, or `None` if no device with a matching friendly name is available.
	"""
	from utils.mmdevice import getOutputDevices
	from pycaw.constants import DEVICE_STATE

	states = (DEVICE_STATE.ACTIVE, DEVICE_STATE.UNPLUGGED, DEVICE_STATE.DISABLED, DEVICE_STATE.NOTPRESENT)
	for state in states:
		try:
			return next(
				device for device in getOutputDevices(stateMask=state) if device.friendlyName == friendlyName
			).id
		except StopIteration:
			# Proceed to the next device state.
			continue
	return None


def upgradeConfigFrom_14_to_15(profile: ConfigObj):
	"""Convert keyboard typing echo configurations from boolean to integer values."""
	_convertTypingEcho(profile, "speakTypedCharacters")
	_convertTypingEcho(profile, "speakTypedWords")


def _convertTypingEcho(profile: ConfigObj, key: str) -> None:
	"""
	Convert a keyboard typing echo configuration from boolean to integer values.

	:param profile: The `ConfigObj` instance representing the user's NVDA configuration file.
	:param key: The configuration key to convert.
	"""
	try:
		oldValue: bool = profile["keyboard"].as_bool(key)
	except KeyError:
		log.debug(f"'{key}' not present in config, no action taken.")
		return
	except ValueError:
		log.error(f"'{key}' is not a boolean, got {profile['keyboard'][key]!r}. Deleting.")
		del profile["keyboard"][key]
		return
	else:
		newValue = TypingEcho.EDIT_CONTROLS.value if oldValue else TypingEcho.OFF.value
		profile["keyboard"][key] = newValue
		log.debug(f"Converted '{key}' from {oldValue!r} to {newValue} ({TypingEcho(newValue).name}).")


def upgradeConfigFrom_15_to_16(profile: ConfigObj) -> None:
	"""Migrate remote.ini settings into the main config."""
	remoteIniPath = os.path.join(os.path.dirname(profile.filename), "remote.ini")
	if not os.path.isfile(remoteIniPath):
		log.debug(f"No remote.ini found, no action taken. Checked {remoteIniPath}")
		return

	try:
		log.debug(f"Loading remote config from {remoteIniPath}")
		remoteConfig = ConfigObj(remoteIniPath, encoding="UTF-8")
	except Exception:
		log.error("Error loading remote.ini", exc_info=True)
		return

	# Create remote section if it doesn't exist
	if "remote" not in profile:
		profile["remote"] = {}

	# Copy all sections from remote.ini
	for section in remoteConfig:
		if section not in profile["remote"]:
			profile["remote"][section] = {}
		profile["remote"][section].update(remoteConfig[section])

	try:
		# Backup the old file just in case
		backupPath = remoteIniPath + ".old"
		if os.path.exists(backupPath):
			os.unlink(backupPath)
		os.rename(remoteIniPath, backupPath)
		log.debug(f"Backed up remote.ini to {backupPath}")
	except Exception:
		log.error("Error backing up remote.ini after migration", exc_info=True)


def upgradeConfigFrom_16_to_17(profile: ConfigObj) -> None:
	"""Rename some of Remote Access's config items.

	Provided as a separate upgrade step so that alpha users don't lose any of their configuration of Remote Access.
	"""
	RENAMED_SECTIONS: dict[str, str] = {
		"controlserver": "controlServer",
		"seen_motds": "seenMOTDs",
		"trusted_certs": "trustedCertificates",
	}
	RENAMED_ITEMS: dict[str, dict[str, str]] = {
		"connections": {"last_connected": "lastConnected"},
		"controlServer": {"connection_type": "connectionMode", "self_hosted": "selfHosted"},
	}
	if "remote" not in profile:
		log.debug("No remote section in config, no action taken.")
		return

	remoteConfig = profile["remote"]
	# Rename sections whose names have changed.
	for oldSectionKey, newSectionKey in RENAMED_SECTIONS.items():
		if oldSectionKey in remoteConfig:
			remoteConfig[newSectionKey] = remoteConfig[oldSectionKey]
			del remoteConfig[oldSectionKey]
			log.debug(f"Renamed config['remote']['{oldSectionKey}'] to config['remote']['{newSectionKey}'].")

	# Rename items (leaves) whose names have changed.
	for sectionKey, renamedItems in RENAMED_ITEMS.items():
		if (section := remoteConfig.get(sectionKey)) is not None:
			for oldItemKey, newItemKey in renamedItems.items():
				if oldItemKey in section:
					section[newItemKey] = section[oldItemKey]
					del section[oldItemKey]
					log.debug(
						f"Renamed config['remote']['{sectionKey}']['{oldItemKey}'] to config['remote']['{sectionKey}']['{newItemKey}'].",
					)


def upgradeConfigFrom_17_to_18(profile: ConfigObj) -> None:
	"""Add dotPad to excluded braille displays by default due to generic USB PID/VID."""
	# Only add to excludedDisplays if the auto section doesn't exist or excludedDisplays is empty/default
	if "braille" not in profile:
		profile["braille"] = {}
	if "auto" not in profile["braille"]:
		profile["braille"]["auto"] = {}
	if "excludedDisplays" not in profile["braille"]["auto"]:
		profile["braille"]["auto"]["excludedDisplays"] = []

	# Only add dotPad if it's not already in the list
	excludedDisplays = profile["braille"]["auto"]["excludedDisplays"]

	if "dotPad" not in excludedDisplays:
		excludedDisplays.append("dotPad")
		log.debug(
			"dotPad added to braille display auto detection excluded displays due to generic USB PID/VID. "
			f"List is now: {excludedDisplays}",
		)


def upgradeConfigFrom_18_to_19(profile: ConfigObj):
	"""Convert report spelling errors configurations from boolean to integer values."""

	section = "documentFormatting"
	key = "reportSpellingErrors"
	newKey = "reportSpellingErrors2"
	try:
		oldValue: bool = profile[section].as_bool(key)
	except KeyError:
		log.debug(f"'{key}' not present in config, no action taken.")
		return
	except ValueError:
		log.error(f"'{key}' is not a boolean, got {profile[section][key]!r}. No action taken.")
		return

	newValue = ReportSpellingErrors.SPEECH.value if oldValue else ReportSpellingErrors.OFF.value
	profile[section][newKey] = newValue
	del profile[section][key]
	log.debug(
		f"Converted '{key}' with value {oldValue} to '{newKey}' with value {newValue}"
		f" ({ReportSpellingErrors(newValue).name}). The old key '{key}' has been deleted.",
	)
