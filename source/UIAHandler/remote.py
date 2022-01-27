# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2021-2022 NV Access Limited, Zahari Yurukov, Babbage B.V., Joseph Lee


from typing import Optional, Union
import time
import os
from ctypes import windll, byref, POINTER
from comtypes import BSTR
from comtypes.safearray import _midlSAFEARRAY as SAFEARRAY
from comtypes.automation import VARIANT
import NVDAHelper
from logHandler import log
from comInterfaces import UIAutomationClient as UIA


_dll=windll[os.path.join(NVDAHelper.versionedLibPath, "UIARemote.dll")]
initialize=_dll.initialize


def msWord_getCustomAttributeValue(
		docElement: POINTER(UIA.IUIAutomationElement),
		textRange: POINTER(UIA.IUIAutomationTextRange),
		customAttribID: int
) -> Optional[Union[int, str]]:
	customAttribValue = VARIANT()
	if _dll.msWord_getCustomAttributeValue(docElement, textRange, customAttribID, byref(customAttribValue)):
				return customAttribValue.value
	return None
