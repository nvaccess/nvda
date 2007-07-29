#appModules/outlook.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import time
import win32com
import appModuleHandler
import api
import eventHandler
import speech
import controlTypes
from keyUtils import key, sendKey
from NVDAObjects.IAccessible import IAccessible
from NVDAObjects.window import Window

try:
	nativeOm=win32com.client.GetActiveObject("outlook.application")
except:
	nativeOm=win32com.client.Dispatch("outlook.application")
outlookVersion=int(nativeOm.version[0])

def getContactString(obj):
		return ", ".join([x for x in [obj.fullName,obj.companyName,obj.jobTitle,obj.email1address] if x and not x.isspace()])

def getReceivedMessageString(obj):
	nameList=[]
	nameList.append(obj.senderName)
	nameList.append(_("subject: %s")%obj.subject)
	nameList.append(_("received: %s")%obj.receivedTime)

	text=", ".join(nameList)
	if obj.unread:
		text="%s %s"%(_("unread"),text)
	if obj.attachments.count>0:
		text="%s %s"%(_("attachment"),text)
	return text

def getSentMessageString(obj):
	nameList=[]
	nameList.append(obj.to)
	nameList.append(_("subject: %s")%obj.subject)
	nameList.append(_("sent: %s")%obj.sentOn)
	return ", ".join(nameList)

class appModule(appModuleHandler.appModule):

	def event_NVDAObject_init(self,obj):
		obj.description=None
		controlID=obj.windowControlID
		className=obj.windowClassName
		if outlookVersion<11 and isinstance(obj,IAccessible) and ((className=="SUPERGRID" and controlID==4704) or (className=="rctrl_renwnd32" and controlID==109)):
			obj.__class__=MessageList_pre2003

class MessageList_pre2003(IAccessible):

	def _get_name(self):
		if hasattr(self,'curMessageItem'):
			return self.curMessageItem.msg.parent.name

	def _get_role(self):
		return controlTypes.ROLE_LIST

	def _get_firstChild(self):
		return getattr(self,"curMessageItem",None)

	def _get_children(self):
		child=getattr(self,"curMessageItem",None)
		if child:
			return [child]
		else:
			return []

	def event_gainFocus(self):
		try:
			msg=nativeOm.ActiveExplorer().selection[0]
		except:
			msg=None
			pass
		if msg:
			self.curMessageItem=MessageItem(self,msg)
		super(MessageList_pre2003,self).event_gainFocus()
		if msg:
			eventHandler.manageEvent("gainFocus",self.curMessageItem)

	def script_moveByMessage(self,keyPress,nextScript):
		if hasattr(self,'curMessageItem'):
			oldEntryID=self.curMessageItem.msg.entryID
		else:
			oldEntryID=None
		sendKey(keyPress)
		try:
			msg=nativeOm.ActiveExplorer().selection[0]
		except:
			msg=None
			pass
		if msg:
			messageItem=MessageItem(self,msg)
			newEntryID=messageItem.msg.entryID
			if newEntryID!=oldEntryID:
				self.curMessageItem=messageItem
				eventHandler.manageEvent("gainFocus",messageItem)

[MessageList_pre2003.bindKey(keyName,scriptName) for keyName,scriptName in [
	("extendedDown","moveByMessage"),
	("extendedUp","moveByMessage"),
	("extendedHome","moveByMessage"),
	("extendedEnd","moveByMessage"),
]]

class MessageItem(Window):

	def __init__(self,parent,msg):
		self.msg=msg
		self.parent=parent
		Window.__init__(self,parent.windowHandle)

	def _get_name(self):
		typeID=self.msg.Class
		if typeID==40:
			return getContactString(self.msg)
		elif typeID==43:
			return getReceivedMessageString(self.msg)

	def _get_role(self):
		return controlTypes.ROLE_LISTITEM

	def _get_states(self):
		return frozenset([controlTypes.STATE_SELECTED])

