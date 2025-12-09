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
	JOBOBJECTINFOCLASS,
	JOB_OBJECT_LIMIT,
	JOBOBJECT_EXTENDED_LIMIT_INFORMATION,
	JOBOBJECT_BASIC_UI_RESTRICTIONS,
	JOB_OBJECT_UILIMIT,
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

	def __init__(self):
		"""
		Initialize the Job object.

		Create a Windows Job object.
		"""
		log.debug("Creating job object...")
		hJob = CreateJobObject(None, None)
		if not hJob:
			raise RuntimeError(f"Failed to create job object, {ctypes.WinError()}")
		self._hJob = hJob

	def setBasicLimits(self, basicLimitFlags: JOB_OBJECT_LIMIT):
		log.debug(f"Limit flags: {basicLimitFlags.name}...")
		limitInfo = JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
		limitInfo.BasicLimitInformation.LimitFlags = basicLimitFlags
		if not SetInformationJobObject(self._hJob, JOBOBJECTINFOCLASS.ExtendedLimitInformation, byref(limitInfo), sizeof(limitInfo)):
			raise RuntimeError(f"Failed to set job object information, {ctypes.WinError()}")

	def setUiRestrictions(self, uiLimitFlags: JOB_OBJECT_UILIMIT):
		log.debug(f"UI limit flags: {uiLimitFlags.name}...")
		uiRestrictions = JOBOBJECT_BASIC_UI_RESTRICTIONS()
		uiRestrictions.UIRestrictionsClass = uiLimitFlags
		if not SetInformationJobObject(self._hJob, JOBOBJECTINFOCLASS.BasicUIRestrictions, byref(uiRestrictions), sizeof(uiRestrictions)):
			raise RuntimeError(f"Failed to set job object UI restrictions, {ctypes.WinError()}")

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
