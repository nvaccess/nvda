# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020-2021 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""Logic for NVDA installation process tests.
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


def read_install_dialog():
	"Smoke test the launcher dialogs used to install NVDA"
	
	spy = _nvdaLib.getSpyLib()
	launchDialog = spy.wait_for_specific_speech("NVDA Launcher")  # ensure the dialog is present.
	spy.wait_for_speech_to_finish()
	spy.get_speech_at_index_until_now(launchDialog)

	_builtIn.sleep(1)  # the dialog is not always receiving keypresses, wait a little longer for it
	# agree to the License Agreement
	spy.emulateKeyPress("alt+a")
	
	# start install
	spy.emulateKeyPress("alt+i")

	spy.wait_for_specific_speech("To install NVDA to your hard drive, please press the Continue button.")

	# exit NVDA Installer
	spy.emulateKeyPress("escape")


def read_portable_copy_dialog():
	"Smoke test the launcher dialogs used to create a portable copy of NVDA"

	spy = _nvdaLib.getSpyLib()
	launchDialog = spy.wait_for_specific_speech("NVDA Launcher")  # ensure the dialog is present.
	spy.wait_for_speech_to_finish()
	spy.get_speech_at_index_until_now(launchDialog)

	_builtIn.sleep(1)  # the dialog is not always receiving keypresses, wait a little longer for it
	# agree to the License Agreement
	spy.emulateKeyPress("alt+a")

	# start portable copy
	spy.emulateKeyPress("alt+p")

	spy.wait_for_specific_speech(
		"To create a portable copy of NVDA, please select the path and other options and then press Continue")
	
	# exit NVDA Installer
	spy.emulateKeyPress("escape")
