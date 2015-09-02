import ctypes
import re
import eventHandler
import keyLabels
import JABHandler
import controlTypes
from ..window import Window
from ..behaviors import EditableTextWithoutAutoSelectDetection, Dialog
import textInfos.offsets
from logHandler import log
from .. import InvalidNVDAObject

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
	"root pane":controlTypes.ROLE_PANEL,
	"glass pane":controlTypes.ROLE_PANEL,
	"layered pane":controlTypes.ROLE_PANEL,
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
		if end==-1 and offset>0:
			# #1892: JAB returns -1 for the end insertion position
			# instead of returning the offsets for the last line.
			# Try one character back.
			(start,end)=self.obj.jabContext.getAccessibleTextLineBounds(offset-1)
		#Java gives end as the last character, not one past the last character
		end=end+1
		return (start,end)

	def _getParagraphOffsets(self,offset):
		return self._getLineOffsets(offset)

	def _getFormatFieldAndOffsets(self, offset, formatConfig, calculateOffsets=True):
		attribs, length = self.obj.jabContext.getTextAttributesInRange(offset, self._endOffset - 1)
		field = textInfos.FormatField()
		field["font-family"] = attribs.fontFamily
		field["font-size"] = "%dpt" % attribs.fontSize
		field["bold"] = bool(attribs.bold)
		field["italic"] = bool(attribs.italic)
		field["strikethrough"] = bool(attribs.strikethrough)
		field["underline"] = bool(attribs.underline)
		if attribs.superscript:
			field["text-position"] = "super"
		elif attribs.subscript:
			field["text-position"] = "sub"
		# TODO: Not sure how to interpret Java's alignment numbers.
		return field, (offset, offset + length)

	def getEmbeddedObject(self, offset=0):
		offset += self._startOffset

		# We need to count the embedded objects to determine which child to use.
		# This could possibly be optimised by caching.
		text = self._getTextRange(0, offset + 1)
		childIndex = text.count(u"\uFFFC") - 1
		jabContext=self.obj.jabContext.getAccessibleChildFromContext(childIndex)
		if jabContext:
			return JAB(jabContext=jabContext)

		raise LookupError

