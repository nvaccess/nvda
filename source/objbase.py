# objbase.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from ctypes import *  # noqa: F403
from ctypes import byref
import objidl
import winBindings.ole32


def GetRunningObjectTable():
	rot = POINTER(objidl.IRunningObjectTable)()  # noqa: F405
	winBindings.ole32.GetRunningObjectTable(0, byref(rot))
	return rot


def CreateBindCtx():
	bctx = POINTER(objidl.IBindCtx)()  # noqa: F405
	winBindings.ole32.CreateBindCtx(0, byref(bctx))
	return bctx
