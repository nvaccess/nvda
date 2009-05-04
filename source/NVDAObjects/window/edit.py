#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import locale
import comtypes.client
import struct
import ctypes
import pythoncom
import win32clipboard
import oleTypes
import globalVars
import eventHandler
import comInterfaces.tom
from logHandler import log
import config
import speech
import winKernel
import api
import winUser
import TextInfos.offsets
from keyUtils import key, sendKey
from scriptHandler import isScriptWaiting
import IAccessibleHandler
import controlTypes
from . import Window
from .. import NVDAObjectTextInfo
import braille

ignoreCaretEvents=False

#Edit control window messages
EM_GETSEL=176
EM_SETSEL=177
EM_GETLINE=196
EM_GETLINECOUNT=186
EM_LINEFROMCHAR=201
EM_LINEINDEX=187
EM_LINELENGTH=193
EM_POSFROMCHAR=214 
EM_CHARFROMPOS=215
EM_GETFIRSTVISIBLELINE=0x0ce
#Rich edit messages
EM_EXGETSEL=winUser.WM_USER+52
EM_EXLINEFROMCHAR=winUser.WM_USER+54
EM_EXSETSEL=winUser.WM_USER+55
EM_GETCHARFORMAT=winUser.WM_USER+58
EM_GETPARAFORMAT=winUser.WM_USER+61
EM_GETTEXTRANGE=winUser.WM_USER+75
EM_FINDWORDBREAK=winUser.WM_USER+76
#Rich edit 2.0 messages
EM_GETTEXTEX=winUser.WM_USER+94
EM_GETTEXTLENGTHEX=winUser.WM_USER+95
#Rich edit 4.0 messages
EM_GETPAGE=winUser.WM_USER+228

LF_FACESIZE=32

#structures

class PointLStruct(ctypes.Structure):
 	_fields_=[
		('x',ctypes.c_long),
		('y',ctypes.c_long),
	]

class CharRangeStruct(ctypes.Structure):
	_fields_=[
		('cpMin',ctypes.c_long),
		('cpMax',ctypes.c_long),
	]

class TextRangeUStruct(ctypes.Structure):
	_fields_=[
		('chrg',CharRangeStruct),
		('lpstrText',ctypes.c_wchar_p),
	]

class TextRangeAStruct(ctypes.Structure):
	_fields_=[
		('chrg',CharRangeStruct),
		('lpstrText',ctypes.c_char_p),
	]

CFM_LINK=0x20
CFE_BOLD=1
CFE_ITALIC=2
CFE_UNDERLINE=4
CFE_STRIKEOUT=8
CFE_PROTECTED=16
CFE_SUBSCRIPT=0x00010000 # Superscript and subscript are 
CFE_SUPERSCRIPT=0x00020000 #  mutually exclusive			 

SCF_SELECTION=0x1

class CharFormat2WStruct(ctypes.Structure):
	_fields_=[
		('cbSize',ctypes.c_uint),
		('dwMask',ctypes.wintypes.DWORD),
		('dwEffects',ctypes.wintypes.DWORD),
		('yHeight',ctypes.c_long),
		('yOffset',ctypes.c_long),
		('crTextColor',ctypes.wintypes.COLORREF),
		('bCharSet',ctypes.c_byte),
		('bPitchAndFamily',ctypes.c_byte),
		('szFaceName',ctypes.c_wchar*LF_FACESIZE),
		('wWeight',ctypes.wintypes.WORD),
		('sSpacing',ctypes.c_short),
		('crBackColor',ctypes.wintypes.COLORREF),
		('lcid',ctypes.wintypes.LCID),
		('dwReserved',ctypes.wintypes.DWORD),
		('sStyle',ctypes.c_short),
		('wKerning',ctypes.wintypes.WORD),
		('bUnderlineType',ctypes.c_byte),
		('bAnimation',ctypes.c_byte),
		('bRevAuthor',ctypes.c_byte),
		('bReserved1',ctypes.c_byte),
	]

class CharFormat2AStruct(ctypes.Structure):
	_fields_=CharFormat2WStruct._fields_[:]
	_fields_[8]=('szFaceName',ctypes.c_char*LF_FACESIZE)

