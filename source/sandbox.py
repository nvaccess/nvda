#!/usr/bin/env python3
"""
Mos Eisley: Windows Process Sandbox
A wretched hive where scum and villainy can be safely contained.

This library provides Windows process sandboxing using restricted tokens,
job objects, low integrity levels, and directory restrictions.
"""

import os
import sys
import subprocess
import ctypes
import logging
from ctypes import wintypes
from dataclasses import dataclass

# Windows-specific imports
try:
	import win32api
	import win32con
	import win32event  # noqa: F401
	import win32job
	import win32process
	import win32security
	import ntsecuritycon  # noqa: F401
	import pywintypes
except ImportError as e:
	raise ImportError("Mos Eisley requires pywin32. Install with: pip install pywin32") from e

__version__ = "1.0.0"
__all__ = [
	"SandboxConfig",
	"SandboxPopen",
]

# ============================================================================
# Windows ctypes helpers (extracted from windows_ctypes.py)
# ============================================================================

from ctypes import (
	POINTER,
	Structure,
	WinDLL,
	c_char_p,
	c_int,
	c_size_t,
	c_void_p,
	windll,
)
from ctypes.wintypes import BOOL, DWORD, HANDLE, LPCWSTR, LPWSTR, ULONG, WORD

kernel32 = WinDLL("kernel32", use_last_error=True)
shell32 = WinDLL("shell32", use_last_error=True)
advapi32 = WinDLL("advapi32", use_last_error=True)

SIZE_T = c_size_t
PVOID = c_void_p
LPVOID = PVOID
LPTSTR = c_void_p
LPBYTE = c_char_p

# Windows structures


class PROC_THREAD_ATTRIBUTE_ENTRY(Structure):
	_fields_ = [
		("Attribute", DWORD),
		("cbSize", SIZE_T),
		("lpValue", PVOID),
	]


PULONG = POINTER(ULONG)


class PROC_THREAD_ATTRIBUTE_LIST(Structure):
	_fields_ = [
		("dwFlags", DWORD),
		("Size", ULONG),
		("Count", ULONG),
		("Reserved", ULONG),
		("Unknown", PULONG),
		("Entries", PROC_THREAD_ATTRIBUTE_ENTRY * 1),
	]


class STARTUPINFO(Structure):
	_fields_ = [
		("cb", DWORD),
		("lpReserved", LPTSTR),
		("lpDesktop", LPTSTR),
		("lpTitle", LPTSTR),
		("dwX", DWORD),
		("dwY", DWORD),
		("dwXSize", DWORD),
		("dwYSize", DWORD),
		("dwXCountChars", DWORD),
		("dwYCountChars", DWORD),
		("dwFillAttribute", DWORD),
		("dwFlags", DWORD),
		("wShowWindow", WORD),
		("cbReserved2", WORD),
		("lpReserved2", LPBYTE),
		("hStdInput", HANDLE),
		("hStdOutput", HANDLE),
		("hStdError", HANDLE),
	]


PPROC_THREAD_ATTRIBUTE_LIST = POINTER(PROC_THREAD_ATTRIBUTE_LIST)


class STARTUPINFOEX(Structure):
	_fields_ = [
		("StartupInfo", STARTUPINFO),
		("lpAttributeList", LPVOID),
	]


class PROCESS_INFORMATION(Structure):
	_fields_ = [
		("hProcess", HANDLE),
		("hThread", HANDLE),
		("dwProcessId", DWORD),
		("dwThreadId", DWORD),
	]


