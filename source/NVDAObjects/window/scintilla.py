# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2007-2022 NV Access Limited, Arnold Loubriat, Babbage B.V., Łukasz Golonka, Joseph Lee,
# Peter Vágner
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import ctypes
import textInfos.offsets
import winKernel
import winUser
import controlTypes
from . import Window
from ..behaviors import EditableTextWithAutoSelectDetection
import watchdog
import eventHandler
import locationHelper
import textUtils

# Window messages
SCI_POSITIONFROMPOINT=2022
SCI_POINTXFROMPOSITION=2164
SCI_POINTYFROMPOSITION=2165
SCI_GETTEXTRANGE=2162
SCI_GETTEXT=2182
SCI_GETTEXTLENGTH=2183
SCI_GETLENGTH=2006
SCI_GETCURRENTPOS=2008
SCI_GETANCHOR=2009
SCI_GOTOPOS=2025
SCI_SETCURRENTPOS=2141
SCI_GETSELECTIONSTART=2143
SCI_GETSELECTIONEND=2145
SCI_SETSEL=2160
SCI_GETLINEENDPOSITION=2136
SCI_GETLINECOUNT=2154
SCI_LINEFROMPOSITION=2166
SCI_POSITIONFROMLINE=2167
SCI_LINELENGTH=2350
SCI_GETSTYLEAT=2010
SCI_GETCHARAT = 2007
SCI_STYLEGETFONT=2486
SCI_STYLEGETSIZE=2485
SCI_STYLEGETBOLD=2483
SCI_STYLEGETITALIC=2484
SCI_STYLEGETUNDERLINE=2488
SCI_WORDSTARTPOSITION=2266
SCI_WORDENDPOSITION=2267
SC_WRAP_NONE=0
SCI_GETWRAPMODE=2269
SCI_GETCODEPAGE=2137
SCI_POSITIONAFTER=2418

#constants
#: Represents an invalid position within a document.
INVALID_POSITION=-1
STYLE_DEFAULT=32
SC_CP_UTF8=65001
space = 32

class CharacterRangeStruct(ctypes.Structure):
	_fields_=[
		('cpMin',ctypes.c_long),
		('cpMax',ctypes.c_long),
	]


