# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 NV Access Limited.

import unittest
from appModules.code import AppModule

class Test_Code_AppModule(unittest.TestCase):
    def test_looks_like_line_col(self):
        # Valid cases
        self.assertTrue(AppModule._looks_like_line_col("Line 10, Col 5"))
        self.assertTrue(AppModule._looks_like_line_col("10:5"))
        self.assertTrue(AppModule._looks_like_line_col("Line: 10 Column: 5"))
        
        # Invalid cases
        self.assertFalse(AppModule._looks_like_line_col("10.5")) # Version-like
        self.assertFalse(AppModule._looks_like_line_col("10 5")) # Just space (as per line 78 logic)
        self.assertFalse(AppModule._looks_like_line_col("10")) # Only one number
        self.assertFalse(AppModule._looks_like_line_col("No numbers here"))
        self.assertFalse(AppModule._looks_like_line_col("v1.2.3"))
        self.assertFalse(AppModule._looks_like_line_col("   10   5   ")) # Only whitespace between
