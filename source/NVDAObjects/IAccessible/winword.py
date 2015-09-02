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
from NVDAObjects.window.winword import WordDocument, WordDocument_WwN
from displayModel import EditableTextDisplayModelTextInfo
from NVDAObjects.window import DisplayModelEditableText

class SpellCheckErrorField(IAccessible,WordDocument_WwN):

	parentSDMCanOverrideName=False
	ignoreFormatting=True

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

	def _get_name(self):
		if self.WinwordVersion<13:
			return super(SpellCheckErrorField,self).description
		return super(SpellCheckErrorField,self).name

	description=None

	def reportFocus(self):
		errorText=self.errorText
		speech.speakObjectProperties(self,name=True,role=True)
		if errorText:
			speech.speakText(errorText)
			speech.speakSpelling(errorText)

	def isDuplicateIAccessibleEvent(self,obj):
		""" We return false here because the spell	checker window raises the focus event every time the value changes instead of the value changed event 
		regardless of the fact that this window already has the focus."""
		return False

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
				
