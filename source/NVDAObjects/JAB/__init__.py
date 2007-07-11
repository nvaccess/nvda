import ctypes
import debug
import appModuleHandler
import speech
import winUser
import JABHandler
import controlTypes
from ..window import Window
import text
import controlTypes
from .. import NVDAObjectTextInfo

JABRolesToNVDARoles={
	"alert":controlTypes.ROLE_DIALOG,
	"column header":controlTypes.ROLE_TABLECOLUMNHEADER,
	"canvas":controlTypes.ROLE_CANVAS,
	"combo box":controlTypes.ROLE_COMBOBOX,
	"desktop icon":controlTypes.ROLE_DESKTOPICON,
	"internal frame":controlTypes.ROLE_INTERNALFRAME,
	"desktop pane":controlTypes.ROLE_DESKTOPPANE,
	"option pane":controlTypes.ROLE_OPTIONPANE,
	"window":controlTypes.ROLE_WINDOW,
	"frame":controlTypes.ROLE_FRAME,
	"dialog":controlTypes.ROLE_DIALOG,
	"color chooser":controlTypes.ROLE_COLORCHOOSER,
	"directory pane":controlTypes.ROLE_DIRECTORYPANE,
	"file chooser":controlTypes.ROLE_FILECHOOSER,
	"filler":controlTypes.ROLE_FILLER,
	"hyperlink":controlTypes.ROLE_LINK,
	"icon":controlTypes.ROLE_ICON,
	"label":controlTypes.ROLE_LABEL,
	"root pane":controlTypes.ROLE_ROOTPANE,
	"glass pane":controlTypes.ROLE_GLASSPANE,
	"layered pane":controlTypes.ROLE_LAYEREDPANE,
	"list":controlTypes.ROLE_LIST,
	"list item":controlTypes.ROLE_LISTITEM,
	"menu bar":controlTypes.ROLE_MENUBAR,
	"popup menu":controlTypes.ROLE_POPUPMENU,
	"menu":controlTypes.ROLE_MENU,
	"menu item":controlTypes.ROLE_MENUITEM,
	"separator":controlTypes.ROLE_SEPARATOR,
	"page tab list":controlTypes.ROLE_TABCONTROL,
	"page tab":controlTypes.ROLE_TAB,
	"panel":controlTypes.ROLE_PANEL,
	"progress bar":controlTypes.ROLE_PROGRESSBAR,
	"password text":controlTypes.ROLE_PASSWORDEDIT,
	"push button":controlTypes.ROLE_BUTTON,
	"toggle button":controlTypes.ROLE_TOGGLEBUTTON,
	"check box":controlTypes.ROLE_CHECKBOX,
	"radio button":controlTypes.ROLE_RADIOBUTTON,
	"row header":controlTypes.ROLE_TABLEROWHEADER,
	"scroll pane":controlTypes.ROLE_SCROLLPANE,
	"scroll bar":controlTypes.ROLE_SCROLLBAR,
	"view port":controlTypes.ROLE_VIEWPORT,
	"slider":controlTypes.ROLE_SLIDER,
	"split pane":controlTypes.ROLE_SPLITPANE,
	"table":controlTypes.ROLE_TABLE,
	"text":controlTypes.ROLE_EDITABLETEXT,
	"tree":controlTypes.ROLE_TREEVIEW,
	"tool bar":controlTypes.ROLE_TOOLBAR,
	"tool tip":controlTypes.ROLE_TOOLTIP,
	"status bar":controlTypes.ROLE_STATUSBAR,
	"statusbar":controlTypes.ROLE_STATUSBAR,
	"date editor":controlTypes.ROLE_DATEEDITOR,
	"spin box":controlTypes.ROLE_SPINBUTTON,
	"font chooser":controlTypes.ROLE_FONTCHOOSER,
	"group box":controlTypes.ROLE_GROUPING,
	"header":controlTypes.ROLE_HEADER,
	"footer":controlTypes.ROLE_FOOTER,
	"paragraph":controlTypes.ROLE_PARAGRAPH,
	"ruler":controlTypes.ROLE_RULER,
	"edit bar":controlTypes.ROLE_EDITBAR,
}

JABStatesToNVDAStates={
	"checked":controlTypes.STATE_CHECKED,
	"focused":controlTypes.STATE_FOCUSED,
	"selected":controlTypes.STATE_SELECTED,
	"pressed":controlTypes.STATE_PRESSED,
	"expanded":controlTypes.STATE_EXPANDED,
	"collapsed":controlTypes.STATE_COLLAPSED,
}

class JABTextInfo(NVDAObjectTextInfo):

	def _getSelOffsets(self):
		info=self.obj.JABObject.getAccessibleTextSelectionInfo()
		start=info.selectionStartIndex
		end=info.selectionEndIndex
		if start<0:
			start=0
		if end<0:
			end=0
		return [start,end]

	def _getStoryText(self):
		if not hasattr(self,'_storyText'):
			storyLength=self._getStoryLength()
			self._storyText=self._getTextRange(0,storyLength)
		return self._storyText

	def _getStoryLength(self):
		if not hasattr(self,'_storyLength'):
			textInfo=self.obj.JABObject.getAccessibleTextInfo(self.obj._JABAccContextInfo.x,self.obj._JABAccContextInfo.y)
			self._storyLength=textInfo.charCount
		return self._storyLength

	def _getLineCount(self):
		return -1 

	def _getTextRange(self,start,end):
		#Java needs end of range as last character, not one past the last character
		return self.obj.JABObject.getAccessibleTextRange(start,end-1)

	def _lineNumFromOffset(self,offset):
		return -1

	def _getLineOffsets(self,offset):
		(start,end)=self.obj.JABObject.getAccessibleTextLineBounds(offset)
		#If start and end are 0, then something is broken in java
		if start==0 and end==0:
			return super(JABTextInfo,self)._getLineOffsets(offset)
		#Java gives end end as the last character, not one past the last character
		end=end+1
		return [start,end]

	def _getParagraphOffsets(self,offset):
		return super(EditTextInfo,self)._getLineOffsets(offset)

