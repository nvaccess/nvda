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
		info=JABHandler.getAccessibleTextSelectionInfo(self.obj.JABVmID,self.obj.JABAccContext)
		return [info.selectionStart,info.selectionEnd]

	def _getStoryText(self):
		if not hasattr(self,'_storyText'):
			storyLength=self._getStoryLength()
			self._storyText=self._getTextRange(0,storyLength)
		return self._storyText

	def _getStoryLength(self):
		if not hasattr(self,'_storyLength'):
			textInfo=JABHandler.getAccessibleTextInfo(self.obj.JABVmID,self.obj.JABAccContext,self.obj._JABAccContextInfo.x,self.obj._JABAccContextInfo.y)
			self._storyLength=textInfo.charCount
		return self._storyLength

	def _getLineCount(self):
		return -1 

	def _getTextRange(self,start,end):
		return JABHandler.getAccessibleTextRange(self.obj.JABVmID,self.obj.JABAccContext,start,end)

	def _lineNumFromOffset(self,offset):
		return -1

	def _getLineOffsets(self,offset):
		return JABHandler.getAccessibleTextLineBounds(self.obj.JABVmID,self.obj.JABAccContext,offset)

	def _getParagraphOffsets(self,offset):
		return super(EditTextInfo,self)._getLineOffsets(offset)

class JAB(Window):

	def __init__(self,vmID,accContext,windowHandle=None):
		if windowHandle is None:
			#windowHandle=JABHandler.bridgeDll.getHWNDFromAccessibleContext(vmID,accContext)
			windowHandle=winUser.getForegroundWindow()
		debug.writeMessage("JAB windowHandle: %s"%windowHandle)
		self.JABVmID=vmID
		self.JABAccContext=accContext
		debug.writeMessage("JAB: about to call contextInfo")
		self._JABAccContextInfo=JABHandler.getAccessibleContextInfo(vmID,accContext)
		Window.__init__(self,windowHandle)

	def __del__(self):
		JABHandler.bridgeDll.releaseJavaObject(self.JABAccContext)

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

	def _get_description(self):
		return self._JABAccContextInfo.description

	def _get_activeChild(self):
		childAccContext=JABHandler.bridgeDll.getActiveDescendent(self.JABVmID,self.JABAccContext)
		if childAccContext<=0:
			return None
		return JAB(self.JABVmID,childAccContext)

	def _get_parent(self):
		parentAccContext=JABHandler.bridgeDll.getAccessibleParentFromContext(self.JABVmID,self.JABAccContext)
		if parentAccContext>0:
			return JAB(self.JABVmID,parentAccContext)

	def _get_next(self):
		parentAccContext=JABHandler.bridgeDll.getAccessibleParentFromContext(self.JABVmID,self.JABAccContext)
		if parentAccContext<=0:
			return None
		parentAccContextInfo=JABHandler.getAccessibleContextInfo(self.JABVmID,parentAccContext)
		newIndex=self._JABAccContextInfo.indexInParent+1
		if newIndex>=parentAccContextInfo.childrenCount:
			JABHandler.bridgeDll.releaseJavaObject(self.JABVmID,parentAccContext)
			return None
		childAccContext=JABHandler.bridgeDll.getAccessibleChildFromContext(self.JABVmID,parentAccContext,newIndex)
		if childAccContext<=0:
			JABHandler.bridgeDll.releaseJavaObject(self.JABVmID,parentAccContext)
			return None
		obj=JAB(self.JABVmID,childAccContext)
		if obj._JABAccContextInfo.indexInParent==self._JABAccContextInfo.indexInParent:
			return None
		return obj

	def _get_previous(self):
		parentAccContext=JABHandler.bridgeDll.getAccessibleParentFromContext(self.JABVmID,self.JABAccContext)
		if parentAccContext<=0:
			return None
		parentAccContextInfo=JABHandler.getAccessibleContextInfo(self.JABVmID,parentAccContext)
		newIndex=self._JABAccContextInfo.indexInParent-1
		if newIndex<0:
			JABHandler.bridgeDll.releaseJavaObject(self.JABVmID,parentAccContext)
			return None
		childAccContext=JABHandler.bridgeDll.getAccessibleChildFromContext(self.JABVmID,parentAccContext,newIndex)
		if childAccContext<=0:
			JABHandler.bridgeDll.releaseJavaObject(self.JABVmID,parentAccContext)
			return None
		obj=JAB(self.JABVmID,childAccContext)
		if obj._JABAccContextInfo.indexInParent==self._JABAccContextInfo.indexInParent:
			return None
		return obj

	def _get_firstChild(self):
		if self._JABAccContextInfo.childrenCount<=0:
			return None
		childAccContext=JABHandler.bridgeDll.getAccessibleChildFromContext(self.JABVmID,self.JABAccContext,0)
		return JAB(self.JABVmID,childAccContext)

