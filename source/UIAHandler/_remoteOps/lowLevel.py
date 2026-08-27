# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2025 NV Access Limited

from __future__ import annotations
import re
from ctypes import (
	oledll,
	byref,
	c_void_p,
	c_long,
	c_ulong,
	c_bool,
)
from comtypes.automation import VARIANT
import enum
import NVDAState
from UIAHandler import UIA
from ._lowLevel import RemoteOperation
from . import _lowLevel

"""
This module contains classes and constants for the low-level Windows UI Automation Remote Operations API,
i.e. Windows.UI.UIAutomation.core.
The low-level UI Automation Remote Operations API is a binary API
that allows for the execution of special byte code specific to UI Automation,
allowing for the execution of multiple UI Automation operations in a remote provider,
via one cross-process call.
"""


_re_COMMethodVtableOffset = re.compile("^<COM method offset (\d+):")
def _getCOMMethodVtableOffset(COMMethod):
	m = _re_COMMethodVtableOffset.match(str(COMMethod))
	if not m:
		raise ValueError(f"Invalid COM method: {COMMethod}")
	return int(m.group(1))

def _makeUIAPatternInstructionId(patternId, COMMethod) -> int:
	vtableOffset = _getCOMMethodVtableOffset(COMMethod)
	return (patternId << 10) | vtableOffset

class OperandId(c_ulong):
	"""
	An operand ID is a unique identifier for an operand (or register) in the remote operation VM.
	It is an unsigned 32 bit integer.
	"""

	def __eq__(self, other: object) -> bool:
		if type(other) is OperandId:
			return self.value == other.value
		return False

	def __repr__(self) -> str:
		return f"OperandId {self.value}"

	def __hash__(self) -> int:
		return hash(self.value)


class RelativeOffset(c_long):
	"""
	A relative offset is a signed 32 bit integer that represents an offset from the current instruction pointer.
	"""

	def __repr__(self) -> str:
		return f"RelativeOffset {self.value}"


_dll = oledll[NVDAState.ReadPaths.UIARemoteDll]


class RemoteOperationStatus(enum.IntEnum):
	Success = 0
	MalformedBytecode = 1
	InstructionLimitExceeded = 2
	UnhandledException = 3
	ExecutionFailure = 4


