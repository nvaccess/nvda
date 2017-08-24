#locationHelper.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017 NV Access Limited, Babbage B.V.

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
		if not isinstance(other,_POINT_CLASSES):
			return NotImplemented
		return Point((self.x+other.x),(self.y+other.y))

	def __radd__(self,other):
		return self.__add__(other)

	def __lt__(self, other):
		"""
		Returns whether self is less than other.
		This first compares y, than x coordinates.
		For example: (x=4,y=3) < (x=3,y=4) because self.y is less than other.y.
		To compare in opposite order (i.e. compare x, than y), use tuple(self) < tuple(other)
		"""
		if not isinstance(other,_POINT_CLASSES):
			try:
				other=toPoint(other)
			except ValueError:
				return False
		return (self.y, self.x) < (other.y, other.x)

	def __le__(self, other):
		"""
		Returns whether self is less than or equal to other.
		This first compares y, than x coordinates.
		For example: (x=4,y=3) < (x=3,y=4) because self.y is less than other.y.
		To compare in opposite order (i.e. compare x, than y), use tuple(self) <= tuple(other)
		"""
		if not isinstance(other,_POINT_CLASSES):
			try:
				other=toPoint(other)
			except ValueError:
				return False
		return (self.y, self.x) <= (other.y, other.x)

	def __gt__(self, other):
		"""
		Returns whether self is greater than other.
		This first compares y, than x coordinates.
		For example: (x=3,y=4) > (x=4,y=3) because self.y is greater than other.y.
		To compare in opposite order (i.e. compare x, than y), use tuple(self) > tuple(other)
		"""
		if not isinstance(other,_POINT_CLASSES):
			try:
				other=toPoint(other)
			except ValueError:
				return False
		return (self.y, self.x) > (other.y, other.x)

	def __ge__(self, other):
		"""
		Returns whether self is greater than or equal to other.
		This first compares y, than x coordinates.
		For example: (x=3,y=4) > (x=4,y=3) because self.y is greater than other.y.
		To compare in opposite order (i.e. compare x, than y), use tuple(self) >= tuple(other)
		"""
		if not isinstance(other,_POINT_CLASSES):
			try:
				other=toPoint(other)
			except ValueError:
				return False
		return (self.y, self.x) >= (other.y, other.x)

	def __eq__(self, other):
		if not isinstance(other,_POINT_CLASSES):
			try:
				other=toPoint(other)
			except ValueError:
				return False
		return self.x==other.x and self.y==other.y

	def __neq__(self, other):
		if not isinstance(other,_POINT_CLASSES):
			try:
				other=toPoint(other)
			except ValueError:
				return False
		return self.x!=self.x or self.y!=other.y

	def __sub__(self,other):
		if not isinstance(other,_POINT_CLASSES):
			return NotImplemented
		return Point((self.x-other.x),(self.y-other.y))

	def __rsub__(self,other):
		return self.__sub__(other)

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
	"""Mix-in class for properties shared between Location and Rect classes"""

	def toRECT(self):
		"""Converts self to a L{ctypes.wintypes.RECT}"""
		return RECT(self.left,self.top,self.right,self.bottom)

	def toLogical(self, hwnd):
		left,top=self.topLeft.toLogical(hwnd)
		right,bottom=self.bottomRight.toLogical(hwnd)
		if type(self) is Location:
			return Location(left,top,right-left,bottom-top)
		return Rect(left,top,right,bottom)

	def toPhysical(self, hwnd):
		left,top=self.topLeft.toPhysical(hwnd)
		right,bottom=self.bottomRight.toPhysical(hwnd)
		if type(self) is Location:
			return Location(left,top,right-left,bottom-top)
		return Rect(left,top,right,bottom)

	def toClient(self, hwnd):
		left, top =self.topLeft.toClient(hwnd)
		if type(self) is Location:
			return Location(left, top, self.width, self.height)
		return Rect(left, top, left+self.width, top+self.height)

	def toScreen(self, hwnd):
		left,top=self.topLeft.toScreen(hwnd)
		if type(self) is Location:
			return Location(left, top, self.width, self.height)
		return Rect(left, top, left+self.width, top+self.height)

	@property
	def topLeft(self):
		return Point(self.left,self.top)

	@property
	def bottomRight(self):
		return Point(self.right,self.bottom)

	@property
	def center(self):
		return Point((self.left+self.right)/2, (self.top+self.bottom)/2)

	def __contains__(self,other):
		"""Returns whether other is a part of self."""
		if isinstance(other,_POINT_CLASSES):
			return other.x >= self.left < self.right and other.y >= self.top < self.bottom
		if isinstance(other,_RECT_CLASSES):
			return self>other
		try:
			other=toRect(other)
		except:
			return False
		return self>other

	def __lt__(self, other):
		"""Returns whether self is a subset of other (i.e. whether all points in self are contained by other)."""
		if not isinstance(other,_RECT_CLASSES):
			try:
				other=toRect(other)
			except ValueError:
				return False
		return self<=other and self!=other

	def __le__(self, other):
		"""Returns whether self is a subset of or equal to other."""
		if not isinstance(other,_RECT_CLASSES):
			try:
				other=toRect(other)
			except ValueError:
				return False
		return self.left >= other.left and self.top >= other.top and self.right <= other.right and self.bottom <= other.bottom

	def __gt__(self, other):
		"""Returns whether self is a superset of other (i.e. whether all points of other are contained by self)."""
		if not isinstance(other,_RECT_CLASSES):
			try:
				other=toRect(other)
			except ValueError:
				return False
		return self>=other and self!=other

	def __ge__(self, other):
		"""Returns whether self is a superset of or equal to other."""
		if not isinstance(other,_RECT_CLASSES):
			try:
				other=toRect(other)
			except ValueError:
				return False
		return other.left >= self.left and other.top >= self.top and other.right <= self.right and other.bottom <= self.bottom

	def __eq__(self, other):
		if not isinstance(other,_RECT_CLASSES):
			try:
				other=toRect(other)
			except ValueError:
				return False
		return other.left == self.left and other.top == self.top and other.right == self.right and other.bottom == self.bottom

	def __neq__(self, other):
		if not isinstance(other,_RECT_CLASSES):
			try:
				other=toRect(other)
			except ValueError:
				return False
		return not (other.left == self.left and other.top == self.top and other.right == self.right and other.bottom == self.bottom)

	def __sub__(self,other):
		if not isinstance(other,_RECT_CLASSES):
			return NotImplemented
		left,top,right,bottom=self.left-other.left,self.top-other.top,self.right-other.right,self.bottom-other.bottom
		if type(self) is Location:
			return Location(left,top,right-left,bottom-top)
		return Rect(left,top,right,bottom)

	def __rsub__(self,other):
		return self.__sub__(other)

	def __and__(self,other):
		"""Returns the intersection of self and other.
		For example, if self = Rect(left=10,top=10,right=25,bottom=25) and other = Rect(left=20,top=20,right=35,bottom=35),
		this results in Rect(left=20,top=20,right=25,bottom=25).
		No intersect results in a rectangle with zeroed coordinates.
		"""
		if not isinstance(other,_RECT_CLASSES):
			try:
				other=toRect(other)
			except ValueError:
				return NotImplemented
		left=max(self.left,other.left)
		top=max(self.top,other.top)
		right=min(self.right,other.right)
		bottom=min(self.bottom,other.bottom)
		if left>right or top>bottom:
			left=top=right=bottom=0
		if type(self) is Location:
			return Location(left,top,right-left,bottom-top)
		return Rect(left,top,right,bottom)

	def __rand__(self,other):
		return self.__and__(other)

