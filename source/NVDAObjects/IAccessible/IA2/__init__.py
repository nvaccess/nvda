import ctypes
import comtypes
import debug
import api
import speech
import IA2Handler
import text
import IAccessibleHandler
from keyUtils import sendKey, isKeyWaiting
from NVDAObjects.IAccessible import IAccessible

objWithCaret=None

class IA2TextTextInfo(text.TextInfo):

	def __init__(self,obj,position,expandToUnit=None,limitToUnit=None):
		super(IA2TextTextInfo,self).__init__(obj,position,expandToUnit,limitToUnit)
		if position==text.POSITION_CARET:
			self._startOffset=self._endOffset=self.obj.IAccessibleTextObject.CaretOffset
		elif position==text.POSITION_SELECTION:
			(self._startOffset,self._endOffset)=self.obj.IAccessibleTextObject.Selection(0)
		elif isinstance(position,text.OffsetsPosition):
			self._startOffset=position.start
			self._endOffset=position.end
		else:
			raise NotImplementedError("Position: %s"%position)
		if expandToUnit==text.UNIT_CHARACTER:
			(self._startOffset,self._endOffset,self._text)=self.obj.IAccessibleTextObject.TextAtOffset(self._startOffset,IA2Handler.TEXT_BOUNDARY_CHAR)
		elif expandToUnit==text.UNIT_WORD:
			(self._startOffset,self._endOffset,self._text)=self.obj.IAccessibleTextObject.TextAtOffset(self._startOffset,IA2Handler.TEXT_BOUNDARY_WORD)
		elif expandToUnit==text.UNIT_LINE:
			(self._startOffset,self._endOffset,self._text)=self.obj.IAccessibleTextObject.TextAtOffset(self._startOffset,IA2Handler.TEXT_BOUNDARY_LINE)
		elif expandToUnit==text.UNIT_PARAGRAPH:
			(self._startOffset,self._endOffset,self._text)=self.obj.IAccessibleTextObject.TextAtOffset(self._startOffset,IA2Handler.TEXT_BOUNDARY_PARAGRAPH)
		elif expandToUnit in [text.UNIT_SCREEN,text.UNIT_STORY]:
			self._startOffset=0
			self._endOffset=self.obj.IAccessibleTextObject.NCharacters
		elif expandToUnit is not None:
			raise NotImplementedError("unit: %s"%expandToUnit)
		if limitToUnit==text.UNIT_CHARACTER:
			(self._lowOffsetLimit,self._highOffsetLimit)=self.obj.IAccessibleTextObject.TextAtOffset(self._startOffset,IA2Handler.TEXT_BOUNDARY_CHAR)[0:2]
		elif limitToUnit==text.UNIT_WORD:
			(self._lowOffsetLimit,self._highOffsetLimit)=self.obj.IAccessibleTextObject.TextAtOffset(self._startOffset,IA2Handler.TEXT_BOUNDARY_WORD)[0:2]
		elif limitToUnit==text.UNIT_LINE:
			(self._lowOffsetLimit,self._highOffsetLimit)=self.obj.IAccessibleTextObject.TextAtOffset(self._startOffset,IA2Handler.TEXT_BOUNDARY_LINE)[0:2]
		elif limitToUnit==text.UNIT_PARAGRAPH:
			(self._lowOffsetLimit,self._highOffsetLimit)=self.obj.IAccessibleTextObject.TextAtOffset(self._startOffset,IA2Handler.TEXT_BOUNDARY_PARAGRAPH)[0:2]
		elif limitToUnit in [text.UNIT_SCREEN,text.UNIT_STORY,None]:
			self._lowOffsetLimit=0
			self._highOffsetLimit=self.obj.IAccessibleTextObject.NCharacters
		else:
			raise NotImplementedError("limitToUnit: %s"%limitToUnit)

	def _get_offsetsPosition(self):
		return text.OffsetsPosition(self._startOffset,self._endOffset)

	_get_position=_get_offsetsPosition

	def _get_text(self):
		if hasattr(self,"_text"):
			return self._text
		else:
			return self.obj.IAccessibleTextObject.Text(self._startOffset,self._endOffset)

	def calculateSelectionChangedInfo(self,info):
		selInfo=text.TextSelectionChangedInfo()
		selectingText=None
		mode=None
		oldStart=self.offsetsPosition.start
		oldEnd=self.offsetsPosition.end
		newStart=info.offsetsPosition.start
		newEnd=info.offsetsPosition.end
		if newEnd>oldEnd:
			mode=text.SELECTIONMODE_SELECTED
			fromOffset=oldEnd
			toOffset=newEnd
		elif newStart<oldStart:
			mode=text.SELECTIONMODE_SELECTED
			fromOffset=newStart
			toOffset=oldStart
		elif oldEnd>newEnd:
			mode=text.SELECTIONMODE_UNSELECTED
			fromOffset=newEnd
			toOffset=oldEnd
		elif oldStart<newStart:
			mode=text.SELECTIONMODE_UNSELECTED
			fromOffset=oldStart
			toOffset=newStart
		if mode is not None:
			selectingText=info.obj.makeTextInfo(text.OffsetsPosition(fromOffset,toOffset)).text
		selInfo.text=selectingText
		selInfo.mode=mode
		return selInfo

	def getRelatedUnit(self,relation):
		if self.unit is None:
			raise RuntimeError("no unit")
		if relation==text.UNITRELATION_NEXT:
			newOffset=self._endOffset
		elif relation==text.UNITRELATION_PREVIOUS:
			newOffset=self._startOffset-1
		elif relation==text.UNITRELATION_FIRST:
			newOffset=self._lowOffsetLimit
		elif relation==text.UNITRELATION_LAST:
			newOffset=self._highOffsetLimit-1
		else:
			raise NotImplementedError("relation: %s"%relation)
		if newOffset>=self._lowOffsetLimit and newOffset<self._highOffsetLimit:
			return self.__class__(self.obj,text.OffsetsPosition(newOffset),expandToUnit=self.unit,limitToUnit=self.limitUnit)
		else:
			raise text.E_noRelatedUnit

class IA2(IAccessible):

	def __init__(self,pacc,childID,windowHandle=None,origChildID=None,objectID=None):
		IAccessible.__init__(self,pacc,childID,windowHandle=windowHandle,origChildID=origChildID,objectID=objectID)
		try:
			self.IAccessibleTextObject=pacc.QueryInterface(IA2Handler.IA2Lib.IAccessibleText)
			self.TextInfo=IA2TextTextInfo
			try:
				self.IAccessibleEditableTextObject=pacc.QueryInterface(IA2Handler.IA2Lib.IAccessibleEditableText)
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
					("ExtendedDelete","delete"),
					("Back","backspace"),
				]]
			except:
				pass
		except:
			pass

	def event_caret(self):
		if self.IAccessibleRole==IAccessibleHandler.ROLE_SYSTEM_CARET:
			return
		focusObject=api.getFocusObject()
		if not isinstance(focusObject,IA2) or focusObject.IAccessibleObject.uniqueID!=self.IAccessibleObject.UniqueID: 
			api.setFocusObject(self)
			api.setNavigatorObject(self)

