# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 NV Access Limited

"""Shared, near-zero-cost signal for "an application recently hung / the core was
recently frozen".

NVDA's object model resolves every property by synchronously calling into the
owning application. When an application stops responding, those calls block the
core thread. Various subsystems (the watchdog, the UIA client jam breaker, the
MSAA winEvent hung-window drop, the Word object-model timeout) detect this and
call L{noteAppHang}. Hot paths (notably C{NVDAObject._getPropertyViaCache}) can
then cheaply ask L{isHungModeActive} whether to switch to a bounded, fall-back
mode instead of risking an indefinite block.

This module deliberately has no NVDA dependencies (only the standard library) so
it can be imported from anywhere, including very low-level modules, without
circular-import risk, and so the check is a single float comparison.
"""

import time

#: Monotonic timestamp of the most recently detected hang/freeze, or 0.0 if none.
_lastHangTime: float = 0.0

#: How long (seconds) hung mode stays active after the last detected hang. It is
#: refreshed each time a hang is detected, so a sustained hang keeps it active;
#: a healthy period of this length lets NVDA return to the normal (unguarded,
#: zero-overhead) path.
HUNG_MODE_WINDOW: float = 5.0


def noteAppHang() -> None:
	"""Record that an application hang / core freeze was just detected.

	Callable from any thread; it only writes a float.
	"""
	global _lastHangTime
	_lastHangTime = time.monotonic()


def isHungModeActive() -> bool:
	"""Whether a hang was detected within the last L{HUNG_MODE_WINDOW} seconds.

	This is the cheap gate hot paths check first. In normal operation it is a
	single subtraction and comparison and is always C{False}, so guarded code
	behaves exactly as before with negligible overhead.
	"""
	last = _lastHangTime
	if not last:
		return False
	return (time.monotonic() - last) < HUNG_MODE_WINDOW
