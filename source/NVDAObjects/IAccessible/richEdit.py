#NVDAObjects/RichEdit.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import struct
import ctypes
import comtypes.automation
import comtypesClient
import oleTypes
import win32com.client
import pythoncom
import winUser
import text
import debug
import speech
import IAccessibleHandler
from winEdit import WinEdit

#structures
class charRange(ctypes.Structure):
	_fields_=[
		('cpMin',ctypes.c_long),
		('cpMax',ctypes.c_long),
	]

#window messages
EM_EXGETSEL=winUser.WM_USER+52

#ITextDocument constants
tomCharacter=1
tomWord=2
tomSentence=3
tomParagraph=4
tomLine=5
tomStory=6
tomScreen=7
tomSection=8
tomColumn=9
tomRow=10
tomWindow=11
tomCell=12
tomCharFormat=13
tomParaFormat=14
tomTable=15
tomObject=16
tomPage=17
#Paragraph alignment
tomAlignLeft=0
tomAlignCenter=1
tomAlignRight=2
tomAlignJustify=3

class RichEdit(WinEdit):

	def __init__(self,*args,**vars):
		WinEdit.__init__(self,*args,**vars)
		try:
			#ptr=ctypes.c_void_p()
			ptr=ctypes.POINTER(comtypes.automation.IUnknown)()
			if ctypes.windll.oleacc.AccessibleObjectFromWindow(self.windowHandle,IAccessibleHandler.OBJID_NATIVEOM,ctypes.byref(comtypes.automation.IDispatch._iid_),ctypes.byref(ptr))!=0:
				raise OSError("No native object model")
			self.dom=comtypesClient.wrap(ptr)
			#We use pywin32 for large IDispatch interfaces since it handles them much better than comtypes
			#o=pythoncom._univgw.interface(ptr.value,pythoncom.IID_IDispatch)
			#t=o.GetTypeInfo()
			#a=t.GetTypeAttr()
			#oleRepr=win32com.client.build.DispatchItem(attr=a)
			#self.dom=win32com.client.CDispatch(o,oleRepr)
		except:
			self.TextInfo=WinEdit.textInfo
			pass

	def __del__(self):
		if hasattr(self,'dom'):
			del self.dom

	def _get_typeString(self):
		if hasattr(self,'dom'):
			return _("rich %s")%IAccessibleHandler.getRoleName(IAccessibleHandler.ROLE_SYSTEM_TEXT)
		else:
			return IAccessibleHandler.getRoleName(IAccessibleHandler.ROLE_SYSTEM_TEXT)

	def text_getSelectionOffsets(self,index):
		if index!=0:
			return None
		offsets=super(RichEdit,self).text_getSelectionOffsets(index)
		if offsets is not None and (offsets[0]>=65535 or offsets[1]>=65535) and hasattr(self,'dom'):
 			start=self.dom.Selection.Start
			end=self.dom.Selection.End
			if start>=0 and end>=0 and end>start:
				offsets=(start,end)
			else:
				offsets=None
		return offsets

	def _get_text_caretOffset(self):
		offset=super(RichEdit,self)._get_text_caretOffset()
		if offset>=65535 and hasattr(self,'dom'):
			offset=self.dom.Selection.Start
		return offset

	def _set_text_caretOffset(self,offset):
		if offset>=65535 and hasattr(self,'dom'):
			self.dom.Selection.SetRange(offset,offset)
		else:
			super(RichEdit,self)._set_text_caretOffset(offset)

	def text_getWordOffsets(self,offset):
		if not hasattr(self,'dom'):
			return super(RichEdit,self).text_getWordOffsets(offset)
		r=self.dom.Range(offset,offset)
		r.Expand(tomWord)
		return (r.Start,r.End)

	def text_getNextWordOffsets(self,offset):
		if not hasattr(self,'dom'):
			return super(RichEdit,self).text_getNextWordOffsets(offset)
		(start,end)=self.text_getWordOffsets(offset)
		r=self.dom.Range(start,start)
		res=r.Move(tomWord,1)
		if res:
			return self.text_getWordOffsets(r.Start)
		else:
			return None

	def text_getPrevWordOffsets(self,offset):
		if not hasattr(self,'dom'):
			return super(RichEdit,self).text_getPrevWordOffsets(offset)
		(start,end)=self.text_getWordOffsets(offset)
		r=self.dom.Range(start,start)
		res=r.Move(tomWord,-1)
		if res:
			return self.text_getWordOffsets(r.Start)
		else:
			return None

	def text_getSentenceOffsets(self,offset):
		if not hasattr(self,'dom'):
			return super(RichEdit,self).text_getSentenceOffsets(offset)
		r=self.dom.Range(offset,offset)
		r.Expand(tomSentence)
		return (r.Start,r.End)

	def text_getNextSentenceOffsets(self,offset):
		if not hasattr(self,'dom'):
			return super(RichEdit,self).text_getNextSentenceOffsets(offset)
		(start,end)=self.text_getSentenceOffsets(offset)
		r=self.dom.Range(start,start)
		res=r.Move(tomSentence,1)
		if res:
			return self.text_getSentenceOffsets(r.Start)
		else:
			return None

	def text_getPrevSentenceOffsets(self,offset):
		if not hasattr(self,'dom'):
			return super(RichEdit,self).text_getPrevSentenceOffsets(offset)
		(start,end)=self.text_getSentenceOffsets(offset)
		r=self.dom.Range(start,start)
		res=r.Move(tomSentence,-1)
		if res:
			return self.text_getSentenceOffsets(r.Start)
		else:
			return None

	def text_getParagraphOffsets(self,offset):
		if not hasattr(self,'dom'):
			return super(RichEdit,self).text_getParagraphOffsets(offset)
		r=self.dom.Range(offset,offset)
		r.Expand(tomParagraph)
		return (r.Start,r.End)

	def text_getNextParagraphOffsets(self,offset):
		if not hasattr(self,'dom'):
			return super(RichEdit,self).text_getNextParagraphOffsets(offset)
		(start,end)=self.text_getParagraphOffsets(offset)
		r=self.dom.Range(start,start)
		res=r.Move(tomParagraph,1)
		if res:
			return self.text_getParagraphOffsets(r.Start)
		else:
			return None

	def text_getPrevParagraphOffsets(self,offset):
		if not hasattr(self,'dom'):
			return super(RichEdit,self).text_getPrevParagraphOffsets(offset)
		(start,end)=self.text_getParagraphOffsets(offset)
		r=self.dom.Range(start,start)
		res=r.Move(tomParagraph,-1)
		if res:
			return self.text_getParagraphOffsets(r.Start)
		else:
			return None

	def text_getFieldOffsets(self,offset):
		r=self.text_getLineOffsets(offset)
		return r

	def text_getNextFieldOffsets(self,offset):
		r=self.text_getNextLineOffsets(offset)
		return r

	def text_getPrevFieldOffsets(self,offset):
		r=self.text_getPrevLineOffsets(offset)
		return r

	def text_getFontName(self,offset):
		if not hasattr(self,'dom'):
			return super(RichEdit,self).text_getFontName(offset)
		return self.dom.Range(offset,offset).Font.Name

	def text_getFontSize(self,offset):
		if not hasattr(self,'dom'):
			return super(RichEdit,self).text_getFontSize(offset)
		return int(self.dom.Range(offset,offset).Font.Size)

	def text_getAlignment(self,offset):
		if not hasattr(self,'dom'):
			return super(RichEdit,self).text_getAlignment(offset)
		alignment=self.dom.Range(offset,offset).Para.Alignment
		if alignment==tomAlignLeft:
			return "left"
		elif alignment==tomAlignCenter:
			return "centered"
		elif alignment==tomAlignRight:
			return "right"
		elif alignment==tomAlignJustify:
			return "justified"

	def text_isBold(self,offset):
		if not hasattr(self,'dom'):
			return super(RichEdit,self).text_isBold(offset)
		return bool(self.dom.Range(offset,offset).Font.Bold)

	def text_isItalic(self,offset):
		if not hasattr(self,'dom'):
			return super(RichEdit,self).text_isItalic(offset)
		return bool(self.dom.Range(offset,offset).Font.Italic)

	def text_isUnderline(self,offset):
		if not hasattr(self,'dom'):
			return super(RichEdit,self).text_isUnderline(offset)
		return bool(self.dom.Range(offset,offset).Font.Underline)

	def text_isSuperscript(self,offset):
		if not hasattr(self,'dom'):
			return super(RichEdit,self).text_isSuperscript(offset)
		return bool(self.dom.Range(offset,offset).Font.Superscript)

	def text_isSubscript(self,offset):
		if not hasattr(self,'dom'):
			return super(RichEdit,self).text_isSubscript(offset)
		return bool(self.dom.Range(offset,offset).Font.Subscript)

