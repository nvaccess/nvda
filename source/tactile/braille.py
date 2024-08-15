# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.


from . import TactileGraphicsBuffer


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


def drawBrailleCells(tgBuf: TactileGraphicsBuffer, x: int, y: int, cells: list[int]):
	for cell in cells:
		for dot in range(0, 8):
			if 1 << dot & cell:
				dotX, dotY = _brailleDotCoords[dot]
				tgBuf.setDot(x + dotX, y + dotY)
		x += 3
