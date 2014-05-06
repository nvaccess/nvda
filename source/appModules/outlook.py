#appModules/outlook.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2010 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from comtypes import COMError
import comtypes.client
import winUser
import appModuleHandler
import eventHandler
import UIAHandler
import api
import controlTypes
import config
import speech
import ui
from NVDAObjects.IAccessible import IAccessible
from NVDAObjects.window import Window
from NVDAObjects.IAccessible.MSHTML import MSHTML
from NVDAObjects.behaviors import RowWithFakeNavigation
from NVDAObjects.UIA import UIA

importanceLabels={
	# Translators: for a high importance email
	2:_("high importance"),
	# Translators: For a low importance email
	0:_("low importance"),
}

def getContactString(obj):
		return ", ".join([x for x in [obj.fullName,obj.companyName,obj.jobTitle,obj.email1address] if x and not x.isspace()])

def getReceivedMessageString(obj):
	nameList=[]
	nameList.append(obj.senderName)
	# Translators: This is presented in outlook or live mail, email subject
	nameList.append(_("subject: %s")%obj.subject)
	# Translators: This is presented in outlook or live mail, email received time
	nameList.append(_("received: %s")%obj.receivedTime)

	text=", ".join(nameList)
	if obj.unread:
		text="%s %s"%(_("unread"),text)
	if obj.attachments.count>0:
		# Translators: This is presented in outlook or live mail, indicating email attachments
		text="%s %s"%(_("attachment"),text)
	return text

def getSentMessageString(obj):
	nameList=[]
	nameList.append(obj.to)
	nameList.append(_("subject: %s")%obj.subject)
	# Translators: This is presented in outlook or live mail, email sent date
	nameList.append(_("sent: %s")%obj.sentOn)
	return ", ".join(nameList)

class AppModule(appModuleHandler.AppModule):

	def _get_nativeOm(self):
		if not getattr(self,'_nativeOm',None):
			try:
				nativeOm=comtypes.client.GetActiveObject("outlook.application",dynamic=True)
			except (COMError,WindowsError):
				nativeOm=None
			self._nativeOm=nativeOm
		return self._nativeOm

	def _get_outlookVersion(self):
		nativeOm=self.nativeOm
		if nativeOm:
			outlookVersion=int(nativeOm.version.split('.')[0])
		else:
			outlookVersion=0
		return outlookVersion

	def event_NVDAObject_init(self,obj):
		role=obj.role
		windowClassName=obj.windowClassName
		controlID=obj.windowControlID
		#The control showing plain text messages has very stuffed parents
		#Use the grandparent window as its parent
		if role==controlTypes.ROLE_EDITABLETEXT and windowClassName=="RichEdit20W" and controlID==8224:
			obj.parent=Window._get_parent(Window._get_parent(obj))
		#The control that shows HTML messages has stuffed parents. Use the control's parent window as its parent
		if windowClassName=="Internet Explorer_Server" and role==controlTypes.ROLE_PANE and not isinstance(obj,MSHTML):
			obj.parent=Window._get_parent(Window._get_parent(obj))
		if role in (controlTypes.ROLE_MENUBAR,controlTypes.ROLE_MENUITEM):
			obj.description=None
		if role in (controlTypes.ROLE_TREEVIEW,controlTypes.ROLE_TREEVIEWITEM,controlTypes.ROLE_LIST,controlTypes.ROLE_LISTITEM):
			obj.shouldAllowIAccessibleFocusEvent=True
		if ((windowClassName=="SUPERGRID" and controlID==4704) or (windowClassName=="rctrl_renwnd32" and controlID==109)) and role==controlTypes.ROLE_UNKNOWN:
			obj.role=controlTypes.ROLE_LISTITEM

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		# Currently all our custom classes are IAccessible
		if isinstance(obj,UIA) and obj.UIAElement.cachedClassName in ("LeafRow","ThreadItem","ThreadHeader"):
			clsList.insert(0,UIAGridRow)
		if not isinstance(obj,IAccessible):
			return
		role=obj.role
		windowClassName=obj.windowClassName
		states=obj.states
		controlID=obj.windowControlID
		if windowClassName=="REListBox20W" and role==controlTypes.ROLE_CHECKBOX:
			clsList.insert(0,REListBox20W_CheckBox)
		elif role==controlTypes.ROLE_LISTITEM and (windowClassName.startswith("REListBox") or windowClassName.startswith("NetUIHWND")):
			clsList.insert(0,AutoCompleteListItem)
		if role==controlTypes.ROLE_LISTITEM and windowClassName=="OUTEXVLB":
			clsList.insert(0, AddressBookEntry)
			return
		if (windowClassName=="SUPERGRID" and controlID==4704) or (windowClassName=="rctrl_renwnd32" and controlID==109):
			outlookVersion=self.outlookVersion
			if outlookVersion and outlookVersion<=9:
				clsList.insert(0, MessageList_pre2003)
			elif obj.event_objectID==winUser.OBJID_CLIENT and obj.event_childID==0:
				clsList.insert(0,SuperGridClient2010)

class REListBox20W_CheckBox(IAccessible):

	def script_checkbox(self, gesture):
		gesture.send()
		self.event_stateChange()

	__gestures={
		"kb:space":"checkbox",
	}

