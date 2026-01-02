# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited.
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import os
import winreg
from _bridge.clients.synthDriverHost32.synthDriver import SynthDriverProxy32
import globalVars


class SynthDriver(SynthDriverProxy32):
	name = "sapi5_32"
	description = "Microsoft Speech API version 5 (32 bit proxy)"
	synthDriver32Path = os.path.join(globalVars.appDir, "synthDrivers32")
	synthDriver32Name = "sapi5"

	@classmethod
	def check(cls):
		if not super().check():
			return False
		try:
			winreg.OpenKey(
				winreg.HKEY_CLASSES_ROOT, r"sapi.spVoice", 0, winreg.KEY_READ | winreg.KEY_WOW64_32KEY
			).Close()
			return True
		except WindowsError:
			return False
