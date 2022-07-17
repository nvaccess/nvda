#appModules/mirc.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010 James Teh <jamie@jantrid.net>

"""App module for mIRC
"""

import controlTypes
from NVDAObjects.window import Window, DisplayModelLiveText
from NVDAObjects.IAccessible import StaticText
import appModuleHandler

class Input(Window):

	def event_gainFocus(self):
		super(Input, self).event_gainFocus()
		try:
			output = self.parent.parent.lastChild.firstChild
		except AttributeError:
			output = None
		if isinstance(output, DisplayModelLiveText):
			output.startMonitoring()
			self._output = output
		else:
			self._output = None

	def event_loseFocus(self):
		if self._output:
			self._output.stopMonitoring()

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.role == controlTypes.Role.WINDOW:
			return
		if obj.windowClassName == "Static" and obj.windowControlID == 32918:
			clsList.remove(StaticText)
			clsList.insert(0, DisplayModelLiveText)
		elif obj.windowClassName == "RichEdit20W" and obj.windowControlID == 32921:
			clsList.insert(0, Input)
