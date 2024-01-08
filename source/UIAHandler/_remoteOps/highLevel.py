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


_pyTypeToRemoteType: dict[Type[object], Type[midLevel.RemoteBaseObject]] = {
	int: RemoteInt,
	bool: RemoteBool,
	str: RemoteString,
	GUID: RemoteGuid
}


class MalformedBytecodeException(RuntimeError):
	pass


@dataclass
class InstructionLimitExceededException(RuntimeError):
	results: list[object]


@dataclass
class RemoteException(RuntimeError):
	errorLocation: int
	extendedError: int
	instructionRecord: midLevel.InstructionRecord | None = None

	def __str__(self) -> str:
		message = f"extendedError {self.extendedError} at instruction {self.errorLocation}"
		if self.instructionRecord is not None:
			message += f": {self.instructionRecord}"
		return message


class ExecutionFailureException(RuntimeError):
	pass


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
	remoteLogging: bool = False
	logOperandId: midLevel.OperandId | None = None


def _addArgsToBuilder(
	rob: midLevel.RemoteOperationBuilder,
	*args: object
) -> list[midLevel.RemoteBaseObject]:
	remoteArgs = []
	for arg in args:
		remoteArg: midLevel.RemoteBaseObject
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
			remoteArg = cast(Type[midLevel.RemoteBaseObject], remoteType)(rob)
			for record in remoteArg._generateInitInstructions(arg):
				rob.addInstructionRecord(record, section="imports")
		remoteArgs.append(remoteArg)
	return remoteArgs


def _fetchAndValidateBuildCache(
	remoteFunc: Callable,
	*remoteArgs: midLevel.RemoteBaseObject,
	remoteLogging: bool = False
) -> _RemoteFuncBuildCache | None:
	buildCache = getattr(remoteFunc, '_remoteFuncBuildCache', None)
	if buildCache is not None:
		if not all(
			remoteArg.operandId == argOperandId
			for remoteArg, argOperandId in zip(remoteArgs, buildCache.argOperandIds)
		):
			log.error("Ignoring Remote function build cache: argument mismatch")
			buildCache = None
		elif buildCache.remoteLogging != remoteLogging:
			log.warning("Ignoring Remote function build cache: remoteLogging mismatch")
			buildCache = None
	return buildCache


def _buildRemoteFunc(
	rob: midLevel.RemoteOperationBuilder,
	remoteFunc: Callable,
	*remoteArgs: midLevel.RemoteBaseObject,
	remoteLogging: bool = False
) -> _RemoteFuncBuildCache:
	rfa = RemoteFuncAPI(rob)
	remoteResults = remoteFunc(rfa, *remoteArgs)
	if isinstance(remoteResults, midLevel.RemoteBaseObject):
		remoteResults = [remoteResults]
	byteCode = b''
	for sectionName in ('constants', 'main'):
		byteCode += rob.getInstructionList(sectionName).getByteCode()
	buildCache = _RemoteFuncBuildCache(
		argOperandIds=[arg.operandId for arg in remoteArgs],
		bytecode=byteCode,
		resultOperandIds=[result.operandId for result in remoteResults],
		remoteLogging=remoteLogging,
		logOperandId=rob._getLogOperandId() if remoteLogging else None
	)
	setattr(remoteFunc, '_remoteFuncBuildCache', buildCache)
	return buildCache


def _dumpRemoteLog(resultSet: lowLevel.RemoteOperationResultSet, buildCache: _RemoteFuncBuildCache):
	if buildCache.logOperandId is not None and resultSet.hasOperand(buildCache.logOperandId):
		logOutput = resultSet.getOperand(buildCache.logOperandId).value
		log.info(f"--- Remote log start ---:\n{logOutput}--- Remote log end ---")

def _getExecutionResults(resultSet: lowLevel.RemoteOperationResultSet, buildCache: _RemoteFuncBuildCache):
	results = []
	for operandId in buildCache.resultOperandIds:
		if resultSet.hasOperand(operandId):
			result = resultSet.getOperand(operandId).value
		else:
			result = None
		results.append(result)
	if len(buildCache.resultOperandIds) == 1:
		return results[0]
	return results


def execute(
	remoteFunc: Callable,
	*args: object,
	remoteLogging=False,
	dumpInstructions=False
) -> object:
	ro = lowLevel.RemoteOperation()
	rob = midLevel.RemoteOperationBuilder(ro, remoteLogging=remoteLogging)
	remoteArgs = _addArgsToBuilder(rob, *args)
	argsByteCode = rob.getInstructionList('imports').getByteCode()
	buildCache: _RemoteFuncBuildCache | None = None
	if not dumpInstructions:
		buildCache = _fetchAndValidateBuildCache(remoteFunc, *remoteArgs, remoteLogging=remoteLogging)
	if buildCache is None:
		buildCache = _buildRemoteFunc(rob, remoteFunc, *remoteArgs, remoteLogging=remoteLogging)
		if dumpInstructions:
			log.info(f"{rob.dumpInstructions()}")
	else:
		log.info("Reusing Remote function build cache")
	for operandId in buildCache.resultOperandIds:
		ro.addToResults(operandId)
	if buildCache.logOperandId is not None:
		ro.addToResults(buildCache.logOperandId)
	resultSet = ro.execute(rob._versionBytes + argsByteCode + buildCache.bytecode)
	if resultSet.status == lowLevel.RemoteOperationStatus.ExecutionFailure:
		raise ExecutionFailureException()
	elif resultSet.status == lowLevel.RemoteOperationStatus.MalformedBytecode:
		raise MalformedBytecodeException()
	if remoteLogging:
		_dumpRemoteLog(resultSet, buildCache)
	results = _getExecutionResults(resultSet, buildCache)
	if resultSet.status == lowLevel.RemoteOperationStatus.InstructionLimitExceeded:
		raise InstructionLimitExceededException(results=results)
	elif resultSet.status == lowLevel.RemoteOperationStatus.UnhandledException:
		instructionRecord = rob.lookupInstructionByGlobalIndex(resultSet.errorLocation) if dumpInstructions else None
		raise RemoteException(
			errorLocation=resultSet.errorLocation,
			extendedError=resultSet.extendedError,
			instructionRecord=instructionRecord
		)
	return results
