# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited.
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

# The following symbols are required by SAPI5.
# However they do nothing.
# Currently audio is generated directly from the runtime using WASAPI,
# So even if audio ducking was proxied to NVDA,
# NVDA would inappropriately duck the runtime which is not what is wanted.
# The work around would be to broker all audio from the runtime via NVDA.


def _isDebug():
	return False


def isAudioDuckingSupported():
	return False


class AudioDucker:
	pass
