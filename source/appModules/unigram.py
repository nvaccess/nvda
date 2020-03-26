# NVDAObjects/appModules/unigram.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2020 Bill Dengler

from NVDAObjects.UIA.UWP_chat import UWPChatAppModule


class AppModule(UWPChatAppModule):
	def _isMessagesListView(self, obj):
		return obj.UIAElement.CachedAutomationID == "Messages"

	def _isMessageTextBox(self, obj):
		return obj.UIAElement.CachedAutomationID == "TextField"

	def getMessage(self, n):
		return self.chat.getChild(self.chat.childCount - n).name
