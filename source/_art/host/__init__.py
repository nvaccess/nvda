# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
The add-on side of the ART boundary.

This package is the boot code of the host process:
the entry point that attaches to the wire ends it was launched with,
and the root service it exposes back to core.

.. warning::
	Nothing in this package may import from core-side-only modules.
	Everything here executes inside the host process, alongside untrusted add-on code,
	so an add-on reading it learns nothing it did not already have.
	Core-side machinery must only ever reach the host over the control connection,
	never by being imported into it.
"""
