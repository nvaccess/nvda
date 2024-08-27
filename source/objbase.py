# objbase.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from ctypes import *  # noqa: F403
import objidl


def GetRunningObjectTable():
	rot = POINTER(objidl.IRunningObjectTable)()  # noqa: F405
	oledll.ole32.GetRunningObjectTable(0, byref(rot))  # noqa: F405
	return rot


def CreateBindCtx():
	bctx = POINTER(objidl.IBindCtx)()  # noqa: F405
	oledll.ole32.CreateBindCtx(0, byref(bctx))  # noqa: F405
	return bctx
