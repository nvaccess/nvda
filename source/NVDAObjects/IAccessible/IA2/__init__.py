import ctypes
import comtypes
import winsound
import api
import speech
import textHandler
import controlTypes
import IAccessibleHandler
from keyUtils import sendKey, isKeyWaiting
from .. import IAccessible
from ... import NVDAObjectTextInfo
from ...window import Window

IA2RolesToNVDARoles={
IAccessibleHandler.IA2_ROLE_UNKNOWN:controlTypes.ROLE_UNKNOWN,
IAccessibleHandler.IA2_ROLE_CANVAS:controlTypes.ROLE_CANVAS,
IAccessibleHandler.IA2_ROLE_CAPTION:controlTypes.ROLE_CAPTION,
IAccessibleHandler.IA2_ROLE_CHECK_MENU_ITEM:controlTypes.ROLE_CHECKMENUITEM,
IAccessibleHandler.IA2_ROLE_COLOR_CHOOSER:controlTypes.ROLE_COLORCHOOSER,
IAccessibleHandler.IA2_ROLE_DATE_EDITOR:controlTypes.ROLE_DATEEDITOR,
IAccessibleHandler.IA2_ROLE_DESKTOP_ICON:controlTypes.ROLE_DESKTOPICON,
IAccessibleHandler.IA2_ROLE_DESKTOP_PANE:controlTypes.ROLE_DESKTOPPANE,
IAccessibleHandler.IA2_ROLE_DIRECTORY_PANE:controlTypes.ROLE_DIRECTORYPANE,
IAccessibleHandler.IA2_ROLE_EDITBAR:controlTypes.ROLE_EDITBAR,
IAccessibleHandler.IA2_ROLE_EMBEDDED_OBJECT:controlTypes.ROLE_EMBEDDEDOBJECT,
IAccessibleHandler.IA2_ROLE_ENDNOTE:controlTypes.ROLE_ENDNOTE,
IAccessibleHandler.IA2_ROLE_FILE_CHOOSER:controlTypes.ROLE_FILECHOOSER,
IAccessibleHandler.IA2_ROLE_FONT_CHOOSER:controlTypes.ROLE_FONTCHOOSER,
IAccessibleHandler.IA2_ROLE_FOOTER:controlTypes.ROLE_FOOTER,
IAccessibleHandler.IA2_ROLE_FOOTNOTE:controlTypes.ROLE_FOOTNOTE,
IAccessibleHandler.IA2_ROLE_FORM:controlTypes.ROLE_FORM,
IAccessibleHandler.IA2_ROLE_FRAME:controlTypes.ROLE_FRAME,
IAccessibleHandler.IA2_ROLE_GLASS_PANE:controlTypes.ROLE_GLASSPANE,
IAccessibleHandler.IA2_ROLE_HEADER:controlTypes.ROLE_HEADER,
IAccessibleHandler.IA2_ROLE_HEADING:controlTypes.ROLE_HEADING,
IAccessibleHandler.IA2_ROLE_ICON:controlTypes.ROLE_ICON,
IAccessibleHandler.IA2_ROLE_IMAGE_MAP:controlTypes.ROLE_IMAGEMAP,
IAccessibleHandler.IA2_ROLE_INPUT_METHOD_WINDOW:controlTypes.ROLE_INPUTWINDOW,
IAccessibleHandler.IA2_ROLE_INTERNAL_FRAME:controlTypes.ROLE_INTERNALFRAME,
IAccessibleHandler.IA2_ROLE_LABEL:controlTypes.ROLE_LABEL,
IAccessibleHandler.IA2_ROLE_LAYERED_PANE:controlTypes.ROLE_LAYEREDPANE,
IAccessibleHandler.IA2_ROLE_NOTE:controlTypes.ROLE_NOTE,
IAccessibleHandler.IA2_ROLE_OPTION_PANE:controlTypes.ROLE_OPTIONPANE,
IAccessibleHandler.IA2_ROLE_PAGE:controlTypes.ROLE_PAGE,
IAccessibleHandler.IA2_ROLE_PARAGRAPH:controlTypes.ROLE_PARAGRAPH,
IAccessibleHandler.IA2_ROLE_RADIO_MENU_ITEM:controlTypes.ROLE_RADIOMENUITEM,
IAccessibleHandler.IA2_ROLE_REDUNDANT_OBJECT:controlTypes.ROLE_REDUNDANTOBJECT,
IAccessibleHandler.IA2_ROLE_ROOT_PANE:controlTypes.ROLE_ROOTPANE,
IAccessibleHandler.IA2_ROLE_RULER:controlTypes.ROLE_RULER,
IAccessibleHandler.IA2_ROLE_SCROLL_PANE:controlTypes.ROLE_SCROLLPANE,
IAccessibleHandler.IA2_ROLE_SECTION:controlTypes.ROLE_SECTION,
IAccessibleHandler.IA2_ROLE_SHAPE:controlTypes.ROLE_SHAPE,
IAccessibleHandler.IA2_ROLE_SPLIT_PANE:controlTypes.ROLE_SPLITPANE,
IAccessibleHandler.IA2_ROLE_TEAR_OFF_MENU:controlTypes.ROLE_TEAROFFMENU,
IAccessibleHandler.IA2_ROLE_TERMINAL:controlTypes.ROLE_TERMINAL,
IAccessibleHandler.IA2_ROLE_TEXT_FRAME:controlTypes.ROLE_TEXTFRAME,
IAccessibleHandler.IA2_ROLE_TOGGLE_BUTTON:controlTypes.ROLE_TOGGLEBUTTON,
IAccessibleHandler.IA2_ROLE_VIEW_PORT:controlTypes.ROLE_VIEWPORT,
}

