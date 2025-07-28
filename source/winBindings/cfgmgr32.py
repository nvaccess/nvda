import ctypes
from ctypes.wintypes import DWORD, ULONG


CM_Get_Device_ID = ctypes.windll.cfgmgr32.CM_Get_Device_IDW
CM_Get_Device_ID.argtypes = (DWORD, ctypes.c_wchar_p, ULONG, ULONG)
CM_Get_Device_ID.restype = DWORD
