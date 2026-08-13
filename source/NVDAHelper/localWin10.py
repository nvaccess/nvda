# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2017-2026 NV Access Limited, Cary-rowen
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Functions exported by nvdaHelperLocalWin10.dll, and supporting definitions."""

from ctypes import CFUNCTYPE, POINTER, c_bool, c_int, c_uint, c_void_p, c_wchar_p, windll
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

_wgcCapture_isSupported = dll.wgcCapture_isSupported
"""
Check whether Windows Graphics Capture is available.

.. seealso::
	``nvdaHelper/localWin10/wgcCapture.h``
"""
_wgcCapture_isSupported.argtypes = ()
_wgcCapture_isSupported.restype = c_bool

_wgcCapture_captureScreenRegion = dll.wgcCapture_captureScreenRegion
"""
Capture a virtual-screen region using Windows Graphics Capture.

.. seealso::
	``nvdaHelper/localWin10/wgcCapture.h``
"""
_wgcCapture_captureScreenRegion.argtypes = (
	c_int,  # screenX
	c_int,  # screenY
	c_uint,  # width
	c_uint,  # height
	POINTER(RGBQUAD),  # image
	c_uint,  # destinationWidth
	c_uint,  # destinationHeight
)
_wgcCapture_captureScreenRegion.restype = c_bool
