from comtypes import BSTR
import NVDAHelper

_dll=NVDAHelper.getHelperLocalWin10Dll()
initialize=_dll.uiaRemote_initialize
getTextContent=_dll.uiaRemote_getTextContent
getTextContent.restype=BSTR
