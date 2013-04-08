from ctypes import *
from ctypes.wintypes import RECT
from comtypes import BSTR
import math
import colors
import XMLFormatting
import api
import winUser
import NVDAHelper
import textInfos
from textInfos.offsets import OffsetsTextInfo
import watchdog
from logHandler import log

_getWindowTextInRect=None
_requestTextChangeNotificationsForWindow=None
#: Objects that have registered for text change notifications.
_textChangeNotificationObjs=[]

def initialize():
	global _getWindowTextInRect,_requestTextChangeNotificationsForWindow
	_getWindowTextInRect=CFUNCTYPE(c_long,c_long,c_long,c_int,c_int,c_int,c_int,c_int,c_int,POINTER(BSTR),POINTER(BSTR))(('displayModel_getWindowTextInRect',NVDAHelper.localLib),((1,),(1,),(1,),(1,),(1,),(1,),(1,),(1,),(2,),(2,)))
	_requestTextChangeNotificationsForWindow=NVDAHelper.localLib.displayModel_requestTextChangeNotificationsForWindow

def getWindowTextInRect(bindingHandle, windowHandle, left, top, right, bottom,minHorizontalWhitespace,minVerticalWhitespace):
	text, cpBuf = watchdog.cancellableExecute(_getWindowTextInRect, bindingHandle, windowHandle, left, top, right, bottom,minHorizontalWhitespace,minVerticalWhitespace)
	if not text or not cpBuf:
		return u"",[]

	characterLocations = []
	cpBufIt = iter(cpBuf)
	for cp in cpBufIt:
		characterLocations.append((ord(cp), ord(next(cpBufIt)), ord(next(cpBufIt)), ord(next(cpBufIt))))
	return text, characterLocations

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

	_cache__storyFieldsAndRects = True
	def _get__storyFieldsAndRects(self):
		try:
			left, top, width, height = self.obj.location
		except TypeError:
			# No location; nothing we can do.
			return [],[]
		bindingHandle=self.obj.appModule.helperLocalBindingHandle
		if not bindingHandle:
			log.debugWarning("AppModule does not have a binding handle")
			return [],[]
		text,rects=getWindowTextInRect(bindingHandle, self.obj.windowHandle, left, top, left + width, top + height,self.minHorizontalWhitespace,self.minVerticalWhitespace)
		if not text:
			return [],[]
		text="<control>%s</control>"%text
		commandList=XMLFormatting.XMLTextParser().parse(text)
		for item in commandList:
			if isinstance(item,textInfos.FieldCommand) and isinstance(item.field,textInfos.FormatField):
				self._normalizeFormatField(item.field)
		return commandList,rects

	def _getStoryOffsetLocations(self):
		baseline=None
		rtl=None
		lastEndOffset=0
		commandList,rects=self._storyFieldsAndRects
		for item in commandList:
			if isinstance(item,textInfos.FieldCommand) and isinstance(item.field,textInfos.FormatField):
				baseline=item.field['baseline']
				rtl=item.field['rtl']
			elif isinstance(item,basestring):
				endOffset=lastEndOffset+len(item)
				for rect in rects[lastEndOffset:endOffset]:
					yield rect,baseline,rtl
				lastEndOffset=endOffset

	def _getFieldsInRange(self,start,end):
		storyFields=self._storyFieldsAndRects[0]
		if not storyFields:
			return []
		commandList=self._storyFieldsAndRects[0]
		#Strip  unwanted commands and text from the start and the end to honour the requested offsets
		stringOffset=0
		for index in xrange(len(storyFields)-1):
			command=commandList[index]
			if isinstance(command,basestring):
				stringLen=len(command)
				if (stringOffset+stringLen)<=start:
					stringOffset+=stringLen
				else:
					del commandList[1:index-1]
					commandList[2]=command[start-stringOffset:]
					break
		end=end-start
		stringOffset=0
		for index in xrange(1,len(commandList)-1):
			command=commandList[index]
			if isinstance(command,basestring):
				stringLen=len(command)
				if (stringOffset+stringLen)<end:
					stringOffset+=stringLen
				else:
					commandList[index]=command[0:end-stringOffset]
					del commandList[index+1:-1]
					break
		return commandList

	def _getStoryText(self):
		return u"".join(x for x in self._storyFieldsAndRects[0] if isinstance(x,basestring))

	def _getStoryLength(self):
		return len(self._getStoryText())

	def _getTextRange(self, start, end):
		return u"".join(x for x in self._getFieldsInRange(start,end) if isinstance(x,basestring))

	def getTextWithFields(self,formatConfig=None):
		start=self._startOffset
		end=self._endOffset
		if start==end:
			return u""
		return self._getFieldsInRange(start,end)

	def _normalizeFormatField(self,field):
		field['bold']=True if field.get('bold')=="true" else False
		field['baseline']=int(field.get('baseline','-1'))
		field['rtl']=True if field.get('rtl')=="1" else False
		field['italic']=True if field.get('italic')=="true" else False
		field['underline']=True if field.get('underline')=="true" else False
		color=field.get('color')
		if color is not None:
			field['color']=colors.RGB.fromCOLORREF(int(color))
		bkColor=field.get('background-color')
		if bkColor is not None:
			field['background-color']=colors.RGB.fromCOLORREF(int(bkColor))

	def _getPointFromOffset(self, offset):
		rects=self._storyFieldsAndRects[1]
		if not rects or offset>=len(rects):
			raise LookupError
		x,y=rects[offset][:2]
		return textInfos.Point(x, y)

	def _getOffsetFromPoint(self, x, y):
		for charOffset, (charLeft, charTop, charRight, charBottom) in enumerate(self._storyFieldsAndRects[1]):
			if charLeft<=x<charRight and charTop<=y<charBottom:
				return charOffset
		raise LookupError

	def _getClosestOffsetFromPoint(self,x,y):
		#Enumerate the character rectangles
		a=enumerate(self._storyFieldsAndRects[1])
		#Convert calculate center points for all the rectangles
		b=((charOffset,(charLeft+(charRight-charLeft)/2,charTop+(charBottom-charTop)/2)) for charOffset,(charLeft,charTop,charRight,charBottom) in a)
		#Calculate distances from all center points to the given x and y
		#But place the distance before the character offset, to make sorting by distance easier
		c=((math.sqrt(abs(x-cx)**2+abs(y-cy)**2),charOffset) for charOffset,(cx,cy) in b)
		#produce a static list of distances and character offsets, sorted by distance 
		d=sorted(c)
		#Return the lowest offset with the shortest distance
		return d[0][1] if len(d)>0 else 0

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
			raise RuntimeError
		x=l[0]+(l[2]/2)
		y=l[1]+(l[3]/2)
		offset=self._getClosestOffsetFromPoint(x,y)
		return offset,offset

	def _get_clipboardText(self):
		return super(DisplayModelTextInfo,self).clipboardText.replace('\0',' ')

