from ctypes import pointer, c_int
from comtypes import BSTR
from comtypes.safearray import _midlSAFEARRAY as SAFEARRAY
from comtypes.automation import VARIANT
import NVDAHelper

_dll=NVDAHelper.getHelperLocalWin10Dll()
initialize=_dll.uiaRemote_initialize
_getTextContent=_dll.uiaRemote_getTextContent
_getTextContent.restype=SAFEARRAY(VARIANT)

def getTextContent(textRange,attribIDs):
	attribIDsArray=SAFEARRAY(c_int).from_param(attribIDs)
	pArray=_getTextContent(textRange,attribIDsArray)
	pArray._needsfree=True
	return pArray.unpack()
