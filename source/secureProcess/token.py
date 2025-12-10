# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from __future__ import annotations
import contextlib
import win32api
import win32profile
import win32security
import win32process
import win32con
from winBindings.winnt import (
	GENERIC_ALL,
)

import logging

log = logging.getLogger(__name__)


integrityLevels = {
	"untrusted": win32security.WinUntrustedLabelSid,
	"low": win32security.WinLowLabelSid,
	"medium": win32security.WinMediumLabelSid,
	"high": win32security.WinHighLabelSid,
	"system": win32security.WinSystemLabelSid,
}


def getCurrentPrimaryToken():
	"""Return the primary access token for the current process.

	This function calls GetCurrentProcess() and OpenProcessToken() to obtain
	a handle to the calling process's primary access token. The token is
	opened with MAXIMUM_ALLOWED access by default.

	:return: Handle to the current process primary token.
	:rtype: PyHANDLE
	"""
	curToken = win32security.OpenProcessToken(
		win32process.GetCurrentProcess(),
		win32con.MAXIMUM_ALLOWED,
	)
	return curToken


def createLeastPrivilegedToken(token):
	"""
	Create a least-privileged token from an existing token.

	This produces a new token with all privileges removed except for SE_CHANGE_NOTIFY.

	:param token: The source token to restrict.
	:returns: A new token with maximum privileges disabled.
	:raises: Underlying win32 API exceptions if token operations fail.
	"""
	log.debug("Removing max privileges from token...")
	return win32security.CreateRestrictedToken(token, win32security.DISABLE_MAX_PRIVILEGE, (), (), ())


allowedRestrictedSids = {
	"Everyone": "S-1-1-0",
	"INTERACTIVE": "S-1-5-4",
	"Authenticated Users": "S-1-5-11",
	"Users": "S-1-5-32-545",
	"Console Logon": "S-1-2-1",
	"NT AUTHORITY\\LOCAL": "S-1-2-0",
	"NT AUTHORITY\\Local account": "S-1-5-113",
}

requiredRestrictedSids = {
	"Restricted": "S-1-5-12",
}


def createRestrictedToken(token, removePrivilages: bool = True, retainUser: bool = False):
	"""Create a new restricted token based on an existing token.

	This function builds a reduced-privilege token by optionally disabling maximum
	privileges and constructing a restricted SID list.
	The restricted SID list always includes the special "Restricted" SID,
	the Logon SID from the source token if one exists,
	and any group SIDs from the source token which match some generic interactive group SIDs.
	These should be enough to allow basic interactive access such as reading and executing system binaries in system32 and installed applications in program files,
	as well as basic interaction with the desktop and window station.
	But by default will not include access to any user's files or profile data, not even  the token user.

	If retainUser is True, the user SID from the source token is also included in the restricted SID list, thus granting access to the user's files and profile data.

	:param token: The source token to restrict.
	:param removePrivilages: If True, disable all privileges on the created token, except SE_CHANGE_NOTIFY.
	:param retainUser: If True, include the user's SID in the restricted SID list.
	:returns: A handle to the newly created restricted token.
	:raises: Exceptions from underlying win32 API calls if token operations fail.
	"""
	restrictFlags = 0
	if removePrivilages:
		log.debug("Removing max privileges from token...")
		restrictFlags |= win32security.DISABLE_MAX_PRIVILEGE
	oldGroups = win32security.GetTokenInformation(token, win32security.TokenGroups)
	oldEnabledGroups = [sid for sid, attrs in oldGroups if attrs & win32security.SE_GROUP_ENABLED]
	restrictToSids = []
	for name, sidString in requiredRestrictedSids.items():
		log.debug(f"Restricting to required group {name}...")
		sid = win32security.ConvertStringSidToSid(sidString)
		restrictToSids.append((sid, 0))
	for name, sidString in allowedRestrictedSids.items():
		sid = win32security.ConvertStringSidToSid(sidString)
		if sid not in oldEnabledGroups:
			continue
		log.debug(f"Retaining existing group {name}...")
		restrictToSids.append((sid, 0))
	for sid, attrs in oldGroups:
		if attrs & win32security.SE_GROUP_LOGON_ID:
			sidString = win32security.ConvertSidToStringSid(sid)
			log.debug("Restricting to Logon Sid")
			restrictToSids.append((sid, 0))
			break
	if retainUser:
		userSid = win32security.GetTokenInformation(token, win32security.TokenUser)[0]
		log.debug("Retaining user SID in restricted token...")
		restrictToSids.append((userSid, 0))
	restrictedToken = win32security.CreateRestrictedToken(
		token,
		restrictFlags,
		(),
		(),
		restrictToSids,
	)
	return restrictedToken


