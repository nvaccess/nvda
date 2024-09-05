# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2024 NV Access Limited

"""
This package contains all the instructions that can be executed by the remote ops framework.
Each instruction contains the appropriate op code and parameter types.
Most instructions also contain a `localExecute` method,
which provides an implementation of the instruction that can be executed locally.
"""


# Import all instructions so that they can be accessed as attributes of this module.
# flake8: noqa: F401

from ..builder import InstructionBase
from .arithmetic import (
	BinaryAdd,
	BinarySubtract,
	BinaryMultiply,
	BinaryDivide,
	InplaceAdd,
	InplaceSubtract,
	InplaceMultiply,
	InplaceDivide,
)
from .array import (
	NewArray,
	IsArray,
	ArrayAppend,
	ArrayGetAt,
	ArrayRemoveAt,
	ArraySetAt,
	ArraySize,
)
from .bool import (
	NewBool,
	IsBool,
	BoolNot,
	BoolAnd,
	BoolOr,
)
from .controlFlow import (
	Halt,
	Fork,
	ForkIfFalse,
	NewLoopBlock,
	EndLoopBlock,
	NewTryBlock,
	EndTryBlock,
	BreakLoop,
	ContinueLoop,
)
from .element import (
	IsElement,
	ElementGetPropertyValue,
	ElementNavigate,
)
from .extension import (
	IsExtensionSupported,
	CallExtension,
)
from .float import (
	NewFloat,
	IsFloat,
)
from .general import (
	Set,
	Compare,
)
from .guid import (
	NewGuid,
	IsGuid,
)
from .int import (
	NewInt,
	IsInt,
	NewUint,
	IsUint,
)
from .null import (
	NewNull,
	IsNull,
)
from .status import (
	SetOperationStatus,
	GetOperationStatus,
)
from .string import (
	NewString,
	IsString,
	StringConcat,
	Stringify,
)
from .textRange import (
	TextRangeGetText,
	TextRangeMove,
	TextRangeMoveEndpointByUnit,
	TextRangeCompare,
	TextRangeClone,
	TextRangeFindAttribute,
	TextRangeFindText,
	TextRangeGetAttributeValue,
	TextRangeGetBoundingRectangles,
	TextRangeGetEnclosingElement,
	TextRangeExpandToEnclosingUnit,
	TextRangeMoveEndpointByRange,
	TextRangeCompareEndpoints,
)
