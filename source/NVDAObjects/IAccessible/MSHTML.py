#NVDAObjects/MSHTML.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import time
import ctypes
import comtypesClient
import comtypes.automation
import pythoncom
import win32com.client
import debug
import winUser
import IAccessibleHandler
from keyUtils import key, sendKey
import api
import text
import speech
import controlTypes
from . import IAccessible

IServiceProvider=comtypesClient.GetModule('lib/Servprov.tlb').IServiceProvider

IID_IHTMLElement=comtypes.GUID('{3050F1FF-98B5-11CF-BB82-00AA00BDCE0B}')
IID_DispHTMLGenericElement=comtypes.GUID('{3050F563-98B5-11CF-BB82-00AA00BDCE0B}')
IID_DispHTMLTextAreaElement=comtypes.GUID('{3050F521-98B5-11CF-BB82-00AA00BDCE0B}')
IID_IHTMLInputTextElement=comtypes.GUID('{3050F2A6-98B5-11CF-BB82-00AA00BDCE0B}')

class MSHTMLTextRangePosition(text.Position):

	def __init__(self,textRange):
		self.textRange=textRange

	def compareStart(self,p):
		res=self.textRange.compareEndPoints("startToStart",p.textRange)
		return res

	def compareEnd(self,p):
		return self.textRange.compareEndPoints("endToEnd",p.textRange)

class MSHTMLTextInfo(text.TextInfo):

	def _expandToLine(self,textRange):
		if self.basePosition in [text.POSITION_CARET,text.POSITION_SELECTION]:
			oldSelMark=self.obj.domElement.document.selection.createRange().getBookmark()
			sendKey(key("ExtendedEnd"))
			api.processPendingEvents()
			textRange.setEndPoint("endToEnd",self.obj.domElement.document.selection.createRange())
			sendKey(key("ExtendedHome"))
			api.processPendingEvents()
			textRange.setEndPoint("startToStart",self.obj.domElement.document.selection.createRange())
			self.obj.domElement.document.selection.createRange().moveToBookmark(oldSelMark)
		else:
			textRange.expand("sentence")

	def __init__(self,obj,position,expandToUnit=None,limitToUnit=None):
		super(MSHTMLTextInfo,self).__init__(obj,position,expandToUnit,limitToUnit)
		if isinstance(position,MSHTMLTextRangePosition):
			self._rangeObj=position.textRange
			if expandToUnit:
				self._rangeObj.collapse()
		else:
			self._rangeObj=self.obj.domElement.document.selection.createRange().duplicate()
		if position==text.POSITION_CARET:
			self._rangeObj.collapse()
		#Expand the position if its character, word or paragraph
		if expandToUnit in [text.UNIT_CHARACTER,text.UNIT_WORD,text.UNIT_PARAGRAPH]:
			self._rangeObj.expand(expandToUnit)
		elif expandToUnit==text.UNIT_LINE:
			self._expandToLine(self._rangeObj)
		elif expandToUnit in [text.UNIT_SCREEN,text.UNIT_STORY]:
			self._rangeObj.expand("textedit")
		elif expandToUnit is not None:
			raise NotImplementedError("unit: %s"%expandToUnit)
		self._limitRangeObj=self.obj.domElement.document.selection.createRange().duplicate()
		if limitToUnit in [text.UNIT_CHARACTER,text.UNIT_WORD,text.UNIT_PARAGRAPH]:
			self._limitRangeObj.expand(limitToUnit)
		elif limitToUnit==text.UNIT_LINE:
			self._expandToLine(self._limitRangeObj)
		elif limitToUnit in [text.UNIT_SCREEN,text.UNIT_STORY,None]:
			self._limitRangeObj.expand("textedit")
		else:
			raise NotImplementedError("unit: %s"%limitToUnit)

	def _get_position(self):
		return MSHTMLTextRangePosition(self._rangeObj.duplicate())

	def _get_text(self):
		return self._rangeObj.text

	def calculateSelectionChangedInfo(self,info):
		selInfo=text.TextSelectionChangedInfo()
		before=self._rangeObj.duplicate()
		after=info._rangeObj.duplicate()
		leftDelta=before.compareEndPoints("startToStart",after)
		rightDelta=before.compareEndPoints("endToEnd",after)
		afterLen=after.compareEndPoints("startToEnd",after)
		mode=None
		selectingText=None
		if leftDelta<0:
			mode=text.SELECTIONMODE_UNSELECTED
			before.setEndPoint("endToStart",after)
			selectingText=before.text
		elif leftDelta>0:
			mode=text.SELECTIONMODE_SELECTED
			after.setEndPoint("endToStart",before)
			selectingText=after.text
		elif rightDelta>0:
			mode=text.SELECTIONMODE_UNSELECTED
			before.setEndPoint("startToEnd",after)
			selectingText=before.text
		elif rightDelta<0:
			mode=text.SELECTIONMODE_SELECTED
			after.setEndPoint("startToEnd",before)
			selectingText=after.text
		selInfo.mode=mode
		selInfo.text=selectingText
		return selInfo

	def getRelatedUnit(self,relation):
		if self.unit is None:
			raise RuntimeError("No unit")
		if self.unit in [text.UNIT_CHARACTER,text.UNIT_WORD,text.UNIT_PARAGRAPH]:
			unit=self.unit
		elif self.unit in [text.UNIT_SCREEN,text.UNIT_STORY]:
			unit="textedit"
		elif self.unit==text.UNIT_LINE:
			unit="sentence"
		newRangeObj=self._rangeObj.duplicate()
		res=0
		if relation==text.UNITRELATION_NEXT:
			res=newRangeObj.move(unit,1)
		elif relation==text.UNITRELATION_PREVIOUS:
			res=newRangeObj.move(unit,-1)
		elif relation==text.UNITRELATION_FIRST:
			res=newRangeObj.move("textedit",-1)
		elif relation==text.UNITRELATION_LAST:
			res=newRangeObj.move("textedit",1)
			res=newRangeObj.move("character",-1)
		newRangeObj.collapse()
		if res and self._limitRangeObj.compareEndPoints("startToStart",newRangeObj)<=0 and self._limitRangeObj.compareEndPoints("endToEnd",newRangeObj)>=0: 
			return self.__class__(self.obj,MSHTMLTextRangePosition(newRangeObj),expandToUnit=self.unit,limitToUnit=self.limitUnit)
		else:
			raise text.E_noRelatedUnit

