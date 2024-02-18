# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2023 NV Access Limited

from __future__ import annotations
import contextlib
from typing import (
	Type,
	Any,
	Generator,
	Callable,
	Iterable
)
from dataclasses import dataclass
from logHandler import log
from UIAHandler import UIA
from . import lowLevel
from . import builder
from . import remoteAPI
from . import instructions


@dataclass
class ExecutionResult:
	status: int
	errorLocation: int
	extendedError: int

	def hasOperand(self, operandId: lowLevel.OperandId) -> bool:
		raise NotImplementedError

	def getOperand(self, operandId: lowLevel.OperandId) -> remoteAPI.RemoteBaseObject:
		raise NotImplementedError


class Executor:

	def importElement(self, operandId: lowLevel.OperandId, element: UIA.IUIAutomationElement):
		raise NotImplementedError

	def importTextRange(self, operandId: lowLevel.OperandId, textRange: UIA.IUIAutomationTextRange):
		raise NotImplementedError

	def addToResults(self, operandId: lowLevel.OperandId):
		raise NotImplementedError

	def loadInstructions(self, rob: builder.RemoteOperationBuilder):
		raise NotImplementedError

	def execute(self) -> ExecutionResult:
		raise NotImplementedError


@dataclass
class OperationException(RuntimeError):
	errorLocation: int | None = None
	extendedError: int | None = None
	instructionRecord: instructions.InstructionBase | None = None
	result: remoteAPI.RemoteBaseObject | tuple[remoteAPI.RemoteBaseObject, ...] | None = None

	def __str__(self) -> str:
		message = ""
		if self.errorLocation:
			message += f"\nat instruction {self.errorLocation}"
		if self.instructionRecord is not None:
			message += f": {self.instructionRecord.dumpInstruction()}"
		if self.extendedError:
			message += f"\nextendedError {self.extendedError}"
		return message


class ExecutionFailureException(OperationException):
		pass


class MalformedBytecodeException(OperationException):
	pass


class InstructionLimitExceededException(OperationException):
	pass


class UnhandledException(OperationException):
	pass


class NoReturnException(Exception):
	pass


@dataclass
class RemoteExecutionResult(ExecutionResult):
	resultSet: lowLevel.RemoteOperationResultSet

	def hasOperand(self, operandId: lowLevel.OperandId) -> bool:
		return self.resultSet.hasOperand(operandId)

	def getOperand(self, operandId: lowLevel.OperandId) -> object:
		return self.resultSet.getOperand(operandId)


class RemoteExecutor(Executor):
	_ro: lowLevel.RemoteOperation
	_isConnectionBound = False
	_byteCode: bytes = b""

	def __init__(self):
		self._ro = lowLevel.RemoteOperation()

	def importElement(self, operandId: lowLevel.OperandId, element: UIA.IUIAutomationElement):
		self._ro.importElement(operandId, element)
		self._isConnectionBound = True

	def importTextRange(self, operandId: lowLevel.OperandId, textRange: UIA.IUIAutomationTextRange):
		self._ro.importTextRange(operandId, textRange)
		self._isConnectionBound = True

	def addToResults(self, operandId: lowLevel.OperandId):
		self._ro.addToResults(operandId)

	def loadInstructions(self, rob: builder.RemoteOperationBuilder):
		self._byteCode = rob.getByteCode()

	def execute(self) -> ExecutionResult:
		if not self._isConnectionBound:
			raise RuntimeError("RemoteExecutor must be bound to a connection before execution")
		resultSet = self._ro.execute(self._byteCode)
		return RemoteExecutionResult(
			status=resultSet.status,
			errorLocation=resultSet.errorLocation,
			extendedError=resultSet.extendedError,
			resultSet=resultSet
		)


