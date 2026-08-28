# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Child program checking that an ART exception keeps its type when it crosses into a fresh host.

Run as a process by ``TestExceptionTaxonomyAcrossProcess``.
Must run in its own process because rpyc rebuilds a remote exception as its real class
only when that class's module is already resident,
but ART's tests import :mod:`_art.exceptions`,
which masks the failure.

This program doesn't import :mod:`_art.exceptions` before making the boundary call.
It boots the host as the real entry point does,
asks core for a capability (which core refuses with a :class:`~_art.exceptions.PermissionNotGrantedError`),
and only then inspects the exception.
That models add-on code that catches an ART exception without having imported the taxonomy in that module,
relying on the boot path to have made it resident.

Exits ``0`` if the exception arrived as its real class,
and non-zero with a diagnostic on standard error otherwise.
"""

import sys

from _art.host import entrypoint
from _art.host.rootService import HostRootService
from _art.transport import Connection

#: The capability the probe requests; core refuses every capability for now.
_REQUESTED_CAPABILITY = "audio"


def _check() -> list[str]:
	"""Drive one refused capability request and report everything wrong with the result.

	:returns: Human-readable descriptions of each failed expectation, empty if all held.
	"""
	stream = entrypoint._claimControlStream()
	conn = Connection(stream, HostRootService(), name="taxonomy probe host")
	conn.bgEventLoop(daemon=True)
	core = conn.remoteService
	try:
		try:
			core.requestCapability(_REQUESTED_CAPABILITY)
		except BaseException as caught:  # noqa: BLE001
			return _describeFailures(caught)
		return ["requestCapability returned instead of raising"]
	finally:
		conn.close()


def _describeFailures(caught: BaseException) -> list[str]:
	"""Compare a caught exception against what a real add-on would rely on.

	Imports are deferred to here, after the exception has already been rebuilt, so that naming
	the taxonomy for the check cannot be what makes it resident.

	:param caught: The exception the host received from core.
	:returns: A description of each broken expectation, empty if the type survived intact.
	"""
	from _art.exceptions import CapabilityDeniedError, CapabilityUnavailableError, PermissionNotGrantedError
	from rpyc.core import vinegar

	received = type(caught)
	failures: list[str] = []
	if issubclass(received, vinegar.GenericException):
		failures.append(f"rebuilt as a GenericException ({received.__module__}.{received.__name__})")
	if not isinstance(caught, CapabilityUnavailableError):
		failures.append("not caught by `except CapabilityUnavailableError`")
	if not isinstance(caught, CapabilityDeniedError):
		failures.append("not caught by `except CapabilityDeniedError`")
	if not isinstance(caught, PermissionNotGrantedError):
		failures.append("not caught by `except PermissionNotGrantedError`")
	return failures


if __name__ == "__main__":
	failures = _check()
	if failures:
		sys.stderr.write("; ".join(failures))
		sys.exit(1)
	sys.exit(0)
