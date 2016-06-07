# appModule for visual studio
#author: mohammad suliman (mohmad.s93@gmail.com)

import appModuleHandler
from NVDAObjects.UIA import UIA, WpfTextView, Toast
from NVDAObjects.behaviors import RowWithoutCellObjects, RowWithFakeNavigation
from NVDAObjects.IAccessible import IAccessible, ContentGenericClient
from NVDAObjects.window import Desktop 
from NVDAObjects import NVDAObjectTextInfo
import textInfos
import controlTypes
import UIAHandler
import api
import ui
import tones
from logHandler import log
import eventHandler
import scriptHandler
from globalCommands import SCRCAT_FOCUS
import re
import speech
import config
import time

# some user configuration vars to control how the add-on behaves
announceIntelliSensePosInfo = False
beepOnBreakpoints = True
announceBreakpoints = True

# global vars

#whether last focused object was an intelliSense item
intelliSenseLastFocused = False
#last focused intelliSense object
lastFocusedIntelliSenseItem = None
#whether the caret has moved to a different line in the code editor 
caretMovedToDifferentLine = False
#visual studio version
studioVersion = None

class AppModule(appModuleHandler.AppModule):

	def __init__(self, processID, appName=None):
		super(AppModule, self).__init__(processID, appName)
		#put the version of visual studio in the global variable, so other parts of the code have access to it
		global studioVersion 
		studioVersion = self.productVersion

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.role == controlTypes.ROLE_TAB and isinstance(obj, UIA) and obj.UIAElement.currentClassName == "TabItem":
			clsList.insert(0, editorTabItem)
		elif obj.role == controlTypes.ROLE_TABCONTROL and isinstance(obj, UIA) and obj.UIAElement.currentClassName == "DocumentGroup":
			clsList.insert(0, editorTabControl)
		elif isinstance(obj, UIA) and obj.UIAElement.currentClassName == "IntellisenseMenuItem" and obj.role == controlTypes.ROLE_MENUITEM:
			clsList.insert(0, IntelliSenseMenuItem)
		elif isinstance(obj, UIA) and obj.UIAElement.currentClassName == "MenuItem" and obj.role == controlTypes.ROLE_MENUITEM:
			clsList.insert(0, VSMenuItem)
		elif obj.name == 'Treegrid Accessibility' and obj.role == controlTypes.ROLE_WINDOW:
			clsList.insert(0, VarsTreeView)
		elif obj.name is None and obj.windowClassName == 'TREEGRID' and obj.role == controlTypes.ROLE_PANE:
			clsList.insert(0, BadVarView)
		elif isinstance(obj, UIA) and obj.UIAElement.currentClassName == "TextMarker" and obj.role == controlTypes.ROLE_UNKNOWN and obj.name.startswith("Breakpoint"):
			clsList.insert(0, Breakpoint)
		elif obj.name == "Text Editor" and obj.role == controlTypes.ROLE_EDITABLETEXT:
			clsList.insert(0, TextEditor)
		elif obj.role == controlTypes.ROLE_DATAITEM and isinstance(obj, UIA) and obj.UIAElement.currentClassName == "ListViewItem":
			clsList.insert(0, ErrorsListItem)
		elif obj.name == "Quick Info Tool Tip" and obj.role == controlTypes.ROLE_TOOLTIP:
			clsList.insert(0, QuickInfoToolTip)
		elif obj.name == "Signature Help" and obj.role == controlTypes.ROLE_UNKNOWN and isinstance(obj, UIA) and obj.UIAElement.currentClassName == "WpfSignatureHelp":
			clsList.insert(0, ParameterInfo)
		elif obj.role == controlTypes.ROLE_LISTITEM and obj.windowClassName == "TBToolboxPane":
			clsList.insert(0, ToolboxItem)
		elif obj.name == "Active Files" and obj.role in (controlTypes.ROLE_DIALOG, controlTypes.ROLE_LIST):
			clsList.insert(0, SwitcherDialog)
		elif obj.windowClassName.startswith("WindowsForms10.") and obj.windowText != "PropertyGridView":
			clsList.insert(0, FormsComponent)
		elif isinstance(obj, UIA) and obj.UIAElement.currentClassName == "ViewPresenter" and obj.role == controlTypes.ROLE_PANE:
			clsList.insert(0, EditorAncestor)

	def event_NVDAObject_init(self, obj):
		if obj.name == "Active Files" and obj.role in (controlTypes.ROLE_DIALOG, controlTypes.ROLE_LIST):
			#this object reports the descktop object as its parent, this causes 2 issues 
			#redundent announcement of the foreground object 
			#and losing the real foreground object which makes reporting the status bar script not reliable, which is crootial for breakpoint reporting to work.
			obj.role = controlTypes.ROLE_LIST
			parent = obj.parent
			if isinstance(parent, Desktop):
				obj.parent = api.getForegroundObject()
			#description here also is redundant, so, remove it
			obj.description = ""
		elif obj.windowClassName == "ToolWindowSelectAccList":
			#all objects with this window class name have a description which is identical to the name
			#don't think that someone is interested to hear it
			obj.description = ""

	def event_appModule_loseFocus(self):
		global intelliSenseLastFocused
		global lastFocusedIntelliSenseItem
		lastFocusedIntelliSenseItem		= None
		intelliSenseLastFocused = False

	def event_gainFocus(self, obj, nextHandler):
		global intelliSenseLastFocused, lastFocusedIntelliSenseItem
		intelliSenseLastFocused = False
		lastFocusedIntelliSenseItem = None
		if self._shouldIgnoreFocusEvent(obj):
			return 
		nextHandler()

	def _shouldIgnoreFocusEvent(self, obj):
		if obj.name is None and obj.role == controlTypes.ROLE_UNKNOWN and obj.windowClassName == "TBToolboxPane":
			return True

