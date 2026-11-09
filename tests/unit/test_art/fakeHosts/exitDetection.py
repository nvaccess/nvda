# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Child program standing in for a misbehaving ART host.

Run as a process by the lifecycle conformance tests, as ``fakeHost.py <behaviour> [arguments]``.
Boots through the real :func:`_art.host.entrypoint.main`,
so the standard streams, host marker and logging are set up exactly as in a real host,
but swaps in a host half that misbehaves in the way ``behaviour`` names:

* ``exitBeforeReady <status>``: exits immediately with ``status``, without signalling readiness.
* ``exitBeforeServe <status>``: exits immediately after signalling readiness with ``status``.
* ``closeAndLinger``: closes the control connection without signalling readiness, then stays running.

Unlike a probe, this does not check anything itself; the test observes how core copes with it.
"""

from __future__ import annotations

import os
import sys
import time
from collections.abc import Callable
from typing import TYPE_CHECKING, Final

from _art.host import entrypoint

if TYPE_CHECKING:
	from rpyc.core.stream import Stream

#: How long a lingering host stays up, in seconds; far longer than any test should take to kill it.
_LINGER_SECONDS: float = 600.0


def _exitBeforeReady(stream: Stream, status: str) -> None:
	os._exit(int(status))


def _exitBeforeServe(stream: Stream, status: str) -> None:
	from _art.host.rootService import HostRootService
	from _art.transport import Connection

	conn = Connection(stream, HostRootService, name=entrypoint.CONTROL_CONNECTION_NAME)
	entrypoint._signalReadiness(conn)
	os._exit(int(status))


def _closeAndLinger(stream) -> None:
	stream.close()
	time.sleep(_LINGER_SECONDS)


_BEHAVIOURS: Final[dict[str, Callable[Stream, str]]] = {
	"exitBeforeReady": _exitBeforeReady,
	"exitBeforeServe": _exitBeforeServe,
	"closeAndLinger": _closeAndLinger,
}


if __name__ == "__main__":
	entrypoint.run = lambda stream: _BEHAVIOURS[sys.argv[1]](stream, *sys.argv[2:])
	sys.exit(entrypoint.main())
