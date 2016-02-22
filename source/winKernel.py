#winKernel.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import ctypes
import ctypes.wintypes
from ctypes import *
from ctypes.wintypes import *

kernel32=ctypes.windll.kernel32
advapi32 = windll.advapi32

#Constants
INFINITE = 0xffffffff
#Process control
PROCESS_ALL_ACCESS=0x1F0FFF
PROCESS_TERMINATE=0x1
PROCESS_VM_OPERATION=0x8
PROCESS_VM_READ=0x10
PROCESS_VM_WRITE=0X20
SYNCHRONIZE=0x100000
PROCESS_QUERY_INFORMATION=0x400
READ_CONTROL=0x20000
MEM_COMMIT=0x1000
MEM_RELEASE=0x8000
PAGE_READWRITE=0x4
MAXIMUM_ALLOWED = 0x2000000
STARTF_USESTDHANDLES = 0x00000100
#Console handles
STD_INPUT_HANDLE=-10
STD_OUTPUT_HANDLE=-11
STD_ERROR_HANDLE=-12
LOCALE_USER_DEFAULT=0x0400
DATE_LONGDATE=0x00000002 
TIME_NOSECONDS=0x00000002

def GetStdHandle(handleID):
	h=kernel32.GetStdHandle(handleID)
	if h==0:
		raise WinError()
	return h

GENERIC_READ=0x80000000
GENERIC_WRITE=0x40000000
FILE_SHARE_READ=1
FILE_SHARE_WRITE=2
OPEN_EXISTING=3

def CreateFile(fileName,desiredAccess,shareMode,securityAttributes,creationDisposition,flags,templateFile):
	res=kernel32.CreateFileW(fileName,desiredAccess,shareMode,securityAttributes,creationDisposition,flags,templateFile)
	if res==0:
		raise ctypes.WinError()
	return res



def openProcess(*args):
	return kernel32.OpenProcess(*args)

def closeHandle(*args):
	return kernel32.CloseHandle(*args)

#added by Rui Batista to use on Say_battery_status script 
#copied from platform sdk documentation (with required changes to work in python) 
class SYSTEM_POWER_STATUS(ctypes.Structure):
	_fields_ = [("ACLineStatus", ctypes.c_byte), ("BatteryFlag", ctypes.c_byte), ("BatteryLifePercent", ctypes.c_byte), ("Reserved1", ctypes.c_byte), ("BatteryLifeTime", ctypes.wintypes.DWORD), ("BatteryFullLiveTime", ctypes.wintypes.DWORD)]


def GetSystemPowerStatus(sps):
	return kernel32.GetSystemPowerStatus(ctypes.byref(sps))

def getThreadLocale():
	return kernel32.GetThreadLocale()

class SYSTEMTIME(ctypes.Structure):
	_fields_ = (
		("wYear", WORD),
		("wMonth", WORD),
		("wDayOfWeek", WORD),
		("wDay", WORD),
		("wHour", WORD),
		("wMinute", WORD),
		("wSecond", WORD),
		("wMilliseconds", WORD)
	)

def GetDateFormat(Locale,dwFlags,date,lpFormat):
	if date is not None:
		date=SYSTEMTIME(date.year,date.month,0,date.day,date.hour,date.minute,date.second,0)
		lpDate=byref(date)
	else:
		lpDate=None
	bufferLength=kernel32.GetDateFormatW(Locale, dwFlags, lpDate, lpFormat, None, 0)
	buf=ctypes.create_unicode_buffer("", bufferLength)
	kernel32.GetDateFormatW(Locale, dwFlags, lpDate, lpFormat, buf, bufferLength)
	return buf.value

def GetTimeFormat(Locale,dwFlags,date,lpFormat):
	if date is not None:
		date=SYSTEMTIME(date.year,date.month,0,date.day,date.hour,date.minute,date.second,0)
		lpTime=byref(date)
	else:
		lpTime=None
	bufferLength=kernel32.GetTimeFormatW(Locale,dwFlags,lpTime,lpFormat, None, 0)
	buf=ctypes.create_unicode_buffer("", bufferLength)
	kernel32.GetTimeFormatW(Locale,dwFlags,lpTime,lpFormat, buf, bufferLength)
	return buf.value

def openProcess(*args):
	return kernel32.OpenProcess(*args)

def virtualAllocEx(*args):
	res = kernel32.VirtualAllocEx(*args)
	if res == 0:
		raise WinError()
	return res

def virtualFreeEx(*args):
	return kernel32.VirtualFreeEx(*args)

