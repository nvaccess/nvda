# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Tianze
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""Logic for automatedImageDescriptions tests."""

import NvdaLib as _nvdaLib
from ChromeLib import ChromeLib as _ChromeLib
from SystemTestSpy import (
	_getLib,
)


import os
import pathlib

_chrome: _ChromeLib = _getLib("ChromeLib")


def NVDA_Caption():
	spy = _nvdaLib.getSpyLib()
	iconPath = os.path.join(
		_nvdaLib._locations.repoRoot,
		"source",
		"images",
		"nvda.ico",
	)
	url = pathlib.Path(iconPath).as_uri()

	_chrome.prepareChrome(
		f"""
		<div>
			<img src={url}>
		</div>
		""",
	)

	# locate graph to generate caption
	spy.emulateKeyPress("g")
	spy.emulateKeyPress("NVDA+windows+,")
	spy.wait_for_specific_speech(
		"at non-visual desktop access non-visual desktop access non-visual desktop access non-visual desktop access non-visual desktop access non-visual desktop access non-visual",
		maxWaitSeconds=30,
	)
