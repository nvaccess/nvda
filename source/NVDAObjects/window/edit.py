#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2018 NV Access Limited, Babbage B.V.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import locale
import comtypes.client
import struct
import ctypes
from comtypes import COMError
import pythoncom
import win32clipboard
import oleTypes
import colors
import globalVars
import eventHandler
import comInterfaces.tom
from logHandler import log
import languageHandler
import config
import speech
import winKernel
import api
import winUser
import textInfos.offsets
from keyboardHandler import KeyboardInputGesture
from scriptHandler import isScriptWaiting
import IAccessibleHandler
import controlTypes
from . import Window
from .. import NVDAObjectTextInfo
from ..behaviors import EditableTextWithAutoSelectDetection
import braille
import watchdog

selOffsetsAtLastCaretEvent=None

TA_BOTTOM=8

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
CFE_AUTOBACKCOLOR=0x4000000
CFE_AUTOCOLOR=0x40000000
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

class EditTextInfo(textInfos.offsets.OffsetsTextInfo):

	def _getPointFromOffset(self,offset):
		if self.obj.editAPIVersion==1 or self.obj.editAPIVersion>=3:
			processHandle=self.obj.processHandle
			internalP=winKernel.virtualAllocEx(processHandle,None,ctypes.sizeof(PointLStruct),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
			try:
				p=PointLStruct(0,0)
				winKernel.writeProcessMemory(processHandle,internalP,ctypes.byref(p),ctypes.sizeof(p),None)
				watchdog.cancellableSendMessage(self.obj.windowHandle,winUser.EM_POSFROMCHAR,internalP,offset)
				winKernel.readProcessMemory(processHandle,internalP,ctypes.byref(p),ctypes.sizeof(p),None)
			finally:
				winKernel.virtualFreeEx(processHandle,internalP,0,winKernel.MEM_RELEASE)
			point=textInfos.Point(p.x,p.y)
		else:
			res=watchdog.cancellableSendMessage(self.obj.windowHandle,winUser.EM_POSFROMCHAR,offset,None)
			point=textInfos.Point(winUser.GET_X_LPARAM(res),winUser.GET_Y_LPARAM(res))
		if -1 in (point.x, point.y):
			raise LookupError("Point with client coordinates x=%d, y=%d not within client area of object" %
				(point.x, point.y))
		point.x, point.y = winUser.ClientToScreen(self.obj.windowHandle, point.x, point.y)
		return point


	def _getOffsetFromPoint(self,x,y):
		x, y = winUser.ScreenToClient(self.obj.windowHandle, x, y)
		if self.obj.editAPIVersion>=1:
			processHandle=self.obj.processHandle
			internalP=winKernel.virtualAllocEx(processHandle,None,ctypes.sizeof(PointLStruct),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
			try:
				p=PointLStruct(x,y)
				winKernel.writeProcessMemory(processHandle,internalP,ctypes.byref(p),ctypes.sizeof(p),None)
				offset=watchdog.cancellableSendMessage(self.obj.windowHandle,winUser.EM_CHARFROMPOS,0,internalP)
			finally:
				winKernel.virtualFreeEx(processHandle,internalP,0,winKernel.MEM_RELEASE)
		else:
			p=x+(y<<16)
			res=watchdog.cancellableSendMessage(self.obj.windowHandle,winUser.EM_CHARFROMPOS,0,p)
			offset=winUser.LOWORD(res)
			lineNum=winUser.HIWORD(res)
			if offset==0xFFFF and lineNum==0xFFFF:
				raise LookupError("Point outside client area")
			if self._getStoryLength() > 0xFFFF:
				# Returned offsets are 16 bits, therefore for large documents, we need to make sure that the correct offset is returned.
				# We can calculate this by using the start offset of the line with the retrieved line number.
				lineStart=watchdog.cancellableSendMessage(self.obj.windowHandle,winUser.EM_LINEINDEX,lineNum,0)
				# Get the last 16 bits of the line number
				lineStart16=lineStart&0xFFFF
				if lineStart16 > offset:
					# There are cases where the last 16 bits of the line start are greather than the 16 bits offset.
					# For example, this happens when the line start offset is 65534 (0xFFFE)
					# and the offset we need ought to be 65537 (0x10001), which is a 17 bits number
					# In that case, add 0x10000 to the offset, which will make the eventual formula return the correct offset,
					# unless a line has more than 65535 characters, in which case we can't get a reliable offset.
					offset+=0x10000
				offset = (offset - lineStart16) + lineStart
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
		try:
			winKernel.writeProcessMemory(processHandle,internalCharFormat,ctypes.byref(charFormat),ctypes.sizeof(charFormat),None)
			watchdog.cancellableSendMessage(self.obj.windowHandle,EM_GETCHARFORMAT,SCF_SELECTION, internalCharFormat)
			winKernel.readProcessMemory(processHandle,internalCharFormat,ctypes.byref(charFormat),ctypes.sizeof(charFormat),None)
		finally:
			winKernel.virtualFreeEx(processHandle,internalCharFormat,0,winKernel.MEM_RELEASE)
		if oldSel!=(offset,offset+1):
			self._setSelectionOffsets(oldSel[0],oldSel[1])
		return charFormat

	def _getFormatFieldAndOffsets(self,offset,formatConfig,calculateOffsets=True):
		#Basic edit fields do not support formatting at all.
		# Formatting for unidentified edit fields is ignored.
		# Note that unidentified rich edit fields will most likely use L{ITextDocumentTextInfo}.
		if self.obj.editAPIVersion<1:
			return super(EditTextInfo,self)._getFormatFieldAndOffsets(offset,formatConfig,calculateOffsets=calculateOffsets)
		if calculateOffsets:
			startOffset,endOffset=self._getWordOffsets(offset)
		else:
			startOffset,endOffset=self._startOffset,self._endOffset
		formatField=textInfos.FormatField()
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
		if formatConfig["reportColor"]:
			if charFormat is None: charFormat=self._getCharFormat(offset)
			formatField["color"]=colors.RGB.fromCOLORREF(charFormat.crTextColor) if not charFormat.dwEffects&CFE_AUTOCOLOR else _("default color")
			formatField["background-color"]=colors.RGB.fromCOLORREF(charFormat.crBackColor) if not charFormat.dwEffects&CFE_AUTOBACKCOLOR else _("default color")
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
			try:
				watchdog.cancellableSendMessage(self.obj.windowHandle,EM_EXGETSEL,0, internalCharRange)
				winKernel.readProcessMemory(processHandle,internalCharRange,ctypes.byref(charRange),ctypes.sizeof(charRange),None)
			finally:
				winKernel.virtualFreeEx(processHandle,internalCharRange,0,winKernel.MEM_RELEASE)
			return (charRange.cpMin,charRange.cpMax)
		else:
			start=ctypes.c_uint()
			end=ctypes.c_uint()
			res=watchdog.cancellableSendMessage(self.obj.windowHandle,winUser.EM_GETSEL,ctypes.byref(start),ctypes.byref(end))
			return start.value,end.value

	def _setSelectionOffsets(self,start,end):
		if self.obj.editAPIVersion>=1:
			charRange=CharRangeStruct()
			charRange.cpMin=start
			charRange.cpMax=end
			processHandle=self.obj.processHandle
			internalCharRange=winKernel.virtualAllocEx(processHandle,None,ctypes.sizeof(charRange),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
			try:
				winKernel.writeProcessMemory(processHandle,internalCharRange,ctypes.byref(charRange),ctypes.sizeof(charRange),None)
				watchdog.cancellableSendMessage(self.obj.windowHandle,EM_EXSETSEL,0, internalCharRange)
			finally:
				winKernel.virtualFreeEx(processHandle,internalCharRange,0,winKernel.MEM_RELEASE)
		else:
			watchdog.cancellableSendMessage(self.obj.windowHandle,winUser.EM_SETSEL,start,end)
		#Make sure the Window is always scrolled to the caret
		watchdog.cancellableSendMessage(self.obj.windowHandle,winUser.EM_SCROLLCARET,0,0)

	def _getCaretOffset(self):
		return self._getSelectionOffsets()[0]

	def _setCaretOffset(self,offset):
		return self._setSelectionOffsets(offset,offset)

	def _getStoryText(self):
		if controlTypes.STATE_PROTECTED in self.obj.states:
			return u'*'*(self._getStoryLength()-1)
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
			try:
				winKernel.writeProcessMemory(processHandle,internalInfo,ctypes.byref(info),ctypes.sizeof(info),None)
				textLen=watchdog.cancellableSendMessage(self.obj.windowHandle,EM_GETTEXTLENGTHEX,internalInfo,0)
			finally:
				winKernel.virtualFreeEx(processHandle,internalInfo,0,winKernel.MEM_RELEASE)
			return textLen+1
		else:
			return watchdog.cancellableSendMessage(self.obj.windowHandle,winUser.WM_GETTEXTLENGTH,0,0)+1

	def _getLineCount(self):
		return self.obj.windowTextLineCount

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
			try:
				textRange.lpstrText=internalBuf
				internalTextRange=winKernel.virtualAllocEx(processHandle,None,ctypes.sizeof(textRange),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
				try:
					winKernel.writeProcessMemory(processHandle,internalTextRange,ctypes.byref(textRange),ctypes.sizeof(textRange),None)
					res=watchdog.cancellableSendMessage(self.obj.windowHandle,EM_GETTEXTRANGE,0,internalTextRange)
				finally:
					winKernel.virtualFreeEx(processHandle,internalTextRange,0,winKernel.MEM_RELEASE)
				buf=(ctypes.c_byte*bufLen)()
				winKernel.readProcessMemory(processHandle,internalBuf,buf,bufLen,None)
			finally:
				winKernel.virtualFreeEx(processHandle,internalBuf,0,winKernel.MEM_RELEASE)
			if self.obj.isWindowUnicode or (res>1 and (buf[res]!=0 or buf[res+1]!=0)): 
				text=ctypes.cast(buf,ctypes.c_wchar_p).value
			else:
				text=unicode(ctypes.cast(buf,ctypes.c_char_p).value, errors="replace", encoding=locale.getlocale()[1])
			# #4095: Some protected richEdit controls do not hide their password characters.
			# We do this specifically.
			# Note that protected standard edit controls get characters hidden in _getStoryText.
			if text and controlTypes.STATE_PROTECTED in self.obj.states:
				text=u'*'*len(text)
		else:
			text=self._getStoryText()[start:end]
		return text

	def _getWordOffsets(self,offset):
		if self.obj.editAPIVersion>=2:
			start=watchdog.cancellableSendMessage(self.obj.windowHandle,EM_FINDWORDBREAK,WB_MOVEWORDLEFT,offset)
			end=watchdog.cancellableSendMessage(self.obj.windowHandle,EM_FINDWORDBREAK,WB_MOVEWORDRIGHT,start)
			if end<=offset:
				start=end
				end=watchdog.cancellableSendMessage(self.obj.windowHandle,EM_FINDWORDBREAK,WB_MOVEWORDRIGHT,offset)
			return (start,end)
		else:
			if self._getTextRange(offset,offset+1) in ['\r','\n']:
				return offset,offset+1
			else:
				return super(EditTextInfo,self)._getWordOffsets(offset)


	def _getLineNumFromOffset(self,offset):
		if self.obj.editAPIVersion>=1:
			res=watchdog.cancellableSendMessage(self.obj.windowHandle,EM_EXLINEFROMCHAR,0,offset)
			return res
		else:
			return watchdog.cancellableSendMessage(self.obj.windowHandle,winUser.EM_LINEFROMCHAR,offset,0)

	def _getLineOffsets(self,offset):
		lineNum=self._getLineNumFromOffset(offset)
		start=watchdog.cancellableSendMessage(self.obj.windowHandle,winUser.EM_LINEINDEX,lineNum,0)
		length=watchdog.cancellableSendMessage(self.obj.windowHandle,winUser.EM_LINELENGTH,offset,0)
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
	comInterfaces.tom.tomCharacter:textInfos.UNIT_CHARACTER,
	comInterfaces.tom.tomWord:textInfos.UNIT_WORD,
	comInterfaces.tom.tomLine:textInfos.UNIT_LINE,
	comInterfaces.tom.tomSentence:textInfos.UNIT_SENTENCE,
	comInterfaces.tom.tomParagraph:textInfos.UNIT_PARAGRAPH,
	comInterfaces.tom.tomStory:textInfos.UNIT_STORY,
}

NVDAUnitsToITextDocumentUnits={
	textInfos.UNIT_CHARACTER:comInterfaces.tom.tomCharacter,
	textInfos.UNIT_WORD:comInterfaces.tom.tomWord,
	textInfos.UNIT_LINE:comInterfaces.tom.tomLine,
	textInfos.UNIT_SENTENCE:comInterfaces.tom.tomSentence,
	textInfos.UNIT_PARAGRAPH:comInterfaces.tom.tomParagraph,
	textInfos.UNIT_STORY:comInterfaces.tom.tomStory,
	textInfos.UNIT_READINGCHUNK:comInterfaces.tom.tomSentence,
}

class ITextDocumentTextInfo(textInfos.TextInfo):

	def _get_pointAtStart(self):
		p=textInfos.Point(0,0)
		(p.x,p.y)=self._rangeObj.GetPoint(comInterfaces.tom.tomStart)
		if p.x and p.y:
			return p
		else:
			raise NotImplementedError

	def _getFormatFieldAtRange(self,range,formatConfig):
		formatField=textInfos.FormatField()
		fontObj=None
		paraFormatObj=None
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
			linkRange=range.Duplicate
			linkRange.Collapse(comInterfaces.tom.tomStart)
			formatField["link"]=linkRange.Expand(comInterfaces.tom.tomLink)>0
		if formatConfig["reportColor"]:
			if not fontObj: fontObj=range.font
			fgColor=fontObj.foreColor
			if fgColor==comInterfaces.tom.tomAutoColor:
				# Translators: The default color of text when a color has not been set by the author. 
				formatField['color']=_("default color")
			elif fgColor&0xff000000:
				# The color is a palet index (we don't know the palet)
				# Translators: The color of text cannot be detected. 
				formatField['color']=_("Unknown color")
			else:
				formatField["color"]=colors.RGB.fromCOLORREF(fgColor)
			bkColor=fontObj.backColor
			if bkColor==comInterfaces.tom.tomAutoColor:
				# Translators: The default background color  when a color has not been set by the author. 
				formatField['background-color']=_("default color")
			elif bkColor&0xff000000:
				# The color is a palet index (we don't know the palet)
				# Translators: The background color cannot be detected. 
				formatField['background-color']=_("Unknown color")
			else:
				formatField["background-color"]=colors.RGB.fromCOLORREF(bkColor)
		if not fontObj: fontObj=range.font
		try:
			langId = fontObj.languageID
			if langId:
				formatField['language']=languageHandler.windowsLCIDToLocaleName(langId)
		except:
			log.debugWarning("language error",exc_info=True)
			pass
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

	def _getEmbeddedObjectLabel(self,embedRangeObj):
		label=None
		try:
			o=embedRangeObj.GetEmbeddedObject()
		except comtypes.COMError:
			o=None
		if not o:
			return None
		# Outlook >=2007 exposes MSAA on its embedded objects thus we can use accName as the label
		import oleacc
		try:
			label=o.QueryInterface(oleacc.IAccessible).accName(0);
		except comtypes.COMError:
			pass
		if label:
			return label
		# Outlook 2003 and Outlook Express write the embedded object text to the display with GDI thus we can use display model 
		left,top=embedRangeObj.GetPoint(comInterfaces.tom.tomStart)
		right,bottom=embedRangeObj.GetPoint(comInterfaces.tom.tomEnd|TA_BOTTOM)
		# Outlook Express bug: when expanding to the first embedded object on lines after the first, the range's start coordinates are the start coordinates of the previous character (on the line above)
		# Therefore if we detect this, collapse the range and try getting left and top again
		if left>=right:
			r=embedRangeObj.duplicate
			r.collapse(1)
			left,top=r.GetPoint(comInterfaces.tom.tomStart)
		import displayModel
		label=displayModel.DisplayModelTextInfo(self.obj, textInfos.Rect(left, top, right, bottom)).text
		if label and not label.isspace():
			return label
		# Windows Live Mail exposes the label via the embedded object's data (IDataObject)
		try:
			dataObj=o.QueryInterface(oleTypes.IDataObject)
		except comtypes.COMError:
			dataObj=None
		if dataObj:
			try:
				dataObj=pythoncom._univgw.interface(hash(dataObj),pythoncom.IID_IDataObject)
				format=(win32clipboard.CF_UNICODETEXT, None, pythoncom.DVASPECT_CONTENT, -1, pythoncom.TYMED_HGLOBAL)
				medium=dataObj.GetData(format)
				buf=ctypes.create_string_buffer(medium.data)
				buf=ctypes.cast(buf,ctypes.c_wchar_p)
				label=buf.value
			except:
				pass
		if label:
			return label
		# As a final fallback (e.g. could not get display  model text for Outlook Express), use the embedded object's user type (e.g. "recipient").
		try:
			oleObj=o.QueryInterface(oleTypes.IOleObject)
			label=oleObj.GetUserType(1)
		except comtypes.COMError:
			pass
		return label

	def _getTextAtRange(self,rangeObj):
		embedRangeObj=None
		bufText=rangeObj.text
		if not bufText:
			return u""
		if controlTypes.STATE_PROTECTED in self.obj.states:
			return u'*'*len(bufText)
		newTextList=[]
		start=rangeObj.start
		for offset in xrange(len(bufText)):
			if ord(bufText[offset])==0xfffc:
				if embedRangeObj is None: embedRangeObj=rangeObj.duplicate
				embedRangeObj.setRange(start+offset,start+offset+1)
				label=self._getEmbeddedObjectLabel(embedRangeObj)
				if label:
					newTextList.append(label)
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
		if isinstance(position,textInfos.Point):
			self._rangeObj=self.obj.ITextDocumentObject.rangeFromPoint(position.x,position.y)
		elif position==textInfos.POSITION_ALL:
			self._rangeObj=self.obj.ITextDocumentObject.range(0,0)
			self._rangeObj.expand(comInterfaces.tom.tomStory)
		elif position==textInfos.POSITION_SELECTION:
			self._rangeObj=self.obj.ITextSelectionObject.duplicate
		elif position==textInfos.POSITION_CARET:
			self._rangeObj=self.obj.ITextSelectionObject.duplicate
			self._rangeObj.Collapse(True)
		elif position==textInfos.POSITION_FIRST:
			self._rangeObj=self.obj.ITextDocumentObject.range(0,0)
		elif position==textInfos.POSITION_LAST:
			self._rangeObj=self.obj.ITextDocumentObject.range(0,0)
			self._rangeObj.move(comInterfaces.tom.tomStory,1)
			self._rangeObj.moveStart(comInterfaces.tom.tomCharacter,-1)
		elif isinstance(position,textInfos.offsets.Offsets):
			self._rangeObj=self.obj.ITextDocumentObject.range(position.startOffset,position.endOffset)
		else:
			raise NotImplementedError("position: %s"%position)

	def getTextWithFields(self,formatConfig=None):
		if not formatConfig:
			formatConfig=config.conf["documentFormatting"]
		range=self._rangeObj.duplicate
		range.collapse(True)
		if not formatConfig["detectFormatAfterCursor"]:
			range.expand(comInterfaces.tom.tomCharacter)
			return [textInfos.FieldCommand("formatChange",self._getFormatFieldAtRange(range,formatConfig)),
				self._getTextAtRange(self._rangeObj)]
		commandList=[]
		endLimit=self._rangeObj.end
		while range.end<endLimit:
			self._expandFormatRange(range,formatConfig)
			commandList.append(textInfos.FieldCommand("formatChange",self._getFormatFieldAtRange(range,formatConfig)))
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
		return textInfos.offsets.Offsets(self._rangeObj.start,self._rangeObj.end)

	def updateCaret(self):
		self.obj.ITextSelectionObject.start=self.obj.ITextSelectionObject.end=self._rangeObj.start

	def updateSelection(self):
		self.obj.ITextSelectionObject.start=self._rangeObj.start
		self.obj.ITextSelectionObject.end=self._rangeObj.end

class Edit(EditableTextWithAutoSelectDetection, Window):

	editAPIVersion=0
	editValueUnit=textInfos.UNIT_LINE

	def _get_TextInfo(self):
		if self.editAPIVersion!=0 and self.ITextDocumentObject:
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
		global selOffsetsAtLastCaretEvent
		#Fetching formatting and calculating word offsets needs to move the caret, so try to ignore these events
		selOffsets=self.makeTextInfo(textInfos.POSITION_SELECTION).bookmark
		if selOffsets==selOffsetsAtLastCaretEvent:
			return
		selOffsetsAtLastCaretEvent=selOffsets
		#Make sure that this object *really* has the focus before bothering to speak any possible selection change
		api.processPendingEvents()
		if self is not api.getFocusObject() or eventHandler.isPendingEvents('gainFocus'):
			return
		if eventHandler.isPendingEvents('valueChange',self):
			self.hasContentChangedSinceLastSelection=True
		super(Edit,self).event_caret()

	def event_valueChange(self):
		self.event_textChange()

	def _get_states(self):
		states = super(Edit, self)._get_states()
		if self.windowStyle & winUser.ES_MULTILINE:
			states.add(controlTypes.STATE_MULTILINE)
		return states

class RichEdit(Edit):
	editAPIVersion=1

	def makeTextInfo(self,position):
		if self.TextInfo is not ITextDocumentTextInfo:
			return super(RichEdit,self).makeTextInfo(position)
		# #4090: Sometimes ITextDocument support can fail (security restrictions in Outlook 2010)
		# We then fall back to normal Edit support.
		try:
			return self.TextInfo(self,position)
		except COMError:
			log.debugWarning("Could not instanciate ITextDocumentTextInfo",exc_info=True)
			self.TextInfo=EditTextInfo
			return self.TextInfo(self,position)

class RichEdit20(RichEdit):
	editAPIVersion=2

class RichEdit30(RichEdit):
	editAPIVersion=3

class RichEdit50(RichEdit):
	editAPIVersion=5

class UnidentifiedEdit(RichEdit):
	"""
	An edit control for which the edit API version is unknown.
	This class inherrits from L{RichEdit} to ensure L{ITextDocumentTextInfo} initialization failure is handled correctly.
	"""
	editAPIVersion=-1
