#locationHelper.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017-2018 NV Access Limited, Babbage B.V.

"""Classes and helper functions for working with rectangles and coordinates."""

from collections import namedtuple
import windowUtils
import winUser
from ctypes.wintypes import RECT, SMALL_RECT, POINT
import textInfos
import wx

class Point(namedtuple("Point",("x","y"))):
	"""Represents a point on the screen."""

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
			try:
				other=toPoint(other)
			except ValueError:
				return False
		return (self.y, self.x) < (other.y, other.x)

	def xWiseLessThan(self,other):
		"""
		Returns whether self is less than other, first comparing x, then y coordinates.
		For example: (x=3,y=4) < (x=4,y=3) because self.x is less than other.x.
		To compare in opposite order (i.e. compare y, then x), use L{yWiseLessThan}
		"""
		if not isinstance(other,POINT_CLASSES):
			try:
				other=toPoint(other)
			except ValueError:
				return False
		return (self.x, self.y) < (other.x, other.y)

	def yWiseLessOrEq(self,other):
		"""
		Returns whether self is less than or equal to other, first comparing y, then x coordinates.
		For example: (x=4,y=3) <= (x=3,y=4) because self.y is less than or equal to other.y.
		To compare in opposite order (i.e. compare x, then y), use L{xWiseLessOrEq}
		"""
		if not isinstance(other,POINT_CLASSES):
			try:
				other=toPoint(other)
			except ValueError:
				return False
		return (self.y, self.x) <= (other.y, other.x)

	def xWiseLessOrEq(self,other):
		"""
		Returns whether self is less than or equal to other, first comparing x, then y coordinates.
		For example: (x=3,y=4) <= (x=4,y=3) because self.x is less than or equal to other.x.
		To compare in opposite order (i.e. compare y, then x), use L{yWiseLessOrEq}
		"""
		if not isinstance(other,POINT_CLASSES):
			try:
				other=toPoint(other)
			except ValueError:
				return False
		return (self.x, self.y) <= (other.x, other.y)

	def yWiseGreaterThan(self,other):
		"""
		Returns whether self is greater than other, first comparing y, then x coordinates.
		For example: (x=3,y=4) > (x=4,y=3) because self.y is greater than other.y.
		To compare in opposite order (i.e. compare x, then y), use L{xWiseGreaterThan}
		"""
		if not isinstance(other,POINT_CLASSES):
			try:
				other=toPoint(other)
			except ValueError:
				return False
		return (self.y, self.x) > (other.y, other.x)

	def xWiseGreaterThan(self,other):
		"""
		Returns whether self is greater than other, first comparing x, then y coordinates.
		For example: (x=4,y=3) > (x=3,y=4) because self.x is greater than other.x.
		To compare in opposite order (i.e. compare y, then x), use L{yWiseGreaterThan}
		"""
		if not isinstance(other,POINT_CLASSES):
			try:
				other=toPoint(other)
			except ValueError:
				return False
		return (self.x, self.y) > (other.x, other.y)

	def yWiseGreaterOrEq(self,other):
		"""
		Returns whether self is greater than or equal to other, first comparing y, then x coordinates.
		For example: (x=3,y=4) >= (x=4,y=3) because self.y is greater than or equal to other.y.
		To compare in opposite order (i.e. compare x, then y), use L{xWiseGreaterOrEq}
		"""
		if not isinstance(other,POINT_CLASSES):
			try:
				other=toPoint(other)
			except ValueError:
				return False
		return (self.y, self.x) >= (other.y, other.x)

	def xWiseGreaterOrEq(self,other):
		"""
		Returns whether self is greater than or equal to other, first comparing x, then y coordinates.
		For example: (x=4,y=3) >= (x=3,y=4) because self.x is greater than or equal to other.x.
		To compare in opposite order (i.e. compare y, then x), use L{yWiseGreaterOrEq}
		"""
		if not isinstance(other,POINT_CLASSES):
			try:
				other=toPoint(other)
			except ValueError:
				return False
		return (self.x, self.y) >= (other.x, other.y)

	def __eq__(self,other):
		if not isinstance(other,POINT_CLASSES):
			try:
				other=toPoint(other)
			except ValueError:
				return False
		return self.x == other.x and self.y == other.y

	def __ne__(self,other):
		if not isinstance(other,POINT_CLASSES):
			try:
				other=toPoint(other)
			except ValueError:
				return True
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
			try:
				other=toRectLTRB(other)
			except:
				return False
		return self.isSuperset(other) and self!=other

	def isSubset(self,other):
		"""Returns whether this rectangle is a subset of other (i.e. whether all points in this rectangle are contained by other)."""
		if not isinstance(other,RECT_CLASSES):
			try:
				other=toRectLTRB(other)
			except ValueError:
				return False
		return other.left<=self.left<=self.right<=other.right and other.top<=self.top<=self.bottom<=other.bottom

	def isSuperset(self,other):
		"""Returns whether this rectangle is a superset of other (i.e. whether all points of other are contained by this rectangle)."""
		if not isinstance(other,RECT_CLASSES):
			try:
				other=toRectLTRB(other)
			except ValueError:
				return False
		return self.left<=other.left<=other.right<=self.right and self.top<=other.top<=other.bottom<=self.bottom

	def __eq__(self,other):
		if not isinstance(other,RECT_CLASSES):
			try:
				other=toRectLTRB(other)
			except ValueError:
				return False
		return other.left == self.left and other.top == self.top and other.right == self.right and other.bottom == self.bottom

	def __ne__(self,other):
		if not isinstance(other,RECT_CLASSES):
			try:
				other=toRectLTRB(other)
			except ValueError:
				return True
		return other.left != self.left or other.top != self.top or other.right != self.right or other.bottom != self.bottom

	def intersection(self,other):
		"""Returns the intersection of self and other.
		For example, if self = Rect(left=10,top=10,right=25,bottom=25) and other = Rect(left=20,top=20,right=35,bottom=35),
		this results in Rect(left=20,top=20,right=25,bottom=25).
		No intersect results in a rectangle with zeroed coordinates.
		"""
		if not isinstance(other,RECT_CLASSES):
			try:
				other=toRectLTRB(other)
			except ValueError:
				return NotImplemented
		left=max(self.left,other.left)
		top=max(self.top,other.top)
		right=min(self.right,other.right)
		bottom=min(self.bottom,other.bottom)
		if left>right or top>bottom:
			left=top=right=bottom=0
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
			raise ValueError("left=%d is greather than right=%d, which is not allowed"%(left,right))
		if top>bottom:
			raise ValueError("top=%d is greather than bottom=%d, which is not allowed"%(top,bottom))
		return super(RectLTRB, cls).__new__(cls, left, top, right, bottom)

	@property
	def width(self):
		return self.right-self.left

	@property
	def height(self):
		return self.bottom-self.top

	def toLTWH(self):
		return RectLTWH(self.left,self.top,self.width,self.height)

