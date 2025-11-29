# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from typing import ParamSpec
import uuid
import subprocess
import os
import win32security
from ctypes.wintypes import (
	HANDLE,
)
from winBindings.user32 import (
	DESKTOP_ALL_ACCESS,
)
from .childProcess import (
	PopenWithToken,
)
from .token import (
	restrictToken,
	getCurrentPrimaryToken,
	createServiceLogon,
	setTokenIntegrityLevel,
	lookupTokenLogonSidString,
	createTokenEnvironmentBlock,
	createRestrictedSecurityDescriptor,
)
from .desktop import (
	createTempDesktop,
	createTempWindowStation,
	temporarilySwitchWindowStation,
)
from .job import (
	Job,
	JOB_OBJECT_LIMIT,
	JOB_OBJECT_UILIMIT,
)
from .sandboxDir import (
	SandboxDirectory,
)

import logging
log = logging.getLogger(__name__)

class SecurePopen(PopenWithToken):
	"""
	Spawns a process with a restricted token and various isolation options.
	"""

	def __init__(self, argv: list[str], stdin: int | None=None, stdout: int | None=None, stderr: int | None=None, extraEnv: dict[str, str] | None=None, cwd: str | None=None, integrityLevel: str | None="low", removePrivileges: bool=True, allowUser: bool=True, disableDangerousSids: bool=True, runAsLocalService: bool=False, applyUIRestrictions=True, isolateDesktop: bool=False, isolateWindowStation: bool=False, killOnDelete: bool=True, startSuspended: bool=False, hideCriticalErrorDialogs: bool=False):
		"""
		Create and launch a subprocess using a restricted token and optional isolation features.

		This constructor prepares a restricted security token (optionally a service logon token),
		configures integrity level and default DACLs, adjusts the environment for low integrity
		processes, optionally creates an isolated desktop and/or window station, and spawns
		the child process using PopenWithToken. The created process is assigned to a Job so it
		can be terminated automatically when this object is cleaned up.

		:param argv: Command line to execute (program and arguments).
		:param stdin: File descriptor or handle to use for standard input, or None. if subprocessPIPE, then a pipe to the child will be created.
		:param stdout: File descriptor or handle to use for standard output, or None. if subprocessPIPE, then a pipe from the child will be created.
		:param stderr: File descriptor or handle to use for standard error, or None. if subprocessPIPE, then a pipe from the child will be created.
		:param extraEnv: Additional environment variables to add to the process environment.
		:param cwd: Working directory for the child process. If not provided, the current
			working directory is used (or a short-lived sandbox directory with restricted permissions when allowUser is False).
		:param integrityLevel: Integrity level to apply to the restricted token (e.g. "low").
		:param removePrivileges: Remove privileges from the token when restricting it.
		:param allowUser: Whether the user's SID should be allowed in the restricted token.
		:param disableDangerousSids: Disable well-known dangerous SIDs when restricting the token.
		:param runAsLocalService: Use a local service logon token instead of the current primary token.
		:param applyUIRestrictions: Apply maximum UI restrictions to the process via the Windows job object. Includes switching desktops, changing display settings, exiting windows, reading / writing global atoms, access to UI handles from other processes (includes windows and hooks), clipboard reading/writing, and changing system parameters.
		:param isolateDesktop: Create a temporary desktop for the child process.
		:param isolateWindowStation: Create a temporary window station (implies isolated desktop).
		:param killOnDelete: Assign the child to a job that is terminated when this object is closed.
		:param startSuspended: Start the process suspended; call resume() to continue execution.
		:param hideCriticalErrorDialogs: Suppress critical error dialogs for the spawned process.

When the integrity level is "low", TEMP/TMP are redirected to a LocalLow Temp folder. If
		allowUser is False a sandbox directory is created and used as the TEMP/TMP and cwd.
		"""
		log.debug(f"Preparing to launch secure process: {subprocess.list2cmdline(argv)}, options: integrityLevel={integrityLevel}, removePrivileges={removePrivileges}, allowUser={allowUser}, disableDangerousSids={disableDangerousSids}, runAsLocalService={runAsLocalService}, isolateDesktop={isolateDesktop}, isolateWindowStation={isolateWindowStation}, killOnDelete={killOnDelete}, startSuspended={startSuspended}, hideCriticalErrorDialogs={hideCriticalErrorDialogs}...")
		if runAsLocalService:
			log.debug("runAsLocalService requested, creating service logon token and ensuring secLogon is used to launch process...")
			useSecLogon = True
			token = createServiceLogon()
		else:
			log.debug("Using current primary token as basis for child process token")
			useSecLogon = False
			token = getCurrentPrimaryToken()
		log.debug("Preparing restricted DACL for sandboxing, using unique Logon session SID ...")
		logonSidString = lookupTokenLogonSidString(token)
		restrictedSD = createRestrictedSecurityDescriptor(logonSidString, integrityLevel=integrityLevel, includeSystem=True, includeAdministrators=True, includeMe=True)
		desktopName = None
		if isolateWindowStation:
			log.debug("Creating isolated window station and desktop with restricted security descriptor...")
			sa = win32security.SECURITY_ATTRIBUTES()
			sa.SECURITY_DESCRIPTOR = restrictedSD
			sa.bInheritHandle = False
			winstaName, self._winstaHandle = createTempWindowStation(securityAttribs=sa)
			with temporarilySwitchWindowStation(self._winstaHandle):
				desktopName, self._desktopHandle = createTempDesktop(securityAttribs=sa)
			desktopName = f"{winstaName}\\{desktopName}"
			log.debug(f"Isolated window station and desktop created: {desktopName}")
		elif isolateDesktop:
			log.debug("Creating isolated desktop with restricted security descriptor...")
			sa = win32security.SECURITY_ATTRIBUTES()
			sa.SECURITY_DESCRIPTOR = restrictedSD
			sa.bInheritHandle = False
			desktopName, self._desktopHandle = createTempDesktop(securityAttribs=sa)
			log.debug(f"Isolated desktop created: {desktopName}")
		log.debug(f"Preparing restricted token, removePrivileges={removePrivileges}, allowUser={allowUser}, disableDangerousSids={disableDangerousSids}...")
		token = restrictToken(token, removePrivilages=removePrivileges, allowUser=allowUser, disableDangerousSids=disableDangerousSids)
		if not allowUser:
			log.debug("Ensuring restricted token has an appropriate default DACL  so  it can access its own sandbox directory and handles...")
			dacl = restrictedSD.GetSecurityDescriptorDacl()
			win32security.SetTokenInformation(token, win32security.TokenDefaultDacl, dacl)
		if integrityLevel:
			log.debug(f"Setting token integrity level to {integrityLevel}...")
			setTokenIntegrityLevel(token, integrityLevel)
		log.debug("Preparing environment variables appropriate for token...")
		env = createTokenEnvironmentBlock(token)
		if integrityLevel == "low":
			userProfile = env["USERPROFILE"]
			localLow = os.path.join(userProfile, "AppData", "LocalLow")
			temp = os.path.join(localLow, "Temp")
			os.makedirs(temp, exist_ok=True)
			log.debug(f"Setting TEMP and TMP to low integrity Temp folder {temp}...")
			env["TEMP"] = temp
			env["TMP"] = temp
		if not allowUser:
			temp = env['TEMP']
			sbDirName = f"sandbox_{uuid.uuid4()}"
			dacl = restrictedSD.GetSecurityDescriptorDacl()
			self._sandboxDir = SandboxDirectory(os.path.join(temp, sbDirName), dacl, autoRemove=True)
			log.debug(f"Created sandbox directory at {self._sandboxDir.path}, setting TEMP to this path...")
			env["TEMP"] = env['TMP'] = self._sandboxDir.path
			if not cwd:
				log.debug("Setting working directory to sandbox directory...")
				cwd = self._sandboxDir.path
		if extraEnv:
			for key, value in extraEnv.items():
				log.debug(f"Adding extra environment variable: {key}={value}...")
				env[key] = value
		log.debug("Launching subprocess with restricted token...")
		super().__init__(HANDLE(int(token)), argv, useSecLogon=useSecLogon, logonFlags=1, env=env, cwd=cwd, desktop=desktopName, stdin=stdin, stdout=stdout, stderr=stderr, startSuspended=True, hideCriticalErrorDialogs=hideCriticalErrorDialogs)
		self.job = Job()
		if killOnDelete:
			self.job.setBasicLimits(JOB_OBJECT_LIMIT.KILL_ON_JOB_CLOSE)
		self.job.setUiRestrictions(
			JOB_OBJECT_UILIMIT.DESKTOP
			| JOB_OBJECT_UILIMIT.DISPLAYSETTINGS
			| JOB_OBJECT_UILIMIT.EXITWINDOWS
			| JOB_OBJECT_UILIMIT.GLOBALATOMS
			| JOB_OBJECT_UILIMIT.HANDLES
			| JOB_OBJECT_UILIMIT.READCLIPBOARD
			| JOB_OBJECT_UILIMIT.SYSTEMPARAMETERS
			| JOB_OBJECT_UILIMIT.WRITECLIPBOARD
		)
		self.job.assignProcess(self._handle)
		if not startSuspended:
			log.debug("Resuming process execution...")
			self.resume()
