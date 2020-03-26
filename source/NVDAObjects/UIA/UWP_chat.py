# NVDAObjects/UIA/UWP_chat.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2020 Bill Dengler

import appModuleHandler
import ui

from abc import ABCMeta, abstractmethod
from NVDAObjects.behaviors import Monitor
from NVDAObjects.UIA import UIA
from scriptHandler import script


class UWPChatAppModule(appModuleHandler.AppModule, metaclass=ABCMeta):
	"A base app module for UWP chat apps that present messages in a list view."
	_lastMessage = None
	_chat = None
	POLLING_DELAY = 2

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if not isinstance(obj, UIA):
			return
		elif self._isMessagesListView(obj):
			clsList.insert(0, MessagesListView)
		elif self._isMessageTextBox(obj):
			clsList.insert(0, MessageTextBox)

	def event_NVDAObject_init(self, obj):
		if isinstance(obj, UIA) and self._isMessagesListView(obj) and self.chat != obj:
			self.chat = obj
			obj.startMonitoring()

	@script(gestures=[f"kb:control+NVDA+{i}" for i in range(10)])
	def script_reviewRecentMessage(self, gesture):
		try:
			index = int(gesture.mainKeyName[-1])
			if index == 0:
				index = 10
		except (AttributeError, ValueError):
			return
		try:
			ui.message(self.getMessage(index))
		except (AttributeError, IndexError):
			# Translators: This is presented to inform the user that no instant message has been received.
			ui.message(_("No message yet"))

	def event_appModule_gainFocus(self):
		if self.chat:
			self.chat.startMonitoring()

	def event_appModule_loseFocus(self):
		if self.chat:
			self.chat.stopMonitoring()

	def _get_chat(self):
		return self._chat

	def _set_chat(self, obj):
		if obj == self._chat:
			return
		if self._chat:
			self._chat.stopMonitoring()
		self._chat = obj

	@abstractmethod
	def _isMessagesListView(self, obj):
		"Returns whether this object is the list view where new messages arrive."
		raise NotImplementedError

	@abstractmethod
	def _isMessageTextBox(self, obj):
		"Returns whether this object is the text entry field."
		raise NotImplementedError

	@abstractmethod
	def getMessage(self, n):
		"Returns the nth most recent message from the chat list."
		raise NotImplementedError


class MessagesListView(Monitor):
	_lastMessage = None

	def initOverlayClass(self):
		self.POLLING_DELAY = self.appModule.POLLING_DELAY

	def hasChanged(self):
		if self._lastMessage is None:
			self._lastMessage = self.appModule.getMessage(1)
		return self.appModule.getMessage(1) != self._lastMessage

	def reactToChange(self):
		message = self.appModule.getMessage(1)
		ui.message(message)
		self._lastMessage = message

	def _getMostRecentMessage(self):
		try:
			return self.getChild(self.childCount - 1).name
		except IndexError:
			return None


class MessageTextBox(UIA):
	def initOverlayClass(self):
		if not self.appModule.chat:
			for i in self.parent.children:
				if isinstance(i, MessagesListView):
					self.appModule.chat = i
					i.startMonitoring()