# Privilege constants
SE_ASSIGNPRIMARYTOKEN_NAME = "SeAssignPrimaryTokenPrivilege"
SE_AUDIT_NAME = "SeAuditPrivilege"
SE_BACKUP_NAME = "SeBackupPrivilege"
SE_CHANGE_NOTIFY_NAME = "SeChangeNotifyPrivilege"
SE_CREATE_GLOBAL_NAME = "SeCreateGlobalPrivilege"
SE_CREATE_PAGEFILE_NAME = "SeCreatePagefilePrivilege"
SE_CREATE_PERMANENT_NAME = "SeCreatePermanentPrivilege"
SE_CREATE_SYMBOLIC_LINK_NAME = "SeCreateSymbolicLinkPrivilege"
SE_CREATE_TOKEN_NAME = "SeCreateTokenPrivilege"
SE_DEBUG_NAME = "SeDebugPrivilege"
SE_ENABLE_DELEGATION_NAME = "SeEnableDelegationPrivilege"
SE_IMPERSONATE_NAME = "SeImpersonatePrivilege"
SE_INC_BASE_PRIORITY_NAME = "SeIncreaseBasePriorityPrivilege"
SE_INCREASE_QUOTA_NAME = "SeIncreaseQuotaPrivilege"
SE_INC_WORKING_SET_NAME = "SeIncreaseWorkingSetPrivilege"
SE_LOAD_DRIVER_NAME = "SeLoadDriverPrivilege"
SE_LOCK_MEMORY_NAME = "SeLockMemoryPrivilege"
SE_MACHINE_ACCOUNT_NAME = "SeMachineAccountPrivilege"
SE_MANAGE_VOLUME_NAME = "SeManageVolumePrivilege"
SE_PROF_SINGLE_PROCESS_NAME = "SeProfileSingleProcessPrivilege"
SE_RELABEL_NAME = "SeRelabelPrivilege"
SE_REMOTE_SHUTDOWN_NAME = "SeRemoteShutdownPrivilege"
SE_RESTORE_NAME = "SeRestorePrivilege"
SE_SECURITY_NAME = "SeSecurityPrivilege"
SE_SHUTDOWN_NAME = "SeShutdownPrivilege"
SE_SYNC_AGENT_NAME = "SeSyncAgentPrivilege"
SE_SYSTEM_ENVIRONMENT_NAME = "SeSystemEnvironmentPrivilege"
SE_SYSTEM_PROFILE_NAME = "SeSystemProfilePrivilege"
SE_SYSTEMTIME_NAME = "SeSystemtimePrivilege"
SE_TAKE_OWNERSHIP_NAME = "SeTakeOwnershipPrivilege"
SE_TCB_NAME = "SeTcbPrivilege"
SE_TIME_ZONE_NAME = "SeTimeZonePrivilege"
SE_TRUSTED_CREDMAN_ACCESS_NAME = "SeTrustedCredManAccessPrivilege"
SE_UNDOCK_NAME = "SeUndockPrivilege"
SE_UNSOLICITED_INPUT_NAME = "SeUnsolicitedInputPrivilege"

# Privilege attributes
SE_PRIVILEGE_ENABLED_BY_DEFAULT = 0x00000001
SE_PRIVILEGE_ENABLED = 0x00000002
SE_PRIVILEGE_REMOVED = 0x00000004
SE_PRIVILEGE_USED_FOR_ACCESS = 0x80000000

# Standard access rights
SYNCHRONIZE = 0x00100000

# Token access rights
TOKEN_ADJUST_PRIVILEGES = 0x00000020
TOKEN_QUERY = 0x00000008

# Process access rights
PROCESS_CREATE_PROCESS = 0x0080
PROCESS_CREATE_THREAD = 0x0002
PROCESS_DUP_HANDLE = 0x0040
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
PROCESS_SET_INFORMATION = 0x0200
PROCESS_SET_QUOTA = 0x0100
PROCESS_SUSPEND_RESUME = 0x0800
PROCESS_TERMINATE = 0x0001
PROCESS_VM_OPERATION = 0x0008
PROCESS_VM_READ = 0x0010
PROCESS_VM_WRITE = 0x0020
PROCESS_ALL_ACCESS = (
	PROCESS_CREATE_PROCESS
	| PROCESS_CREATE_THREAD
	| PROCESS_DUP_HANDLE
	| PROCESS_QUERY_INFORMATION
	| PROCESS_QUERY_LIMITED_INFORMATION
	| PROCESS_SET_INFORMATION
	| PROCESS_SET_QUOTA
	| PROCESS_SUSPEND_RESUME
	| PROCESS_TERMINATE
	| PROCESS_VM_OPERATION
	| PROCESS_VM_READ
	| PROCESS_VM_WRITE
	| SYNCHRONIZE
)

# Process creation flags
CREATE_NEW_CONSOLE = 0x00000010
EXTENDED_STARTUPINFO_PRESENT = 0x00080000

# UpdateProcThreadAttribute attributes
ProcThreadAttributeParentProcess = 0
PROC_THREAD_ATTRIBUTE_INPUT = 0x00020000
PROC_THREAD_ATTRIBUTE_PARENT_PROCESS = ProcThreadAttributeParentProcess | PROC_THREAD_ATTRIBUTE_INPUT

# Error codes
ERROR_NO_TOKEN = 0x03F0

# Generic access rights
GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
GENERIC_EXECUTE = 0x20000000
GENERIC_ALL = 0x10000000
MAXIMUM_ALLOWED = 0x02000000
ACCESS_SYSTEM_SECURITY = 0x01000000

# Standard rights
DELETE = 0x00010000
READ_CONTROL = 0x00020000
WRITE_DAC = 0x00040000
WRITE_OWNER = 0x00080000
STANDARD_RIGHTS_READ = READ_CONTROL
STANDARD_RIGHTS_WRITE = READ_CONTROL
STANDARD_RIGHTS_EXECUTE = READ_CONTROL
STANDARD_RIGHTS_REQUIRED = DELETE | READ_CONTROL | WRITE_DAC | WRITE_OWNER
STANDARD_RIGHTS_ALL = STANDARD_RIGHTS_REQUIRED | SYNCHRONIZE

