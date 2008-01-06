#appModules/msimn.py - Outlook Express appModule
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import winUser
import controlTypes
import textHandler
import api
import eventHandler
import IAccessibleHandler
import appModuleHandler
import speech
from keyUtils import key, sendKey

lastFocusRole=None
lastFocusWindowHandle=None

#Labels for the header fields of an email, by control ID
envelopeNames={
	1000:_("Attachments"),
	1001:_("To:"),
	1002:_("Newsgroup:"),
	1003:_("CC:"),
	1004:_("Subject:"),
	1005:_("From:"),
	1016:_("Date:"),
	1018:_("Forward to:"),
	1019:_("Answer to:"),
	1020:_("Organisation:"),
	1021:_("Distribution:"),
	1022:_("Key words:"),
	1026:_("BCC:"),
	1037:_("From:"),
}

class appModule(appModuleHandler.appModule):

	def event_NVDAObject_init(self,obj):
		controlID=obj.windowControlID
		windowHandle=obj.windowHandle
		parentWindow=winUser.getAncestor(windowHandle,winUser.GA_PARENT)
		parentClassName=winUser.getClassName(parentWindow)
		#If this object is an email header field, and we have a custom label for it,
		#Then set the object's name to the label 
		if parentClassName=="OE_Envelope" and obj.IAccessibleChildID==0 and envelopeNames.has_key(controlID):
			obj.name=envelopeNames[controlID]
			obj.editAPIHasITextDocument=True
			obj.editValueUnit=textHandler.UNIT_STORY

	def event_gainFocus(self,obj,nextHandler):
		global lastFocusRole, lastFocusWindowHandle
		#Force focus to move to something sane when landing on an outlook express message window
		if obj.windowClassName=="ATH_Note" and obj.IAccessibleObjectID==IAccessibleHandler.OBJID_CLIENT and obj.IAccessibleChildID==0:
			api.processPendingEvents()
			if obj==api.getFocusObject() and controlTypes.STATE_FOCUSED in obj.states:
				return sendKey(key("SHIFT+TAB"))
		ignore=False
		focusRole=obj.role
		focusWindowHandle=obj.windowHandle
		#When deleting a message, an MSAA focus event gets sent before the message is deleted, so the child ID ends up being wrong
		if (focusRole==controlTypes.ROLE_LISTITEM and obj.IAccessibleChildID>1 and not obj.IAccessibleStates&IAccessibleHandler.STATE_SYSTEM_FOCUSED) or (focusRole==controlTypes.ROLE_UNKNOWN and obj.windowClassName=="SysListView32" and obj.IAccessibleChildID>0):
			newObj=obj.parent.activeChild
			if newObj:
				api.setFocusObject(newObj)
				eventHandler.manageEvent("gainFocus",newObj)
			lastFocusWindowHandle=focusWindowHandle
			lastFocusRole=focusRole
			return
		#Outlook express has a bug where deleting a message causes focus to move to the message list.
		if focusWindowHandle==lastFocusWindowHandle and focusRole==controlTypes.ROLE_LIST and lastFocusRole in [controlTypes.ROLE_LISTITEM,controlTypes.ROLE_LIST]:
			ignore=True
		lastFocusRole=focusRole
		lastFocusWindowHandle=focusWindowHandle
		if not ignore:
			return nextHandler()

