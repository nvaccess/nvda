import time
import os
from ctypes import windll, byref, POINTER, c_int, c_void_p, c_bool
from comtypes import BSTR
from comtypes.safearray import _midlSAFEARRAY as SAFEARRAY
from comtypes.automation import VARIANT
import NVDAHelper
from logHandler import log
from comInterfaces import UIAutomationClient as UIA


_dll=windll[os.path.join(NVDAHelper.versionedLibPath, "UIARemote.dll")]
initialize=_dll.initialize


def msWord_getCustomAttributeValue(textRange, customAttribID):
	customAttribValue = VARIANT()
	if _dll.msWord_getCustomAttributeValue(textRange, customAttribID, byref(customAttribValue)):
				return customAttribValue.value
	return None
