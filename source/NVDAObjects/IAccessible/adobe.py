import eventHandler
import winUser
from . import IAccessible, getNVDAObjectFromEvent

class AdobeAcrobatDocumentNode(IAccessible):

	def event_valueChange(self):
		if self.IAccessibleChildID==0 and winUser.isDescendantWindow(winUser.getForegroundWindow(),self.windowHandle):
			# This page may die and be replaced by another with the same event params, so always grab a new one.
			obj = getNVDAObjectFromEvent(self.windowHandle, -4, 0)
			if not obj:
				return
			eventHandler.queueEvent("gainFocus",obj)
