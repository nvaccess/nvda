# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2023 NV Access Limited

from typing import Callable, cast, Type
from comtypes import GUID
from UIAHandler import UIA
from logHandler import log
from . import midLevel
from .midLevel import (
	RemoteInt,
	RemoteBool,
	RemoteString,
	RemoteVariant,
	RemoteExtensionTarget,
	RemoteElement,
	RemoteTextRange,
	RemoteGuid
)


_pyTypeToRemoteType: dict[Type[object], Type[midLevel._RemoteBaseObject]] = {
	int: RemoteInt,
	bool: RemoteBool,
	str: RemoteString,
	GUID: RemoteGuid
}


class RemoteFuncAPI:

	def __init__(self, rob: midLevel.RemoteOperationBuilder):
		self._rob = rob

	def newInt(self, initialValue: int = 0) -> midLevel.RemoteInt:
		return self._rob.newInt(initialValue)

	def newBool(self, initialValue: bool = False) -> midLevel.RemoteBool:
		return self._rob.newBool(initialValue)

	def newString(self, initialValue: str = "") -> midLevel.RemoteString:
		return self._rob.newString(initialValue)

	def newVariant(self) -> midLevel.RemoteVariant:
		return self._rob.newVariant()

	def newNULLExtensionTarget(self) -> midLevel.RemoteExtensionTarget:
		return self._rob.newNULLExtensionTarget()

	def newNULLElement(self) -> midLevel.RemoteElement:
		return self._rob.newNULLElement()

	def newNULLTextRange(self) -> midLevel.RemoteTextRange:
		return self._rob.newNULLTextRange()

	def newGuid(self, initialValue: GUID) -> midLevel.RemoteGuid:
		return self._rob.newGuid(initialValue)

	def ifBlock(self, condition: midLevel.RemoteBool):
		return self._rob.ifBlock(condition)

	def elseBlock(self):
		return self._rob.elseBlock()

	def whileBlock(self, conditionBuilderFunc: Callable[[], RemoteBool]):
		return self._rob.whileBlock(conditionBuilderFunc)

	def breakLoop(self):
		self._rob.breakLoop()

	def continueLoop(self):
		self._rob.continueLoop()

	def tryBlock(self):
		return self._rob.tryBlock()

	def catchBlock(self):
		return self._rob.catchBlock()

	def setOperationStatus(self, status: int | RemoteInt):
		self._rob.setOperationStatus(status)

	def getOperationStatus(self) -> RemoteInt:
		return self._rob.getOperationStatus()

	def halt(self):
		self._rob.halt()

	def logMessage(self, *strings):
		self._rob.logMessage(*strings)


def execute(remoteFunc: Callable, *args: object, enableLogging=False) -> object:
	rob = midLevel.RemoteOperationBuilder(enableLogging=enableLogging)
	remoteArgs = []
	for arg in args:
		remoteArg: midLevel._RemoteBaseObject
		if isinstance(arg, UIA.IUIAutomationElement):
			remoteArg = rob.importElement(arg)
		elif isinstance(arg, UIA.IUIAutomationTextRange):
			remoteArg = rob.importTextRange(arg)
		else:
			remoteType = _pyTypeToRemoteType.get(type(arg))
			if remoteType is None:
				raise TypeError(f"Unsupported argument type: {type(arg)}")
			remoteArg = cast(midLevel._RemoteBaseObject, remoteType).ensureArgumentIsRemote(rob, arg)
		remoteArgs.append(remoteArg)
	ba = RemoteFuncAPI(rob)
	remoteResults = remoteFunc(ba, *remoteArgs)
	if isinstance(remoteResults, midLevel._RemoteBaseObject):
		remoteResults = [remoteResults]
	for remoteResult in remoteResults:
		rob.addToResults(remoteResult)
	if enableLogging:
		log.info(f"{rob.dumpInstructions()}")
	rob.execute()
	if enableLogging:
		log.info(rob.dumpLog())
	if len(remoteResults) == 1:
		return rob.getResult(remoteResults[0])
	return tuple(rob.getResult(remoteResult) for remoteResult in remoteResults)