#almost copied from NVDA core with minor modifications
	def script_reportStatusLine(self, gesture):
		#it seems that the status bar is the last child of the forground object
		#so, get it from there
		obj = api.getForegroundObject().lastChild
		found=False
		if obj and obj.role == controlTypes.ROLE_STATUSBAR:
			text = api.getStatusBarText(obj)
			api.setNavigatorObject(obj)
			found=True
		else:
			info=api.getForegroundObject().flatReviewPosition
			if info:
				info.expand(textInfos.UNIT_STORY)
				info.collapse(True)
				info.expand(textInfos.UNIT_LINE)
				text=info.text
				info.collapse()
				api.setReviewPosition(info)
				found=True
		if not found:
			# Translators: Reported when there is no status line for the current program or window.
			ui.message(_("No status line found"))
			return
		if scriptHandler.getLastScriptRepeatCount()==0:
			ui.message(text)
		else:
			speech.speakSpelling(text)
	# Translators: Input help mode message for report status line text command.
	script_reportStatusLine.__doc__ = _("Reads the current application status bar and moves the navigator to it. If pressed twice, spells the information")
	script_reportStatusLine.category=SCRCAT_FOCUS

	def script_reportParameterInfo(self, gesture):
		# get the parameter info object
		try:
			obj = api.getForegroundObject().firstChild.firstChild
		except:
			return
		if obj.role == controlTypes.ROLE_TOOLTIP:
			# emulate an alert event for this object
			eventHandler.queueEvent("alert", obj)

	__gestures = {
		"kb:NVDA+End": "reportStatusLine",
		"kb:control+shift+space": "reportParameterInfo"
	}


def _shouldIgnoreEditorAncestorFocusEvents():
	global intelliSenseLastFocused
	return intelliSenseLastFocused == True

class editorTabItem(UIA):
	"""one of the editor focus ancestors, we ignore focus entered events in some cases 
	see _shouldIgnoreEditorAncestorFocusEvents for more info
	"""

	def event_focusEntered(self):
		if _shouldIgnoreEditorAncestorFocusEvents():
			return
		return super(editorTabItem, self).event_focusEntered()

