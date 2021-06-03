# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2017-2021 NV Access Limited, Babbage B.V.

"""Classes and helper functions for working with rectangles and coordinates."""

from collections import namedtuple
from collections.abc import Sequence
import windowUtils
import winUser
from ctypes.wintypes import RECT, POINT, DWORD
import wx

class Point(namedtuple("Point",("x","y"))):
	"""Represents a point on the screen."""

	@classmethod
	def fromFloatCollection(cls, *floats):
		"""Creates an instance from float parameters.
		The provided parameters will be converted to ints automatically.
		@raise TypeError: If one of the input parameters isn't a float.
		"""
		if not all(isinstance(f, float) for f in floats):
			raise TypeError("All input parameters must be of type float")
		return cls(*map(int, floats))

	@classmethod
	def fromCompatibleType(cls, point):
		"""Creates an instance from a compatible type.
		Compatible types are defined in L{POINT_CLASSES}.
		"""
		if isinstance(point,POINT_CLASSES):
			return cls(point.x, point.y)
		raise TypeError("point should be one of %s" % ", ".join(cls.__module__+"."+cls.__name__ for cls in POINT_CLASSES))

	@classmethod
	def fromDWORD(cls, dwPoint):
		if isinstance(dwPoint,DWORD):
			dwPoint = dwPoint.value
		if not isinstance(dwPoint, int):
			raise TypeError("dwPoint should be either int or ctypes.wintypes.DWORD (ctypes.ulong)")
		return Point(winUser.GET_X_LPARAM(dwPoint),winUser.GET_Y_LPARAM(dwPoint))

	def __add__(self,other):
		"""Returns a new L{Point} with its coordinates representing the additions of the original x and y coordinates."""
		if not isinstance(other,POINT_CLASSES):
			return NotImplemented
		return Point((self.x+other.x),(self.y+other.y))

	def __radd__(self,other):
		"""Returns a new L{Point} with x = self.x + other.x and y = self.y + other.y."""
		if other == 0:
			return self
		elif not isinstance(other,POINT_CLASSES):
			return NotImplemented
		return Point((other.x+self.x),(other.y+self.y))

	def __sub__(self,other):
		if not isinstance(other,POINT_CLASSES):
			return NotImplemented
		return Point((self.x-other.x),(self.y-other.y))

	def __rsub__(self,other):
		if not isinstance(other,POINT_CLASSES):
			return NotImplemented
		return Point((other.x-self.x),(other.y-self.y))

	def yWiseLessThan(self,other):
		"""
		Returns whether self is less than other, first comparing y, then x coordinates.
		For example: (x=4,y=3) < (x=3,y=4) because self.y is less than other.y.
		To compare in opposite order (i.e. compare x, then y), use L{xWiseLessThan}
		"""
		if not isinstance(other,POINT_CLASSES):
			return NotImplemented
		return (self.y, self.x) < (other.y, other.x)

	def xWiseLessThan(self,other):
		"""
		Returns whether self is less than other, first comparing x, then y coordinates.
		For example: (x=3,y=4) < (x=4,y=3) because self.x is less than other.x.
		To compare in opposite order (i.e. compare y, then x), use L{yWiseLessThan}
		"""
		if not isinstance(other,POINT_CLASSES):
			return NotImplemented
		return (self.x, self.y) < (other.x, other.y)

	def yWiseLessOrEq(self,other):
		"""
		Returns whether self is less than or equal to other, first comparing y, then x coordinates.
		For example: (x=4,y=3) <= (x=3,y=4) because self.y is less than or equal to other.y.
		To compare in opposite order (i.e. compare x, then y), use L{xWiseLessOrEq}
		"""
		if not isinstance(other,POINT_CLASSES):
			return NotImplemented
		return (self.y, self.x) <= (other.y, other.x)

	def xWiseLessOrEq(self,other):
		"""
		Returns whether self is less than or equal to other, first comparing x, then y coordinates.
		For example: (x=3,y=4) <= (x=4,y=3) because self.x is less than or equal to other.x.
		To compare in opposite order (i.e. compare y, then x), use L{yWiseLessOrEq}
		"""
		if not isinstance(other,POINT_CLASSES):
			return NotImplemented
		return (self.x, self.y) <= (other.x, other.y)

	def yWiseGreaterThan(self,other):
		"""
		Returns whether self is greater than other, first comparing y, then x coordinates.
		For example: (x=3,y=4) > (x=4,y=3) because self.y is greater than other.y.
		To compare in opposite order (i.e. compare x, then y), use L{xWiseGreaterThan}
		"""
		if not isinstance(other,POINT_CLASSES):
			return NotImplemented
		return (self.y, self.x) > (other.y, other.x)

	def xWiseGreaterThan(self,other):
		"""
		Returns whether self is greater than other, first comparing x, then y coordinates.
		For example: (x=4,y=3) > (x=3,y=4) because self.x is greater than other.x.
		To compare in opposite order (i.e. compare y, then x), use L{yWiseGreaterThan}
		"""
		if not isinstance(other,POINT_CLASSES):
			return NotImplemented
		return (self.x, self.y) > (other.x, other.y)

	def yWiseGreaterOrEq(self,other):
		"""
		Returns whether self is greater than or equal to other, first comparing y, then x coordinates.
		For example: (x=3,y=4) >= (x=4,y=3) because self.y is greater than or equal to other.y.
		To compare in opposite order (i.e. compare x, then y), use L{xWiseGreaterOrEq}
		"""
		if not isinstance(other,POINT_CLASSES):
			return NotImplemented
		return (self.y, self.x) >= (other.y, other.x)

	def xWiseGreaterOrEq(self,other):
		"""
		Returns whether self is greater than or equal to other, first comparing x, then y coordinates.
		For example: (x=4,y=3) >= (x=3,y=4) because self.x is greater than or equal to other.x.
		To compare in opposite order (i.e. compare y, then x), use L{yWiseGreaterOrEq}
		"""
		if not isinstance(other,POINT_CLASSES):
			return NotImplemented
		return (self.x, self.y) >= (other.x, other.y)

	def __eq__(self,other):
		if not isinstance(other,POINT_CLASSES):
			return NotImplemented
		return self.x == other.x and self.y == other.y

	# As __eq__ was defined on this class, we must provide __hash__ to remain hashable.
	def __hash__(self):
		return super().__hash__()

	def __ne__(self,other):
		if not isinstance(other,POINT_CLASSES):
			return NotImplemented
		return self.x != other.x or self.y != other.y

	def toPOINT(self):
		"""Converts self to a L{ctypes.wintypes.POINT}"""
		return POINT(self.x,self.y)

	def toLogical(self, hwnd):
		"""Converts self from physical to logical coordinates and returns a new L{Point}."""
		return Point(*windowUtils.physicalToLogicalPoint(hwnd, *self))

	def toPhysical(self, hwnd):
		"""Converts self from logical to physical coordinates and returns a new L{Point}"""
		return Point(*windowUtils.logicalToPhysicalPoint(hwnd, *self))

	def toClient(self, hwnd):
		"""Converts self from screen to client coordinates and returns a new L{Point}"""
		return Point(*winUser.ScreenToClient(hwnd, *self))

	def toScreen(self, hwnd):
		"""Converts self from client to screen coordinates and returns a new L{Point}"""
		return Point(*winUser.ClientToScreen(hwnd, *self))

