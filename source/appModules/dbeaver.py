#appModules/dbeaver.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018 NV Access Limited, Josiel Santos

"""App module for DBeaver
This simply uses the app module for Eclipse.
"""

from .eclipse import *
from appModuleHandler import _warnDeprecatedAliasAppModule
_warnDeprecatedAliasAppModule()
