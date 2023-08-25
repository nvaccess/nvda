# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2019 NV Access Limited, Joseph Lee
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Windows Search app module for Windows 10 build 18965 and later.
"""

# Flake8/F403: this is an alias for SearchUI app module.
from .searchui import * # NOQA
from appModuleHandler import _warnDeprecatedAliasAppModule
_warnDeprecatedAliasAppModule()