def toRectLTRB(*params):
	"""
	Converts the given input to L{RectLTRB}.
	Input should be one of the following types:
		* One of l{RECT_CLASSES}.
		* One of L{POINT_CLASSES}: converted to L{Rect} square of one pixel.
		* List or tuple of integers: 4 treated as L{RectLTRB}, 2 treated as L{Point}.
		* List or tuple of mixed types from L{RECT_CLASSES} or L{POINT_CLASSES}: converted to L{RectLTRB} containing all input.
	"""
	if len(params)==0:
		raise TypeError("This function takes at least 1 argument (0 given)")
	if len(params)==1:
		param=params[0]
		if isinstance(param,RectLTRB):
			return param
		if isinstance(param,RECT_CLASSES):
			return RectLTRB(param.left,param.top,param.right,param.bottom)
		if isinstance(param,POINT_CLASSES):
			# Right and bottom edges of the resulting rectangle are considered exclusive
			x,y=point.x,point.y
			return RectLTRB(x,y,x+1,y+1)
		if isinstance(param,(tuple,list)):
			# One indexable in another indexable doesn't make sence, so treat the inner indexable as outer indexable
			params=param
	if all(isinstance(param,(int,long)) for param in params):
		if len(params)==4:
			# Assume that we are converting from a tuple rectangle (RectLTRB).
			# To convert from a tuple location (RectLTWH), use L{toRectLTWH} instead.
			# To convert from a tuple rectangle to L{RectLTWH}, use this function and execute L{toLTWH} on the resulting object.
			return RectLTRB(*params)
		elif len(params)==2:
			x,y=params
			return RectLTRB(x,y,x+1,y+1)
		elif len(params) in (1,3) or len(params)>4:
			raise ValueError("When providing integers, this function requires either 2 or 4 arguments (%d given)"%len(params))
	xs=[]
	ys=[]
	for param in params:
		if isinstance(param,RECT_CLASSES):
			xs.extend((param.left,param.right))
			ys.extend((param.top,param.bottom))
		elif isinstance(param,POINT_CLASSES):
			xs.append(param.x)
			ys.append(param.y)
		else:
			raise ValueError("Unexpected parameter %s"%str(param))
	left=min(xs)
	top=min(ys)
	right=max(xs)
	bottom=max(ys)
	return RectLTRB(left,top,right,bottom)

