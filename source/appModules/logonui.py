#appModules/logonui.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2009-2011 James Teh <jamie@jantrid.net>, Michael Curran <mick@kulgan.net>

import speech
import api
import braille
import controlTypes
from NVDAObjects.IAccessible import IAccessible
from NVDAObjects.behaviors import Dialog
import appModuleHandler
import eventHandler
import UIAHandler
if UIAHandler.isUIAAvailable:
	from NVDAObjects.UIA import UIA

"""App module for the Windows Logon screen
"""

class LogonDialog(Dialog):

	role = controlTypes.ROLE_DIALOG
	isPresentableFocusAncestor = True

	def event_gainFocus(self):
		child = self.firstChild
		if child and controlTypes.STATE_FOCUSED in child.states and not eventHandler.isPendingEvents("gainFocus"):
			# UIA reports that focus is on the top level pane, even when it's actually on the frame below.
			# This causes us to incorrectly use UIA for the top level pane, which causes this pane to be spoken again when the focus moves.
			# Therefore, bounce the focus to the correct object.
			eventHandler.queueEvent("gainFocus", child)
			return

		return super(LogonDialog, self).event_gainFocus()

if UIAHandler.isUIAAvailable:
	class Win8PasswordField(UIA):

		#This UIA object has no invoke pattern, at least set focus.
		def doAction(self,index=None):
			if not index:
				self.setFocus()
			else:
				super(Win8PasswordField,self).doAction(index)

class XPPasswordField(IAccessible):

	def initOverlayClass(self):
		for gesture in ("kb:upArrow", "kb:downArrow"):
			self.bindGesture(gesture, "changeUser")

	def _get_name(self):
		# Focus automatically jumps to the password field when a user is selected. This field has no name.
		# This means that the new selected user is not reported.
		# However, the selected user name is the name of the window object for this field.
		try:
			self.parent.invalidateCache()
			return self.parent.name
		except:
			return super(XPPasswordField, self).name

	def script_changeUser(self, gesture):
		# The up and down arrow keys change the selected user, but there's no reliable NVDA event for detecting this.
		oldName = self.name
		gesture.send()
		self.invalidateCache()
		if oldName == self.name or controlTypes.STATE_FOCUSED not in self.states:
			return
		self.event_gainFocus()

class AppModule(appModuleHandler.AppModule):

	def event_NVDAObject_init(self, obj):
		if obj.windowClassName == "NativeHWNDHost" and obj.parent and not obj.parent.parent:
			# This is the top level pane of the XP logon screen.
			# Make sure it is always presented.
			obj.isPresentableFocusAncestor = True

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		windowClass = obj.windowClassName

		if UIAHandler.isUIAAvailable:
			if isinstance(obj,UIA) and obj.UIAElement.cachedClassName=="TouchEditInner" and obj.role==controlTypes.ROLE_EDITABLETEXT:
				clsList.insert(0,Win8PasswordField)
		if windowClass == "AUTHUI.DLL: LogonUI Logon Window" and obj.parent and obj.parent.parent and not obj.parent.parent.parent:
			clsList.insert(0, LogonDialog)
			return

		if windowClass == "Edit" and not obj.name:
			parent = obj.parent
			if parent and parent.role == controlTypes.ROLE_WINDOW:
				clsList.insert(0, XPPasswordField)
				return

	def event_gainFocus(self,obj,nextHandler):
		if obj.windowClassName=="DirectUIHWND" and obj.role==controlTypes.ROLE_BUTTON and not obj.next:
			prev=obj.previous
			if prev and prev.role==controlTypes.ROLE_STATICTEXT:
				# This is for a popup message in the logon dialog.
				# Present the dialog again so the message will be reported.
				speech.speakObjectProperties(api.getForegroundObject(),name=True,role=True,description=True)
				braille.invalidateCachedFocusAncestors(1)
		nextHandler()