class EditableTextDisplayModelTextInfo(DisplayModelTextInfo):

	minHorizontalWhitespace=1
	minVerticalWhitespace=4

	def _findCaretOffsetFromLocation(self,caretRect,validateBaseline=True,validateHanging=True):
		for charOffset, ((charLeft, charTop, charRight, charBottom),charBaseline,charRtl) in enumerate(self._getStoryOffsetLocations()):
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
			if validateHanging:
				hanging=max(0,charLeft-caretRect.left)-max(0,caretRect.right-charRight)
				# Skip any character who's reading direction disagrees with the caret's hanging direction 
				if (charRtl and hanging>0) or (not charRtl and hanging<0):
					continue
			return charOffset
		raise LookupError

	def _getCaretOffset(self):
		caretRect = winUser.getGUIThreadInfo(self.obj.windowThreadID).rcCaret
		objLocation=self.obj.location
		objRect=RECT(objLocation[0],objLocation[1],objLocation[0]+objLocation[2],objLocation[1]+objLocation[3])
		tempPoint = winUser.POINT()
		tempPoint.x=caretRect.left
		tempPoint.y=caretRect.top
		winUser.user32.ClientToScreen(self.obj.windowHandle, byref(tempPoint))
		caretRect.left=max(objRect.left,tempPoint.x)
		caretRect.top=max(objRect.top,tempPoint.y)
		tempPoint.x=caretRect.right
		tempPoint.y=caretRect.bottom
		winUser.user32.ClientToScreen(self.obj.windowHandle, byref(tempPoint))
		caretRect.right=min(objRect.right,tempPoint.x)
		caretRect.bottom=min(objRect.bottom,tempPoint.y)
		# Find a character offset where the caret overlaps vertically, overlaps horizontally, overlaps the baseline and is totally within or on the correct side for the reading order
		try:
			return self._findCaretOffsetFromLocation(caretRect,validateBaseline=True,validateHanging=True)
		except LookupError:
			pass
		# Find a character offset where the caret overlaps vertically, overlaps horizontally, overlaps the baseline, but does not care about reading order (probably whitespace at beginning or end of a line)
		try:
			return self._findCaretOffsetFromLocation(caretRect,validateBaseline=True,validateHanging=False)
		except LookupError:
			pass
		# Find a character offset where the caret overlaps vertically, overlaps horizontally, but does not care about baseline or reading order (probably vertical whitespace -- blank lines)
		return self._findCaretOffsetFromLocation(caretRect,validateBaseline=False,validateHanging=False)

	def _setCaretOffset(self,offset):
		rects=self._storyFieldsAndRects[1]
		if offset>=len(rects):
			raise RuntimeError("offset %d out of range")
		left,top,right,bottom=rects[offset]
		x=left #+(right-left)/2
		y=top+(bottom-top)/2
		oldX,oldY=winUser.getCursorPos()
		winUser.setCursorPos(x,y)
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
		winUser.setCursorPos(oldX,oldY)

	def _getSelectionOffsets(self):
		offset=self._getCaretOffset()
		return offset,offset

	def _setSelectionOffsets(self,start,end):
		if start!=end:
			raise TypeError("Expanded selections not supported")
		self._setCaretOffset(start)
