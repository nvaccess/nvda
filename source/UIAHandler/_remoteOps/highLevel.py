# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2023 NV Access Limited

from __future__ import annotations
from typing import (
	Callable,
	Type,
	TypeVar,
	Any,
	Concatenate
)
from dataclasses import dataclass
import itertools
from comtypes import GUID
from logHandler import log
from . import lowLevel
from . import midLevel
from .midLevel import (
	RemoteInt,
	RemoteBool,
)


@dataclass
class MalformedBytecodeException(RuntimeError):
	errorLocation: int
	instructionRecord: midLevel.InstructionRecord | None = None

	def __str__(self) -> str:
		message = f"\nMalformed bytes at or near instruction {self.errorLocation}"
		if self.instructionRecord is not None:
			message += f": {self.instructionRecord.dumpRecord()}"
		return message


@dataclass
class InstructionLimitExceededException(RuntimeError):
	errorLocation: int
	results: list[Any]
	instructionRecord: midLevel.InstructionRecord | None = None

	def __str__(self) -> str:
		message = f"Limit reached at instruction {self.errorLocation}"
		if self.instructionRecord is not None:
			message += f": {self.instructionRecord.dumpRecord()}"
		return message


@dataclass
class RemoteException(RuntimeError):
	errorLocation: int
	extendedError: int
	instructionRecord: midLevel.InstructionRecord | None = None

	def __str__(self) -> str:
		message = f"\nError at instruction {self.errorLocation}"
		if self.instructionRecord is not None:
			message += f": {self.instructionRecord.dumpRecord()}"
		message += f"\nextendedError {self.extendedError}"
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

	_TV_newRemoteValue = TypeVar(
		'_TV_newRemoteValue',
		bound=midLevel.RemoteValue
	)

	def _newRemoteValue(
		self,
		RemoteClass: Type[_TV_newRemoteValue],
		value: _TV_newRemoteValue | object
	) -> _TV_newRemoteValue:
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

	def newFloat(self, value: midLevel.RemoteFloat | float = 0.0) -> midLevel.RemoteFloat:
		return self._newRemoteValue(midLevel.RemoteFloat, value)

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

	def newNullElement(self):
		obj = midLevel.RemoteElement(None)
		obj.bind(self.builder)
		return obj

	def newNullTextRange(self):
		obj = midLevel.RemoteTextRange(None)
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

	@midLevel.remoteFunc
	def setOperationStatus(self, status: RemoteInt):
		self.builder.setOperationStatus(status)

	def getOperationStatus(self) -> RemoteInt:
		return self.builder.getOperationStatus()

	def halt(self):
		self.builder.halt()

	def logRuntimeMessage(self, *strings: str | midLevel.RemoteString):
		self.builder.logMessage(*strings)

	def addCompiletimeComment(self, message: str):
		self.builder.addComment(message)


@dataclass
class _RemoteFuncBuildCache:
	localArgs: list[object]
	importedOperandIds: list[midLevel.OperandId]
	bytecode: bytes
	resultOperandIds: list[midLevel.OperandId]
	logOperandId: midLevel.OperandId | None = None


def _importArguments(
	builder: midLevel.RemoteOperationBuilder,
	func: Callable,
	*args: object,
	**kwargs: object
) -> tuple[list[lowLevel.OperandId], list[object]]:
	importedOperandIds = []
	localArgs = []
	for arg in itertools.chain(args, kwargs.values()):
		if isinstance(arg, midLevel.RemoteBaseObject):
			arg.bind(builder, section='imports')
			importedOperandIds.append(arg.operandId)
		else:
			localArgs.append(arg)
	return importedOperandIds, localArgs


