# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2019 NV Access Limited, Łukasz Golonka
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

""" App module for Spring Tool Suite version 4
This simply uses the app module for Eclipse.
"""

# Normally these Flake8 errors shouldn't be ignored but here we are simply reusing existing ap module.

from .eclipse import *  # noqa: F401, F403
from appModuleHandler import _warnDeprecatedAliasAppModule
_warnDeprecatedAliasAppModule()