class IA2TextTextInfo(NVDAObjectTextInfo):

	def _getCaretOffset(self):
		try:
			return self.obj.IAccessibleTextObject.CaretOffset
		except:
			return 0

	def _setCaretOffset(self,offset):
		self.obj.IAccessibleTextObject.SetCaretOffset(offset)

	def _getSelectionOffsets(self):
		if self.obj.IAccessibleTextObject.nSelections>0:
			(start,end)=self.obj.IAccessibleTextObject.Selection[0]
		else:
			start=self._getCaretOffset()
			end=start
		return [min(start,end),max(start,end)]

	def _setSelectionOffsets(self,start,end):
		for selIndex in range(self.obj.IAccessibleTextObject.NSelections):
			self.obj.IAccessibleTextObject.RemoveSelection(selIndex)
		self.obj.IAccessibleTextObject.AddSelection(start,end)

	def _getStoryLength(self):
		if not hasattr(self,'_storyLength'):
			self._storyLength=self.obj.IAccessibleTextObject.NCharacters
		return self._storyLength

	def _getLineCount(self):
			return -1

	def _getTextRange(self,start,end):
		try:
			return self.obj.IAccessibleTextObject.Text(start,end)
		except:
			return ""

	def _getCharacterOffsets(self,offset):
		return self.obj.IAccessibleTextObject.TextAtOffset(offset,IAccessibleHandler.IA2_TEXT_BOUNDARY_CHAR)[0:2]

	def _getWordOffsets(self,offset):
		try:
			return self.obj.IAccessibleTextObject.TextAtOffset(offset,IAccessibleHandler.IA2_TEXT_BOUNDARY_WORD)[0:2]
		except:
			return super(IA2TextTextInfo,self)._getWordOffsets(offset)


	def _getLineOffsets(self,offset):
		try:
			return self.obj.IAccessibleTextObject.TextAtOffset(offset,IAccessibleHandler.IA2_TEXT_BOUNDARY_LINE)[0:2]
		except:
			return super(IA2TextTextInfo,self)._getLineOffsets(offset)

	def _getSentenceOffsets(self,offset):
		try:
			return self.obj.IAccessibleTextObject.TextAtOffset(offset,IAccessibleHandler.IA2_TEXT_BOUNDARY_SENTENCE)[0:2]
		except:
			return super(IA2TextTextInfo,self)._getSentenceOffsets(offset)

	def _getParagraphOffsets(self,offset):
		return self.obj.IAccessibleTextObject.TextAtOffset(offset,IAccessibleHandler.IA2_TEXT_BOUNDARY_PARAGRAPH)[0:2]

	def _lineNumFromOffset(self,offset):
		return -1

