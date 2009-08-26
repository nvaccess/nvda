#appModules/wlmail.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2009 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import _default
import controlTypes
import eventHandler
import api
import winUser
from keyUtils import key, sendKey
from NVDAObjects.IAccessible.MSHTML import MSHTML

class AboutBlankDocument(MSHTML):
	"""A document called about:blank which hosts the HTML message composer document using viewlink.
	Unfortunately, there doesn't seem to be any way to access the real (editable) viewlink document.
	Therefore, we need to ignore this about:blank document so the user can access the editable document.
	"""

	# Make sure a buffer doesn't get created for this document.
	# Otherwise, the viewLink document beneath it will be treated as part of this buffer and won't be accessible.
	role = controlTypes.ROLE_UNKNOWN

	def event_gainFocus(self):
		# This document is useless to us, so don't bother to report it.
		return

class AppModule(_default.AppModule):

	def event_NVDAObject_init(self, obj):
		if obj.windowClassName == "Internet Explorer_Server" and obj.role == controlTypes.ROLE_DOCUMENT:
			parent = obj.parent
			if parent.name == "about:blank":
				self.overlayCustomNVDAObjectClass(obj,AboutBlankDocument,outerMost=True)

	def event_gainFocus(self,obj,nextHandler):
		nextHandler()
		#Force focus to move to something sane when landing on a plain text message window
		if obj.windowClassName=="ATH_Note" and obj.event_objectID==winUser.OBJID_CLIENT and obj.IAccessibleChildID==0:
			api.processPendingEvents()
			if obj==api.getFocusObject() and controlTypes.STATE_FOCUSED in obj.states:
				return sendKey(key("SHIFT+TAB"))
