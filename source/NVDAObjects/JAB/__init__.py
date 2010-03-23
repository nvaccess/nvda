import ctypes
import re
import JABHandler
import controlTypes
from ..window import Window
from ..behaviors import EditableTextWithoutAutoSelectDetection
import textInfos.offsets
from logHandler import log

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
	"busy":controlTypes.STATE_BUSY,
	"checked":controlTypes.STATE_CHECKED,
	"focused":controlTypes.STATE_FOCUSED,
	"selected":controlTypes.STATE_SELECTED,
	"pressed":controlTypes.STATE_PRESSED,
	"expanded":controlTypes.STATE_EXPANDED,
	"collapsed":controlTypes.STATE_COLLAPSED,
	"iconified":controlTypes.STATE_ICONIFIED,
	"modal":controlTypes.STATE_MODAL,
	"multi_line":controlTypes.STATE_MULTILINE,
	"focusable":controlTypes.STATE_FOCUSABLE,
	"editable":controlTypes.STATE_EDITABLE,
}

re_simpleXmlTag=re.compile(r"\<[^>]+\>")

class JABTextInfo(textInfos.offsets.OffsetsTextInfo):

	def _getOffsetFromPoint(self,x,y):
		info=self.obj.jabContext.getAccessibleTextInfo(x,y)
		offset=max(min(info.indexAtPoint,info.charCount-1),0)
		return offset

	def _getCaretOffset(self):
		textInfo=self.obj.jabContext.getAccessibleTextInfo(self.obj._JABAccContextInfo.x,self.obj._JABAccContextInfo.y)
		offset=textInfo.caretIndex
		# OpenOffice sometimes returns nonsense, so treat charCount < offset as no caret.
		if offset==-1 or textInfo.charCount<offset:
			raise RuntimeError("no available caret in this object")
		return offset

	def _setCaretOffset(self,offset):
		self.obj.jabContext.setCaretPosition(offset)

	def _getSelectionOffsets(self):
		info=self.obj.jabContext.getAccessibleTextSelectionInfo()
		start=max(info.selectionStartIndex,0)
		end=max(info.selectionEndIndex,0)
		return (start,end)

	def _setSelectionOffsets(self,start,end):
		self.obj.jabContext.selectTextRange(start,end)

	def _getStoryLength(self):
		if not hasattr(self,'_storyLength'):
			textInfo=self.obj.jabContext.getAccessibleTextInfo(self.obj._JABAccContextInfo.x,self.obj._JABAccContextInfo.y)
			self._storyLength=textInfo.charCount
		return self._storyLength

	def _getTextRange(self,start,end):
		#Java needs end of range as last character, not one past the last character
		text=self.obj.jabContext.getAccessibleTextRange(start,end-1)
		return text

	def _getLineNumFromOffset(self,offset):
		return None

	def _getLineOffsets(self,offset):
		(start,end)=self.obj.jabContext.getAccessibleTextLineBounds(offset)
		#Java gives end as the last character, not one past the last character
		end=end+1
		return [start,end]

	def _getParagraphOffsets(self,offset):
		return self._getLineOffsets(offset)

