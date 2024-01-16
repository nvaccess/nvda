# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2023 NV Access Limited


from typing import Type
from dataclasses import dataclass
from ctypes import (
	oledll,
	byref,
	c_void_p,
	c_long,
	c_ulong,
	c_wchar,
	c_double,
	c_bool
)
import ctypes
from comtypes.automation import VARIANT
from comtypes import GUID
import os
import enum
from UIAHandler import UIA
import NVDAHelper


class OperandId(c_ulong):

	def __eq__(self, other: object) -> bool:
		if type(other) is OperandId:
			return self.value == other.value
		return False

	def __repr__(self) -> str:
		return f"OperandId {self.value}"


class RelativeOffset(c_long):
	def __repr__(self) -> str:
		return f"RelativeOffset {self.value}"


_dll = oledll[os.path.join(NVDAHelper.versionedLibPath, "UIARemote.dll")]


class RemoteOperationResultSet:

	def __init__(self, pResults: c_void_p):
		if not pResults or not isinstance(pResults, c_void_p):
			raise RuntimeError("Invalid results pointer")
		self._pResults = pResults

	@property
	def errorLocation(self) -> int:
		val = c_long()
		_dll.remoteOpResult_getErrorLocation(self._pResults, byref(val))
		return val.value

	@property
	def extendedError(self) -> int:
		val = c_long()
		_dll.remoteOpResult_getExtendedError(self._pResults, byref(val))
		return val.value

	@property
	def status(self) -> int:
		val = c_long()
		_dll.remoteOpResult_getStatus(self._pResults, byref(val))
		return RemoteOperationStatus(val.value)

	def hasOperand(self, operandId: OperandId) -> bool:
		val = c_bool()
		_dll.remoteOpResult_hasOperand(self._pResults, operandId, byref(val))
		return val.value

	def getOperand(self, operandId: OperandId) -> VARIANT:
		val = VARIANT()
		_dll.remoteOpResult_getOperand(self._pResults, operandId, byref(val))
		return val

	def __del__(self):
		_dll.remoteOpResult_free(self._pResults)


class RemoteOperation:

	def __init__(self):
		self._pRemoteOperation = c_void_p()
		_dll.remoteOp_create(byref(self._pRemoteOperation))

	def importElement(self, operandId: OperandId, element: UIA.IUIAutomationElement):
		_dll.remoteOp_importElement(self._pRemoteOperation, operandId, element)

	def importTextRange(self, operandId: OperandId, textRange: UIA.IUIAutomationTextRange):
		_dll.remoteOp_importTextRange(self._pRemoteOperation, operandId, textRange)

	def addToResults(self, operandId: OperandId):
		_dll.remoteOp_addToResults(self._pRemoteOperation, operandId)

	def isOpcodeSupported(self, opcode: int) -> bool:
		val = c_bool()
		_dll.remoteOp_isOpcodeSupported(self._pRemoteOperation, opcode, byref(val))
		return val.value

	def execute(self, byteCodeArray: bytes):
		pResults = c_void_p()
		_dll.remoteOp_execute(self._pRemoteOperation, byteCodeArray, len(byteCodeArray), byref(pResults))
		return RemoteOperationResultSet(pResults)

	def __del__(self):
		_dll.remoteOp_free(self._pRemoteOperation)


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
	NewTryBlock = 0x0a
	EndTryBlock = 0x0b
	SetOperationStatus = 0x0c
	GetOperationStatus = 0x0d

	# Arithmetic
	Add = 0x0e
	Subtract = 0x0f
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
	BoolAnd = 0x1a
	BoolOr = 0x1b

	# Generic comparison
	Compare = 0x1c

	# New object constructors
	NewInt = 0x1d
	NewUint = 0x1e
	NewBool = 0x1f
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
	RemoteArrayAppend = 0x2a
	RemoteArraySetAt = 0x2b
	RemoteArrayRemoveAt = 0x2c
	RemoteArrayGetAt = 0x2d
	RemoteArraySize = 0x2e

	# RemoteStringMap methods
	RemoteStringMapInsert = 0x2f
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
	IsNull = 0x3a
	IsNotSupported = 0x3b
	IsMixedAttribute = 0x3c
	IsBool = 0x3d
	IsInt = 0x3e
	IsUint = 0x3f
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
	LookupId = 0x4a
	LookupGuid = 0x4b

	# Cache requests
	NewCacheRequest = 0x4c
	IsCacheRequest = 0x4d
	CacheRequestAddProperty = 0x4e
	CacheRequestAddPattern = 0x4f
	PopulateCache = 0x50

	Stringify = 0x51
	GetMetadataValue = 0x52

	# Extensibility
	CallExtension = 0x53
	IsExtensionSupported = 0x54


