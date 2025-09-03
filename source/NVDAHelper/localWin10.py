from ctypes import c_int, c_void_p, cdll, wstring_at
from winBindings.oleaut32 import SysFreeString

import NVDAState

dll = cdll.LoadLibrary(NVDAState.ReadPaths.nvdaHelperLocalWin10Dll)


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


uwpOcr_getLanguages = dll.uwpOcr_getLanguages
uwpOcr_getLanguages.argtypes = ()
uwpOcr_getLanguages.restype = c_void_p
uwpOcr_getLanguages.errcheck = _bstrReturnErrcheck

uwpOcr_initialize = dll.uwpOcr_initialize
uwpOcr_initialize.restype = c_void_p

uwpOcr_terminate = dll.uwpOcr_terminate
uwpOcr_terminate.argtypes = [c_void_p]
uwpOcr_terminate.restype = None

uwpOcr_recognize = dll.uwpOcr_recognize
uwpOcr_recognize.argtypes = [c_void_p, c_void_p, c_int, c_int]
