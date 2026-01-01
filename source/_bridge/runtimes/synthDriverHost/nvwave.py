# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited.
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

# Required as sapi4 imports this symbol
WAVE_FORMAT_PCM = 1

# WavePlayer is overridden  at runtime as a proxy to NVDA.
WavePlayer = None