class SuperGridClient2010(IAccessible):

	def isDuplicateIAccessibleEvent(self,obj):
		return False

	def event_gainFocus(self):
		# #3834: UIA has a much better implementation for rows, so use it if available.
		if self.appModule.outlookVersion<14 or not UIAHandler.handler:
			return super(SuperGridClient2010,self).event_gainFocus()
		try:
			kwargs = {}
			UIA.kwargsFromSuper(kwargs, relation="focus")
			obj=UIA(**kwargs)
		except:
			log.debugWarning("Retrieving UIA focus failed", exc_info=True)
			return super(SuperGridClient2010,self).event_gainFocus()
		if not isinstance(obj,UIAGridRow):
			return super(SuperGridClient2010,self).event_gainFocus()
		obj.parent=self.parent
		eventHandler.executeEvent("gainFocus",obj)

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
			msg=self.nativeOm.ActiveExplorer().selection[0]
		except:
			msg=None
			pass
		if msg:
			self.curMessageItem=MessageItem(self,msg)
		super(MessageList_pre2003,self).event_gainFocus()
		if msg:
			eventHandler.executeEvent("gainFocus",self.curMessageItem)

	def script_moveByMessage(self,gesture):
		if hasattr(self,'curMessageItem'):
			oldEntryID=self.curMessageItem.msg.entryID
		else:
			oldEntryID=None
		gesture.send()
		try:
			msg=self.nativeOm.ActiveExplorer().selection[0]
		except:
			msg=None
			pass
		if msg:
			messageItem=MessageItem(self,msg)
			newEntryID=messageItem.msg.entryID
			if newEntryID!=oldEntryID:
				self.curMessageItem=messageItem
				eventHandler.executeEvent("gainFocus",messageItem)

	__moveByMessageGestures = (
		"kb:downArrow",
		"kb:upArrow",
		"kb:home",
		"kb:end",
		"kb:delete",
	)

	def initOverlayClass(self):
		for gesture in self.__moveByMessageGestures:
			self.bindGesture(gesture, "moveByMessage")

class MessageItem(Window):

	def __init__(self,windowHandle=None,parent=None,msg=None):
		if not parent or not msg:
			raise ArguementError("__init__ needs windowHandle, parent and msg arguments")
		if not windowHandle:
			windowHandle=parent.windowHandle
		self.msg=msg
		self.parent=parent
		Window.__init__(self,windowHandle=windowHandle)

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

class AddressBookEntry(IAccessible):

	def script_moveByEntry(self,gesture):
		gesture.send()
		eventHandler.queueEvent("nameChange",self)

	__moveByEntryGestures = (
		"kb:downArrow",
		"kb:upArrow",
		"kb:home",
		"kb:end",
		"kb:delete",
	)

	def initOverlayClass(self):
		for gesture in self.__moveByEntryGestures:
			self.bindGesture(gesture, "moveByEntry")

class AutoCompleteListItem(IAccessible):

	def event_stateChange(self):
		states=self.states
		focus=api.getFocusObject()
		if (focus.role==controlTypes.ROLE_EDITABLETEXT or focus.role==controlTypes.ROLE_BUTTON) and controlTypes.STATE_SELECTED in states and controlTypes.STATE_INVISIBLE not in states and controlTypes.STATE_UNAVAILABLE not in states and controlTypes.STATE_OFFSCREEN not in states:
			speech.cancelSpeech()
			ui.message(self.name)

class UIAGridRow(RowWithFakeNavigation,UIA):

	rowHeaderText=None
	columnHeaderText=None

	def _get_name(self):
		textList=[]
		if controlTypes.STATE_EXPANDED in self.states:
			textList.append(controlTypes.stateLabels[controlTypes.STATE_EXPANDED])
		elif controlTypes.STATE_COLLAPSED in self.states:
			textList.append(controlTypes.stateLabels[controlTypes.STATE_COLLAPSED])
		selection=None
		if self.appModule.nativeOm:
			try:
				selection=self.appModule.nativeOm.activeExplorer().selection.item(1)
			except COMError:
				pass
		if selection:
			try:
				unread=selection.unread
			except COMError:
				unread=False
			# Translators: when an email is unread
			if unread: textList.append(_("unread"))
			try:
				attachmentCount=selection.attachments.count
			except COMError:
				attachmentCount=0
			# Translators: when an email has attachments
			if attachmentCount>0: textList.append(_("has attachment"))
			try:
				importance=selection.importance
			except COMError:
				importance=1
			importanceLabel=importanceLabels.get(importance)
			if importanceLabel: textList.append(importanceLabel)
		if selection.messageClass=="IPM.Schedule.Meeting.Request":
			# Translators: the email is a meeting request
			textList.append(_("meeting request"))
		for child in self.children:
			if isinstance(child,UIAGridRow) or child.role==controlTypes.ROLE_GRAPHIC or not child.name:
				continue
			text=None
			if config.conf['documentFormatting']['reportTableHeaders'] and child.columnHeaderText:
				text=u"{header} {name}".format(header=child.columnHeaderText,name=child.name)
			else:
				text=child.name
			if text:
				text+=","
				textList.append(text)
		return " ".join(textList)

	value=None

	def _get_positionInfo(self):
		info=super(UIAGridRow,self).positionInfo
		if info is None: info={}
		UIAClassName=self.UIAElement.cachedClassName
		if UIAClassName=="ThreadHeader":
			info['level']=1
		elif UIAClassName=="ThreadItem" and isinstance(super(UIAGridRow,self).parent,UIAGridRow):
			info['level']=2
		return info

	def _get_role(self):
		role=super(UIAGridRow,self).role
		if role==controlTypes.ROLE_TREEVIEW:
			role=controlTypes.ROLE_TREEVIEWITEM
		return role

	def setFocus(self):
		super(UIAGridRow,self).setFocus()
		eventHandler.queueEvent("gainFocus",self)
