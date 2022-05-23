"""App module for Zend Eclipse PHP Developer Tools
This simply uses the app module for Eclipse.
"""

from .eclipse import *
from appModuleHandler import _warnDeprecatedAliasAppModule
_warnDeprecatedAliasAppModule()
