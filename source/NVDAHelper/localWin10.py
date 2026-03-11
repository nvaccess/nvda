# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2017-2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Functions exported by nvdaHelperLocalWin10.dll, and supporting definitions."""

from ctypes import CFUNCTYPE, POINTER, c_bool, c_uint, c_void_p, c_wchar_p, windll
from ctypes.wintypes import HWND
from comtypes import BSTR

import NVDAState
from winBindings.gdi32 import RGBQUAD

dll = windll.LoadLibrary(NVDAState.ReadPaths.nvdaHelperLocalWin10Dll)

UwpOcr_P = c_void_p
"""Pointer to an UwpOcr object."""

uwpOcr_getLanguages = dll.uwpOcr_getLanguages
"""
Get supported language codes separated by semicolons.

.. seealso::
	``nvdaHelper/localWin10/uwpOcr.h``
"""
uwpOcr_getLanguages.argtypes = ()
uwpOcr_getLanguages.restype = BSTR

uwpOcr_Callback = CFUNCTYPE(None, c_wchar_p)
"""Function called when recognition is complete."""

uwpOcr_initialize = dll.uwpOcr_initialize
"""
Initialise a UWP OCR instance.

.. seealso::
	``nvdaHelper/localWin10/uwpOcr.h``
"""
uwpOcr_initialize.argtypes = (
	c_wchar_p,  # language
	uwpOcr_Callback,  # callback
)
uwpOcr_initialize.restype = UwpOcr_P

uwpOcr_terminate = dll.uwpOcr_terminate
"""
Terminate a UWP OCR instance.

.. seealso::
	``nvdaHelper/localWin10/uwpOcr.h``
"""
uwpOcr_terminate.argtypes = (
	UwpOcr_P,  # instance
)
uwpOcr_terminate.restype = None

uwpOcr_recognize = dll.uwpOcr_recognize
"""
Recognise text in an image.

.. seealso::
	``nvdaHelper/localWin10/uwpOcr.h``
"""
uwpOcr_recognize.argtypes = (
	UwpOcr_P,  # instance
	POINTER(RGBQUAD),  # image
	c_uint,  # width
	c_uint,  # height
)
uwpOcr_recognize.restype = None

# --- Windows Graphics Capture functions ---

WgcCapture_H = c_void_p
"""Opaque handle to a WgcCapture instance."""

wgcCapture_Callback = CFUNCTYPE(None, c_wchar_p)
"""Function called when WGC recognition is complete."""

wgcCapture_isSupported = dll.wgcCapture_isSupported
"""
Check whether Windows.Graphics.Capture is available (Win10 1903+).

.. seealso::
	``nvdaHelper/localWin10/wgcCapture.h``
"""
wgcCapture_isSupported.argtypes = ()
wgcCapture_isSupported.restype = c_bool

wgcCapture_initialize = dll.wgcCapture_initialize
"""
Initialise a WGC capture and OCR instance.

.. seealso::
	``nvdaHelper/localWin10/wgcCapture.h``
"""
wgcCapture_initialize.argtypes = (
	c_wchar_p,  # language
	wgcCapture_Callback,  # callback
)
wgcCapture_initialize.restype = WgcCapture_H

wgcCapture_recognizeWindow = dll.wgcCapture_recognizeWindow
"""
Capture an entire window by HWND and run OCR asynchronously.

.. seealso::
	``nvdaHelper/localWin10/wgcCapture.h``
"""
wgcCapture_recognizeWindow.argtypes = (
	WgcCapture_H,  # handle
	HWND,  # hwnd
)
wgcCapture_recognizeWindow.restype = None

wgcCapture_recognizeWindowRegion = dll.wgcCapture_recognizeWindowRegion
"""
Capture a sub-region of a window and run OCR asynchronously.

.. seealso::
	``nvdaHelper/localWin10/wgcCapture.h``
"""
wgcCapture_recognizeWindowRegion.argtypes = (
	WgcCapture_H,  # handle
	HWND,  # hwnd
	c_uint,  # x
	c_uint,  # y
	c_uint,  # width
	c_uint,  # height
)
wgcCapture_recognizeWindowRegion.restype = None

wgcCapture_terminate = dll.wgcCapture_terminate
"""
Terminate and free a WGC capture and OCR instance.

.. seealso::
	``nvdaHelper/localWin10/wgcCapture.h``
"""
wgcCapture_terminate.argtypes = (
	WgcCapture_H,  # handle
)
wgcCapture_terminate.restype = None
