#appModules/msimn.py - Outlook Express appModule
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import winUser
import api
import IAccessibleHandler
import appModuleHandler

envelopeNames={
	1000:_("Attachments"),
	1001:_("To:"),
	1003:_("CC:"),
	1004:_("Subject:"),
	1005:_("From:"),
	1016:_("Date:"),
	1026:_("BCC:"),
	1037:_("From:"),
}

class appModule(appModuleHandler.appModule):

	def event_IAccessible_gainFocus(self,window,objectID,childID,nextHandler):
		focusObject=api.getFocusObject()
		controlID=winUser.getControlID(window)
		parentWindow=winUser.getAncestor(window,winUser.GA_PARENT)
		parentClassName=winUser.getClassName(parentWindow)
		if parentClassName=="OE_Envelope" and objectID==IAccessibleHandler.OBJID_CLIENT and envelopeNames.has_key(controlID):
			focusObject.setProperty('typeString',envelopeNames[controlID])
		nextHandler(window,objectID,childID)
