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

import sys
from typing import Final

from rpyc.core.stream import Stream

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


def main(argv: list[str] | None = None) -> int:
	"""Entry point of the host process.

	:param argv: Unused for now.
		Accepted so that the build ID and the launch arguments that follow it have somewhere to go.
	:returns: Process exit status.
	"""
	raise NotImplementedError


if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
