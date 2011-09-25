#appModules/msimn.py - Outlook Express appModule
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2010 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import winUser
import controlTypes
import displayModel
import textInfos
import api
import appModuleHandler
import speech
from keyboardHandler import KeyboardInputGesture
from NVDAObjects.IAccessible import sysListView32
import watchdog

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

class AppModule(appModuleHandler.AppModule):

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
			obj.editValueUnit=textInfos.UNIT_STORY

	def chooseNVDAObjectOverlayClasses(self,obj,clsList):
		if obj.windowClassName=="SysListView32" and obj.windowControlID in (128,129,130) and obj.role==controlTypes.ROLE_LISTITEM:
			clsList.insert(0,MessageRuleListItem)
		elif "SysListView32" in obj.windowClassName and obj.role==controlTypes.ROLE_LISTITEM and obj.parent.name=="Outlook Express Message List":
			clsList.insert(0,MessageListItem)

	def event_gainFocus(self,obj,nextHandler):
		nextHandler()
		#Force focus to move to something sane when landing on an outlook express message window
		if obj.windowClassName=="ATH_Note" and obj.event_objectID==winUser.OBJID_CLIENT and obj.IAccessibleChildID==0:
			api.processPendingEvents()
			if obj==api.getFocusObject() and controlTypes.STATE_FOCUSED in obj.states:
				return KeyboardInputGesture.fromName("shift+tab").send()

class MessageRuleListItem(sysListView32.ListItem):
	"""Used for the checkbox list items used to select message rule types in in message filters"""

	role=controlTypes.ROLE_CHECKBOX

	def _get_states(self):
		states=super(MessageRuleListItem,self).states
		if (watchdog.cancellableSendMessage(self.windowHandle,sysListView32.LVM_GETITEMSTATE,self.IAccessibleChildID-1,sysListView32.LVIS_STATEIMAGEMASK)>>12)==8:
			states.add(controlTypes.STATE_CHECKED)
		return states

class MessageListItem(sysListView32.ListItem):

	def _get_isUnread(self):
		info=displayModel.DisplayModelTextInfo(self,textInfos.POSITION_FIRST)
		info.expand(textInfos.UNIT_CHARACTER)
		fields=info.getTextWithFields()
		try:
			isUnread=fields[1].field['bold']
		except:
			isUnread=False
		return isUnread

	def _get_name(self):
		nameList=[]
		imageState=watchdog.cancellableSendMessage(self.windowHandle,sysListView32.LVM_GETITEMSTATE,self.IAccessibleChildID-1,sysListView32.LVIS_STATEIMAGEMASK)>>12
		if imageState==5:
			nameList.append(controlTypes.speechStateLabels[controlTypes.STATE_COLLAPSED])
		elif imageState==6:
			nameList.append(controlTypes.speechStateLabels[controlTypes.STATE_EXPANDED])
		if self.isUnread:
			nameList.append(_("unread"))
		name=super(MessageListItem,self).name
		if name:
			nameList.append(name)
		return " ".join(nameList)