def readProcessMemory(*args):
	return kernel32.ReadProcessMemory(*args)

def writeProcessMemory(*args):
	return kernel32.WriteProcessMemory(*args)

def waitForSingleObject(handle,timeout):
	return kernel32.WaitForSingleObject(handle,timeout)

SHUTDOWN_NORETRY = 0x00000001

def SetProcessShutdownParameters(level, flags):
	res = kernel32.SetProcessShutdownParameters(level, flags)
	if res == 0:
		raise ctypes.WinError()

def GetExitCodeProcess(process):
	exitCode = ctypes.wintypes.DWORD()
	if not kernel32.GetExitCodeProcess(process, ctypes.byref(exitCode)):
		raise ctypes.WinError()
	return exitCode.value

def TerminateProcess(process, exitCode):
	if not kernel32.TerminateProcess(process, exitCode):
		raise ctypes.WinError()

DRIVE_UNKNOWN = 0
DRIVE_NO_ROOT_DIR = 1
DRIVE_REMOVABLE = 2
DRIVE_FIXED = 3
DRIVE_REMOTE = 4
DRIVE_CDROM = 5
DRIVE_RAMDISK = 6

def GetDriveType(rootPathName):
	return kernel32.GetDriveTypeW(rootPathName)

class SECURITY_ATTRIBUTES(Structure):
	_fields_ = (
		("nLength", DWORD),
		("lpSecurityDescriptor", LPVOID),
		("bInheritHandle", BOOL)
	)
	def __init__(self, **kwargs):
		super(SECURITY_ATTRIBUTES, self).__init__(nLength=sizeof(self), **kwargs)

def CreatePipe(pipeAttributes, size):
	read = ctypes.wintypes.HANDLE()
	write = ctypes.wintypes.HANDLE()
	if kernel32.CreatePipe(ctypes.byref(read), ctypes.byref(write), byref(pipeAttributes) if pipeAttributes else None, ctypes.wintypes.DWORD(size)) == 0:
		raise ctypes.WinError()
	return read.value, write.value

class STARTUPINFOW(Structure):
	_fields_=(
		('cb',DWORD),
		('lpReserved',LPWSTR),
		('lpDesktop',LPWSTR),
		('lpTitle',LPWSTR),
		('dwX',DWORD),
		('dwY',DWORD),
		('dwXSize',DWORD),
		('dwYSize',DWORD),
		('dwXCountChars',DWORD),
		('dwYCountChars',DWORD),
		('dwFillAttribute',DWORD),
		('dwFlags',DWORD),
		('wShowWindow',WORD),
		('cbReserved2',WORD),
		('lpReserved2',POINTER(c_byte)),
		('hSTDInput',HANDLE),
		('hSTDOutput',HANDLE),
		('hSTDError',HANDLE),
	)
	def __init__(self, **kwargs):
		super(STARTUPINFOW, self).__init__(cb=sizeof(self), **kwargs)
STARTUPINFO = STARTUPINFOW

class PROCESS_INFORMATION(Structure):
	_fields_=(
		('hProcess',HANDLE),
		('hThread',HANDLE),
		('dwProcessID',DWORD),
		('dwThreadID',DWORD),
	)

def CreateProcessAsUser(token, applicationName, commandLine, processAttributes, threadAttributes, inheritHandles, creationFlags, environment, currentDirectory, startupInfo, processInformation):
	if advapi32.CreateProcessAsUserW(token, applicationName, commandLine, processAttributes, threadAttributes, inheritHandles, creationFlags, environment, currentDirectory, byref(startupInfo), byref(processInformation)) == 0:
		raise WinError()

def GetCurrentProcess():
	return kernel32.GetCurrentProcess()

def OpenProcessToken(ProcessHandle, DesiredAccess):
	token = HANDLE()
	if advapi32.OpenProcessToken(ProcessHandle, DesiredAccess, byref(token)) == 0:
		raise WinError()
	return token.value

DUPLICATE_SAME_ACCESS = 0x00000002

def DuplicateHandle(sourceProcessHandle, sourceHandle, targetProcessHandle, desiredAccess, inheritHandle, options):
	targetHandle = HANDLE()
	if kernel32.DuplicateHandle(sourceProcessHandle, sourceHandle, targetProcessHandle, byref(targetHandle), desiredAccess, inheritHandle, options) == 0:
		raise WinError()
	return targetHandle.value

PAPCFUNC = ctypes.WINFUNCTYPE(None, ctypes.wintypes.ULONG)
THREAD_SET_CONTEXT = 16
