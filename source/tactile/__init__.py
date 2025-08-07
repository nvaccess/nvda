# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.


import abc

"""
This package provides classes for working with tactile graphics.
"""


class TactileGraphicsBuffer(abc.ABC):
	"""
	An abstract class representing a buffer for storing tactile graphics.
	The buffer has a width and height, and single dots can be set using the setDot method.
	"""

	width: int
	height: int

	def __init__(self, width: int, height: int):
		"""
		Initializes the buffer with the given width and height.
		"""
		self.width = width
		self.height = height

	@abc.abstractmethod
	def setDot(self, x, y):
		"""
		Sets a dot at the given coordinates.
		"""
		pass
