# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
First-launch code of the ART host process.

Run as ``python -m _art.host.entrypoint``
with the control connection wired to the process's standard input and output.

The work is split in two so that the same boot path can be exercised without a process:

* :func:`run` is process-agnostic and takes a ready-made stream.
* :func:`main` is the process half, and does the standard stream manipulation that only makes sense when running in our own process.
"""

from __future__ import annotations

import logging
import os
import sys
import traceback
from typing import Final

from rpyc.core.stream import PipeStream, Stream
from winBindings.kernel32 import CloseHandle

from .. import _HOST_MARKER_ENV
from ..winHandles import claimHandleFromDescriptor

#: Name of the host's end of the control connection, used in logging.
CONTROL_CONNECTION_NAME: Final[str] = "ART host control"
#: File descriptor of this process's standard input.
_STDIN_FD: Final[int] = 0
#: File descriptor of this process's standard output.
_STDOUT_FD: Final[int] = 1
#: File descriptor of this process's standard error.
_STDERR_FD: Final[int] = 2


def run(stream: Stream) -> None:
	"""Serve the host root service over ``stream`` until the connection closes.

	Runs the event loop in the calling thread, so this blocks for the lifetime of the host.

	:param stream: The host's end of the control connection.
	"""
	# Import late to allow ``main`` to set the host marker first.
	from .._log import log
	from ..transport import Connection
	from .rootService import HostRootService

	service = HostRootService()
	conn = Connection(stream, service, name=CONTROL_CONNECTION_NAME)
	log.debug("ART host serving control connection")
	try:
		conn.eventLoop()
	finally:
		log.debug("ART host control connection closed")
		conn.close()


def _redirectToDevNull(targetFd: int) -> None:
	"""Point a descriptor at the null device.

	The descriptor opened to reach the null device is closed again before returning,
	so this owns nothing once it is done.

	:param targetFd: Descriptor to redirect.
		Left open, but pointing at the null device.
	:raises OSError: If the null device cannot be opened, or ``targetFd`` cannot be redirected.
	"""
	devNullFd = os.open(os.devnull, os.O_RDWR)
	try:
		os.dup2(devNullFd, targetFd)
	finally:
		os.close(devNullFd)


def _redirectStandardStreams() -> None:
	"""Move this process's standard input and output off the descriptors carrying the control connection.

	Standard input is pointed at the null device, and standard output is folded into standard error,
	so that anything written to either after boot cannot desynchronise rpyc's framing on the wire.
	Both the descriptors and the :mod:`sys` objects layered over them are moved,
	since either is enough to corrupt the connection.

	Standard error is left where it is:
	it is the host's diagnostic channel, which NVDA drains to its log.

	Owns nothing on return, so a caller part way through claiming descriptors
	has nothing extra to release if this raises.

	:raises OSError: If the null device cannot be opened, or a descriptor cannot be redirected.
	"""
	# Make stdin point to the null device
	_redirectToDevNull(_STDIN_FD)
	sys.stdin = open(os.devnull)  # noqa: SIM115
	# make stdout point to stderr
	try:
		os.dup2(_STDERR_FD, _STDOUT_FD)
	except OSError:
		# No usable standard error, so redirect to the null device instead
		_redirectToDevNull(_STDOUT_FD)
	sys.stdout = sys.stderr if sys.stderr is not None else open(os.devnull, "w")  # noqa: SIM115


def _claimControlStream() -> Stream:
	"""Take private ownership of the standard descriptors and return the control stream.

	The control connection runs over stdin and stdout, which carry framed rpyc traffic rather than text.
	Writing anything else to them will corrupt the connection.
	To give the wire exclusive use of the original descriptors, duplicate them,
	then move the standard streams elsewhere (see :func:`_redirectStandardStreams`).

	The duplicated descriptors are then converted into handles the returned stream solely owns,
	so that nothing else closes them out from under it
	(see :func:`_art.winHandles.claimHandleFromDescriptor`).

	:returns: The host's end of the control connection.
	:raises OSError: If the descriptors cannot be duplicated, redirected, or claimed.
		Nothing is left open in that case.
	"""
	readFd = -1
	writeFd = -1
	readHandle: int | None = None
	try:
		readFd = os.dup(_STDIN_FD)
		writeFd = os.dup(_STDOUT_FD)
		_redirectStandardStreams()
		# ``PipeStream`` closes the handles it is built from, so it has to be their sole owner:
		# leaving the descriptors open would hand the C runtime a second claim on them.
		readHandle = claimHandleFromDescriptor(readFd)
		readFd = -1
		writeHandle = claimHandleFromDescriptor(writeFd)
		writeFd = -1
	# Deliberately not ``except BaseException``:
	# a signal-delivered exception can land between a successful claim and resetting the variable  to its sentinel,
	# at which point the descriptor has been closed, unbeknownst to us.
	# Closing it again could land on a recycled descriptor,
	# so leaking it is the safest option.
	except Exception:
		if readFd >= 0:
			os.close(readFd)
		if writeFd >= 0:
			os.close(writeFd)
		if readHandle is not None:
			CloseHandle(readHandle)
		raise
	return PipeStream(readHandle, writeHandle)


def _initializeLogging() -> None:
	"""Send this process's log output to standard error.

	Configures the ``_art`` logger tree root, which every ART logger propagates to, so all of the host's records reach the handler.
	The level is set as low as it goes so that the host captures everything for now;
	NVDA drains the host's standard error into its own log.
	"""
	artLog = logging.getLogger("_art")
	artLog.setLevel(logging.DEBUG)
	handler = logging.StreamHandler(sys.stderr if sys.stderr is not None else open(os.devnull))  # noqa: SIM115
	handler.setFormatter(logging.Formatter("ART host: %(levelname)s - %(name)s - %(message)s"))
	artLog.addHandler(handler)


def main(argv: list[str] | None = None) -> int:
	"""Entry point of the host process.

	:param argv: Unused for now.
		Accepted so that the build ID and the launch arguments that follow it have somewhere to go.
	:returns: Process exit status.
		0 on success;
		1 if claiming the control stream fails, or if we get an unhandled exception from ``run``.
	"""
	# Mark this process as the host before any shared module is imported,
	# so shared code doesn't attempt to pull in core.
	os.environ[_HOST_MARKER_ENV] = "1"
	try:
		stream = _claimControlStream()
	except OSError as exc:
		# We don't have logging yet, so output directly to stderr, if it exists.
		if sys.stderr is not None:
			print("ART host could not claim its control stream", file=sys.stderr)
			traceback.print_exception(exc, file=sys.stderr)
		return 1
	_initializeLogging()
	# Import late because we needed to add the host marker first.
	from .._log import log

	try:
		run(stream)
	except Exception:  # noqa: BLE001
		log.exception("Unhandled exception in ART host")
		return 1
	return 0


if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
