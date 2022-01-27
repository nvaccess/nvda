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


_dll = windll[os.path.join(NVDAHelper.versionedLibPath, "UIARemote.dll")]
initialize = _dll.initialize


def msWord_getCustomAttributeValue(
		docElement: POINTER(UIA.IUIAutomationElement),
		textRange: POINTER(UIA.IUIAutomationTextRange),
		customAttribID: int
) -> Optional[Union[int, str]]:
	customAttribValue = VARIANT()
	if _dll.msWord_getCustomAttributeValue(docElement, textRange, customAttribID, byref(customAttribValue)):
		return customAttribValue.value
	return None
