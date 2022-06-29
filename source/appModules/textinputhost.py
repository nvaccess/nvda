# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2019-2021 NV Access Limited, Joseph Lee
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""App module for Windows 10/11 Modern Keyboard aka new touch keyboard panel.
This is for 20H1 text input host window."""

# Flake8/F403: alias of Composable Shell modern keyboard app module.
from .windowsinternal_composableshell_experiences_textinput_inputapp import * # NOQA
from appModuleHandler import _warnDeprecatedAliasAppModule
_warnDeprecatedAliasAppModule()
