#appModules/soffice.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2010 Michael Curran <mick@kulgan.net>

import appModuleHandler
import controlTypes
from NVDAObjects.window import Window
from NVDAObjects.IAccessible import IAccessible

class AppModule(appModuleHandler.AppModule):

	def event_valueChange(self,obj,nextHandler):
		#Ignore value changes from an annoying progress bar  which is a child of the main window
		#that keeps moving due to application performance
		if isinstance(obj,IAccessible) and obj.role==controlTypes.Role.PROGRESSBAR:
			windowParent=Window._get_parent(obj)
			if windowParent and windowParent.windowClassName=="SWT_Window0":
				return
		return nextHandler()
