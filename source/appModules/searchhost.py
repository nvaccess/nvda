# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021 NV Access Limited, Joseph Lee
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Windows Search app module for Windows 11 (build 22000) and later.
"""

from .searchui import AppModule, StartMenuSearchField
__all__ = ["AppModule", "StartMenuSearchField"]
from appModuleHandler import _warnDeprecatedAliasAppModule
_warnDeprecatedAliasAppModule()
