# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2021-2022 NV Access Limited


from typing import Optional, Union
import os
from ctypes import windll, byref, POINTER
from comtypes.automation import VARIANT
import NVDAHelper
from comInterfaces import UIAutomationClient as UIA


_dll = None


def initialize(doRemote: bool, UIAClient: POINTER(UIA.IUIAutomation)):
	"""
	Initializes UI Automation remote operations.
	@param doRemote: true if code should be executed remotely, or false for locally.
	@param UIAClient: the current instance of the UI Automation client library running in NVDA.
	"""
	global _dll
	_dll = windll[os.path.join(NVDAHelper.versionedLibPath, "UIARemote.dll")]
	_dll.initialize(doRemote, UIAClient)


def msWord_getCustomAttributeValue(
		docElement: POINTER(UIA.IUIAutomationElement),
		textRange: POINTER(UIA.IUIAutomationTextRange),
		customAttribID: int
) -> Optional[Union[int, str]]:
	if _dll is None:
		raise RuntimeError("UIARemote not initialized")
	customAttribValue = VARIANT()
	if _dll.msWord_getCustomAttributeValue(docElement, textRange, customAttribID, byref(customAttribValue)):
		return customAttribValue.value
	return None