class ComparisonType(enum.IntEnum):
	Equal = 0
	NotEqual = 1
	GreaterThan = 2
	LessThan = 3
	GreaterThanOrEqual = 4
	LessThanOrEqual = 5


class NavigationType(enum.IntEnum):
	Parent = 0
	NextSibling = 1
	PreviousSibling = 2
	FirstChild = 3
	LastChild = 4


@dataclass
class ParamSpec:
	name: str
	ctype: Type[ctypes._SimpleCData | ctypes.Array | ctypes.Structure]


@dataclass
class InstructionSpec:
	paramSpecs: list[ParamSpec]
	finalParamRepeat: bool = False

	def __init__(
		self,
		*params: tuple[str, Type[ctypes._SimpleCData | ctypes.Array | ctypes.Structure]],
		finalParamRepeat: bool = False
	):
		self.paramSpecs = [ParamSpec(*p) for p in params]
		self.finalParamRepeat = finalParamRepeat


InstructionSpecs: dict[InstructionType, InstructionSpec] = {
	InstructionType.Nop: InstructionSpec(),
	InstructionType.Set: InstructionSpec(
		("target", OperandId),
		("source", OperandId)
	),
	InstructionType.ForkIfTrue: InstructionSpec(
		("condition", OperandId),
		("trueBranch", RelativeOffset),
	),
	InstructionType.ForkIfFalse: InstructionSpec(
		("condition", OperandId),
		("falseBranch", RelativeOffset),
	),
	InstructionType.Fork: InstructionSpec(
		("branch", RelativeOffset),
	),
	InstructionType.Halt: InstructionSpec(),
	InstructionType.NewLoopBlock: InstructionSpec(
		('break', RelativeOffset),
		('continue', RelativeOffset)
	),
	InstructionType.EndLoopBlock: InstructionSpec(),
	InstructionType.BreakLoop: InstructionSpec(),
	InstructionType.ContinueLoop: InstructionSpec(),
	InstructionType.NewTryBlock: InstructionSpec(
		('catch', RelativeOffset),
	),
	InstructionType.EndTryBlock: InstructionSpec(),
	InstructionType.SetOperationStatus: InstructionSpec(
		('result', OperandId),
		('status', c_ulong)
	),
	InstructionType.GetOperationStatus: InstructionSpec(
		('result', OperandId),
	),
	InstructionType.Add: InstructionSpec(
		('target', OperandId),
		('value', OperandId)
	),
	InstructionType.Subtract: InstructionSpec(
		('target', OperandId),
		('value', OperandId)
	),
	InstructionType.Multiply: InstructionSpec(
		('target', OperandId),
		('value', OperandId)
	),
	InstructionType.Divide: InstructionSpec(
		('target', OperandId),
		('value', OperandId)
	),
	InstructionType.BinaryAdd: InstructionSpec(
		('result', OperandId),
		('left', OperandId),
		('right', OperandId)
	),
	InstructionType.BinarySubtract: InstructionSpec(
		('result', OperandId),
		('left', OperandId),
		('right', OperandId)
	),
	InstructionType.BinaryMultiply: InstructionSpec(
		('result', OperandId),
		('left', OperandId),
		('right', OperandId)
	),
	InstructionType.BinaryDivide: InstructionSpec(
		('result', OperandId),
		('left', OperandId),
		('right', OperandId)
	),
	InstructionType.InPlaceBoolNot: InstructionSpec(
		('target', OperandId)
	),
	InstructionType.InPlaceBoolAnd: InstructionSpec(
		('target', OperandId),
		('value', OperandId)
	),
	InstructionType.InPlaceBoolOr: InstructionSpec(
		('target', OperandId),
		('value', OperandId)
	),
	InstructionType.BoolNot: InstructionSpec(
		('result', OperandId),
		('value', OperandId)
	),
	InstructionType.BoolAnd: InstructionSpec(
		('result', OperandId),
		('left', OperandId),
		('right', OperandId)
	),
	InstructionType.BoolOr: InstructionSpec(
		('result', OperandId),
		('left', OperandId),
		('right', OperandId)
	),
	InstructionType.Compare: InstructionSpec(
		('result', OperandId),
		('left', OperandId),
		('right', OperandId),
		('comparison', c_ulong)
	),
	InstructionType.NewInt: InstructionSpec(
		('result', OperandId),
		('value', c_long)
	),
	InstructionType.NewUint: InstructionSpec(
		('result', OperandId),
		('value', c_ulong)
	),
	InstructionType.NewBool: InstructionSpec(
		('result', OperandId),
		('value', c_bool)
	),
	InstructionType.NewDouble: InstructionSpec(
		('result', OperandId),
		('value', c_double)
	),
	InstructionType.NewChar: InstructionSpec(
		('result', OperandId),
		('value', c_wchar)
	),
	InstructionType.NewString: InstructionSpec(
		('result', OperandId),
		('length', c_ulong),
		('value', ctypes.Array[c_wchar])
	),
	InstructionType.NewPoint: InstructionSpec(
		('result', OperandId),
		('x', c_double),
		('y', c_double)
	),
	InstructionType.NewRect: InstructionSpec(
		('result', OperandId),
		('left', c_double),
		('top', c_double),
		('width', c_double),
		('height', c_double)
	),
	InstructionType.NewArray: InstructionSpec(
		('result', OperandId)
	),
	# InstructionType.NewStringMap: InstructionSpec(),
	InstructionType.NewNull: InstructionSpec(
		('result', OperandId)
	),
	# InstructionType.GetPointProperty: InstructionSpec(),
	# InstructionType.GetRectProperty: InstructionSpec(),
	InstructionType.RemoteArrayAppend: InstructionSpec(
		('target', OperandId),
		('value', OperandId)
	),
	InstructionType.RemoteArraySetAt: InstructionSpec(
		('target', OperandId),
		('index', OperandId),
		('value', OperandId)
	),
	InstructionType.RemoteArrayRemoveAt: InstructionSpec(
		('target', OperandId),
		('index', OperandId)
	),
	InstructionType.RemoteArrayGetAt: InstructionSpec(
		('result', OperandId),
		('target', OperandId),
		('index', OperandId)
	),
	InstructionType.RemoteArraySize: InstructionSpec(
		('result', OperandId),
		('target', OperandId)
	),
	# InstructionType.RemoteStringMapInsert: InstructionSpec(),
	# InstructionType.RemoteStringMapRemove: InstructionSpec(),
	# InstructionType.RemoteStringMapHasKey: InstructionSpec(),
	# InstructionType.RemoteStringMapLookup: InstructionSpec(),
	# InstructionType.RemoteStringMapSize: InstructionSpec(),
	InstructionType.RemoteStringGetAt: InstructionSpec(
		('result', OperandId),
		('target', OperandId),
		('index', c_ulong)
	),
	InstructionType.RemoteStringSubstr: InstructionSpec(
		('result', OperandId),
		('target', OperandId),
		('start', c_ulong),
		('length', c_ulong)
	),
	InstructionType.RemoteStringConcat: InstructionSpec(
		('result', OperandId),
		('left', OperandId),
		('right', OperandId)
	),
	InstructionType.RemoteStringSize: InstructionSpec(
		('result', OperandId),
		('target', OperandId)
	),
	InstructionType.GetPropertyValue: InstructionSpec(
		('result', OperandId),
		('target', OperandId),
		('propertyId', OperandId),
		('ignoreDefault', OperandId)
	),
	InstructionType.Navigate: InstructionSpec(
		('result', OperandId),
		('target', OperandId),
		('direction', OperandId)
	),
	InstructionType.IsNull: InstructionSpec(
		('result', OperandId),
		('target', OperandId)
	),
	InstructionType.IsNotSupported: InstructionSpec(
		('result', OperandId),
		('target', OperandId)
	),
	InstructionType.IsMixedAttribute: InstructionSpec(
		('result', OperandId),
		('target', OperandId)
	),
	InstructionType.IsBool: InstructionSpec(
		('result', OperandId),
		('target', OperandId)
	),
	InstructionType.IsInt: InstructionSpec(
		('result', OperandId),
		('target', OperandId)
	),
	InstructionType.IsUint: InstructionSpec(
		('result', OperandId),
		('target', OperandId)
	),
	InstructionType.IsDouble: InstructionSpec(
		('result', OperandId),
		('target', OperandId)
	),
	InstructionType.IsChar: InstructionSpec(
		('result', OperandId),
		('target', OperandId)
	),
	InstructionType.IsString: InstructionSpec(
		('result', OperandId),
		('target', OperandId)
	),
	InstructionType.IsPoint: InstructionSpec(
		('result', OperandId),
		('target', OperandId)
	),
	InstructionType.IsRect: InstructionSpec(
		('result', OperandId),
		('target', OperandId)
	),
	InstructionType.IsArray: InstructionSpec(
		('result', OperandId),
		('target', OperandId)
	),
	InstructionType.IsStringMap: InstructionSpec(
		('result', OperandId),
		('target', OperandId)
	),
	InstructionType.IsElement: InstructionSpec(
		('result', OperandId),
		('target', OperandId)
	),
	InstructionType.NewGuid: InstructionSpec(
		('result', OperandId),
		('value', GUID)
	),
	InstructionType.IsGuid: InstructionSpec(
		('result', OperandId),
		('target', OperandId)
	),
	InstructionType.LookupId: InstructionSpec(
		('result', OperandId),
		('target', OperandId)
	),
	InstructionType.LookupGuid: InstructionSpec(
		('result', OperandId),
		('target', OperandId)
	),
	InstructionType.NewCacheRequest: InstructionSpec(
		('result', OperandId)
	),
	InstructionType.IsCacheRequest: InstructionSpec(
		('result', OperandId),
		('target', OperandId)
	),
	InstructionType.CacheRequestAddProperty: InstructionSpec(
		('target', OperandId),
		('propertyId', OperandId)
	),
	InstructionType.CacheRequestAddPattern: InstructionSpec(
		('target', OperandId),
		('patternId', OperandId)
	),
	# InstructionType.PopulateCache: InstructionSpec(),
	InstructionType.Stringify: InstructionSpec(
		('result', OperandId),
		('target', OperandId)
	),
	InstructionType.GetMetadataValue: InstructionSpec(
		('result', OperandId),
		('target', OperandId),
		('key', OperandId)
	),
	InstructionType.CallExtension: InstructionSpec(
		('target', OperandId),
		('extensionGuid', OperandId),
		('argCount', c_ulong),
		('arg', OperandId),
		finalParamRepeat=True
	),
	InstructionType.IsExtensionSupported: InstructionSpec(
		('result', OperandId),
		('target', OperandId),
		('extensionGuid', OperandId)
	)
}
