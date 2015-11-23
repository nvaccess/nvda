#appModules/outlook.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2014 NVDA Contributors <http://www.nvaccess.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from comtypes import COMError
import comtypes.client
from hwPortUtils import SYSTEMTIME
import scriptHandler
import winKernel
import comHelper
import winUser
from logHandler import log
import textInfos
import braille
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
from NVDAObjects.window.winword import WordDocument, WordDocumentTreeInterceptor
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

	_hasTriedoutlookAppSwitch=False

	def _registerCOMWithFocusJuggle(self):
		import wx
		import gui
		# Translators: The title for the dialog shown while Microsoft Outlook initializes.
		d=wx.Dialog(None,title=_("Waiting for Outlook..."))
		d.Center(wx.BOTH | wx.CENTER_ON_SCREEN)
		gui.mainFrame.prePopup()
		d.Show()
		self._hasTriedoutlookAppSwitch=True
		#Make sure NVDA detects and reports focus on the waiting dialog
		api.processPendingEvents()
		comtypes.client.PumpEvents(1)
		d.Destroy()
		gui.mainFrame.postPopup()

	def _get_nativeOm(self):
		try:
			nativeOm=comHelper.getActiveObject("outlook.application",dynamic=True)
		except (COMError,WindowsError,RuntimeError):
			if self._hasTriedoutlookAppSwitch:
				log.error("Failed to get native object model",exc_info=True)
			nativeOm=None
		if not nativeOm and not self._hasTriedoutlookAppSwitch:
			self._registerCOMWithFocusJuggle()
			return None
		self.nativeOm=nativeOm
		return self.nativeOm

	def _get_outlookVersion(self):
		nativeOm=self.nativeOm
		if nativeOm:
			outlookVersion=int(nativeOm.version.split('.')[0])
		else:
			outlookVersion=0
		return outlookVersion

	def isBadUIAWindow(self,hwnd):
		if winUser.getClassName(hwnd) in ("WeekViewWnd","DayViewWnd"):
			return True
		return False

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
		if WordDocument in clsList:
			clsList.insert(0,OutlookWordDocument)
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
		if (windowClassName == "AfxWndW" and controlID==109) or (windowClassName in ("WeekViewWnd","DayViewWnd")):
			clsList.insert(0,CalendarView)

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

	def _get_shouldAllowIAccessibleFocusEvent(self):
		# The window must really have focus.
		# Outlook can sometimes fire invalid focus events when showing daily tasks within the calendar.
		if winUser.getGUIThreadInfo(self.windowThreadID).hwndFocus!=self.windowHandle:
			return False
		return super(SuperGridClient2010,self).shouldAllowIAccessibleFocusEvent

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