class JAB(Window):

	def __init__(self,JABObject):
		self.JABObject=JABObject
		self._JABAccContextInfo=JABObject.getAccessibleContextInfo()
		if self._JABAccContextInfo.accessibleText:
			self.TextInfo=JABTextInfo
			if self.JABRole in ["text","password text","edit bar","view port","paragraph"]:
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
		Window.__init__(self,self.JABObject.hwnd)
		self.reviewPosition=self.makeTextInfo(text.POSITION_CARET)

	def __eq__(self,other):
		if (id(self)==id(other)) or (self.__class__==other.__class__ and self.JABObject==other.JABObject):
			return True
		else:
			return False

	def __ne__(self,other):
		if (self.__class__!=other.__class__) or (self.JABObject!=other.JABObject):
			return True
		else:
			return False
 
	def _get_name(self):
		return self._JABAccContextInfo.name

	def _get_JABRole(self):
		return self._JABAccContextInfo.role_en_US

	def _get_role(self):
		return JABRolesToNVDARoles.get(self.JABRole,controlTypes.ROLE_UNKNOWN)

	def _get_JABStates(self):
		return self._JABAccContextInfo.states_en_US

	def _get_states(self):
		debug.writeMessage("states: %s"%self.JABStates)
		stateSet=set()
		stateString=self.JABStates
		for state in stateString.split(','):
			if JABStatesToNVDAStates.has_key(state):
				stateSet.add(JABStatesToNVDAStates[state])
		return stateSet

	def _get_value(self):
		value=None
		if self._JABAccContextInfo.accessibleText:
			info=self.makeTextInfo(text.POSITION_CARET)
			info.expand(text.UNIT_LINE)
			value=info.text
			if self.name==value:
				value=None
		if value is None and self.role not in [controlTypes.ROLE_CHECKBOX,controlTypes.ROLE_MENU,controlTypes.ROLE_MENUITEM,controlTypes.ROLE_RADIOBUTTON] and self._JABAccContextInfo.accessibleValue:
			value=self.JABObject.getCurrentAccessibleValueFromContext()
		return value

	def _get_description(self):
		return self._JABAccContextInfo.description

	def _get_hasFocus(self):
		if controlTypes.STATE_FOCUSED in self.states:
			return True
		else:
			return False

	def _get_positionString(self):
		if self._JABAccContextInfo.childrenCount:
			return None
		parent=self.parent
		if not parent or (self.role!=controlTypes.ROLE_RADIOBUTTON and parent.role not in [controlTypes.ROLE_TREEVIEW,controlTypes.ROLE_LIST]):
			return None
		index=self._JABAccContextInfo.indexInParent+1
		childCount=parent._JABAccContextInfo.childrenCount
		return _("%d of %d")%(index,childCount)



	def _get_activeChild(self):
		JABObject=self.JABObject.getActiveDescendent()
		if JABObject:
			return JAB(JABObject)
		else:
			return None

	def _get_parent(self):
		if not hasattr(self,'_parent'):
			JABObject=self.JABObject.getAccessibleParentFromContext()
			if JABObject:
				self._parent=JAB(JABObject)
		if hasattr(self,'_parent'):
			return self._parent
 
	def _get_next(self):
		JABObject=self.JABObject.getAccessibleParentFromContext()
		if not JABObject:
			return None
		parentInfo=JABObject.getAccessibleContextInfo()
		newIndex=self._JABAccContextInfo.indexInParent+1
		if newIndex>=parentInfo.childrenCount:
			return None
		JABObject=JABObject.getAccessibleChildFromContext(newIndex)
		if not JABObject:
			return None
		childInfo=JABObject.getAccessibleContextInfo()
		if childInfo.indexInParent==self._JABAccContextInfo.indexInParent:
			return None
		return JAB(JABObject)

	def _get_previous(self):
		JABObject=self.JABObject.getAccessibleParentFromContext()
		if not JABObject:
			return None
		parentInfo=JABObject.getAccessibleContextInfo()
		newIndex=self._JABAccContextInfo.indexInParent-1
		if newIndex<0:
			return None
		JABObject=JABObject.getAccessibleChildFromContext(newIndex)
		if not JABObject:
			return None
		childInfo=JABObject.getAccessibleContextInfo()
		if childInfo.indexInParent==self._JABAccContextInfo.indexInParent:
			return None
		return JAB(JABObject)

	def _get_firstChild(self):
		if self._JABAccContextInfo.childrenCount<=0:
			return None
		JABObject=self.JABObject.getAccessibleChildFromContext(0)
		if JABObject:
			return JAB(JABObject)
		else:
			return None

	def event_stateChange(self):
		self._JABAccContextInfo=self.JABObject.getAccessibleContextInfo()
		super(JAB,self).event_stateChange()

	def event_gainFocus(self):
		parent=self.parent
		if self.role in [controlTypes.ROLE_LIST,controlTypes.ROLE_EDITABLETEXT] and parent and parent.role==controlTypes.ROLE_COMBOBOX:
			return
		super(JAB,self).event_gainFocus()
