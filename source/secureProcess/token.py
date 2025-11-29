# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from __future__ import annotations
import win32profile
import win32security
import win32process
import win32con
from winBindings.winnt import (
	GENERIC_ALL,
)

import logging
log = logging.getLogger(__name__)


DANGEROUS_SIDS = {
	"Administrators": "S-1-5-32-544",
	"System": "S-1-5-18",
	"NT AUTHORITY\\SERVICES": "S-1-5-6",
}

ALLOWED_GROUP_SIDS = {
	"Everyone": "S-1-1-0",
	"INTERACTIVE": "S-1-5-4",
	"Authenticated Users": "S-1-5-11",
	"Users": "S-1-5-32-545",
	"Console Logon": "S-1-2-1",
	"NT AUTHORITY\\LOCAL": "S-1-2-0",
	"NT AUTHORITY\\Local account": "S-1-5-113",
}

REQUIRED_GROUP_SIDS = {
	"Restricted": "S-1-5-12",
}

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


def restrictToken(token: PyHandle, removePrivilages: bool=True, allowUser: bool=True, disableDangerousSids: bool=True):
	"""Create a restricted token derived from an existing token.

	This function can remove enabled privileges, restrict the token's group SIDs
	to a limited set, and disable membership of dangerous groups. The resulting
	restricted token is suitable for launching or using in contexts that require
	lower privileges than the original token.

	:param token: The original token to restrict.
	:param removePrivilages: If True, attempt to remove all enabled privileges from
		the token (but skips change-notify privilege for directory traversal).
	:param allowUser: If True, include the user SID in the restricted token;
		if False, the user SID is omitted and only allowed/required groups and the
		logon SID are included.
	:param disableDangerousSids: If True, disable membership of well-known
		dangerous groups (for example Administrators or System) if present in the
		token.

	:returns: A handle to the newly created restricted token.
	:raises: Exceptions raised by underlying win32 API calls on failure.
	"""
	restrictFlags = 0
	if removePrivilages:
		oldPrivileges = win32security.GetTokenInformation(token, win32security.TokenPrivileges)
		for priv, attrs in oldPrivileges:
			if attrs & win32con.SE_PRIVILEGE_ENABLED:
				privName = win32security.LookupPrivilegeName(None, priv)
				if privName == win32security.SE_CHANGE_NOTIFY_NAME:
					continue
				log.debug(f"Removing privilege: {privName}...")
		restrictFlags = win32security.DISABLE_MAX_PRIVILEGE
	restrictToSids = []
	oldGroups = win32security.GetTokenInformation(token, win32security.TokenGroups)
	oldEnabledGroups = [sid for sid, attrs in oldGroups if attrs & win32security.SE_GROUP_ENABLED]
	if not allowUser:
		log.debug("User not allowed, so not including user SID in SIDs to restrict to.")
		for name, sidString in ALLOWED_GROUP_SIDS.items():
			sid = win32security.ConvertStringSidToSid(sidString)
			if sid not in oldEnabledGroups:
				continue
			log.debug(f"Restricting to existing group {name}...")
			restrictToSids.append((sid, 0))
		for name, sidString in REQUIRED_GROUP_SIDS.items():
			log.debug(f"Restricting to required group {name}...")
			sid = win32security.ConvertStringSidToSid(sidString)
			restrictToSids.append((sid, 0))
		for sid, attrs in oldGroups:
			if attrs & win32security.SE_GROUP_LOGON_ID:
				sidString = win32security.ConvertSidToStringSid(sid)
				log.debug("Restricting to Logon Sid")
				restrictToSids.append((sid, 0))
				break
	sidsToDisable = []
	if disableDangerousSids:
		for name, sidString in DANGEROUS_SIDS.items():
			sid = win32security.ConvertStringSidToSid(sidString)
			if sid in oldEnabledGroups:
				log.debug(f"Disabling dangerous group {name}...")
			sidsToDisable.append((sid, 0))
	restrictedToken = win32security.CreateRestrictedToken(
		token,
		restrictFlags,
		sidsToDisable,
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
	""" Return the user SID string for the given token."""
	userSid = win32security.GetTokenInformation(token, win32security.TokenUser)[0]
	return win32security.ConvertSidToStringSid(userSid)


def lookupTokenLogonSidString(token) -> str:
	""" Return the unique logon session SID string for the given token."""
	groups = win32security.GetTokenInformation(token, win32security.TokenGroups)
	for sid, attrs in groups:
		if attrs & win32security.SE_GROUP_LOGON_ID:
			return win32security.ConvertSidToStringSid(sid)
	raise RuntimeError("Could not find Logon SID in token")


def createEnvironmentBlock(vars: dict[str, str]) -> str:
	""" Create a Windows environment block from a dictionary of variables."""
	log.debug(f"Building process environment block containing {len(vars)} variables...")
	envBlock = "\0".join(f"{key}={value}" for key, value in vars.items()) + "\0\0"
	return envBlock

def createTokenEnvironmentBlock(token):
	""" Generate standard environment variables for a given token. """
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
		#win32security.SYSTEM_ALARM_ACE_TYPE: "ALARM",
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

def createRestrictedDacl(uniqueRestrictedSidString: str, includeSystem: bool=True, includeAdministrators: bool=True, includeMe: bool=True):
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

def createRestrictedSecurityDescriptor(uniqueRestrictedSidString: str, integrityLevel: str | None="low", includeSystem: bool=True, includeAdministrators: bool=True, includeMe: bool=True):
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
	dacl = createRestrictedDacl(uniqueRestrictedSidString, includeSystem=includeSystem, includeAdministrators=includeAdministrators, includeMe=includeMe)
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
