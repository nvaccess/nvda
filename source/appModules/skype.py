# -*- coding: UTF-8 -*-
#appModules/skype.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2007-2013 Peter Vágner, NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

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
		self.oldCount = self.childCount
		self.oldLastMessageText = self.getLastMessageText()
		displayModel.requestTextChangeNotifications(self, True)

	def stopMonitoring(self):
		displayModel.requestTextChangeNotifications(self, False)

	def getLastMessageText(self):
		ia = self.IAccessibleObject
		for c in xrange(self.childCount, -1, -1):
			if ia.accRole(c) == oleacc.ROLE_SYSTEM_LISTITEM:
				return ia.accName(c)
		return None

	def getOldLastMessageId(self):
		if not self.oldLastMessageText:
			return None
		ia = self.IAccessibleObject
		for c in xrange(self.childCount, -1, -1):
			if ia.accName(c) == self.oldLastMessageText:
				return c
		return None

	def reportMessage(self, text):
		if text.startswith("["):
			# Remove the timestamp.
			text = text.split("] ", 1)[1]
		ui.message(text)

	def handleChange(self):
		newCount = self.childCount
		if newCount == self.oldCount:
			# optimisation: If the count is the same, there's no change.
			return
		self.oldCount = newCount
		if not config.conf["presentation"]["reportDynamicContentChanges"]:
			# optimisation: If we're not reporting new messages, just make sure we set state correctly ofr next time.
			self.oldLastMessageText = self.getLastMessageText()
			return

		# Ideally, we'd determine new messages based just on the change in child count,
		# but children can be inserted in the middle when messages are expanded.
		oldLastMessageId = self.getOldLastMessageId()
		if not oldLastMessageId:
			self.oldLastMessageText = self.getLastMessageText()
			return
		ia = self.IAccessibleObject
		text = None
		for c in xrange(oldLastMessageId + 1, newCount + 1):
			if ia.accRole(c) != oleacc.ROLE_SYSTEM_LISTITEM:
				# Not a message.
				continue
			text = ia.accName(c)
			if not text:
				continue
			self.reportMessage(text)
		if text:
			self.oldLastMessageText = text

	def event_textChange(self):
		# This event is called from another thread, but this needs to run in the main thread.
		queueHandler.queueFunction(queueHandler.eventQueue, self.handleChange)

class AppModule(appModuleHandler.AppModule):

	def __init__(self, *args, **kwargs):
		super(AppModule, self).__init__(*args, **kwargs)
		self.chatWindow = None
		self.chatOutputList = None

	def event_NVDAObject_init(self,obj):
		if controlTypes.STATE_FOCUSED in obj.states and obj.role not in (controlTypes.ROLE_POPUPMENU,controlTypes.ROLE_MENUITEM,controlTypes.ROLE_MENUBAR):
			# The window handle reported by Skype accessibles is sometimes incorrect.
			# This object is focused, so we can override with the focus window.
			obj.windowHandle=winUser.getGUIThreadInfo(None).hwndFocus
			obj.windowClassName=winUser.getClassName(obj.windowHandle)
		if obj.value and obj.windowClassName in ("TMainUserList", "TchatOutputList", "TInboxList", "TActivechatOutputList", "TConversationsControl"):
			# The name and value both include the user's name, so kill the value to avoid doubling up.
			# The value includes the Skype name,
			# but we care more about the additional info (e.g. new event count) included in the name.
			obj.value=None

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName == "TChatContentControl" and obj.role == controlTypes.ROLE_LIST:
			clsList.insert(0, ChatOutputList)

	def event_focusEntered(self, obj, nextHandler):
		if isinstance(obj, NVDAObjects.IAccessible.IAccessible) and obj.windowClassName == "TConversationForm" and obj.IAccessibleRole == oleacc.ROLE_SYSTEM_CLIENT:
			# The user has entered a Skype conversation.
			self.chatWindow = obj.windowHandle
			try:
				self.chatOutputList = NVDAObjects.IAccessible.getNVDAObjectFromEvent(
					windowUtils.findDescendantWindow(obj.windowHandle, className="TChatContentControl"),
					winUser.OBJID_CLIENT, 1)
			except LookupError:
				pass
			else:
				self.chatOutputList.startMonitoring()
		nextHandler()
	# A conversation might have its own top level window,
	# but foreground changes often trigger gainFocus instead of focusEntered.
	# Therefore, explicitly treat foreground events as focusEntered.
	event_foreground = event_focusEntered

	def conversationLostFocus(self):
		self.chatWindow = None
		self.chatOutputList.stopMonitoring()
		self.chatOutputList = None

	def event_gainFocus(self, obj, nextHandler):
		if self.chatWindow and not winUser.isDescendantWindow(self.chatWindow, obj.windowHandle):
			self.conversationLostFocus()
		nextHandler()

	def event_appModule_loseFocus(self):
		if self.chatWindow:
			self.conversationLostFocus()
