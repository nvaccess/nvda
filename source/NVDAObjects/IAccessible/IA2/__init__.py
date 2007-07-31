import ctypes
import comtypes
import debug
import api
import speech
import IA2Handler
import textHandler
import controlTypes
import IAccessibleHandler
from keyUtils import sendKey, isKeyWaiting
from .. import IAccessible
from ... import NVDAObjectTextInfo

IA2RolesToNVDARoles={
IA2Handler.ROLE_UNKNOWN:controlTypes.ROLE_UNKNOWN,
IA2Handler.ROLE_CANVAS:controlTypes.ROLE_CANVAS,
IA2Handler.ROLE_CAPTION:controlTypes.ROLE_CAPTION,
IA2Handler.ROLE_CHECK_MENU_ITEM:controlTypes.ROLE_CHECKMENUITEM,
IA2Handler.ROLE_COLOR_CHOOSER:controlTypes.ROLE_COLORCHOOSER,
IA2Handler.ROLE_DATE_EDITOR:controlTypes.ROLE_DATEEDITOR,
IA2Handler.ROLE_DESKTOP_ICON:controlTypes.ROLE_DESKTOPICON,
IA2Handler.ROLE_DESKTOP_PANE:controlTypes.ROLE_DESKTOPPANE,
IA2Handler.ROLE_DIRECTORY_PANE:controlTypes.ROLE_DIRECTORYPANE,
IA2Handler.ROLE_EDITBAR:controlTypes.ROLE_EDITBAR,
IA2Handler.ROLE_EMBEDDED_OBJECT:controlTypes.ROLE_EMBEDDEDOBJECT,
IA2Handler.ROLE_ENDNOTE:controlTypes.ROLE_ENDNOTE,
IA2Handler.ROLE_FILE_CHOOSER:controlTypes.ROLE_FILECHOOSER,
IA2Handler.ROLE_FONT_CHOOSER:controlTypes.ROLE_FONTCHOOSER,
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
IA2Handler.ROLE_INTERNAL_FRAME:controlTypes.ROLE_INTERNALFRAME,
IA2Handler.ROLE_LABEL:controlTypes.ROLE_LABEL,
IA2Handler.ROLE_LAYERED_PANE:controlTypes.ROLE_LAYEREDPANE,
IA2Handler.ROLE_NOTE:controlTypes.ROLE_NOTE,
IA2Handler.ROLE_OPTION_PANE:controlTypes.ROLE_OPTIONPANE,
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

class IA2TextTextInfo(NVDAObjectTextInfo):

	def _getCaretOffset(self):
		return self.obj.IAccessibleTextObject.CaretOffset

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
		return -1 #winUser.sendMessage(self.obj.windowHandle,SCI_GETLINECOUNT,0,0)

	def _getTextRange(self,start,end):
		return self.obj.IAccessibleTextObject.Text(start,end)

	def _getCharacterOffsets(self,offset):
		return self.obj.IAccessibleTextObject.TextAtOffset(offset,IA2Handler.TEXT_BOUNDARY_CHAR)[0:2]

	def _getWordOffsets(self,offset):
		return self.obj.IAccessibleTextObject.TextAtOffset(offset,IA2Handler.TEXT_BOUNDARY_WORD)[0:2]

	def _getLineOffsets(self,offset):
		return self.obj.IAccessibleTextObject.TextAtOffset(offset,IA2Handler.TEXT_BOUNDARY_LINE)[0:2]

	def _getSentenceOffsets(self,offset):
		return self.obj.IAccessibleTextObject.TextAtOffset(offset,IA2Handler.TEXT_BOUNDARY_SENTENCE)[0:2]

	def _getParagraphOffsets(self,offset):
		return self.obj.IAccessibleTextObject.TextAtOffset(offset,IA2Handler.TEXT_BOUNDARY_PARAGRAPH)[0:2]

	def _lineNumFromOffset(self,offset):
		return -1 #winUser.sendMessage(self.obj.windowHandle,SCI_LINEFROMPOSITION,offset,0)

class IA2(IAccessible):

	def __init__(self,windowHandle=None,IAccessibleObject=None,IAccessibleChildID=None,IAccessibleOrigChildID=None,IAccessibleObjectID=None):
		IAccessible.__init__(self,windowHandle=windowHandle,IAccessibleObject=IAccessibleObject,IAccessibleChildID=IAccessibleChildID,IAccessibleOrigChildID=IAccessibleOrigChildID,IAccessibleObjectID=IAccessibleObjectID)
		try:
			self.IAccessibleTextObject=IAccessibleObject.QueryInterface(IA2Handler.IA2Lib.IAccessibleText)
			self.TextInfo=IA2TextTextInfo
			try:
				self.IAccessibleEditableTextObject=IAccessibleObject.QueryInterface(IA2Handler.IA2Lib.IAccessibleEditableText)
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

