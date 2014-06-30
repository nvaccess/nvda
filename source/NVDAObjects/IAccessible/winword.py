#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2012 NVDA Contributors
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from comtypes import COMError
import comtypes.automation
import comtypes.client
import ctypes
import NVDAHelper
from logHandler import log
import oleacc
import winUser
import speech
import controlTypes
import textInfos
import eventHandler

from . import IAccessible
from NVDAObjects.window.winword import WordDocument 
from displayModel import EditableTextDisplayModelTextInfo
from NVDAObjects.window import DisplayModelEditableText

class SpellCheckErrorField(IAccessible,WordDocument):

	parentSDMCanOverrideName=False

	def _get_location(self):
		return super(IAccessible,self).location

	def _get_errorText(self):
		if self.WinwordVersion>=13:
			return self.value 		
		fields=EditableTextDisplayModelTextInfo(self,textInfos.POSITION_ALL).getTextWithFields()
		inBold=False
		textList=[]
		for field in fields:
			if isinstance(field,basestring):
				if inBold: textList.append(field)
			elif field.field:
				inBold=field.field.get('bold',False)
			if not inBold and len(textList)>0:
				break
		return u"".join(textList)

	def _get_documentWindowHandle(self):
		return NVDAHelper.localLib.findWindowWithClassInThread(self.windowThreadID,u"_WwG",True)

	def _get_WinwordWindowObject(self):
		hwnd=self.documentWindowHandle
		if hwnd:
			try:
				window=comtypes.client.dynamic.Dispatch(oleacc.AccessibleObjectFromWindow(hwnd,winUser.OBJID_NATIVEOM,interface=comtypes.automation.IDispatch))
			except (COMError, WindowsError):
				log.debugWarning("Could not get MS Word object model",exc_info=True)
				return None
			try:
				return window.application.activeWindow.activePane
			except COMError:
				log.debugWarning("can't use activeWindow, resorting to windows[1]",exc_info=True)
				return window.application.windows[1].activePane

	def _get_name(self):
		if self.WinwordVersion<13:
			return super(SpellCheckErrorField,self).description
		return super(SpellCheckErrorField,self).name

	description=None

	def reportFocus(self):
		errorText=self.errorText
		if self.WinwordVersion<13:		
			speech.speakObjectProperties(self,name=True,role=True)
		if errorText:
			speech.speakText(errorText)
			speech.speakSpelling(errorText)


class ProtectedDocumentPane(IAccessible):
	"""The pane that gets focus in case a document opens in protected mode in word
	This is mapped to the window class _WWB and role oleacc.ROLE_SYSTEM_CLIENT
	"""
	
	def event_gainFocus(self):
		"""On gaining focus, simply set the focus on a child of type word document. 
		This is just a container window.
		"""
		if eventHandler.isPendingEvents("gainFocus"):
			return
		document=next((x for x in self.children if isinstance(x,WordDocument)), None)  
		if document:
			curThreadID=ctypes.windll.kernel32.GetCurrentThreadId()
			ctypes.windll.user32.AttachThreadInput(curThreadID,document.windowThreadID,True)
			ctypes.windll.user32.SetFocus(document.windowHandle)
			ctypes.windll.user32.AttachThreadInput(curThreadID,document.windowThreadID,False)
			if not document.WinwordWindowObject.active:
				document.WinwordWindowObject.activate()
				
