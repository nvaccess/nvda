#appModules/soffice.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import appModuleHandler
import controlTypes
import speech
import api

inDocument=False

class appModule(appModuleHandler.appModule):

	def event_gainFocus(self,obj,nextHandler):
		global inDocument
		if obj.role==controlTypes.ROLE_EDITABLETEXT:
			parent=obj.parent
			if parent and parent.role==controlTypes.ROLE_CANVAS:
				if not inDocument:
					inDocument=True
					return nextHandler()
				else:
					api.setNavigatorObject(obj)
					return
		inDocument=False
		return nextHandler()