class getTextExStruct(ctypes.Structure):
	_fields_=[
		('cb',ctypes.wintypes.DWORD),
		('flags',ctypes.wintypes.DWORD),
		('codepage',ctypes.c_uint),
		('lpDefaultChar',ctypes.wintypes.LPCSTR),
		('lpUsedDefChar',ctypes.c_void_p),
	]

class getTextLengthExStruct(ctypes.Structure):
	_fields_=[
		('flags',ctypes.wintypes.DWORD),
		('codepage',ctypes.c_uint),
	]

#getTextEx flags
GT_DEFAULT=0
GT_USECRLF=1
GT_SELECTION=2
GT_RAWTEXT=4
GT_NOHIDDENTEXT=8

#getTextLengthEx flags
GTL_DEFAULT=0
GTL_USECRLF=1
GTL_PRECISE=2
GTL_CLOSE=4
GTL_NUMCHARS=8
GTL_NUMBYTES=16

#findWordbreak constants
WB_CLASSIFY=3
WB_MOVEWORDLEFT=4
WB_MOVEWORDRIGHT=5
WB_LEFTBREAK=6
WB_RIGHTBREAK=7

class EditTextInfo(TextInfos.offsets.OffsetsTextInfo):

	def _getPointFromOffset(self,offset):
		if self.obj.editAPIVersion==1:
			processHandle=self.obj.processHandle
			internalP=winKernel.virtualAllocEx(processHandle,None,ctypes.sizeof(PointLStruct),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
			p=PointLStruct(0,0)
			winKernel.writeProcessMemory(processHandle,internalP,ctypes.byref(p),ctypes.sizeof(p),None)
			winUser.sendMessage(self.obj.windowHandle,EM_POSFROMCHAR,internalP,offset)
			winKernel.readProcessMemory(processHandle,internalP,ctypes.byref(p),ctypes.sizeof(p),None)
			winKernel.virtualFreeEx(processHandle,internalP,0,winKernel.MEM_RELEASE)
			point=TextInfos.Point(p.x,p.y)
		else:
			res=winUser.sendMessage(self.obj.windowHandle,EM_POSFROMCHAR,offset,None)
			point=TextInfos.Point(winUser.LOWORD(res),winUser.HIWORD(res))
		(left,top,width,height)=self.obj.location
		if point.x and point.y:
			point.x=point.x+left
			point.y=point.y+top
			return point
		else:
			raise NotImplementedError

	def _getOffsetFromPoint(self,x,y):
		(left,top,width,height)=self.obj.location
		if self.obj.editAPIVersion>=1:
			processHandle=self.obj.processHandle
			internalP=winKernel.virtualAllocEx(processHandle,None,ctypes.sizeof(PointLStruct),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
			p=PointLStruct(x-left,y-top)
			winKernel.writeProcessMemory(processHandle,internalP,ctypes.byref(p),ctypes.sizeof(p),None)
			offset=winUser.sendMessage(self.obj.windowHandle,EM_CHARFROMPOS,0,internalP)
			winKernel.virtualFreeEx(processHandle,internalP,0,winKernel.MEM_RELEASE)
		else:
			p=(x-left)+((y-top)<<16)
			offset=winUser.sendMessage(self.obj.windowHandle,EM_CHARFROMPOS,0,p)&0xffff
		return offset

	def _getCharFormat(self,offset):
		oldSel=self._getSelectionOffsets()
		if oldSel!=(offset,offset+1):
			self._setSelectionOffsets(offset,offset+1)
		if self.obj.isWindowUnicode:
			charFormatStruct=CharFormat2WStruct
		else:
			charFormatStruct=CharFormat2AStruct
		charFormat=charFormatStruct()
		charFormat.cbSize=ctypes.sizeof(charFormatStruct)
		processHandle=self.obj.processHandle
		internalCharFormat=winKernel.virtualAllocEx(processHandle,None,ctypes.sizeof(charFormat),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
		winKernel.writeProcessMemory(processHandle,internalCharFormat,ctypes.byref(charFormat),ctypes.sizeof(charFormat),None)
		winUser.sendMessage(self.obj.windowHandle,EM_GETCHARFORMAT,SCF_SELECTION, internalCharFormat)
		winKernel.readProcessMemory(processHandle,internalCharFormat,ctypes.byref(charFormat),ctypes.sizeof(charFormat),None)
		winKernel.virtualFreeEx(processHandle,internalCharFormat,0,winKernel.MEM_RELEASE)
		if oldSel!=(offset,offset+1):
			self._setSelectionOffsets(oldSel[0],oldSel[1])
		return charFormat

	def _getFormatFieldAndOffsets(self,offset,formatConfig,calculateOffsets=True):
		#Basic edit fields do not support formatting at all
		if self.obj.editAPIVersion<1:
			return super(EditTextInfo,self)._getFormatFieldAndOffsets(offset,formatConfig,calculateOffsets=calculateOffsets)
		if calculateOffsets:
			startOffset,endOffset=self._getWordOffsets(offset)
		else:
			startOffset,endOffset=self._startOffset,self._endOffset
		formatField=TextInfos.FormatField()
		charFormat=None
		if formatConfig["reportFontName"]:
			if charFormat is None: charFormat=self._getCharFormat(offset)
			formatField["font-name"]=charFormat.szFaceName
		if formatConfig["reportFontSize"]:
			if charFormat is None: charFormat=self._getCharFormat(offset)
			formatField["font-size"]="%spt"%(charFormat.yHeight/20)
		if formatConfig["reportFontAttributes"]:
			if charFormat is None: charFormat=self._getCharFormat(offset)
			formatField["bold"]=bool(charFormat.dwEffects&CFE_BOLD)
			formatField["italic"]=bool(charFormat.dwEffects&CFE_ITALIC)
			formatField["underline"]=bool(charFormat.dwEffects&CFE_UNDERLINE)
			formatField["strikethrough"]=bool(charFormat.dwEffects&CFE_STRIKEOUT)
			if charFormat.dwEffects&CFE_SUBSCRIPT:
				formatField["text-position"]="sub"
			elif charFormat.dwEffects&CFE_SUPERSCRIPT:
				formatField["text-position"]="super"
		if formatConfig["reportLineNumber"]:
			formatField["line-number"]=self._getLineNumFromOffset(offset)+1
		if formatConfig["reportLinks"]:
			if charFormat is None: charFormat=self._getCharFormat(offset)
			formatField["link"]=bool(charFormat.dwEffects&CFM_LINK)
		return formatField,(startOffset,endOffset)

	def _getSelectionOffsets(self):
		if self.obj.editAPIVersion>=1:
			charRange=CharRangeStruct()
			processHandle=self.obj.processHandle
			internalCharRange=winKernel.virtualAllocEx(processHandle,None,ctypes.sizeof(charRange),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
			winUser.sendMessage(self.obj.windowHandle,EM_EXGETSEL,0, internalCharRange)
			winKernel.readProcessMemory(processHandle,internalCharRange,ctypes.byref(charRange),ctypes.sizeof(charRange),None)
			winKernel.virtualFreeEx(processHandle,internalCharRange,0,winKernel.MEM_RELEASE)
			return (charRange.cpMin,charRange.cpMax)
		else:
			start=ctypes.c_uint()
			end=ctypes.c_uint()
			res=winUser.sendMessage(self.obj.windowHandle,EM_GETSEL,ctypes.byref(start),ctypes.byref(end))
			return start.value,end.value

	def _setSelectionOffsets(self,start,end):
		if self.obj.editAPIVersion>=1:
			charRange=CharRangeStruct()
			charRange.cpMin=start
			charRange.cpMax=end
			processHandle=self.obj.processHandle
			internalCharRange=winKernel.virtualAllocEx(processHandle,None,ctypes.sizeof(charRange),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
			winKernel.writeProcessMemory(processHandle,internalCharRange,ctypes.byref(charRange),ctypes.sizeof(charRange),None)
			winUser.sendMessage(self.obj.windowHandle,EM_EXSETSEL,0, internalCharRange)
			winKernel.virtualFreeEx(processHandle,internalCharRange,0,winKernel.MEM_RELEASE)
		else:
			winUser.sendMessage(self.obj.windowHandle,EM_SETSEL,start,end)

	def _getCaretOffset(self):
		return self._getSelectionOffsets()[0]

	def _setCaretOffset(self,offset):
		return self._setSelectionOffsets(offset,offset)

	def _getStoryText(self):
		return self.obj.windowText

	def _getStoryLength(self):
		if self.obj.editAPIVersion>=2:
			info=getTextLengthExStruct()
			info.flags=GTL_NUMCHARS
			if self.obj.isWindowUnicode:
				info.codepage=1200
			else:
				info.codepage=0
			processHandle=self.obj.processHandle
			internalInfo=winKernel.virtualAllocEx(processHandle,None,ctypes.sizeof(info),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
			winKernel.writeProcessMemory(processHandle,internalInfo,ctypes.byref(info),ctypes.sizeof(info),None)
			textLen=winUser.sendMessage(self.obj.windowHandle,EM_GETTEXTLENGTHEX,internalInfo,0)
			winKernel.virtualFreeEx(processHandle,internalInfo,0,winKernel.MEM_RELEASE)
			return textLen+1
		else:
			return winUser.sendMessage(self.obj.windowHandle,winUser.WM_GETTEXTLENGTH,0,0)+1

	def _getLineCount(self):
		return winUser.sendMessage(self.obj.windowHandle,EM_GETLINECOUNT,0,0)

	def _getTextRange(self,start,end):
		if self.obj.editAPIVersion>=2:
			bufLen=((end-start)+1)*2
			if self.obj.isWindowUnicode:
				textRange=TextRangeUStruct()
			else:
				textRange=TextRangeAStruct()
			textRange.chrg.cpMin=start
			textRange.chrg.cpMax=end
			processHandle=self.obj.processHandle
			internalBuf=winKernel.virtualAllocEx(processHandle,None,bufLen,winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
			textRange.lpstrText=internalBuf
			internalTextRange=winKernel.virtualAllocEx(processHandle,None,ctypes.sizeof(textRange),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
			winKernel.writeProcessMemory(processHandle,internalTextRange,ctypes.byref(textRange),ctypes.sizeof(textRange),None)
			res=winUser.sendMessage(self.obj.windowHandle,EM_GETTEXTRANGE,0,internalTextRange)
			winKernel.virtualFreeEx(processHandle,internalTextRange,0,winKernel.MEM_RELEASE)
			buf=(ctypes.c_byte*bufLen)()
			winKernel.readProcessMemory(processHandle,internalBuf,buf,bufLen,None)
			winKernel.virtualFreeEx(processHandle,internalBuf,0,winKernel.MEM_RELEASE)
			if self.obj.isWindowUnicode or (res>1 and (buf[res]!=0 or buf[res+1]!=0)): 
				return ctypes.cast(buf,ctypes.c_wchar_p).value
			else:
				return unicode(ctypes.cast(buf,ctypes.c_char_p).value, errors="replace", encoding=locale.getlocale()[1])
		else:
			return self._getStoryText()[start:end]

	def _getWordOffsets(self,offset):
		if self.obj.editAPIVersion>=2:
			start=winUser.sendMessage(self.obj.windowHandle,EM_FINDWORDBREAK,WB_MOVEWORDLEFT,offset)
			end=winUser.sendMessage(self.obj.windowHandle,EM_FINDWORDBREAK,WB_MOVEWORDRIGHT,start)
			if end<=offset:
				start=end
				end=winUser.sendMessage(self.obj.windowHandle,EM_FINDWORDBREAK,WB_MOVEWORDRIGHT,offset)
			return (start,end)
		elif self.basePosition in (TextInfos.POSITION_CARET,TextInfos.POSITION_SELECTION) and self.obj==api.getFocusObject():
			if offset>=(self._getStoryLength()-1):
				return [offset,offset+1]
			oldSel=self._getSelectionOffsets()
			self._setSelectionOffsets(offset,offset)
			sendKey(key("control+ExtendedLeft"))
			back=self._getSelectionOffsets()[0]
			sendKey(key("control+ExtendedRight"))
			forward=self._getSelectionOffsets()[0]
			if (back<=offset) and (forward>offset):
				start=back
				end=forward
			elif (back<offset) and (forward==offset):
				start=forward
				sendKey(key("control+ExtendedRight"))
	 			forward=self._getSelectionOffsets()[0]
				end=forward
			else:
				return super(EditTextInfo,self)._getWordOffsets(offset)
			self._setSelectionOffsets(oldSel[0],oldSel[1])
			return [start,end]
		else:
			return super(EditTextInfo,self)._getWordOffsets(offset)

	def _getLineNumFromOffset(self,offset):
		global ignoreCaretEvents
		if self.obj.editAPIVersion>=1:
			ignoreCaretEvents=True
			res=winUser.sendMessage(self.obj.windowHandle,EM_EXLINEFROMCHAR,0,offset)
			ignoreCaretEvents=False
			return res
		else:
			return winUser.sendMessage(self.obj.windowHandle,EM_LINEFROMCHAR,offset,0)

	def _getLineOffsets(self,offset):
		lineNum=self._getLineNumFromOffset(offset)
		start=winUser.sendMessage(self.obj.windowHandle,EM_LINEINDEX,lineNum,0)
		length=winUser.sendMessage(self.obj.windowHandle,EM_LINELENGTH,offset,0)
		end=start+length
		#If we just seem to get invalid line info, calculate manually
		if start<=0 and end<=0 and lineNum<=0 and self._getLineCount()<=0 and self._getStoryLength()>0:
			return super(EditTextInfo,self)._getLineOffsets(offset)
		#Some edit controls that show both line feed and carage return can give a length not including the line feed
		if end<=offset:
			end=offset+1
		#edit controls lye about their line length
		limit=self._getStoryLength()
		while self._getLineNumFromOffset(end)==lineNum and end<limit:
			end+=1
		return (start,end)

	def _getParagraphOffsets(self,offset):
		return self._getLineOffsets(offset)

ITextDocumentUnitsToNVDAUnits={
	comInterfaces.tom.tomCharacter:TextInfos.UNIT_CHARACTER,
	comInterfaces.tom.tomWord:TextInfos.UNIT_WORD,
	comInterfaces.tom.tomLine:TextInfos.UNIT_LINE,
	comInterfaces.tom.tomSentence:TextInfos.UNIT_SENTENCE,
	comInterfaces.tom.tomParagraph:TextInfos.UNIT_PARAGRAPH,
	comInterfaces.tom.tomStory:TextInfos.UNIT_STORY,
}

NVDAUnitsToITextDocumentUnits={
	TextInfos.UNIT_CHARACTER:comInterfaces.tom.tomCharacter,
	TextInfos.UNIT_WORD:comInterfaces.tom.tomWord,
	TextInfos.UNIT_LINE:comInterfaces.tom.tomLine,
	TextInfos.UNIT_SENTENCE:comInterfaces.tom.tomSentence,
	TextInfos.UNIT_PARAGRAPH:comInterfaces.tom.tomParagraph,
	TextInfos.UNIT_STORY:comInterfaces.tom.tomStory,
	TextInfos.UNIT_READINGCHUNK:comInterfaces.tom.tomSentence,
}

class ITextDocumentTextInfo(TextInfos.TextInfo):

	def _get_pointAtStart(self):
		p=TextInfos.Point(0,0)
		(p.x,p.y)=self._rangeObj.GetPoint(comInterfaces.tom.tomStart)
		if p.x and p.y:
			return p
		else:
			raise NotImplementedError

	def _getCharFormat(self,range):
		oldSel=self.obj.ITextSelectionObject.duplicate
		if not (oldSel.start==range.start and oldSel.end==range.end):
			self.obj.ITextSelectionObject.start=range.start
			self.obj.ITextSelectionObject.end=range.end
		if self.obj.isWindowUnicode:
			charFormatStruct=CharFormat2WStruct
		else:
			charFormatStruct=CharFormat2AStruct
		charFormat=charFormatStruct()
		charFormat.cbSize=ctypes.sizeof(charFormatStruct)
		processHandle=self.obj.processHandle
		internalCharFormat=winKernel.virtualAllocEx(processHandle,None,ctypes.sizeof(charFormat),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
		winKernel.writeProcessMemory(processHandle,internalCharFormat,ctypes.byref(charFormat),ctypes.sizeof(charFormat),None)
		winUser.sendMessage(self.obj.windowHandle,EM_GETCHARFORMAT,SCF_SELECTION, internalCharFormat)
		winKernel.readProcessMemory(processHandle,internalCharFormat,ctypes.byref(charFormat),ctypes.sizeof(charFormat),None)
		winKernel.virtualFreeEx(processHandle,internalCharFormat,0,winKernel.MEM_RELEASE)
		if not (oldSel.start==range.start and oldSel.end==range.end):
			self.obj.ITextSelectionObject.start=oldSel.start
			self.obj.ITextSelectionObject.end=oldSel.end
		return charFormat

	def _getFormatFieldAtRange(self,range,formatConfig):
		formatField=TextInfos.FormatField()
		fontObj=None
		paraFormatObj=None
		charFormat=None
		if formatConfig["reportAlignment"]:
			if not paraFormatObj: paraFormatObj=range.para
			alignment=paraFormatObj.alignment
			if alignment==comInterfaces.tom.tomAlignLeft:
				formatField["text-align"]="left"
			elif alignment==comInterfaces.tom.tomAlignCenter:
				formatField["text-align"]="center"
			elif alignment==comInterfaces.tom.tomAlignRight:
				formatField["text-align"]="right"
			elif alignment==comInterfaces.tom.tomAlignJustify:
				formatField["text-align"]="justify"
		if formatConfig["reportLineNumber"]:
			formatField["line-number"]=range.getIndex(comInterfaces.tom.tomLine)
		if formatConfig["reportFontName"]:
			if not fontObj: fontObj=range.font
			formatField["font-name"]=fontObj.name
		if formatConfig["reportFontSize"]:
			if not fontObj: fontObj=range.font
			formatField["font-size"]="%spt"%fontObj.size
		if formatConfig["reportFontAttributes"]:
			if not fontObj: fontObj=range.font
			formatField["bold"]=bool(fontObj.bold)
			formatField["italic"]=bool(fontObj.italic)
			formatField["underline"]=bool(fontObj.underline)
			formatField["strikethrough"]=bool(fontObj.StrikeThrough)
			if fontObj.superscript:
				formatField["text-position"]="super"
			elif fontObj.subscript:
				formatField["text-position"]="sub"
		if formatConfig["reportLinks"]:
			if charFormat is None: charFormat=self._getCharFormat(range)
			formatField["link"]=bool(charFormat.dwEffects&CFM_LINK)
		return formatField

	def _expandFormatRange(self,range,formatConfig):
		startLimit=self._rangeObj.start
		endLimit=self._rangeObj.end
		chunkRange=range.duplicate
		if formatConfig["reportLineNumber"]:
			chunkRange.expand(comInterfaces.tom.tomLine)
		else:
			chunkRange.expand(comInterfaces.tom.tomParagraph)
		chunkStart=chunkRange.start
		chunkEnd=chunkRange.end
		if startLimit<chunkStart:
			startLimit=chunkStart
		if endLimit>chunkEnd:
			endLimit=chunkEnd
		#range.moveEnd(comInterfaces.tom.tomCharFormat,1)
		range.expand(comInterfaces.tom.tomCharFormat)
		if range.end>endLimit:
			range.end=endLimit
		if range.start<startLimit:
			range.start=startLimit

	def _getTextAtRange(self,rangeObj):
		embedRangeObj=None
		bufText=rangeObj.text
		if bufText is None:
			bufText=""
		newTextList=[]
		start=rangeObj.start
		for offset in range(len(bufText)):
			if ord(bufText[offset])==0xfffc:
				if embedRangeObj is None: embedRangeObj=rangeObj.duplicate
				embedRangeObj.setRange(start+offset,start+offset)
				try:
					o=embedRangeObj.GetEmbeddedObject()
					#Fetch a description for this object
					o=o.QueryInterface(oleTypes.IOleObject)
					dataObj=o.GetClipboardData(0)
					dataObj=pythoncom._univgw.interface(hash(dataObj),pythoncom.IID_IDataObject)
					format=(win32clipboard.CF_UNICODETEXT, None, pythoncom.DVASPECT_CONTENT, -1, pythoncom.TYMED_HGLOBAL)
					medium=dataObj.GetData(format)
					buf=ctypes.create_string_buffer(medium.data)
					buf=ctypes.cast(buf,ctypes.c_wchar_p)
					label=buf.value
				except comtypes.COMError:
					label=_("unknown")
				if label:
					newTextList.append(_("%s embedded object")%label)
				else:
					newTextList.append(_("embedded object"))
			else:
				newTextList.append(bufText[offset])
		return "".join(newTextList)

	def __init__(self,obj,position,_rangeObj=None):
		super(ITextDocumentTextInfo,self).__init__(obj,position)
		if _rangeObj:
			self._rangeObj=_rangeObj.Duplicate
			return
		if isinstance(position,TextInfos.Point):
			self._rangeObj=self.obj.ITextDocumentObject.rangeFromPoint(position.x,position.y)
		elif position==TextInfos.POSITION_ALL:
			self._rangeObj=self.obj.ITextDocumentObject.range(0,0)
			self._rangeObj.expand(comInterfaces.tom.tomStory)
		elif position==TextInfos.POSITION_SELECTION:
			self._rangeObj=self.obj.ITextSelectionObject.duplicate
		elif position==TextInfos.POSITION_CARET:
			self._rangeObj=self.obj.ITextSelectionObject.duplicate
			self._rangeObj.Collapse(True)
		elif position==TextInfos.POSITION_FIRST:
			self._rangeObj=self.obj.ITextDocumentObject.range(0,0)
		elif position==TextInfos.POSITION_LAST:
			self._rangeObj=self.obj.ITextDocumentObject.range(0,0)
			self._rangeObj.move(comInterfaces.tom.tomStory,1)
			self._rangeObj.moveStart(comInterfaces.tom.tomCharacter,-1)
		elif isinstance(position,TextInfos.offsets.Offsets):
			self._rangeObj=self.obj.ITextDocumentObject.range(position.startOffset,position.endOffset)
		else:
			raise NotImplementedError("position: %s"%position)

	def getInitialFields(self,formatConfig=None):
		if not formatConfig:
			formatConfig=config.conf["documentFormatting"]
		range=self._rangeObj.duplicate
		range.collapse(True)
		range.expand(comInterfaces.tom.tomCharacter)
		return [self._getFormatFieldAtRange(range,formatConfig)]

	def getTextWithFields(self,formatConfig=None):
		if not formatConfig:
			formatConfig=config.conf["documentFormatting"]
		if not formatConfig["detectFormatAfterCursor"]:
			return [self._getTextAtRange(self._rangeObj)]
		commandList=[]
		endLimit=self._rangeObj.end
		range=self._rangeObj.duplicate
		range.collapse(True)
		hasLoopedOnce=False
		while range.end<endLimit:
			self._expandFormatRange(range,formatConfig)
			if hasLoopedOnce:
				commandList.append(TextInfos.FieldCommand("formatChange",self._getFormatFieldAtRange(range,formatConfig)))
			else:
				hasLoopedOnce=True
			commandList.append(self._getTextAtRange(range))
			end=range.end
			range.start=end
			#Trying to set the start past the end of the document forces both start and end back to the previous offset, so catch this
			if range.end<end:
				break
		return commandList

	def expand(self,unit):
		if unit in NVDAUnitsToITextDocumentUnits:
			self._rangeObj.Expand(NVDAUnitsToITextDocumentUnits[unit])
		else:
			raise NotImplementedError("unit: %s"%unit)

	def compareEndPoints(self,other,which):
		if which=="startToStart":
			diff=self._rangeObj.Start-other._rangeObj.Start
		elif which=="startToEnd":
			diff=self._rangeObj.Start-other._rangeObj.End
		elif which=="endToStart":
			diff=self._rangeObj.End-other._rangeObj.Start
		elif which=="endToEnd":
			diff=self._rangeObj.End-other._rangeObj.End
		else:
			raise ValueError("bad argument - which: %s"%which)
		if diff<0:
			diff=-1
		elif diff>0:
			diff=1
		return diff

	def setEndPoint(self,other,which):
		if which=="startToStart":
			self._rangeObj.Start=other._rangeObj.Start
		elif which=="startToEnd":
			self._rangeObj.Start=other._rangeObj.End
		elif which=="endToStart":
			self._rangeObj.End=other._rangeObj.Start
		elif which=="endToEnd":
			self._rangeObj.End=other._rangeObj.End
		else:
			raise ValueError("bad argument - which: %s"%which)

	def _get_isCollapsed(self):
		if self._rangeObj.Start==self._rangeObj.End:
			return True
		else:
			return False

	def collapse(self,end=False):
		a=self._rangeObj.Start
		b=self._rangeObj.end
		startOffset=min(a,b)
		endOffset=max(a,b)
		if not end:
			offset=startOffset
		else:
			offset=endOffset
		self._rangeObj.SetRange(offset,offset)

	def copy(self):
		return ITextDocumentTextInfo(self.obj,None,_rangeObj=self._rangeObj)

	def _get_text(self):
		return self._getTextAtRange(self._rangeObj)

	def move(self,unit,direction,endPoint=None):
		if unit in NVDAUnitsToITextDocumentUnits:
			unit=NVDAUnitsToITextDocumentUnits[unit]
		else:
			raise NotImplementedError("unit: %s"%unit)
		if endPoint=="start":
			moveFunc=self._rangeObj.MoveStart
		elif endPoint=="end":
			moveFunc=self._rangeObj.MoveEnd
		else:
			moveFunc=self._rangeObj.Move
		res=moveFunc(unit,direction)
		return res

	def _get_bookmark(self):
		return TextInfos.offsets.Offsets(self._rangeObj.start,self._rangeObj.end)

	def updateCaret(self):
		self.obj.ITextSelectionObject.start=self.obj.ITextSelectionObject.end=self._rangeObj.start

	def updateSelection(self):
		self.obj.ITextSelectionObject.start=self._rangeObj.start
		self.obj.ITextSelectionObject.end=self._rangeObj.end

class Edit(Window):

	editAPIVersion=0
	editAPIUnicode=True
	useITextDocumentSupport=False
	editValueUnit=TextInfos.UNIT_LINE

	def _get_TextInfo(self):
		if self.editAPIVersion>1 and self.useITextDocumentSupport and self.ITextDocumentObject:
			return ITextDocumentTextInfo
		else:
			return EditTextInfo

	def _get_ITextDocumentObject(self):
		if not hasattr(self,'_ITextDocumentObject'):
			try:
				ptr=ctypes.POINTER(comInterfaces.tom.ITextDocument)()
				ctypes.windll.oleacc.AccessibleObjectFromWindow(self.windowHandle,-16,ctypes.byref(ptr._iid_),ctypes.byref(ptr))
				self._ITextDocumentObject=ptr
			except:
				log.error("Error getting ITextDocument",exc_info=True)
				self._ITextDocumentObject=None
		return self._ITextDocumentObject

	def _get_ITextSelectionObject(self):
		if not hasattr(self,'_ITextSelectionObject'):
			try:
				self._ITextSelectionObject=self.ITextDocumentObject.selection
			except:
				self._ITextSelectionObject=None
		return self._ITextSelectionObject

	def _get_value(self):
		return None

	def _get_role(self):
		return controlTypes.ROLE_EDITABLETEXT

	def event_caret(self):
		#Make sure that this object *really* has the focus before bothering to speak any possible selection change
		api.processPendingEvents()
		if self is not api.getFocusObject() or eventHandler.isPendingEvents('gainFocus'):
			return
		if eventHandler.isPendingEvents('valueChange',self):
			self.hasContentChangedSinceLastSelection=True
		if globalVars.caretMovesReviewCursor:
			api.setReviewPosition(self.makeTextInfo(TextInfos.POSITION_CARET))
		braille.handler.handleCaretMove(self)
		self.detectPossibleSelectionChange()

	def event_valueChange(self):
		self.hasContentChangedSinceLastSelection=True

	def event_gainFocus(self):
		self.initAutoSelectDetection()
		super(Edit,self).event_gainFocus()

	def _get_states(self):
		states = super(Edit, self)._get_states()
		if self.windowStyle & winUser.ES_MULTILINE:
			states.add(controlTypes.STATE_MULTILINE)
		return states

[Edit.bindKey(keyName,scriptName) for keyName,scriptName in [
	("ExtendedUp","moveByLine"),
	("ExtendedDown","moveByLine"),
	("ExtendedLeft","moveByCharacter"),
	("ExtendedRight","moveByCharacter"),
	("ExtendedPrior","moveByLine"),
	("ExtendedNext","moveByLine"),
	("Control+ExtendedLeft","moveByWord"),
	("Control+ExtendedRight","moveByWord"),
	("control+extendedDown","moveByParagraph"),
	("control+extendedUp","moveByParagraph"),
	("ExtendedHome","moveByCharacter"),
	("ExtendedEnd","moveByCharacter"),
	("control+extendedHome","moveByLine"),
	("control+extendedEnd","moveByLine"),
	("ExtendedDelete","delete"),
	("Back","backspace"),
]]

class RichEdit(Edit):
	editAPIVersion=1

class RichEdit20(RichEdit):
	editAPIVersion=2

class RichEdit30(RichEdit):
	editAPIVersion=3

class RichEdit50(RichEdit):
	editAPIVersion=5