class Operation:
	_executorClass: Type[Executor] = RemoteExecutor
	_compiletimeLoggingEnabled: bool
	_runtimeLoggingEnabled: bool
	_remoteLog: remoteAPI.RemoteString | None = None
	_rob: builder.RemoteOperationBuilder
	_importedElements: dict[lowLevel.OperandId, UIA.IUIAutomationElement]
	_importedTextRanges: dict[lowLevel.OperandId, UIA.IUIAutomationTextRange]
	_requestedResults: dict[lowLevel.OperandId, remoteAPI.RemoteBaseObject]
	_staticOperands: list[remoteAPI.RemoteBaseObject]
	_returnIdOperand: remoteAPI.RemoteInt | None = None
	_yieldListOperand: remoteAPI.RemoteArray | None = None
	_built = False
	_executed = False

	def __init__(
		self,
		enableCompiletimeLogging: bool = False,
		enableRuntimeLogging: bool = False,
		localMode=False
	):
		self._compiletimeLoggingEnabled = enableCompiletimeLogging
		self._runtimeLoggingEnabled = enableRuntimeLogging
		self._localMode = localMode
		if localMode:
			from .localExecute import LocalExecutor
			self._executorClass = LocalExecutor
		self._rob = builder.RemoteOperationBuilder()
		self._importedElements = {}
		self._importedTextRanges = {}
		self._requestedResults = {}
		self._staticOperands = []

	def importElement(
		self,
		element: UIA.IUIAutomationElement,
		operandId: lowLevel.OperandId | None = None
	) -> remoteAPI.RemoteElement:
		if operandId is None:
			operandId = self._rob.requestNewOperandId()
		self._importedElements[operandId] = element
		self._rob.getDefaultInstructionList().addMetaCommand(
			f"importElement into {operandId}, value  {element}"
		)
		return remoteAPI.RemoteElement(self._rob, operandId)

	def importTextRange(
		self,
		textRange: UIA.IUIAutomationTextRange,
		operandId: lowLevel.OperandId | None = None
	) -> remoteAPI.RemoteTextRange:
		if operandId is None:
			operandId = self._rob.requestNewOperandId()
		self._importedTextRanges[operandId] = textRange
		self._rob.getDefaultInstructionList().addMetaCommand(
			f"importTextRange into {operandId}, value  {textRange}"
		)
		return remoteAPI.RemoteTextRange(self._rob, operandId)

	def addToResults(self, *operands: remoteAPI.RemoteBaseObject):
		for operand in operands:
			self._requestedResults[operand.operandId] = operand

	def _registerStaticOperand(self, operand: remoteAPI.RemoteBaseObject):
		self._staticOperands.append(operand)
		self.addToResults(operand)

	def _refreshStaticInstructions(self):
		with self._rob.overrideDefaultSection('static'):
			self._rob.getDefaultInstructionList().clear()
			for operand in self._staticOperands:
				if isinstance(operand, remoteAPI.RemoteElement):
					localElement = operand.localValue
					if not localElement:
						remoteAPI.RemoteNull.createNew(self._rob, operandId=operand.operandId)
					else:
						self.importElement(operand.localValue, operandId=operand.operandId)
				elif isinstance(operand, remoteAPI.RemoteTextRange):
					localTextRange = operand.localValue
					if not localTextRange:
						remoteAPI.RemoteNull.createNew(self._rob, operandId=operand.operandId)
					else:
						self.importTextRange(operand.localValue, operandId=operand.operandId)
				else:
					type(operand).createNew(self._rob, initialValue=operand.localValue, operandId=operand.operandId)

	@contextlib.contextmanager
	def buildContext(self):
		if self._built:
			raise RuntimeError("RemoteOperation cannot be built more than once")
		ra = remoteAPI.RemoteAPI(self, enableRemoteLogging=self._runtimeLoggingEnabled)
		self._remoteLog = logObj = ra.getLogObject()
		if logObj is not None:
			self.addToResults(logObj)
		yield ra
		ra.halt()
		if self._compiletimeLoggingEnabled:
			log.info(
				"RemoteOperation built.\n"
				"--- Instructions Start ---\n"
				f"{self._rob.dumpInstructions()}"
				"--- Instructions End ---"
			)
		self._built = True

	def buildFunction(
		self,
		func: Callable[[remoteAPI.RemoteAPI], None]
	) -> Operation:
		with self.buildContext() as ra:
			self._returnIdOperand = ra.newInt(-1)
			self.addToResults(self._returnIdOperand)
			func(ra)
		return self

	def buildIterableFunction(
		self,
		func: Callable[[remoteAPI.RemoteAPI], None]
	) -> Operation:
		with self.buildContext() as ra:
			self._yieldListOperand = ra.newArray()
			self.addToResults(self._yieldListOperand)
			func(ra)
		return self

	def _handleExecutionResult(self, executionResult: ExecutionResult):
		for operand in self._requestedResults.values():
			operand._setExecutionResult(executionResult)
		shouldDumpInstructions = False
		try:
			if executionResult.status == lowLevel.RemoteOperationStatus.ExecutionFailure:
				shouldDumpInstructions = True
				raise ExecutionFailureException()
			instructionRecord = None
			errorLocation = executionResult.errorLocation
			if errorLocation >= 0:
				instructions = self._rob.getAllInstructions()
				try:
					instructionRecord = instructions[errorLocation]
				except (IndexError, RuntimeError):
					pass
			if executionResult.status == lowLevel.RemoteOperationStatus.MalformedBytecode:
				shouldDumpInstructions = True
				raise MalformedBytecodeException(errorLocation=errorLocation, instructionRecord=instructionRecord)
			if self._remoteLog is not None:
				logOutput = self._remoteLog.localValue
				if logOutput:
					log.info(
						"--- remote log start ---\n"
						f"{logOutput}"
						"--- remote log end ---"
					)
			if executionResult.status == lowLevel.RemoteOperationStatus.InstructionLimitExceeded:
				raise InstructionLimitExceededException(
					errorLocation=executionResult.errorLocation,
					instructionRecord=instructionRecord,
				)
			elif executionResult.status == lowLevel.RemoteOperationStatus.UnhandledException:
				shouldDumpInstructions = True
				raise UnhandledException(
					errorLocation=executionResult.errorLocation,
					extendedError=executionResult.extendedError,
					instructionRecord=instructionRecord,
				)
		finally:
			if shouldDumpInstructions:
				log.info(
					"--- Instructions Start ---\n"
					f"{self._rob.dumpInstructions()}"
					"--- Instructions End ---"
				)

	def _execute(self) -> ExecutionResult:
		if not self._built:
			raise RuntimeError("RemoteOperation must be built before execution")
		executor = self._executorClass()
		for operandId, element in self._importedElements.items():
			executor.importElement(operandId, element)
		for operandId, textRange in self._importedTextRanges.items():
			executor.importTextRange(operandId, textRange)
		for operandId in self._requestedResults:
			executor.addToResults(operandId)
		executor.loadInstructions(self._rob)
		executionResult = executor.execute()
		self._handleExecutionResult(executionResult)
		return executionResult

	def execute(self) -> Any:
		self._execute()
		if self._returnIdOperand is None:
			raise RuntimeError("RemoteOperation has no return operand")
		returnId = self._returnIdOperand.localValue
		if returnId < 0:
			raise NoReturnException()
		return self._requestedResults[lowLevel.OperandId(returnId)].localValue

	def executeUntilSuccess(self, maxTries: int = 100) -> Iterable[bool]:
		count = 0
		while True:
			count += 1
			if count > 1:
				self._refreshStaticInstructions()
			try:
				return self.execute()
			except InstructionLimitExceededException:
				if count == maxTries:
					raise

	def iterExecute(self) -> Generator[Any, None, None]:
		if self._yieldListOperand is None:
			raise RuntimeError("RemoteOperation has no yield list operand")
		instructionLimit = None
		try:
			self._execute()
		except InstructionLimitExceededException as e:
			instructionLimit = e
		for value in self._yieldListOperand.localValue:
			yield value
		if instructionLimit is not None:
			raise instructionLimit

	def iterExecuteUntilSuccess(self, maxTries: int = 100) -> Generator[Any, None, None]:
		count = 0
		while True:
			count += 1
			if count > 1:
				self._refreshStaticInstructions()
			try:
				yield from self.iterExecute()
				return
			except InstructionLimitExceededException:
				if count == maxTries:
					raise
