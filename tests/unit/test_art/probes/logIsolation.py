# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Child program checking that the host's logging stays isolated from NVDA core.

Run as a process by ``TestHostLoggingIsolation``.
Must run in its own process because :mod:`_art._log` chooses its logger once, at import time,
from the host marker, and a core-side test process has already resolved that choice the other way
(and imported ``logHandler``).

It reproduces the ordering of the real host boot path:

* import the entry point, which must not pull core in by itself;
* set the host marker exactly as :func:`_art.host.entrypoint.main` does;
* import the transport tree, which reaches :mod:`_art._log`.

At each step it checks that ``logHandler`` never becomes resident,
and finally that shared code received the host's own logger (with the NVDA methods it relies on).

Exits ``0`` if the host stayed isolated, and non-zero with a diagnostic on standard error otherwise.
"""

import os
import sys


def _check() -> list[str]:
	"""Boot far enough to import the transport, checking core never comes with it.

	:returns: Human-readable descriptions of each failed expectation, empty if all held.
	"""
	import _art
	from _art.host import (
		entrypoint,  # noqa: F401 - Needed to assert that the entrypoint itself doesn't import logHandler
	)

	failures: list[str] = []
	if "logHandler" in sys.modules:
		failures.append("importing the host entry point pulled in logHandler")

	# Mark this process as the host, exactly as ``entrypoint.main`` does,
	# before importing anything that reaches ``_art._log``.
	os.environ[_art._HOST_MARKER_ENV] = "1"

	import _art.transport

	artTransportBroughtLogHandler = False
	if "logHandler" in sys.modules:
		failures.append("importing the transport tree pulled in logHandler")
		artTransportBroughtLogHandler = True

	from _art._log import log

	if not artTransportBroughtLogHandler and "logHandler" in sys.modules:
		failures.append("importing the log shim  pulled in logHandler")

	if not hasattr(log, "debugWarning"):
		failures.append("the host logger has no debugWarning method")
	else:
		try:
			log.debugWarning("host logging isolation probe")
		except Exception as caught:  # noqa: BLE001
			failures.append(f"log.debugWarning raised: {caught!r}")

	return failures


if __name__ == "__main__":
	failures = _check()
	if failures:
		sys.stderr.write("; ".join(failures))
		sys.exit(1)
	sys.exit(0)