class _RectMixin:
	"""Mix-in class for properties shared between RectLTRB and RectLTWH classes"""

	@classmethod
	def fromFloatCollection(cls, *floats):
		"""Creates an instance from float parameters.
		The provided parameters will be converted to ints automatically.
		@raise TypeError: If one of the input parameters isn't a float.
		"""
		if not all(isinstance(f, float) for f in floats):
			raise TypeError("All input parameters must be of type float")
		return cls(*map(int, floats))

	@classmethod
	def fromCompatibleType(cls, rect):
		"""Creates an instance from a compatible type.
		Compatible types are defined in L{RECT_CLASSES}.
		"""
		if isinstance(rect,cls):
			return rect
		if isinstance(rect,RECT_CLASSES):
			if cls is RectLTWH:
				return cls(rect.left, rect.top, rect.right-rect.left, rect.bottom-rect.top)
			elif cls is RectLTRB:
				return cls(rect.left, rect.top, rect.right, rect.bottom)
		raise TypeError("rect should be one of %s" % ", ".join(cls.__module__+"."+cls.__name__ for cls in RECT_CLASSES))

	@classmethod
	def fromPoint(cls, point):
		"""Creates an instance from a compatible point type with a width and height of 0."""
		if isinstance(point,POINT_CLASSES):
			if cls is RectLTWH:
				return cls(point.x, point.y, 0, 0)
			elif cls is RectLTRB:
				return cls(point.x, point.y, point.x, point.y)
			else:
				raise RuntimeError("%s is not known as a valid subclass of _RectMixin" % cls.__name__)
		raise TypeError("point should be one of %s" % ", ".join(cls.__module__+"."+cls.__name__ for cls in POINT_CLASSES))

	@classmethod
	def fromCollection(cls, *items):
		"""Creates a bounding rectangle for the provided collection of items.
		The highest coordinates found in the collection are considered exclusive.
		For example, if you provide Point(x=1,y=1) and point(x=2,y=2),
		The resulting rectangle coordinates are left=1,top=1,right=2,bottom=2.
		Input could be of mixed types from either L{RECT_CLASSES} or L{POINT_CLASSES}.
		"""
		if len(items)==0:
			raise TypeError("This function takes at least 1 argument (0 given)")
		xs=set()
		ys=set()
		for item in items:
			if isinstance(item,RECT_CLASSES):
				xs.update((item.left,item.right))
				ys.update((item.top,item.bottom))
			elif isinstance(item,POINT_CLASSES):
				xs.add(item.x)
				ys.add(item.y)
			else:
				raise ValueError("Unexpected parameter %s"%str(item))
		left=min(xs)
		top=min(ys)
		right=max(xs)
		bottom=max(ys)
		if cls is RectLTWH:
			return cls(left, top, right-left, bottom-top)
		return cls(left, top, right, bottom)

	def toRECT(self):
		"""Converts self to a L{ctypes.wintypes.RECT}"""
		return RECT(self.left,self.top,self.right,self.bottom)

	def toLogical(self, hwnd):
		left,top=self.topLeft.toLogical(hwnd)
		right,bottom=self.bottomRight.toLogical(hwnd)
		if isinstance(self, RectLTWH):
			return RectLTWH(left,top,right-left,bottom-top)
		return RectLTRB(left,top,right,bottom)

	def toPhysical(self, hwnd):
		left,top=self.topLeft.toPhysical(hwnd)
		right,bottom=self.bottomRight.toPhysical(hwnd)
		if isinstance(self, RectLTWH):
			return RectLTWH(left,top,right-left,bottom-top)
		return RectLTRB(left,top,right,bottom)

	def toClient(self, hwnd):
		left, top =self.topLeft.toClient(hwnd)
		if isinstance(self, RectLTWH):
			return RectLTWH(left, top, self.width, self.height)
		return RectLTRB(left, top, left+self.width, top+self.height)

	def toScreen(self, hwnd):
		left,top=self.topLeft.toScreen(hwnd)
		if isinstance(self, RectLTWH):
			return RectLTWH(left, top, self.width, self.height)
		return RectLTRB(left, top, left+self.width, top+self.height)

	@property
	def topLeft(self):
		return Point(self.left,self.top)

	@property
	def topRight(self):
		return Point(self.right,self.top)

	@property
	def bottomLeft(self):
		return Point(self.left,self.bottom)

	@property
	def bottomRight(self):
		return Point(self.right,self.bottom)

	@property
	def center(self):
		return Point(int(round(self.left+self.width/2.0)), int(round(self.top+self.height/2.0)))

	def __contains__(self,other):
		"""Returns whether other is a part of this rectangle."""
		if isinstance(other,POINT_CLASSES):
			return self.left <= other.x < self.right and  self.top <= other.y < self.bottom
		if not isinstance(other,RECT_CLASSES):
			return NotImplemented
		return self.isSuperset(other) and self!=other

	def isSubset(self,other):
		"""Returns whether this rectangle is a subset of other (i.e. whether all points in this rectangle are contained by other)."""
		if not isinstance(other,RECT_CLASSES):
			return False
		return other.left<=self.left<=self.right<=other.right and other.top<=self.top<=self.bottom<=other.bottom

	def isSuperset(self,other):
		"""Returns whether this rectangle is a superset of other (i.e. whether all points of other are contained by this rectangle)."""
		if not isinstance(other,RECT_CLASSES):
			raise TypeError("other should be one of %s" % ", ".join(cls.__module__+"."+cls.__name__ for cls in RECT_CLASSES))
		return self.left<=other.left<=other.right<=self.right and self.top<=other.top<=other.bottom<=self.bottom

	def __eq__(self,other):
		if not isinstance(other,RECT_CLASSES):
			return NotImplemented
		return other.left == self.left and other.top == self.top and other.right == self.right and other.bottom == self.bottom

	# As __eq__ was defined on this class, we must provide __hash__ to remain hashable.
	def __hash__(self):
		return super().__hash__()

	def __ne__(self,other):
		if not isinstance(other,RECT_CLASSES):
			return NotImplemented
		return other.left != self.left or other.top != self.top or other.right != self.right or other.bottom != self.bottom

	def intersection(self,other):
		"""Returns the intersection of self and other.
		For example, if self = Rect(left=10,top=10,right=25,bottom=25) and other = Rect(left=20,top=20,right=35,bottom=35),
		this results in Rect(left=20,top=20,right=25,bottom=25).
		No intersect results in a rectangle with zeroed coordinates.
		"""
		if not isinstance(other,RECT_CLASSES):
			raise TypeError("other should be one of %s" % ", ".join(cls.__module__+"."+cls.__name__ for cls in RECT_CLASSES))
		left=max(self.left,other.left)
		top=max(self.top,other.top)
		right=min(self.right,other.right)
		bottom=min(self.bottom,other.bottom)
		if left>right or top>bottom:
			left=top=right=bottom=0
		if isinstance(self, RectLTWH):
			return RectLTWH(left,top,right-left,bottom-top)
		return RectLTRB(left,top,right,bottom)

	def expandOrShrink(self, margin):
		"""Expands or shrinks the boundaries of the rectangle with the given margin.
		For example, if self = Rect(left=10,top=10,right=25,bottom=25) and margin = 10,
		this results in Rect(left=0,top=0,right=35,bottom=35).
		If self = Rect(left=10,top=10,right=25,bottom=25) and margin = -5,
		this results in Rect(left=15,top=15,right=20,bottom=20).
		"""
		if not isinstance(margin, int):
			raise TypeError("Margin should be an integer")
		left=self.left-margin
		top=self.top-margin
		right=self.right+margin
		bottom=self.bottom+margin
		if left>right or top>bottom:
			raise RuntimeError("The provided margin of %d would result in a rectangle with a negative width or height, which is not allowed"%margin)
		if isinstance(self, RectLTWH):
			return RectLTWH(left,top,right-left,bottom-top)
		return RectLTRB(left,top,right,bottom)

