#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2015 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import appModuleHandler

class AppModule(appModuleHandler.AppModule):

	def event_gainFocus(self, obj, nextHandler):
		if obj.windowClassName == "LockAppHostFrameWindow":
			# This window becomes foreground before the actual lock screen appears.
			# The name is ugly and it isn't useful, so ignore it.
			return
		nextHandler()