class editorTabControl(UIA):
	"""one of the editor focus ancestors, we ignore focus entered events in some cases 
	see _shouldIgnoreEditorAncestorFocusEvents for more info
	"""

	def event_focusEntered(self):
		if _shouldIgnoreEditorAncestorFocusEvents():
			return
		return super(editorTabControl, self).event_focusEntered()


REG_CUT_POS_INFO = re.compile(" \d+ of \d+$")
REG_GET_ITEM_INDEX = re.compile("^ \d+")
REG_GET_GROUP_COUNT = re.compile("\d+$")

class IntelliSenseMenuItem(UIA):

	def _get_states(self):
		states = set()
		#only fetch the states witch are likely to change
		#fetching some states for this view can throw an exception, which causes a latency
		e=self.UIACachedStatesElement
		try:
			hasKeyboardFocus=e.cachedHasKeyboardFocus
		except COMError:
			hasKeyboardFocus=False
		if hasKeyboardFocus:
			states.add(controlTypes.STATE_FOCUSED)
		# Don't fetch the role unless we must, but never fetch it more than once.
		role=None
		if e.getCachedPropertyValue(UIAHandler.UIA_IsSelectionItemPatternAvailablePropertyId):
			role=self.role
			states.add(controlTypes.STATE_CHECKABLE if role==controlTypes.ROLE_RADIOBUTTON else controlTypes.STATE_SELECTABLE)
			if e.getCachedPropertyValue(UIAHandler.UIA_SelectionItemIsSelectedPropertyId):
				states.add(controlTypes.STATE_CHECKED if role==controlTypes.ROLE_RADIOBUTTON else controlTypes.STATE_SELECTED)
		# those states won't change for this UI element, so add them to the states set
		states.add(controlTypes.STATE_FOCUSABLE)
		states.add(controlTypes.STATE_READONLY)
		return states

	def event_gainFocus(self):
		global intelliSenseLastFocused
		global lastFocusedIntelliSenseItem
		intelliSenseLastFocused = True
		lastFocusedIntelliSenseItem = self
		super(IntelliSenseMenuItem, self).event_gainFocus()

	def _get_name(self):
		# by default, the name of the intelliSense menu item includes the position info
		#so, remove it
		oldName = super(IntelliSenseMenuItem, self).name
		newName = re.sub(REG_CUT_POS_INFO, "", oldName)
		return newName

	def _get_positionInfo(self):
		"""gets the position info of the intelliSense menu item based on the original name
		the user can turn that off by setting to false the appropriate flag
		"""
		if announceIntelliSensePosInfo == False:
			return {}
		oldName = super(intelliSenseMenuItem, self).name
		info={}
		if re.search(REG_CUT_POS_INFO, oldName) is None:
			return {}
		positionalInfoStr = re.search(REG_CUT_POS_INFO, oldName).group()
		itemIndex = int(re.search(REG_GET_ITEM_INDEX, positionalInfoStr).group())
		if itemIndex>0:
			info['indexInGroup']=itemIndex
		groupCount = int(re.search(REG_GET_GROUP_COUNT, positionalInfoStr).group())
		if groupCount>0:
			info['similarItemsInGroup'] = groupCount
		return info


class VarsTreeView(IAccessible):
	"""the parent view of the variables view in the locals / autos/ watch windows"""

	role = controlTypes.ROLE_TREEVIEW
	name = ''

	def event_focusEntered(self):
		speech.speakObject(self,reason=controlTypes.REASON_FOCUSENTERED)

