from ctypes import *
from comtypes import BSTR
import NVDAHelper

_getWindowTextInRect=CFUNCTYPE(c_long,c_long,c_long,c_int,c_int,c_int,c_int,POINTER(BSTR),POINTER(BSTR))(('displayModel_getWindowTextInRect',NVDAHelper.localLib),((1,),(1,),(1,),(1,),(1,),(1,),(2,),(2,)))
def getWindowTextInRect(bindingHandle, windowHandle, left, top, right, bottom):
	text, cpBuf = _getWindowTextInRect(bindingHandle, windowHandle, left, top, right, bottom)
	characterPoints = []
	cpBufIt = iter(cpBuf)
	for cp in cpBufIt:
		characterPoints.append((ord(cp), ord(next(cpBufIt))))
	return text, characterPoints