class CalendarView(IAccessible):
	"""Support for announcing time slots and appointments in Outlook Calendar.
	"""

	_lastStartDate=None

	def _generateTimeRangeText(self,startTime,endTime):
		startText=winKernel.GetTimeFormat(winKernel.LOCALE_USER_DEFAULT, winKernel.TIME_NOSECONDS, startTime, None)
		endText=winKernel.GetTimeFormat(winKernel.LOCALE_USER_DEFAULT, winKernel.TIME_NOSECONDS, endTime, None)
		startDate=startTime.date()
		endDate=endTime.date()
		if not CalendarView._lastStartDate or startDate!=CalendarView._lastStartDate or endDate!=startDate: 
			startText="%s %s"%(winKernel.GetDateFormat(winKernel.LOCALE_USER_DEFAULT, winKernel.DATE_LONGDATE, startTime, None),startText)
		if endDate!=startDate:
			endText="%s %s"%(winKernel.GetDateFormat(winKernel.LOCALE_USER_DEFAULT, winKernel.DATE_LONGDATE, endTime, None),endText)
		CalendarView._lastStartDate=startDate
		# Translators: a message reporting the time range (i.e. start time to end time) of an Outlook calendar entry
		return _("{startTime} to {endTime}").format(startTime=startText,endTime=endText)

	def isDuplicateIAccessibleEvent(self,obj):
		return False

	def event_nameChange(self):
		pass

	def event_stateChange(self):
		pass

	def reportFocus(self):
		if self.appModule.outlookVersion>=13 and self.appModule.nativeOm:
			e=self.appModule.nativeOm.activeExplorer()
			s=e.selection
			if s.count>0:
				p=s.item(1)
				try:
					start=p.start
					end=p.end
				except COMError:
					return super(CalendarView,self).reportFocus()
				t=self._generateTimeRangeText(start,end)
				# Translators: A message reported when on a calendar appointment in Microsoft Outlook
				speech.speakMessage(_("Appointment {subject}, {time}").format(subject=p.subject,time=t))
			else:
				v=e.currentView
				try:
					selectedStartTime=v.selectedStartTime
					selectedEndTime=v.selectedEndTime
				except COMError:
					return super(CalendarView,self).reportFocus()
				timeSlotText=self._generateTimeRangeText(selectedStartTime,selectedEndTime)
				startLimit=u"%s %s"%(winKernel.GetDateFormat(winKernel.LOCALE_USER_DEFAULT, winKernel.DATE_LONGDATE, selectedStartTime, None),winKernel.GetTimeFormat(winKernel.LOCALE_USER_DEFAULT, winKernel.TIME_NOSECONDS, selectedStartTime, None))
				endLimit=u"%s %s"%(winKernel.GetDateFormat(winKernel.LOCALE_USER_DEFAULT, winKernel.DATE_LONGDATE, selectedEndTime, None),winKernel.GetTimeFormat(winKernel.LOCALE_USER_DEFAULT, winKernel.TIME_NOSECONDS, selectedEndTime, None))
				query=u'[Start] < "{endLimit}" And [End] > "{startLimit}"'.format(startLimit=startLimit,endLimit=endLimit)
				i=e.currentFolder.items
				i.sort('[Start]')
				i.IncludeRecurrences =True
				if i.find(query):
					# Translators: a message when the current time slot on an Outlook Calendar has an appointment
					timeSlotText=_("has appointment")+" "+timeSlotText
				speech.speakMessage(timeSlotText)
		else:
			self.event_valueChange()

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
			try:
				messageClass=selection.messageClass
			except COMError:
				messageClass=None
			if messageClass=="IPM.Schedule.Meeting.Request":
				# Translators: the email is a meeting request
				textList.append(_("meeting request"))
		childrenCacheRequest=UIAHandler.handler.baseCacheRequest.clone()
		childrenCacheRequest.addProperty(UIAHandler.UIA_NamePropertyId)
		childrenCacheRequest.addProperty(UIAHandler.UIA_TableItemColumnHeaderItemsPropertyId)
		childrenCacheRequest.TreeScope=UIAHandler.TreeScope_Children
		childrenCacheRequest.treeFilter=UIAHandler.handler.clientObject.createPropertyCondition(UIAHandler.UIA_ControlTypePropertyId,UIAHandler.UIA_TextControlTypeId)
		cachedChildren=self.UIAElement.buildUpdatedCache(childrenCacheRequest).getCachedChildren()
		for index in xrange(cachedChildren.length):
			e=cachedChildren.getElement(index)
			name=e.cachedName
			columnHeaderTextList=[]
			if name and config.conf['documentFormatting']['reportTableHeaders']:
				columnHeaderItems=e.getCachedPropertyValueEx(UIAHandler.UIA_TableItemColumnHeaderItemsPropertyId,True)
			else:
				columnHeaderItems=None
			if columnHeaderItems:
				columnHeaderItems=columnHeaderItems.QueryInterface(UIAHandler.IUIAutomationElementArray)
				for index in xrange(columnHeaderItems.length):
					columnHeaderItem=columnHeaderItems.getElement(index)
					columnHeaderTextList.append(columnHeaderItem.currentName)
			columnHeaderText=" ".join(columnHeaderTextList)
			if columnHeaderText:
				text=u"{header} {name}".format(header=columnHeaderText,name=name)
			else:
				text=name
			if text:
				text=text+u","
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
		elif role==controlTypes.ROLE_DATAITEM:
			role=controlTypes.ROLE_LISTITEM
		return role

	def setFocus(self):
		super(UIAGridRow,self).setFocus()
		eventHandler.queueEvent("gainFocus",self)

class MailViewerTreeInterceptor(WordDocumentTreeInterceptor):
	"""A BrowseMode treeInterceptor specifically for readonly emails, where tab and shift+tab are safe and we know will not edit the document."""

	def script_tab(self,gesture):
		bookmark=self.rootNVDAObject.makeTextInfo(textInfos.POSITION_SELECTION).bookmark
		gesture.send()
		info,caretMoved=self.rootNVDAObject._hasCaretMoved(bookmark)
		if not caretMoved:
			return
		info=self.makeTextInfo(textInfos.POSITION_SELECTION)
		inTable=info._rangeObj.tables.count>0
		isCollapsed=info.isCollapsed
		if inTable and isCollapsed:
			info.expand(textInfos.UNIT_CELL)
			isCollapsed=False
		if not isCollapsed:
			speech.speakTextInfo(info,reason=controlTypes.REASON_FOCUS)
		braille.handler.handleCaretMove(self)

	__gestures={
		"kb:tab":"tab",
		"kb:shift+tab":"tab",
	}

class OutlookWordDocument(WordDocument):

	def _get_isReadonlyViewer(self):
		# #2975: The only way we know an email is read-only is if the underlying email has been sent.
		try:
			return self.appModule.nativeOm.activeInspector().currentItem.sent
		except (COMError,NameError,AttributeError):
			return False

	def _get_treeInterceptorClass(self):
		if self.isReadonlyViewer:
			return MailViewerTreeInterceptor
		return super(OutlookWordDocument,self).treeInterceptorClass

	def _get_shouldCreateTreeInterceptor(self):
		return self.isReadonlyViewer

	def _get_role(self):
		return controlTypes.ROLE_DOCUMENT if self.isReadonlyViewer else super(OutlookWordDocument,self).role
