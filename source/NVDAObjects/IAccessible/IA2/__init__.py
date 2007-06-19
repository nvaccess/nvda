import ctypes
import comtypes
import debug
import api
import speech
import IA2Handler
import text
import controlTypes
import IAccessibleHandler
from keyUtils import sendKey, isKeyWaiting
from NVDAObjects.IAccessible import IAccessible

IA2RolesToNVDARoles={
IA2Handler.ROLE_UNKNOWN:controlTypes.ROLE_UNKNOWN,
IA2Handler.ROLE_CANVAS:controlTypes.ROLE_CANVAS,
IA2Handler.ROLE_CAPTION:controlTypes.ROLE_CAPTION,
IA2Handler.ROLE_CHECK_MENU_ITEM:controlTypes.ROLE_CHECKMENUITEM,
IA2Handler.ROLE_COLOR_CHOOSER:controlTypes.ROLE_DIALOG,
IA2Handler.ROLE_DATE_EDITOR:controlTypes.ROLE_DATEEDITOR,
IA2Handler.ROLE_DESKTOP_ICON:controlTypes.ROLE_ICON,
IA2Handler.ROLE_DESKTOP_PANE:controlTypes.ROLE_PANE,
IA2Handler.ROLE_DIRECTORY_PANE:controlTypes.ROLE_DIRECTORYPANE,
IA2Handler.ROLE_EDITBAR:controlTypes.ROLE_EDITABLETEXT,
IA2Handler.ROLE_EMBEDDED_OBJECT:controlTypes.ROLE_EMBEDDEDOBJECT,
IA2Handler.ROLE_ENDNOTE:controlTypes.ROLE_ENDNOTE,
IA2Handler.ROLE_FILE_CHOOSER:controlTypes.ROLE_DIALOG,
IA2Handler.ROLE_FONT_CHOOSER:controlTypes.ROLE_DIALOG,
IA2Handler.ROLE_FOOTER:controlTypes.ROLE_FOOTER,
IA2Handler.ROLE_FOOTNOTE:controlTypes.ROLE_FOOTNOTE,
IA2Handler.ROLE_FORM:controlTypes.ROLE_FORM,
IA2Handler.ROLE_FRAME:controlTypes.ROLE_FRAME,
IA2Handler.ROLE_GLASS_PANE:controlTypes.ROLE_GLASSPANE,
IA2Handler.ROLE_HEADER:controlTypes.ROLE_HEADER,
IA2Handler.ROLE_HEADING:controlTypes.ROLE_HEADING,
IA2Handler.ROLE_ICON:controlTypes.ROLE_ICON,
IA2Handler.ROLE_IMAGE_MAP:controlTypes.ROLE_IMAGEMAP,
IA2Handler.ROLE_INPUT_METHOD_WINDOW:controlTypes.ROLE_INPUTWINDOW,
IA2Handler.ROLE_INTERNAL_FRAME:controlTypes.ROLE_FRAME,
IA2Handler.ROLE_LABEL:controlTypes.ROLE_LABEL,
IA2Handler.ROLE_LAYERED_PANE:controlTypes.ROLE_LAYEREDPANE,
IA2Handler.ROLE_NOTE:controlTypes.ROLE_NOTE,
IA2Handler.ROLE_OPTION_PANE:controlTypes.ROLE_PROPERTYPAGE,
IA2Handler.ROLE_PAGE:controlTypes.ROLE_PAGE,
IA2Handler.ROLE_PARAGRAPH:controlTypes.ROLE_PARAGRAPH,
IA2Handler.ROLE_RADIO_MENU_ITEM:controlTypes.ROLE_RADIOMENUITEM,
IA2Handler.ROLE_REDUNDANT_OBJECT:controlTypes.ROLE_REDUNDANTOBJECT,
IA2Handler.ROLE_ROOT_PANE:controlTypes.ROLE_ROOTPANE,
IA2Handler.ROLE_RULER:controlTypes.ROLE_RULER,
IA2Handler.ROLE_SCROLL_PANE:controlTypes.ROLE_SCROLLPANE,
IA2Handler.ROLE_SECTION:controlTypes.ROLE_SECTION,
IA2Handler.ROLE_SHAPE:controlTypes.ROLE_SHAPE,
IA2Handler.ROLE_SPLIT_PANE:controlTypes.ROLE_SPLITPANE,
IA2Handler.ROLE_TEAR_OFF_MENU:controlTypes.ROLE_TEAROFFMENU,
IA2Handler.ROLE_TERMINAL:controlTypes.ROLE_TERMINAL,
IA2Handler.ROLE_TEXT_FRAME:controlTypes.ROLE_TEXTFRAME,
IA2Handler.ROLE_TOGGLE_BUTTON:controlTypes.ROLE_TOGGLEBUTTON,
IA2Handler.ROLE_VIEW_PORT:controlTypes.ROLE_VIEWPORT,
}

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
		self._storyLength=self.obj.IAccessibleTextObject.NCharacters
		#If the start offset is higher than the actual text length, then we need to handle it specially
		if self._startOffset>=self._storyLength:
			self._text=""
		elif expandToUnit==text.UNIT_CHARACTER:
			(self._startOffset,self._endOffset,self._text)=self.obj.IAccessibleTextObject.TextAtOffset(self._startOffset,IA2Handler.TEXT_BOUNDARY_CHAR)
		elif expandToUnit==text.UNIT_WORD:
			(self._startOffset,self._endOffset,self._text)=self.obj.IAccessibleTextObject.TextAtOffset(self._startOffset,IA2Handler.TEXT_BOUNDARY_WORD)
		elif expandToUnit==text.UNIT_LINE:
			(self._startOffset,self._endOffset,self._text)=self.obj.IAccessibleTextObject.TextAtOffset(self._startOffset,IA2Handler.TEXT_BOUNDARY_LINE)
		elif expandToUnit==text.UNIT_PARAGRAPH:
			(self._startOffset,self._endOffset,self._text)=self.obj.IAccessibleTextObject.TextAtOffset(self._startOffset,IA2Handler.TEXT_BOUNDARY_PARAGRAPH)
		elif expandToUnit in [text.UNIT_SCREEN,text.UNIT_STORY]:
			self._startOffset=0
			self._endOffset=self._storyLength
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
			self._highOffsetLimit=self._storyLength
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

	def disabled_get_role(self):
		IA2Role=self.IAccessibleObject.role()
		if IA2Role>IA2Handler.ROLE_UNKNOWN and IA2RolesToNVDARoles.has_key(IA2Role):
			return IA2RolesToNVDARoles[IA2Role]
		else:
			return super(IA2,self)._get_role()

	def event_caret(self):
		if self.IAccessibleRole==IAccessibleHandler.ROLE_SYSTEM_CARET:
			return
		focusObject=api.getFocusObject()
		if not isinstance(focusObject,IA2) or focusObject.IAccessibleObject.uniqueID!=self.IAccessibleObject.UniqueID: 
			api.setFocusObject(self)
			api.setNavigatorObject(self)

