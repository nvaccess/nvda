#objidl.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from ctypes import POINTER
from ctypes.wintypes import HWND, HRESULT, BOOL
from comtypes import GUID, COMMETHOD, IUnknown

class IOleWindow(IUnknown):
	_iid_ = GUID("{00000114-0000-0000-C000-000000000046}")
	_methods_ = [
		COMMETHOD([], HRESULT, "GetWindow",
			(["out"], POINTER(HWND), "phwnd")
		),
		COMMETHOD([], HRESULT, "ContextSensitiveHelp",
			(["in"], BOOL, "fEnterMode")
		),
	]
