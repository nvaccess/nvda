# -*- coding: UTF-8 -*-
#appModules/skype.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2007-2014 Peter Vágner, NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import re
from comtypes import COMError
import wx
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
import NVDAObjects.behaviors
import api

# Translators: The name of the NVDA command category for Skype specific commands.
SCRCAT_SKYPE = _("Skype")

class Conversation(NVDAObjects.IAccessible.IAccessible):
	scriptCategory = SCRCAT_SKYPE

	def initOverlayClass(self):
		for n in xrange(0, 10):
			self.bindGesture("kb:NVDA+control+%d" % n, "reviewRecentMessage")

	def _gainedFocus(self):
		# The user has entered this Skype conversation.
		if self.appModule.conversation:
			# A conversation was already focused.
			if self.appModule.conversation.windowHandle == self.windowHandle:
				# This is the same conversation.
				return
			# This is another conversation that hasn't been cleaned up yet.
			self.appModule.conversation.lostFocus()

		self.appModule.conversation = self
		try:
			self.outputList = NVDAObjects.IAccessible.getNVDAObjectFromEvent(
				windowUtils.findDescendantWindow(self.windowHandle, className="TChatContentControl"),
				winUser.OBJID_CLIENT, 0).lastChild
		except LookupError:
			pass
		else:
			self.outputList.startMonitoring()
		try:
			self.typingIndicator = NVDAObjects.IAccessible.getNVDAObjectFromEvent(
				windowUtils.findDescendantWindow(self.windowHandle, className="TWidgetControl"),
				winUser.OBJID_CLIENT, 1)
		except LookupError:
			pass
		else:
			self.typingIndicator.startMonitoring()

	def event_focusEntered(self):
		self._gainedFocus()
		super(Conversation, self).event_focusEntered()

	def event_gainFocus(self):
		# A conversation might have its own top level window,
		# but foreground changes often trigger gainFocus instead of focusEntered.
		self._gainedFocus()
		super(Conversation, self).event_gainFocus()

	def lostFocus(self):
		self.appModule.conversation = None
		self.outputList.stopMonitoring()
		self.outputList = None
		self.typingIndicator.stopMonitoring()
		self.typingIndicator = None

	def script_reviewRecentMessage(self, gesture):
		try:
			index = int(gesture.mainKeyName[-1])
		except (AttributeError, ValueError):
			return
		if index == 0:
			index = 10
		self.outputList.reviewRecentMessage(index)
	# Describes the NVDA command to review messages in Skype.
	script_reviewRecentMessage.__doc__ = _("Reports and moves the review cursor to a recent message")
	script_reviewRecentMessage.canPropagate = True

class ChatOutputList(NVDAObjects.IAccessible.IAccessible):

	def startMonitoring(self):
		self.oldMessageCount = None
		self.update(initial=True)
		displayModel.requestTextChangeNotifications(self, True)

	def stopMonitoring(self):
		displayModel.requestTextChangeNotifications(self, False)

	RE_MESSAGE = re.compile(r"^From (?P<from>.*), (?P<body>.*), sent on (?P<time>.*?)(?: Edited by .* at .*?)?(?: Not delivered|New)?$")
	def reportMessage(self, text):
		# Messages are ridiculously verbose.
		# Strip the time and other metadata if possible.
		m = self.RE_MESSAGE.match(text)
		if m:
			text = "%s, %s" % (m.group("from"), m.group("body"))
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

	def reviewRecentMessage(self, index):
		count = self._getMessageCount()
		if index > count:
			# Translators: This is presented to inform the user that no instant message has been received.
			ui.message(_("No message yet"))
			return
		message = self.getChild(count - index)
		api.setNavigatorObject(message)
		self.reportMessage(message.name)

class Notification(NVDAObjects.behaviors.Notification):
	role = controlTypes.ROLE_ALERT

	def _get_name(self):
		return " ".join(child.name for child in self.children)

	def event_show(self):
		# There is a delay before the content of the notification is ready.
		wx.CallLater(500, self.event_alert)

class TypingIndicator(NVDAObjects.IAccessible.IAccessible):

	def startMonitoring(self):
		displayModel.requestTextChangeNotifications(self, True)

	def stopMonitoring(self):
		displayModel.requestTextChangeNotifications(self, False)

	def _report(self):
		if self.name:
			ui.message(self.name)
		else:
			# Translators: Indicates that a contact stopped typing.
			ui.message(_("Typing stopped"))

	def event_textChange(self):
		# This event is called from another thread, but this needs to run in the main thread.
		queueHandler.queueFunction(queueHandler.eventQueue, self._report)

class AppModule(appModuleHandler.AppModule):

	def __init__(self, *args, **kwargs):
		super(AppModule, self).__init__(*args, **kwargs)
		self.conversation = None

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
		wClass = obj.windowClassName
		role = obj.role
		if isinstance(obj, NVDAObjects.IAccessible.IAccessible) and obj.windowClassName == "TConversationForm" and obj.IAccessibleRole == oleacc.ROLE_SYSTEM_CLIENT:
			clsList.insert(0, Conversation)
		elif wClass == "TChatContentControl" and role == controlTypes.ROLE_LIST:
			clsList.insert(0, ChatOutputList)
		elif wClass == "TTrayAlert" and role == controlTypes.ROLE_WINDOW:
			clsList.insert(0, Notification)
		elif wClass == "TWidgetControl" and role == controlTypes.ROLE_LISTITEM:
			clsList.insert(0, TypingIndicator)

	def event_gainFocus(self, obj, nextHandler):
		if self.conversation and not winUser.isDescendantWindow(self.conversation.windowHandle, obj.windowHandle):
			self.conversation.lostFocus()
		nextHandler()

	def event_appModule_loseFocus(self):
		if self.conversation:
			self.conversation.lostFocus()
