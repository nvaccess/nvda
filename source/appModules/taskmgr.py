# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2018-2022 NV Access Limited, Derek Riemer
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import appModuleHandler
from NVDAObjects import NVDAObject
from NVDAObjects.UIA import UIA

def isChildOfRow(obj):
	"""
	calculates obj's ancestors  , discovering if this is a child of a row.
	If obj is a child of a row, this returns true.
	"""
	while obj.parent and obj.parent.presentationType != obj.presType_content:
		if isinstance(obj.parent, UIA) and obj.parent.UIAAutomationId == "TmViewRow":
			return True
		obj = obj.parent
	return False

class BrokenUIAChild(UIA):
	# This is A child which is layout, but should be content.
	presentationType = NVDAObject.presType_content

class AppModule(appModuleHandler.AppModule):
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if isinstance(obj, UIA) and obj.UIAAutomationId == "TmRowIcon":
			# This is an icon and really is layout. Don't show it.
			return
		if obj.presentationType == obj.presType_layout and isChildOfRow(obj):
			clsList.insert(0, BrokenUIAChild)
