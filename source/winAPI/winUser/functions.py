# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited, Cyrille Bougot
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from ctypes import windll
from .constants import SysColorIndex


# dll handles
user32 = windll.user32


def GetSysColor(index: SysColorIndex):
	return user32.GetSysColor(index)
