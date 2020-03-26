# appModules/unigram.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2020 Bill Dengler

import appModuleHandler
import time
import threading
import ui
import UIAHandler

from comtypes import COMError
from NVDAObjects.UIA import UIA
from scriptHandler import script


class AppModule(appModuleHandler.AppModule):
	_lastMessage = None
	_chat = None

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if not isinstance(obj, UIA):
			return
		elif obj.UIAElement.CachedAutomationID == "Messages":
			clsList.insert(0, MessagesListView)
		elif obj.UIAElement.CachedAutomationID == "TextField":
			clsList.insert(0, MessageTextBox)

	def event_NVDAObject_init(self, obj):
		if isinstance(obj, UIA) and obj.UIAElement.CachedAutomationID == "Messages" and self.chat != obj:
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
			ui.message(self.chat.getChild(self.chat._getChildCount() - index).name)
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


class MessagesListView(UIA):
	_monitoring = False

	def _getChildCount(self):
		childrenCacheRequest = UIAHandler.handler.baseCacheRequest.clone()
		childrenCacheRequest.TreeScope = UIAHandler.TreeScope_Children
		try:
			cachedChildren = self.UIAElement.buildUpdatedCache(childrenCacheRequest).getCachedChildren()
		except COMError:
			return len(super().children)
		if not cachedChildren:
			# GetCachedChildren returns null if there are no children.
			raise IndexError
		return cachedChildren.length

	def _monitor(self):
		try:
			lastMessage = self.getChild(self._getChildCount() - 1).name
		except IndexError:
			lastMessage = None
		while self._monitoring:
			try:
				message = self.getChild(self._getChildCount() - 1).name
			except IndexError:
				message = None
			if message != lastMessage:
				ui.message(message)
				lastMessage = message
			time.sleep(2)

	def startMonitoring(self):
		if self._monitoring:
			return
		self._monitoring = True
		threading.Thread(target=self._monitor).start()

	def stopMonitoring(self):
		self._monitoring = False


class MessageTextBox(UIA):
	def initOverlayClass(self):
		if not self.appModule.chat:
			for i in self.parent.children:
				if isinstance(i, MessagesListView):
					self.appModule.chat = i
					i.startMonitoring()