# a regular expression for removing level info from first child's value, see _get_positionInfo for more info
REG_CUT_LEVEL_INFO = re.compile(" @ tree depth \d+$")
#a regular expression for getting the level from the first matching child value, see _get_positionInfo for more info
REG_GET_LEVEL = re.compile("\d+$")
class BadVarView(ContentGenericClient):
	"""the view that showes the variable info (name, value, type) in the locals / autos / watch windows
	also, the call stack window uses this view to expose its info
	"""

	role = controlTypes.ROLE_TREEVIEWITEM
	TextInfo=NVDAObjectTextInfo

	def _getMatchingParentChildren(self):
		parentChildren = self.parent.children
		matchingChildren = []
		for index, child in enumerate(parentChildren):
			if controlTypes.STATE_SELECTED in child.states or controlTypes.STATE_FOCUSED in child.states and not child.name.startswith("[Column"):
				matchingChildren.append(parentChildren[index + 1])
				matchingChildren.append(parentChildren[index + 2])
				if self._isCallStackWindow():
					break
				matchingChildren.append(parentChildren[index + 3])
				break
		return matchingChildren

	def _isCallStackWindow(self):
		try:
			return self.parent.parent.parent.parent.name == "Call Stack"
		except:
			return False

	def isDuplicateIAccessibleEvent(self,obj):
		if isinstance(obj, BadVarView):
			return self == obj
		return super(BadVarView, self).isDuplicateIAccessibleEvent(obj)

	def _get_name(self):
		matchingChildren = self._getMatchingParentChildren()
		if matchingChildren is None:
			return None
		if len(matchingChildren) < 2:
			return None
		res  = []
		for child in matchingChildren:
			name = child.name
			value = child.value
			#remove the level info 
			value = str(value)
			value = re.sub(REG_CUT_LEVEL_INFO, "", value)
			res.append(name + ": ")
			res.append(value)
			res.append(", ")
		#remove last coma 
		res.pop(-1)
		return "".join(res)

	def _get_states(self):
		superStates = super(BadVarView, self).states
		matchingChildren = self._getMatchingParentChildren()
		if matchingChildren is None:
			return superStates
		if len(matchingChildren) == 0:
			return superStates
		states = matchingChildren[0]._get_states() | superStates
		if self.name.startswith("Name: None"):
			#if this happens, then the view has no meaningful info
			states.add(controlTypes.STATE_UNAVAILABLE)
		return states

	def _isEqual(self, other):
		if not isinstance(other, BadVarView):
			return False
		return self is other

	def _get_positionInfo(self):
		# only calculate the level
		#the level is found in the first matching child's value. which is usually the name of the variable
		#suppose  the view shows info about a var called i, which is not a part of an array, then value string will be as following
		# i @ tree depth 1
		#index in group,  similar items in group are not easy to calculate, and it won't be efficien
		matchingChildStr = self._getMatchingParentChildren().pop(0).value
		matchingChildStr = str(matchingChildStr)
		levelStr = re.search(REG_GET_LEVEL, matchingChildStr)
		if levelStr is None:
			return {}
		levelStr = levelStr.group()
		if not levelStr.isdigit():
			return {}
		level = int(levelStr)
		if level <= 0:
			return {}
		info = {}
		info["level"] = level
		return info

	def event_stateChange(self):
		#we don't need to report this event for 2 reasons:
		#expand / collapse events is faked with the scripts below, they won't work otherwise
		#the view is more responsive without reporting this event
		return 

	def event_gainFocus(self):
		if self.hasFocus == False:
			#don't report  focus event for this view if the hasFocus property is False
			#this event is redundant and confusing, and a correct focus event will be fired after this one
			return
		self.parent.firstChild = self
		super(BadVarView, self).event_gainFocus()

	def event_typedCharacter(self, ch):
		#default implementation of typedCharacter causes VS and NVDA to crash badly, if the user hits esc while in the quick watch window
		#only speek typed characters if needed
		if config.conf["keyboard"]["speakTypedCharacters"] and ord(ch)>=32:
			speech.speakSpelling(ch)
		return

	def script_expand(self, gesture):
		if controlTypes.STATE_COLLAPSED in self.states:
			ui.message(_("expanded"))
		gesture.send()
		return

	def script_collapse(self, gesture):
		if controlTypes.STATE_EXPANDED in self.states:
			ui.message(_("collapsed"))
		gesture.send()
		return

	__gestures = {
		"kb:leftArrow": "collapse",
		"kb:rightArrow": "expand"
	}


