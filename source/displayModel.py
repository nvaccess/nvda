from ctypes import *
from comtypes import BSTR
import winUser
import NVDAHelper
import textInfos
from textInfos.offsets import OffsetsTextInfo

_getWindowTextInRect=CFUNCTYPE(c_long,c_long,c_long,c_int,c_int,c_int,c_int,POINTER(BSTR),POINTER(BSTR))(('displayModel_getWindowTextInRect',NVDAHelper.localLib),((1,),(1,),(1,),(1,),(1,),(1,),(2,),(2,)))
def getWindowTextInRect(bindingHandle, windowHandle, left, top, right, bottom):
	text, cpBuf = _getWindowTextInRect(bindingHandle, windowHandle, left, top, right, bottom)
	characterPoints = []
	cpBufIt = iter(cpBuf)
	for cp in cpBufIt:
		characterPoints.append((ord(cp), ord(next(cpBufIt))))
	return text, characterPoints

class DisplayModelTextInfo(OffsetsTextInfo):

	_cache__textAndPoints = True
	def _get__textAndPoints(self):
		left, top, width, height = self.obj.location
		return getWindowTextInRect(self.obj.appModule.helperLocalBindingHandle, self.obj.windowHandle, left, top, left + width, top + height)

	def _getStoryText(self):
		return self._textAndPoints[0]

	def _getStoryLength(self):
		return len(self._getStoryText())

	def _getTextRange(self, start, end):
		return self._getStoryText()[start:end]

	def _getPointFromOffset(self, offset):
		x, y = self._textAndPoints[1][offset]
		return textInfos.Point(x, y)

	def _getOffsetFromPoint(self, x, y):
		offset = None
		for charOffset, (charX, charY) in enumerate(self._textAndPoints[1]):
			if charY > y:
				break
			if charX < x:
				offset = charOffset
		if offset is None:
			raise LookupError
		return offset

	def _getCaretOffset(self):
		clientLeft, clientTop, clientWidth, clientHeight = self.obj.location
		caretRect = winUser.getGUIThreadInfo(self.obj.windowThreadID).rcCaret
		return self._getOffsetFromPoint(clientLeft + caretRect.right , clientTop + caretRect.bottom)
