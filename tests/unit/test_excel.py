# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022 NV Access Limited

"""Unit tests for the excel module.
"""

import unittest
import NVDAObjects.window.excel as excel


class TestCellStates(unittest.TestCase):
	def test_cellStateMapsToState(self):
		"""All Excel Cell info states should map to a controlTypes.State
		"""
		for cellState in excel.NvCellState:
			excel._nvCellStatesToStates[cellState]  # throws if cellState is missing
