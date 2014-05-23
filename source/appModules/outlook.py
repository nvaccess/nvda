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
import appModuleHandler
import eventHandler
import api
import controlTypes
import speech
import ui
from NVDAObjects.IAccessible import IAccessible
from NVDAObjects.window import Window
from NVDAObjects.IAccessible.MSHTML import MSHTML

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
		# Translators: A title for a dialog shown while Microsoft PowerPoint initializes
		d=wx.Dialog(None,title=_("Waiting for Outlook..."))
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
		return "%s to %s"%(startText,endText)

	def isDuplicateIAccessibleEvent(self,obj):
		return False

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
				speech.speakMessage("Appointment %s, %s"%(p.subject,t))
			else:
				v=e.currentView
				selectedStartTime=v.selectedStartTime
				selectedEndTime=v.selectedEndTime
				timeSlotText=self._generateTimeRangeText(selectedStartTime,selectedEndTime)
				startLimit="%s %s"%(winKernel.GetDateFormat(winKernel.LOCALE_USER_DEFAULT, winKernel.DATE_LONGDATE, selectedStartTime, None),winKernel.GetTimeFormat(winKernel.LOCALE_USER_DEFAULT, winKernel.TIME_NOSECONDS, selectedStartTime, None))
				endLimit="%s %s"%(winKernel.GetDateFormat(winKernel.LOCALE_USER_DEFAULT, winKernel.DATE_LONGDATE, selectedEndTime, None),winKernel.GetTimeFormat(winKernel.LOCALE_USER_DEFAULT, winKernel.TIME_NOSECONDS, selectedEndTime, None))
				query='[Start] < "{endLimit}" And [End] > "{startLimit}"'.format(startLimit=startLimit,endLimit=endLimit)
				i=e.currentFolder.items
				i.sort('[Start]')
				i.IncludeRecurrences =True
				if i.find(query):
					timeSlotText="has appointment "+timeSlotText
				speech.speakMessage(timeSlotText)
		else:
			self.event_valueChange()
