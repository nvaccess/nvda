# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
Exceptions shared by both sides of the ART boundary.

The hierarchy is shaped to allow add-ons to determine the reason a capability is unabailable
with varying levels of specificity according to their needs:

	CapabilityUnavailableError
		CapabilityDeniedError
			PermissionNotGrantedError
			PermissionRevokedError
		CapabilityLostError

.. note::
	Catching these across the boundary requires ``instantiate_custom_exceptions``;
	see :data:`_art.transport.config.PROTOCOL_CONFIG`.
"""


class CapabilityUnavailableError(Exception):
	"""A capability cannot be used."""


class CapabilityDeniedError(CapabilityUnavailableError):
	"""A capability is unavailable for a policy reason."""


class PermissionNotGrantedError(CapabilityDeniedError):
	"""The permission has never been held.

	Covers ``Denied``, ``Prompt``, and permissions absent from the add-on's manifest.
	"""


class PermissionRevokedError(CapabilityDeniedError):
	"""The permission was granted earlier in this session, and has since been revoked."""


class CapabilityLostError(CapabilityUnavailableError):
	"""A capability became unusable for an infrastructure reason, such as a crash or teardown.

	Not a policy decision; the permission may still be granted.
	"""
