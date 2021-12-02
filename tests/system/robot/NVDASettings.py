# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""Logic for smoketesting the settings.
"""

from robot.libraries.BuiltIn import BuiltIn
# relative import not used for 'systemTestUtils' because the folder is added to the path for 'libraries'
# imported methods start with underscore (_) so they don't get imported into robot files as keywords
from SystemTestSpy import (
	_getLib,
)

# Imported for type information
from robot.libraries.Process import Process as _ProcessLib
from robot.utils.asserts import assert_true, assert_false

from AssertsLib import AssertsLib as _AssertsLib

import os
from typing import Optional
import NvdaLib as _nvdaLib
from NvdaLib import NvdaLib as _nvdaRobotLib
from tests.system.libraries.SystemTestSpy.windows import GetVisibleWindowTitles
_nvdaProcessAlias = _nvdaRobotLib.nvdaProcessAlias

_builtIn: BuiltIn = BuiltIn()
_process: _ProcessLib = _getLib("Process")
_asserts: _AssertsLib = _getLib("AssertsLib")


def navigate_to_settings(settingsName):
	spy = _nvdaLib.getSpyLib()
	# open settings menu
	spy.emulateKeyPress("NVDA+n")
	spy.emulateKeyPress("p")
	spy.emulateKeyPress("s")
	spy.emulateKeyPress("leftWindows+upArrow")  # maximise
	spy.wait_for_speech_to_finish()

	# navigate to setting
	for letter in settingsName.lower():
		spy.emulateKeyPress(letter)

	spy.wait_for_speech_to_finish()
	spy.reset_all_speech_index()


def read_settings(settingsName, cacheFolder, currentVersion, compareVersion: Optional[str] = None):
	spy = _nvdaLib.getSpyLib()
	start_speech_index = spy.get_next_speech_index()
	advancedWarning = "I understand that changing these settings may cause NVDA to function incorrectly."

	# read new setting
	lastSpeech = ""
	while "OK" not in lastSpeech:
		spy.emulateKeyPress("tab")
		spy.wait_for_speech_to_finish()
		lastSpeech = spy.get_last_speech()
		if lastSpeech.split("  ")[0] == advancedWarning:
			spy.emulateKeyPress("space")

	actualSpeech = spy.get_speech_at_index_until_now(start_speech_index)
	os.makedirs(f"{cacheFolder}/{currentVersion}", exist_ok=True)
	with open(f"{cacheFolder}/{currentVersion}/{settingsName}.txt", "w") as f:
		f.write(actualSpeech)

	if compareVersion:
		with open(f"{cacheFolder}/{compareVersion}/{settingsName}.txt", "r") as f:
			compareText = f.read()

		_asserts.strings_match(compareText, actualSpeech)


def open_general_to_braille_then_speech():
	spy = _nvdaLib.getSpyLib()
	# open the general settings dialog
	spy.emulateKeyPress("nvda+control+g")
	# navigate to the panel selection
	spy.emulateKeyPress("shift+tab")
	# open the braille settings dialog
	spy.emulateKeyPress("b")

	# enter the panel
	spy.wait_for_speech_to_finish()
	spy.emulateKeyPress("tab")
	# open the braille driver dialog
	spy.emulateKeyPress("alt+h")

	# change window focus to desktop
	spy.emulateKeyPress("windows+d")

	# open the speech settings dialog
	spy.emulateKeyPress("nvda+control+v")
	spy.wait_for_speech_to_finish()

	windowsTitles = GetVisibleWindowTitles()
	errMsg = f'open windows titles: {",".join(windowsTitles)}'
	assert_true("NVDA Settings: Braille (normal configuration)" in windowsTitles, msg=errMsg)
	assert_true("Select Braille Display" in windowsTitles, msg=errMsg)
	assert_true("NVDA Settings: Speech (normal configuration)" in windowsTitles, msg=errMsg)


def open_braille_then_speech():
	spy = _nvdaLib.getSpyLib()
	# open the braille settings dialog directly
	# using gesture defined in settings-gestures.ini
	spy.emulateKeyPress("control+/")

	# enter the panel
	spy.wait_for_speech_to_finish()
	spy.emulateKeyPress("tab")
	# open the braille driver dialog
	spy.emulateKeyPress("alt+h")

	# change window focus to desktop
	spy.emulateKeyPress("windows+d")

	# open the speech settings dialog
	spy.emulateKeyPress("nvda+control+v")
	spy.wait_for_speech_to_finish()

	windowsTitles = GetVisibleWindowTitles()
	errMsg = f'open windows titles: {",".join(windowsTitles)}'
	assert_true("NVDA Settings: Braille (normal configuration)" in windowsTitles, msg=errMsg)
	assert_true("Select Braille Display" in windowsTitles, msg=errMsg)
	assert_false("NVDA Settings: Speech (normal configuration)" in windowsTitles, msg=errMsg)