class MSHTML(IAccessible):

	def __init__(self,*args,**kwargs):
		super(MSHTML,self).__init__(*args,**kwargs)
		self.domElement=self.getDOMElementFromIAccessible()

	def getDOMElementFromIAccessible(self):
		s=self.IAccessibleObject.QueryInterface(IServiceProvider)
		interfaceAddress=s.QueryService(ctypes.byref(IID_IHTMLElement),ctypes.byref(IID_IHTMLElement))
		#We use pywin32 for large IDispatch interfaces since it handles them much better than comtypes
		o=pythoncom._univgw.interface(interfaceAddress,pythoncom.IID_IDispatch)
		t=o.GetTypeInfo()
		a=t.GetTypeAttr()
		oleRepr=win32com.client.build.DispatchItem(attr=a)
		return win32com.client.CDispatch(o,oleRepr)

	def _get_value(self):
		if self.IAccessibleRole==IAccessibleHandler.ROLE_SYSTEM_PANE:
			return ""
		else:
			return super(MSHTML,self)._get_value()


	def _get_isContentEditable(self):
		if hasattr(self,'domElement') and self.domElement.isContentEditable:
			return True
		else:
			return False

	def event_gainFocus(self):
		if self.IAccessibleRole==IAccessibleHandler.ROLE_SYSTEM_PANE and self.IAccessibleObjectID==-4:
			return
		if self.isContentEditable: 
			self.TextInfo=MSHTMLTextInfo
			self.role=controlTypes.ROLE_EDITABLETEXT
		if not api.isVirtualBufferPassThrough():
			api.toggleVirtualBufferPassThrough()
		IAccessible.event_gainFocus(self)

	def event_looseFocus(self):
		if hasattr(self,'domElement'):
			self.TextInfo=super(MSHTML,self).TextInfo

[MSHTML.bindKey(keyName,scriptName) for keyName,scriptName in [
	("ExtendedUp","moveByLine"),
	("ExtendedDown","moveByLine"),
	("ExtendedLeft","moveByCharacter"),
	("ExtendedRight","moveByCharacter"),
	("Control+ExtendedLeft","moveByWord"),
	("Control+ExtendedRight","moveByWord"),
	("Shift+ExtendedRight","changeSelection"),
	("Shift+ExtendedLeft","changeSelection"),
	("Shift+ExtendedHome","changeSelection"),
	("Shift+ExtendedEnd","changeSelection"),
	("Shift+ExtendedUp","changeSelection"),
	("Shift+ExtendedDown","changeSelection"),
	("Control+Shift+ExtendedLeft","changeSelection"),
	("Control+Shift+ExtendedRight","changeSelection"),
	("ExtendedHome","moveByCharacter"),
	("ExtendedEnd","moveByCharacter"),
	("control+extendedHome","moveByLine"),
	("control+extendedEnd","moveByLine"),
	("control+shift+extendedHome","changeSelection"),
	("control+shift+extendedEnd","changeSelection"),
	("ExtendedDelete","moveByCharacter"),
	("Back","backspace"),
]]