def toRectLTWH(*params):
	"""
	Converts the given input to L{RectLTWH}.
	Input should be one of the following types:
		* One of l{RECT_CLASSES}.
		* One of L{POINT_CLASSES}: converted to L{RectLTWH} square of one pixel.
		* List or tuple of integers: 4 treated as L{RectLTWH}, 2 treated as L{Point}.
		* List or tuple of mixed types from L{RECT_CLASSES} or L{POINT_CLASSES}: converted to L{RectLTWH} containing all input.
	"""
	if len(params)==0:
		raise TypeError("This function takes at least 1 argument (0 given)")
	if len(params)==1:
		param=params[0]
		if isinstance(param,RectLTWH):
			return param
		if not isinstance(param,RECT_CLASSES+POINT_CLASSES) and isinstance(param,(tuple,list)):
			# One indexable in another indexable doesn't make sence, so treat the inner indexable as outer indexable
			params=param
	if len(params)==4 and all(isinstance(param,(int,long)) for param in params):
		# Assume that we are converting from a tuple location (RectLTWH).
		# To convert from a tuple rectangle (RectLTRB), use L{toRectLTRB} instead.
		# To convert from a tuple location to L{RectLTRB}, use this function and execute L{toLTRB} on the resulting object.
		return RectLTWH(*params)
	return toRectLTRB(*params).toLTWH()

def toPoint(*params):
	"""
	Converts the given input to L{Point}.
	Input should either be one of L{POINT_CLASSES}, 2 integers or one double word.
	"""
	if not len(params) in (1,2):
		raise TypeError("This function takes 1 or 2 arguments (%d given)"%len(params))
	if len(params)==1:
		param=params[0]
		if isinstance(param,Point):
			return param
		if isinstance(param,POINT_CLASSES):
			return Point(param.x,param.y)
		if isinstance(param,(int,long)):
			return Point(winUser.GET_X_LPARAM(param),winUser.GET_Y_LPARAM(param))
	if all(isinstance(param,(int,long)) for param in params) and len(params)==2:
		return Point(*params)
	raise ValueError("Unexpected parameter(s) %s"%params)

#: Classes which support conversion to locationHelper Points using their x and y properties.
#: type: tuple
POINT_CLASSES=(Point, POINT, textInfos.Point, wx.Point)
#: Classes which support conversion to locationHelper RectLTRB/LTWH using their left, top, right and bottom properties.
#: type: tuple
RECT_CLASSES=(RectLTRB, RectLTWH, RECT, SMALL_RECT, textInfos.Rect)
