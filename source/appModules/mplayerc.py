#appModules/mplayerc.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import appModuleHandler
from NVDAObjects.IAccessible import IAccessible, getNVDAObjectFromEvent
import controlTypes
import api
import IAccessibleHandler
import ctypes
import speech
import keyboardHandler

class appModule(appModuleHandler.appModule):

	def event_NVDAObject_init(self,obj):
		if obj.windowClassName=="#32770" and obj.windowControlID==10021:
			obj.__class__=MPCStatusBar

	def script_reportStatusLine(self,keyPress,nextScript):
		focus=api.getFocusObject()
		statusBarObject=focus.statusBar
		if not statusBarObject:
			statusWindow=ctypes.windll.user32.FindWindowExW(focus.parent.windowHandle,0,u'#32770',0)
			if statusWindow:
				statusBarObject=getNVDAObjectFromEvent(statusWindow,IAccessibleHandler.OBJID_CLIENT,0)
		if not statusBarObject:
			speech.speakMessage(_("no status bar found"))
			return
		if keyboardHandler.lastKeyCount == 1:
			speech.speakObject(statusBarObject,reason=speech.REASON_QUERY)
		else:
			speech.speakSpelling(statusBarObject.value)
		api.setNavigatorObject(statusBarObject)
	script_reportStatusLine.__doc__ = _("reads the current aplication status bar and moves the navigation cursor to it")

class MPCStatusBar(IAccessible):

	def _get_firstChild(self):
		return None

	def _get_lastChild(self):
		return None

	def _get_children(self):
		return []

	def _get_role(self):
		return controlTypes.ROLE_STATUSBAR

	def _get_value(self):
		oldValue=super(MPCStatusBar,self)._get_value()
		valueFromChildren=" ".join([" ".join([y for y in (x.name,x.value) if y and not y.isspace()]) for x in super(MPCStatusBar,self)._get_children() if x.role == controlTypes.ROLE_GRAPHIC])
		if valueFromChildren:
			return valueFromChildren
		else:
			return oldValue
