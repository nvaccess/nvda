# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
Core-side ownership of add-on sessions.

An add-on session is the full live unit:
host process, loaded add-on, granted capabilities, and the control connection between them.
This package owns launching one, watching it, and tearing it down.

* :mod:`.rootService`: the root service core exposes to the host.
"""