class VSMenuItem(UIA):
	"""ordinary menu items in visual studio"""

	def _get_states(self):
		states = super(VSMenuItem, self)._get_states()
		# visual studio exposes the menu item which has a sub menu as collapsed
		#add HASPOP state to fix NVDA behavior when this state is present
		if controlTypes.STATE_COLLAPSED in states:
			states.add(controlTypes.STATE_HASPOPUP)
		#this state is redundant in this context, it causes NVDA to say "not checked" for each menu item
		states.discard(controlTypes.STATE_CHECKABLE)
		return states

#this method is only a work around til the issue #6021 is resolved
	def _get_keyboardShortcut(self):
		ret = ""
		try:
			ret += self.UIAElement.currentAccessKey
		except COMError:
			pass
		if ret != "":
			#add a double space to the end of the string
			ret +="  "
		try:
			ret += self.UIAElement.currentAcceleratorKey
		except COMError:
			pass
		return ret


REG_GET_LINE_TEXT = re.compile("Ln \d+")
REG_GET_LINE_NUM = re.compile("\d+$")

def _getCurLineNumber():
	"""gets current line number which has the caret in the editor based on status bar text"""
	obj = api.getForegroundObject().lastChild
	text = None
	if obj and obj.role == controlTypes.ROLE_STATUSBAR:
		text = api.getStatusBarText(obj)
	if not text:
		return 0
	lineInfo = re.search(REG_GET_LINE_TEXT, text)
	if not lineInfo:
		return 0
	lineInfo = lineInfo.group()
	lineNum = re.search(REG_GET_LINE_NUM, lineInfo)
	if not lineNum:
		return 0
	lineNum = int(lineNum.group())
	if lineNum <= 0:
		return 0
	return lineNum

REG_GET_BREAKPOINT_STATE = re.compile("Enabled|Disabled")

class Breakpoint(UIA):
	"""a class for break point control to allow us to detect and report break points once the caret reaches a line with break point""" 

	def event_nameChange(self):
		global caretMovedToDifferentLine
		# return if we already announced the break point for the current line 
		if not caretMovedToDifferentLine:
			return
		caretMovedToDifferentLine = False
		currentLineNum = _getCurLineNumber()
		BPLineNum = self._getLineNumber()
		if currentLineNum == 0 or BPLineNum == 0 \
		or currentLineNum != BPLineNum:
			return
		global announceBreakpoints, beepOnbreakPoints
		if beepOnBreakpoints:
			tones.beep(1000, 50)
		if not announceBreakpoints:
			return
		message = _("breakpoint")
		state = re.search(REG_GET_BREAKPOINT_STATE, self.name)
		if  state:
			message += ", " 
			message += state.group()
		ui.message(message)

	def _getLineNumber(self):
		"""gets the line number of the breakpoint based on the automation ID"""
		try:
			ret=self.UIAElement.currentAutomationID
		except Exception as e:
			return 0
		lineNum = re.search(REG_GET_LINE_NUM, ret)
		if not lineNum:
			return 0
		lineNum = int(lineNum.group())
		if lineNum <= 0:
			return 0
		return lineNum

