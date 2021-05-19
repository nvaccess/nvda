# -*- coding: UTF-8 -*-
#appModules/miranda32.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2019 NV Access Limited, Aleksey Sadovoy, Peter Vágner, Joseph Lee, Bill Dengler
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import ui
import config
from ctypes import *
from ctypes.wintypes import *
import winKernel
from NVDAObjects.IAccessible import IAccessible, ContentGenericClient
from NVDAObjects.behaviors import Dialog
import appModuleHandler
import speech
import braille
import controlTypes
from scriptHandler import isScriptWaiting
import api
import mouseHandler
import oleacc
from keyboardHandler import KeyboardInputGesture
import watchdog

#contact list window messages
CLM_FIRST=0x1000    #this is the same as LVM_FIRST
CLM_LAST=0x1100

#messages, compare with equivalent TVM_s in the MSDN
CLM_ENSUREVISIBLE=CLM_FIRST+6    #wParam=hItem, lParam=partialOk
CLE_TOGGLE=-1
CLE_COLLAPSE=0
CLE_EXPAND=1
CLE_INVALID=0xFFFF
CLM_EXPAND=CLM_FIRST+7    #wParam=hItem, lParam=CLE_
CLM_FINDCONTACT=CLM_FIRST+8    #wParam=hContact, returns an hItem
CLM_FINDGROUP=CLM_FIRST+9    #wParam=hGroup, returns an hItem
CLM_GETBKCOLOR=CLM_FIRST+10   #returns a COLORREF
CLM_GETCHECKMARK=CLM_FIRST+11   #wParam=hItem, returns 1 or 0
CLM_GETCOUNT=CLM_FIRST+12   #returns the total number of items
CLM_GETEXPAND=CLM_FIRST+14   #wParam=hItem, returns a CLE_, CLE_INVALID if not a group
CLM_GETEXTRACOLUMNS=CLM_FIRST+15   #returns number of extra columns
CLM_GETEXTRAIMAGE=CLM_FIRST+16   #wParam=hItem, lParam=MAKELPARAM(iColumn (0 based),0), returns iImage or 0xFF
CLM_GETEXTRAIMAGELIST=CLM_FIRST+17   #returns HIMAGELIST
CLM_GETFONT=CLM_FIRST+18   #wParam=fontId, see clm_setfont. returns hFont.
CLM_GETINDENT=CLM_FIRST+19   #wParam=new group indent
CLM_GETISEARCHSTRING=CLM_FIRST+20   #lParam=(char*)pszStr, max 120 bytes, returns number of chars in string
MAXITEMTEXTLEN=120
CLM_GETITEMTEXT=CLM_FIRST+21   #wParam=hItem, lParam=(char*)pszStr, max 120 bytes
CLM_GETSELECTION=CLM_FIRST+23   #returns hItem
CLM_SELECTITEM=CLM_FIRST+26   #wParam=hItem
CLM_GETHIDEOFFLINEROOT=CLM_FIRST+40   #returns TRUE/FALSE
CLM_GETEXSTYLE=CLM_FIRST+44   #returns CLS_EX_ flags
CLM_GETLEFTMARGIN=CLM_FIRST+46   #returns count of pixels
CLCIT_INVALID=-1
CLCIT_GROUP=0
CLCIT_CONTACT=1
CLCIT_DIVIDER=2
CLCIT_INFO=3
CLM_GETITEMTYPE=CLM_FIRST+49	#wParam=hItem, returns a CLCIT_
CLGN_ROOT=0
CLGN_CHILD=1
CLGN_PARENT=2
CLGN_NEXT=3
CLGN_PREVIOUS=4
CLGN_NEXTCONTACT=5
CLGN_PREVIOUSCONTACT=6
CLGN_NEXTGROUP=7
CLGN_PREVIOUSGROUP=8
CLM_GETNEXTITEM=CLM_FIRST+50   #wParam=flag, lParam=hItem, returns an hItem
CLM_GETTEXTCOLOR=CLM_FIRST+51   #wParam=FONTID_, returns COLORREF
MAXSTATUSMSGLEN=256
CLM_GETSTATUSMSG=CLM_FIRST+105

