#appModules/msimn.py - Outlook Express appModule
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import winUser
import controlTypes
import api
import IAccessibleHandler
import appModuleHandler
import speech

lastFocusRole=None

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
		#Sometimes list items in the message list get a focus event, yet their focus state is not set
		#So allow reportFocus to run on these objects
		if obj.role==controlTypes.ROLE_LISTITEM:
			obj.reportFocusNeedsIAccessibleFocusState=False

	def event_gainFocus(self,obj,nextHandler):
		global lastFocusRole
		ignore=False
		focusRole=obj.role
		#Outlook express has a bug where deleting a message causes focus to move to the message list.
		if focusRole==controlTypes.ROLE_LIST and lastFocusRole==controlTypes.ROLE_LISTITEM:
			ignore=True
		lastFocusRole=focusRole
		if not ignore:
			return nextHandler()

