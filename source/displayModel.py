# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2006-2021 NV Access Limited, Babbage B.V., Joseph Lee

import ctypes
from ctypes import *
from ctypes.wintypes import RECT
from comtypes import BSTR
import unicodedata
import math
import colors
import XMLFormatting
import api
import winUser
import mouseHandler
import NVDAHelper
import textInfos
from textInfos.offsets import OffsetsTextInfo
import watchdog
from logHandler import log
import windowUtils
from locationHelper import RectLTRB, RectLTWH
import textUtils
from typing import (
	Union,
	List,
	Tuple,
	Optional,
	Dict
)

#: A text info unit constant for a single chunk in a display model
UNIT_DISPLAYCHUNK = "displayChunk"


def wcharToInt(c):
	i=ord(c)
	return c_short(i).value

def detectStringDirection(s):
	direction=0
	for b in (unicodedata.bidirectional(ch) for ch in s):
		if b=='L': direction+=1
		if b in ('R','AL'): direction-=1
	return direction

def normalizeRtlString(s):
	l=[]
	for c in s:
		#If this is an arabic presentation form b character (commenly given by Windows when converting from glyphs)
		#Decompose it to its original basic arabic (non-presentational_ character.
		if 0xfe70<=ord(c)<=0xfeff:
			d=unicodedata.decomposition(c)
			d=d.split(' ') if d else None
			if d and len(d)==2 and d[0] in ('<initial>','<medial>','<final>','<isolated>'):
				c=chr(int(d[1],16))
		l.append(c)
	return u"".join(l)

def yieldListRange(l,start,stop):
	for x in range(start,stop):
		yield l[x]

def processWindowChunksInLine(commandList,rects,startIndex,startOffset,endIndex,endOffset):
	windowStartIndex=startIndex
	lastEndOffset=windowStartOffset=startOffset
	lastHwnd=None
	for index in range(startIndex,endIndex+1):
		item=commandList[index] if index<endIndex else None
		if isinstance(item,str):
			lastEndOffset += textUtils.WideStringOffsetConverter(item).wideStringLength
		else:
			hwnd=item.field['hwnd'] if item else None
			if lastHwnd is not None and hwnd!=lastHwnd:
				processFieldsAndRectsRangeReadingdirection(commandList,rects,windowStartIndex,windowStartOffset,index,lastEndOffset)
				windowStartIndex=index
				windowStartOffset=lastEndOffset
			lastHwnd=hwnd

