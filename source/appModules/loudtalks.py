#appModules/loudtalks.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2010 Peter Vagner <peter.v@datagate.sk>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import _default
from NVDAObjects.IAccessible import IAccessible
import oleacc
from NVDAObjects.IAccessible.sysListView32 import ListItem
import controlTypes
from NVDAObjects.window import Window

class loudTalksLink(Window):

	value = None

	role = controlTypes.ROLE_LINK


class loudTalksBrokenPropertyPage(IAccessible):

	children =[]


class loudTalksContactListItem(ListItem):

	shouldAllowIAccessibleFocusEvent = True

	def _get_keyboardShortcut(self):
		keyboardShortcut = super(loudTalksContactListItem,self).keyboardShortcut
		if keyboardShortcut == "None":
			 return None
		return keyboardShortcut


class AppModule(_default.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName == "UrlStaticWndClass":
			clsList.insert(0, loudTalksLink)
		elif obj.windowControlID == 1009 and isinstance(obj, IAccessible) and obj.IAccessibleRole == oleacc.ROLE_SYSTEM_LISTITEM:
			clsList.insert(0, loudTalksContactListItem)
		elif obj.windowControlID == 0 and isinstance(obj, IAccessible) and obj.IAccessibleRole == oleacc.ROLE_SYSTEM_PROPERTYPAGE:
			clsList.insert(0, loudTalksBrokenPropertyPage)