#other constants
ANSILOGS=(1001,1006)
MESSAGEVIEWERS=(1001,1005,3011,5005)

class AppModule(appModuleHandler.AppModule):
	lastTextLengths={}
	lastMessages=[]
	# Must not be > 9.
	MessageHistoryLength=3

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.role == controlTypes.ROLE_WINDOW: 
			return
		windowClass = obj.windowClassName
		if windowClass == "CListControl":
			try:
				clsList.remove(ContentGenericClient)
			except ValueError:
				pass
			clsList.insert(0, mirandaIMContactList)
		elif windowClass in ("MButtonClass", "TSButtonClass", "CLCButtonClass"):
			clsList.insert(0, mirandaIMButton)
		elif windowClass == "Hyperlink":
			clsList.insert(0, mirandaIMHyperlink)
		elif isinstance(obj, IAccessible) and obj.IAccessibleRole == oleacc.ROLE_SYSTEM_PROPERTYPAGE:
			clsList.insert(0, MPropertyPage)
		elif isinstance(obj, IAccessible) and obj.IAccessibleRole == oleacc.ROLE_SYSTEM_SCROLLBAR and obj.windowControlID in MESSAGEVIEWERS:
			clsList.insert(0, MirandaMessageViewerScrollbar)
		elif windowClass == "ListBox" and obj.windowControlID == 0:
			clsList.insert(0, DuplicateFocusListBox)

	def event_NVDAObject_init(self,obj):
		if obj.windowClassName=="ColourPicker":
			obj.role=controlTypes.ROLE_COLORCHOOSER
		elif (obj.windowControlID in ANSILOGS) and (obj.windowClassName=="RichEdit20A"):
			obj._isWindowUnicode=False

	def script_readMessage(self,gesture):
		num=int(gesture.mainKeyName[-1])
		if len(self.lastMessages)>num-1:
			ui.message(self.lastMessages[num-1])
		else:
			# Translators: This is presented to inform the user that no instant message has been received.
			ui.message(_("No message yet"))
	# Translators: The description of an NVDA command to view one of the recent messages.
	script_readMessage.__doc__=_("Displays one of the recent messages")

	def __init__(self, *args, **kwargs):
		super(AppModule, self).__init__(*args, **kwargs)
		for n in range(1, self.MessageHistoryLength + 1):
			self.bindGesture("kb:NVDA+control+%s" % n, "readMessage")