def processFieldsAndRectsRangeReadingdirection(commandList,rects,startIndex,startOffset,endIndex,endOffset):
	containsRtl=False # True if any rtl text is found at all
	curFormatField=None 
	overallDirection=0 # The general reading direction calculated based on the amount of rtl vs ltr text there is
	# Detect the direction for fields with an unknown reading direction, and calculate an over all direction for the entire passage
	for index in range(startIndex,endIndex):
		item=commandList[index]
		if isinstance(item,textInfos.FieldCommand) and isinstance(item.field,textInfos.FormatField):
			curFormatField=item.field
		elif isinstance(item,str):
			direction=curFormatField['direction']
			if direction==0:
				curFormatField['direction']=direction=detectStringDirection(item)
			elif direction==-2: #numbers in an rtl context
				curFormatField['direction']=direction=-1
				curFormatField['shouldReverseText']=False
			if direction<0:
				containsRtl=True
			overallDirection+=direction
	if not containsRtl:
		# As no rtl text was ever seen, then there is nothing else to do
		return
	if overallDirection==0: overallDirection=1
	# following the calculated over all reading direction of the passage, correct all weak/neutral fields to have the same reading direction as the field preceeding them 
	lastDirection=overallDirection
	for index in range(startIndex,endIndex):
		if overallDirection<0: index=endIndex-index-1
		item=commandList[index]
		if isinstance(item,textInfos.FieldCommand) and isinstance(item.field,textInfos.FormatField):
			direction=item.field['direction']
			if direction==0:
				item.field['direction']=lastDirection
			lastDirection=direction
	# For fields that are rtl, reverse their text, their rects, and the order of consecutive rtl fields 
	lastEndOffset=startOffset
	runDirection=None
	runStartIndex=None
	runStartOffset=None
	if overallDirection<0:
		reorderList=[]
	for index in range(startIndex,endIndex+1):
		item=commandList[index] if index<endIndex else None
		if isinstance(item,str):
			lastEndOffset += textUtils.WideStringOffsetConverter(item).wideStringLength
		elif not item or (isinstance(item,textInfos.FieldCommand) and isinstance(item.field,textInfos.FormatField)):
			direction=item.field['direction'] if item else None
			if direction is None or (direction!=runDirection): 
				if runDirection is not None:
					# This is the end of a run of consecutive fields of the same direction
					if runDirection<0:
						#This run is rtl, so reverse its rects, the text within the fields, and the order of fields themselves
						#Reverse rects
						rects[runStartOffset:lastEndOffset]=rects[lastEndOffset-1:runStartOffset-1 if runStartOffset>0 else None:-1]
						rectsStart=runStartOffset
						for i in range(runStartIndex,index,2):
							command=commandList[i]
							text=commandList[i+1]
							rectsEnd = rectsStart + textUtils.WideStringOffsetConverter(text).wideStringLength
							commandList[i+1]=command
							shouldReverseText=command.field.get('shouldReverseText',True)
							commandList[i]=normalizeRtlString(text[::-1] if shouldReverseText else text)
							if not shouldReverseText:
								#Because all the rects in the run were already reversed, we need to undo that for this field
								rects[rectsStart:rectsEnd]=rects[rectsEnd-1:rectsStart-1 if rectsStart>0 else None:-1]
							rectsStart=rectsEnd
						#Reverse commandList
						commandList[runStartIndex:index]=commandList[index-1:runStartIndex-1 if runStartIndex>0 else None:-1]
					if overallDirection<0:
						#As the overall reading direction of the passage is rtl, record the location of this run so we can reverse the order of runs later
						reorderList.append((runStartIndex,runStartOffset,index,lastEndOffset))
				if item:
					runStartIndex=index
					runStartOffset=lastEndOffset
					runDirection=direction
	if overallDirection<0:
		# As the overall reading direction of the passage is rtl, build a new command list and rects list with the order of runs reversed
		# The content of each run is already in logical reading order itself
		newCommandList=[]
		newRects=[]
		for si,so,ei,eo in reversed(reorderList):
			newCommandList.extend(yieldListRange(commandList,si,ei))
			newRects.extend(yieldListRange(rects,so,eo))
		# Update the original command list and rect list replacing the old content for this passage with the reordered runs
		commandList[startIndex:endIndex]=newCommandList
		rects[startOffset:endOffset]=newRects

_getWindowTextInRect=None
_requestTextChangeNotificationsForWindow=None
#: Objects that have registered for text change notifications.
_textChangeNotificationObjs=[]

def initialize():
	global _getWindowTextInRect,_requestTextChangeNotificationsForWindow, _getFocusRect
	_getWindowTextInRect=CFUNCTYPE(c_long,c_long,c_long,c_bool,c_int,c_int,c_int,c_int,c_int,c_int,c_bool,POINTER(BSTR),POINTER(BSTR))(('displayModel_getWindowTextInRect',NVDAHelper.localLib),((1,),(1,),(1,),(1,),(1,),(1,),(1,),(1,),(1,),(1,),(2,),(2,)))
	_requestTextChangeNotificationsForWindow=NVDAHelper.localLib.displayModel_requestTextChangeNotificationsForWindow

