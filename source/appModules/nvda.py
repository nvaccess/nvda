#appModules/nvda.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2008-2011 NV Access Inc
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import appModuleHandler
import api
import controlTypes
import versionInfo

class AppModule(appModuleHandler.AppModule):

	def event_NVDAObject_init(self, obj):
		# It seems that context menus always get the name "context" and this cannot be overridden.
		# Fudge the name of the NVDA system tray menu to make it more friendly.
		if obj.role == controlTypes.ROLE_POPUPMENU:
			parent = obj.parent
			if parent and parent.parent==api.getDesktopObject():
				obj.name=versionInfo.name

	def event_gainFocus(self, obj, nextHandler):
		if obj.role == controlTypes.ROLE_UNKNOWN and controlTypes.STATE_INVISIBLE in obj.states:
			return
		nextHandler()

	# Silence invisible unknowns for stateChange as well.
	event_stateChange = event_gainFocus
