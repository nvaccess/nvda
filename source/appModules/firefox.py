#appModules/firefox.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import appModuleHandler
import controlTypes
import api
import speech
import winUser

class AppModule(appModuleHandler.AppModule):

	def event_stateChange(self, obj, nextHandler):
		if obj.role == controlTypes.ROLE_DOCUMENT and controlTypes.STATE_BUSY in obj.states and winUser.isWindowVisible(obj.windowHandle):
			statusBar = api.getStatusBar()
			if statusBar:
				statusText = api.getStatusBarText(statusBar)
				speech.cancelSpeech()
				speech.speakMessage(controlTypes.speechStateLabels[controlTypes.STATE_BUSY])
				speech.speakMessage(statusText)
				return
		nextHandler()

	event_gainFocus = event_stateChange
