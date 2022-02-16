# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2021 NV Access Limited, Yogesh Kumar, Manish Agrawal, Joseph Lee, Davy Kager,
# Babbage B.V., Leonard de Ruijter
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from comtypes import COMError
from comtypes.hresult import S_OK
import comtypes.client
import comtypes.automation
import ctypes
from hwPortUtils import SYSTEMTIME
import scriptHandler
from scriptHandler import script
import winKernel
import comHelper
import NVDAHelper
import winUser
from logHandler import log
import textInfos
import braille
import appModuleHandler
import eventHandler
import UIAHandler
from UIAHandler.utils import createUIAMultiPropertyCondition
import api
import controlTypes
import config
import speech
import ui
from NVDAObjects.IAccessible import IAccessible
from NVDAObjects.window import Window
from NVDAObjects.window.winword import WordDocument as BaseWordDocument
from NVDAObjects.IAccessible.winword import WordDocument, WordDocumentTreeInterceptor, BrowseModeWordDocumentTextInfo, WordDocumentTextInfo
from NVDAObjects.IAccessible.MSHTML import MSHTML
from NVDAObjects.behaviors import RowWithFakeNavigation, Dialog
from NVDAObjects.UIA import UIA
from NVDAObjects.UIA.wordDocument import WordDocument as UIAWordDocument
import languageHandler


PR_LAST_VERB_EXECUTED=0x10810003
VERB_REPLYTOSENDER=102
VERB_REPLYTOALL=103
VERB_FORWARD=104
executedVerbLabels={
	# Translators: the last action taken on an Outlook mail message
	VERB_REPLYTOSENDER:_("replied"),
	# Translators: the last action taken on an Outlook mail message
	VERB_REPLYTOALL:_("replied all"),
	# Translators: the last action taken on an Outlook mail message
	VERB_FORWARD:_("forwarded"),
}


