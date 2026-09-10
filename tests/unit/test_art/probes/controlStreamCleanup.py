# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Child program asserting that a failed host boot strands neither a descriptor nor a handle.

Run as a process by ``TestControlStreamHandleOwnership``, for the same reason as
``controlStream.py``: :func:`_art.host.entrypoint._claimControlStream` takes over the standard
streams of whichever process calls it, which is not something a test runner can survive.

``controlStream.py`` covers the success path; this covers the unwind. Takes the one-based index of
the claim to fail as its only argument, because the two claims strand different things:

* failing the first leaves two descriptors to close; and
* failing the second leaves one descriptor and one handle, which need different calls to release.

Reports what it saw on standard error, and exits non-zero if the unwind was incomplete.
"""

import msvcrt
import os
import sys
from typing import Any, Final

from _art.host import entrypoint

#: One-based index of the claim to fail.
FAILING_CLAIM: Final[int] = int(sys.argv[1])

#: Descriptors ``_claimControlStream`` duplicated for the control connection.
duplicated: list[int] = []
#: Handles it claimed before the induced failure.
claimed: list[int] = []
#: Handles it released while unwinding.
released: list[int] = []

_realDup = os.dup
_realClaim = entrypoint.claimHandleFromDescriptor
_realCloseHandle = entrypoint.CloseHandle


def _spyDup(fd: int) -> int:
	"""Stand in for :func:`os.dup`, recording what it hands out."""
	duplicate = _realDup(fd)
	duplicated.append(duplicate)
	return duplicate


def _failNthClaim(fd: int) -> int:
	"""Claim for real until ``FAILING_CLAIM``, then fail the way an unclaimable descriptor would.

	``claimHandleFromDescriptor`` leaves its descriptor open when it fails, so the caller is still
	the owner of ``fd``, along with anything claimed before it.
	"""
	if len(claimed) + 1 == FAILING_CLAIM:
		raise OSError("Induced claim failure")
	handle = _realClaim(fd)
	claimed.append(handle)
	return handle


def _spyCloseHandle(handle: int) -> Any:
	"""Stand in for ``CloseHandle``, recording what the unwind releases before releasing it."""
	released.append(handle)
	return _realCloseHandle(handle)


os.dup = _spyDup
entrypoint.claimHandleFromDescriptor = _failNthClaim
entrypoint.CloseHandle = _spyCloseHandle
try:
	entrypoint._claimControlStream()
except OSError:
	propagated = True
else:
	propagated = False
finally:
	os.dup = _realDup
	entrypoint.claimHandleFromDescriptor = _realClaim
	entrypoint.CloseHandle = _realCloseHandle

# Checked before anything is written, so that nothing of ours can reuse a descriptor number first.
# A descriptor that still resolves to a handle is a second owner of one the unwind should have closed.
retained: list[int] = []
for fd in duplicated:
	try:
		msvcrt.get_osfhandle(fd)
	except OSError:
		continue
	retained.append(fd)

sys.stderr.write(f"{propagated=} {duplicated=} {retained=} {claimed=} {released=}")
# Every handle claimed before the failure must have been released, and no descriptor kept back.
sys.exit(0 if propagated and len(duplicated) == 2 and not retained and released == claimed else 1)