class IA2(IAccessible):

	def __init__(self,windowHandle=None,IAccessibleObject=None,IAccessibleChildID=None,IAccessibleOrigChildID=None,IAccessibleObjectID=None):
		replacedTextInfo=False
		windowHandle=IAccessibleHandler.windowFromAccessibleObject(IAccessibleObject)
		try:
			self.IAccessibleActionObject=IAccessibleObject.QueryInterface(IAccessibleHandler.IAccessibleAction)
		except:
			pass
		try:
			self.IAccessibleTextObject=IAccessibleObject.QueryInterface(IAccessibleHandler.IAccessibleText)
			self.TextInfo=IA2TextTextInfo
			replacedTextInfo=True
			try:
				self.IAccessibleEditableTextObject=IAccessibleObject.QueryInterface(IAccessibleHandler.IAccessibleEditableText)
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
		IAccessible.__init__(self,windowHandle=windowHandle,IAccessibleObject=IAccessibleObject,IAccessibleChildID=IAccessibleChildID,IAccessibleOrigChildID=IAccessibleOrigChildID,IAccessibleObjectID=IAccessibleObjectID)
		self._lastMouseTextOffsets=None
		if replacedTextInfo:
			self.reviewPosition=self.makeTextInfo(textHandler.POSITION_CARET)

	def _isEqual(self,other):
		if not isinstance(other,IA2):
			return IAccessible._isEqual(self,other)
		if not Window._isEqual(self,other):
			return False
		if self.IAccessibleChildID!=other.IAccessibleChildID:
			return False
		if self.IAccessibleObject==other.IAccessibleObject:
			return True
		if self.IAccessibleObject.UniqueID!=other.IAccessibleObject.UniqueID:
			return False
		if self.IAccessibleRole!=other.IAccessibleRole:
			return False
		return True

	def _get_role(self):
		IA2Role=self.IAccessibleObject.role()
		if IA2Role>IAccessibleHandler.IA2_ROLE_UNKNOWN and IA2RolesToNVDARoles.has_key(IA2Role):
			return IA2RolesToNVDARoles[IA2Role]
		else:
			return super(IA2,self)._get_role()

	def _get_actionStrings(self):
		if not hasattr(self,'IAccessibleActionObject'):
			return super(IA2,self)._get_actionStrings()
		actions=[]
		for index in range(self.IAccessibleActionObject.nActions()):
			try:
				name=self.IAccessibleActionObject.localizedName(index)
			except:
				name=None
			if not name:
				try:
					name=self.IAccessibleActionObject.name(index)
				except:
					name=None
			if name:
				actions.append(name)
		return actions

	def doAction(self,index):
		if not hasattr(self,'IAccessibleActionObject'):
			return super(IA2,self).doAction(index)
		self.IAccessibleActionObject.doAction(index)

	def event_caret(self):
		if self.IAccessibleRole==IAccessibleHandler.ROLE_SYSTEM_CARET:
			return
		focusObject=api.getFocusObject()
		if self!=focusObject and not self.virtualBuffer:
			IAccessibleHandler.focus_manageEvent(self,needsFocusState=False)

	def event_mouseMove(self,x,y):
		#As Gecko 1.9 still has MSAA text node objects, these get hit by accHitTest, so
		#We must find the real object and cache it
		obj=getattr(self,'_realMouseObject',None)
		if not obj:
			obj=self
			while obj and not hasattr(obj,'IAccessibleTextObject'):
				obj=obj.parent
			if obj:
				self._realMouseObject=obj
			else:
				obj=self
		mouseEntered=obj._mouseEntered
		super(IA2,obj).event_mouseMove(x,y)
		if not hasattr(obj,'IAccessibleTextObject'):
			return 
		(left,top,width,height)=obj.location
		offset=obj.IAccessibleTextObject.OffsetAtPoint(x,y,IAccessibleHandler.IA2_COORDTYPE_SCREEN_RELATIVE)
		if obj._lastMouseTextOffsets is None or offset<obj._lastMouseTextOffsets[0] or offset>=obj._lastMouseTextOffsets[1]:   
			if mouseEntered:
				speech.cancelSpeech()
			info=obj.makeTextInfo(textHandler.Bookmark(obj.TextInfo,(offset,offset)))
			info.expand(textHandler.UNIT_WORD)
			speech.speakText(info.text)
			obj._lastMouseTextOffsets=(info._startOffset,info._endOffset)
