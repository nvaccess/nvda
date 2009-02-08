#NVDAObjects/MSHTML.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import time
import ctypes
import comtypes.client
import comtypes.automation
from comInterfaces.servprov import IServiceProvider
import winUser
import globalVars
import IAccessibleHandler
from keyUtils import key, sendKey
import api
import textHandler
from logHandler import log
import speech
import controlTypes
from . import IAccessible
import NVDAObjects
import virtualBufferHandler

lastMSHTMLEditGainFocusTimeStamp=0


IID_IHTMLElement=comtypes.GUID('{3050F1FF-98B5-11CF-BB82-00AA00BDCE0B}')

class MSHTMLTextInfo(textHandler.TextInfo):

	def _expandToLine(self,textRange):
		parent=textRange.parentElement()
		if not parent.isMultiline: #fastest solution for single line edits (<input type="text">)
			textRange.expand("textEdit")
			return
		parentRect=parent.getBoundingClientRect()
		#This can be simplified when comtypes is fixed
		lineTop=comtypes.client.dynamic._Dispatch(textRange._comobj).offsetTop
		lineLeft=parentRect.left+parent.clientLeft
		#editable documents have a different right most boundary to <textarea> elements.
		if self.obj.IHTMLElement.document.body.isContentEditable:
			lineRight=parentRect.right 
		else:
			lineRight=parentRect.left+parent.clientWidth
		tempRange=textRange.duplicate()
		tempRange.moveToPoint(lineLeft,lineTop)
		textRange.setEndPoint("startToStart",tempRange)
		tempRange.moveToPoint(lineRight,lineTop)
		textRange.setEndPoint("endToStart",tempRange)

	def __init__(self,obj,position,_rangeObj=None):
		super(MSHTMLTextInfo,self).__init__(obj,position)
		if _rangeObj:
			self._rangeObj=_rangeObj.duplicate()
			return
		if position in (textHandler.POSITION_CARET,textHandler.POSITION_SELECTION):
			if self.obj.IHTMLElement.uniqueID!=self.obj.IHTMLElement.document.activeElement.uniqueID:
				raise RuntimeError("Only works with currently selected element")
			self._rangeObj=self.obj.IHTMLElement.document.selection.createRange()
			if position==textHandler.POSITION_CARET:
				self._rangeObj.collapse()
			return
		self._rangeObj=self.obj.IHTMLElement.createTextRange()
		if position==textHandler.POSITION_FIRST:
			self._rangeObj.collapse()
		elif position==textHandler.POSITION_LAST:
			self._rangeObj.expand("textedit")
			self.collapse(True)
			self._rangeObj.move("character",-1)
		elif position==textHandler.POSITION_ALL:
			self._rangeObj.expand("textedit")
		elif isinstance(position,textHandler.Bookmark):
			if position.infoClass==self.__class__:
				self._rangeObj.moveToBookmark(position.data)
			else:
				raise TypeError("Bookmark was for %s type, not for %s type"%(position.infoClass.__name__,self.__class__.__name__))
		else:
			raise NotImplementedError("position: %s"%position)

	def expand(self,unit):
		if unit==textHandler.UNIT_LINE and self.basePosition not in [textHandler.POSITION_SELECTION,textHandler.POSITION_CARET]:
			unit=textHandler.UNIT_SENTENCE
		if unit==textHandler.UNIT_READINGCHUNK:
			unit=textHandler.UNIT_SENTENCE
		if unit in [textHandler.UNIT_CHARACTER,textHandler.UNIT_WORD,textHandler.UNIT_SENTENCE,textHandler.UNIT_PARAGRAPH]:
			res=self._rangeObj.expand(unit)
			if not res and unit=="word": #IHTMLTxtRange.expand fails to handle word when at the start of a field
				res=self._rangeObj.moveEnd(unit,1)
				if res:
					self._rangeObj.moveStart(unit,-1)
		elif unit==textHandler.UNIT_LINE:
			self._expandToLine(self._rangeObj)
		elif unit==textHandler.UNIT_STORY:
			self._rangeObj.expand("textedit")
		else:
			raise NotImplementedError("unit: %s"%unit)

	def _get_isCollapsed(self):
		if self._rangeObj.compareEndPoints("startToEnd",self._rangeObj)==0:
			return True
		else:
			return False


	def collapse(self,end=False):
		self._rangeObj.collapse(not end)

	def copy(self):
		return self.__class__(self.obj,None,_rangeObj=self._rangeObj.duplicate())

	def compareEndPoints(self,other,which):
		return self._rangeObj.compareEndPoints(which,other._rangeObj)

	def setEndPoint(self,other,which):
		self._rangeObj.setEndPoint(which,other._rangeObj)

	def _get_text(self):
		text=self._rangeObj.text
		if not text:
			text=""
		return text


	def move(self,unit,direction, endPoint=None):
		if unit in [textHandler.UNIT_READINGCHUNK,textHandler.UNIT_LINE]:
			unit=textHandler.UNIT_SENTENCE
		if unit==textHandler.UNIT_STORY:
			unit="textedit"
		if endPoint=="start":
			moveFunc=self._rangeObj.moveStart
		elif endPoint=="end":
			moveFunc=self._rangeObj.moveEnd
		else:
			moveFunc=self._rangeObj.move
		res=moveFunc(unit,direction)
		return res

	def updateCaret(self):
		self._rangeObj.select()

	def updateSelection(self):
		self._rangeObj.select()

	def _get_bookmark(self):
		return textHandler.Bookmark(self.__class__,self._rangeObj.getBookmark())

