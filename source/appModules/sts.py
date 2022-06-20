"""App module for Spring Tool Suite
This simply uses the app module for Eclipse.
"""

from .eclipse import *
from appModuleHandler import _warnDeprecatedAliasAppModule
_warnDeprecatedAliasAppModule()
