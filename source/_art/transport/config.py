# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
rpyc protocol configuration and global patches for the ART transport.

.. note::
	Importing this module applies patches that the transport depends on, so it must be imported before any connection is created.
	It is imported by ``connection`` for that reason.
"""

import builtins

import rpyc.core.vinegar


#: The rpyc protocol configuration shared by every ART connection.
#:
#: These defaults are deliberately restrictive.
#: Add-ons are untrusted, so they must only ever be able to invoke methods explicitly exposed on a :class:`.service.Service`.
#: ``allow_getattr`` is intentionally left at the rpyc default (``True``) because exposed methods are reached via attribute access on the netref;
#: with public, safe and all attribute access disabled, only the ``exposed`` allowlist remains reachable.
#:
#: .. warning::
#: 	None of the security-critical flags below should be loosened without a security review..
PROTOCOL_CONFIG: dict[str, object] = {
	# Only explicitly exposed methods may cross the boundary.
	"allow_public_attrs": False,
	"allow_safe_attrs": False,
	"allow_all_attrs": False,
	"allow_setattr": False,
	"allow_delattr": False,
	# pickle would permit arbitrary code execution during deserialization.
	"allow_pickle": False,
	# A raising handler must not tear down the whole channel.
	"close_catchall": True,
}


def _applyPatches() -> None:
	"""Apply the rpyc patches that ART relies on.

	.. note::
		This function is idempotent.
	"""
	# NVDA ships its own top-level ``exceptions`` module.
	# rpyc's vinegar imports ``exceptions`` (a Python 2 relic) in preference to ``builtins`` when present, which makes deserialization of remote exceptions fail.
	# Force it back to ``builtins``.
	rpyc.core.vinegar.exceptions_module = builtins


_applyPatches()