class Location(_RectMixin, namedtuple("Location",("left","top","width","height"))):
	"""Represents a rectangle on the screen, based on left and top coordinates, width and height."""

	@property
	def right(self):
		return self.left+self.width

	@property
	def bottom(self):
		return self.top+self.height

	def toRect(self):
		return Rect(self.left,self.top,self.right,self.bottom)

class Rect(_RectMixin, namedtuple("Rect",("left","top","right","bottom"))):
	"""Represents a rectangle on the screen.
	By convention, the right and bottom edges of the rectangle are normally considered exclusive.
	"""

	@property
	def width(self):
		return self.right-self.left

	@property
	def height(self):
		return self.bottom-self.top

	def toLocation(self):
		return Location(self.left,self.top,self.width,self.height)

def toRect(*params):
	"""
	Converts the given input to L{Rect}.
	Input should be one of the following types:
		* One of l{_RECT_CLASSES}.
		* One of L{_POINT_CLASSES}: converted to L{Rect} square of one pixel.
		* List or tuple of integers: 4 treated as L{Rect}, 2 treated as L{Point}.
		* List or tuple of mixed types from L{_RECT_CLASSES} or L{_POINT_CLASSES}: converted to L{Rect} containing all input.
	"""
	if len(params)==0:
		raise TypeError("This function takes at least 1 argument (0 given)")
	if len(params)==1:
		param=params[0]
		if isinstance(param,Rect):
			return param
		if isinstance(param,_RECT_CLASSES):
			return Rect(param.left,param.top,param.right,param.bottom)
		if isinstance(param,_POINT_CLASSES):
			# Right and bottom edges of the resulting rectangle are considered exclusive
			x,y=point.x,point.y
			return Rect(x,y,x+1,y+1)
		if isinstance(param,(tuple,list)):
			# One indexable in another indexable doesn't make sence, so treat the inner indexable as outer indexable
			params=param
	if all(isinstance(param,(int,long)) for param in params):
		if len(params)==4:
			# Assume that we are converting from a tuple rectangle.
			# To convert from a tuple location, use L{toLocation} instead.
			# To convert from a tuple rectangle to L{Location}, use this function and execute L{toLocation} on the resulting object.
			return Rect(*params)
		elif len(params)==2:
			x,y=params
			return Rect(x,y,x+1,y+1)
		elif len(params) in (1,3) or len(params)>4:
			raise ValueError("When providing integers, this function requires either 2 or 4 arguments (%d given)"%len(params))
	xs=[]
	ys=[]
	for param in params:
		if isinstance(param,_RECT_CLASSES):
			xs.extend((param.left,param.right))
			ys.extend((param.top,param.bottom))
		elif isinstance(param,_POINT_CLASSES):
			xs.append(param.x)
			ys.append(param.y)
		else:
			raise ValueError("Unexpected parameter %s"%str(param))
	left=min(xs)
	top=min(ys)
	right=max(xs)
	bottom=max(ys)
	return Rect(left,top,right,bottom)

