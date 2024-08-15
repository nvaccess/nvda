# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.


class TactileGraphicsBuffer:
	width: int
	height: int

	def __init__(self, width: int, height: int):
		self.width = width
		self.height = height

	def setDot(self, x, y):
		pass