def setTokenIntegrityLevel(token: PyHandle, level: str):
	"""
	Set the integrity level on a token.

	This updates the token's mandatory integrity level (SACL) to the given named level. Typical values for
	``level`` are "untrusted", "low", "medium", "high" and "system".

	:param token: The token whose integrity level will be changed.
	:param level: The named integrity level to apply.

	:raises KeyError: If ``level`` is not found in the integrityLevels map.
	:raises: Underlying win32 API exceptions if creating the SID or setting
		the token information fails.

	:returns: None
	"""
	levelId = integrityLevels[level]
	sid = win32security.CreateWellKnownSid(levelId, None)
	mandatoryLabel = (sid, win32security.SE_GROUP_INTEGRITY)
	win32security.SetTokenInformation(
		token,
		win32security.TokenIntegrityLevel,
		mandatoryLabel,
	)


def createServiceLogon():
	"""
	Create a logon token for the built-in LocalService account.

	This is a small convenience wrapper around win32security.LogonUser that
	requests a service-type logon for the "LocalService" account in the
	"NT AUTHORITY" domain. The call uses the LOGON32_LOGON_SERVICE logon
	type and the default logon provider.

	:return: A handle to the created logon token.
	:raises: Exceptions raised by the underlying LogonUser call if the logon
		attempt fails or if the Win32 API returns an error.
	"""
	log.debug("Calling LogonUser for LocalService...")
	token = win32security.LogonUser(
		"LocalService",
		"NT AUTHORITY",
		"",
		win32con.LOGON32_LOGON_SERVICE,
		win32con.LOGON32_PROVIDER_DEFAULT,
	)
	return token


def lookupTokenUserSidString(token) -> str:
	"""Return the user SID string for the given token."""
	userSid = win32security.GetTokenInformation(token, win32security.TokenUser)[0]
	return win32security.ConvertSidToStringSid(userSid)


def lookupTokenLogonSidString(token) -> str:
	"""Return the unique logon session SID string for the given token."""
	groups = win32security.GetTokenInformation(token, win32security.TokenGroups)
	for sid, attrs in groups:
		if attrs & win32security.SE_GROUP_LOGON_ID:
			return win32security.ConvertSidToStringSid(sid)
	raise RuntimeError("Could not find Logon SID in token")


def createEnvironmentBlock(vars: dict[str, str]) -> str:
	"""Create a Windows environment block from a dictionary of variables."""
	log.debug(f"Building process environment block containing {len(vars)} variables...")
	envBlock = "\0".join(f"{key}={value}" for key, value in vars.items()) + "\0\0"
	return envBlock


def createTokenEnvironmentBlock(token):
	"""Generate standard environment variables for a given token."""
	return win32profile.CreateEnvironmentBlock(token, False)


def accessMaskToString(mask) -> str:
	"""
	Decodes an integer access mask into a list of human-readable strings.
	"""
	rights = []
	# Generic mappings
	if mask & win32con.GENERIC_ALL:
		rights.append("GENERIC_ALL")
	if mask & win32con.GENERIC_READ:
		rights.append("GENERIC_READ")
	if mask & win32con.GENERIC_WRITE:
		rights.append("GENERIC_WRITE")
	if mask & win32con.GENERIC_EXECUTE:
		rights.append("GENERIC_EXECUTE")
	# Standard Rights
	if mask & win32con.DELETE:
		rights.append("DELETE")
	if mask & win32con.READ_CONTROL:
		rights.append("READ_CONTROL")
	if mask & win32con.WRITE_DAC:
		rights.append("WRITE_DAC")
	if mask & win32con.WRITE_OWNER:
		rights.append("WRITE_OWNER")
	if mask & win32con.SYNCHRONIZE:
		rights.append("SYNCHRONIZE")
	# If no specific flags matched, just return the hex
	if not rights:
		return "none"
	return f"{', '.join(rights)}"


