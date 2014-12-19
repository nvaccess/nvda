# -*- coding: UTF-8 -*-
#appModules/skype.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2007-2014 Peter Vágner, NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from comtypes import COMError
import appModuleHandler
import controlTypes
import winUser
import NVDAObjects.IAccessible
import oleacc
import ui
import windowUtils
import displayModel
import queueHandler
import config

class ChatOutputList(NVDAObjects.IAccessible.IAccessible):

	def startMonitoring(self):
		self.oldMessageCount = None
		self.update(initial=True)
		displayModel.requestTextChangeNotifications(self, True)

	def stopMonitoring(self):
		displayModel.requestTextChangeNotifications(self, False)

	def reportMessage(self, text):
		ui.message(text)

	def _getMessageCount(self):
		ia = self.IAccessibleObject
		for c in xrange(self.childCount, -1, -1):
			try:
				if ia.accRole(c) != oleacc.ROLE_SYSTEM_LISTITEM or ia.accState(c) & oleacc.STATE_SYSTEM_UNAVAILABLE:
					# Not a message.
					continue
			except COMError:
				# The child probably disappeared after we fetched childCount.
				continue
			return c
		return 0

	def update(self, initial=False):
		newCount = self._getMessageCount()
		if (not initial and config.conf["presentation"]["reportDynamicContentChanges"]
				#4644: Don't report a flood of messages.
				and newCount - self.oldMessageCount < 5):
			ia = self.IAccessibleObject
			for c in xrange(self.oldMessageCount + 1, newCount + 1):
				text = ia.accName(c)
				if not text:
					continue
				self.reportMessage(text)
		self.oldMessageCount = newCount

	def event_textChange(self):
		# This event is called from another thread, but this needs to run in the main thread.
		queueHandler.queueFunction(queueHandler.eventQueue, self.update)

class AppModule(appModuleHandler.AppModule):

	def __init__(self, *args, **kwargs):
		super(AppModule, self).__init__(*args, **kwargs)
		self.chatWindow = None
		self.chatOutputList = None

	def event_NVDAObject_init(self,obj):
		if isinstance(obj, NVDAObjects.IAccessible.IAccessible) and obj.event_objectID is None and controlTypes.STATE_FOCUSED in obj.states and obj.role not in (controlTypes.ROLE_POPUPMENU,controlTypes.ROLE_MENUITEM,controlTypes.ROLE_MENUBAR):
			# The window handle reported by Skype accessibles is sometimes incorrect.
			# This object is focused, so we can override with the focus window.
			obj.windowHandle=winUser.getGUIThreadInfo(None).hwndFocus
			obj.windowClassName=winUser.getClassName(obj.windowHandle)
		if obj.value and obj.windowClassName in ("TMainUserList", "TConversationList", "TInboxList", "TActiveConversationList", "TConversationsControl"):
			# The name and value both include the user's name, so kill the value to avoid doubling up.
			# The value includes the Skype name,
			# but we care more about the additional info (e.g. new event count) included in the name.
			obj.value=None
		elif isinstance(obj, NVDAObjects.IAccessible.IAccessible) and obj.IAccessibleRole == oleacc.ROLE_SYSTEM_PANE and not obj.name:
			# Prevent extraneous reporting of pane when tabbing through a conversation form.
			obj.shouldAllowIAccessibleFocusEvent = False

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName == "TChatContentControl" and obj.role == controlTypes.ROLE_LIST:
			clsList.insert(0, ChatOutputList)

	def conversationMaybeFocused(self, obj):
		if not isinstance(obj, NVDAObjects.IAccessible.IAccessible) or obj.windowClassName != "TConversationForm" or obj.IAccessibleRole != oleacc.ROLE_SYSTEM_CLIENT:
			# This isn't a Skype conversation.
			return
		# The user has entered a Skype conversation.

		if self.chatWindow:
			# Another conversation was already focused and hasn't been cleaned up yet.
			self.conversationLostFocus()

		window = obj.windowHandle
		self.chatWindow = window
		try:
			self.chatOutputList = NVDAObjects.IAccessible.getNVDAObjectFromEvent(
				windowUtils.findDescendantWindow(window, className="TChatContentControl"),
				winUser.OBJID_CLIENT, 0).lastChild
		except LookupError:
			pass
		else:
			self.chatOutputList.startMonitoring()

	def event_focusEntered(self, obj, nextHandler):
		self.conversationMaybeFocused(obj)
		nextHandler()

	def conversationLostFocus(self):
		self.chatWindow = None
		self.chatOutputList.stopMonitoring()
		self.chatOutputList = None

	def event_gainFocus(self, obj, nextHandler):
		if self.chatWindow and not winUser.isDescendantWindow(self.chatWindow, obj.windowHandle):
			self.conversationLostFocus()
		# A conversation might have its own top level window,
		# but foreground changes often trigger gainFocus instead of focusEntered.
		self.conversationMaybeFocused(obj)
		nextHandler()

	def event_appModule_loseFocus(self):
		if self.chatWindow:
			self.conversationLostFocus()
