# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020-2021 NV Access Limited, Łukasz Golonka
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

""" System related functions."""
import ctypes
import winKernel
import shellapi
import winUser
import functools
import shlobj


@functools.lru_cache(maxsize=1)
def hasSyswow64Dir() -> bool:
	"""Returns `True` if the current system has separate system32 directories for 32-bit processes."""
	nativeSys32 = shlobj.SHGetKnownFolderPath(shlobj.FolderId.SYSTEM)
	Syswow64Sys32 = shlobj.SHGetKnownFolderPath(shlobj.FolderId.SYSTEM_X86)
	return nativeSys32 != Syswow64Sys32


def openUserConfigurationDirectory():
	"""Opens directory containing config files for the current user"""
	import globalVars
	shellapi.ShellExecute(0, None, globalVars.appArgs.configPath, None, None, winUser.SW_SHOWNORMAL)


def openDefaultConfigurationDirectory():
	"""Opens the directory which would be used to store configuration by default.
	Used as a fallback when trying to explore user config from the start menu,
	and NVDA is not running."""
	import config
	path = config.getUserDefaultConfigPath()
	if not path:
		raise ValueError("no user default config path")
	config.initConfigPath(path)
	shellapi.ShellExecute(0, None, path, None, None, winUser.SW_SHOWNORMAL)


TokenUIAccess = 26


def hasUiAccess():
	token = ctypes.wintypes.HANDLE()
	ctypes.windll.advapi32.OpenProcessToken(
		ctypes.windll.kernel32.GetCurrentProcess(),
		winKernel.MAXIMUM_ALLOWED,
		ctypes.byref(token)
	)
	try:
		val = ctypes.wintypes.DWORD()
		ctypes.windll.advapi32.GetTokenInformation(
			token,
			TokenUIAccess,
			ctypes.byref(val),
			ctypes.sizeof(ctypes.wintypes.DWORD),
			ctypes.byref(ctypes.wintypes.DWORD())
		)
		return bool(val.value)
	finally:
		ctypes.windll.kernel32.CloseHandle(token)

#: Value from the TOKEN_INFORMATION_CLASS enumeration:
#: https://docs.microsoft.com/en-us/windows/win32/api/winnt/ne-winnt-token_information_class
#: When calling The Win32 GetTokenInformation function, the buffer receives a TOKEN_ORIGIN value.
#: If the token resulted from a logon that used explicit credentials, such as passing a name, domain,
#: and password to the LogonUser function, then the TOKEN_ORIGIN structure will contain the ID of
#: the logon session that created it.
#: If the token resulted from network authentication, then this value will be zero.
TOKEN_ORIGIN = 17  # TokenOrigin in winnt.h


class TokenOrigin(ctypes.Structure):
	"""TOKEN_ORIGIN structure: https://docs.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-token_origin
	This structure is used in calls to the Win32 GetTokenInformation function.
	"""
	_fields_ = [
		("originatingLogonSession", ctypes.c_ulonglong)  # OriginatingLogonSession in C structure
	]


def getProcessTokenOrigin(processHandle: int) -> TokenOrigin:
	token = ctypes.wintypes.HANDLE()
	if not ctypes.windll.advapi32.OpenProcessToken(
		processHandle,
		winKernel.MAXIMUM_ALLOWED,
		ctypes.byref(token)
	):
		raise ctypes.WinError()
	try:
		val = TokenOrigin()
		if not ctypes.windll.advapi32.GetTokenInformation(
			token,
			TOKEN_ORIGIN,
			ctypes.byref(val),
			ctypes.sizeof(val),
			ctypes.byref(ctypes.wintypes.DWORD())
		):
			raise ctypes.WinError()
		return val
	finally:
		ctypes.windll.kernel32.CloseHandle(token)


def getProcessLogonSessionId(processHandle: int) -> int:
	return getProcessTokenOrigin(processHandle).originatingLogonSession


@functools.lru_cache(maxsize=1)
def getCurrentProcessLogonSessionId() -> int:
	return getProcessLogonSessionId(winKernel.GetCurrentProcess())


def execElevated(path, params=None, wait=False, handleAlreadyElevated=False):
	import subprocess
	if params is not None:
		params = subprocess.list2cmdline(params)
	sei = shellapi.SHELLEXECUTEINFO(lpFile=path, lpParameters=params, nShow=winUser.SW_HIDE)
	# IsUserAnAdmin is apparently deprecated so may not work above Windows 8
	if not handleAlreadyElevated or not ctypes.windll.shell32.IsUserAnAdmin():
		sei.lpVerb = "runas"
	if wait:
		sei.fMask = shellapi.SEE_MASK_NOCLOSEPROCESS
	shellapi.ShellExecuteEx(sei)
	if wait:
		try:
			h = ctypes.wintypes.HANDLE(sei.hProcess)
			msg = ctypes.wintypes.MSG()
			while ctypes.windll.user32.MsgWaitForMultipleObjects(1, ctypes.byref(h), False, -1, 255) == 1:
				while ctypes.windll.user32.PeekMessageW(ctypes.byref(msg), None, 0, 0, 1):
					ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
					ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))
			return winKernel.GetExitCodeProcess(sei.hProcess)
		finally:
			winKernel.closeHandle(sei.hProcess)
