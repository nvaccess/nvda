# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, tianze
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html
"""Logic for automatedImageDescriptions tests."""

import NvdaLib as _nvdaLib


def NVDA_Caption():
	spy = _nvdaLib.getSpyLib()
	# open menu to generate caption
	spy.emulateKeyPress("NVDA+n")
	spy.emulateKeyPress("NVDA+windows+,")
	spy.wait_for_specific_speech(
		"non-visual desktop access access access access access access access access access",
	)
