# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2023 NV Access Limited

from __future__ import annotations
import contextlib
from typing import (
	TypeVar,
	ParamSpec,
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
class RemoteOperationException(RuntimeError):
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


class ExecutionFailureException(RemoteOperationException):
		pass


class MalformedBytecodeException(RemoteOperationException):
	pass


class InstructionLimitExceededException(RemoteOperationException):
	pass


class UnhandledRemoteException(RemoteOperationException):
	pass


_remoteFunc_paramSpec = ParamSpec('_remoteFunc_paramSpec')
_remoteFunc_return = TypeVar('_remoteFunc_return', bound=remoteAPI.RemoteBaseObject | tuple[remoteAPI.RemoteBaseObject, ...])


class RemoteOperation:
	_remoteLoggingEnabled: bool
	_ro:  lowLevel.RemoteOperation
	_rob: builder.RemoteOperationBuilder
	_requestedResults: list[remoteAPI.RemoteBaseObject]
	_isConnectionBound = False
	_built = False
	_executed = False

	def __init__(self, enableRemoteLogging: bool = False):
		self._remoteLoggingEnabled = enableRemoteLogging
		self._ro = lowLevel.RemoteOperation()
		self._rob = builder.RemoteOperationBuilder()
		self._requestedResults = []

	def importElement(self, element: UIA.IUIAutomationElement) -> remoteAPI.RemoteElement:
		operandId = self._rob.requestNewOperandId()
		self._ro.importElement(operandId, element)
		self._rob.getInstructionList('imports').addMetaCommand(f"import element into {operandId}")
		self._isConnectionBound = True
		return remoteAPI.RemoteElement(self._rob, operandId)

	def importTextRange(self, textRange: UIA.IUIAutomationTextRange) -> remoteAPI.RemoteTextRange:
		operandId = self._rob.requestNewOperandId()
		self._ro.importTextRange(operandId, textRange)
		self._rob.getInstructionList('imports').addMetaCommand(f"import textRange into {operandId}")
		self._isConnectionBound = True
		return remoteAPI.RemoteTextRange(self._rob, operandId)

	def addToResults(self, *operands: remoteAPI.RemoteBaseObject):
		for operand in operands:
			self._ro.addToResults(operand.operandId)
			self._requestedResults.append(operand)

	@contextlib.contextmanager
	def buildContext(self):
		if self._built:
			raise RuntimeError("RemoteOperation cannot be built more than once")
		if not self._isConnectionBound:
			raise RuntimeError("RemoteOperation must be bound to a connection before building")
		ra = remoteAPI.RemoteAPI(self._rob, enableRemoteLogging=self._remoteLoggingEnabled)
		log.info("building RemoteOperation:")
		yield ra
		ra.halt()
		log.info(
			"RemoteOperation built.\n"
			"--- Instructions Start ---\n"
			f"{self._rob.dumpInstructions()}"
			"--- Instructions End ---"
		)
		self._built = True

	def _execute(self) -> None:
		if not self._built:
			raise RuntimeError("RemoteOperation must be built before execution")
		byteCode = self._rob.getByteCode()
		resultSet = self._ro.execute(byteCode)
		for operand in self._requestedResults:
			operand._setResultSet(resultSet)
		if resultSet.status == lowLevel.RemoteOperationStatus.ExecutionFailure:
			raise ExecutionFailureException()
		instructionRecord = None
		errorLocation = resultSet.errorLocation
		if errorLocation >= 0:
			try:
				instructionRecord = self._rob.lookupInstructionByGlobalIndex(errorLocation)
			except (IndexError, RuntimeError):
				pass
		if resultSet.status == lowLevel.RemoteOperationStatus.MalformedBytecode:
			raise MalformedBytecodeException(errorLocation=errorLocation, instructionRecord=instructionRecord)
		if resultSet.status == lowLevel.RemoteOperationStatus.InstructionLimitExceeded:
			raise InstructionLimitExceededException(
				errorLocation=resultSet.errorLocation,
				instructionRecord=instructionRecord,
			)
		elif resultSet.status == lowLevel.RemoteOperationStatus.UnhandledException:
			raise UnhandledRemoteException(
				errorLocation=resultSet.errorLocation,
				extendedError=resultSet.extendedError,
				instructionRecord=instructionRecord,
			)

	def execute(self):
		log.info("Executing RemoteOperation")
		self._execute()

	def executeUntilSuccess(self, maxTries: int = 100) -> Iterable[bool]:
		count = 0
		for count in range(1, maxTries + 1):
			log.info(f"Executing RemoteOperation, try {count}")
			try:
				self._execute()
				log.info("RemoteOperation executed successfully")
				yield True
				return
			except InstructionLimitExceededException:
				log.info("instruction limit exceeded")
				yield False
