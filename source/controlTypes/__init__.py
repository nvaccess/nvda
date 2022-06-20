# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2007-2021 NV Access Limited, Babbage B.V.

from .formatFields import TextPosition
from .isCurrent import IsCurrent
from .outputReason import OutputReason
from .processAndLabelStates import processAndLabelStates
from .role import Role, silentRolesOnFocus, silentValuesForRoles
from .state import State, STATES_SORTED
from .descriptionFrom import DescriptionFrom
from .roleAndStateSpecialCases import transformRoleStates
from . import deprecatedAliases
# deprecatedAliases included for backwards compatibility.
# Supress F403 - unable to detect undefined names.
# Supress F401 - imported but unused
from .deprecatedAliases import *  # noqa: F403, F401

# Override (and limit) the symbols exported by the controlTypes package
# These are the symbols available when `from controlTypes import *` is used.
# Note, deprecated aliases are exposed for backwards compatibility, using these aliases is not recommended,
# consult the deprecatedAliases module for alternatives.
__all__ = [
	"IsCurrent",
	"OutputReason",
	"processAndLabelStates",
	"Role",
	"silentRolesOnFocus",
	"silentValuesForRoles",
	"State",
	"STATES_SORTED",
	"DescriptionFrom",
	"TextPosition",
	"transformRoleStates",
	*deprecatedAliases.__all__
]