class JAB(Window):

	def findOverlayClasses(self,clsList):
		role = self.JABRole
		if self._JABAccContextInfo.accessibleText and role in ("text","password text","edit bar","view port","paragraph"):
			clsList.append(EditableTextWithoutAutoSelectDetection)
		elif role in ("dialog", "alert"):
			clsList.append(Dialog)
		elif role=="combo box":
			clsList.append(ComboBox)
		elif role=="table":
			clsList.append(Table)
		elif self.parent and isinstance(self.parent,Table) and self.parent._jabTableInfo:
			clsList.append(TableCell)
		clsList.append(JAB)

	@classmethod
	def kwargsFromSuper(cls,kwargs,relation=None):
		jabContext=None
		windowHandle=kwargs['windowHandle']
		if relation=="focus":
			vmID=ctypes.c_int()
			accContext=JABHandler.JOBJECT64()
			JABHandler.bridgeDll.getAccessibleContextWithFocus(windowHandle,ctypes.byref(vmID),ctypes.byref(accContext))
			jabContext=JABHandler.JABContext(hwnd=windowHandle,vmID=vmID.value,accContext=accContext.value)
		elif isinstance(relation,tuple):
			jabContext=JABHandler.JABContext(hwnd=windowHandle)
			if jabContext:
				jabContext=jabContext.getAccessibleContextAt(*relation)
		else:
			jabContext=JABHandler.JABContext(hwnd=windowHandle)
		if not jabContext:
			return False
		kwargs['jabContext']=jabContext
		return True

	def __init__(self,relation=None,windowHandle=None,jabContext=None):
		if not windowHandle:
			windowHandle=jabContext.hwnd
		self.windowHandle=windowHandle
		self.jabContext=jabContext
		super(JAB,self).__init__(windowHandle=windowHandle)
		try:
			self._JABAccContextInfo
		except RuntimeError:
			raise InvalidNVDAObject("Could not get accessible context info")

	def _get__JABAccContextInfo(self):
		return self.jabContext.getAccessibleContextInfo()

	def _get_TextInfo(self):
		if self._JABAccContextInfo.accessibleText and self.role not in [controlTypes.ROLE_BUTTON,controlTypes.ROLE_MENUITEM,controlTypes.ROLE_MENU,controlTypes.ROLE_LISTITEM]:
			return JABTextInfo
		return super(JAB,self).TextInfo

	def _isEqual(self,other):
		return super(JAB,self)._isEqual(other) and self.jabContext==other.jabContext

	def _get_keyboardShortcut(self):
		bindings=self.jabContext.getAccessibleKeyBindings()
		if not bindings or bindings.keyBindingsCount<1: 
			return None
		shortcutsList=[]
		for index in xrange(bindings.keyBindingsCount):
			binding=bindings.keyBindingInfo[index]
			# We don't support these modifiers
			if binding.modifiers&(JABHandler.ACCESSIBLE_META_KEYSTROKE|JABHandler.ACCESSIBLE_ALT_GRAPH_KEYSTROKE|JABHandler.ACCESSIBLE_BUTTON1_KEYSTROKE|JABHandler.ACCESSIBLE_BUTTON2_KEYSTROKE|JABHandler.ACCESSIBLE_BUTTON3_KEYSTROKE):
				continue
			keyList=[]
			# We assume alt  if there are no modifiers at all and its not a menu item as this is clearly a nmonic
			if (binding.modifiers&JABHandler.ACCESSIBLE_ALT_KEYSTROKE) or (not binding.modifiers and self.role!=controlTypes.ROLE_MENUITEM):
				keyList.append(keyLabels.localizedKeyLabels['alt'])
			if binding.modifiers&JABHandler.ACCESSIBLE_CONTROL_KEYSTROKE:
				keyList.append(keyLabels.localizedKeyLabels['control'])
			if binding.modifiers&JABHandler.ACCESSIBLE_SHIFT_KEYSTROKE:
				keyList.append(keyLabels.localizedKeyLabels['shift'])
			keyList.append(binding.character)
		shortcutsList.append("+".join(keyList))
		return ", ".join(shortcutsList)

	def _get_name(self):
		return re_simpleXmlTag.sub(" ", self._JABAccContextInfo.name)

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
		if role==controlTypes.ROLE_LABEL:
			return controlTypes.ROLE_STATICTEXT
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
		targets=self._getJABRelationTargets('memberOf')
		for index,target in enumerate(targets):
			if target==self.jabContext:
				return {'indexInGroup':index+1,'similarItemsInGroup':len(targets)}
		parent=self.parent
		if isinstance(parent,JAB) and self.role in (controlTypes.ROLE_TREEVIEWITEM,controlTypes.ROLE_LISTITEM):
			index=self._JABAccContextInfo.indexInParent+1
			childCount=parent._JABAccContextInfo.childrenCount
			return {'indexInGroup':index,'similarItemsInGroup':childCount}
		return {}

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
		if self.indexInParent is None:
			return None
		newIndex=self.indexInParent+1
		if newIndex>=parent._JABAccContextInfo.childrenCount:
			return None
		jabContext=parent.jabContext.getAccessibleChildFromContext(newIndex)
		if not jabContext:
			return None
		obj=JAB(jabContext=jabContext)
		if not isinstance(obj.parent,JAB):
			obj.parent=parent
		if obj.indexInParent is None:
			obj.indexInParent=newIndex
		elif obj.indexInParent<=self.indexInParent: 
			return None
		return obj

	def _get_previous(self):
		parent=self.parent
		if not isinstance(parent,JAB):
			return super(JAB,self).previous
		if self.indexInParent is None:
			return None
		newIndex=self.indexInParent-1
		if newIndex<0:
			return None
		jabContext=parent.jabContext.getAccessibleChildFromContext(newIndex)
		if not jabContext:
			return None
		obj=JAB(jabContext=jabContext)
		if not isinstance(obj.parent,JAB):
			obj.parent=parent
		if obj.indexInParent is None:
			obj.indexInParent=newIndex
		elif obj.indexInParent>=self.indexInParent: 
			return None
		return obj

	def _get_firstChild(self):
		if self._JABAccContextInfo.childrenCount<=0:
			return None
		jabContext=self.jabContext.getAccessibleChildFromContext(0)
		if jabContext:
			obj=JAB(jabContext=jabContext)
			if not isinstance(obj.parent,JAB):
				obj.parent=self
			if obj.indexInParent is None:
				obj.indexInParent=0
			return obj
		else:
			return None

	def _get_lastChild(self):
		if self._JABAccContextInfo.childrenCount<=0:
			return None
		jabContext=self.jabContext.getAccessibleChildFromContext(self.childCount-1)
		if jabContext:
			obj=JAB(jabContext=jabContext)
			if not isinstance(obj.parent,JAB):
				obj.parent=self
			if obj.indexInParent is None:
				obj.indexInParent=self.childCount-1
			return obj
		else:
			return None

	def _get_childCount(self):
		return self._JABAccContextInfo.childrenCount

	def _get_children(self):
		children=[]
		for index in xrange(self._JABAccContextInfo.childrenCount):
			jabContext=self.jabContext.getAccessibleChildFromContext(index)
			if jabContext:
				obj=JAB(jabContext=jabContext)
				if not isinstance(obj.parent,JAB):
					obj.parent=self
				if obj.indexInParent is None:
					obj.indexInParent=index
				children.append(obj)
		return children

	def _get_indexInParent(self):
		index = self._JABAccContextInfo.indexInParent
		if index == -1:
			return None
		return index

	def _getJABRelationTargets(self, key):
		rs = self.jabContext.getAccessibleRelationSet()
		targets=[]
		for relation in rs.relations[:rs.relationCount]:
			for target in relation.targets[:relation.targetCount]:
				if relation.key == key:
					targets.append(JABHandler.JABContext(self.jabContext.hwnd, self.jabContext.vmID, target))
				else:
					JABHandler.bridgeDll.releaseJavaObject(self.jabContext.vmID,target)
		return targets

	def _get_flowsTo(self):
		targets=self._getJABRelationTargets("flowsTo")
		if targets:
			return targets[0]

	def _get_flowsFrom(self):
		targets=self._getJABRelationTargets("flowsFrom")
		if targets:
			return targets[0]

	def reportFocus(self):
		parent=self.parent
		if self.role in [controlTypes.ROLE_LIST] and isinstance(parent,JAB) and parent.role==controlTypes.ROLE_COMBOBOX:
			return
		super(JAB,self).reportFocus()

	def _get__actions(self):
		actions = JABHandler.AccessibleActions()
		JABHandler.bridgeDll.getAccessibleActions(self.jabContext.vmID, self.jabContext.accContext, actions)
		return actions.actionInfo[:actions.actionsCount]

	def _get_actionCount(self):
		return len(self._actions)

	def getActionName(self, index=None):
		if index is None:
			index = self.defaultActionIndex
		try:
			return self._actions[index].name
		except IndexError:
			raise NotImplementedError

	def doAction(self, index=None):
		if index is None:
			index = self.defaultActionIndex
		try:
			JABHandler.bridgeDll.doAccessibleActions(self.jabContext.vmID, self.jabContext.accContext,
				JABHandler.AccessibleActionsToDo(actionsCount=1, actions=(self._actions[index],)),
				JABHandler.jint())
		except (IndexError, RuntimeError):
			raise NotImplementedError

	def _get_activeDescendant(self):
		descendantFound=False
		jabContext=self.jabContext
		while jabContext:
			try:
				tempContext=jabContext.getActiveDescendent()
			except:
				break
			if not tempContext:
				break
			try:
				depth=tempContext.getObjectDepth()
			except:
				depth=-1
			if depth<=0 or tempContext==jabContext: 
				break
			jabContext=tempContext
			descendantFound=True
		if descendantFound:
			return JAB(jabContext=jabContext)

	def event_gainFocus(self):
		if eventHandler.isPendingEvents("gainFocus"):
			return
		super(JAB,self).event_gainFocus()
		if eventHandler.isPendingEvents("gainFocus"):
			return
		activeDescendant=self.activeDescendant
		if activeDescendant:
			eventHandler.queueEvent("gainFocus",activeDescendant)

