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

_nativeOm=None

def getNativeOm():
	global _nativeOm
	if not _nativeOm:
		try:
			_nativeOm=win32com.client.GetActiveObject("outlook.Application")
		except:
			_nativeOm=win32com.client.Dispatch("outlook.Application")
	return _nativeOm

class appModule(appModuleHandler.appModule):

	def event_NVDAObject_init(self,obj):
		obj.description=None
		controlID=obj.windowControlID
		className=obj.windowClassName
		nativeOm=getNativeOm()
		if nativeOm and nativeOm.version.startswith("9.0") and isinstance(obj,IAccessible) and className=="SUPERGRID" and controlID==4704:
			obj.__class__=MessageList_2000

class MessageList_2000(IAccessible):

	def _get_name(self):
		return _("Messages")

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
		super(MessageList_2000,self).event_gainFocus()
		nativeOm=getNativeOm()
		if nativeOm:
			self.curMessageItem=MessageItem(self,nativeOm.ActiveExplorer().selection[0])
			eventHandler.manageEvent("gainFocus",self.curMessageItem)

	def script_moveByMessage(self,keyPress,nextScript):
		oldEntryID=self.curMessageItem.msg.entryID
		sendKey(keyPress)
		messageItem=MessageItem(self,getNativeOm().ActiveExplorer().selection[0])
		newEntryID=messageItem.msg.entryID
		if newEntryID!=oldEntryID:
			self.curMessageItem=messageItem
			eventHandler.manageEvent("gainFocus",messageItem)

[MessageList_2000.bindKey(keyName,scriptName) for keyName,scriptName in [
	("extendedDown","moveByMessage"),
	("extendedUp","moveByMessage"),
]]

class MessageItem(Window):

	def __init__(self,parent,msg):
		self.msg=msg
		self.parent=parent
		Window.__init__(self,parent.windowHandle)

	def _get_name(self):
		nameList=[]
		if self.msg.attachments.count>0:
			nameList.append(_("attachment"))
		if self.msg.unread:
			nameList.append(_("unread"))
		nameList.append(self.msg.senderName)
		return " ".join(nameList)

	def _get_role(self):
		return controlTypes.ROLE_LISTITEM

	def _get_states(self):
		return frozenset([controlTypes.STATE_SELECTED])

	def _get_value(self):
		return _("Subject: %s, Received: %s")%(self.msg.subject,self.msg.receivedTime)
