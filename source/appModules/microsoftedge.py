# MicrosoftEdge.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018 NV Access Limited, Joseph Lee

"""appModule for Microsoft Edge main process"""

import appModuleHandler
import api
import ui

class AppModule(appModuleHandler.AppModule):

	def event_UIA_notification(self, obj, nextHandler, displayString=None, **kwargs):
		# #8423: even though content process is focused, notifications are fired by main Edge process.
		# The base object will simply ignore this, so notifications must be announced here and no more.
		# And no, notifications should be limited to Edge context - that is, focused item is part of Edge (both main and content processes).
		if api.getFocusObject().appModule.appName.startswith("microsoftedge"):
			ui.message(displayString)

