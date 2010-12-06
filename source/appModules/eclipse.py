#appModules/eclipse.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010 James Teh <jamie@jantrid.net>

import controlTypes
import appModuleHandler

class AppModule(appModuleHandler.AppModule):

	def event_NVDAObject_init(self, obj):
		if obj.windowClassName == "SysTreeView32" and obj.role == controlTypes.ROLE_TREEVIEWITEM and controlTypes.STATE_FOCUSED not in obj.states:
			# Eclipse tree views seem to fire a focus event on the previously focused item before firing focus on the new item (EclipseBug:315339).
			# Try to filter this out.
			obj.shouldAllowIAccessibleFocusEvent = False
