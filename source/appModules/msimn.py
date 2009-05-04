#appModules/msimn.py - Outlook Express appModule
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import winUser
import controlTypes
import TextInfos
import api
import eventHandler
import IAccessibleHandler
import _default
import speech
from keyUtils import key, sendKey

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

class AppModule(_default.AppModule):

	def event_NVDAObject_init(self,obj):
		controlID=obj.windowControlID
		windowHandle=obj.windowHandle
		parentWindow=winUser.getAncestor(windowHandle,winUser.GA_PARENT)
		parentClassName=winUser.getClassName(parentWindow)
		#If this object is an email header field, and we have a custom label for it,
		#Then set the object's name to the label 
		if parentClassName=="OE_Envelope" and obj.IAccessibleChildID==0 and envelopeNames.has_key(controlID):
			obj.name=envelopeNames[controlID]
			obj.useITextDocumentSupport=True
			obj.editValueUnit=TextInfos.UNIT_STORY

	def event_gainFocus(self,obj,nextHandler):
		nextHandler()
		#Force focus to move to something sane when landing on an outlook express message window
		if obj.windowClassName=="ATH_Note" and obj.event_objectID==IAccessibleHandler.OBJID_CLIENT and obj.IAccessibleChildID==0:
			api.processPendingEvents()
			if obj==api.getFocusObject() and controlTypes.STATE_FOCUSED in obj.states:
				return sendKey(key("SHIFT+TAB"))