class MSHTML(IAccessible):

	def __init__(self,*args,**kwargs):
		super(MSHTML,self).__init__(*args,**kwargs)
		try:
			self.IHTMLElement.createTextRange()
			self.TextInfo=MSHTMLTextInfo
		except:
			pass
		if self.TextInfo==MSHTMLTextInfo:
			[self.bindKey_runtime(keyName,scriptName) for keyName,scriptName in [
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

	def _get_IHTMLElement(self):
		if not hasattr(self,'_IHTMLElement'):
			s=self.IAccessibleObject.QueryInterface(IServiceProvider)
			interfaceAddress=s.QueryService(ctypes.byref(IID_IHTMLElement),ctypes.byref(comtypes.automation.IDispatch._iid_))
			ptr=ctypes.POINTER(comtypes.automation.IDispatch)(interfaceAddress)
			self._IHTMLElement=comtypes.client.dynamic.Dispatch(ptr)
		return self._IHTMLElement

	def _get_value(self):
		if self.IAccessibleRole==IAccessibleHandler.ROLE_SYSTEM_PANE:
			return ""
		else:
			return super(MSHTML,self).value

	def _get_role(self):
		if self.IHTMLElement.tagName.lower()=="body":
			return controlTypes.ROLE_DOCUMENT
		return super(MSHTML,self).role

	def _get_states(self):
		states=super(MSHTML,self).states
		if self.IHTMLElement.isContentEditable:
			states.add(controlTypes.STATE_EDITABLE)
		if self.IHTMLElement.isMultiline:
			states.add(controlTypes.STATE_MULTILINE)
		return states

	def _get_isContentEditable(self):
		if hasattr(self,'IHTMLElement'): 
			try:
				return bool(self.IHTMLElement.isContentEditable)
			except:
				return False
		else:
			return False

	def event_gainFocus(self):
		if not self.isContentEditable:
			vbuf=self.virtualBuffer
			if vbuf and vbuf.passThrough:
				vbuf.passThrough=True
				virtualBufferHandler.reportPassThrough(vbuf)
		super(MSHTML,self).event_gainFocus()

	def reportFocus(self):
		global lastMSHTMLEditGainFocusTimeStamp
		timeStamp=time.time()
		if self.isContentEditable and (timeStamp-lastMSHTMLEditGainFocusTimeStamp)>0.5:
			super(MSHTML,self).reportFocus()
		lastMSHTMLEditGainFocusTimeStamp=timeStamp