def getCaretRect(obj):
	left = ctypes.c_long()
	top = ctypes.c_long()
	right = ctypes.c_long()
	bottom = ctypes.c_long()
	res = watchdog.cancellableExecute(
		NVDAHelper.localLib.displayModel_getCaretRect,
		obj.appModule.helperLocalBindingHandle,
		obj.windowThreadID,
		ctypes.byref(left),
		ctypes.byref(top),
		ctypes.byref(right),
		ctypes.byref(bottom)
	)
	if res != 0:
		raise RuntimeError(f"displayModel_getCaretRect failed with res {res}")
	return RectLTRB(
		left.value,
		top.value,
		right.value,
		bottom.value
	)

def getWindowTextInRect(bindingHandle, windowHandle, left, top, right, bottom,minHorizontalWhitespace,minVerticalWhitespace,stripOuterWhitespace=True,includeDescendantWindows=True):
	text, cpBuf = watchdog.cancellableExecute(_getWindowTextInRect, bindingHandle, windowHandle, includeDescendantWindows, left, top, right, bottom,minHorizontalWhitespace,minVerticalWhitespace,stripOuterWhitespace)
	if not text or not cpBuf:
		return u"",[]

	characterLocations = []
	cpBufIt = iter(cpBuf)
	for cp in cpBufIt:
		left, top, right, bottom = (
			wcharToInt(cp),
			wcharToInt(next(cpBufIt)),
			wcharToInt(next(cpBufIt)),
			wcharToInt(next(cpBufIt))
		)
		if right < left:
			left, right = right, left
		characterLocations.append(RectLTRB(left, top, right, bottom))
	return text, characterLocations

def getFocusRect(obj):
	left=c_long()
	top=c_long()
	right=c_long()
	bottom=c_long()
	if NVDAHelper.localLib.displayModel_getFocusRect(obj.appModule.helperLocalBindingHandle,obj.windowHandle,byref(left),byref(top),byref(right),byref(bottom))==0:
		return left.value,top.value,right.value,bottom.value
	return None

def requestTextChangeNotifications(obj, enable):
	"""Request or cancel notifications for when the display text changes in an NVDAObject.
	A textChange event (event_textChange) will be fired on the object when its text changes.
	Note that this event does not provide any information about the changed text itself.
	It is important to request that notifications be cancelled when you no longer require them or when the object is no longer in use,
	as otherwise, resources will not be released.
	@param obj: The NVDAObject for which text change notifications are desired.
	@type obj: NVDAObject
	@param enable: C{True} to enable notifications, C{False} to disable them.
	@type enable: bool
	"""
	if not enable:
		_textChangeNotificationObjs.remove(obj)
	watchdog.cancellableExecute(_requestTextChangeNotificationsForWindow, obj.appModule.helperLocalBindingHandle, obj.windowHandle, enable)
	if enable:
		_textChangeNotificationObjs.append(obj)

def textChangeNotify(windowHandle, left, top, right, bottom):
	for obj in _textChangeNotificationObjs:
		if windowHandle == obj.windowHandle:
			# It is safe to call this event from this RPC thread.
			# This avoids an extra core cycle.
			obj.event_textChange()

