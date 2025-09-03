from ctypes import CFUNCTYPE, c_uint, c_void_p, c_wchar_p, windll, wstring_at
from comtypes import BSTR
from winBindings.oleaut32 import SysFreeString

import NVDAState

dll = windll.LoadLibrary(NVDAState.ReadPaths.nvdaHelperLocalWin10Dll)


def _bstrReturnErrcheck(address: int, *_) -> str:
	"""Handle a BSTR returned from a ctypes function call.
	This includes freeing the memory.
	This is needed for nvdaHelperLocalWin10 functions which return a BSTR.
	"""
	# comtypes.BSTR.from_address seems to cause a crash for some reason. Not sure why.
	# Just access the string ourselves.
	# This will terminate at a null character, even though BSTR allows nulls.
	# We're only using this for normal, null-terminated strings anyway.
	# import comtypes
	# val = comtypes.BSTR.from_param(address)
	val = wstring_at(address)
	SysFreeString(address)
	return val


UwpOcr_P = c_void_p

uwpOcr_getLanguages = dll.uwpOcr_getLanguages
uwpOcr_getLanguages.argtypes = ()
uwpOcr_getLanguages.restype = BSTR
# uwpOcr_getLanguages.restype = c_void_p
# uwpOcr_getLanguages.errcheck = _bstrReturnErrcheck

uwpOcr_Callback = CFUNCTYPE(None, c_wchar_p)

uwpOcr_initialize = dll.uwpOcr_initialize
uwpOcr_initialize.argtypes = (c_wchar_p, uwpOcr_Callback)
uwpOcr_initialize.restype = UwpOcr_P

uwpOcr_terminate = dll.uwpOcr_terminate
uwpOcr_terminate.argtypes = (UwpOcr_P,)
uwpOcr_terminate.restype = None

uwpOcr_recognize = dll.uwpOcr_recognize
uwpOcr_recognize.argtypes = [UwpOcr_P, c_void_p, c_uint, c_uint]
uwpOcr_recognize.restype = None
