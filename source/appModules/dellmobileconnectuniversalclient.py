# appModules/dellmobileconnectuniversalclient.py
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 Bill Dengler
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import api
import appModuleHandler
import braille
import config
import controlTypes
import speech
import textInfos
import ui
from NVDAObjects.behaviors import Monitor
from NVDAObjects.UIA import UIA
from scriptHandler import script


class AppModule(appModuleHandler.AppModule):
	_lastMessage = None
	_chat = None

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if not isinstance(obj, UIA):
			return
		if obj.UIAElement.CachedAutomationID == "MessageTextBody":
			clsList.insert(0, MessageTextBody)
		elif obj.UIAElement.CachedAutomationID == "MessagesListView":
			clsList.insert(0, MessagesListView)
		elif isinstance(obj.parent, MessagesListView):
			clsList.insert(0, MessagesListViewItem)
		elif obj.UIAElement.CachedAutomationID == "MessageTextBox":
			clsList.insert(0, MessageTextBox)

	def event_NVDAObject_init(self, obj):
		if isinstance(obj, UIA) and obj.UIAElement.CachedAutomationID == "MessagesListView" and self.chat != obj:
			self.chat = obj
			obj.startMonitoring()

	@script(gestures=[f"kb:control+NVDA+{i}" for i in range(10)])
	def script_reviewRecentMessage(self, gesture):
		try:
			index = int(gesture.mainKeyName[-1]) - 1
		except (AttributeError, ValueError):
			return
		if index == -1:
			index = 9
		try:
			message = self.chat.getChild(index)
			api.setNavigatorObject(message, isFocus=True)
			ui.message(message.name)
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


class MessageTextBody(UIA):
	role = controlTypes.ROLE_UNKNOWN

	def _get_notification(self):
		title = ''
		for i in self.parent.parent.children:
			if isinstance(i, UIA) and i.UIAElement.CachedAutomationID in ("ContactName", "AppTitle"):
				title = i.name
		return (title, self.makeTextInfo(textInfos.POSITION_ALL).text)

	def initOverlayClass(self):
		# We only want to notify the user once a message window is created,
		# and not everytime the message text gains focus (such as when tabbing
		# in the notification window).
		if self.notification != self.appModule._lastMessage and config.conf["presentation"]["reportHelpBalloons"]:
			title, content = self.notification
			self.appModule._lastMessage = self.notification
			speech.speak(
				(title, speech.EndUtteranceCommand(), content),
				priority=speech.priorities.SpeechPriority.NOW
			)
			braille.handler.message(f"{title}: {content}")


class MessagesListView(Monitor):
	_lastMessage = None

	def _getMostRecentMessage(self):
		try:
			return self.getChild(0).name
		except IndexError:
			return None

	def hasChanged(self):
		if not self._lastMessage:
			self._lastMessage = self._getMostRecentMessage()
		message = self._getMostRecentMessage()
		return message != self._lastMessage

	def reactToChange(self):
		message = self._getMostRecentMessage()
		ui.message(message)
		self._lastMessage = message


class MessagesListViewItem(UIA):
	def _get_name(self):
		name = super().name
		if name.startswith(",, "):
			return name[3:]
		return name


class MessageTextBox(UIA):
	def initOverlayClass(self):
		if not self.appModule.chat:
			for i in self.parent.children:
				if isinstance(i, MessagesListView):
					self.appModule.chat = i
					i.startMonitoring()
