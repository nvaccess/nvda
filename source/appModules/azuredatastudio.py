# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 NV Access Limited, Leonard de Ruijter
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

""" App module for Azure Data Studio.
This app module inherrits from the app module for Visual Studio Code.
"""

# Ignoring Flake8 imported but unused error since appModuleHandler yet uses the import.
from .code import AppModule  # noqa: F401
from appModuleHandler import _warnDeprecatedAliasAppModule
_warnDeprecatedAliasAppModule()
