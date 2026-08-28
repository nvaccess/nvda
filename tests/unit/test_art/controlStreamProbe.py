# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Child program asserting that the host boot path keeps no claim on its control descriptors.

Run as a process by ``TestControlStreamHandleOwnership``, because
:func:`_art.host.entrypoint._claimControlStream` takes over the standard streams of whichever
process calls it, which is not something a test runner can survive.

Reports the descriptors it saw on standard error, and exits non-zero if any of them outlived
the call.
"""

import msvcrt
import os
import sys

from _art.host import entrypoint

#: Descriptors ``_claimControlStream`` duplicated for the control connection.
duplicated: list[int] = []
_realDup = os.dup


def _spyDup(fd: int) -> int:
	"""Stand in for :func:`os.dup`, recording what it hands out."""
	duplicate = _realDup(fd)
	duplicated.append(duplicate)
	return duplicate


os.dup = _spyDup
try:
	entrypoint._claimControlStream()
finally:
	os.dup = _realDup

# A descriptor that still resolves to a handle is a second owner of one the stream will close.
retained: list[int] = []
for fd in duplicated:
	try:
		msvcrt.get_osfhandle(fd)
	except OSError:
		continue
	retained.append(fd)

sys.stderr.write(f"duplicated={duplicated} retained={retained}")
sys.exit(1 if retained or len(duplicated) != 2 else 0)
