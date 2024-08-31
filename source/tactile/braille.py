# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.


"""
This module provides functions for drawing Braille cells on a TactileGraphicsBuffer.
"""

from . import TactileGraphicsBuffer


CELL_WIDTH = 2


_brailleDotCoords = [
	# dot1
	(0, 0),
	# dot2
	(0, 1),
	# dot3
	(0, 2),
	# dot4
	(1, 0),
	# dot5
	(1, 1),
	# dot6
	(1, 2),
	# dot7
	(0, 3),
	# dot8
	(1, 3),
]


def drawBrailleCells(tgBuf: TactileGraphicsBuffer, x: int, y: int, cells: list[int], hCellPadding: int = 1):
	"""
	Draws Braille cells on the given TactileGraphicsBuffer.
	:param tgBuf: The TactileGraphicsBuffer to draw on.
	:param x: The x coordinate of the top-left corner of the first cell.
	:param y: The y coordinate of the top-left corner of the first cell.
	:param cells: A list of 8-bit integers representing the Braille cells to draw.
	:param hCellPadding: The horizontal padding between cells.
	"""
	for cell in cells:
		for dot in range(0, 8):
			if 1 << dot & cell:
				dotX, dotY = _brailleDotCoords[dot]
				# Check if the coordinates are within bounds
				if 0 <= (x + dotX) < tgBuf.width and 0 <= (y + dotY) < tgBuf.height:
					tgBuf.setDot(x + dotX, y + dotY)
		x += CELL_WIDTH + hCellPadding
