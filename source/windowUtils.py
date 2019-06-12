#windowUtils.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2013 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Utilities for working with windows (HWNDs).
"""

import ctypes
import weakref
import winUser
from winUser import WNDCLASSEXW, WNDPROC, LRESULT
from logHandler import log

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
	@type className: str
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

DEFAULT_DPI_LEVEL = 96.0
# The constant (defined in winGdi.h) to get the number of logical pixels per inch on the x axis
# via the GetDeviceCaps function.
LOGPIXELSX = 88
def getWindowScalingFactor(window):
	"""Gets the logical scaling factor used for the given window handle. This is based off the Dpi reported by windows
	for the given window handle / divided by the "base" DPI level of 96. Typically this is a result of using the scaling
	percentage in the windows display settings. 100% is typically 96 DPI, 150% is typically 144 DPI.
	@param window: a native Windows window handle (hWnd)
	@returns the logical scaling factor. EG. 1.0 if the window DPI level is 96, 1.5 if the window DPI level is 144"""
	user32 = ctypes.windll.user32
	try:
		winDpi = user32.GetDpiForWindow(window)
	except:
		log.debug("GetDpiForWindow failed, using GetDeviceCaps instead")
		dc = user32.GetDC(window)
		winDpi = ctypes.windll.gdi32.GetDeviceCaps(dc, LOGPIXELSX)
		ret = user32.ReleaseDC(window, dc)
		if ret != 1:
			log.error("Unable to release the device context.")

	# For GetDpiForWindow: an invalid hwnd value will result in a return value of 0.
	# There is little information about what GetDeviceCaps does in the case of a failure for LOGPIXELSX, however,
	# a value of zero is certainly an error.
	if winDpi <= 0:
		log.debugWarning("Failed to get the DPI for the window, assuming a "
		                 "DPI of {} and using a scaling of 1.0. The hWnd value "
		                 "used was: {}".format(DEFAULT_DPI_LEVEL, window))
		return 1.0

	return winDpi / DEFAULT_DPI_LEVEL



appInstance = ctypes.windll.kernel32.GetModuleHandleW(None)
class CustomWindow(object):
	"""Base class to enable simple implementation of custom windows.
	Subclasses need only set L{className} and implement L{windowProc}.
	Simply create an instance to create the window.
	The window will be destroyed when the instance is deleted,
	but it can be explicitly destroyed using L{destroy}.
	"""

	#: The class name of this window.
	#: @type: str
	className = None

	_hwndsToInstances = weakref.WeakValueDictionary()

	def __init__(self, windowName=None):
		"""Constructor.
		@raise WindowsError: If an error occurs.
		"""
		if not isinstance(self.className, str):
			raise ValueError("className attribute must be a unicode string")
		if windowName and not isinstance(windowName, str):
			raise ValueError("windowName must be a unicode string")
		self._wClass = WNDCLASSEXW(
			cbSize=ctypes.sizeof(WNDCLASSEXW),
			lpfnWndProc = CustomWindow._rawWindowProc,
			hInstance = appInstance,
			lpszClassName = self.className,
		)
		res = self._classAtom = ctypes.windll.user32.RegisterClassExW(ctypes.byref(self._wClass))
		if res == 0:
			raise ctypes.WinError()
		res = ctypes.windll.user32.CreateWindowExW(0, self._classAtom, windowName or self.className, 0, 0, 0, 0, 0, None, None, appInstance, None)
		if res == 0:
			raise ctypes.WinError()
		#: The handle to the created window.
		#: @type: int
		self.handle = res
		self._hwndsToInstances[res] = self

	def destroy(self):
		"""Destroy the window.
		This will be called automatically when this instance is deleted,
		but you may wish to call it earlier.
		"""
		ctypes.windll.user32.DestroyWindow(self.handle)
		self.handle = None
		ctypes.windll.user32.UnregisterClassW(self._classAtom, appInstance)

	def __del__(self):
		if self.handle:
			self.destroy()

	def windowProc(self, hwnd, msg, wParam, lParam):
		"""Process messages sent to this window.
		@param hwnd: The handle to this window.
		@type hwnd: int
		@param msg: The message.
		@type msg: int
		@param wParam: Additional message information.
		@type wParam: int
		@param lParam: Additional message information.
		@type lParam: int
		@return: The result of the message processing
			or C{None} to call DefWindowProc.
		@rtype: int or None
		"""

	@WNDPROC
	def _rawWindowProc(hwnd, msg, wParam, lParam):
		try:
			inst = CustomWindow._hwndsToInstances[hwnd]
		except KeyError:
			return ctypes.windll.user32.DefWindowProcW(hwnd, msg, wParam, lParam)
		try:
			res = inst.windowProc(hwnd, msg, wParam, lParam)
			if res is not None:
				return res
		except:
			log.exception("Error in wndProc")
		return ctypes.windll.user32.DefWindowProcW(hwnd, msg, wParam, lParam)
