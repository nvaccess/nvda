# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited, Joseph Lee
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""App module for Windows 11 Calculator"""

# Renamed from Windows 10 Calculator in 2021 with the release of Windows 11.
from .calculator import AppModule, noCalculatorEntryAnnouncements
__all__ = ["AppModule", "noCalculatorEntryAnnouncements"]
from appModuleHandler import _warnDeprecatedAliasAppModule
_warnDeprecatedAliasAppModule()
