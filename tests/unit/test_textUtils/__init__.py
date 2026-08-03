# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the textUtils package."""

import unittest

from winBindings.icu import ICU_AVAILABLE


skipIfNoICU = unittest.skipUnless(ICU_AVAILABLE, "ICU library not available on this system")
"""Decorator skipping tests that need the Windows built-in ICU library."""
