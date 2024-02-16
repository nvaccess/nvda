# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2023 NV Access Limited

from __future__ import annotations
import contextlib
from typing import (
	Type,
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
	_loggingEnabled: bool
	_remoteLog: remoteAPI.RemoteString | None = None
	_rob: builder.RemoteOperationBuilder
	_importedElements: dict[lowLevel.OperandId, UIA.IUIAutomationElement]
	_importedTextRanges: dict[lowLevel.OperandId, UIA.IUIAutomationTextRange]
	_requestedResults: list[remoteAPI.RemoteBaseObject]
	_staticOperands: list[remoteAPI.RemoteBaseObject]
	_built = False
	_executed = False

	def __init__(self, enableLogging: bool = False, localMode=False):
		self._loggingEnabled = enableLogging
		self._localMode = localMode
		if localMode:
			from .localExecute import LocalExecutor 
			self._executorClass = LocalExecutor
		self._rob = builder.RemoteOperationBuilder()
		self._importedElements = {}
		self._importedTextRanges = {}
		self._requestedResults = []
		self._staticOperands = []

	def importElement(self, element: UIA.IUIAutomationElement, operandId: lowLevel.OperandId | None = None) -> remoteAPI.RemoteElement:
		if operandId is None:
			operandId = self._rob.requestNewOperandId()
		self._importedElements[operandId] = element
		return remoteAPI.RemoteElement(self._rob, operandId)

	def importTextRange(self, textRange: UIA.IUIAutomationTextRange, operandId: lowLevel.OperandId | None = None) -> remoteAPI.RemoteTextRange:
		if operandId is None:
			operandId = self._rob.requestNewOperandId()
		self._importedTextRanges[operandId] = textRange
		return remoteAPI.RemoteTextRange(self._rob, operandId)

	def addToResults(self, *operands: remoteAPI.RemoteBaseObject):
		for operand in operands:
			self._requestedResults.append(operand)

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
		ra = remoteAPI.RemoteAPI(self, enableRemoteLogging=self._loggingEnabled)
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

	def _executeAndHandleResults(self) -> None:
		if not self._built:
			raise RuntimeError("RemoteOperation must be built before execution")
		executor = self._executorClass()
		for operandId, element in self._importedElements.items():
			executor.importElement(operandId, element)
		for operandId, textRange in self._importedTextRanges.items():
			executor.importTextRange(operandId, textRange)
		for operand in self._requestedResults:
			executor.addToResults(operand.operandId)
		executor.loadInstructions(self._rob)
		resultSet = executor.execute()
		for operand in self._requestedResults:
			operand._setExecutionResult(resultSet)
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
			if count > 1:
				self._refreshStaticInstructions()
			log.info(f"Executing RemoteOperation, try {count}")
			try:
				self._executeAndHandleResults()
				log.info("RemoteOperation executed successfully")
				yield True
				return
			except InstructionLimitExceededException:
				log.info("instruction limit exceeded")
				yield False
