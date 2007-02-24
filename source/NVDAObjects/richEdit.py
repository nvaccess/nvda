#NVDAObjects/richEdit.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import struct
import ctypes
import comtypes.automation
import win32com.client
import pythoncom
import winUser
import audio			
import IAccessibleHandler
import winEdit		

class NVDAObject_richEdit(winEdit.NVDAObject_winEdit):

	class constants:
		#Units
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

	def __init__(self,*args,**vars):
		winEdit.NVDAObject_winEdit.__init__(self,*args,**vars)
		try:
			ptr=ctypes.c_void_p()
			if ctypes.windll.oleacc.AccessibleObjectFromWindow(self.windowHandle,IAccessibleHandler.OBJID_NATIVEOM,ctypes.byref(comtypes.automation.IDispatch._iid_),ctypes.byref(ptr))!=0:
				raise OSError("No native object model")
			#We use pywin32 for large IDispatch interfaces since it handles them much better than comtypes
			o=pythoncom._univgw.interface(ptr.value,pythoncom.IID_IDispatch)
			t=o.GetTypeInfo()
			a=t.GetTypeAttr()
			oleRepr=win32com.client.build.DispatchItem(attr=a)
			self.dom=win32com.client.CDispatch(o,oleRepr)
		except:
			pass

	def __del__(self):
		if hasattr(self,'dom'):
			del self.dom

	def _get_typeString(self):
		if hasattr(self,'dom'):
			return _("rich %s")%IAccessibleHandler.getRoleName(IAccessibleHandler.ROLE_SYSTEM_TEXT)
		else:
			return IAccessibleHandler.getRoleName(IAccessibleHandler.ROLE_SYSTEM_TEXT)

	def get_text_selectionCount(self):
		if not hasattr(self,'dom'):
			return super(NVDAObject_richEdit,self)._get_text_selectionCount()
		if self.dom.Selection.Start!=self.dom.Selection.End:
			return 1
		else:
			return 0

	def text_getSelectionOffsets(self,index):
		if not hasattr(self,'dom'):
			return super(NVDAObject_richEdit,self).text_getSelectionOffsets(index)
		if index!=0:
			return None
		start=self.dom.Selection.Start
		end=self.dom.Selection.End
		if start!=end:
			return (start,end)
		else:
			return None

	def text_getWordOffsets(self,offset):
		if not hasattr(self,'dom'):
			return super(NVDAObject_richEdit,self).text_getWordOffsets(offset)
		r=self.dom.Range(offset,offset)
		r.Expand(self.constants.tomWord)
		return (r.Start,r.End)

	def text_getNextWordOffsets(self,offset):
		if not hasattr(self,'dom'):
			return super(NVDAObject_richEdit,self).text_getNextWordOffsets(offset)
		(start,end)=self.text_getWordOffsets(offset)
		r=self.dom.Range(start,start)
		res=r.Move(self.constants.tomWord,1)
		if res:
			return self.text_getWordOffsets(r.Start)
		else:
			return None

	def text_getPrevWordOffsets(self,offset):
		if not hasattr(self,'dom'):
			return super(NVDAObject_richEdit,self).text_getPrevWordOffsets(offset)
		(start,end)=self.text_getWordOffsets(offset)
		r=self.dom.Range(start,start)
		res=r.Move(self.constants.tomWord,-1)
		if res:
			return self.text_getWordOffsets(r.Start)
		else:
			return None

	def text_getSentenceOffsets(self,offset):
		if not hasattr(self,'dom'):
			return super(NVDAObject_richEdit,self).text_getSentenceOffsets(offset)
		r=self.dom.Range(offset,offset)
		r.Expand(self.constants.tomSentence)
		return (r.Start,r.End)

	def text_getNextSentenceOffsets(self,offset):
		if not hasattr(self,'dom'):
			return super(NVDAObject_richEdit,self).text_getNextSentenceOffsets(offset)
		(start,end)=self.text_getSentenceOffsets(offset)
		r=self.dom.Range(start,start)
		res=r.Move(self.constants.tomSentence,1)
		if res:
			return self.text_getSentenceOffsets(r.Start)
		else:
			return None

	def text_getPrevSentenceOffsets(self,offset):
		if not hasattr(self,'dom'):
			return super(NVDAObject_richEdit,self).text_getPrevSentenceOffsets(offset)
		(start,end)=self.text_getSentenceOffsets(offset)
		r=self.dom.Range(start,start)
		res=r.Move(self.constants.tomSentence,-1)
		if res:
			return self.text_getSentenceOffsets(r.Start)
		else:
			return None

	def text_getParagraphOffsets(self,offset):
		if not hasattr(self,'dom'):
			return super(NVDAObject_richEdit,self).text_getParagraphOffsets(offset)
		r=self.dom.Range(offset,offset)
		r.Expand(self.constants.tomParagraph)
		return (r.Start,r.End)

	def text_getNextParagraphOffsets(self,offset):
		if not hasattr(self,'dom'):
			return super(NVDAObject_richEdit,self).text_getNextParagraphOffsets(offset)
		(start,end)=self.text_getParagraphOffsets(offset)
		r=self.dom.Range(start,start)
		res=r.Move(self.constants.tomParagraph,1)
		if res:
			return self.text_getParagraphOffsets(r.Start)
		else:
			return None

	def text_getPrevParagraphOffsets(self,offset):
		if not hasattr(self,'dom'):
			return super(NVDAObject_richEdit,self).text_getPrevParagraphOffsets(offset)
		(start,end)=self.text_getParagraphOffsets(offset)
		r=self.dom.Range(start,start)
		res=r.Move(self.constants.tomParagraph,-1)
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
			return super(NVDAObject_richEdit,self).text_getFontName(offset)
		return self.dom.Range(offset,offset).Font.Name

	def text_getFontSize(self,offset):
		if not hasattr(self,'dom'):
			return super(NVDAObject_richEdit,self).text_getFontSize(offset)
		return int(self.dom.Range(offset,offset).Font.Size)

	def text_getAlignment(self,offset):
		if not hasattr(self,'dom'):
			return super(NVDAObject_richEdit,self).text_getAlignment(offset)
		alignment=self.dom.Range(offset,offset).Para.Alignment
		if alignment==self.constants.tomAlignLeft:
			return "left"
		elif alignment==self.constants.tomAlignCenter:
			return "centered"
		elif alignment==self.constants.tomAlignRight:
			return "right"
		elif alignment==self.constants.tomAlignJustify:
			return "justified"

	def text_isBold(self,offset):
		if not hasattr(self,'dom'):
			return super(NVDAObject_richEdit,self).text_isBold(offset)
		return bool(self.dom.Range(offset,offset).Font.Bold)

	def text_isItalic(self,offset):
		if not hasattr(self,'dom'):
			return super(NVDAObject_richEdit,self).text_isItalic(offset)
		return bool(self.dom.Range(offset,offset).Font.Italic)

	def text_isUnderline(self,offset):
		if not hasattr(self,'dom'):
			return super(NVDAObject_richEdit,self).text_isUnderline(offset)
		return bool(self.dom.Range(offset,offset).Font.Underline)

	def text_isSuperscript(self,offset):
		if not hasattr(self,'dom'):
			return super(NVDAObject_richEdit,self).text_isSuperscript(offset)
		return bool(self.dom.Range(offset,offset).Font.Superscript)

	def text_isSubscript(self,offset):
		if not hasattr(self,'dom'):
			return super(NVDAObject_richEdit,self).text_isSubscript(offset)
		return bool(self.dom.Range(offset,offset).Font.Subscript)
