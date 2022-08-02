# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020-2021 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html


"""Types used in IAccessibleHander.
Kept here so they can be re-used without having to worry about circular imports.
"""
import enum
from typing import Tuple

IAccessibleObjectIdentifierType = Tuple[
	int,  # windowHandle
	int,  # objectID
	int,  # childID
]


# IAccessible2 relations (not included in the typelib)
@enum.unique
class RelationType(str, enum.Enum):
	FLOWS_FROM = "flowsFrom"
	FLOWS_TO = "flowsTo"
	CONTAINING_DOCUMENT = "containingDocument"
	DETAILS = "details"
	DETAILS_FOR = "detailsFor"