class TextEditor(WpfTextView):
	"""VS text editor view 
	we need this class to try to tell whether the caret has moved to a different line 
	this helps us to not make several announcements of the same breakpoint when moving the caret left and rite on the same line
	also, commands for navigating the code with the debugger now causes NVDA to report the line which was executed.
	"""

	description = ""

	def event_gainFocus(self):
		global lastFocusedIntelliSenseItem, intelliSenseLastFocused
		# in many cases, the editor fire focus events when intelliSense menu is opened, which leads to a lengthy announcements after reporting the current intelliSense item
		#so, allow the focus to return to the editor if that happens, but don't report the focus event, and set the navigator object to be last reported intelliSense item to allow the user to review
		if self._isCompletionPopupShowing():
			api.setNavigatorObject(lastFocusedIntelliSenseItem)
			intelliSenseLastFocused = True
			return 
		super(TextEditor, self).event_gainFocus()

	def _isCompletionPopupShowing(self):
		obj = api.getForegroundObject()
		try:
			if obj.firstChild.firstChild.firstChild.next.next.role == controlTypes.ROLE_POPUPMENU:
				return True
		except Exception as e:
			pass
		try:
			obj1 = obj .firstChild
			obj2 = obj1.firstChild
			if obj1.role == controlTypes.ROLE_WINDOW and obj1.name == ''\
			and obj2.role == controlTypes.ROLE_WINDOW and obj2.name == '':
				return True
		except Exception as e:
			pass
		return False

	def script_caret_moveByLine(self, gesture):
		global caretMovedToDifferentLine
		caretMovedToDifferentLine = True
		super(TextEditor, self).script_caret_moveByLine(gesture)

#this method is only a work around til the bug with compareing UIA bookmarks is resolved
#we need to bind debugger stepping commands to  moveByLine only 
	def script_debugger_step(self, gesture):
		global caretMovedToDifferentLine
		caretMovedToDifferentLine = True
		try:
			info=self.makeTextInfo(textInfos.POSITION_CARET)
		except:
			log.debug("exception")
			gesture.send()
			return
		bookmark=info.bookmark
		gesture.send()
		for i in xrange(4):
			caretMoved,newInfo=self._hasCaretMoved(bookmark)
		if not caretMoved:
			log.debug("caret move failed")
		self._caretScriptPostMovedHelper(textInfos.UNIT_LINE,gesture,newInfo)

	__gestures = {
		"kb:f10": "debugger_step",
		"kb:f11": "debugger_step",
		"kb:f5": "debugger_step",
		"kb:shift+f11": "debugger_step"
	}


REG_SPLIT_ERROR = re.compile("(Severity:.*)(Code:.*)(Description:.*\r?\n?.*)(Project:.*)(File:.*)(Line:.*)")
REG_SPLIT_ERROR_NO_CODE_COL = re.compile("(Severity:.*)(Description:.*\r?\n?.*)(Project:.*)(File:.*)(Line:.*)")
REG_SPLIT_ERROR_NO_FILE_COL = re.compile("(Severity:.*)(Code:.*)(Description:.*\r?\n?.*)(Project:.*)(Line:.*)")
REG_SPLIT_ERROR_NO_LINE_COL = re.compile("(Severity:.*)(Code:.*)(Description:.*\r?\n?.*)(Project:.*)(File:.*)")
class ErrorsListItem(RowWithoutCellObjects, RowWithFakeNavigation, UIA):
	""" a class for list item of the errors list
	the goal is to enable the user to navigate each row with NVDA's commands for navigating tables (ctrl+alt+right/left arrow). in addition, it is possible to move directly to a column with ctrl + alt + number, where the number is the column number we wish to move to
	"""

	def _getColumnContent(self, column):
		children = UIA._get_children(self)
		try:
			return children[column - 1].firstChild.name
		except Exception as e:
			log.debug(e)
		return ""


	def _getColumnHeader(self, column):
		text = self._getColumnContentAndHeader(column)
		# extract the header
		text = text.split(":", 1)[0]
		#remove spaces if there are any
		text = text.strip()
		return text

	def _getColumnContentAndHeader(self, column):
		global REG_SPLIT_ERROR, REG_SPLIT_ERROR_NO_CODE_COL, REG_SPLIT_ERROR_NO_FILE_COL, REG_SPLIT_ERROR_NO_LINE_COL
		if column < 1 or column > 6:
			return ""
		try:
			return re.search(REG_SPLIT_ERROR, self.name).group(column)
		except:
			pass
		try:
			return re.search(REG_SPLIT_ERROR_NO_CODE_COL, self.name).group(column)
		except:
			pass
		try:
			return re.search(REG_SPLIT_ERROR_NO_FILE_COL, self.name).group(column)
		except:
			pass
		try:
			return re.search(REG_SPLIT_ERROR_NO_LINE_COL, self.name).group(column)
		except:
			pass
		return ""

	def _getColumnLocation(self,column):
		if column < 1 or column > self.childCount:
			return None
		child = None
		try:
			child = UIA._get_children(self)[column - 1].firstChild
		except Exception as e:
			log.debug(e)
		if not child:
			return None
		return child.location

	def _get_childCount(self):
		return len(UIA._get_children(self))

	def initOverlayClass(self):
		for i in xrange(10):
			self.bindGesture("kb:control+alt+" + str(i), "moveToColumn")

	def script_moveToColumn(self, gesture):
		keyName = gesture.displayName
		# extract the number from the key name
		columnNum = re.search("\d+$", keyName).group()
		columnNum = int(columnNum)
		if columnNum > self.childCount + 1or columnNum == 0:
			return
		self._moveToColumnNumber(columnNum)


