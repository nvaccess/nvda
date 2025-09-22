# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2025 NV Access Limited, Rui Batista, Aleksey Sadovoy, Peter Vagner,
# Mozilla Corporation, Babbage B.V., Joseph Lee, Łukasz Golonka
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
Functions that wrap Windows API functions from kernel32.dll and advapi32.dll.

When working on this file, consider moving to winAPI.
"""

import contextlib
import ctypes
import ctypes.wintypes
from ctypes import byref, sizeof, Structure, WinError
from ctypes.wintypes import BOOL, DWORD, HANDLE, LARGE_INTEGER, LCID, LPVOID
from typing import (
	TYPE_CHECKING,
	Optional,
	Union,
)

if TYPE_CHECKING:
	from winAPI._powerTracking import SystemPowerStatus


import winBindings.advapi32
import winBindings.kernel32
from winBindings.kernel32 import (
	FILETIME as _FILETIME,
	PTIMERAPCROUTINE as _PTIMERAPCROUTINE,
	SYSTEMTIME as _SYSTEMTIME,
	TIME_ZONE_INFORMATION as _TIME_ZONE_INFORMATION,
)
from utils import _deprecate


__getattr__ = _deprecate.handleDeprecations(
	_deprecate.MovedSymbol("kernel32", "winBindings.kernel32", "dll"),
	_deprecate.MovedSymbol(
		"SYSTEM_POWER_STATUS",
		"winBindings.kernel32",
	),
	_deprecate.MovedSymbol(
		"FILETIME",
		"winBindings.kernel32",
	),
	_deprecate.MovedSymbol(
		"SYSTEMTIME",
		"winBindings.kernel32",
	),
	_deprecate.MovedSymbol(
		"TIME_ZONE_INFORMATION",
		"winBindings.kernel32",
	),
	_deprecate.MovedSymbol(
		"STARTUPINFO",
		"winBindings.advapi32",
	),
	_deprecate.MovedSymbol(
		"STARTUPINFOW",
		"winBindings.advapi32",
	),
	_deprecate.MovedSymbol(
		"PROCESS_INFORMATION",
		"winBindings.advapi32",
	),
	_deprecate.MovedSymbol(
		"PAPCFUNC ",
		"winBindings.kernel32",
	),
	_deprecate.MovedSymbol("advapi32", "winBindings.advapi32", "dll"),
)


# Constants
INFINITE = 0xFFFFFFFF
# Process control
PROCESS_ALL_ACCESS = 0x1F0FFF
PROCESS_TERMINATE = 0x1
PROCESS_VM_OPERATION = 0x8
PROCESS_VM_READ = 0x10
PROCESS_VM_WRITE = 0x20
SYNCHRONIZE = 0x100000
PROCESS_QUERY_INFORMATION = 0x400
READ_CONTROL = 0x20000
MEM_COMMIT = 0x1000
MEM_RELEASE = 0x8000
PAGE_READWRITE = 0x4
MAXIMUM_ALLOWED = 0x2000000
STARTF_USESTDHANDLES = 0x00000100
# Console handles
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12
LOCALE_USER_DEFAULT = 0x0400
LOCALE_NAME_USER_DEFAULT = None
DATE_LONGDATE = 0x00000002
TIME_NOSECONDS = 0x00000002
# Create Mutex
ERROR_ALREADY_EXISTS = 0xB7
# Wait return types
WAIT_ABANDONED = 0x00000080
WAIT_IO_COMPLETION = 0x000000C0
WAIT_OBJECT_0 = 0x00000000
WAIT_TIMEOUT = 0x00000102
WAIT_FAILED = 0xFFFFFFFF
# Image file machine constants
IMAGE_FILE_MACHINE_UNKNOWN = 0
# LoadLibraryEx constants
LOAD_WITH_ALTERED_SEARCH_PATH = 0x8


def GetStdHandle(handleID):
	h = winBindings.kernel32.GetStdHandle(handleID)
	if h == 0:
		raise WinError()
	return h


GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
FILE_SHARE_READ = 1
FILE_SHARE_WRITE = 2
FILE_SHARE_DELETE = 4
OPEN_EXISTING = 3


def CreateFile(
	fileName,
	desiredAccess,
	shareMode,
	securityAttributes,
	creationDisposition,
	flags,
	templateFile,
):
	res = winBindings.kernel32.CreateFile(
		fileName,
		desiredAccess,
		shareMode,
		securityAttributes,
		creationDisposition,
		flags,
		templateFile,
	)
	if res == 0:
		raise ctypes.WinError()
	return res


def createEvent(eventAttributes=None, manualReset=False, initialState=False, name=None):
	res = winBindings.kernel32.CreateEvent(eventAttributes, manualReset, initialState, name)
	if res == 0:
		raise ctypes.WinError()
	return res


def createWaitableTimer(securityAttributes=None, manualReset=False, name=None):
	"""Wrapper to the kernel32 CreateWaitableTimer function.
	Consult https://msdn.microsoft.com/en-us/library/windows/desktop/ms682492.aspx for Microsoft's documentation.
	In contrast with the original function, this wrapper assumes the following defaults.
	@param securityAttributes: Defaults to C{None};
		The timer object gets a default security descriptor and the handle cannot be inherited.
		The ACLs in the default security descriptor for a timer come from the primary or impersonation token of the creator.
	@type securityAttributes: pointer to L{SECURITY_ATTRIBUTES}
	@param manualReset: Defaults to C{False} which means the timer is a synchronization timer.
		If C{True}, the timer is a manual-reset notification timer.
	@type manualReset: bool
	@param name: Defaults to C{None}, the timer object is created without a name.
	@type name: str
	"""
	res = winBindings.kernel32.CreateWaitableTimer(securityAttributes, manualReset, name)
	if res == 0:
		raise ctypes.WinError()
	return res


def setWaitableTimer(
	handle: int,
	dueTime: int,
	period: int = 0,
	completionRoutine: _PTIMERAPCROUTINE | None = None,
	arg: int | None = None,
	resume: bool = False,
):
	"""Wrapper to the kernel32 SETWaitableTimer function.

	Consult https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-setwaitabletimer for Microsoft's documentation.

	:param handle: A handle to the timer object.
	:param dueTime: Relative time (in milliseconds).
		Note that the original function requires relative time to be supplied as a negative nanoseconds value.
	:param period: Defaults to 0, timer is only executed once.
		Value should be supplied in milliseconds.
	:param completionRoutine: An optional function to be executed when the timer elapses.
	:param arg: A pointer to a structure that is passed to the completion routine, defaults to ``None``. .
	:param resume: Whether to restore a system in suspended power conservation mode when the timer state is set to signaled, defaults to ``False``.
		If the system does not support a restore, the call succeeds, but ``GetLastError`` returns ``ERROR_NOT_SUPPORTED``.
	"""
	if completionRoutine is None:
		completionRoutine = _PTIMERAPCROUTINE(0)
	res = winBindings.kernel32.SetWaitableTimer(
		handle,
		# due time is in 100 nanosecond intervals, relative time should be negated.
		LARGE_INTEGER(dueTime * -10000),
		period,
		completionRoutine,
		arg,
		resume,
	)
	if res == 0:
		raise ctypes.WinError()
	return True


def openProcess(*args) -> int:
	try:
		return winBindings.kernel32.OpenProcess(*args) or 0
	except Exception:
		# Compatibility: error should just be a handle of 0.
		return 0


def closeHandle(*args):
	return winBindings.kernel32.CloseHandle(*args)


def GetSystemPowerStatus(sps: "SystemPowerStatus") -> int:
	return winBindings.kernel32.GetSystemPowerStatus(ctypes.byref(sps))


def getThreadLocale():
	return winBindings.kernel32.GetThreadLocale()


ERROR_INVALID_FUNCTION = 0x1
ERROR_ACCESS_DENIED = 0x5
ERROR_INVALID_HANDLE = 0x6


@contextlib.contextmanager
def suspendWow64Redirection():
	"""Context manager which disables Wow64 redirection for a section of code and re-enables it afterwards"""
	oldValue = LPVOID()
	res = winBindings.kernel32.Wow64DisableWow64FsRedirection(byref(oldValue))
	if res == 0:
		# Disabling redirection failed.
		# This can occur if we're running on 32-bit Windows (no Wow64 redirection)
		# or as a 64-bit process on 64-bit Windows (Wow64 redirection not applicable)
		# In this case failure is expected and there is no reason to raise an exception.
		# Inspect last error code to determine reason for the failure.
		errorCode = winBindings.kernel32.GetLastError()
		if errorCode == ERROR_INVALID_FUNCTION:  # Redirection not supported or not applicable.
			redirectionDisabled = False
		else:
			raise WinError(errorCode)
	else:
		redirectionDisabled = True
	try:
		yield
	finally:
		if redirectionDisabled:
			if winBindings.kernel32.Wow64RevertWow64FsRedirection(oldValue) == 0:
				raise WinError()


def time_tToFileTime(time_tToConvert: float) -> _FILETIME:
	"""Converts time_t as returned from `time.time` to a FILETIME structure.
	Based on a code snipped from:
	https://docs.microsoft.com/en-us/windows/win32/sysinfo/converting-a-time-t-value-to-a-file-time
	"""
	timeAsFileTime = _FILETIME()
	res = (int(time_tToConvert) * 10000000) + 116444736000000000
	timeAsFileTime.dwLowDateTime = res
	timeAsFileTime.dwHighDateTime = res >> 32
	return timeAsFileTime


def FileTimeToSystemTime(lpFileTime: _FILETIME, lpSystemTime: _SYSTEMTIME) -> None:
	if winBindings.kernel32.FileTimeToSystemTime(byref(lpFileTime), byref(lpSystemTime)) == 0:
		raise WinError()


def SystemTimeToTzSpecificLocalTime(
	timeZoneInformation: Union[_TIME_ZONE_INFORMATION, None],
	lpUniversalTime: _SYSTEMTIME,
	lpLocalTime: _SYSTEMTIME,
) -> None:
	"""Wrapper for `SystemTimeToTzSpecificLocalTime` from kernel32.
	:param lpTimeZoneInformation: Either TIME_ZONE_INFORMATION containing info about the desired time zone
	or `None` when the current time zone as configured in Windows settings should be used.
	:param lpUniversalTime: SYSTEMTIME structure containing time in UTC wwhich you wish to convert.
	: param lpLocalTime: A SYSTEMTIME structure in which time converted to the desired time zone would be placed.
	:raises WinError
	"""
	if timeZoneInformation is not None:
		lpTimeZoneInformation = byref(timeZoneInformation)
	else:
		lpTimeZoneInformation = None
	if (
		winBindings.kernel32.SystemTimeToTzSpecificLocalTime(
			lpTimeZoneInformation,
			byref(lpUniversalTime),
			byref(lpLocalTime),
		)
		== 0
	):
		raise WinError()


def GetDateFormatEx(Locale, dwFlags, date, lpFormat):
	if date is not None:
		date = _SYSTEMTIME(date.year, date.month, 0, date.day, date.hour, date.minute, date.second, 0)
		lpDate = byref(date)
	else:
		lpDate = None
	bufferLength = winBindings.kernel32.GetDateFormatEx(Locale, dwFlags, lpDate, lpFormat, None, 0, None)
	buf = ctypes.create_unicode_buffer("", bufferLength)
	winBindings.kernel32.GetDateFormatEx(Locale, dwFlags, lpDate, lpFormat, buf, bufferLength, None)
	return buf.value


def GetTimeFormatEx(Locale, dwFlags, date, lpFormat):
	if date is not None:
		date = _SYSTEMTIME(date.year, date.month, 0, date.day, date.hour, date.minute, date.second, 0)
		lpTime = byref(date)
	else:
		lpTime = None
	bufferLength = winBindings.kernel32.GetTimeFormatEx(Locale, dwFlags, lpTime, lpFormat, None, 0)
	buf = ctypes.create_unicode_buffer("", bufferLength)
	winBindings.kernel32.GetTimeFormatEx(Locale, dwFlags, lpTime, lpFormat, buf, bufferLength)
	return buf.value


def virtualAllocEx(*args):
	res = winBindings.kernel32.VirtualAllocEx(*args)
	if res == 0:
		raise WinError()
	return res


def virtualFreeEx(*args):
	return winBindings.kernel32.VirtualFreeEx(*args)


def readProcessMemory(*args):
	return winBindings.kernel32.ReadProcessMemory(*args)


def writeProcessMemory(*args):
	return winBindings.kernel32.WriteProcessMemory(*args)


def waitForSingleObject(handle, timeout):
	res = winBindings.kernel32.WaitForSingleObject(handle, timeout)
	if res == WAIT_FAILED:
		raise ctypes.WinError()
	return res


def waitForSingleObjectEx(handle, timeout, alertable):
	res = winBindings.kernel32.WaitForSingleObjectEx(handle, timeout, alertable)
	if res == WAIT_FAILED:
		raise ctypes.WinError()
	return res


SHUTDOWN_NORETRY = 0x00000001


def SetProcessShutdownParameters(level, flags):
	res = winBindings.kernel32.SetProcessShutdownParameters(level, flags)
	if res == 0:
		raise ctypes.WinError()


def GetExitCodeProcess(process):
	exitCode = ctypes.wintypes.DWORD()
	if not winBindings.kernel32.GetExitCodeProcess(process, ctypes.byref(exitCode)):
		raise ctypes.WinError()
	return exitCode.value


def TerminateProcess(process, exitCode):
	if not winBindings.kernel32.TerminateProcess(process, exitCode):
		raise ctypes.WinError()


DRIVE_UNKNOWN = 0
DRIVE_NO_ROOT_DIR = 1
DRIVE_REMOVABLE = 2
DRIVE_FIXED = 3
DRIVE_REMOTE = 4
DRIVE_CDROM = 5
DRIVE_RAMDISK = 6


def GetDriveType(rootPathName):
	return winBindings.kernel32.GetDriveType(rootPathName)


class SECURITY_ATTRIBUTES(Structure):
	_fields_ = (
		("nLength", DWORD),
		("lpSecurityDescriptor", LPVOID),
		("bInheritHandle", BOOL),
	)

	def __init__(self, **kwargs):
		super(SECURITY_ATTRIBUTES, self).__init__(nLength=sizeof(self), **kwargs)


def CreatePipe(pipeAttributes, size):
	read = ctypes.wintypes.HANDLE()
	write = ctypes.wintypes.HANDLE()
	if (
		winBindings.kernel32.CreatePipe(
			ctypes.byref(read),
			ctypes.byref(write),
			byref(pipeAttributes) if pipeAttributes else None,
			ctypes.wintypes.DWORD(size),
		)
		== 0
	):
		raise ctypes.WinError()
	return read.value, write.value


def CreateProcessAsUser(
	token,
	applicationName,
	commandLine,
	processAttributes,
	threadAttributes,
	inheritHandles,
	creationFlags,
	environment,
	currentDirectory,
	startupInfo,
	processInformation,
):
	if (
		winBindings.advapi32.CreateProcessAsUser(
			token,
			applicationName,
			commandLine,
			processAttributes,
			threadAttributes,
			inheritHandles,
			creationFlags,
			environment,
			currentDirectory,
			byref(startupInfo),
			byref(processInformation),
		)
		== 0
	):
		raise WinError()


def GetCurrentProcess():
	return winBindings.kernel32.GetCurrentProcess()


def OpenProcessToken(ProcessHandle, DesiredAccess):
	token = HANDLE()
	if winBindings.advapi32.OpenProcessToken(ProcessHandle, DesiredAccess, byref(token)) == 0:
		raise WinError()
	return token.value


DUPLICATE_SAME_ACCESS = 0x00000002


def DuplicateHandle(
	sourceProcessHandle,
	sourceHandle,
	targetProcessHandle,
	desiredAccess,
	inheritHandle,
	options,
):
	targetHandle = HANDLE()
	if (
		winBindings.kernel32.DuplicateHandle(
			sourceProcessHandle,
			sourceHandle,
			targetProcessHandle,
			byref(targetHandle),
			desiredAccess,
			inheritHandle,
			options,
		)
		== 0
	):
		raise WinError()
	return targetHandle.value


THREAD_SET_CONTEXT = 16

GMEM_MOVEABLE = 2


class HGLOBAL(HANDLE):
	"""
	A class for the HGLOBAL Windows handle type.
	This class can auto-free the handle when it goes out of scope,
	and also contains a classmethod for alloc,
	And a context manager compatible method for locking.
	"""

	def __init__(self, h, autoFree=True):
		"""
		@param h: the raw Windows HGLOBAL handle
		@param autoFree: True by default, the handle will automatically be freed with GlobalFree
		when this object goes out of scope.
		"""
		super(HGLOBAL, self).__init__(h)
		self._autoFree = autoFree

	def __del__(self):
		if self and self._autoFree:
			winBindings.kernel32.GlobalFree(self)

	@classmethod
	def alloc(cls, flags, size):
		"""
		Allocates global memory with GlobalAlloc
		providing it as an instance of this class.
		This method Takes the same arguments as GlobalAlloc.
		"""
		h = winBindings.kernel32.GlobalAlloc(flags, size)
		return cls(h)

	@contextlib.contextmanager
	def lock(self):
		"""
		Used as a context manager,
		This method locks the global memory with GlobalLock,
		providing the usable memory address to the body of the 'with' statement.
		When the body completes, GlobalUnlock is automatically called.
		"""
		try:
			yield winBindings.kernel32.GlobalLock(self)
		finally:
			winBindings.kernel32.GlobalUnlock(self)

	def forget(self):
		"""
		Sets this HGLOBAL value to NULL, forgetting the existing value.
		Necessary if you pass this HGLOBAL to an API that takes ownership and therefore will handle freeing itself.
		"""
		self.value = None


MOVEFILE_COPY_ALLOWED = 0x2
MOVEFILE_CREATE_HARDLINK = 0x10
MOVEFILE_DELAY_UNTIL_REBOOT = 0x4
MOVEFILE_FAIL_IF_NOT_TRACKABLE = 0x20
MOVEFILE_REPLACE_EXISTING = 0x1
MOVEFILE_WRITE_THROUGH = 0x8


def moveFileEx(lpExistingFileName: str, lpNewFileName: str, dwFlags: int):
	# If MoveFileExW fails, Windows will raise appropriate errors.
	if not winBindings.kernel32.MoveFileEx(lpExistingFileName, lpNewFileName, dwFlags):
		raise ctypes.WinError()


# Thread execution states
ES_CONTINUOUS = 0x80000000
ES_DISPLAY_REQUIRED = 0x2
ES_SYSTEM_REQUIRED = 0x1


def SetThreadExecutionState(esFlags):
	res = winBindings.kernel32.SetThreadExecutionState(esFlags)
	if not res:
		raise WinError()
	return res


def LCIDToLocaleName(windowsLCID: LCID) -> Optional[str]:
	# NVDA cannot run with this imported at module level
	from logHandler import log

	dwFlags = 0
	bufferLength = winBindings.kernel32.LCIDToLocaleName(windowsLCID, None, 0, dwFlags)
	if bufferLength == 0:
		# This means that there was an error fetching the LCID.
		# As the buffer is empty, this indicates that the windowsLCID is invalid.
		log.debugWarning(f"Invalid LCID {windowsLCID}")
		return None
	buffer = ctypes.create_unicode_buffer("", bufferLength)
	bufferLength = winBindings.kernel32.LCIDToLocaleName(windowsLCID, buffer, bufferLength, dwFlags)
	if bufferLength == 0:
		# This means that there was an error fetching the LCID.
		# As we have already checked if the LCID is valid by receiveing a non-zero buffer length,
		# something unexpected has failed.
		raise ctypes.WinError()
	return buffer.value