# Token rights
TOKEN_ASSIGN_PRIMARY = 0x0001
TOKEN_DUPLICATE = 0x0002
TOKEN_IMPERSONATE = 0x0004
TOKEN_QUERY_SOURCE = 0x0010
TOKEN_ADJUST_GROUPS = 0x0040
TOKEN_ADJUST_DEFAULT = 0x0080
TOKEN_ADJUST_SESSIONID = 0x0100
TOKEN_ALL_ACCESS = (
	STANDARD_RIGHTS_REQUIRED
	| TOKEN_ASSIGN_PRIMARY
	| TOKEN_DUPLICATE
	| TOKEN_IMPERSONATE
	| TOKEN_QUERY
	| TOKEN_QUERY_SOURCE
	| TOKEN_ADJUST_PRIVILEGES
	| TOKEN_ADJUST_GROUPS
	| TOKEN_ADJUST_DEFAULT
	| TOKEN_ADJUST_SESSIONID
)

# Group attributes
SE_GROUP_MANDATORY = 0x00000001
SE_GROUP_ENABLED_BY_DEFAULT = 0x00000002
SE_GROUP_ENABLED = 0x00000004
SE_GROUP_OWNER = 0x00000008
SE_GROUP_USE_FOR_DENY_ONLY = 0x00000010
SE_GROUP_INTEGRITY = 0x00000020
SE_GROUP_INTEGRITY_ENABLED = 0x00000040
SE_GROUP_RESOURCE = 0x20000000
SE_GROUP_LOGON_ID = 0xC0000000

# Token information classes
TokenIntegrityLevel = 25

# Well-known SID types
WinUntrustedLabelSid = 65
WinLowLabelSid = 66
WinMediumLabelSid = 67
WinHighLabelSid = 68
WinSystemLabelSid = 69

PSID = POINTER(ctypes.c_char)


class SID_AND_ATTRIBUTES(ctypes.Structure):
	_fields_ = [("Sid", PSID), ("Attributes", wintypes.DWORD)]


class TOKEN_MANDATORY_LABEL(ctypes.Structure):
	_fields_ = [
		("Label", SID_AND_ATTRIBUTES),
	]


# Function prototypes
PDWORD = POINTER(DWORD)
PSIZE_T = POINTER(SIZE_T)
LPSECURITY_ATTRIBUTES = LPVOID
LPPROC_THREAD_ATTRIBUTE_LIST = PPROC_THREAD_ATTRIBUTE_LIST

# GetLastError
GetLastError = windll.kernel32.GetLastError
GetLastError.restype = DWORD

# GetCurrentProcess
GetCurrentProcess = kernel32.GetCurrentProcess
GetCurrentProcess.restype = HANDLE

# OpenProcessToken
OpenProcessToken = advapi32.OpenProcessToken
OpenProcessToken.restype = BOOL
OpenProcessToken.argtypes = [HANDLE, DWORD, POINTER(HANDLE)]

# GetTokenInformation
GetTokenInformation = advapi32.GetTokenInformation
GetTokenInformation.restype = BOOL
GetTokenInformation.argtypes = [HANDLE, c_int, LPVOID, DWORD, PDWORD]

# InitializeProcThreadAttributeList
InitializeProcThreadAttributeList = kernel32.InitializeProcThreadAttributeList
InitializeProcThreadAttributeList.restype = BOOL
InitializeProcThreadAttributeList.argtypes = [LPPROC_THREAD_ATTRIBUTE_LIST, DWORD, DWORD, PSIZE_T]

# UpdateProcThreadAttribute
UpdateProcThreadAttribute = kernel32.UpdateProcThreadAttribute
UpdateProcThreadAttribute.restype = BOOL
UpdateProcThreadAttribute.argtypes = [
	LPPROC_THREAD_ATTRIBUTE_LIST,
	DWORD,
	DWORD,
	PVOID,
	SIZE_T,
	PVOID,
	PSIZE_T,
]

# CreateProcess
CreateProcess = kernel32.CreateProcessW
CreateProcess.restype = BOOL
CreateProcess.argtypes = [
	LPCWSTR,
	LPWSTR,
	LPSECURITY_ATTRIBUTES,
	LPSECURITY_ATTRIBUTES,
	BOOL,
	DWORD,
	LPVOID,
	LPCWSTR,
	POINTER(STARTUPINFOEX),
	POINTER(PROCESS_INFORMATION),
]

# DeleteProcThreadAttributeList
DeleteProcThreadAttributeList = kernel32.DeleteProcThreadAttributeList
DeleteProcThreadAttributeList.restype = None
DeleteProcThreadAttributeList.argtypes = [LPPROC_THREAD_ATTRIBUTE_LIST]

# CloseHandle
CloseHandle = kernel32.CloseHandle
CloseHandle.restype = BOOL
CloseHandle.argtypes = [HANDLE]

# CreateWellKnownSid function signature
advapi32.CreateWellKnownSid.argtypes = [
	ctypes.c_int,  # WELL_KNOWN_SID_TYPE
	ctypes.c_void_p,  # PSID DomainSid (optional)
	ctypes.c_void_p,  # PSID pSid
	POINTER(DWORD),  # DWORD *cbSid
]
advapi32.CreateWellKnownSid.restype = BOOL