def toLocation(*params):
	"""
	Converts the given input to L{Location}.
	Input should be one of the following types:
		* One of l{_RECT_CLASSES}.
		* One of L{_POINT_CLASSES}: converted to L{Location} square of one pixel.
		* List or tuple of integers: 4 treated as L{Rect}, 2 treated as L{Point}.
		* List or tuple of mixed types from L{_RECT_CLASSES} or L{_POINT_CLASSES}: converted to L{Location} containing all input.
	"""
	if len(params)==0:
		raise TypeError("This function takes at least 1 argument (0 given)")
	if len(params)==1:
		param=params[0]
		if isinstance(param,Location):
			return param
		if not isinstance(param,_RECT_CLASSES+_POINT_CLASSES) and isinstance(param,(tuple,list)):
			# One indexable in another indexable doesn't make sence, so treat the inner indexable as outer indexable
			params=param
	if len(params)==4 and all(isinstance(param,(int,long)) for param in params):
		# Assume that we are converting from a tuple location.
		# To convert from a tuple rectangle, use L{toRectangle} instead.
		# To convert from a tuple location to L{Rect}, use this function and execute L{toRect} on the resulting location.
		return Location(*params)
	return toRect(*params).toLocation()

def toPoint(*params):
	"""
	Converts the given input to L{Point}.
	Input should either be one of L{_POINT_CLASSES}, 2 integers or one double word.
	"""
	if not len(params) in (1,2):
		raise TypeError("This function takes 1 or 2 arguments (%d given)"%len(params))
	if len(params)==1:
		param=params[0]
		if isinstance(param,Point):
			return param
		if isinstance(param,_POINT_CLASSES):
			return Point(param.x,param.y)
		if isinstance(param,(int,long)):
			return Point(winUser.GET_X_LPARAM(param),winUser.GET_Y_LPARAM(param))
	if all(isinstance(param,(int,long)) for param in params) and len(params)==2:
		return Point(*params)
	raise ValueError("Unexpected parameter(s) %s"%params)

#: Classes which support conversion to locationHelper Points using their x and y properties.
#: type: tuple
_POINT_CLASSES=(Point, POINT, textInfos.Point, wx.Point)
#: Classes which support conversion to locationHelper Rects and Locations using their left, top, right and bottom properties.
#: type: tuple
_RECT_CLASSES=(Rect, Location, RECT, SMALL_RECT, textInfos.Rect, wx.Rect)
