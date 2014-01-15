#windowUtils.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2013 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Utilities for working with windows (HWNDs).
"""

import ctypes
import winUser

WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.wintypes.BOOL, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
def findDescendantWindow(parent, visible=None, controlID=None, className=None):
	"""Find a descendant window matching specified criteria.
	@param parent: The handle of the parent window to search within.
	@type parent: int
	@param visible: Whether the window should be visible or C{None} if irrelevant.
	@type visible: bool
	@param controlID: The control ID of the window or C{None} if irrelevant.
	@type controlID: int
	@param className: The class name of the window or C{None} if irrelevant.
	@type className: basestring
	@return: The handle of the matching descendant window.
	@rtype: int
	@raise LookupError: if no matching window is found.
	"""
	# We need something mutable to store the result from the callback.
	result = []
	@WNDENUMPROC
	def callback(window, data):
		if (
			(visible is None or winUser.isWindowVisible(window) == visible)
			and (not controlID or winUser.getControlID(window) == controlID)
			and (not className or winUser.getClassName(window) == className)
		):
			result.append(window)
			return False
		return True
	ctypes.windll.user32.EnumChildWindows(parent, callback, 0)
	try:
		return result[0]
	except IndexError:
		raise LookupError("No matching descendant window found")

try:
	# Windows >= 8.1
	_logicalToPhysicalPoint = ctypes.windll.user32.LogicalToPhysicalPointForPerMonitorDPI
	_physicalToLogicalPoint = ctypes.windll.user32.PhysicalToLogicalPointForPerMonitorDPI
except AttributeError:
	try:
		# Windows Vista..Windows 8
		_logicalToPhysicalPoint = ctypes.windll.user32.LogicalToPhysicalPoint
		_physicalToLogicalPoint = ctypes.windll.user32.PhysicalToLogicalPoint
	except AttributeError:
		# Windows <= XP
		_logicalToPhysicalPoint = None
		_physicalToLogicalPoint = None

def logicalToPhysicalPoint(window, x, y):
	"""Converts the logical coordinates of a point in a window to physical coordinates.
	This should be used when points are received directly from a window that is not DPI aware.
	@param window: The window handle.
	@param x: The logical x coordinate.
	@type x: int
	@param y: The logical y coordinate.
	@type y: int
	@return: The physical x and y coordinates.
	@rtype: tuple of (int, int)
	"""
	if not _logicalToPhysicalPoint:
		return x, y
	point = ctypes.wintypes.POINT(x, y)
	_logicalToPhysicalPoint(window, ctypes.byref(point))
	return point.x, point.y

def physicalToLogicalPoint(window, x, y):
	"""Converts the physical coordinates of a point in a window to logical coordinates.
	This should be used when sending points directly to a window that is not DPI aware.
	@param window: The window handle.
	@param x: The physical x coordinate.
	@type x: int
	@param y: The physical y coordinate.
	@type y: int
	@return: The logical x and y coordinates.
	@rtype: tuple of (int, int)
	"""
	if not _physicalToLogicalPoint:
		return x, y
	point = ctypes.wintypes.POINT(x, y)
	_physicalToLogicalPoint(window, ctypes.byref(point))
	return point.x, point.y