# EqualSid
EqualSid = advapi32.EqualSid
EqualSid.restype = BOOL
EqualSid.argtypes = [PVOID, PVOID]

# GetLengthSid
GetLengthSid = advapi32.GetLengthSid
GetLengthSid.restype = DWORD
GetLengthSid.argtypes = [PVOID]


def create_well_known_sid(well_known_sid_type, domain_sid=None):
	"""Create a well-known SID in ctypes format."""
	cbSid = wintypes.DWORD()
	advapi32.CreateWellKnownSid(well_known_sid_type, domain_sid, None, ctypes.byref(cbSid))
	if cbSid.value:
		Sid = (ctypes.c_char * cbSid.value)()
		if advapi32.CreateWellKnownSid(well_known_sid_type, domain_sid, Sid, ctypes.byref(cbSid)):
			return Sid
	raise ctypes.WinError(ctypes.get_last_error())


integrity_level_sid = {
	"untrusted": create_well_known_sid(WinUntrustedLabelSid),
	"low": create_well_known_sid(WinLowLabelSid),
	"medium": create_well_known_sid(WinMediumLabelSid),
	"high": create_well_known_sid(WinHighLabelSid),
	"system": create_well_known_sid(WinSystemLabelSid),
}


def _equal_sid_buffers(sid1_buffer, sid2_buffer):
	"""Compare two SID buffers."""
	return advapi32.EqualSid(sid1_buffer, sid2_buffer)


# ============================================================================
# Configuration
# ============================================================================


@dataclass
class SandboxConfig:
	"""
	Configuration for sandbox security features.

	Each boolean flag controls whether a specific security feature is enabled.
	Users can create custom configurations by setting these flags.
	"""

	# Token restrictions
	enable_restricted_token: bool = True
	"""Create a restricted security token for the process."""

	enable_privilege_removal: bool = True
	"""Remove dangerous privileges like SE_DEBUG_NAME, SE_TCB_NAME, SE_BACKUP_NAME,
    SE_RESTORE_NAME, SE_SHUTDOWN_NAME, SE_LOAD_DRIVER_NAME, SE_SYSTEM_PROFILE_NAME."""

	enable_low_integrity: bool = True
	"""Run the process at low integrity level (prevents writing to most system locations)."""

	enable_sid_restrictions: bool = True
	"""Enable Security Identifier (SID) restrictions on the token."""

	restrict_user_sid: bool = True
	"""Disable the current user SID in the restricted token.
    WARNING: This prevents access to user files and directories.
    Set to False if the process needs to access user data/addons."""

	# Job object restrictions
	enable_job_object: bool = True
	"""Create a job object to contain and limit the process."""

	enable_memory_limits: bool = True
	"""Limit process memory usage to 100MB."""

	enable_process_limits: bool = True
	"""Limit the number of active processes in the job to 1."""

	enable_ui_restrictions: bool = True
	"""Prevent the process from creating/switching desktops and accessing clipboard.
    Specifically blocks: JOB_OBJECT_UILIMIT_DESKTOP, JOB_OBJECT_UILIMIT_READCLIPBOARD,
    JOB_OBJECT_UILIMIT_WRITECLIPBOARD."""

	enable_kill_on_job_close: bool = True
	"""Automatically terminate the process when the job object is closed."""

	# Process creation flags
	enable_suspended_creation: bool = True
	"""Create the process in suspended state initially (for setup before execution)."""

	def log_config(self):
		"""Log the current configuration"""
		logger.info("=" * 60)
		logger.info("Sandbox Configuration")
		logger.info("=" * 60)
		logger.info("Token Restrictions:")
		logger.info(f"  Restricted Token: {'ENABLED' if self.enable_restricted_token else 'DISABLED'}")
		logger.info(f"  Privilege Removal: {'ENABLED' if self.enable_privilege_removal else 'DISABLED'}")
		logger.info(f"  Low Integrity: {'ENABLED' if self.enable_low_integrity else 'DISABLED'}")
		logger.info(f"  SID Restrictions: {'ENABLED' if self.enable_sid_restrictions else 'DISABLED'}")
		logger.info(f"  Restrict User SID: {'ENABLED' if self.restrict_user_sid else 'DISABLED'}")
		logger.info("Job Object Restrictions:")
		logger.info(f"  Job Object: {'ENABLED' if self.enable_job_object else 'DISABLED'}")
		logger.info(f"  Memory Limits: {'ENABLED' if self.enable_memory_limits else 'DISABLED'}")
		logger.info(f"  Process Limits: {'ENABLED' if self.enable_process_limits else 'DISABLED'}")
		logger.info(f"  UI Restrictions: {'ENABLED' if self.enable_ui_restrictions else 'DISABLED'}")
		logger.info(f"  Kill on Job Close: {'ENABLED' if self.enable_kill_on_job_close else 'DISABLED'}")
		logger.info("Process Creation:")
		logger.info(f"  Suspended Creation: {'ENABLED' if self.enable_suspended_creation else 'DISABLED'}")
		logger.info("=" * 60)


