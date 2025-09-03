from ctypes import CFUNCTYPE, c_uint, c_void_p, c_wchar_p, windll
from comtypes import BSTR

import NVDAState

dll = windll.LoadLibrary(NVDAState.ReadPaths.nvdaHelperLocalWin10Dll)

UwpOcr_P = c_void_p

uwpOcr_getLanguages = dll.uwpOcr_getLanguages
uwpOcr_getLanguages.argtypes = ()
uwpOcr_getLanguages.restype = BSTR

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
