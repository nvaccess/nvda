#appModules/esybraille.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2016-2018 Didier Poitou (Eurobraille), Babbage B.V.

"""App module for Esybraille
This imports the esysuite appModule,
"""

from .esysuite import *
from appModuleHandler import _warnDeprecatedAliasAppModule
_warnDeprecatedAliasAppModule()