def _validateBuildCache(
	buildCache: _RemoteFuncBuildCache,
	importedOperandIds: list[midLevel.OperandId],
	localArgs: list[object],
	logOperandId: midLevel.OperandId | None,
) -> bool:
	if buildCache.importedOperandIds != importedOperandIds:
		log.error("Ignoring Remote function build cache: imported  arguments mismatch")
		return False
	elif buildCache.logOperandId != logOperandId:
		log.warning("Ignoring Remote function build cache: remoteLogging mismatch")
		return False
	elif buildCache.localArgs != localArgs:
		log.warning("Ignoring Remote function build cache: localArgs mismatch")
		return False
	return True


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


_execute_ReturnType = TypeVar('_execute_ReturnType')


def execute(
	remoteFunc: Callable[Concatenate[RemoteFuncAPI, ...], Any],
	*args: object,
	remoteLogging=False,
	dumpInstructions=False,
	**kwargs
) -> Any:
	ro = lowLevel.RemoteOperation()
	builder = midLevel.RemoteOperationBuilder(ro, remoteLogging=remoteLogging)
	logOperandId = builder.getLogOperandId()
	buildCache: _RemoteFuncBuildCache | None = None
	rfa = RemoteFuncAPI(builder)
	processedArgs, processedKwargs = midLevel.processArgs(remoteFunc, rfa, *args, **kwargs)
	importedOperandIds, localArgs = _importArguments(builder, remoteFunc, *processedArgs, **processedKwargs)
	importsByteCode = builder.getRecordList('imports').getByteCode()
	buildCache = getattr(remoteFunc, '_remoteFuncBuildCache', None)
	if buildCache:
		if not _validateBuildCache(
			buildCache, importedOperandIds=importedOperandIds, localArgs=localArgs, logOperandId=logOperandId
		):
			buildCache = None
	if buildCache is None:
		remoteResults = remoteFunc(rfa, *processedArgs, **processedKwargs)
		rfa.halt()
		if isinstance(remoteResults, midLevel.RemoteBaseObject):
			remoteResults = [remoteResults]
		globalsByteCode = builder.getRecordList('globals').getByteCode()
		mainByteCode = builder.getRecordList('main').getByteCode()
		buildCache = _RemoteFuncBuildCache(
			localArgs=localArgs,
			importedOperandIds=importedOperandIds,
			bytecode=globalsByteCode + mainByteCode,
			resultOperandIds=[result.operandId for result in remoteResults],
			logOperandId=logOperandId
		)
		remoteFunc._remoteFuncBuildCache = buildCache
	else:
		log.info(f"Reusing Remote function build cache for {remoteFunc.__qualname__}")
	for operandId in buildCache.resultOperandIds:
		ro.addToResults(operandId)
	if buildCache.logOperandId is not None:
		ro.addToResults(buildCache.logOperandId)
	if dumpInstructions:
		log.info(f"{builder.dumpInstructions()}")
	resultSet = ro.execute(builder._versionBytes + importsByteCode + buildCache.bytecode)
	if resultSet.status == lowLevel.RemoteOperationStatus.ExecutionFailure:
		raise ExecutionFailureException()
	instructionRecord = None
	errorLocation = resultSet.errorLocation
	if dumpInstructions and errorLocation >= 0:
		try:
			instructionRecord = builder.lookupInstructionByGlobalIndex(resultSet.errorLocation)
		except IndexError:
			pass
	if resultSet.status == lowLevel.RemoteOperationStatus.MalformedBytecode:
		raise MalformedBytecodeException(errorLocation=errorLocation, instructionRecord=instructionRecord)
	if remoteLogging:
		_dumpRemoteLog(resultSet, buildCache)
	results = _getExecutionResults(resultSet, buildCache)
	if resultSet.status == lowLevel.RemoteOperationStatus.InstructionLimitExceeded:
		raise InstructionLimitExceededException(
			errorLocation=resultSet.errorLocation, results=results, instructionRecord=instructionRecord
		)
	elif resultSet.status == lowLevel.RemoteOperationStatus.UnhandledException:
		raise RemoteException(
			errorLocation=resultSet.errorLocation,
			extendedError=resultSet.extendedError,
			instructionRecord=instructionRecord
		)
	return results