class QuickInfoToolTip(Toast):

	def _get_name(self):
		return "Quick Info"

	def _get_description(self):
		# this view has a long description, don't think the user wants to hear it every tiem he invokes the quick info
		return ""

#think the parameter info is useless, the info which is exposed to screen readers seems very poor compared to the description of this view in VS documentation
#so, I am seriously considering removing it
class ParameterInfo (Toast):
	role = controlTypes.ROLE_TOOLTIP

	def _get_description(self):
		return ""

class ToolboxItem(IAccessible):
	role = controlTypes.ROLE_TREEVIEWITEM

	def event_gainFocus(self):
		badStates = set((controlTypes.STATE_INVISIBLE, controlTypes.STATE_UNAVAILABLE, controlTypes.STATE_OFFSCREEN))
		if badStates.issubset(self.states) or controlTypes.STATE_SELECTED not in self.states:
			#if the focus object has those states, or the object don't has a selected state, don't report this invalid focus event.
			#a valid focus event will be fired after then.
			return
		super(ToolboxItem, self).event_gainFocus()

	def event_stateChange(self):
		#no need to report state change for this object for the following reasons:
		#on expand / collaps: a focus event is fired
		#a state change event is fired when moving between tool box items, and causes NVDA to announce "not available" each time
		return 

	def _get_value(self):
		#the value is exposed as level info, don't report it
		return 

	def _get_positionInfo(self):
		info = {}
		level = super(ToolboxItem, self).value
		#the level is zero based, unlike NVDA's convention of 1 based level, so, fix it.
		level = int(level)
		level += 1
		info["level"] = level
		return info