class InstructionType(enum.IntEnum):
	Nop = 0x00
	Set = 0x01

	# Control flow
	ForkIfTrue = 0x02
	ForkIfFalse = 0x03
	Fork = 0x04
	Halt = 0x05

	# Loops
	NewLoopBlock = 0x06
	EndLoopBlock = 0x07
	BreakLoop = 0x08
	ContinueLoop = 0x09

	# Error handling
	NewTryBlock = 0x0A
	EndTryBlock = 0x0B
	SetOperationStatus = 0x0C
	GetOperationStatus = 0x0D

	# Arithmetic
	Add = 0x0E
	Subtract = 0x0F
	Multiply = 0x10
	Divide = 0x11
	BinaryAdd = 0x12
	BinarySubtract = 0x13
	BinaryMultiply = 0x14
	BinaryDivide = 0x15

	# Boolean operators
	InPlaceBoolNot = 0x16
	InPlaceBoolAnd = 0x17
	InPlaceBoolOr = 0x18

	BoolNot = 0x19
	BoolAnd = 0x1A
	BoolOr = 0x1B

	# Generic comparison
	Compare = 0x1C

	# New object constructors
	NewInt = 0x1D
	NewUint = 0x1E
	NewBool = 0x1F
	NewDouble = 0x20
	NewChar = 0x21
	NewString = 0x22
	NewPoint = 0x23
	NewRect = 0x24
	NewArray = 0x25
	NewStringMap = 0x26
	NewNull = 0x27

	# Point and Rect methods
	GetPointProperty = 0x28
	GetRectProperty = 0x29

	# RemoteArray methods
	RemoteArrayAppend = 0x2A
	RemoteArraySetAt = 0x2B
	RemoteArrayRemoveAt = 0x2C
	RemoteArrayGetAt = 0x2D
	RemoteArraySize = 0x2E

	# RemoteStringMap methods
	RemoteStringMapInsert = 0x2F
	RemoteStringMapRemove = 0x30
	RemoteStringMapHasKey = 0x31
	RemoteStringMapLookup = 0x32
	RemoteStringMapSize = 0x33

	# RemoteString methods
	RemoteStringGetAt = 0x34
	RemoteStringSubstr = 0x35
	RemoteStringConcat = 0x36
	RemoteStringSize = 0x37

	# UIA element methods
	GetPropertyValue = 0x38
	Navigate = 0x39

	# Type interrogation methods
	IsNull = 0x3A
	IsNotSupported = 0x3B
	IsMixedAttribute = 0x3C
	IsBool = 0x3D
	IsInt = 0x3E
	IsUint = 0x3F
	IsDouble = 0x40
	IsChar = 0x41
	IsString = 0x42
	IsPoint = 0x43
	IsRect = 0x44
	IsArray = 0x45
	IsStringMap = 0x46
	IsElement = 0x47

	# GUID support
	NewGuid = 0x48
	IsGuid = 0x49
	LookupId = 0x4A
	LookupGuid = 0x4B

	# Cache requests
	NewCacheRequest = 0x4C
	IsCacheRequest = 0x4D
	CacheRequestAddProperty = 0x4E
	CacheRequestAddPattern = 0x4F
	PopulateCache = 0x50

	Stringify = 0x51
	GetMetadataValue = 0x52

	# Extensibility
	CallExtension = 0x53
	IsExtensionSupported = 0x54

	# text ranges
	TextRangeClone = 0x271E0103
	TextRangeCompare = 0x271E0104
	TextRangeCompareEndpoints = 0x271E0105
	TextRangeExpandToEnclosingUnit = 0x271E0106
	TextRangeFindAttribute = 0x271E0107
	TextRangeFindText = 0x271E0108
	TextRangeGetAttributeValue = 0x271E0109
	TextRangeGetBoundingRectangles = 0x271E010A
	TextRangeGetEnclosingElement = 0x271E010B
	TextRangeGetText = 0x271E010C
	TextRangeMove = 0x271E010D
	TextRangeMoveEndpointByUnit = 0x271E010E
	TextRangeMoveEndpointByRange = 0x271E010F
	TextRangeSelect = 0x271E0110
	TextRangeAddToSelection = 0x271E0111
	TextRangeRemoveFromSelection = 0x271E0112
	TextRangeScrollIntoView = 0x271E0113
	TextRangeGetChildren = 0x271E0114
	TextRangeShowContextMenu = 0x271E0115

	# Text pattern
	ElementGetTextPattern = UIA.UIA_TextPatternId
	TextPatternRangeFromChild = _makeUIAPatternInstructionId(UIA.UIA_TextPatternId, UIA.IUIAutomationTextPattern.RangeFromChild)


class ComparisonType(enum.IntEnum):
	Equal = 0
	NotEqual = 1
	GreaterThan = 2
	LessThan = 3
	GreaterThanOrEqual = 4
	LessThanOrEqual = 5


class NavigationDirection(enum.IntEnum):
	Parent = 0
	NextSibling = 1
	PreviousSibling = 2
	FirstChild = 3
	LastChild = 4


class TextUnit(enum.IntEnum):
	Character = 0
	Format = 1
	Word = 2
	Line = 3
	Paragraph = 4
	Page = 5
	Document = 6


class TextPatternRangeEndpoint(enum.IntEnum):
	Start = 0
	End = 1


class AutomationIdentifierType(enum.IntEnum):
	Property = 0
	Pattern = 1
	Event = 2
	ControlType = 3
	TextAttribute = 4
	LandmarkType = 5
	Annotation = 6
	Changes = 7
	Style = 8

PropertyId = enum.IntEnum(
	"PropertyId",
	{k[4:-10]: v for k, v in vars(UIA).items() if k.endswith("PropertyId")},
)


PatternId = enum.IntEnum(
	"PatternId",
	{k[4:-9]: v for k, v in vars(UIA).items() if k.endswith("PatternId")},
)


AttributeId = enum.IntEnum(
	"AttributeId",
	{k[4:-11]: v for k, v in vars(UIA).items() if k.endswith("AttributeId")},
)

StyleId = enum.IntEnum(
	"StyleId",
	{k[8:]: v for k, v in vars(UIA).items() if k.startswith("StyleId")},
)
