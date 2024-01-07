# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2023 NV Access Limited

import enum
from dataclasses import dataclass
from typing import Callable, cast, Type
from comtypes import GUID
from UIAHandler import UIA
from logHandler import log
from . import lowLevel
from . import midLevel
from .midLevel import (
	RemoteInt,
	RemoteBool,
	RemoteString,
	RemoteVariant,
	RemoteExtensionTarget,
	RemoteElement,
	RemoteTextRange,
	RemoteGuid
)


_pyTypeToRemoteType: dict[Type[object], Type[midLevel._RemoteBaseObject]] = {
	int: RemoteInt,
	bool: RemoteBool,
	str: RemoteString,
	GUID: RemoteGuid
}


class RemoteFuncAPI:

	def __init__(self, rob: midLevel.RemoteOperationBuilder):
		self._rob = rob

	def newInt(self, initialValue: int = 0) -> RemoteInt:
		return RemoteInt._new(self._rob, initialValue)

	def newBool(self, initialValue: bool = False) -> RemoteBool:
		return RemoteBool._new(self._rob, initialValue)

	def newString(self, initialValue: str = "") -> RemoteString:
		return RemoteString._new(self._rob, initialValue)

	def newNULLVariant(self) -> RemoteVariant:
		return RemoteVariant._new(self._rob)

	def newNULLExtensionTarget(self) -> RemoteExtensionTarget:
		return RemoteExtensionTarget._new(self._rob)

	def newNULLElement(self) -> RemoteElement:
		return RemoteElement._new(self._rob)

	def newNULLTextRange(self) -> RemoteTextRange:
		return RemoteTextRange._new(self._rob)

	def newGuid(self, initialValue: GUID) -> RemoteGuid:
		return RemoteGuid._new(self._rob, initialValue)

	def ifBlock(self, condition: midLevel.RemoteBool):
		return self._rob.ifBlock(condition)

	def elseBlock(self):
		return self._rob.elseBlock()

	def whileBlock(self, conditionBuilderFunc: Callable[[], RemoteBool]):
		return self._rob.whileBlock(conditionBuilderFunc)

	def breakLoop(self):
		self._rob.breakLoop()

	def continueLoop(self):
		self._rob.continueLoop()

	def tryBlock(self):
		return self._rob.tryBlock()

	def catchBlock(self):
		return self._rob.catchBlock()

	def setOperationStatus(self, status: int | RemoteInt):
		self._rob.setOperationStatus(status)

	def getOperationStatus(self) -> RemoteInt:
		return self._rob.getOperationStatus()

	def halt(self):
		self._rob.halt()

	def logMessage(self, *strings):
		self._rob.logMessage(*strings)


@dataclass
class _RemoteFuncBuildCache:
	argOperandIds: list[midLevel.OperandId]
	bytecode: bytes
	resultOperandIds: list[midLevel.OperandId]
	logOperandId: midLevel.OperandId | None = None


def _addArgsToBuilder(
	rob: midLevel.RemoteOperationBuilder,
	*args: object
) -> list[midLevel._RemoteBaseObject]:
	remoteArgs = []
	for arg in args:
		remoteArg: midLevel._RemoteBaseObject
		if isinstance(arg, UIA.IUIAutomationElement):
			remoteArg = rob.importElement(arg)
		elif isinstance(arg, UIA.IUIAutomationTextRange):
			remoteArg = rob.importTextRange(arg)
		else:
			if isinstance(arg, enum.Enum):
				arg = arg.value
			remoteType = _pyTypeToRemoteType.get(type(arg))
			if remoteType is None:
				raise TypeError(f"Unsupported argument type: {type(arg)}")
			remoteArg = cast(Type[midLevel._RemoteBaseObject], remoteType)(rob)
			for record in remoteArg._generateInitInstructions(arg):
				rob.addInstructionRecord(record, section="imports")
		remoteArgs.append(remoteArg)
	return remoteArgs


def _fetchAndValidateBuildCache(
	remoteFunc: Callable,
	*remoteArgs: midLevel._RemoteBaseObject
) -> _RemoteFuncBuildCache | None:
	buildCache = getattr(remoteFunc, '_remoteFuncBuildCache', None)
	if buildCache is not None:
		if not all(
			remoteArg.operandId == argOperandId
			for remoteArg, argOperandId in zip(remoteArgs, buildCache.argOperandIds)
		):
			log.error("Ignoring Remote function build cache: argument mismatch")
			buildCache = None
	return buildCache


def _buildRemoteFunc(
	rob: midLevel.RemoteOperationBuilder,
	remoteFunc: Callable,
	*remoteArgs: midLevel._RemoteBaseObject,
	enableLogging: bool = False
) -> _RemoteFuncBuildCache:
	rfa = RemoteFuncAPI(rob)
	remoteResults = remoteFunc(rfa, *remoteArgs)
	if isinstance(remoteResults, midLevel._RemoteBaseObject):
		remoteResults = [remoteResults]
	if enableLogging:
		log.info(f"{rob.dumpInstructions()}")
	byteCode = b''
	for sectionName in ('constants', 'main'):
		byteCode += rob.getInstructionList(sectionName).getByteCode()
	buildCache = _RemoteFuncBuildCache(
		argOperandIds=[arg.operandId for arg in remoteArgs],
		bytecode=byteCode,
		resultOperandIds=[result.operandId for result in remoteResults],
		logOperandId=rob._getLogOperandId()
	)
	setattr(remoteFunc, '_remoteFuncBuildCache', buildCache)
	return buildCache


def _dumpExecutionLog(rox: midLevel.RemoteOperationExecutor):
	log.info(
		"--- Execution log start ---:\n"
		f"{rox.getLogOutput()}"
		"--- Execution log end ---"
	)


def _getExecutionResults(rox: midLevel.RemoteOperationExecutor, buildCache: _RemoteFuncBuildCache):
	if len(buildCache.resultOperandIds) == 1:
		return rox.getResult(buildCache.resultOperandIds[0])
	return tuple(rox.getResult(operandId) for operandId in buildCache.resultOperandIds)


def execute(remoteFunc: Callable, *args: object, enableLogging=False) -> object:
	ro = lowLevel.RemoteOperation()
	rob = midLevel.RemoteOperationBuilder(ro, enableLogging=enableLogging)
	remoteArgs = _addArgsToBuilder(rob, *args)
	argsByteCode = rob.getInstructionList('imports').getByteCode()
	buildCache = _fetchAndValidateBuildCache(remoteFunc, *remoteArgs)
	if buildCache is None:
		buildCache = _buildRemoteFunc(rob, remoteFunc, *remoteArgs, enableLogging=enableLogging)
	else:
		log.info("Using Remote function build cache")
	rox = midLevel.RemoteOperationExecutor(ro)
	for operandId in buildCache.resultOperandIds:
		rox.addToResults(operandId)
	if buildCache.logOperandId is not None:
		rox.setLogOperandId(buildCache.logOperandId)
	try:
		rox.execute(argsByteCode + buildCache.bytecode)
	finally:
		if enableLogging:
			_dumpExecutionLog(rox)
	return _getExecutionResults(rox, buildCache)
