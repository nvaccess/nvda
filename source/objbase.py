#objbase.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from ctypes import *
import objidl

def GetRunningObjectTable():
	rot = POINTER(objidl.IRunningObjectTable)()
	oledll.ole32.GetRunningObjectTable(0, byref(rot))
	return rot

def CreateBindCtx():
	bctx = POINTER(objidl.IBindCtx)()
	oledll.ole32.CreateBindCtx(0, byref(bctx))
	return bctx
