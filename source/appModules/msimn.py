#appModules/msimn.py - Outlook Express appModule
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2012 NVDA Contributors
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import winUser
import controlTypes
import displayModel
import textInfos
import api
import appModuleHandler
from keyboardHandler import KeyboardInputGesture
from NVDAObjects.window import Window
from NVDAObjects.IAccessible import IAccessible, sysListView32
import watchdog
from NVDAObjects.behaviors import _FakeTableCell

messageListImageLabels={
	# Translators: This Outlook Express message has an attachment
	8:_("has attachment"),
	# Translators: this Outlook Express message is flagged
	34:_("flagged"),
}

#Labels for the header fields of an email, by control ID
envelopeNames={
	# Translators: This is presented in outlook or live mail to indicate email attachments.
	1000:_("Attachments"),
	# Translators: This is presented in outlook or live mail when creating a new email 'to:' or 'recipient:'
	1001:_("To:"),
	# Translators: This is presented in outlook or live mail when sending an email to a newsgroup
	1002:_("Newsgroup:"),
	# Translators: This is presented in outlook or live mail, email carbon copy
	1003:_("CC:"),
	# Translators: This is presented in outlook or live mail, email subject
	1004:_("Subject:"),
	# Translators: This is presented in outlook or live mail, email sender
	1005:_("From:"),
	# Translators: This is presented in outlook or live mail, date of email
	1016:_("Date:"),
	# Translators: This is presented in outlook or live mail
	1018:_("Forward to:"),
	# Translators: This is presented in outlook or live mail
	1019:_("Answer to:"),
	# Translators: This is presented in outlook or live mail
	1020:_("Organisation:"),
	# Translators: This is presented in outlook or live mail
	1021:_("Distribution:"),
	# Translators: This is presented in outlook or live mail
	1022:_("Key words:"),
	# Translators: This is presented in outlook or live mail, email blind carbon copy
	1026:_("BCC:"),
	# Translators: This is presented in outlook or live mail, email sender
	1037:_("From:"),
}

class AppModule(appModuleHandler.AppModule):

	def event_NVDAObject_init(self,obj):
		if not isinstance(obj,Window): return
		controlID=obj.windowControlID
		windowHandle=obj.windowHandle
		parentWindow=winUser.getAncestor(windowHandle,winUser.GA_PARENT)
		parentClassName=winUser.getClassName(parentWindow)
		#If this object is an email header field, and we have a custom label for it,
		#Then set the object's name to the label 
		if parentClassName=="OE_Envelope" and isinstance(obj,IAccessible) and obj.IAccessibleChildID==0 and controlID in envelopeNames:
			obj.name=envelopeNames[controlID]
			obj.useITextDocumentSupport=True
			obj.editValueUnit=textInfos.UNIT_STORY

	def chooseNVDAObjectOverlayClasses(self,obj,clsList):
		if obj.windowClassName=="SysListView32" and obj.windowControlID in (128,129,130) and obj.role==controlTypes.Role.LISTITEM:
			clsList.insert(0,MessageRuleListItem)
		elif "SysListView32" in obj.windowClassName and obj.role==controlTypes.Role.LISTITEM and obj.parent.name=="Outlook Express Message List":
			clsList.insert(0,MessageListItem)

	def event_gainFocus(self,obj,nextHandler):
		nextHandler()
		#Force focus to move to something sane when landing on an outlook express message window
		if obj.windowClassName=="ATH_Note" and obj.event_objectID==winUser.OBJID_CLIENT and obj.IAccessibleChildID==0:
			api.processPendingEvents()
			if obj==api.getFocusObject() and controlTypes.State.FOCUSED in obj.states:
				return KeyboardInputGesture.fromName("shift+tab").send()

class MessageRuleListItem(sysListView32.ListItem):
	"""Used for the checkbox list items used to select message rule types in in message filters"""

	role=controlTypes.Role.CHECKBOX

	def _get_states(self):
		states=super(MessageRuleListItem,self).states
		if (watchdog.cancellableSendMessage(self.windowHandle,sysListView32.LVM_GETITEMSTATE,self.IAccessibleChildID-1,sysListView32.LVIS_STATEIMAGEMASK)>>12)==8:
			states.add(controlTypes.State.CHECKED)
		return states

class MessageListItem(sysListView32.ListItem):

	def _getColumnContent(self,column):
		content=super(MessageListItem,self)._getColumnContent(column)
		if not content:
			imageID=self._getColumnImageID(column)
			if imageID>0:
				content=messageListImageLabels.get(imageID,"")
		return content

	def _get_isUnread(self):
		info=displayModel.DisplayModelTextInfo(self,textInfos.POSITION_FIRST)
		info.expand(textInfos.UNIT_CHARACTER)
		fields=info.getTextWithFields()
		try:
			isUnread=fields[0].field['bold']
		except:
			isUnread=False
		return isUnread

	def _get_name(self):
		nameList=[]
		imageState=watchdog.cancellableSendMessage(self.windowHandle,sysListView32.LVM_GETITEMSTATE,self.IAccessibleChildID-1,sysListView32.LVIS_STATEIMAGEMASK)>>12
		if imageState==5:
			nameList.append(controlTypes.State.COLLAPSED.displayString)
		elif imageState==6:
			nameList.append(controlTypes.State.EXPANDED.displayString)
		if self.isUnread:
			# Translators: Displayed in outlook or live mail to indicate an email is unread
			nameList.append(_("unread"))
		name=super(MessageListItem,self).name
		if name:
			nameList.append(name)
		return " ".join(nameList)