class ComboBox(JAB):

	def _get_states(self):
		states=super(ComboBox,self).states
		if controlTypes.STATE_COLLAPSED not in states and controlTypes.STATE_EXPANDED not in states:
			if self.childCount==1 and self.firstChild and self.firstChild.role==controlTypes.ROLE_POPUPMENU:
				if controlTypes.STATE_INVISIBLE in self.firstChild.states:
					states.add(controlTypes.STATE_COLLAPSED)
				else:
					states.add(controlTypes.STATE_EXPANDED)
		return states

	def _get_activeDescendant(self):
		if controlTypes.STATE_COLLAPSED in self.states:
			return None
		return super(ComboBox,self).activeDescendant

	def _get_value(self):
		value=super(ComboBox,self).value
		if not value and not self.activeDescendant: 
			descendant=super(ComboBox,self).activeDescendant
			if descendant:
				value=descendant.name
		return value

class Table(JAB):

	def _get__jabTableInfo(self):
		info=self.jabContext.getAccessibleTableInfo()
		if info:
			self._jabTableInfo=info
			return info

	def _get_rowCount(self):
		if self._jabTableInfo:
			return self._jabTableInfo.rowCount

	def _get_columnCount(self):
		if self._jabTableInfo:
			return self._jabTableInfo.columnCount

	def _get_tableID(self):
		return self._jabTableInfo.jabTable.accContext.value