# ============================================================================
# Logging
# ============================================================================
# Create module logger - no automatic configuration for libraries
logger = logging.getLogger(__name__)


# ============================================================================
# Token Creation (extracted from launcher.py)
# ============================================================================


def create_restricted_token(config: SandboxConfig):
	"""Create a restricted token based on configuration settings."""
	if not config.enable_restricted_token:
		logger.info("Restricted token creation DISABLED by config")
		return None

	try:
		current_process = win32api.GetCurrentProcess()
		token_handle = win32security.OpenProcessToken(current_process, win32security.TOKEN_ALL_ACCESS)

		privileges_to_delete = []
		sids_to_disable = []

		if config.enable_privilege_removal:
			privilege_constants = [
				win32security.SE_DEBUG_NAME,
				win32security.SE_TCB_NAME,
				win32security.SE_CREATE_PERMANENT_NAME,
				win32security.SE_BACKUP_NAME,
				win32security.SE_RESTORE_NAME,
				win32security.SE_SHUTDOWN_NAME,
				win32security.SE_LOAD_DRIVER_NAME,
				win32security.SE_SYSTEM_PROFILE_NAME,
			]

			for priv_const in privilege_constants:
				try:
					luid = win32security.LookupPrivilegeValue(None, priv_const)
					privileges_to_delete.append((luid, 0))
				except pywintypes.error as e:
					logger.debug(f"Info: Could not lookup privilege {priv_const}: {e}")

			logger.info(f"Removing {len(privileges_to_delete)} privileges")
		else:
			logger.info("Privilege removal DISABLED by config")

		if config.enable_sid_restrictions:
			logger.debug("Preparing SID restrictions for user directory access control...")
			try:
				# Get current user SID
				user_sid = win32security.GetTokenInformation(token_handle, win32security.TokenUser)[0]
				user_sid_string = win32security.ConvertSidToStringSid(user_sid)
				logger.debug(f"Current user SID: {user_sid_string}")

				# Conditionally disable the user SID based on configuration
				if config.restrict_user_sid:
					logger.debug(f"Disabling user SID for access control: {user_sid_string}")
					sids_to_disable.append((user_sid, 0))
				else:
					logger.debug(f"Keeping user SID (restrict_user_sid=False): {user_sid_string}")

				# Get user's groups
				groups = win32security.GetTokenInformation(token_handle, win32security.TokenGroups)

				essential_group_sids = {
					"S-1-1-0",  # Everyone
					"S-1-5-4",  # Interactive
					"S-1-5-11",  # Authenticated Users
					"S-1-5-32-545",  # Users
					"S-1-5-32-544",  # Administrators
					"S-1-5-18",  # SYSTEM
					"S-1-5-19",  # LOCAL SERVICE
					"S-1-5-20",  # NETWORK SERVICE
					"S-1-2-0",  # Local
					"S-1-2-1",  # Console Logon
				}

				# Keep the user's primary domain group
				user_domain_groups = set()
				if "-" in user_sid_string:
					domain_part = "-".join(user_sid_string.split("-")[:-1])
					user_domain_groups.add(f"{domain_part}-513")  # Domain Users
					user_domain_groups.add(f"{domain_part}-515")  # Domain Computers

				for group_sid, attributes in groups:
					group_sid_string = win32security.ConvertSidToStringSid(group_sid)

					# Skip essential system groups
					if group_sid_string in essential_group_sids:
						logger.debug(f"Keeping essential group: {group_sid_string}")
						continue

					# Skip integrity level SIDs
					if group_sid_string.startswith("S-1-16-"):
						logger.debug(f"Keeping integrity level SID: {group_sid_string}")
						continue

					# Skip user's domain groups
					if group_sid_string in user_domain_groups:
						logger.debug(f"Keeping user domain group: {group_sid_string}")
						continue

					# Keep logon session SIDs - REQUIRED for ctypes!
					if group_sid_string.startswith("S-1-5-5-"):
						logger.debug(f"Keeping logon session SID (REQUIRED): {group_sid_string}")
						continue

					# Only disable non-essential groups
					non_essential_patterns = [
						"S-1-5-32-559",  # Performance Log Users
						"S-1-5-15",  # This Organization
						"S-1-5-113",  # Local account
						"S-1-5-64-10",  # NTLM Authentication
						"S-1-5-32-547",  # Power Users
						"S-1-5-114",  # Local account and member of Administrators group
					]

					should_disable = any(
						group_sid_string.startswith(pattern) for pattern in non_essential_patterns
					)

					if should_disable:
						sids_to_disable.append((group_sid, 0))
						logger.debug(f"Will disable non-essential group: {group_sid_string}")
					else:
						logger.debug(f"Keeping group for functionality: {group_sid_string}")

				logger.info(f"SID restrictions: {len(sids_to_disable)} SIDs to disable")

			except Exception as e:
				logger.error(f"Error preparing SID restrictions: {e}")
				sids_to_disable = []
		else:
			logger.info("SID restrictions DISABLED by config")

		restricted_token = win32security.CreateRestrictedToken(
			token_handle,
			0,
			sids_to_disable if sids_to_disable else None,
			privileges_to_delete if privileges_to_delete else None,
			None,
		)

		win32api.CloseHandle(token_handle)
		logger.info("Created restricted token successfully")

		if config.enable_low_integrity:
			try:
				logger.debug("Attempting to set Low Integrity Level on token...")
				low_integrity_sid = integrity_level_sid["low"]

				token_label = TOKEN_MANDATORY_LABEL()
				token_label.Label.Sid = low_integrity_sid
				token_label.Label.Attributes = SE_GROUP_INTEGRITY

				if not advapi32.SetTokenInformation(
					int(restricted_token),
					TokenIntegrityLevel,
					ctypes.byref(token_label),
					ctypes.sizeof(token_label),
				):
					error_code = ctypes.get_last_error()
					win32api.CloseHandle(restricted_token)
					raise ctypes.WinError(error_code, "SetTokenInformation for Low Integrity Level failed")

				logger.info("Successfully set Low Integrity Level on token.")
			except Exception as e_il:
				logger.error(f"Failed to set Low Integrity Level: {e_il}")
				if restricted_token:
					win32api.CloseHandle(restricted_token)
				return None
		else:
			logger.info("Low Integrity Level DISABLED by config")

		return restricted_token

	except Exception as e:
		logger.error(f"Failed to create restricted token: {e}")
		if "token_handle" in locals() and token_handle:
			try:
				win32api.CloseHandle(token_handle)
			except Exception:
				pass
		if "restricted_token" in locals() and restricted_token:
			try:
				win32api.CloseHandle(restricted_token)
			except Exception:
				pass
		return None


