# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2024 NV Access Limited


from __future__ import annotations
from typing import (
	Type,
	Any,
	Callable,
	Generator,
	TypeVar,
	cast,
)
import contextlib
from comtypes import (
	GUID,
)
from UIAHandler import UIA
from .lowLevel import RelativeOffset
from . import instructions
from . import builder
from .remoteFuncWrapper import (
	remoteContextManager,
)
from . import operation
from .remoteTypes import (
	RemoteBaseObject,
	RemoteVariant,
	RemoteBool,
	RemoteIntBase,
	RemoteInt,
	RemoteUint,
	RemoteFloat,
	RemoteString,
	RemoteGuid,
	RemoteArray,
	RemoteElement,
	RemoteTextRange,
)


class RemoteAPI(builder._RemoteBase):
	_op: operation.Operation
	_rob: builder.RemoteOperationBuilder
	_logObj: RemoteString | None = None

	def __init__(self, op: operation.Operation, enableRemoteLogging: bool = False):
		super().__init__(op._rob)
		self._op = op
		self._logObj = self.newString() if enableRemoteLogging else None

	def Return(self, *values: RemoteBaseObject | int | float | str | bool | None):
		remoteValues = [RemoteBaseObject.ensureRemote(self.rob, value) for value in values]
		if len(remoteValues) == 1:
			remoteValue = remoteValues[0]
		else:
			remoteValue = self.newArray()
			self.addCompiletimeComment(
				f"Created {remoteValue} for returning values {remoteValues}",
			)
			for value in remoteValues:
				remoteValue.append(value)
		if self._op._returnIdOperand is None:
			raise RuntimeError("ReturnIdOperand not set not created")
		self._op.addToResults(remoteValue)
		self.addCompiletimeComment(
			f"Returning {remoteValue}",
		)
		self._op._returnIdOperand.set(remoteValue.operandId.value)
		self.halt()

	def Yield(self, *values: RemoteBaseObject | int | float | str | bool | None):
		self.addCompiletimeComment(f"Begin yield {values}")
		remoteValues = [RemoteBaseObject.ensureRemote(self.rob, value) for value in values]
		if len(remoteValues) == 1:
			remoteValue = remoteValues[0]
		else:
			remoteValue = self.newArray()
			self.addCompiletimeComment(
				f"Created {remoteValue} for yielding values {remoteValues}",
			)
			for value in remoteValues:
				remoteValue.append(value)
		if self._op._yieldListOperand is None:
			raise RuntimeError("YieldIdOperand not set not created")
		self._op.addToResults(remoteValue)
		self.addCompiletimeComment(f"Yielding {remoteValue}")
		self._op._yieldListOperand.append(remoteValue)

	_newObject_RemoteType = TypeVar("_newObject_RemoteType", bound=RemoteBaseObject)

	def _newObject(
		self,
		RemoteType: Type[_newObject_RemoteType],
		value: Any,
		static: bool = False,
	) -> _newObject_RemoteType:
		section = "static" if static else "main"
		with self.rob.overrideDefaultSection(section):
			obj = RemoteType.createNew(self.rob, value)
		if static:
			self._op._registerStaticOperand(obj)
		return obj

	def newUint(self, value: int = 0, static: bool = False) -> RemoteUint:
		return self._newObject(RemoteUint, value, static=static)

	def newInt(self, value: int = 0, static: bool = False) -> RemoteInt:
		return self._newObject(RemoteInt, value, static=static)

	def newFloat(self, value: float = 0.0, static: bool = False) -> RemoteFloat:
		return self._newObject(RemoteFloat, value, static=static)

	def newString(self, value: str = "", static: bool = False) -> RemoteString:
		return self._newObject(RemoteString, value, static=static)

	def newBool(self, value: bool = False, static: bool = False) -> RemoteBool:
		return self._newObject(RemoteBool, value, static=static)

	def newGuid(self, value: GUID | str | None = None, static: bool = False) -> RemoteGuid:
		if value is None:
			realValue = GUID()
		elif isinstance(value, str):
			realValue = GUID(value)
		else:
			realValue = value
		return self._newObject(RemoteGuid, realValue, static=static)

	def newVariant(self) -> RemoteVariant:
		return RemoteVariant.createNew(self.rob)

	def newArray(self) -> RemoteArray:
		return RemoteArray.createNew(self.rob)

	def newElement(
		self,
		value: UIA.IUIAutomationElement | None = None,
		static: bool = False,
	) -> RemoteElement:
		section = "static" if static else "main"
		with self.rob.overrideDefaultSection(section):
			if value is not None:
				obj = self._op.importElement(value)
				if static:
					self._op._registerStaticOperand(obj)
				return obj
			else:
				return self._newObject(RemoteElement, value, static=static)

	def newTextRange(
		self,
		value: UIA.IUIAutomationTextRange | None = None,
		static: bool = False,
	) -> RemoteTextRange:
		section = "static" if static else "main"
		with self.rob.overrideDefaultSection(section):
			if value is not None:
				obj = self._op.importTextRange(value)
				obj = obj.clone()
				if static:
					self._op._registerStaticOperand(obj)
				return obj
			else:
				return self._newObject(RemoteTextRange, value, static=static)

	def getOperationStatus(self) -> RemoteInt:
		instructionList = self.rob.getDefaultInstructionList()
		result = RemoteInt(self.rob, self.rob.requestNewOperandId())
		instructionList.addInstruction(
			instructions.GetOperationStatus(
				result=result,
			),
		)
		return result

	def setOperationStatus(self, status: RemoteInt | int):
		instructionList = self.rob.getDefaultInstructionList()
		instructionList.addInstruction(
			instructions.SetOperationStatus(
				status=RemoteInt.ensureRemote(self.rob, status),
			),
		)

	_scopeInstructionJustExited: instructions.InstructionBase | None = None

	@contextlib.contextmanager
	def ifBlock(self, condition: RemoteBool, silent: bool = False):
		instructionList = self.rob.getDefaultInstructionList()
		conditionInstruction = instructions.ForkIfFalse(
			condition=condition,
			branch=RelativeOffset(1),  # offset updated after yield
		)
		conditionInstructionIndex = instructionList.addInstruction(conditionInstruction)
		if not silent:
			instructionList.addComment("If block body")
		yield
		if not silent:
			instructionList.addComment("End of if block body")
		nextInstructionIndex = instructionList.getInstructionCount()
		conditionInstruction.branch = RelativeOffset(nextInstructionIndex - conditionInstructionIndex)
		self._scopeInstructionJustExited = conditionInstruction

	@contextlib.contextmanager
	def elseBlock(self, silent: bool = False):
		scopeInstructionJustExited = self._scopeInstructionJustExited
		if not isinstance(scopeInstructionJustExited, instructions.ForkIfFalse):
			raise RuntimeError("Else block not directly preceded by If block")
		instructionList = self.rob.getDefaultInstructionList()
		ifConditionInstruction = cast(instructions.ForkIfFalse, scopeInstructionJustExited)
		# add a final jump instruction to the previous if block to skip over the else block.
		if not silent:
			instructionList.addComment("Jump over else block")
		jumpElseInstruction = instructions.Fork(RelativeOffset(1))  # offset updated after yield
		jumpElseInstructionIndex = instructionList.addInstruction(jumpElseInstruction)
		# increment the false offset of the previous if block to take the new jump instruction into account.
		ifConditionInstruction.branch.value += 1
		if not silent:
			instructionList.addComment("Else block body")
		yield
		if not silent:
			instructionList.addComment("End of else block body")
		# update the jump instruction to jump to the real end of the else block.
		nextInstructionIndex = instructionList.getInstructionCount()
		jumpElseInstruction.jumpTo = RelativeOffset(nextInstructionIndex - jumpElseInstructionIndex)
		self._scopeInstructionJustExited = None

	def continueLoop(self):
		instructionList = self.rob.getDefaultInstructionList()
		instructionList.addInstruction(instructions.ContinueLoop())

	def breakLoop(self):
		instructionList = self.rob.getDefaultInstructionList()
		instructionList.addInstruction(instructions.BreakLoop())

	@contextlib.contextmanager
	def whileBlock(self, conditionBuilderFunc: Callable[[], RemoteBool], silent: bool = False):
		instructionList = self.rob.getDefaultInstructionList()
		# Add a new loop block instruction to start the while loop
		loopBlockInstruction = instructions.NewLoopBlock(
			breakBranch=RelativeOffset(1),  # offset updated after yield
			continueBranch=RelativeOffset(1),
		)
		loopBlockInstructionIndex = instructionList.addInstruction(loopBlockInstruction)
		# generate the loop condition.
		# This must be evaluated lazily via a callable
		# because any instructions that produce the condition bool
		# must be added inside the loop block,
		# so that the condition is fully re-evaluated on each iteration.
		condition = conditionBuilderFunc()
		with self.ifBlock(condition, silent=True):
			# Add the loop body
			if not silent:
				instructionList.addComment("While block body")
			yield
			if not silent:
				instructionList.addComment("End of while block body")
			self.continueLoop()
		instructionList.addInstruction(instructions.EndLoopBlock())
		# update the loop break offset to jump to the end of the loop body
		nextInstructionIndex = instructionList.getInstructionCount()
		loopBlockInstruction.breakBranch = RelativeOffset(nextInstructionIndex - loopBlockInstructionIndex)
		self._scopeInstructionJustExited = loopBlockInstruction

	_range_intTypeVar = TypeVar("_range_intTypeVar", bound=RemoteIntBase)

	@remoteContextManager
	def forEachNumInRange(
		self,
		start: _range_intTypeVar | int,
		stop: _range_intTypeVar | int,
		step: _range_intTypeVar | int = 1,
	) -> Generator[RemoteIntBase, None, None]:
		RemoteType: Type[RemoteIntBase] = RemoteInt
		for arg in (start, stop, step):
			if isinstance(arg, RemoteUint):
				RemoteType = RemoteUint
				break
		remoteStart = cast(RemoteIntBase, RemoteType).ensureRemote(self.rob, cast(RemoteIntBase, start))
		remoteStop = cast(RemoteIntBase, RemoteType).ensureRemote(self.rob, cast(RemoteIntBase, stop))
		remoteStep = cast(RemoteIntBase, RemoteType).ensureRemote(self.rob, cast(RemoteIntBase, step))
		counter = remoteStart.copy()
		with self.whileBlock(lambda: counter < remoteStop):
			yield cast(RemoteIntBase, counter)
			counter += remoteStep

	@remoteContextManager
	def forEachItemInArray(
		self,
		array: RemoteArray,
	) -> Generator[RemoteVariant, None, None]:
		with self.forEachNumInRange(0, array.size()) as index:
			yield array[index]

	@contextlib.contextmanager
	def tryBlock(self, silent: bool = False):
		instructionList = self.rob.getDefaultInstructionList()
		# Add a new try block instruction to start the try block
		tryBlockInstruction = instructions.NewTryBlock(
			catchBranch=RelativeOffset(1),  # offset updated after yield
		)
		tryBlockInstructionIndex = instructionList.addInstruction(tryBlockInstruction)
		# Add the try block body
		if not silent:
			instructionList.addComment("Try block body")
		yield
		if not silent:
			instructionList.addComment("End of try block body")
		instructionList.addInstruction(instructions.EndTryBlock())
		# update the try block catch offset to jump to the end of the try block body
		nextInstructionIndex = instructionList.getInstructionCount()
		tryBlockInstruction.catchBranch = RelativeOffset(nextInstructionIndex - tryBlockInstructionIndex)
		self._scopeInstructionJustExited = tryBlockInstruction

	@contextlib.contextmanager
	def catchBlock(self, silent: bool = False):
		scopeInstructionJustExited = self._scopeInstructionJustExited
		if not isinstance(scopeInstructionJustExited, instructions.NewTryBlock):
			raise RuntimeError("Catch block not directly preceded by Try block")
		instructionList = self.rob.getDefaultInstructionList()
		tryBlockInstruction = cast(instructions.NewTryBlock, scopeInstructionJustExited)
		# add a final jump instruction to the previous try block to skip over the catch block.
		if not silent:
			instructionList.addComment("Jump over catch block")
		jumpCatchInstruction = instructions.Fork(
			jumpTo=RelativeOffset(1),  # offset updated after yield
		)
		jumpCatchInstructionIndex = instructionList.addInstruction(jumpCatchInstruction)
		# increment the catch offset of the previous try block to take the new jump instruction into account.
		tryBlockInstruction.catchBranch.value += 1
		# fetch the error status that caused the catch
		status = self.getOperationStatus()
		# reset the error status to 0
		self.setOperationStatus(0)
		# Add the catch block body
		if not silent:
			instructionList.addComment("Catch block body")
		yield status
		if not silent:
			instructionList.addComment("End of catch block body")
		# update the jump instruction to jump to the real end of the catch block.
		nextInstructionIndex = instructionList.getInstructionCount()
		jumpCatchInstruction.jumpTo = RelativeOffset(nextInstructionIndex - jumpCatchInstructionIndex)
		self._scopeInstructionJustExited = None

	def halt(self):
		instructionList = self.rob.getDefaultInstructionList()
		instructionList.addInstruction(instructions.Halt())

	def logRuntimeMessage(self, *args: str | RemoteBaseObject) -> None:
		if self._logObj is None:
			return
		instructionList = self.rob.getDefaultInstructionList()
		logObj = self._logObj
		instructionList.addComment("Begin logMessage code")
		lastIndex = len(args) - 1
		requiresNewLine = True
		for index, arg in enumerate(args):
			if index == lastIndex and isinstance(arg, str):
				arg += "\n"
				requiresNewLine = False
			if isinstance(arg, RemoteString):
				string = arg
			elif isinstance(arg, RemoteBaseObject):
				string = arg.stringify()
			else:  # arg is str
				string = self.newString(arg)
			logObj += string
		if requiresNewLine:
			logObj += "\n"
		instructionList.addComment("End logMessage code")

	def getLogObject(self) -> RemoteString | None:
		return self._logObj

	def addCompiletimeComment(self, comment: str):
		instructionList = self.rob.getDefaultInstructionList()
		instructionList.addComment(comment)
