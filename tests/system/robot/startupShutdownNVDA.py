# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""Logic for startupShutdownNVDA tests.
"""

from robot.libraries.BuiltIn import BuiltIn
# relative import not used for 'systemTestUtils' because the folder is added to the path for 'libraries'
# imported methods start with underscore (_) so they don't get imported into robot files as keywords
from SystemTestSpy import (
	_getLib,
)

# Imported for type information
from robot.libraries.Process import Process as _ProcessLib

from AssertsLib import AssertsLib as _AssertsLib

import NvdaLib as _nvdaLib
from NvdaLib import NvdaLib as _nvdaRobotLib
_nvdaProcessAlias = _nvdaRobotLib.nvdaProcessAlias

_builtIn: BuiltIn = BuiltIn()
_process: _ProcessLib = _getLib("Process")
_asserts: _AssertsLib = _getLib("AssertsLib")


def NVDA_Starts():
	""" Test that NVDA can start"""
	_process.process_should_be_running(_nvdaProcessAlias)


def quits_from_keyboard():
	"""Ensure NVDA can be quit from keyboard."""
	spy = _nvdaLib.getSpyLib()
	spy.wait_for_specific_speech("Welcome to NVDA")  # ensure the dialog is present.
	spy.wait_for_speech_to_finish()
	_builtIn.sleep(1)  # the dialog is not always receiving the enter keypress, wait a little longer for it
	spy.emulateKeyPress("enter")

	spy.emulateKeyPress("insert+q")
	exitTitleIndex = spy.wait_for_specific_speech("Exit NVDA")

	spy.wait_for_speech_to_finish()
	actualSpeech = spy.get_speech_at_index_until_now(exitTitleIndex)

	_asserts.strings_match(
		actualSpeech,
		"\n".join([
			"Exit NVDA  dialog",
			"What would you like to do?  combo box  Exit  collapsed  Alt plus d"
		])
	)
	_builtIn.sleep(1)  # the dialog is not always receiving the enter keypress, wait a little longer for it
	spy.emulateKeyPress("enter", blockUntilProcessed=False)
	_process.wait_for_process(_nvdaProcessAlias, timeout="10 sec")
	_process.process_should_be_stopped(_nvdaProcessAlias)


def read_welcome_dialog():
	spy = _nvdaLib.getSpyLib()
	welcomeTitleIndex = spy.wait_for_specific_speech("Welcome to NVDA")  # ensure the dialog is present.
	spy.wait_for_speech_to_finish()
	actualSpeech = spy.get_speech_at_index_until_now(welcomeTitleIndex)

	_asserts.strings_match(
		actualSpeech,
		"\n".join([
			(
				"Welcome to NVDA  dialog  Welcome to NVDA! Most commands for controlling NVDA require you to hold "
				"down the NVDA key while pressing other keys. By default, the numpad Insert and main Insert keys "
				"may both be used as the NVDA key. You can also configure NVDA to use the Caps Lock as the NVDA "
				"key. Press NVDA plus n at any time to activate the NVDA menu. From this menu, you can configure "
				"NVDA, get help and access other NVDA functions."
			),
			"Options  grouping",
			"Keyboard layout:  combo box  desktop  collapsed  Alt plus k"
		])
	)
	_builtIn.sleep(1)  # the dialog is not always receiving the enter keypress, wait a little longer for it
	spy.emulateKeyPress("enter")
