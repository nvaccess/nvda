# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2024 NV Access Limited

from __future__ import annotations
from typing import Type, cast
from dataclasses import dataclass
from comtypes import COMError
from . import lowLevel
from UIAHandler import UIA
from . import builder
from . import instructions
from . import operation


@dataclass
class LocalExecutionResult(operation.ExecutionResult):
	results: dict[lowLevel.OperandId, object]

	def hasOperand(self, operandId: lowLevel.OperandId) -> bool:
		return operandId in self.results

	def getOperand(self, operandId: lowLevel.OperandId) -> object:
		return self.results[operandId]


class HaltException(Exception):
	pass


class BreakLoopException(Exception):
	pass


class BadOperationStatusException(Exception):
	pass


class InstructionLimitExceededException(Exception):
	pass


@dataclass
class LocalOperationResultSet:
	_registers: dict[lowLevel.OperandId, object]
	status: int
	errorLocation: int
	extendedError: int

	def hasOperand(self, operandId: lowLevel.OperandId) -> bool:
		return operandId in self._registers

	def getOperand(self, operandId: lowLevel.OperandId) -> object:
		return self._registers[operandId]


class LocalExecutor(operation.Executor):
	_registers: dict[lowLevel.OperandId, object]
	_requestedResults: set[lowLevel.OperandId]
	_operationStatus: int = 0
	_instructions: list[builder.InstructionBase]
	_ip: int
	_instructionLoopDepth = 0
	_instructionCounter = 0
	_maxInstructions: int

	def __init__(self, maxInstructions: int = 10000):
		self._maxInstructions = maxInstructions
		self._registers = {}
		self._requestedResults = set()

	@property
	def operationStatus(self) -> int:
		return self._operationStatus

	@operationStatus.setter
	def operationStatus(self, value: int):
		self._operationStatus = value
		if value < 0:
			raise BadOperationStatusException()

	def storeRegisterValue(self, operandId: lowLevel.OperandId, value: object):
		self._registers[operandId] = value

	def fetchRegisterValue(self, operandId: lowLevel.OperandId) -> object:
		return self._registers[operandId]

	def _operationStatusFromException(self, e: Exception) -> int:
		if isinstance(e, COMError):
			return e.hresult
		elif isinstance(e, ZeroDivisionError):
			return -805306220
		else:
			return 0

	def _execute_ForkIfFalse(self, instruction: instructions.ForkIfFalse):
		condition = self._registers[instruction.condition.operandId]
		if not isinstance(condition, bool):
			raise RuntimeError(f"Expected bool, got {type(condition)}")
		if not condition:
			self._ip += instruction.branch.value
		else:
			self._ip += 1

	def _execute_NewLoopBlock(self, instruction: instructions.NewLoopBlock):
		breakAddress = self._ip + instruction.breakBranch.value
		continueAddress = self._ip + instruction.continueBranch.value
		self._ip += 1
		self._instructionLoop(
			stopInstruction=instructions.EndLoopBlock,
			breakAddress=breakAddress,
			continueAddress=continueAddress,
		)

	def _execute_NewTryBlock(self, instruction: instructions.NewTryBlock):
		self._ip += 1
		catchAddress = self._ip + instruction.catchBranch.value
		self._instructionLoop(instructions.EndTryBlock, catchAddress=catchAddress)

	def _execute_ContinueLoop(self, instruction: instructions.ContinueLoop, continueAddress: int | None):
		if continueAddress is not None:
			self._ip = continueAddress
		else:
			raise RuntimeError("ContinueLoop instruction encountered outside of loop")

	def _execute_SetOperationStatus(self, instruction: instructions.SetOperationStatus):
		self.operationStatus = cast(int, self._registers[instruction.status.operandId])
		self._ip += 1

	def _execute_GetOperationStatus(self, instruction: instructions.GetOperationStatus):
		self._registers[instruction.result.operandId] = self.operationStatus
		self._ip += 1

	def _executeInstruction(
		self,
		instruction: builder.InstructionBase,
		breakAddress: int | None = None,
		continueAddress: int | None = None,
	):
		match instruction:
			case instructions.Halt():
				raise HaltException()
			case instructions.Fork():
				self._ip += instruction.jumpTo.value
			case instructions.ForkIfFalse():
				self._execute_ForkIfFalse(instruction)
			case instructions.NewLoopBlock():
				self._execute_NewLoopBlock(instruction)
			case instructions.NewTryBlock():
				self._execute_NewTryBlock(instruction)
			case instructions.BreakLoop():
				raise BreakLoopException()
			case instructions.ContinueLoop():
				self._execute_ContinueLoop(instruction, continueAddress)
			case instructions.SetOperationStatus():
				self._execute_SetOperationStatus(instruction)
			case instructions.GetOperationStatus():
				self._execute_GetOperationStatus(instruction)
			case _:
				instruction.localExecute(self._registers)
				self._ip += 1

	def _instructionLoop(
		self,
		stopInstruction: Type[builder.InstructionBase] | None = None,
		breakAddress: int | None = None,
		continueAddress: int | None = None,
		catchAddress: int | None = None,
	):
		self._instructionLoopDepth += 1
		try:
			while self._ip < len(self._instructions):
				instruction = self._instructions[self._ip]
				self._instructionCounter += 1
				if self._maxInstructions is not None and self._instructionCounter > self._maxInstructions:
					raise InstructionLimitExceededException()
				if stopInstruction is not None and type(instruction) is stopInstruction:
					self._ip += 1
					break
				try:
					self._executeInstruction(instruction, breakAddress, continueAddress)
				except Exception as e:
					self.operationStatus = self._operationStatusFromException(e)
					raise
		except BreakLoopException:
			if breakAddress is not None:
				self._ip = breakAddress
			else:
				raise RuntimeError("BreakLoop instruction encountered outside of loop")
		except BadOperationStatusException:
			if catchAddress is not None:
				self._ip = catchAddress
			else:
				raise
		finally:
			self._instructionLoopDepth -= 1

	def importElement(self, operandId: lowLevel.OperandId, element: UIA.IUIAutomationElement):
		self._registers[operandId] = element

	def importTextRange(self, operandId: lowLevel.OperandId, textRange: UIA.IUIAutomationTextRange):
		self._registers[operandId] = textRange

	def addToResults(self, operandId: lowLevel.OperandId):
		self._requestedResults.add(operandId)

	def loadInstructions(self, rob: builder.RemoteOperationBuilder):
		self._instructions = rob.getAllInstructions()

	def execute(self) -> LocalExecutionResult:
		self._ip = 0
		self._instructionCounter = 0
		status = lowLevel.RemoteOperationStatus.Success
		try:
			self._instructionLoop()
		except HaltException:
			pass
		except InstructionLimitExceededException:
			status = lowLevel.RemoteOperationStatus.InstructionLimitExceeded
		except BadOperationStatusException:
			status = lowLevel.RemoteOperationStatus.UnhandledException
		return LocalExecutionResult(
			results={k: v for k, v in self._registers.items() if k in self._requestedResults},
			status=status,
			errorLocation=self._ip,
			extendedError=self._operationStatus,
		)