# ============================================================================
# Job Object Creation (extracted from launcher.py)
# ============================================================================


def create_job_object(config: SandboxConfig):
	"""Create a job object based on configuration settings."""
	if not config.enable_job_object:
		logger.info("Job object creation DISABLED by config")
		return None

	try:
		job = win32job.CreateJobObject(None, "")

		# Build limit flags based on config
		limit_flags = 0
		if config.enable_process_limits:
			limit_flags |= win32job.JOB_OBJECT_LIMIT_ACTIVE_PROCESS
		if config.enable_memory_limits:
			limit_flags |= win32job.JOB_OBJECT_LIMIT_PROCESS_MEMORY
		if config.enable_kill_on_job_close:
			limit_flags |= win32job.JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE

		extended_limit_info = {
			"BasicLimitInformation": {
				"PerProcessUserTimeLimit": 0,
				"PerJobUserTimeLimit": 0,
				"LimitFlags": limit_flags,
				"MinimumWorkingSetSize": 0,
				"MaximumWorkingSetSize": 0,
				"ActiveProcessLimit": 1 if config.enable_process_limits else 0,
				"Affinity": 0,
				"PriorityClass": 0,
				"SchedulingClass": 0,
			},
			"IoInfo": {
				"ReadOperationCount": 0,
				"WriteOperationCount": 0,
				"OtherOperationCount": 0,
				"ReadTransferCount": 0,
				"WriteTransferCount": 0,
				"OtherTransferCount": 0,
			},
			"ProcessMemoryLimit": 100 * 1024 * 1024 if config.enable_memory_limits else 0,
			"JobMemoryLimit": 0,
			"PeakProcessMemoryUsed": 0,
			"PeakJobMemoryUsed": 0,
		}

		if config.enable_memory_limits or config.enable_process_limits or config.enable_kill_on_job_close:
			try:
				win32job.SetInformationJobObject(
					job, win32job.JobObjectExtendedLimitInformation, extended_limit_info
				)
				logger.info("Set extended job limits")
			except Exception as e:
				logger.warning(f"Warning: Could not set extended limits: {e}")

		if config.enable_ui_restrictions:
			try:
				ui_restrictions = {
					"UIRestrictionsClass": (
						win32job.JOB_OBJECT_UILIMIT_DESKTOP
						| win32job.JOB_OBJECT_UILIMIT_READCLIPBOARD
						| win32job.JOB_OBJECT_UILIMIT_WRITECLIPBOARD
					)
				}

				win32job.SetInformationJobObject(job, win32job.JobObjectBasicUIRestrictions, ui_restrictions)
				logger.info("Set UI restrictions")
			except Exception as e:
				logger.warning(f"Warning: Could not set UI restrictions: {e}")
		else:
			logger.info("UI restrictions DISABLED by config")

		logger.info("Created job object")
		return job

	except Exception as e:
		logger.error(f"Failed to create job object: {e}")
		return None


# ============================================================================
# Main SandboxPopen Class (extracted from sandbox_subprocess.py)
# ============================================================================


class SandboxException(subprocess.SubprocessError):
	"""Exception raised when sandbox-specific operations fail"""

	pass


