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
from typing import Final

from rpyc.core.stream import PipeStream, Stream
from winBindings.kernel32 import CloseHandle

from .. import _HOST_MARKER_ENV
from ..winHandles import claimHandleFromDescriptor

#: Name of the host's end of the control connection, used in logging.
CONTROL_CONNECTION_NAME: Final[str] = "ART host control"


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


def _claimControlStream() -> Stream:
	"""Take private ownership of the standard descriptors and return the control stream.

	The control connection runs over stdin and stdout,  which carry framed rpyc traffic rather than text.
	Writing anything else to them will corrupt the connection.
	To ensure the wire has exclusive use of the original descriptors, duplicate them, then:

	* point stdin (descriptor 0) at the null device; and
	* alias stdout (descriptor 1)  to stderr (descriptor 2).

	The duplicated descriptors are then converted into handles the returned stream solely owns,
	so that nothing else closes them out from under it
	(see :func:`_art.winHandles.claimHandleFromDescriptor`).

	Standard error is the host's diagnostic channel,
	which NVDA drains to its log.

	:returns: The host's end of the control connection.
	"""
	# File descriptors of the standard streams.
	STDIN_FD: Final[int] = 0
	STDOUT_FD: Final[int] = 1
	STDERR_FD: Final[int] = 2
	# Duplicate the current stdin and stdout for our own use
	readFd = os.dup(STDIN_FD)
	try:
		writeFd = os.dup(STDOUT_FD)
	except:
		os.close(readFd)
		raise
	try:
		# Make stdin point to the null device
		devNullFd = os.open(os.devnull, os.O_RDWR)
		try:
			os.dup2(devNullFd, STDIN_FD)
		finally:
			os.close(devNullFd)
		sys.stdin = open(os.devnull)  # noqa: SIM115
		# make stdout point to stderr
		try:
			os.dup2(STDERR_FD, STDOUT_FD)
		except OSError:
			# No usable standard error, so redirect to the null device instead
			devNullFd = os.open(os.devnull, os.O_RDWR)
			try:
				os.dup2(devNullFd, STDOUT_FD)
			finally:
				os.close(devNullFd)
		sys.stdout = sys.stderr if sys.stderr is not None else open(os.devnull, "w")  # noqa: SIM115
	except:
		os.close(readFd)
		os.close(writeFd)
		raise
	# ``PipeStream`` closes the handles it is built from, so it has to be their sole owner:
	# leaving the descriptors open would hand the C runtime a second claim on them.
	try:
		readHandle = claimHandleFromDescriptor(readFd)
	except OSError:
		os.close(readFd)
		os.close(writeFd)
		raise
	try:
		writeHandle = claimHandleFromDescriptor(writeFd)
	except OSError:
		os.close(writeFd)
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
	handler = logging.StreamHandler(sys.stderr)
	handler.setFormatter(logging.Formatter("ART host: %(levelname)s - %(name)s - %(message)s"))
	artLog.addHandler(handler)


def main(argv: list[str] | None = None) -> int:
	"""Entry point of the host process.

	:param argv: Unused for now.
		Accepted so that the build ID and the launch arguments that follow it have somewhere to go.
	:returns: Process exit status.
	"""
	# Mark this process as the host before any shared module is imported,
	# so shared code doesn't attempt to pull in core.
	os.environ[_HOST_MARKER_ENV] = "1"
	try:
		stream = _claimControlStream()
	except OSError:
		# We don't have logging yet, so output directly to stderr.
		print("ART host could not claim its control stream", file=sys.stderr)
		raise
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
