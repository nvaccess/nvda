# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2023 NV Access Limited

from __future__ import annotations
import contextlib
from typing import (
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
from . import localExecute


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


class Operation:
	_loggingEnabled: bool
	_remoteLog: remoteAPI.RemoteString | None = None
	_rob: builder.RemoteOperationBuilder
	_requestedResults: list[remoteAPI.RemoteBaseObject]
	_isConnectionBound = False
	_built = False
	_executed = False

	def __init__(self, enableLogging: bool = False):
		self._loggingEnabled = enableLogging
		self._rob = builder.RemoteOperationBuilder()
		self._requestedResults = []

	def _importElement(self, operandId: lowLevel.OperandId, element: UIA.IUIAutomationElement):
		raise NotImplementedError

	def importElement(self, element: UIA.IUIAutomationElement) -> remoteAPI.RemoteElement:
		operandId = self._rob.requestNewOperandId()
		self._importElement(operandId, element)
		self._rob.getInstructionList('imports').addMetaCommand(f"import element into {operandId}")
		self._isConnectionBound = True
		return remoteAPI.RemoteElement(self._rob, operandId)

	def _importTextRange(self, operandId: lowLevel.OperandId, textRange: UIA.IUIAutomationTextRange):
		raise NotImplementedError

	def importTextRange(self, textRange: UIA.IUIAutomationTextRange) -> remoteAPI.RemoteTextRange:
		operandId = self._rob.requestNewOperandId()
		self._importTextRange(operandId, textRange)
		self._rob.getInstructionList('imports').addMetaCommand(f"import textRange into {operandId}")
		self._isConnectionBound = True
		return remoteAPI.RemoteTextRange(self._rob, operandId)

	def _addToResults(self, operand: remoteAPI.RemoteBaseObject):
		raise NotImplementedError

	def addToResults(self, *operands: remoteAPI.RemoteBaseObject):
		for operand in operands:
			self._addToResults(operand)
			self._requestedResults.append(operand)
			self._rob.getInstructionList('main').addMetaCommand(f"add result {operand}")

	@contextlib.contextmanager
	def buildContext(self):
		if self._built:
			raise RuntimeError("RemoteOperation cannot be built more than once")
		if not self._isConnectionBound:
			raise RuntimeError("RemoteOperation must be bound to a connection before building")
		ra = remoteAPI.RemoteAPI(self._rob, enableRemoteLogging=self._loggingEnabled)
		self._remoteLog = logObj = ra.getLogObject()
		if logObj is not None:
			self.addToResults(logObj)
		yield ra
		ra.halt()
		if self._loggingEnabled:
			log.info(
				"RemoteOperation built.\n"
				"--- Instructions Start ---\n"
				f"{self._rob.dumpInstructions()}"
				"--- Instructions End ---"
			)
		self._built = True

	def _execute(self):
		raise NotImplementedError

	def _executeAndHandleResults(self) -> None:
		if not self._built:
			raise RuntimeError("RemoteOperation must be built before execution")
		resultSet = self._execute()
		for operand in self._requestedResults:
			operand._setResultSet(resultSet)
		if resultSet.status == lowLevel.RemoteOperationStatus.ExecutionFailure:
			raise ExecutionFailureException()
		instructionRecord = None
		errorLocation = resultSet.errorLocation
		if errorLocation >= 0:
			instructions = self._rob.getAllInstructions()
			try:
				instructionRecord = instructions[errorLocation]
			except (IndexError, RuntimeError):
				pass
		if resultSet.status == lowLevel.RemoteOperationStatus.MalformedBytecode:
			raise MalformedBytecodeException(errorLocation=errorLocation, instructionRecord=instructionRecord)
		if self._remoteLog is not None:
			logOutput = self._remoteLog.localValue
			log.info(
				"--- remote log start ---\n"
				f"{logOutput}"
				"--- remote log end ---"
			)
		if resultSet.status == lowLevel.RemoteOperationStatus.InstructionLimitExceeded:
			raise InstructionLimitExceededException(
				errorLocation=resultSet.errorLocation,
				instructionRecord=instructionRecord,
			)
		elif resultSet.status == lowLevel.RemoteOperationStatus.UnhandledException:
			raise UnhandledException(
				errorLocation=resultSet.errorLocation,
				extendedError=resultSet.extendedError,
				instructionRecord=instructionRecord,
			)

	def execute(self):
		log.info("Executing RemoteOperation")
		self._executeAndHandleResults()

	def executeUntilSuccess(self, maxTries: int = 100) -> Iterable[bool]:
		count = 0
		for count in range(1, maxTries + 1):
			log.info(f"Executing RemoteOperation, try {count}")
			try:
				self._executeAndHandleResults()
				log.info("RemoteOperation executed successfully")
				yield True
				return
			except InstructionLimitExceededException:
				log.info("instruction limit exceeded")
				yield False


@dataclass
class OperationResult:
	status: int
	errorLocation: int
	extendedError: int
	hasOperand: Callable[[lowLevel.OperandId], bool]
	getOperand: Callable[[lowLevel.OperandId], object]


class RemoteOperation(Operation):
	_ro: lowLevel.RemoteOperation

	def __init__(self, enableLogging: bool = False):
		super().__init__(enableLogging)
		self._ro = lowLevel.RemoteOperation()

	def _importElement(self, operandId: lowLevel.OperandId, element: UIA.IUIAutomationElement):
		self._ro.importElement(operandId, element)

	def _importTextRange(self, operandId: lowLevel.OperandId, textRange: UIA.IUIAutomationTextRange):
		self._ro.importTextRange(operandId, textRange)

	def _addToResults(self, operand: remoteAPI.RemoteBaseObject):
		self._ro.addToResults(operand.operandId)

	def _execute(self):
		byteCode = self._rob.getByteCode()
		resultSet = self._ro.execute(byteCode)
		return OperationResult(
			status=resultSet.status,
			errorLocation=resultSet.errorLocation,
			extendedError=resultSet.extendedError,
			hasOperand=resultSet.hasOperand,
			getOperand=resultSet.getOperand
		)


class LocalOperation(Operation):
	_executor: localExecute.LocalExecutor

	def __init__(self, enableLogging: bool = False):
		super().__init__(enableLogging)
		self._executor = localExecute.LocalExecutor()

	def _importElement(self, operandId: lowLevel.OperandId, element: UIA.IUIAutomationElement):
		self._executor.storeRegisterValue(operandId, element)

	def _importTextRange(self, operandId: lowLevel.OperandId, textRange: UIA.IUIAutomationTextRange):
		self._executor.storeRegisterValue(operandId, textRange)

	def _addToResults(self, operand: remoteAPI.RemoteBaseObject):
		return

	def _execute(self):
		instructions = self._rob.getAllInstructions()
		self._executor.loadInstructions(instructions)
		resultSet = self._executor.execute()
		return OperationResult(
			status=resultSet.status,
			errorLocation=resultSet.errorLocation,
			extendedError=resultSet.extendedError,
			hasOperand=resultSet.hasOperand,
			getOperand=resultSet.getOperand
		)
