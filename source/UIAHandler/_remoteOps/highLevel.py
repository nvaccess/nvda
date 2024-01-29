# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2023 NV Access Limited

from __future__ import annotations
import inspect
from typing import (
	Callable,
	TypeVar,
	Any,
	Concatenate,
	ParamSpec
)
from dataclasses import dataclass
from logHandler import log
from . import lowLevel
from . import midLevel


@dataclass
class MalformedBytecodeException(RuntimeError):
	errorLocation: int
	instructionRecord: midLevel.Instruction | None = None

	def __str__(self) -> str:
		message = f"\nMalformed bytes at or near instruction {self.errorLocation}"
		if self.instructionRecord is not None:
			message += f": {self.instructionRecord.dumpInstruction()}"
		return message


@dataclass
class InstructionLimitExceededException(RuntimeError):
	errorLocation: int
	results: list[Any]
	instructionRecord: midLevel.Instruction | None = None

	def __str__(self) -> str:
		message = f"Limit reached at instruction {self.errorLocation}"
		if self.instructionRecord is not None:
			message += f": {self.instructionRecord.dumpInstruction()}"
		return message


@dataclass
class RemoteException(RuntimeError):
	errorLocation: int
	extendedError: int
	instructionRecord: midLevel.Instruction | None = None

	def __str__(self) -> str:
		message = f"\nError at instruction {self.errorLocation}"
		if self.instructionRecord is not None:
			message += f": {self.instructionRecord.dumpInstruction()}"
		message += f"\nextendedError {self.extendedError}"
		return message


class ExecutionFailureException(RuntimeError):
	pass


@dataclass
class _RemoteFuncBuildCache:
	metaArgsString: str
	importedOperandIds: dict[str, midLevel.OperandId]
	globalsByteCode: bytes
	mainByteCode: bytes
	resultOperandIds: list[midLevel.OperandId]
	logOperandId: midLevel.OperandId | None = None


_remoteFunc_paramSpec = ParamSpec('_remoteFunc_paramSpec')
_remoteFunc_return = TypeVar('_remoteFunc_return')

def _importArguments(
	builder: midLevel.RemoteOperationBuilder,
	func: Callable[Concatenate[midLevel.RemoteAPI, _remoteFunc_paramSpec], object],
	ra: midLevel.RemoteAPI,
	*args: _remoteFunc_paramSpec.args,
	**kwargs: _remoteFunc_paramSpec.kwargs
) -> tuple[dict[str, lowLevel.OperandId], str]:
	funcSig = inspect.signature(func)
	boundSig = funcSig.bind(ra, *args, **kwargs)
	boundSig.apply_defaults()
	importedArgs: dict[str, midLevel.RemoteBaseObject] = {}
	metaArgs: dict[str, object] = {}
	for index, (name, val) in enumerate(boundSig.arguments.items()):
		if index == 0:
			# Skip ra
			continue
		if isinstance(val, midLevel.RemoteBaseObject):
			val.bind(builder, builder._getNewOperandId())
			val._initOperand("imports")
			importedArgs[name] = val
		else:
			metaArgs[name] = val
	if metaArgs:
		output = "Meta arguments:\n"
		output += "\n".join(
			f"{name} = {val}" for name, val in metaArgs.items()
		)
		log.info(output)
	if importedArgs:
		output = "Imported arguments:\n"
		output += "\n".join(
			f"{name} = {val.operandId}" for name, val in importedArgs.items()
		)
		log.info(output)
	return (
		{name: val.operandId for name, val in importedArgs.items()},
		str(metaArgs)
	)


def _validateBuildCache(
	buildCache: _RemoteFuncBuildCache,
	importedOperandIds: dict[str, midLevel.OperandId],
	metaArgsString: str,
	logOperandId: midLevel.OperandId | None,
) -> bool:
	if buildCache.importedOperandIds != importedOperandIds:
		log.error("Ignoring Remote function build cache: imported  arguments mismatch")
		return False
	elif buildCache.logOperandId != logOperandId:
		log.warning("Ignoring Remote function build cache: remoteLogging mismatch")
		return False
	elif buildCache.metaArgsString != metaArgsString:
		log.error("Ignoring Remote function build cache: meta arguments mismatch")
		return False
	return True


