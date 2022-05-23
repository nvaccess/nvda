#appModules/win32calc.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2007-2017 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""App module for Windows Calculator (desktop version) for Windows 10 LTSB (Long-Term Servicing Branch) and Server, only difference being executable name.
"""

from .calc import *
from appModuleHandler import _warnDeprecatedAliasAppModule
_warnDeprecatedAliasAppModule()
