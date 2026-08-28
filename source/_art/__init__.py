# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""NVDA Add-on Runtime (ART)

This package defines NVDA's out-of-process, sandboxed add-on runtime.

* :mod:`.transport`: Generic transport over anonymous pipes.
* :mod:`.host`: The add-on side of the boundary:
	the host entry point and the root service it exposes to core.
* :mod:`.session`: The core side of the boundary:
	host controllers, core-side wire ends, and the root service core exposes to the host.
* :mod:`.exceptions`: The capability failure taxonomy, shared by both sides.
* :mod:`.winHandles`: Handle ownership helpers, shared by both sides.
"""
