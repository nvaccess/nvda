# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""A host that hangs before readiness, or after readiness without serving its root service."""

import sys
import time

from _art.host import entrypoint
from rpyc.core.stream import Stream


def run(stream: Stream) -> None:
	if sys.argv[1] == "afterReady":
		from _art.host.rootService import HostRootService
		from _art.transport import Connection

		conn = Connection(stream, HostRootService(), name=entrypoint.CONTROL_CONNECTION_NAME)
		entrypoint._signalReadiness(conn)
	# Keep the stream open, but never serve requests. Core must kill this process.
	time.sleep(600)


if __name__ == "__main__":
	entrypoint.run = run
	sys.exit(entrypoint.main())