class SwitcherDialog(IAccessible):
	"""the view of the file / tool windows switcher which is used to move between opened files and active tool windows
	in latest version of VS (2015 currently), only gainFocus event method is needed to report the first selected entry when a file is opened
	in older versions, this view manages all the user interaction with this view. AKA moving between entries using the corresponding keyboard commands
	"""

	def initOverlayClass(self):
		#all entries of the dialog (active files and active tool windows entries)
		self.entries = []
		#whether a focus entered event should be fired to the active files list
		self.shouldFireFocusEnteredEventFiles = True
		#whether a focus entered event should be fired to the active tool windows  list
		self.shouldFireFocusEnteredEventTools = True

	def event_gainFocus(self):
		#add active files entries 
		try:
			self.entries.extend(self.children[1].children)
		except:
			#no active files
			pass
		#add active tool windows entries
		try:
			self.entries.extend(self.children[0].children)
		except:
			#no active tool windows, this should not happen never
			pass
		self._reportSelectedEntry()

	def _getSelectedEntry(self):
		for entry in self.entries:
			if controlTypes.STATE_SELECTED in entry.states:
				return entry
		return None

	def _reportSelectedEntry(self):
		obj = self._getSelectedEntry()
		if obj is None:
			return
		self._reportFocusEnteredEventForParent(obj)
		api.setNavigatorObject(obj)
		speech.speakObject(obj, reason=controlTypes.REASON_FOCUS)

	def _reportFocusEnteredEventForParent(self, obj):
		"""checks if we need to fire a focusEntered event for the selected entry's parent, and fires an event if we need to"""
		if obj.parent.name == "Active Files" and self.shouldFireFocusEnteredEventFiles:
			eventHandler.executeEvent("focusEntered", obj.parent)
			self.shouldFireFocusEnteredEventFiles = False
			self.shouldFireFocusEnteredEventTools = True
		if obj.parent.name == "Active Tool Windows" and self.shouldFireFocusEnteredEventTools:
			eventHandler.executeEvent("focusEntered", obj.parent)
			self.shouldFireFocusEnteredEventFiles = True
			self.shouldFireFocusEnteredEventTools = False

	def script_onEntryChange(self, gesture):
		gesture.send()
		if studioVersion.startswith('14.0'):
			#if VS 2015 is the current version, then don't do any thing, a correct focus event will be fired, and the controle will move to the focused view.
			return
		self._reportSelectedEntry()

	__gestures = {
		"kb:control+downArrow": "onEntryChange",
		"kb:control+upArrow": "onEntryChange",
		"kb:control+leftArrow": "onEntryChange",
		"kb:control+rightArrow": "onEntryChange",
		"kb:control+tab": "onEntryChange",
		"kb:control+shift+tab": "onEntryChange"
		}


REG_SPLIT_LOCATION_TEXT = re.compile("(\d+), (\d+) (\d+), (\d+)")

class FormsComponent(IAccessible):
	"""the UI component in windows forms designer """

	def script_onSizeChange(self, gesture):
		gesture.send()
		#get the position from the status bar
		obj = api.getForegroundObject().lastChild
		text = obj.children[2].name
		width = re.match(REG_SPLIT_LOCATION_TEXT, text).group(3)
		hight = re.match(REG_SPLIT_LOCATION_TEXT, text).group(4)
		msg = _("width: %s  hight: %s" %(width, hight))
		ui.message(msg)

	def script_onLocationChange(self, gesture):
		gesture.send()
		#get the location from the status bar
		obj = api.getForegroundObject().lastChild
		text = obj.children[2].name
		x = re.match(REG_SPLIT_LOCATION_TEXT, text).group(1)
		y = re.match(REG_SPLIT_LOCATION_TEXT, text).group(2)
		msg = "X: %s  y: %s" %(x, y)
		ui.message(msg)

	__gestures = {
		"kb:shift+upArrow": "onSizeChange",
		"kb:shift+downArrow": "onSizeChange",
		"kb:shift+rightArrow": "onSizeChange",
		"kb:shift+leftArrow": "onSizeChange",
		"kb:control+upArrow": "onLocationChange",
		"kb:control+downArrow": "onLocationChange",
		"kb:control+rightArrow": "onLocationChange",
		"kb:control+leftArrow": "onLocationChange",
		"kb:upArrow": "onLocationChange",
		"kb:downArrow": "onLocationChange",
		"kb:leftArrow": "onLocationChange",
		"kb:rightArrow": "onLocationChange"
	}

class EditorAncestor(UIA):
	"""an ancestor of the code editor, we need this because this control returns true incorrectly when comparing it with other instance of the same type
	this causes NVDA to not execute focus entered events when it should do
	the issue is present when using ctrl + f6 / ctrl + shift + f6 to move between openned code editors
	"""
	
	def _isEqual(self, other):
		return False

