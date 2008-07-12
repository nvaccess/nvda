import eventHandler
import speech
import winUser
from . import IAccessible

class Page(IAccessible):

	def event_valueChange(self):
		if self.IAccessibleChildID==0 and winUser.isDescendantWindow(winUser.getForegroundWindow(),self.windowHandle):
			eventHandler.queueEvent("gainFocus",self)

class Document(IAccessible):

	def event_valueChange(self):
		if self.IAccessibleChildID==0 and winUser.isDescendantWindow(winUser.getForegroundWindow(),self.windowHandle):
			eventHandler.queueEvent("gainFocus",self)