class JAB(Window):

	def findOverlayClasses(self,clsList):
		if self._JABAccContextInfo.accessibleText and self.JABRole in ("text","password text","edit bar","view port","paragraph"):
			clsList.append(EditableTextWithoutAutoSelectDetection)
		clsList.append(JAB)
		return clsList

	@classmethod
	def objectFromPoint(cls,x,y,windowHandle=None):
		jabContext=JABHandler.JABContext(hwnd=windowHandle)
		if not jabContext:
			return
		newJabContext=jabContext.getAccessibleContextAt(x,y)
		if not newJabContext:
			return
		return JAB(jabContext=newJabContext)

	@classmethod
	def objectWithFocus(cls,windowHandle=None):
		vmID=ctypes.c_int()
		accContext=ctypes.c_int()
		JABHandler.bridgeDll.getAccessibleContextWithFocus(windowHandle,ctypes.byref(vmID),ctypes.byref(accContext))
		jabContext=JABHandler.JABContext(hwnd=windowHandle,vmID=vmID.value,accContext=accContext.value)
		focusObject=JAB(jabContext=jabContext)
		activeChild=focusObject.activeChild
		if activeChild and activeChild.role!=controlTypes.ROLE_UNKNOWN:
			focusObject=activeChild
		if focusObject.role==controlTypes.ROLE_UNKNOWN:
			return
		return focusObject

	def __init__(self,relation=None,windowHandle=None,jabContext=None):
		if windowHandle and not jabContext:
			jabContext=JABHandler.JABContext(hwnd=windowHandle)
		elif jabContext and not windowHandle:
			windowHandle=jabContext.hwnd
		elif not windowHandle and not jabContext:
			raise TypeError("Give either a valid window handle or jab context")
		self.windowHandle=windowHandle
		self.jabContext=jabContext
		self._JABAccContextInfo=jabContext.getAccessibleContextInfo()
		super(JAB,self).__init__(windowHandle=windowHandle)

	def _get_TextInfo(self):
		if self._JABAccContextInfo.accessibleText and self.role not in [controlTypes.ROLE_BUTTON,controlTypes.ROLE_MENUITEM,controlTypes.ROLE_MENU,controlTypes.ROLE_LISTITEM]:
			return JABTextInfo
		return super(JAB,self).TextInfo

	def _isEqual(self,other):
		return super(JAB,self)._isEqual(other) and self.jabContext==other.jabContext

	def _get_name(self):
		return self._JABAccContextInfo.name

	def _get_JABRole(self):
		return self._JABAccContextInfo.role_en_US

	def _get_role(self):
		role = JABRolesToNVDARoles.get(self.JABRole,controlTypes.ROLE_UNKNOWN)
		if role in ( controlTypes.ROLE_LABEL, controlTypes.ROLE_PANEL) and self.parent:
			parentRole = self.parent.role
			if parentRole == controlTypes.ROLE_LIST:
				return controlTypes.ROLE_LISTITEM
			elif parentRole in (controlTypes.ROLE_TREEVIEW, controlTypes.ROLE_TREEVIEWITEM):
				return controlTypes.ROLE_TREEVIEWITEM
		return role

	def _get_JABStates(self):
		return self._JABAccContextInfo.states_en_US

	def _get_states(self):
		log.debug("states: %s"%self.JABStates)
		stateSet=set()
		stateString=self.JABStates
		stateStrings=stateString.split(',')
		for state in stateStrings:
			if JABStatesToNVDAStates.has_key(state):
				stateSet.add(JABStatesToNVDAStates[state])
		if "visible" not in stateStrings:
			stateSet.add(controlTypes.STATE_INVISIBLE)
		if "showing" not in stateStrings:
			stateSet.add(controlTypes.STATE_OFFSCREEN)
		if "expandable" not in stateStrings:
			stateSet.discard(controlTypes.STATE_COLLAPSED)
		return stateSet

	def _get_value(self):
		if self.role not in [controlTypes.ROLE_CHECKBOX,controlTypes.ROLE_MENU,controlTypes.ROLE_MENUITEM,controlTypes.ROLE_RADIOBUTTON,controlTypes.ROLE_BUTTON] and self._JABAccContextInfo.accessibleValue and not self._JABAccContextInfo.accessibleText:
			return self.jabContext.getCurrentAccessibleValueFromContext()

	def _get_description(self):
		return re_simpleXmlTag.sub(" ", self._JABAccContextInfo.description)

	def _get_location(self):
		return (self._JABAccContextInfo.x,self._JABAccContextInfo.y,self._JABAccContextInfo.width,self._JABAccContextInfo.height)

	def _get_hasFocus(self):
		if controlTypes.STATE_FOCUSED in self.states:
			return True
		else:
			return False

	def _get_positionInfo(self):
		if self._JABAccContextInfo.childrenCount:
			return {}
		parent=self.parent
		if not isinstance(parent,JAB) or (self.role!=controlTypes.ROLE_RADIOBUTTON and parent.role not in [controlTypes.ROLE_TREEVIEW,controlTypes.ROLE_LIST]):
			return {}
		index=self._JABAccContextInfo.indexInParent+1
		childCount=parent._JABAccContextInfo.childrenCount
		return {'indexInGroup':index,'similarItemsInGroup':childCount}


	def _get_activeChild(self):
		jabContext=self.jabContext.getActiveDescendent()
		if jabContext:
			return JAB(jabContext=jabContext)
		else:
			return None

	def _get_parent(self):
		if not hasattr(self,'_parent'):
			jabContext=self.jabContext.getAccessibleParentFromContext()
			if jabContext:
				self._parent=JAB(jabContext=jabContext)
			else:
				self._parent=super(JAB,self).parent
		return self._parent
 
	def _get_next(self):
		parent=self.parent
		if not isinstance(parent,JAB):
			return super(JAB,self).next
		newIndex=self._JABAccContextInfo.indexInParent+1
		if newIndex>=parent._JABAccContextInfo.childrenCount:
			return None
		jabContext=parent.jabContext.getAccessibleChildFromContext(newIndex)
		if not jabContext:
			return None
		childInfo=jabContext.getAccessibleContextInfo()
		if childInfo.indexInParent==self._JABAccContextInfo.indexInParent:
			return None
		return JAB(jabContext=jabContext)

	def _get_previous(self):
		parent=self.parent
		if not isinstance(parent,JAB):
			return super(JAB,self).previous
		newIndex=self._JABAccContextInfo.indexInParent-1
		if newIndex<0:
			return None
		jabContext=parent.jabContext.getAccessibleChildFromContext(newIndex)
		if not jabContext:
			return None
		childInfo=jabContext.getAccessibleContextInfo()
		if childInfo.indexInParent==self._JABAccContextInfo.indexInParent:
			return None
		return JAB(jabContext=jabContext)

	def _get_firstChild(self):
		if self._JABAccContextInfo.childrenCount<=0:
			return None
		jabContext=self.jabContext.getAccessibleChildFromContext(0)
		if jabContext:
			return JAB(jabContext=jabContext)
		else:
			return None

	def _get_lastChild(self):
		if self._JABAccContextInfo.childrenCount<=0:
			return None
		jabContext=self.jabContext.getAccessibleChildFromContext(self._JABAccContextInfo.childrenCount-1)
		if jabContext:
			return JAB(jabContext=jabContext)
		else:
			return None

	def _get_children(self):
		children=[]
		for index in range(self._JABAccContextInfo.childrenCount):
			jabContext=self.jabContext.getAccessibleChildFromContext(index)
			if jabContext:
				children.append(JAB(jabContext=jabContext))
		return children

	def event_stateChange(self):
		self._JABAccContextInfo=self.jabContext.getAccessibleContextInfo()
		super(JAB,self).event_stateChange()

	def reportFocus(self):
		parent=self.parent
		if self.role in [controlTypes.ROLE_LIST] and isinstance(parent,JAB) and parent.role==controlTypes.ROLE_COMBOBOX:
			return
		super(JAB,self).reportFocus()