def getAceTypeString(ace_type):
	"""Returns a string representation of the ACE type."""
	types = {
		win32security.ACCESS_ALLOWED_ACE_TYPE: "ALLOW",
		win32security.ACCESS_DENIED_ACE_TYPE: "DENY",
		win32security.SYSTEM_AUDIT_ACE_TYPE: "AUDIT",
		# win32security.SYSTEM_ALARM_ACE_TYPE: "ALARM",
	}
	return types.get(ace_type, f"Unknown ({ace_type})")


def getDaclString(dacl):
	"""Return a human-readable string representation of a DACL.

	:param dacl: The discretionary access control list to decode.
	:returns: A multi-line string describing each ACE, or a message indicating
		that the DACL is empty (granting full access).
	"""
	if dacl is None:
		return "empty DACL, full access granted"
	aceStrings = []
	ace_count = dacl.GetAceCount()
	for i in range(ace_count):
		(ace_type, ace_flags), access_mask, sid = dacl.GetAce(i)
		sidString = win32security.ConvertSidToStringSid(sid)
		try:
			name, domain, type_ = win32security.LookupAccountSid(None, sid)
			account_name = f"{domain}\\{name}"
		except Exception:
			account_name = f"SID {sidString}"
		aceString = f"{getAceTypeString(ace_type)} {accessMaskToString(access_mask)} for {account_name}"
		aceStrings.append(aceString)
	return "\n".join(aceStrings)


def createRestrictedDacl(
	uniqueRestrictedSidString: str,
	includeSystem: bool = True,
	includeAdministrators: bool = True,
	includeMe: bool = True,
):
	"""
	Create a discretionary access control list (DACL) that allows access to a
	restricted subject and, optionally, to other well-known principals.

	This helper builds an ACL containing one or more access-allowed ACEs that
	grant GENERIC_ALL to the provided restricted SID and, depending on the
	arguments, to SYSTEM, the built-in Administrators group, and the current
	calling user. The resulting ACL is suitable for use when constructing a
	security descriptor intended to limit access to a particular restricted
	subject while still permitting essential system or administrative access.

	:param uniqueRestrictedSidString: The string representation of the SID for
		the restricted principal that must be granted access.
	:param includeSystem: If True, include an ACE granting access to the
		local SYSTEM account.
	:param includeAdministrators: If True, include an ACE granting access to
		the built-in Administrators group.
	:param includeMe: If True, include an ACE granting access to the current
		calling user (unless that user is SYSTEM or equals the restricted SID).

	:returns: An ACL object populated with the requested ACEs.
	:raises: Underlying win32 API exceptions (for example when converting SIDs
		or reading the current token) if operations fail.
	"""
	dacl = win32security.ACL()
	# Allow access to the unique restricted SID
	restrictedSid = win32security.ConvertStringSidToSid(uniqueRestrictedSidString)
	log.debug(f"Adding allow ACE for restricted SID {uniqueRestrictedSidString}...")
	dacl.AddAccessAllowedAce(win32security.ACL_REVISION, GENERIC_ALL, restrictedSid)
	# Optionally allow access to SYSTEM
	systemSid = win32security.CreateWellKnownSid(win32security.WinLocalSystemSid, None)
	if includeSystem:
		log.debug("Adding allow ACE for SYSTEM...")
		dacl.AddAccessAllowedAce(win32security.ACL_REVISION, GENERIC_ALL, systemSid)
	adminsSid = win32security.CreateWellKnownSid(win32security.WinBuiltinAdministratorsSid, None)
	if includeAdministrators:
		log.debug("Adding allow ACE for ADMINISTRATORS...")
		dacl.AddAccessAllowedAce(win32security.ACL_REVISION, GENERIC_ALL, adminsSid)
	# Optionally allow access to the caller.
	if includeMe:
		curToken = getCurrentPrimaryToken()
		curUserSid = win32security.GetTokenInformation(curToken, win32security.TokenUser)[0]
		if not includeSystem or (curUserSid != systemSid):
			if curUserSid != restrictedSid:
				log.debug("Adding allow ACE for current user...")
				dacl.AddAccessAllowedAce(win32security.ACL_REVISION, GENERIC_ALL, curUserSid)
	return dacl