class TableCell(JAB):

	role=controlTypes.ROLE_TABLECELL

	def _get_table(self):
		if self.parent and isinstance(self.parent,Table):
			self.table=self.parent
			return self.table

	def _get_tableID(self):
		return self.table.tableID

	def _get_rowNumber(self):
		return self.table._jabTableInfo.jabTable.getAccessibleTableRow(self.indexInParent)+1

	def _get_columnNumber(self):
		return self.table._jabTableInfo.jabTable.getAccessibleTableColumn(self.indexInParent)+1

	def _get_rowHeaderText(self):
		headerTableInfo=self.table.jabContext.getAccessibleTableRowHeader()
		if headerTableInfo and headerTableInfo.jabTable:
			textList=[]
			row=self.rowNumber-1
			for col in xrange(headerTableInfo.columnCount):
				cellInfo=headerTableInfo.jabTable.getAccessibleTableCellInfo(row,col)
				if cellInfo and cellInfo.jabContext:
					obj=JAB(jabContext=cellInfo.jabContext)
					if obj.name: textList.append(obj.name)
					if obj.description: textList.append(obj.description)
			jabContext=self.table._jabTableInfo.jabTable.getAccessibleTableRowDescription(row)
			if jabContext:
				obj=JAB(jabContext=jabContext)
				if obj.name: textList.append(obj.name)
				if obj.description: textList.append(obj.description)
			return " ".join(textList)

	def _get_columnHeaderText(self):
		headerTableInfo=self.table.jabContext.getAccessibleTableColumnHeader()
		if headerTableInfo and headerTableInfo.jabTable:
			textList=[]
			col=self.columnNumber-1
			for row in xrange(headerTableInfo.rowCount):
				cellInfo=headerTableInfo.jabTable.getAccessibleTableCellInfo(row,col)
				if cellInfo and cellInfo.jabContext:
					obj=JAB(jabContext=cellInfo.jabContext)
					if obj.name: textList.append(obj.name)
					if obj.description: textList.append(obj.description)
			jabContext=self.table._jabTableInfo.jabTable.getAccessibleTableColumnDescription(col)
			if jabContext:
				obj=JAB(jabContext=jabContext)
				if obj.name: textList.append(obj.name)
				if obj.description: textList.append(obj.description)
			return " ".join(textList)
