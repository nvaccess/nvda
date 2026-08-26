# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Dot Incorporated, Bram Duvigneau
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
Shared mutable state for the asyncio event loop module.
"""

import asyncio
from threading import Thread

TERMINATE_TIMEOUT_SECONDS = 5
"""Time to wait for tasks to finish while terminating the event loop."""

eventLoop: asyncio.BaseEventLoop | None = None
"""The asyncio event loop used by NVDA, or ``None`` before it is initialized."""
asyncioThread: Thread | None = None
"""Thread running the asyncio event loop, or ``None`` while it is not running."""
