"""App module for Miranda IM for Windows x64
This simply uses the miranda32 app module.
"""

from .miranda32 import *
from appModuleHandler import _warnDeprecatedAliasAppModule
_warnDeprecatedAliasAppModule()
