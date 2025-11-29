# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt


import ctypes
from ctypes import (
	byref,
	sizeof,
)
from ctypes.wintypes import (
	HANDLE,
)
from winBindings.jobapi2 import (
	JobObjectExtendedLimitInformation,
	JOBOBJECT_EXTENDED_LIMIT_INFORMATION,
	JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE,
)
from winBindings.kernel32 import (
	CloseHandle,
	CreateJobObject,
	AssignProcessToJobObject,
	SetInformationJobObject,
)

import logging
log = logging.getLogger(__name__)


class Job:
	"""Manage a Windows Job object.

	This class wraps a Windows Job object, allowing processes to be
	assigned to the job and optionally ensuring all processes are
	terminated when the job handle is closed.
	The job is automatically closed when the Job object is destroyed.
	"""

	def __init__(self, killOnClose: bool=False):
		"""
		Initialize the Job object.

		Create a Windows Job object and optionally configure it so that all
		processes assigned to the job are terminated when the job handle is
		closed.

		:param killOnClose: If True, configure the job to kill processes on
			job-handle close.
		:raises RuntimeError: If creating the job object or setting its
			information fails.
		"""
		log.debug("Creating job object...")
		hJob = CreateJobObject(None, None)
		if not hJob:
			raise RuntimeError(f"Failed to create job object, {ctypes.WinError()}")
		self._hJob = hJob
		if killOnClose:
			log.debug("Setting job object to kill processes on close...")
			limitInfo = JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
			limitInfo.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
			if not SetInformationJobObject(self._hJob, JobObjectExtendedLimitInformation, byref(limitInfo), sizeof(limitInfo)):
				raise RuntimeError(f"Failed to set job object information, {ctypes.WinError()}")

	def assignProcess(self, processHandle: HANDLE):
		"""
		Assign a process to the job object.

		Assign the given process handle to this job so the process becomes
		subject to the job's limits and controls. The caller is responsible for
		providing a valid process handle with the necessary access rights.

		:param processHandle: Handle of the process to assign to the job.
		:raises RuntimeError: If assigning the process to the job fails.
		"""
		log.debug("Assigning process to job object...")
		if not AssignProcessToJobObject(self._hJob, processHandle):
			raise RuntimeError(f"Failed to assign process to job object, {ctypes.WinError()}")

	def close(self):
		""" Closes the job object."""
		if self._hJob:
			log.debug("Closing job object...")
			CloseHandle(self._hJob)
			self._hJob = None

	def __del__(self):
		self.close()