class ScintillaTextInfo(textInfos.offsets.OffsetsTextInfo):

	class TextRangeStruct(ctypes.Structure):
		_fields_ = [
			('chrg', CharacterRangeStruct),
			('lpstrText', ctypes.c_char_p),
		]

	def _get_encoding(self):
		cp=watchdog.cancellableSendMessage(self.obj.windowHandle,SCI_GETCODEPAGE,0,0)
		if cp==SC_CP_UTF8:
			return "utf-8"
		else:
			return textUtils.USER_ANSI_CODE_PAGE

	def _getOffsetFromPoint(self,x,y):
		x, y = winUser.ScreenToClient(self.obj.windowHandle, x, y)
		return watchdog.cancellableSendMessage(self.obj.windowHandle,SCI_POSITIONFROMPOINT,x,y)

	def _getPointFromOffset(self,offset):
		point=locationHelper.Point(
			watchdog.cancellableSendMessage(self.obj.windowHandle,SCI_POINTXFROMPOSITION,None,offset),
			watchdog.cancellableSendMessage(self.obj.windowHandle,SCI_POINTYFROMPOSITION,None,offset)
		).toScreen(self.obj.windowHandle)
		if point.x is not None and point.y is not None:
			return point
		else:
			raise NotImplementedError

	def _getFormatFieldAndOffsets(self,offset,formatConfig,calculateOffsets=True):
		style=watchdog.cancellableSendMessage(self.obj.windowHandle,SCI_GETSTYLEAT,offset,0)
		if calculateOffsets:
			#we need to manually see how far the style goes, limit to line
			lineStart,lineEnd=self._getLineOffsets(offset)
			startOffset=offset
			while startOffset>lineStart:
				curStyle=watchdog.cancellableSendMessage(self.obj.windowHandle,SCI_GETSTYLEAT,startOffset-1,0)
				if curStyle==style:
					startOffset-=1
				else:
					break
			endOffset=offset+1
			while endOffset<lineEnd:
				curStyle=watchdog.cancellableSendMessage(self.obj.windowHandle,SCI_GETSTYLEAT,endOffset,0)
				if curStyle==style:
					endOffset+=1
				else:
					break
		else:
			startOffset,endOffset=(self._startOffset,self._endOffset)
		formatField=textInfos.FormatField()
		if formatConfig["reportFontName"]:
			#To get font name, We need to allocate memory with in Scintilla's process, and then copy it out
			fontNameBuf=ctypes.create_string_buffer(32)
			internalBuf=winKernel.virtualAllocEx(self.obj.processHandle,None,len(fontNameBuf),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
			try:
				watchdog.cancellableSendMessage(self.obj.windowHandle,SCI_STYLEGETFONT,style, internalBuf)
				winKernel.readProcessMemory(self.obj.processHandle,internalBuf,fontNameBuf,len(fontNameBuf),None)
			finally:
				winKernel.virtualFreeEx(self.obj.processHandle,internalBuf,0,winKernel.MEM_RELEASE)
			formatField["font-name"]=fontNameBuf.value.decode("utf-8")
		if formatConfig["reportFontSize"]:
			formatField["font-size"]="%spt"%watchdog.cancellableSendMessage(self.obj.windowHandle,SCI_STYLEGETSIZE,style,0)
		if formatConfig["reportLineNumber"]:
			formatField["line-number"]=self._getLineNumFromOffset(offset)+1
		if formatConfig["reportFontAttributes"]:
			formatField["bold"]=bool(watchdog.cancellableSendMessage(self.obj.windowHandle,SCI_STYLEGETBOLD,style,0))
			formatField["italic"]=bool(watchdog.cancellableSendMessage(self.obj.windowHandle,SCI_STYLEGETITALIC,style,0))
			formatField["underline"]=bool(watchdog.cancellableSendMessage(self.obj.windowHandle,SCI_STYLEGETUNDERLINE,style,0))
		return formatField,(startOffset,endOffset)

	def _getCaretOffset(self):
		return watchdog.cancellableSendMessage(self.obj.windowHandle,SCI_GETCURRENTPOS,0,0)

	def _setCaretOffset(self,offset):
		watchdog.cancellableSendMessage(self.obj.windowHandle,SCI_GOTOPOS,offset,0)
		# #5678: A caret event sometimes doesn't get fired when we do this,
		# so fake one just in case.
		eventHandler.executeEvent("caret", self.obj)

	def _getSelectionOffsets(self):
		start=watchdog.cancellableSendMessage(self.obj.windowHandle,SCI_GETSELECTIONSTART,0,0)
		end=watchdog.cancellableSendMessage(self.obj.windowHandle,SCI_GETSELECTIONEND,0,0)
		return (start,end)

	def _setSelectionOffsets(self,start,end):
		watchdog.cancellableSendMessage(self.obj.windowHandle,SCI_SETSEL,start,end)

	def _getStoryText(self):
		if not hasattr(self,'_storyText'):
			storyLength=self._getStoryLength()
			self._storyText=self._getTextRange(0,storyLength)
		return self._storyText

	def _getStoryLength(self):
		if not hasattr(self,'_storyLength'):
			self._storyLength=watchdog.cancellableSendMessage(self.obj.windowHandle,SCI_GETTEXTLENGTH,0,0)
		return self._storyLength

	def _getLineCount(self):
		return watchdog.cancellableSendMessage(self.obj.windowHandle,SCI_GETLINECOUNT,0,0)

	def _getTextRange(self,start,end):
		bufLen = (end - start) + 1
		textRange = self.TextRangeStruct()
		textRange.chrg.cpMin = start
		textRange.chrg.cpMax = end
		processHandle = self.obj.processHandle
		internalBuf = winKernel.virtualAllocEx(processHandle, None, bufLen, winKernel.MEM_COMMIT, winKernel.PAGE_READWRITE)
		try:
			textRange.lpstrText = internalBuf
			internalTextRange = winKernel.virtualAllocEx(processHandle, None, ctypes.sizeof(textRange), winKernel.MEM_COMMIT, winKernel.PAGE_READWRITE)
			try:
				winKernel.writeProcessMemory(processHandle, internalTextRange, ctypes.byref(textRange), ctypes.sizeof(textRange), None)
				numBytes = watchdog.cancellableSendMessage(self.obj.windowHandle, SCI_GETTEXTRANGE, 0, internalTextRange)
			finally:
				winKernel.virtualFreeEx(processHandle, internalTextRange, 0, winKernel.MEM_RELEASE)
			buf = ctypes.create_string_buffer(bufLen)
			winKernel.readProcessMemory(processHandle, internalBuf, buf, bufLen, None)
		finally:
			winKernel.virtualFreeEx(processHandle, internalBuf, 0, winKernel.MEM_RELEASE)
		return textUtils.getTextFromRawBytes(buf.raw, numChars=numBytes, encoding=self.encoding, errorsFallback="surrogateescape")

	def _getWordOffsets(self,offset):
		start=watchdog.cancellableSendMessage(self.obj.windowHandle,SCI_WORDSTARTPOSITION,offset,0)
		end=watchdog.cancellableSendMessage(self.obj.windowHandle,SCI_WORDENDPOSITION,start,0)
		if end<=offset:
			start=end
			end=watchdog.cancellableSendMessage(self.obj.windowHandle,SCI_WORDENDPOSITION,offset,0)
		# #8295: When calculating offsets with Scintilla messages spaces are considered to be words.
		# Therefore check if character at offset is  a space, and if so calculate it again.
		if watchdog.cancellableSendMessage(self.obj.windowHandle, SCI_GETCHARAT, end, 0) == space:
			end = watchdog.cancellableSendMessage(self.obj.windowHandle, SCI_WORDENDPOSITION, end, 0)
		if watchdog.cancellableSendMessage(self.obj.windowHandle, SCI_GETCHARAT, start, 0) == space:
			start = watchdog.cancellableSendMessage(self.obj.windowHandle, SCI_WORDSTARTPOSITION, start, 0)
		return [start,end]

	def _getLineNumFromOffset(self,offset):
		return watchdog.cancellableSendMessage(self.obj.windowHandle,SCI_LINEFROMPOSITION,offset,0)

	def _getLineOffsets(self,offset):
		if watchdog.cancellableSendMessage(self.obj.windowHandle,SCI_GETWRAPMODE,None,None)!=SC_WRAP_NONE:
			# Lines in Scintilla refer to document lines, not wrapped lines.
			# There's no way to retrieve wrapped lines, so use screen coordinates.
			y = self._getPointFromOffset(offset).y
			location=self.obj.location
			start = self._getOffsetFromPoint(location.left, y)
			end=self._getOffsetFromPoint(location.right, y)
			# If this line wraps to the next line,
			# end is the first offset of the next line.
			if self._getPointFromOffset(end).y==y:
				# This is the end of the document line.
				# Include the EOL characters in the returned offsets.
				end=watchdog.cancellableSendMessage(self.obj.windowHandle,SCI_POSITIONAFTER,end,None)
			return (start,end)

		line=watchdog.cancellableSendMessage(self.obj.windowHandle,SCI_LINEFROMPOSITION,offset,0)
		start=watchdog.cancellableSendMessage(self.obj.windowHandle,SCI_POSITIONFROMLINE,line,0)
		end=start+watchdog.cancellableSendMessage(self.obj.windowHandle,SCI_LINELENGTH,line,0)
		return (start,end)

	def _getParagraphOffsets(self,offset):
		return self._getLineOffsets(offset)

	def _getCharacterOffsets(self,offset):
		if offset>=self._getStoryLength(): return offset,offset+1
		end=watchdog.cancellableSendMessage(self.obj.windowHandle,SCI_POSITIONAFTER,offset,0)
		start=offset
		tempOffset=offset-1
		
		while tempOffset > INVALID_POSITION:
			start=watchdog.cancellableSendMessage(self.obj.windowHandle,SCI_POSITIONAFTER,tempOffset,0)
			if start<end:
				break
			elif tempOffset==0:
				start=tempOffset
				break
			else:
				tempOffset-=1
		return [start,end]


#The Scintilla NVDA object, inherists the generic MSAA NVDA object
class Scintilla(EditableTextWithAutoSelectDetection, Window):

	TextInfo=ScintillaTextInfo

#The name of the object is gotten by the standard way of getting a window name, can't use MSAA name (since it contains all the text)
	def _get_name(self):
		return winUser.getWindowText(self.windowHandle)

#The role of the object should be editable text
	def _get_role(self):
		return controlTypes.Role.EDITABLETEXT

	def _get_states(self):
		states = super(Scintilla, self)._get_states()
		# Scintilla controls are always multiline.
		states.add(controlTypes.State.MULTILINE)
		return states