class DisplayModelTextInfo(OffsetsTextInfo):

	minHorizontalWhitespace=8
	minVerticalWhitespace=32
	stripOuterWhitespace=True
	includeDescendantWindows=True

	def _get_backgroundSelectionColor(self):
		self.backgroundSelectionColor=colors.RGB.fromCOLORREF(winUser.user32.GetSysColor(13))
		return self.backgroundSelectionColor

	def _get_foregroundSelectionColor(self):
		self.foregroundSelectionColor=colors.RGB.fromCOLORREF(winUser.user32.GetSysColor(14))
		return self.foregroundSelectionColor

	def _getSelectionOffsets(self):
		if self.backgroundSelectionColor is not None and self.foregroundSelectionColor is not None:
			fields=self._storyFieldsAndRects[0]
			startOffset=None
			endOffset=None
			curOffset=0
			inHighlightChunk=False
			for item in fields:
				if isinstance(item,textInfos.FieldCommand) and item.command=="formatChange" and item.field.get('color',None)==self.foregroundSelectionColor and item.field.get('background-color',None)==self.backgroundSelectionColor: 
					inHighlightChunk=True
					if startOffset is None:
						startOffset=curOffset
				elif isinstance(item,str):
					curOffset += textUtils.WideStringOffsetConverter(item).wideStringLength
					if inHighlightChunk:
						endOffset=curOffset
				else:
					inHighlightChunk=False
			if startOffset is not None and endOffset is not None:
				return (startOffset,endOffset)
		raise LookupError

	def __init__(self, obj, position,limitRect=None):
		if isinstance(position, RectLTRB):
			limitRect=position
			position=textInfos.POSITION_ALL
		if limitRect is not None:
			self._location = limitRect.left, limitRect.top, limitRect.right, limitRect.bottom
		else:
			self._location = None
		super(DisplayModelTextInfo, self).__init__(obj, position)

	_cache__storyFieldsAndRects = True

	def _get__storyFieldsAndRects(self) -> Tuple[
		List[Union[str, textInfos.FieldCommand]],
		List[RectLTRB],
		List[int],
		List[int]
	]:
		# All returned coordinates are logical coordinates.
		if self._location:
			left, top, right, bottom = self._location
		else:
			try:
				left, top, width, height = self.obj.location
			except TypeError:
				# No location; nothing we can do.
				return [], [], [], []
			right = left + width
			bottom = top + height
		bindingHandle=self.obj.appModule.helperLocalBindingHandle
		if not bindingHandle:
			log.debugWarning("AppModule does not have a binding handle")
			return [], [], [], []
		left,top=windowUtils.physicalToLogicalPoint(self.obj.windowHandle,left,top)
		right,bottom=windowUtils.physicalToLogicalPoint(self.obj.windowHandle,right,bottom)
		text,rects=getWindowTextInRect(bindingHandle, self.obj.windowHandle, left, top, right, bottom, self.minHorizontalWhitespace, self.minVerticalWhitespace,self.stripOuterWhitespace,self.includeDescendantWindows)
		if not text:
			return [], [], [], []
		text="<control>%s</control>"%text
		commandList=XMLFormatting.XMLTextParser().parse(text)
		curFormatField=None
		lastEndOffset=0
		lineStartOffset=0
		lineStartIndex=0
		lineBaseline=None
		lineEndOffsets = []
		displayChunkEndOffsets = []
		for index in range(len(commandList)):
			item=commandList[index]
			if isinstance(item,str):
				lastEndOffset += textUtils.WideStringOffsetConverter(item).wideStringLength
				displayChunkEndOffsets.append(lastEndOffset)
			elif isinstance(item,textInfos.FieldCommand):
				if isinstance(item.field,textInfos.FormatField):
					curFormatField=item.field
					self._normalizeFormatField(curFormatField)
				else:
					curFormatField=None
				baseline=curFormatField['baseline'] if curFormatField  else None
				if baseline!=lineBaseline:
					if lineBaseline is not None:
						processWindowChunksInLine(commandList,rects,lineStartIndex,lineStartOffset,index,lastEndOffset)
						#Convert the whitespace at the end of the line into a line feed
						item=commandList[index-1]
						if (
							isinstance(item,str)
							# Since we're searching for white space, it is safe to
							# do this opperation on the length of the pythonic string
							and len(item)==1
							and item.isspace()
						):
							commandList[index-1]=u'\n'
						lineEndOffsets.append(lastEndOffset)
					if baseline is not None:
						lineStartIndex=index
						lineStartOffset=lastEndOffset
						lineBaseline=baseline
		return commandList, rects, lineEndOffsets, displayChunkEndOffsets

	def _getStoryOffsetLocations(self):
		baseline=None
		direction=0
		lastEndOffset=0
		commandList, rects = self._storyFieldsAndRects[:2]
		for item in commandList:
			if isinstance(item,textInfos.FieldCommand) and isinstance(item.field,textInfos.FormatField):
				baseline=item.field['baseline']
				direction=item.field['direction']
			elif isinstance(item,str):
				endOffset = lastEndOffset + textUtils.WideStringOffsetConverter(item).wideStringLength
				for rect in rects[lastEndOffset:endOffset]:
					yield rect,baseline,direction
				lastEndOffset=endOffset

	def _getFieldsInRange(self,start,end):
		storyFields=self._storyFieldsAndRects[0]
		if not storyFields:
			return []
		#Strip  unwanted commands and text from the start and the end to honour the requested offsets
		lastEndOffset=0
		startIndex=endIndex=relStart=relEnd=None
		for index in range(len(storyFields)):
			item=storyFields[index]
			if isinstance(item,str):
				endOffset = lastEndOffset + textUtils.WideStringOffsetConverter(item).wideStringLength
				if lastEndOffset<=start<endOffset:
					startIndex=index-1
					relStart=start-lastEndOffset
				if lastEndOffset<end<=endOffset:
					endIndex=index+1
					relEnd=end-lastEndOffset
				lastEndOffset=endOffset
		if startIndex is None:
			return []
		if endIndex is None:
			endIndex=len(storyFields)
		commandList=storyFields[startIndex:endIndex]
		if (endIndex-startIndex)==2 and relStart is not None and relEnd is not None:
			commandList[1]=commandList[1][relStart:relEnd]
		else:
			if relStart is not None:
				commandList[1]=commandList[1][relStart:]
			if relEnd is not None:
				commandList[-1]=commandList[-1][:relEnd]
		return commandList

	def _getStoryText(self):
		return u"".join(x for x in self._storyFieldsAndRects[0] if isinstance(x,str))

	def _getStoryLength(self):
		lineEndOffsets=self._storyFieldsAndRects[2]
		if lineEndOffsets:
			return lineEndOffsets[-1]
		return 0

	useUniscribe=False

	def _getTextRange(self, start, end):
		return u"".join(x for x in self._getFieldsInRange(start,end) if isinstance(x,str))

	def getTextWithFields(self, formatConfig: Optional[Dict] = None) -> textInfos.TextInfo.TextWithFieldsT:
		start=self._startOffset
		end=self._endOffset
		if start==end:
			return u""
		return self._getFieldsInRange(start,end)

	def _normalizeFormatField(self,field):
		field['bold']=True if field.get('bold')=="true" else False
		field['hwnd']=int(field.get('hwnd','0'),16)
		field['baseline']=int(field.get('baseline','-1'))
		field['direction']=int(field.get('direction','0'))
		field['italic']=True if field.get('italic')=="true" else False
		field['underline']=True if field.get('underline')=="true" else False
		color=field.get('color')
		if color is not None:
			field['color'] = colors.RGB.fromDisplayModelFormatColor_t(int(color))
		bkColor=field.get('background-color')
		if bkColor is not None:
			field['background-color'] = colors.RGB.fromDisplayModelFormatColor_t(int(bkColor))

	def _getOffsetFromPoint(self, x, y):
		# Accepts physical coordinates.
		x,y=windowUtils.physicalToLogicalPoint(self.obj.windowHandle,x,y)
		for charOffset, (charLeft, charTop, charRight, charBottom) in enumerate(self._storyFieldsAndRects[1]):
			if charLeft<=x<charRight and charTop<=y<charBottom:
				return charOffset
		raise LookupError

	def _getClosestOffsetFromPoint(self,x,y):
		# Accepts physical coordinates.
		x,y=windowUtils.physicalToLogicalPoint(self.obj.windowHandle,x,y)
		#Enumerate the character rectangles
		a=enumerate(self._storyFieldsAndRects[1])
		#Convert calculate center points for all the rectangles
		b = ((charOffset, rect.center) for charOffset, rect in a)
		# Calculate distances from all center points to the given x and y
		# But place the distance before the character offset, to make sorting by distance easier
		c = ((math.sqrt(abs(x - center.x) ** 2 + abs(y - center.y) ** 2), charOffset) for charOffset, center in b)
		#produce a static list of distances and character offsets, sorted by distance 
		d=sorted(c)
		#Return the lowest offset with the shortest distance
		return d[0][1] if len(d)>0 else 0

	def _getBoundingRectFromOffset(self, offset):
		# Returns physical coordinates.
		rects=self._storyFieldsAndRects[1]
		if not rects or offset>=len(rects):
			raise LookupError
		return rects[offset].toPhysical(self.obj.windowHandle).toLTWH()

	def _getNVDAObjectFromOffset(self,offset):
		try:
			p=self._getPointFromOffset(offset)
		except (NotImplementedError,LookupError):
			return self.obj
		obj=api.getDesktopObject().objectFromPoint(p.x,p.y)
		from NVDAObjects.window import Window
		if not obj or not isinstance(obj,Window) or not winUser.isDescendantWindow(self.obj.windowHandle,obj.windowHandle):
			return self.obj
		return obj

	def _getOffsetsFromNVDAObject(self,obj):
		l=obj.location
		if not l:
			log.debugWarning("object has no location")
			raise LookupError
		offset=self._getClosestOffsetFromPoint(*l.center)
		return offset,offset

	def _getOffsetsInPreCalculatedOffsets(self, preCalculated, offset):
		limit = preCalculated[-1]
		if not limit:
			return (offset, offset + 1)
		offset=min(offset,limit-1)
		startOffset=0
		endOffset=0
		for preCalculatedEndOffset in preCalculated:
			startOffset = endOffset
			endOffset = preCalculatedEndOffset
			if preCalculatedEndOffset > offset:
				break
		return (startOffset, endOffset)

	def _getLineOffsets(self, offset):
		lineEndOffsets = self._storyFieldsAndRects[2]
		if not lineEndOffsets:
			return (offset, offset + 1)
		return self._getOffsetsInPreCalculatedOffsets(lineEndOffsets, offset)

	def _getDisplayChunkOffsets(self, offset):
		displayChunkEndOffsets = self._storyFieldsAndRects[3]
		if not displayChunkEndOffsets:
			return (offset, offset + 1)
		return self._getOffsetsInPreCalculatedOffsets(displayChunkEndOffsets, offset)

	def _getUnitOffsets(self, unit, offset):
		if unit is UNIT_DISPLAYCHUNK:
			return self._getDisplayChunkOffsets(offset)
		return super()._getUnitOffsets(unit, offset)

	def _get_clipboardText(self):
		return "\r\n".join(x.strip('\r\n') for x in self.getTextInChunks(textInfos.UNIT_LINE))

	def getTextInChunks(self,unit):
		# Specifically handle the line and display chunk units.
		# We have the line offsets pre-calculated, and we can not guarantee lines end with \n
		if unit is UNIT_DISPLAYCHUNK:
			for x in self._getFieldsInRange(self._startOffset, self._endOffset):
				if not isinstance(x, str):
					continue
				yield x
			return
		if unit is textInfos.UNIT_LINE:
			text=self.text
			relStart=0
			for lineEndOffset in self._storyFieldsAndRects[2]:
				if lineEndOffset<=self._startOffset:
					continue
				relEnd=min(self._endOffset,lineEndOffset)-self._startOffset
				yield text[relStart:relEnd]
				relStart=relEnd
				if lineEndOffset>=self._endOffset:
					return
			return
		for chunk in super(DisplayModelTextInfo,self).getTextInChunks(unit):
			yield chunk

	def _get_boundingRects(self):
		# The base implementation for OffsetsTextInfo is conservative,
		# However here, since bounding rectangles are always known and on screen, we can use them all.
		lineEndOffsets = [
			offset for offset in self._storyFieldsAndRects[2]
			if self._startOffset < offset < self._endOffset
		]
		lineEndOffsets.append(self._endOffset)
		startOffset = endOffset = self._startOffset
		rects = []
		for lineEndOffset in lineEndOffsets:
			startOffset=endOffset
			endOffset=lineEndOffset
			rects.append(RectLTWH.fromCollection(*self._storyFieldsAndRects[1][startOffset:endOffset]).toPhysical(self.obj.windowHandle))
		return rects

	def _getFirstVisibleOffset(self):
		return 0

	def _getLastVisibleOffset(self):
		return self._getStoryLength()

