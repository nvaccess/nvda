# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from typing import ParamSpec
import uuid
import subprocess
import os
import win32con
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
	createRestrictedToken,
	createRestrictedDacl,
	createLeastPrivilegedToken,
	getCurrentPrimaryToken,
	logonUser,
	setTokenIntegrityLevel,
	lookupTokenLogonSidString,
	createTokenEnvironmentBlock,
	getTokenDefaultDacl,
	createSaclFromToken,
	createSecurityDescriptorFromDaclAndSacl,
	impersonateToken,
	getUnelevatedCurrentInteractiveUserTokenFromShell,
	isTokenElevated,
	generateUniqueSandboxSidString,
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

	def __init__(self, argv: list[str], stdin: int | None=None, stdout: int | None=None, stderr: int | None=None, extraEnv: dict[str, str] | None=None, cwd: str | None=None, integrityLevel: str | None=None, removePrivileges: bool=False, removeElevation:bool=False, restrictToken: bool=False, retainUserInRestrictedToken: bool=False, username: str | None=None, domain: str=".", password: str="", logonType: str="interactive", applyUIRestrictions=False, isolateDesktop: bool=False, isolateWindowStation: bool=False, killOnDelete: bool=False, startSuspended: bool=False, hideCriticalErrorDialogs: bool=False):
		"""
		Create and launch a subprocess using optionally a restricted token, particular integrity level, and isolation features.

		This constructor prepares a Windows access token based on the current user (though optionally a service logon token instead), makes a restricted token from that if requested,
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
			working directory is used (or a short-lived sandbox directory with restricted permissions when restrictedToken is True and retainUserInRestrictedToken is False.
		:param integrityLevel: Integrity level to apply to the restricted token (e.g. "low").
		:param removeElevation: If the current token is elevated, obtain an unelevated interactive user token from the shell instead.
		:param removePrivileges: Remove privileges from the token when restricting it.
		:param restrictedToken: Whether to create a restricted token for the child process. The restricted token will have a restricted SID list including the "Restricted" SID and the Logon SID from the source token, as well as interactive group SIDs. Enough to allow basic interactive access, but not enough to access the user's own files or profile data unless retainUserInRestrictedToken is also True.
		:param retainUserInRestrictedToken: Include the user SID from the source token in the restricted SID list, thus granting access to the user's files and profile data.
		:param username: Username to log on as. If provided, a logon token for this user will be created via secLogon and used instead of the current primary token.
		:param domain: Domain of the user to log on as.
		:param password: Password for the user to log on as.
		:param logonType: The type of logon to perform (e.g., "interactive", "service",
		:param applyUIRestrictions: Apply maximum UI restrictions to the process via the Windows job object. Includes switching desktops, changing display settings, exiting windows, reading / writing global atoms, access to UI handles from other processes (includes windows and hooks), clipboard reading/writing, and changing system parameters.
		:param isolateDesktop: Create a temporary desktop for the child process.
		:param isolateWindowStation: Create a temporary window station (implies isolated desktop).
		:param killOnDelete: Assign the child to a job that is terminated when this object is closed.
		:param startSuspended: Start the process suspended; call resume() to continue execution.
		:param hideCriticalErrorDialogs: Suppress critical error dialogs for the spawned process.

When the integrity level is "low", TEMP/TMP are redirected to a LocalLow Temp folder. If
		restrictedtoken is True and retainUserInRestrictedtoken is False a sandbox directory is created and used as the TEMP/TMP and cwd.
		"""
		log.debug(f"Preparing to launch secure process: {subprocess.list2cmdline(argv)}, options: {integrityLevel=}, {removePrivileges=}, {removeElevation=}, {restrictToken=}, {retainUserInRestrictedToken=}, {username=}, {domain=}, {logonType=}, {isolateDesktop=}, {isolateWindowStation=}, {killOnDelete=}, {startSuspended=}, {hideCriticalErrorDialogs=}...")
		useSecLogon = False
		if username:
			log.debug(f"Logging on as user {username=} {domain=} {logonType=}...")
			useSecLogon = True
			token = logonUser(username, domain, password, logonType)
		else:
			log.debug("Fetching current primary token...")
			token = getCurrentPrimaryToken()
		if removeElevation and isTokenElevated(token):
			log.debug("Current token is elevated but removeElevation is requested, obtaining unelevated interactive user token from shell...")
			token = getUnelevatedCurrentInteractiveUserTokenFromShell()
			log.debug("Successfully obtained unelevated interactive user token from shell.")
			log.debug("Ensuring secLogon is used to launch process...")
			useSecLogon = True
		defaultDacl = getTokenDefaultDacl(token)
		if restrictToken:
			uniqueSandboxSidString = generateUniqueSandboxSidString()
			token = createRestrictedToken(token, removePrivilages=removePrivileges, retainUser=retainUserInRestrictedToken, includeExtraSidStrings=[uniqueSandboxSidString])
			if not retainUserInRestrictedToken:
				log.debug("Adding unique sandbox SID to token default DACL")
				defaultDacl.AddAccessAllowedAce(win32security.ACL_REVISION, win32con.GENERIC_ALL, win32security.ConvertStringSidToSid(uniqueSandboxSidString))
				win32security.SetTokenInformation(token, win32security.TokenDefaultDacl, defaultDacl)
		elif removePrivileges:
			token = createLeastPrivilegedToken(token)
		if integrityLevel:
			log.debug(f"Setting token integrity level to {integrityLevel}...")
			setTokenIntegrityLevel(token, integrityLevel)
		defaultSacl = createSaclFromToken(token)
		defaultSD = createSecurityDescriptorFromDaclAndSacl(defaultDacl, defaultSacl)
		desktopName = None
		if isolateWindowStation:
			log.debug("Creating isolated window station and desktop...")
			sa = win32security.SECURITY_ATTRIBUTES()
			sa.SECURITY_DESCRIPTOR = defaultSD
			sa.bInheritHandle = False
			winstaName, self._winstaHandle = createTempWindowStation(securityAttribs=sa)
			with temporarilySwitchWindowStation(self._winstaHandle):
				desktopName, self._desktopHandle = createTempDesktop(securityAttribs=sa)
			desktopName = f"{winstaName}\\{desktopName}"
			log.debug(f"Isolated window station and desktop created: {desktopName}")
		elif isolateDesktop:
			log.debug("Creating isolated desktop...")
			sa = win32security.SECURITY_ATTRIBUTES()
			sa.SECURITY_DESCRIPTOR =defaultSD
			sa.bInheritHandle = False
			desktopName, self._desktopHandle = createTempDesktop(securityAttribs=sa)
			log.debug(f"Isolated desktop created: {desktopName}")
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
		if restrictToken and not retainUserInRestrictedToken:
			temp = env['TEMP']
			sbDirName = f"sandbox_{uuid.uuid4()}"
			self._sandboxDir = SandboxDirectory(os.path.join(temp, sbDirName), defaultDacl, autoRemove=True)
			log.debug(f"Created sandbox directory at {self._sandboxDir.path}, setting TEMP to this path...")
			env["TEMP"] = env['TMP'] = self._sandboxDir.path
		if not cwd:
			with impersonateToken(token):
				cwd = os.getcwd()
				try:
					os.listdir(cwd)
				except (PermissionError, FileNotFoundError):
					cwd = env["TEMP"]
					log.debug(f"Parent working directory not accessible for child process. Using {cwd}...")
		if extraEnv:
			for key, value in extraEnv.items():
				log.debug(f"Adding extra environment variable: {key}={value}...")
				env[key] = value
		log.debug("Launching subprocess with restricted token...")
		super().__init__(HANDLE(int(token)), argv, useSecLogon=useSecLogon, logonFlags=1, env=env, cwd=cwd, desktop=desktopName, stdin=stdin, stdout=stdout, stderr=stderr, startSuspended=True, hideCriticalErrorDialogs=hideCriticalErrorDialogs)
		self.job = Job()
		if killOnDelete:
			self.job.setBasicLimits(JOB_OBJECT_LIMIT.KILL_ON_JOB_CLOSE)
		if applyUIRestrictions:
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
