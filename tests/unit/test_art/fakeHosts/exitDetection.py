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

Unlike a probe, this does not check anything itself; the test observes how core copes with it.
"""

from __future__ import annotations

import os
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING, Final

from _art.host import entrypoint

if TYPE_CHECKING:
	from rpyc.core.stream import Stream


def _exitBeforeReady(stream: Stream, status: str) -> None:
	os._exit(int(status))


_BEHAVIOURS: Final[dict[str, Callable[Stream, str]]] = {
	"exitBeforeReady": _exitBeforeReady,
}


if __name__ == "__main__":
	entrypoint.run = lambda stream: _BEHAVIOURS[sys.argv[1]](stream, *sys.argv[2:])
	sys.exit(entrypoint.main())