class TextInfo(text.TextInfo):

	unitMap={
		text.UNIT_CHARACTER:tomCharacter,
		text.UNIT_WORD:tomWord,
		text.UNIT_LINE:tomLine,
		text.UNIT_PARAGRAPH:tomParagraph,
		text.UNIT_PAGE:tomPage,
		text.UNIT_TABLE:tomTable,
		text.UNIT_COLUMN:tomColumn,
		text.UNIT_ROW:tomRow,
		text.UNIT_CELL:tomCell,
		text.UNIT_SCREEN:tomStory,
		text.UNIT_STORY:tomStory,
	}

	def __init__(self,obj,position,expandToUnit=None,limitToUnit=None):
		super(self.__class__,self).__init__(obj,position,expandToUnit,limitToUnit)
		#Create a range object for the given position
		if position==text.POSITION_FIRST:
			self._range=self.obj.dom.Range(0,0)
		elif position==text.POSITION_LAST:
			self._range=self.obj.dom.Range(0,0)
			self._range.expand(tomStory)
			self._range.Start=self._range.End=self._range.End-1
		elif position in [text.POSITION_CARET,text.POSITION_SELECTION]:
			self._range=self.obj.dom.selection.Duplicate
			if position==text.POSITION_CARET:
				self._range.End=self._range.Start
		elif isinstance(position,text.OffsetsPosition):
			self._range=self.obj.dom.Range(position.start,position.end)
		elif isinstance(position,text.OffsetPosition):
			self._range=self.obj.dom.Range(position.offset,position.offset)
		else:
			raise NotImplementedError("position: %s"%position)
		#Expand the range object to the given unit
		if expandToUnit is not None:
			unit=self.unitMap.get(expandToUnit,None)
			if unit is not None:
				self._range.expand(unit)
			else:
				raise NotImplementedError("expandToUnit: %s"%expandToUnit)
		#create another range object expanded to the given limit unit
		if limitToUnit not in [None,text.UNIT_SCREEN,text.UNIT_STORY]:
			unit=self.unitMap.get(limitToUnit)
			if unit is not None:
				self._limitRange=self._range.Duplicate
				self._limitRange.expand(unit)
			else:
				raise NotImplementedError("limitToUnit: %s"%limitToUnit)

	def _get_startOffset(self):
		return self._range.Start

	def _get_endOffset(self):
		return self._range.End

	def _get_text(self):
		obj=self._range.getEmbeddedObject()
		if ctypes.cast(obj,ctypes.c_void_p).value==None:
			return ""
		obj=obj.QueryInterface(oleTypes.IOleObject)
		clipFormat=oleTypes.wireCLIPFORMAT()
		clipFormat.u.dwValue=winUser.CF_TEXT
		format=oleTypes.tagFORMATETC
		format.cfFormat=clipFormat
		format.ptd=None
		format.dwAspect=1
		format.lindex=0
		format.tymed=1

		return ""

	def getRelatedUnit(self,relation):
		unit=self.unitMap.get(self.unit,None)
		if unit is None:
			raise RuntimeError("No unit")
		r=self._range.Duplicate
		r.End=r.Start
		moved=0
		if relation==text.UNITRELATION_NEXT:
			moved=r.move(unit,1)
		elif relation==text.UNITRELATION_PREVIOUS:
			moved=r.move(unit,-1)
		elif relation==text.UNITRELATION_FIRST:
			r.setRange(0,0)
			moved=1
		elif relation==text.UNITRELATION_LAST:
			r.Start=r.End=self._limitRange.End-1
			moved=1
		if moved==0 or (hasattr(self,"_limitRange") and not r.inRange(self._limitRange)):
			raise text.E_noRelatedUnit
		return self.__class__(self.obj,text.OffsetPosition(r.Start),expandToUnit=self.unit,limitToUnit=self.limitUnit)

class testTextInfo(WinEdit.TextInfo):

	APIVersion=2

RichEdit.TextInfo=testTextInfo