class EditableTextDisplayModelTextInfo(DisplayModelTextInfo):

	minHorizontalWhitespace=1
	minVerticalWhitespace=4
	stripOuterWhitespace=False

	def _findCaretOffsetFromLocation(
			self,
			caretRect: RectLTRB,
			validateBaseline: bool = True,
			validateDirection: bool = True
	):
		# Accepts logical coordinates.
		for charOffset, ((charLeft, charTop, charRight, charBottom),charBaseline,charDirection) in enumerate(self._getStoryOffsetLocations()):
			# Skip any character that does not overlap the caret vertically
			if (caretRect.bottom<=charTop or caretRect.top>=charBottom):
				continue
			# Skip any character that does not overlap the caret horizontally
			if (caretRect.right<=charLeft or caretRect.left>=charRight):
				continue
			# skip over any character that does not have a baseline or who's baseline the caret does not go through
			if validateBaseline and (charBaseline<0 or not (caretRect.top<charBaseline<=caretRect.bottom)):
				continue
			# Does the caret hang off the right side of the character more than the left?
			if validateDirection:
				direction=max(0,charLeft-caretRect.left)-max(0,caretRect.right-charRight)
				# Skip any character who's reading direction disagrees with the caret's direction
				if (charDirection<0 and direction>0) or (not charDirection<0 and direction<0):
					continue
			return charOffset
		raise LookupError

	def _getCaretOffset(self):
		caretRect = getCaretRect(self.obj)
		objLocation = self.obj.location
		objRect = objLocation.toLTRB().toLogical(self.obj.windowHandle)
		caretRect = caretRect.intersection(objRect)
		if not any(caretRect):
			raise RuntimeError("The caret rectangle does not overlap with the window")
		# Find a character offset where the caret overlaps vertically, overlaps horizontally, overlaps the baseline and is totally within or on the correct side for the reading order
		try:
			return self._findCaretOffsetFromLocation(caretRect,validateBaseline=True,validateDirection=True)
		except LookupError:
			pass
		# Find a character offset where the caret overlaps vertically, overlaps horizontally, overlaps the baseline, but does not care about reading order (probably whitespace at beginning or end of a line)
		try:
			return self._findCaretOffsetFromLocation(caretRect,validateBaseline=True,validateDirection=False)
		except LookupError:
			pass
		# Find a character offset where the caret overlaps vertically, overlaps horizontally, but does not care about baseline or reading order (probably vertical whitespace -- blank lines)
		try:
			return self._findCaretOffsetFromLocation(caretRect,validateBaseline=False,validateDirection=False)
		except LookupError:
			raise RuntimeError

	def _setCaretOffset(self,offset):
		rects=self._storyFieldsAndRects[1]
		if offset>=len(rects):
			raise RuntimeError("offset %d out of range")
		rect = rects[offset]
		x = rect.left
		y= rect.center.y
		x,y=windowUtils.logicalToPhysicalPoint(self.obj.windowHandle,x,y)
		oldX,oldY=winUser.getCursorPos()
		winUser.setCursorPos(x,y)
		mouseHandler.doPrimaryClick()
		winUser.setCursorPos(oldX,oldY)

	def _getSelectionOffsets(self):
		try:
			return super(EditableTextDisplayModelTextInfo,self)._getSelectionOffsets()
		except LookupError:
			offset=self._getCaretOffset()
			return offset,offset

	def _setSelectionOffsets(self,start,end):
		if start!=end:
			raise NotImplementedError("Expanded selections not supported")
		self._setCaretOffset(start)
