# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2023 NV Access Limited

from __future__ import annotations
from typing import Callable, Type, TypeVar
from dataclasses import dataclass
from comtypes import GUID
from logHandler import log
from . import lowLevel
from . import midLevel
from .midLevel import (
	RemoteInt,
	RemoteBool,
)


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


class RemoteFuncAPI(midLevel._RemoteBase):

	def __init__(self, builder: midLevel.RemoteOperationBuilder):
		self.bind(builder)

	_TV_newRemoteObject = TypeVar('_TV_newRemoteObject', bound=midLevel.RemoteBaseObject)
	def _newRemoteObject(self, RemoteClass: Type[_TV_newRemoteObject]) -> _TV_newRemoteObject:
		obj = RemoteClass()
		obj.bind(self.builder)
		return obj

	_TV_newRemoteValue = TypeVar('_TV_newRemoteValue', bound=midLevel.RemoteValue)
	def _newRemoteValue(self, RemoteClass: Type[_TV_newRemoteValue], value: _TV_newRemoteValue | object) -> _TV_newRemoteValue:
		if isinstance(value, RemoteClass):
			value.bind(self.builder)
			return value.copy()
		obj = RemoteClass(value)
		obj.bind(self.builder)
		return obj

	def newUint(self, value: midLevel.RemoteUint | int = 0) -> midLevel.RemoteUint:
		return self._newRemoteValue(midLevel.RemoteUint, value)

	def newInt(self, value: midLevel.RemoteInt | int = 0) -> midLevel.RemoteInt:
		return self._newRemoteValue(midLevel.RemoteInt, value)

	def newString(self, value: str = "") -> midLevel.RemoteString: 
		return self._newRemoteValue(midLevel.RemoteString, value)

	def newBool(self, value: bool = False) -> midLevel.RemoteBool:
		return self._newRemoteValue(midLevel.RemoteBool, value)

	def newGuid(self, value: GUID | str = "") -> midLevel.RemoteGuid:
		return self._newRemoteValue(midLevel.RemoteGuid, value)

	def newVariant(self) -> midLevel.RemoteVariant:
		return self._newRemoteObject(midLevel.RemoteVariant)

	def newArray(self):
		obj = midLevel.RemoteArray()
		obj.bind(self.builder)
		return obj

	def ifBlock(self, condition: midLevel.RemoteBool):
		return self.builder.ifBlock(condition)

	def elseBlock(self):
		return self.builder.elseBlock()

	def whileBlock(self, conditionBuilderFunc: Callable[[], RemoteBool]):
		return self.builder.whileBlock(conditionBuilderFunc)

	def breakLoop(self):
		self.builder.breakLoop()

	def continueLoop(self):
		self.builder.continueLoop()

	def tryBlock(self):
		return self.builder.tryBlock()

	def catchBlock(self):
		return self.builder.catchBlock()

	def setOperationStatus(self, status: RemoteInt):
		self.builder.setOperationStatus(status)

	def getOperationStatus(self) -> RemoteInt:
		return self.builder.getOperationStatus()

	def halt(self):
		self.builder.halt()

	def logMessage(self, *strings: str | midLevel.RemoteString):
		self.builder.logMessage(*strings)


@dataclass
class _RemoteFuncBuildCache:
	argOperandIds: list[midLevel.OperandId]
	bytecode: bytes
	resultOperandIds: list[midLevel.OperandId]
	remoteLogging: bool = False
	logOperandId: midLevel.OperandId | None = None

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
	builder: midLevel.RemoteOperationBuilder,
	remoteFunc: Callable,
	*remoteArgs: midLevel.RemoteBaseObject,
	remoteLogging: bool = False
) -> _RemoteFuncBuildCache:
	rfa = RemoteFuncAPI(builder)
	remoteResults = remoteFunc(rfa, *remoteArgs)
	if isinstance(remoteResults, midLevel.RemoteBaseObject):
		remoteResults = [remoteResults]
	byteCode = b''
	for sectionName in ('constants', 'main'):
		byteCode += builder.getInstructionList(sectionName).getByteCode()
	buildCache = _RemoteFuncBuildCache(
		argOperandIds=[arg.operandId for arg in remoteArgs],
		bytecode=byteCode,
		resultOperandIds=[result.operandId for result in remoteResults],
		remoteLogging=remoteLogging,
		logOperandId=builder._getLogOperandId() if remoteLogging else None
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
	*args: midLevel.RemoteBaseObject,
	remoteLogging=False,
	dumpInstructions=False,
) -> object:
	ro = lowLevel.RemoteOperation()
	builder = midLevel.RemoteOperationBuilder(ro, remoteLogging=remoteLogging)
	for arg in args:
		arg.bind(builder, section="imports")
	argsByteCode = builder.getInstructionList('imports').getByteCode()
	buildCache: _RemoteFuncBuildCache | None = None
	if not dumpInstructions:
		buildCache = _fetchAndValidateBuildCache(remoteFunc, *args, remoteLogging=remoteLogging)
	if buildCache is None:
		buildCache = _buildRemoteFunc(builder, remoteFunc, *args, remoteLogging=remoteLogging)
		if dumpInstructions:
			log.info(f"{builder.dumpInstructions()}")
	else:
		log.info("Reusing Remote function build cache")
	for operandId in buildCache.resultOperandIds:
		ro.addToResults(operandId)
	if buildCache.logOperandId is not None:
		ro.addToResults(buildCache.logOperandId)
	resultSet = ro.execute(builder._versionBytes + argsByteCode + buildCache.bytecode)
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
		instructionRecord = builder.lookupInstructionByGlobalIndex(resultSet.errorLocation) if dumpInstructions else None
		raise RemoteException(
			errorLocation=resultSet.errorLocation,
			extendedError=resultSet.extendedError,
			instructionRecord=instructionRecord
		)
	return results
