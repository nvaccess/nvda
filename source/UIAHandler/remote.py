# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2021-2022 NV Access Limited


from typing import Optional, Union
import os
from ctypes import windll, byref, POINTER
from comtypes.automation import VARIANT
from comtypes import GUID
import NVDAHelper
from comInterfaces import UIAutomationClient as UIA


_dll = None


def initialize(doRemote: bool, UIAClient: POINTER(UIA.IUIAutomation)):
	"""
	Initializes UI Automation remote operations.
	@param doRemote: true if code should be executed remotely, or false for locally.
	@param UIAClient: the current instance of the UI Automation client library running in NVDA.
	"""
	return True

def msWord_getCustomAttributeValue(
		docElement: POINTER(UIA.IUIAutomationElement),
		textRange: POINTER(UIA.IUIAutomationTextRange),
		customAttribID: int
) -> Optional[Union[int, str]]:
	from ._remoteOps import highLevel
	from logHandler import log
	# Several custom extension GUIDs specific to Microsoft Word
	guid_msWord_extendedTextRangePattern = GUID("{93514122-FF04-4B2C-A4AD-4AB04587C129}")
	guid_msWord_getCustomAttributeValue = GUID("{081ACA91-32F2-46F0-9FB9-017038BC45F8}")
	with highLevel.RemoteOperationBuilder(enableLogging=True) as rob:
		remote_docElement = rob.newElement(docElement)
		remote_textRange = rob.newTextRange(textRange)
		remote_customAttribID = rob.newInt(customAttribID)
		remote_customAttribValue = rob.newVariant()
		rob.addToResults(remote_customAttribValue)
		with rob.ifBlock(remote_docElement.isExtensionSupported(guid_msWord_extendedTextRangePattern)):
			rob.logMessage("msWord_getCustomAttributeValue: docElement supports extendedTextRangePattern")
			remote_extendedTextRangePattern = rob.newExtensionTarget()
			rob.logMessage("msWord_getCustomAttributeValue: doing callExtension for extendedTextRangePattern")
			remote_docElement.callExtension(
				guid_msWord_extendedTextRangePattern,
				remote_extendedTextRangePattern
			)
			with rob.ifBlock(remote_extendedTextRangePattern.isNull()):
				rob.logMessage("msWord_getCustomAttributeValue: extendedTextRangePattern is null")
				rob.halt()
			with  rob.elseBlock():
				rob.logMessage("msWord_getCustomAttributeValue: got extendedTextRangePattern ")
				with rob.ifBlock(remote_extendedTextRangePattern.isExtensionSupported(guid_msWord_getCustomAttributeValue)):
					rob.logMessage("msWord_getCustomAttributeValue: extendedTextRangePattern supports getCustomAttributeValue")
					rob.logMessage("msWord_getCustomAttributeValue: doing callExtension for getCustomAttributeValue")
					remote_extendedTextRangePattern.callExtension(
						guid_msWord_getCustomAttributeValue,
						remote_textRange,
						remote_customAttribID,
						remote_customAttribValue
					)
					rob.logMessage("msWord_getCustomAttributeValue: got customAttribValue of ", remote_customAttribValue)
				with rob.elseBlock():
					rob.logMessage("msWord_getCustomAttributeValue: extendedTextRangePattern does not support getCustomAttributeValue")
		with rob.elseBlock():
			rob.logMessage("msWord_getCustomAttributeValue: docElement does not support extendedTextRangePattern")
		rob.logMessage("msWord_getCustomAttributeValue end")
	log.info(rob.dumpLog())
	result = rob.getResult(remote_customAttribValue)
	return result
