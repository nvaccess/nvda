#appModules/thunderbird.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2012 NVDA Contributors
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import appModuleHandler
import controlTypes
import api
import speech
import winUser

class AppModule(appModuleHandler.AppModule):

	def event_gainFocus(self, obj, nextHandler):
		if obj.role == controlTypes.Role.DOCUMENT and controlTypes.State.BUSY in obj.states and winUser.isWindowVisible(obj.windowHandle):
			statusBar = api.getStatusBar()
			if statusBar:
				try:
					# The document loading status is contained in the second field of the status bar.
					statusText = statusBar.firstChild.next.name
				except:
					# Fall back to reading the entire status bar.
					statusText = api.getStatusBarText(statusBar)
				speech.speakMessage(controlTypes.State.BUSY.displayString)
				speech.speakMessage(statusText)
				return
		nextHandler()
