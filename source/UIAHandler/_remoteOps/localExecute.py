# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2023 NV Access Limited

from __future__ import annotations
from typing import Type, cast
from dataclasses import dataclass
from comtypes import COMError
from . import lowLevel
from logHandler import log
from . import builder
from . import instructions


class HaltException(Exception):
	pass


class BreakLoopException(Exception):
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


class LocalExecutor:
	_registers: dict[lowLevel.OperandId, object]
	_operationStatus: int = 0
	_instructions: list[builder.InstructionBase]
	_ip: int
	_instructionLoopDepth = 0
	_instructionCounter = 0
	_maxInstructions = None

	def __init__(self, maxInstructions: int | None = None):
		self._registers = {}
		self._maxInstructions = maxInstructions

	def storeRegisterValue(self, operandId: lowLevel.OperandId, value: object):
		self._registers[operandId] = value

	def fetchRegisterValue(self, operandId: lowLevel.OperandId) -> object:
		return self._registers[operandId]

	def loadInstructions(self, instructions: list[builder.InstructionBase]):
		self._instructions = instructions.copy()
		self._ip = 0

	def _setOperationStatusFromException(self, e: Exception):
		if isinstance(e, HaltException):
			# Halting is not an error.
			return
		elif isinstance(e, COMError):
			self._operationStatus = e.hresult
		else:
			self._operationStatus = -1

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
			continueAddress=continueAddress
		)

	def _execute_NewTryBlock(self, instruction: instructions.NewTryBlock):
		self._ip += 1
		catchAddress = self._ip + instruction.catchBranch.value
		self._instructionLoop(instructions.EndTryBlock, catchAddress=catchAddress)

	def _execute_BreakLoop(self, instruction: instructions.BreakLoop, breakAddress: int | None):
		if breakAddress is not None:
			self._ip = breakAddress
			raise BreakLoopException()
		raise RuntimeError("BreakLoop instruction encountered outside of loop")

	def _execute_ContinueLoop(self, instruction: instructions.ContinueLoop, continueAddress: int | None):
		if continueAddress is not None:
			self._ip = continueAddress
		else:
			raise RuntimeError("ContinueLoop instruction encountered outside of loop")

	def _execute_SetOperationStatus(self, instruction: instructions.SetOperationStatus):
		self._operationStatus = cast(int, self._registers[instruction.status.operandId])
		self._ip += 1

	def _execute_GetOperationStatus(self, instruction: instructions.GetOperationStatus):
		self._registers[instruction.result.operandId] = self._operationStatus
		self._ip += 1

	def _executeInstruction(
		self,
		instruction: builder.InstructionBase,
		breakAddress: int | None = None,
		continueAddress: int | None = None
	):
		if type(instruction) is instructions.Halt:
			raise HaltException()
		elif type(instruction) is instructions.Fork:
			self._ip += instruction.jumpTo.value
		elif type(instruction) is instructions.ForkIfFalse:
			self._execute_ForkIfFalse(instruction)
		elif type(instruction) is instructions.NewLoopBlock:
			self._execute_NewLoopBlock(instruction)
		elif type(instruction) is instructions.NewTryBlock:
			self._execute_NewTryBlock(instruction)
		elif type(instruction) is instructions.BreakLoop:
			self._execute_BreakLoop(instruction, breakAddress)
		elif type(instruction) is instructions.ContinueLoop:
			self._execute_ContinueLoop(instruction, continueAddress)
		elif type(instruction) is instructions.SetOperationStatus:
			self._execute_SetOperationStatus(instruction)
		elif type(instruction) is instructions.GetOperationStatus:
			self._execute_GetOperationStatus(instruction)
		else:
			instruction.localExecute(self._registers)
			self._ip += 1

	def _instructionLoop(
		self,
		stopInstruction: Type[builder.InstructionBase] | None = None,
		breakAddress: int | None = None,
		continueAddress: int | None = None,
		catchAddress: int | None = None
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
				self._executeInstruction(instruction, breakAddress, continueAddress)
		except InstructionLimitExceededException:
			raise
		except HaltException:
			pass
		except BreakLoopException:
			pass
		except Exception as e:
			if catchAddress is not None:
				self._ip = catchAddress
			self._setOperationStatusFromException(e)
			log.error("Exception during local execution", exc_info=True)
		finally:
			self._instructionLoopDepth -= 1

	def execute(self):
		self._ip = 0
		status = lowLevel.RemoteOperationStatus.Success
		try:
			self._instructionLoop()
		except InstructionLimitExceededException:
			status = lowLevel.RemoteOperationStatus.InstructionLimitExceeded
		else:
			if self._operationStatus != 0:
				status = lowLevel.RemoteOperationStatus.UnhandledException
		return LocalOperationResultSet(
			_registers=self._registers,
			status=status,
			errorLocation=self._ip,
			extendedError=self._operationStatus
		)