def _buildRemotefunction(
	builder: midLevel.RemoteOperationBuilder,
	remoteFunc: Callable[Concatenate[midLevel.RemoteAPI, _remoteFunc_paramSpec], object],
	ra: midLevel.RemoteAPI,
	*args: _remoteFunc_paramSpec.args,
	**kwargs: _remoteFunc_paramSpec.kwargs
) -> _RemoteFuncBuildCache:
	log.info(f"Building Remote function {remoteFunc.__qualname__}")
	importedOperandIds, metaArgsString = _importArguments(builder, remoteFunc, ra, *args, **kwargs)
	logOperandId = builder.getLogOperandId()
	buildCacheAttrName = f"_remoteFuncBuildCache_{metaArgsString}"
	buildCache = getattr(remoteFunc, buildCacheAttrName, None)
	if buildCache:
		if not _validateBuildCache(
			buildCache, importedOperandIds=importedOperandIds, metaArgsString=metaArgsString, logOperandId=logOperandId
		):
			buildCache = None
	if buildCache is None:
		remoteResult = remoteFunc(ra, *args, **kwargs)
		ra.halt()
		remoteResults = []
		if isinstance(remoteResult, (tuple, list)):
			remoteResults.extend(remoteResult)
		else:
			remoteResults.append(remoteResult)
		log.info(
			"--- Instructions Start ---\n"
			f"{builder.dumpInstructions()}"
			"--- Instructions End ---"
		)
		globals = builder.getInstructionList('globals')
		main = builder.getInstructionList('main')
		buildCache = _RemoteFuncBuildCache(
			metaArgsString=metaArgsString,
			importedOperandIds=importedOperandIds,
			globalsByteCode=globals.getByteCode(),
			mainByteCode=main.getByteCode(),
			resultOperandIds=[result.operandId for result in remoteResults],
			logOperandId=logOperandId
		)
		setattr(remoteFunc, buildCacheAttrName, buildCache)
	else:
		log.info(f"Reusing Remote function build cache {buildCacheAttrName}")
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


# _execute_ReturnType = TypeVar('_execute_ReturnType')


def execute(
	remoteFunc: Callable[Concatenate[midLevel.RemoteAPI, _remoteFunc_paramSpec], object],
	*args: _remoteFunc_paramSpec.args,
	**kwargs: _remoteFunc_paramSpec.kwargs
) -> Any:
	ro = lowLevel.RemoteOperation()
	builder = midLevel.RemoteOperationBuilder(ro, remoteLogging=False)
	ra = midLevel.RemoteAPI(builder)
	buildCache = _buildRemotefunction(builder, remoteFunc, ra, *args, **kwargs)
	for operandId in buildCache.resultOperandIds:
		ro.addToResults(operandId)
	if buildCache.logOperandId is not None:
		ro.addToResults(buildCache.logOperandId)
	importsByteCode = builder.getInstructionList('imports').getByteCode()
	globalsByteCode = buildCache.globalsByteCode
	mainByteCode = buildCache.mainByteCode
	resultSet = ro.execute(builder._versionBytes + importsByteCode + globalsByteCode + mainByteCode)
	if resultSet.status == lowLevel.RemoteOperationStatus.ExecutionFailure:
		raise ExecutionFailureException()
	instructionRecord = None
	errorLocation = resultSet.errorLocation
	if errorLocation >= 0:
		try:
			instructionRecord = builder.lookupInstructionByGlobalIndex(resultSet.errorLocation)
		except (IndexError, RuntimeError):
			pass
	if resultSet.status == lowLevel.RemoteOperationStatus.MalformedBytecode:
		raise MalformedBytecodeException(errorLocation=errorLocation, instructionRecord=instructionRecord)
	if builder._loggingEnablede :
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
