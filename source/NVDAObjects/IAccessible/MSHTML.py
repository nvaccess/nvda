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

class MSHTMLTextInfo(text.TextInfo):

	def _getSelectionOffsets(self):
		mark=self._rangeObj.getBookmark()
		start=(ord(mark[2])-self._offsetBias)-((ord(mark[8])-self._lineNumBias)/2)
		if ord(mark[1])==3:
			end=(ord(mark[40])-self._offsetBias)-((ord(mark[8])-self._lineNumBias)/2)
		else:
			end=start
		return [start,end]

	def _expandToLine(self,textRange):
		oldSelMark=self.obj.domElement.document.selection.createRange().getBookmark()
		curMark=textRange.getBookmark()
		self.obj.domElement.document.selection.createRange().moveToBookmark(curMark)
		api.processPendingEvents()
		sendKey(key("ExtendedEnd"))
		api.processPendingEvents()
		textRange.setEndPoint("endToEnd",self.obj.domElement.document.selection.createRange())
		sendKey(key("ExtendedHome"))
		api.processPendingEvents()
		textRange.setEndPoint("startToStart",self.obj.domElement.document.selection.createRange())
		self.obj.domElement.document.selection.createRange().moveToBookmark(oldSelMark)

	def __init__(self,obj,position,_rangeObj=None,_lineNumBias=None,_offsetBias=None):
		super(MSHTMLTextInfo,self).__init__(obj,position)
		if self.obj.domElement.uniqueID!=self.obj.domElement.document.activeElement.uniqueID:
			raise RuntimeError("Only works with currently selected element")
		if _rangeObj:
			self._rangeObj=_rangeObj.duplicate()
			self._lineNumBias=_lineNumBias
			self._offsetBias=_offsetBias
			return
		self._rangeObj=self.obj.domElement.document.selection.createRange().duplicate()
		biasRange=self._rangeObj.duplicate()
		biasRange.move("textedit",-1)
		biasRange.collapse()
		biasMark=biasRange.getBookmark()
		self._lineNumBias=ord(biasMark[8])
		self._offsetBias=ord(biasMark[2])
		if position==text.POSITION_SELECTION:
			pass
		elif position==text.POSITION_CARET:
			self._rangeObj.collapse()
		elif position==text.POSITION_FIRST:
			self._rangeObj.move("textedit",-1)
		elif position==text.POSITION_FIRST:
			self._rangeObj.expand("textedit")
			self.collapse(True)
			self._rangeObj.move("character",-1)
		elif isinstance(position,text.Bookmark):
			self._rangeObj.moveToBookmark(position.data)
		else:
			raise NotImplementedError("position: %s"%position)

	def expand(self,unit):
		if unit==text.UNIT_LINE and self.basePosition not in [text.POSITION_SELECTION,text.POSITION_CARET]:
			unit=text.UNIT_SENTENCE
		if unit==text.UNIT_READINGCHUNK:
			unit=text.UNIT_SENTENCE
		if unit in [text.UNIT_CHARACTER,text.UNIT_WORD,text.UNIT_SENTENCE,text.UNIT_PARAGRAPH]:
			self._rangeObj.expand(unit)
		elif unit==text.UNIT_LINE:
			self._expandToLine(self._rangeObj)
		elif unit==text.UNIT_STORY:
			self._rangeObj.expand("textedit")
		else:
			raise NotImplementedError("unit: %s"%unit)

	def collapse(self,end=False):
		self._rangeObj.collapse(not end)

	def copy(self):
		return self.__class__(self.obj,None,_rangeObj=self._rangeObj,_lineNumBias=self._lineNumBias,_offsetBias=self._offsetBias)

	def compareStart(self,info):
		newOffsets=self._getSelectionOffsets()
		oldOffsets=info._getSelectionOffsets()
		return newOffsets[0]-oldOffsets[0]

	def compareEnd(self,info):
		newOffsets=self._getSelectionOffsets()
		oldOffsets=info._getSelectionOffsets()
		return newOffsets[1]-oldOffsets[1]

	def _get_text(self):
		return self._rangeObj.text

	def moveByUnit(self,unit,num,start=True,end=True):
		if unit in [text.UNIT_READINGCHUNK,text.UNIT_LINE]:
			unit=text.UNIT_SENTENCE
		if unit==text.UNIT_STORY:
			unit="textedit"
		if start and not end:
			moveFunc=self._rangeObj.moveStart
		elif end and not start:
			moveFunc=self._rangeObj.moveEnd
		else:
			moveFunc=self._rangeObj.move
		res=moveFunc(unit,num)
		return res

	def updateCaret(self):
		self._rangeObj.select()

	def updateSelection(self):
		self._rangeObj.select()

	def _get_bookmark(self):
		return text.Bookmark(self._rangeObj.getBookmark())

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