#: The number of seconds in a day, used to make all day appointments and selections less verbose.
#: Type: float
SECONDS_PER_DAY = 86400.0

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

	def __init__(self,*args,**kwargs):
		super(AppModule,self).__init__(*args,**kwargs)
		# Explicitly allow gainFocus events for the window class that hosts the active Outlook DatePicker cell
		# This object gets focus but its window does not conform to our GUI thread info window checks
		eventHandler.requestEvents("gainFocus",processId=self.processID,windowClassName="rctrl_renwnd32")

	_hasTriedoutlookAppSwitch=False

	def _registerCOMWithFocusJuggle(self):
		import wx
		import gui
		# Translators: The title for the dialog shown while Microsoft Outlook initializes.
		d=wx.Dialog(None,title=_("Waiting for Outlook..."))
		d.CentreOnScreen()
		gui.mainFrame.prePopup()
		d.Show()
		self._hasTriedoutlookAppSwitch=True
		#Make sure NVDA detects and reports focus on the waiting dialog
		api.processPendingEvents()
		try:
			comtypes.client.PumpEvents(1)
		except WindowsError:
			log.debugWarning("Error while pumping com events", exc_info=True)
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
		windowClass=winUser.getClassName(hwnd)
		# #2816: Outlook versions before 2016 auto complete does not fire enough UIA events, IAccessible is better.
		if windowClass=="NetUIHWND":
			parentHwnd=winUser.getAncestor(hwnd,winUser.GA_ROOT)
			if winUser.getClassName(parentHwnd)=="Net UI Tool Window":
				versionMajor=int(self.productVersion.split('.')[0])
				if versionMajor<16:
					return True
		if windowClass in ("WeekViewWnd","DayViewWnd"):
			return True
		return False

	def event_NVDAObject_init(self,obj):
		role=obj.role
		windowClassName=obj.windowClassName
		controlID=obj.windowControlID
		#The control showing plain text messages has very stuffed parents
		#Use the grandparent window as its parent
		if role==controlTypes.Role.EDITABLETEXT and windowClassName=="RichEdit20W" and controlID==8224:
			obj.parent=Window._get_parent(Window._get_parent(obj))
		#The control that shows HTML messages has stuffed parents. Use the control's parent window as its parent
		if windowClassName=="Internet Explorer_Server" and role==controlTypes.Role.PANE and not isinstance(obj,MSHTML):
			obj.parent=Window._get_parent(Window._get_parent(obj))
		if role in (controlTypes.Role.MENUBAR,controlTypes.Role.MENUITEM):
			obj.description=None
		if role in (controlTypes.Role.TREEVIEW,controlTypes.Role.TREEVIEWITEM,controlTypes.Role.LIST,controlTypes.Role.LISTITEM):
			obj.shouldAllowIAccessibleFocusEvent=True
		if ((windowClassName=="SUPERGRID" and controlID==4704) or (windowClassName=="rctrl_renwnd32" and controlID==109)) and role==controlTypes.Role.UNKNOWN:
			obj.role=controlTypes.Role.LISTITEM

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if UIAWordDocument in clsList:
			# Overlay class for Outlook message viewer when UI Automation for MS Word is enabled.
			clsList.insert(0,OutlookUIAWordDocument)
		if isinstance(obj,UIA) and obj.UIAElement.cachedClassName in ("LeafRow","ThreadItem","ThreadHeader"):
			clsList.insert(0,UIAGridRow)
		role=obj.role
		windowClassName=obj.windowClassName
		# AutoComplete listItems.
		# This class is abstract enough to  support both UIA and MSAA
		if role==controlTypes.Role.LISTITEM and (windowClassName.startswith("REListBox") or windowClassName.startswith("NetUIHWND")):
			clsList.insert(0,AutoCompleteListItem)
		#  all   remaining classes are IAccessible
		if not isinstance(obj,IAccessible):
			return
		# Outlook uses dialogs for many forms such as appointment / meeting creation. In these cases, there is no sane dialog caption that can be calculated as the dialog inly contains controls.
		# Therefore remove the Dialog behavior for these imbedded dialog forms so as to not announce junk as the caption
		if Dialog in clsList:
			parentWindow=winUser.getAncestor(obj.windowHandle,winUser.GA_PARENT)
			if parentWindow and winUser.getClassName(parentWindow)=="AfxWndW":
				clsList.remove(Dialog)
		if WordDocument in clsList:
			clsList.insert(0,OutlookWordDocument)
		states=obj.states
		controlID=obj.windowControlID
		# Support the date picker in Outlook Meeting / Appointment creation forms 
		if controlID==4352 and role==controlTypes.Role.BUTTON:
			clsList.insert(0,DatePickerButton)
		elif role==controlTypes.Role.TABLECELL and windowClassName=="rctrl_renwnd32":
			clsList.insert(0,DatePickerCell)
		elif windowClassName=="REListBox20W" and role==controlTypes.Role.CHECKBOX:
			clsList.insert(0,REListBox20W_CheckBox)
		if role==controlTypes.Role.LISTITEM and windowClassName=="OUTEXVLB":
			clsList.insert(0, AddressBookEntry)
			return
		if (windowClassName=="SUPERGRID" and controlID==4704) or (windowClassName=="rctrl_renwnd32" and controlID==109):
			outlookVersion=self.outlookVersion
			if (
				outlookVersion
				and outlookVersion > 9
				and obj.event_objectID==winUser.OBJID_CLIENT
				and obj.event_childID==0
			):
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
			UIA.kwargsFromSuper(kwargs, relation="focus", ignoreNonNativeElementsWithFocus=False)
			obj = UIA(**kwargs)
		except Exception:
			log.error("Retrieving UIA focus failed", exc_info=True)
			return super(SuperGridClient2010,self).event_gainFocus()
		if not isinstance(obj,UIAGridRow):
			return super(SuperGridClient2010,self).event_gainFocus()
		obj.parent=self.parent
		eventHandler.executeEvent("gainFocus",obj)


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

class AutoCompleteListItem(Window):

	def event_stateChange(self):
		states=self.states
		focus=api.getFocusObject()
		if (focus.role==controlTypes.Role.EDITABLETEXT or focus.role==controlTypes.Role.BUTTON) and controlTypes.State.SELECTED in states and controlTypes.State.INVISIBLE not in states and controlTypes.State.UNAVAILABLE not in states and controlTypes.State.OFFSCREEN not in states:
			speech.cancelSpeech()
			text=self.name
			# Some newer versions of Outlook don't put the contact as the name of the listItem, rather it is on the parent 
			if not text:
				text=self.parent.name
			ui.message(text)

