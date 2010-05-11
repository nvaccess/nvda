from ctypes import *
from ctypes.wintypes import RECT
from comtypes import BSTR
import api
import winUser
import NVDAHelper
import textInfos
from textInfos.offsets import OffsetsTextInfo

_getWindowTextInRect=None

def initialize():
	global _getWindowTextInRect
	_getWindowTextInRect=CFUNCTYPE(c_long,c_long,c_long,c_int,c_int,c_int,c_int,c_int,c_int,POINTER(BSTR),POINTER(BSTR))(('displayModel_getWindowTextInRect',NVDAHelper.localLib),((1,),(1,),(1,),(1,),(1,),(1,),(1,),(1,),(2,),(2,)))

def getWindowTextInRect(bindingHandle, windowHandle, left, top, right, bottom,minHorizontalWhitespace,minVerticalWhitespace):
	text, cpBuf = _getWindowTextInRect(bindingHandle, windowHandle, left, top, right, bottom,minHorizontalWhitespace,minVerticalWhitespace)
	if not text or not cpBuf:
		return "",[]

	characterRects = []
	cpBufIt = iter(cpBuf)
	for cp in cpBufIt:
		characterRects.append((ord(cp), ord(next(cpBufIt)), ord(next(cpBufIt)), ord(next(cpBufIt))))
	return text, characterRects

class DisplayModelTextInfo(OffsetsTextInfo):

	minHorizontalWhitespace=8
	minVerticalWhitespace=32

	_cache__textAndRects = True
	def _get__textAndRects(self):
		left, top, width, height = self.obj.location
		return getWindowTextInRect(self.obj.appModule.helperLocalBindingHandle, self.obj.windowHandle, left, top, left + width, top + height,self.minHorizontalWhitespace,self.minVerticalWhitespace)

	def _get_NVDAObjectAtStart(self):
		p=self.pointAtStart
		obj=api.getDesktopObject().objectFromPoint(p.x,p.y)
		from NVDAObjects.window import Window
		if not obj or not isinstance(obj,Window) or not winUser.isDescendantWindow(self.obj.windowHandle,obj.windowHandle):
			obj=self.obj
		return obj


	def _getStoryText(self):
		return self._textAndRects[0]

	def _getStoryLength(self):
		return len(self._getStoryText())

	def _getTextRange(self, start, end):
		return self._getStoryText()[start:end]

	def _getPointFromOffset(self, offset):
		x, y = self._textAndRects[1][offset][:2]
		return textInfos.Point(x, y)

	def _getOffsetFromPoint(self, x, y):
		for charOffset, (charLeft, charTop, charRight, charBottom) in enumerate(self._textAndRects[1]):
			if charLeft<=x<charRight and charTop<=y<charBottom:
				return charOffset
		raise LookupError

class EditableTextDisplayModelTextInfo(DisplayModelTextInfo):

	minHorizontalWhitespace=1
	minVerticalWhitespace=4

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
		import speech
		for charOffset, (charLeft, charTop, charRight, charBottom) in enumerate(self._textAndRects[1]):
			#speech.speakMessage("caret %d,%d char %d,%d"%(caretRect.top,caretRect.bottom,charTop,charBottom))
			if caretRect.left>=charLeft and caretRect.right<=charRight and ((caretRect.top<=charTop and caretRect.bottom>=charBottom) or (caretRect.top>=charTop and caretRect.bottom<=charBottom)):
				return charOffset
		raise RuntimeError
