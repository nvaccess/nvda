# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Windows handle ownership helpers shared by both sides of the ART boundary."""

from __future__ import annotations

import msvcrt
import os
from ctypes import WinError, byref
from ctypes.wintypes import HANDLE

import winKernel
from winBindings.kernel32 import DuplicateHandle, GetCurrentProcess


def duplicateHandleForSelf(handle: int) -> int:
	"""Duplicate a handle within this process, with the same access as the original.

	The duplicate is independent of ``handle``: closing one does not close the other.

	:param handle: Handle to duplicate.
	:returns: The value of an independent handle to the same object.
	:raises OSError: If duplication fails.
	"""
	duplicate = HANDLE()
	currentProcess = GetCurrentProcess()
	if not DuplicateHandle(
		currentProcess,
		HANDLE(int(handle)),
		currentProcess,
		byref(duplicate),
		0,
		False,
		winKernel.DUPLICATE_SAME_ACCESS,
	):
		raise WinError()
	return duplicate.value


def duplicateHandleIntoProcess(handle: HANDLE, accessMask: int, targetProcess: int) -> HANDLE:
	"""Duplicate a handle so it is valid in another process.

	:param handle: Handle to duplicate.
	:param accessMask: Desired access for the duplicate.
	:param targetProcess: Handle of the process to duplicate into.
	:returns: A handle valid in ``targetProcess``.
	:raises OSError: If duplication fails.
	"""
	duplicate = HANDLE()
	if not DuplicateHandle(
		GetCurrentProcess(),
		handle,
		targetProcess,
		byref(duplicate),
		accessMask,
		False,
		0,
	):
		raise WinError()
	return duplicate


def claimHandleFromDescriptor(fd: int) -> int:
	"""Take sole ownership of the kernel handle behind a C runtime file descriptor.

	Returns a handle that is independent of ``fd`, but which points to the same object.
	Closes ``fd`` if successful.

	:param fd: Descriptor to claim. Closed on success, and left open if duplication fails.
	:returns: The value of a handle to the same object, owned by the caller.
	:raises OSError: If ``fd`` is not a valid descriptor, or duplication fails.
	"""
	handle = duplicateHandleForSelf(msvcrt.get_osfhandle(fd))
	os.close(fd)
	return handle