def createRestrictedSecurityDescriptor(
	uniqueRestrictedSidString: str,
	integrityLevel: str | None = "low",
	includeSystem: bool = True,
	includeAdministrators: bool = True,
	includeMe: bool = True,
):
	"""
	Create a security descriptor that restricts access to a single principal.

	This function builds a SECURITY_DESCRIPTOR whose DACL grants GENERIC_ALL to
	the provided restricted SID and, optionally, to SYSTEM, the built-in
	Administrators group, and the current calling user. If an integrityLevel is
	provided, a mandatory integrity SACL is also attached to the security
	descriptor to enforce the requested integrity policy.

	:param uniqueRestrictedSidString: The string representation of the SID to
		which access should be granted.
	:param integrityLevel: Named integrity level to apply to the SACL (for
		example "low", "medium", "high"), or None to omit a SACL.
	:param includeSystem: If True, include an ACE granting access to the
		local SYSTEM account.
	:param includeAdministrators: If True, include an ACE granting access to
		the built-in Administrators group.
	:param includeMe: If True, include an ACE granting access to the current
		calling user (unless that user is SYSTEM or equals the restricted SID).

	:returns: A SECURITY_DESCRIPTOR with the requested DACL and optional SACL.
	:raises: Exceptions propagated from underlying win32 API calls on failure.
	"""
	sd = win32security.SECURITY_DESCRIPTOR()
	sd.Initialize()
	dacl = createRestrictedDacl(
		uniqueRestrictedSidString,
		includeSystem=includeSystem,
		includeAdministrators=includeAdministrators,
		includeMe=includeMe,
	)
	sd.SetSecurityDescriptorDacl(1, dacl, 0)
	if integrityLevel:
		log.debug(f"Setting integrity level to {integrityLevel}...")
		levelId = integrityLevels[integrityLevel]
		sid = win32security.CreateWellKnownSid(levelId, None)
		sacl = win32security.ACL()
		policy = win32security.SYSTEM_MANDATORY_LABEL_NO_WRITE_UP
		sacl.AddMandatoryAce(win32security.ACL_REVISION_DS, 0, policy, sid)
		sd.SetSecurityDescriptorSacl(1, sacl, 0)
	return sd

@contextlib.contextmanager
def impersonateToken(token):
	"""Context manager to impersonate a given token within a context.

	This context manager calls ImpersonateLoggedOnUser with the provided token
	when entering the context, and reverts to the original security context
	when exiting the context.

	:param token: The token to impersonate.
	"""
	win32security.ImpersonateLoggedOnUser(token)
	try:
		yield
	finally:
		win32security.RevertToSelf()

def isTokenElevated(token) -> bool:
	"""
	Check if a given token is elevated.

	:param token: The token to check.
	:return: True if the token is elevated, False otherwise.
	"""
	elevation = win32security.GetTokenInformation(token, win32security.TokenElevation)
	return elevation != 0

def getUnelevatedCurrentInteractiveUserTokenFromShell():
	"""Return an unelevated primary token for the current interactive user.

	This function locates the shell window for the active desktop session,
	determines the process ID of the shell, opens that process and obtains
	its primary token. A duplicated primary token is returned so callers can
	use it for impersonation or process creation within the interactive
	session without inheriting elevation from the current process.

	:raises RuntimeError: If the shell window cannot be located.
	:return: A duplicated primary token for the interactive user's shell
		process.
	"""

	import ctypes
	shellWindow = ctypes.windll.user32.GetShellWindow()
	if not shellWindow:
		raise RuntimeError("Could not find shell window; no interactive user session?")
	tid, pid = win32process.GetWindowThreadProcessId(shellWindow)
	log.debug(f"Found shell process with PID {pid}...")
	shellProcess = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, False, pid)
	token = win32security.OpenProcessToken(shellProcess, win32con.MAXIMUM_ALLOWED)
	token = win32security.DuplicateTokenEx(token, win32security.SecurityImpersonation, win32security.TOKEN_ALL_ACCESS, win32security.TokenPrimary, None)
	return token