class CalendarView(IAccessible):
	"""Support for announcing time slots and appointments in Outlook Calendar.
	"""

	_lastStartDate=None

	def _generateTimeRangeText(self,startTime,endTime):
		startText=winKernel.GetTimeFormatEx(winKernel.LOCALE_NAME_USER_DEFAULT, winKernel.TIME_NOSECONDS, startTime, None)
		endText=winKernel.GetTimeFormatEx(winKernel.LOCALE_NAME_USER_DEFAULT, winKernel.TIME_NOSECONDS, endTime, None)
		startDate=startTime.date()
		endDate=endTime.date()
		if not CalendarView._lastStartDate or startDate!=CalendarView._lastStartDate or endDate!=startDate: 
			startDateText=winKernel.GetDateFormatEx(winKernel.LOCALE_NAME_USER_DEFAULT, winKernel.DATE_LONGDATE, startTime, None)
			startText="%s %s"%(startDateText,startText)
		CalendarView._lastStartDate=startDate
		if endDate!=startDate:
			if ((startTime.hour, startTime.minute, startTime.second) == (0, 0, 0) and
				(endDate - startDate).total_seconds()==SECONDS_PER_DAY
			):
				# Translators: a message reporting the date of a all day Outlook calendar entry
				return _("{date} (all day)").format(date=startDateText)
			endText="%s %s"%(winKernel.GetDateFormatEx(winKernel.LOCALE_NAME_USER_DEFAULT, winKernel.DATE_LONGDATE, endTime, None),endText)
		# Translators: a message reporting the time range (i.e. start time to end time) of an Outlook calendar entry
		return _("{startTime} to {endTime}").format(startTime=startText,endTime=endText)

	@staticmethod
	def _generateCategoriesText(appointment):
		categories = appointment.Categories
		if not categories:
			return None
		# Categories is a delimited string of category names that have been assigned to an Outlook item.
		# This property uses the user locale's list separator to separate entries.
		# See also https://docs.microsoft.com/en-us/office/vba/api/outlook.appointmentitem.categories
		bufLength = 4
		separatorBuf = ctypes.create_unicode_buffer(bufLength)
		if ctypes.windll.kernel32.GetLocaleInfoW(
			languageHandler.LOCALE_USER_DEFAULT,
			languageHandler.LOCALE.SLIST,
			separatorBuf,
			bufLength
		) == 0:
			raise ctypes.WinError()

		# Translators: Part of a message reported when on a calendar appointment with one or more categories
		# in Microsoft Outlook.
		return _("categories {categories}").format(categories=categories)

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
				# Translators: A message reported when on a calendar appointment with category in Microsoft Outlook
				message = _("Appointment {subject}, {time}").format(subject=p.subject, time=t)
				try:
					categoriesText = self._generateCategoriesText(p)
				except COMError:
					categoriesText = None
				if categoriesText is not None:
					message = f"{message}, {categoriesText}"
				ui.message(message)
			else:
				v=e.currentView
				try:
					selectedStartTime=v.selectedStartTime
					selectedEndTime=v.selectedEndTime
				except COMError:
					return super(CalendarView,self).reportFocus()
				timeSlotText=self._generateTimeRangeText(selectedStartTime,selectedEndTime)
				startDate = winKernel.GetDateFormatEx(
					winKernel.LOCALE_NAME_USER_DEFAULT,
					winKernel.DATE_LONGDATE,
					selectedStartTime,
					None
				)
				startTime = winKernel.GetTimeFormatEx(
					winKernel.LOCALE_NAME_USER_DEFAULT,
					winKernel.TIME_NOSECONDS,
					selectedStartTime,
					None
				)
				endDate = winKernel.GetDateFormatEx(
					winKernel.LOCALE_NAME_USER_DEFAULT,
					winKernel.DATE_LONGDATE,
					selectedEndTime,
					None
				)
				endTime = winKernel.GetTimeFormatEx(
					winKernel.LOCALE_NAME_USER_DEFAULT,
					winKernel.TIME_NOSECONDS,
					selectedEndTime,
					None
				)
				query = f'[Start] < "{endDate} {endTime}" And [End] > "{startDate} {startTime}"'
				i=e.currentFolder.items
				i.sort('[Start]')
				i.IncludeRecurrences =True
				if i.find(query):
					# Translators: a message when the current time slot on an Outlook Calendar has an appointment
					timeSlotText=_("Has appointment")+" "+timeSlotText
				ui.message(timeSlotText)
		else:
			self.event_valueChange()

