#virtualBuffers/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import NVDAObjects
import IAccessible

def getVirtualBuffer(obj):
	if isinstance(obj,NVDAObjects.IAccessible.NVDAObject_IAccessible):
		return IAccessible.getVirtualBuffer(obj)

def update(obj):
	if isinstance(obj,NVDAObjects.window.NVDAObject_window):
		IAccessible.update(obj)