class RectLTWH(_RectMixin, namedtuple("RectLTWH",("left","top","width","height"))):
	"""
	Represents a rectangle on the screen, based on left and top coordinates, width and height.
	To represent a rectangle using left, top, right and bottom coordinates, use L{RectLTRB}.
	"""

	@property
	def right(self):
		return self.left+self.width

	@property
	def bottom(self):
		return self.top+self.height

	def toLTRB(self):
		return RectLTRB(self.left,self.top,self.right,self.bottom)

class RectLTRB(_RectMixin, namedtuple("RectLTRB",("left","top","right","bottom"))):
	"""Represents a rectangle on the screen.
	By convention, the right and bottom edges of the rectangle are normally considered exclusive.
	To represent a rectangle based on width and height instead, use L{RectLTWH}.
	"""

	def __new__(cls, left, top, right, bottom):
		if left>right:
			raise ValueError("left=%d is greater than right=%d, which is not allowed" % (left, right))
		if top>bottom:
			raise ValueError("top=%d is greater than bottom=%d, which is not allowed" % (top, bottom))
		return super(RectLTRB, cls).__new__(cls, left, top, right, bottom)

	@property
	def width(self):
		return self.right-self.left

	@property
	def height(self):
		return self.bottom-self.top

	def toLTWH(self):
		return RectLTWH(self.left,self.top,self.width,self.height)

#: Classes which support conversion to locationHelper Points using their x and y properties.
#: type: tuple
POINT_CLASSES=(Point, POINT, wx.Point)
#: Classes which support conversion to locationHelper RectLTRB/LTWH using their left, top, right and bottom properties.
#: type: tuple
RECT_CLASSES=(RectLTRB, RectLTWH, RECT)
