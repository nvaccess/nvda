# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2013-2026 NV Access Limited, Bill Dengler, Christopher Proß
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
Utilities for working with windows (HWNDs).

When working on this file, consider moving to winAPI.
"""

import contextlib
import ctypes
import ctypes.wintypes
import weakref
import winBindings.kernel32
import winBindings.user32
import winBindings.gdi32
import winUser
from winBindings.user32 import WNDCLASSEXW, WNDPROC
from logHandler import log
from abc import abstractmethod
from baseObject import AutoPropertyObject
from collections.abc import Iterator
from typing import Optional, TYPE_CHECKING
from winBindings import user32

if TYPE_CHECKING:
	# locationHelper imports this module, so importing it at runtime would create an import cycle
	# and would pull wx into every importer of this low level module.
	import locationHelper


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

	user32.EnumChildWindows(parent, callback, 0)
	try:
		return result[0]
	except IndexError:
		raise LookupError("No matching descendant window found")


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
	point = ctypes.wintypes.POINT(x, y)
	user32.LogicalToPhysicalPointForPerMonitorDPI(window, ctypes.byref(point))
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
	point = ctypes.wintypes.POINT(x, y)
	user32.PhysicalToLogicalPointForPerMonitorDPI(window, ctypes.byref(point))
	return point.x, point.y


DPI_AWARENESS_CONTEXT_UNAWARE = -1
"""The predefined DPI_AWARENESS_CONTEXT handle value for DPI unaware behavior."""


@contextlib.contextmanager
def _threadDpiAwarenessContext(dpiContext: int) -> Iterator[None]:
	"""Temporarily switch the current thread's DPI awareness context.

	:param dpiContext: The DPI_AWARENESS_CONTEXT handle value to apply.
	:raise OSError: If the context cannot be applied.
	"""
	previousContext = user32.SetThreadDpiAwarenessContext(dpiContext)
	if not previousContext:
		raise OSError(f"Could not set the thread DPI awareness context {dpiContext}")
	try:
		yield
	finally:
		user32.SetThreadDpiAwarenessContext(previousContext)


@contextlib.contextmanager
def threadDpiAwarenessContextOfWindow(window: int) -> Iterator[None]:
	"""Temporarily switch the current thread's DPI awareness context to that of the given window.

	Coordinate queries made inside this context return values
	as the given window sees them,
	which for a DPI virtualized window is its virtualized coordinate space.

	:param window: The window handle.
	:raise OSError: If the window's DPI awareness context cannot be applied,
		for example because the window handle is no longer valid.
	"""
	with _threadDpiAwarenessContext(user32.GetWindowDpiAwarenessContext(window)):
		yield


def _fetchWindowRect(window: int) -> "locationHelper.RectLTRB":
	"""Fetch a window's bounding rectangle in the current thread's DPI awareness context.

	:param window: The window handle.
	:return: The window rectangle.
	:raise OSError: If the rectangle cannot be fetched.
	"""
	import locationHelper

	rect = ctypes.wintypes.RECT()
	if not user32.GetWindowRect(window, ctypes.byref(rect)):
		raise ctypes.WinError()
	return locationHelper.RectLTRB.fromCompatibleType(rect)


def getPhysicalWindowRect(window: int) -> "locationHelper.RectLTRB":
	"""Fetch a window's bounding rectangle in physical screen coordinates.

	NVDA is per monitor DPI aware, so its own view of screen coordinates is physical.

	:param window: The window handle.
	:return: The window rectangle in physical screen coordinates.
	:raise OSError: If the rectangle cannot be fetched.
	"""
	return _fetchWindowRect(window)


def getWindowRectInWindowDpiContext(window: int) -> "locationHelper.RectLTRB":
	"""Fetch a window's bounding rectangle as seen from the window's own DPI awareness context.

	For a window whose coordinates are DPI virtualized by the system,
	this returns the virtualized rectangle,
	while a plain ``GetWindowRect`` call from NVDA returns the physical rectangle.
	Comparing and combining both rectangles allows converting between the two coordinate spaces
	without relying on ``PhysicalToLogicalPointForPerMonitorDPI``,
	which fails for points outside the physical window rectangle.

	:param window: The window handle.
	:return: The window rectangle in the coordinate space of the window's own DPI awareness context.
	:raise OSError: If the DPI awareness context cannot be applied or the rectangle cannot be fetched.
	"""
	with threadDpiAwarenessContextOfWindow(window):
		return _fetchWindowRect(window)


def getWindowRectInUnawareDpiContext(window: int) -> "locationHelper.RectLTRB":
	"""Fetch a window's bounding rectangle as seen by a DPI unaware process.

	This is the 96 DPI based view the system presents to DPI unaware callers.
	It applies to any window, including DPI aware ones,
	and anchors conversions from 96 DPI based coordinate spaces to physical coordinates.

	:param window: The window handle.
	:return: The window rectangle in the 96 DPI based coordinate space.
	:raise OSError: If the DPI awareness context cannot be applied or the rectangle cannot be fetched.
	"""
	with _threadDpiAwarenessContext(DPI_AWARENESS_CONTEXT_UNAWARE):
		return _fetchWindowRect(window)


DEFAULT_DPI_LEVEL = 96
# The constant (defined in winGdi.h) to get the number of logical pixels per inch on the x axis
# via the GetDeviceCaps function.
LOGPIXELSX = 88


def getWindowScalingFactor(window: int) -> int:
	"""Gets the logical scaling factor used for the given window handle. This is based off the Dpi reported by windows
	for the given window handle / divided by the "base" DPI level of 96. Typically this is a result of using the scaling
	percentage in the windows display settings. 100% is typically 96 DPI, 150% is typically 144 DPI.
	@param window: a native Windows window handle (hWnd)
	@returns the logical scaling factor. EG. 1.0 if the window DPI level is 96, 1.5 if the window DPI level is 144"""
	try:
		winDpi: int = user32.GetDpiForWindow(window)
	except:  # noqa: E722
		log.debug("GetDpiForWindow failed, using GetDeviceCaps instead")
		dc = user32.GetDC(window)
		winDpi: int = winBindings.gdi32.GetDeviceCaps(dc, LOGPIXELSX)
		ret = user32.ReleaseDC(window, dc)
		if ret != 1:
			log.error("Unable to release the device context.")

	# For GetDpiForWindow: an invalid hwnd value will result in a return value of 0.
	# There is little information about what GetDeviceCaps does in the case of a failure for LOGPIXELSX, however,
	# a value of zero is certainly an error.
	if winDpi <= 0:
		log.debugWarning(
			"Failed to get the DPI for the window, assuming a "
			"DPI of {} and using a scaling of 1. The hWnd value "
			"used was: {}".format(DEFAULT_DPI_LEVEL, window),
		)
		return 1

	return round(winDpi / DEFAULT_DPI_LEVEL)


appInstance = winBindings.kernel32.GetModuleHandle(None)


class CustomWindow(AutoPropertyObject):
	"""Base class to enable simple implementation of custom windows.
	Subclasses need only set L{className} and implement L{windowProc}.
	Simply create an instance to create the window.
	The window will be destroyed when the instance is deleted,
	but it can be explicitly destroyed using L{destroy}.
	"""

	handle: Optional[int] = None

	@classmethod
	def __new__(cls, *args, **kwargs):
		for instance in cls._hwndsToInstances.values():
			if type(instance) is cls:
				raise RuntimeError(f"Only one instance of {cls.__qualname__} may exist at a time")
		return super().__new__(cls, *args, **kwargs)

	_wClass: WNDCLASSEXW

	@classmethod
	def _get__wClass(cls):
		return WNDCLASSEXW(
			cbSize=ctypes.sizeof(WNDCLASSEXW),
			lpfnWndProc=cls._rawWindowProc,
			hInstance=appInstance,
			lpszClassName=cls.className,
		)

	_abstract_className = True

	className: str

	@classmethod
	def _get_className(cls) -> str:
		"""The class name of this window."""
		return None

	_hwndsToInstances = weakref.WeakValueDictionary()

	def __init__(
		self,
		windowName: Optional[str] = None,
		windowStyle: int = 0,
		extendedWindowStyle: int = 0,
		parent: Optional[int] = None,
	):
		"""Constructor.
		@param windowName: The name of the window.
		@param windowStyle: The style of the window.
			This is a combination of the C{winUser.WS_*} constants.
		@param extendedWindowStyle: The extended style of the window.
			This is a combination of the C{winUser.WS_EX_*} constants.
		@param parent: The handle of the parent window, if any.
		@raise WindowsError: If an error occurs.
		"""
		if not isinstance(self.className, str):
			raise TypeError("className attribute must be a unicode string")
		if windowName is not None and not isinstance(windowName, str):
			raise TypeError("windowName must be a unicode string")
		if not isinstance(windowStyle, int):
			raise TypeError("windowStyle must be an integer")
		if not isinstance(extendedWindowStyle, int):
			raise TypeError("extendedWindowStyle must be an integer")
		if parent and not isinstance(parent, int):
			raise TypeError("parent must be an integer")
		res = self._classAtom = winBindings.user32.RegisterClassEx(ctypes.byref(self._wClass))
		if res == 0:
			raise ctypes.WinError()
		res = winBindings.user32.CreateWindowEx(
			extendedWindowStyle,
			# The class atom should be stored as the low word of the class name string pointer.
			ctypes.cast(ctypes.c_void_p(self._classAtom), ctypes.wintypes.LPCWSTR),
			windowName or self.className,
			windowStyle,
			0,
			0,
			0,
			0,
			parent,
			None,
			appInstance,
			None,
		)
		if res == 0:
			raise ctypes.WinError()
		#: The handle to the created window.
		self.handle: int = res
		self._hwndsToInstances[res] = self

	def destroy(self):
		"""Destroy the window.
		This will be called automatically when this instance is deleted,
		but you may wish to call it earlier.
		"""
		if not user32.DestroyWindow(self.handle):
			log.error(
				f"Error destroying window for {self.__class__.__qualname__}",
				exc_info=ctypes.WinError(),
			)
		self.handle = None
		if not winBindings.user32.UnregisterClass(
			# The class atom should be stored as the low word of the class name string pointer.
			ctypes.cast(ctypes.c_void_p(self._classAtom), ctypes.wintypes.LPCWSTR),
			appInstance,
		):
			log.error(
				f"Error unregistering window class for {self.__class__.__qualname__}",
				exc_info=ctypes.WinError(),
			)
		self._classAtom = None

	def __del__(self):
		if getattr(self, "handle", None):
			self.destroy()

	@abstractmethod
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
		return None

	@staticmethod
	@WNDPROC
	def _rawWindowProc(hwnd, msg, wParam, lParam):
		try:
			inst = CustomWindow._hwndsToInstances[hwnd]
		except KeyError:
			log.debug("CustomWindow rawWindowProc called for unknown window %d" % hwnd)
			return user32.DefWindowProc(hwnd, msg, wParam, lParam)
		try:
			res = inst.windowProc(hwnd, msg, wParam, lParam)
			if res is not None:
				return res
		except:  # noqa: E722
			log.exception("Error in wndProc")
		return user32.DefWindowProc(hwnd, msg, wParam, lParam)
