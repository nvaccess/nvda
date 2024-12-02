# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
This module provides utility functions for working with tactile graphics.
"""

from typing import Tuple
from . import TactileGraphicsBuffer


def isPointInBounds(tgBuf: TactileGraphicsBuffer, x: int, y: int) -> bool:
	"""
	Check if a point lies within the buffer boundaries.
	:param tgBuf: The buffer to check against
	:param x: X coordinate to check
	:param y: Y coordinate to check
	:return: True if the point is within bounds, False otherwise
	"""
	return 0 <= x < tgBuf.width and 0 <= y < tgBuf.height


def setDotIfInBounds(tgBuf: TactileGraphicsBuffer, x: int, y: int) -> None:
	"""
	Set a dot at the given coordinates if they are within the buffer boundaries.
	:param tgBuf: The buffer to draw on
	:param x: X coordinate
	:param y: Y coordinate
	"""
	if isPointInBounds(tgBuf, x, y):
		tgBuf.setDot(x, y)


def getLineDirections(x1: int, y1: int, x2: int, y2: int) -> Tuple[int, int, int, int]:
	"""
	Calculate direction and delta values for line drawing.
	:param x1: Starting x coordinate
	:param y1: Starting y coordinate
	:param x2: Ending x coordinate
	:param y2: Ending y coordinate
	:return: Tuple of (dx, dy, xDirection, yDirection)
	"""
	dx = abs(x2 - x1)
	dy = abs(y2 - y1)
	xDirection = 1 if x1 == x2 else (1 if x1 < x2 else -1)
	yDirection = 1 if y1 == y2 else (1 if y1 < y2 else -1)
	return dx, dy, xDirection, yDirection
