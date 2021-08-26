#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017 NV Access Limited

"""appModule for Microsoft Edge content processes"""

import appModuleHandler
import controlTypes
import winUser
from NVDAObjects.IAccessible import IAccessible

class CoreComponentInputSourcePane(IAccessible):
	shouldAllowIAccessibleFocusEvent=False

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self,obj,clsList):
		# #6948: Ignore MSAA focus event on CoreComponentInputSource pane 
		# as this happens on a broken object sometimes after getting a valid UIA focus event on the document
		# This would cause "Web runtime component" to be spoken twice,
		# And browse mode to be come unusable as this object is outside the document.
		if isinstance(obj,IAccessible) and obj.windowClassName=='Windows.UI.Core.CoreComponentInputSource' and obj.event_objectID==winUser.OBJID_CLIENT and obj.event_childID==0 and obj.role==controlTypes.Role.PANE:
			clsList.insert(0,CoreComponentInputSourcePane)
		return clsList