class mirandaIMContactList(IAccessible):

	def _get_name(self):
		hItem=watchdog.cancellableSendMessage(self.windowHandle,CLM_GETSELECTION,0,0)
		internalBuf=winKernel.virtualAllocEx(self.processHandle,None,MAXITEMTEXTLEN,winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
		try:
			watchdog.cancellableSendMessage(self.windowHandle,CLM_GETITEMTEXT,hItem,internalBuf)
			buf=create_unicode_buffer(MAXITEMTEXTLEN)
			winKernel.readProcessMemory(self.processHandle,internalBuf,buf,MAXITEMTEXTLEN,None)
			text=buf.value
			statusMsgPtr=watchdog.cancellableSendMessage(self.windowHandle,CLM_GETSTATUSMSG,hItem,0)
			if statusMsgPtr>0:
				buf2=create_unicode_buffer(MAXSTATUSMSGLEN)
				winKernel.readProcessMemory(self.processHandle,statusMsgPtr,buf2,MAXSTATUSMSGLEN,None)
				text="%s %s"%(text,buf2.value)
		finally:
			winKernel.virtualFreeEx(self.processHandle,internalBuf,0,winKernel.MEM_RELEASE)
		return text

	def _get_role(self):
		hItem=watchdog.cancellableSendMessage(self.windowHandle,CLM_GETSELECTION,0,0)
		iType=watchdog.cancellableSendMessage(self.windowHandle,CLM_GETITEMTYPE,hItem,0)
		if iType==CLCIT_DIVIDER or iType==CLCIT_INVALID: #some clists treat invalid as divider
			return controlTypes.ROLE_SEPARATOR
		else:
			return controlTypes.ROLE_TREEVIEWITEM

	def _get_states(self):
		newStates=super(mirandaIMContactList,self)._get_states()
		hItem=watchdog.cancellableSendMessage(self.windowHandle,CLM_GETSELECTION,0,0)
		state=watchdog.cancellableSendMessage(self.windowHandle,CLM_GETEXPAND,hItem,0)
		if state==CLE_EXPAND:
			newStates.add(controlTypes.STATE_EXPANDED)
		elif state==CLE_COLLAPSE:
			newStates.add(controlTypes.STATE_COLLAPSED)
		return newStates

	def script_changeItem(self,gesture):
		gesture.send()
		if not isScriptWaiting():
			api.processPendingEvents()
			speech.speakObject(self, reason=controlTypes.OutputReason.FOCUS)
			braille.handler.handleGainFocus(self)

	__changeItemGestures = (
		"kb:downArrow",
		"kb:upArrow",
		"kb:leftArrow",
		"kb:rightArrow",
		"kb:home",
		"kb:end",
		"kb:pageUp",
		"kb:pageDown",
	)

	def initOverlayClass(self):
		for gesture in self.__changeItemGestures:
			self.bindGesture(gesture, "changeItem")

class mirandaIMButton(IAccessible):

	def _get_name(self):
		api.moveMouseToNVDAObject(self)
		return super(mirandaIMButton,self)._get_name()

	def _get_role(self):
		return controlTypes.ROLE_BUTTON

	def getActionName(self):
		if controlTypes.STATE_FOCUSED not in self.states:
			return
		return "Click"

	def doAction(self):
		if controlTypes.STATE_FOCUSED not in self.states:
			return
		KeyboardInputGesture.fromName("space").send()

	def script_doDefaultAction(self,gesture):
		self.doAction()

	def initOverlayClass(self):
		self.bindGesture("kb:enter", "doDefaultAction")

class mirandaIMHyperlink(mirandaIMButton):

	def _get_role(self):
		return controlTypes.ROLE_LINK

class MPropertyPage(Dialog,IAccessible):

	def _get_name(self):
		name=super(MPropertyPage,self)._get_name()
		if not name:
			try:
				tc=self.parent.next.firstChild
			except AttributeError:
				tc=None
			if tc and tc.role==controlTypes.ROLE_TABCONTROL:
				children=tc.children
				for index in range(len(children)):
					if (children[index].role==controlTypes.ROLE_TAB) and (controlTypes.STATE_SELECTED in children[index].states):
						name=children[index].name
						break
		return name


class MirandaMessageViewerScrollbar(IAccessible):
	def event_valueChange(self):
		curTextLength=len(self.windowText)
		if self.windowHandle not in self.appModule.lastTextLengths:
			self.appModule.lastTextLengths[self.windowHandle]=curTextLength
		elif self.appModule.lastTextLengths[self.windowHandle]<curTextLength:
			message=self.windowText[self.appModule.lastTextLengths[self.windowHandle]:]
			self.appModule.lastMessages.insert(0,message)
			self.appModule.lastMessages=self.appModule.lastMessages[:self.appModule.MessageHistoryLength]
			if config.conf["presentation"]["reportDynamicContentChanges"]:
				ui.message(message)
			self.appModule.lastTextLengths[self.windowHandle]=curTextLength
		super(MirandaMessageViewerScrollbar,self).event_valueChange()

class DuplicateFocusListBox(IAccessible):
	"""A list box which annoyingly fires focus events every second, even when a menu is open.
	"""

	def _get_shouldAllowIAccessibleFocusEvent(self):
		# Stop annoying duplicate focus events, which are fired even if a menu is open.
		focus = api.getFocusObject()
		focusRole = focus.role
		focusStates = focus.states
		if (self == focus or
			(focusRole == controlTypes.ROLE_MENUITEM and controlTypes.STATE_FOCUSED in focusStates) or
			(focusRole == controlTypes.ROLE_POPUPMENU and controlTypes.STATE_INVISIBLE not in focusStates)
		):
			return False
		return super(DuplicateFocusListBox, self).shouldAllowIAccessibleFocusEvent