def _format_windows_error(original_exception, prefix=""):
	"""Format Windows error with last error code and message."""
	try:
		error_code = ctypes.get_last_error()
		if error_code:
			win_error = ctypes.WinError(error_code)
			return f"{prefix}{original_exception} (Windows Error {error_code}: {win_error})"
		else:
			return f"{prefix}{original_exception}"
	except Exception:
		return f"{prefix}{original_exception}"


class SandboxPopen(subprocess.Popen):
	"""
	A subprocess.Popen subclass that provides Windows sandboxing capabilities.

	This class maintains all the security features:
	- Restricted tokens with removed privileges and low integrity level
	- Job objects with memory and process limits
	- Low integrity directory access controls

	Usage:
	    config = SandboxConfig(restrict_user_sid=False)
	    with SandboxPopen(["python", "script.py"], config=config) as proc:
	        proc.wait()
	"""

	def __init__(
		self,
		*args,
		config=None,
		restricted_token=None,
		job_object=None,
		low_integrity_dirs=None,
		sandbox_temp_dir=None,
		allowed_directory=None,
		**kwargs,
	):
		# Store sandbox-specific parameters
		self.config = config or SandboxConfig()
		self.restricted_token = restricted_token
		self.job_object = job_object
		self.low_integrity_dirs = low_integrity_dirs or []
		self.sandbox_temp_dir = sandbox_temp_dir
		self.allowed_directory = allowed_directory

		# Create restricted token and job object if needed
		if not self.restricted_token and self.config.enable_restricted_token:
			self.restricted_token = create_restricted_token(self.config)
		if not self.job_object and self.config.enable_job_object:
			self.job_object = create_job_object(self.config)

		# Track handles for cleanup
		self._sandbox_handles = []
		self._process_assigned_to_job = False

		# Set up environment for sandbox
		env = kwargs.get("env", os.environ.copy())
		if env is None:
			env = os.environ.copy()

		if allowed_directory:
			env["SANDBOX_ALLOWED_DIR"] = allowed_directory
		if sandbox_temp_dir:
			env["TEMP"] = sandbox_temp_dir
			env["TMP"] = sandbox_temp_dir

		kwargs["env"] = env

		# Always create suspended on Windows when using restricted token or job object
		if sys.platform == "win32" and (self.restricted_token or self.job_object):
			creationflags = kwargs.get("creationflags", 0)
			creationflags |= win32con.CREATE_SUSPENDED
			kwargs["creationflags"] = creationflags

		# Log initialization for debugging
		logger.debug(f"Initializing SandboxPopen with restricted token: {self.restricted_token is not None}")
		logger.debug(f"Job object: {self.job_object is not None}")
		logger.debug(f"Low integrity directories: {len(self.low_integrity_dirs)}")

		# Remove unsupported parameters for older Python versions
		if sys.version_info < (3, 10) and "pipesize" in kwargs:
			kwargs.pop("pipesize")

		# Call parent constructor
		super().__init__(*args, **kwargs)

	def _execute_child(self, *args, **kwargs):
		"""
		Override _execute_child to use CreateProcessAsUser with restricted token
		"""
		if sys.platform != "win32":
			# Fall back to parent implementation on non-Windows
			return super()._execute_child(*args, **kwargs)

		# Windows-specific implementation with CreateProcessAsUser
		return self._execute_child_windows(*args, **kwargs)

	def _execute_child_windows(self, *args, **kwargs):
		# Extract parameters from args/kwargs for compatibility
		args_list = list(args)
		args_dict = kwargs

		# Map positional arguments
		param_names = [
			"args",
			"executable",
			"preexec_fn",
			"close_fds",
			"pass_fds",
			"cwd",
			"env",
			"startupinfo",
			"creationflags",
			"shell",
			"p2cread",
			"p2cwrite",
			"c2pread",
			"c2pwrite",
			"errread",
			"errwrite",
			"restore_signals",
			"gid",
			"gids",
			"uid",
			"umask",
			"start_new_session",
		]

		params = {}
		for i, name in enumerate(param_names):
			if i < len(args_list):
				params[name] = args_list[i]
			elif name in args_dict:
				params[name] = args_dict[name]
			else:
				params[name] = None

		# Extract ALL parameters we need
		args = params["args"]
		executable = params["executable"]
		cwd = params["cwd"]
		env = params["env"]
		startupinfo = params["startupinfo"]
		creationflags = params["creationflags"]
		p2cread = params["p2cread"]
		p2cwrite = params["p2cwrite"]
		c2pread = params["c2pread"]
		c2pwrite = params["c2pwrite"]
		errread = params["errread"]
		errwrite = params["errwrite"]

		"""
        Windows-specific child execution with CreateProcessAsUser
        """
		# Use parent's argument processing logic
		if not isinstance(args, str):
			args = subprocess.list2cmdline(args)

		# Handle startupinfo
		if startupinfo is None:
			startupinfo = win32process.STARTUPINFO()
		elif hasattr(startupinfo, "dwFlags"):
			# Convert subprocess.STARTUPINFO to win32process.STARTUPINFO
			si = win32process.STARTUPINFO()
			si.dwFlags = startupinfo.dwFlags
			si.wShowWindow = getattr(startupinfo, "wShowWindow", 0)
			startupinfo = si

		# Set up standard handles
		logger.debug(f"Handle setup: p2cread={p2cread}, c2pwrite={c2pwrite}, errwrite={errwrite}")

		if p2cread is not None and p2cread != -1:
			startupinfo.hStdInput = p2cread
			logger.debug(f"Set stdin to pipe handle: {p2cread}")
		else:
			startupinfo.hStdInput = win32api.GetStdHandle(win32api.STD_INPUT_HANDLE)
			logger.debug(f"Set stdin to inherited handle: {startupinfo.hStdInput}")

		if c2pwrite is not None and c2pwrite != -1:
			startupinfo.hStdOutput = c2pwrite
			logger.debug(f"Set stdout to pipe handle: {c2pwrite}")
		else:
			startupinfo.hStdOutput = win32api.GetStdHandle(win32api.STD_OUTPUT_HANDLE)
			logger.debug(f"Set stdout to inherited handle: {startupinfo.hStdOutput}")

		if errwrite is not None and errwrite != -1:
			startupinfo.hStdError = errwrite
			logger.debug(f"Set stderr to pipe handle: {errwrite}")
		else:
			startupinfo.hStdError = win32api.GetStdHandle(win32api.STD_ERROR_HANDLE)
			logger.debug(f"Set stderr to inherited handle: {startupinfo.hStdError}")

		if (
			startupinfo.hStdInput != win32api.GetStdHandle(win32api.STD_INPUT_HANDLE)
			or startupinfo.hStdOutput != win32api.GetStdHandle(win32api.STD_OUTPUT_HANDLE)
			or startupinfo.hStdError != win32api.GetStdHandle(win32api.STD_ERROR_HANDLE)
		):
			startupinfo.dwFlags |= win32con.STARTF_USESTDHANDLES

		# Ensure process is created suspended for job object assignment
		if self.restricted_token or self.job_object:
			creationflags |= win32con.CREATE_SUSPENDED

		try:
			if self.restricted_token:
				# Use CreateProcessAsUser with restricted token
				logger.info("Creating process with restricted token...")
				logger.debug(f"Command: {args}")

				process_info = win32process.CreateProcessAsUser(
					self.restricted_token,
					executable,
					args,
					None,  # Process security attributes
					None,  # Thread security attributes
					True,  # Inherit handles
					creationflags,
					env,
					cwd,
					startupinfo,
				)
			else:
				# Fall back to regular CreateProcess
				logger.info("Creating process with regular CreateProcess...")
				logger.debug(f"Command: {args}")

				process_info = win32process.CreateProcess(
					executable,
					args,
					None,  # Process security attributes
					None,  # Thread security attributes
					True,  # Inherit handles
					creationflags,
					env,
					cwd,
					startupinfo,
				)

			# Extract handles from process_info
			process_handle = process_info[0]  # Process handle
			thread_handle = process_info[1]  # Thread handle
			self.pid = process_info[2]  # Process ID
			thread_id = process_info[3]  # Thread ID

			# Convert pywin32 handle to int for subprocess compatibility
			self._handle = int(process_handle)

			# Store handles for cleanup
			self._sandbox_handles.extend([process_handle, thread_handle])

			logger.info(f"Process created with PID: {self.pid}")

			# Assign to job object if provided
			if self.job_object:
				logger.debug("Assigning process to job object...")
				try:
					win32job.AssignProcessToJobObject(self.job_object, process_handle)
					self._process_assigned_to_job = True
					logger.info("Process assigned to job object successfully")
				except Exception as e:
					logger.error(f"Failed to assign process to job object: {e}")
					# Terminate the process if job assignment fails
					try:
						win32process.TerminateProcess(process_handle, 1)
					except Exception as e:
						pass
					raise SandboxException(
						_format_windows_error(e, "Failed to assign process to job object: ")
					)

			# Resume the process if it was created suspended
			if creationflags & win32con.CREATE_SUSPENDED:
				logger.debug("Resuming suspended process...")
				win32process.ResumeThread(thread_handle)
				logger.info("Process resumed and running in sandbox")

			# Note: Handle cleanup is handled by the parent subprocess.Popen class
			# We don't need to manually close handles here

		except Exception as e:
			# Clean up on error
			self._cleanup_handles()
			logger.error(f"Failed to create sandboxed process: {e}")
			raise SandboxException(_format_windows_error(e, "Failed to create sandboxed process: "))

	def _cleanup_handles(self):
		"""Clean up Windows handles"""
		for handle in self._sandbox_handles:
			try:
				if handle:
					win32api.CloseHandle(handle)
			except Exception:
				pass
		self._sandbox_handles.clear()

	def __exit__(self, type, value, traceback):
		"""Clean up on context manager exit."""
		try:
			result = super().__exit__(type, value, traceback)
		finally:
			self._cleanup_handles()
		return result
