# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited.
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import os
from comtypes import GUID
import winreg
from _bridge.clients.synthDriverHost32.synthDriver import SynthDriverProxy32
import globalVars

CLSID_TTSEnumerator = GUID("{D67C0280-C743-11cd-80E5-00AA003E4B50}")


class SynthDriver(SynthDriverProxy32):
	name = "sapi4_32"
	# Translators: Description for a speech synthesizer.
	description = _("Microsoft Speech API version 4")
	synthDriver32Path = os.path.join(globalVars.appDir, "_synthDrivers32")
	synthDriver32Name = "sapi4"

	@classmethod
	def check(cls):
		if not super().check():
			return False
		try:
			winreg.OpenKey(
				winreg.HKEY_CLASSES_ROOT,
				r"CLSID\%s" % CLSID_TTSEnumerator,
				0,
				winreg.KEY_READ | winreg.KEY_WOW64_32KEY,
			).Close()
			return True
		except WindowsError:
			return False