class UIAGridRow(RowWithFakeNavigation,UIA):

	rowHeaderText=None
	columnHeaderText=None

	def _get_name(self):
		textList=[]
		if controlTypes.State.EXPANDED in self.states:
			textList.append(controlTypes.State.EXPANDED.displayString)
		elif controlTypes.State.COLLAPSED in self.states:
			textList.append(controlTypes.State.COLLAPSED.displayString)
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
				mapiObject=selection.mapiObject
			except COMError:
				mapiObject=None
			if mapiObject:
				v=comtypes.automation.VARIANT()
				res=NVDAHelper.localLib.nvdaInProcUtils_outlook_getMAPIProp(
					self.appModule.helperLocalBindingHandle,
					self.windowThreadID,
					mapiObject,
					PR_LAST_VERB_EXECUTED,
					ctypes.byref(v)
				)
				if res==S_OK:
					verbLabel=executedVerbLabels.get(v.value,None)
					if verbLabel:
						textList.append(verbLabel)
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
		# We must filter the children for just text and image elements otherwise getCachedChildren fails completely in conversation view.
		childrenCacheRequest.treeFilter=createUIAMultiPropertyCondition({UIAHandler.UIA_ControlTypePropertyId:[UIAHandler.UIA_TextControlTypeId,UIAHandler.UIA_ImageControlTypeId]})
		cachedChildren=self.UIAElement.buildUpdatedCache(childrenCacheRequest).getCachedChildren()
		if not cachedChildren:
			# There are no children
			# This is unexpected here.
			log.debugWarning("Unable to get relevant children for UIAGridRow", stack_info=True)
			return super(UIAGridRow, self).name
		for index in range(cachedChildren.length):
			e=cachedChildren.getElement(index)
			UIAControlType=e.cachedControlType
			UIAClassName=e.cachedClassName
			# We only want to include particular children.
			# We only include the flagField if the object model's flagIcon or flagStatus is set.
			# Stops us from reporting "unflagged" which is too verbose.
			if selection and UIAClassName=="FlagField":
				try:
					if not selection.flagIcon and not selection.flagStatus: continue
				except COMError:
					continue
			# the category field should only be reported if the objectModel's categories property actually contains a valid string.
			# Stops us from reporting "no categories" which is too verbose.
			elif selection and UIAClassName=="CategoryField":
				try:
					if not selection.categories: continue
				except COMError:
					continue
			# And we don't care about anything else that is not a text element. 
			elif UIAControlType!=UIAHandler.UIA_TextControlTypeId:
				continue
			name=e.cachedName
			columnHeaderTextList=[]
			if name and config.conf['documentFormatting']['reportTableHeaders']:
				columnHeaderItems=e.getCachedPropertyValueEx(UIAHandler.UIA_TableItemColumnHeaderItemsPropertyId,True)
			else:
				columnHeaderItems=None
			if columnHeaderItems:
				columnHeaderItems=columnHeaderItems.QueryInterface(UIAHandler.IUIAutomationElementArray)
				for index in range(columnHeaderItems.length):
					columnHeaderItem=columnHeaderItems.getElement(index)
					columnHeaderTextList.append(columnHeaderItem.currentName)
			columnHeaderText=" ".join(columnHeaderTextList)
			if columnHeaderText:
				text=u"{header} {name}".format(header=columnHeaderText,name=name)
			else:
				text=name
			if text:
				if UIAClassName=="FlagField":
					textList.insert(0,text)
				else:
					text+=u","
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
		if role==controlTypes.Role.TREEVIEW:
			role=controlTypes.Role.TREEVIEWITEM
		elif role==controlTypes.Role.DATAITEM:
			role=controlTypes.Role.LISTITEM
		return role

	def setFocus(self):
		super(UIAGridRow,self).setFocus()
		eventHandler.queueEvent("gainFocus",self)

class MailViewerTextInfoForTreeInterceptor(WordDocumentTextInfo):

	def _get_shouldIncludeLayoutTables(self):
		return config.conf['documentFormatting']['includeLayoutTables']

class MailViewerTreeInterceptorTextInfo(BrowseModeWordDocumentTextInfo):
	InnerTextInfoClass=MailViewerTextInfoForTreeInterceptor

class MailViewerTreeInterceptor(WordDocumentTreeInterceptor):
	"""A BrowseMode treeInterceptor specifically for readonly emails, where tab and shift+tab are safe and we know will not edit the document."""

	TextInfo=MailViewerTreeInterceptorTextInfo

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
			speech.speakTextInfo(info, reason=controlTypes.OutputReason.FOCUS)
		braille.handler.handleCaretMove(self)

	__gestures={
		"kb:tab":"tab",
		"kb:shift+tab":"tab",
	}


class BaseOutlookWordDocument(BaseWordDocument):

	@script(gestures=["kb:tab", "kb:shift+tab"])
	def script_tab(self, gesture):
		bookmark = self.makeTextInfo(textInfos.POSITION_SELECTION).bookmark
		gesture.send()
		info, caretMoved = self._hasCaretMoved(bookmark)
		if not caretMoved:
			return
		self.reportTab()


class OutlookWordDocument(WordDocument, BaseOutlookWordDocument):

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
		return controlTypes.Role.DOCUMENT if self.isReadonlyViewer else super(OutlookWordDocument,self).role

	ignoreEditorRevisions=True
	ignorePageNumbers=True # This includes page sections, and page columns. None of which are appropriate for outlook.


class OutlookUIAWordDocument(UIAWordDocument, BaseOutlookWordDocument):
	""" Forces browse mode to be used on the UI Automation Outlook message viewer if the message is being read)."""

	def _get_isReadonlyViewer(self):
		return controlTypes.State.READONLY in self.states

	def _get_shouldCreateTreeInterceptor(self):
		return self.isReadonlyViewer

class DatePickerButton(IAccessible):
	# Value is a duplicate of name so get rid of it
	value=None

class DatePickerCell(IAccessible):
	# Value is a duplicate of name so get rid of it
	value=None

	# Focus events are always on this object with the exact same event parameters
	# Therefore we cannot safely filter out duplicates
	def isDuplicateIAccessibleEvent(self,obj):
		return False
