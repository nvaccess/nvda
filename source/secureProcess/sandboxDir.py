# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt


import os
import shutil

import win32con
import win32file
import win32security
from logHandler import log


class SandboxDirectory:
	"""Manage a sandbox directory with a specified DACL.

	Creates the directory at the given path, applies the provided DACL
	(discretionary access control list), and provides removal semantics
	including scheduling deletion on next reboot if immediate removal fails.
	"""

	def __init__(self, path: str, dacl, autoRemove: bool = False):
		"""Initialize the sandbox directory.

		Creates the directory at the given path (parents are created as needed),
		applies the provided DACL, and records whether the directory should be
		automatically removed when this object is garbage-collected.

		:param path: Filesystem path for the sandbox directory.
		:param dacl: A pywin32 Discretionary access control list to apply to the directory.
		:param autoRemove: If True, the directory will be removed when the
		    object is garbage-collected.
		"""
		log.debug(f"Creating sandbox directory at: {path}...")
		self._path = os.fspath(path)
		self._auto_remove = autoRemove
		self._removed = False
		os.makedirs(self._path, exist_ok=True)
		self._applyDacl(dacl)

	def _applyDacl(self, dacl):
		log.debug("Applying DACL to sandbox directory...")
		win32security.SetNamedSecurityInfo(
			self._path,
			win32security.SE_FILE_OBJECT,
			win32security.DACL_SECURITY_INFORMATION | win32security.PROTECTED_DACL_SECURITY_INFORMATION,
			None,
			None,
			dacl,
			None,
		)

	def _scheduleDeleteOnReboot(self):
		win32file.MoveFileEx(self._path, None, win32con.MOVEFILE_DELAY_UNTIL_REBOOT)

	def remove(self):
		log.debug("Removing sandbox directory...")
		try:
			shutil.rmtree(self._path)
		except OSError:
			log.debug("Failed to remove sandbox directory, scheduling for deletion on next reboot...")
			self._scheduleDeleteOnReboot()
		self._removed = True

	def __del__(self):
		if self._auto_remove and not self._removed:
			self.remove()

	@property
	def path(self) -> str:
		"""the path of the sandbox directory."""
		return self._path
