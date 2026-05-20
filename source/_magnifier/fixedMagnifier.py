# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
Fixed magnifier module.
"""

from .magnifier import Magnifier
from .utils.types import MagnifiedView


class FixedMagnifier(Magnifier):
	"""Displays a floating magnified panel that can be pinned anywhere on the screen."""

	_MAGNIFIED_VIEW = MagnifiedView.FIXED

	def __init__(self):
		super().__init__()

	def _startMagnifier(self) -> None:
		super()._startMagnifier()

	def _stopMagnifier(self) -> None:
		super()._stopMagnifier()

	def _doUpdate(self):
		pass
