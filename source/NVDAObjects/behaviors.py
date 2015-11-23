# -*- coding: UTF-8 -*-
#NVDAObjects/behaviors.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2013 NV Access Limited, Peter Vágner

"""Mix-in classes which provide common behaviour for particular types of controls across different APIs.
"""

import os
import time
import threading
import difflib
import tones
import queueHandler
import eventHandler
import controlTypes
import speech
import characterProcessing
import config
from . import NVDAObject, NVDAObjectTextInfo
import textInfos
import editableText
from logHandler import log
import api
import ui
import braille

class ProgressBar(NVDAObject):

	progressValueCache={} #key is made of "speech" or "beep" and an x,y coordinate, value is the last percentage

	def event_valueChange(self):
		pbConf=config.conf["presentation"]["progressBarUpdates"]
		states=self.states
		if pbConf["progressBarOutputMode"]=="off" or controlTypes.STATE_INVISIBLE in states or controlTypes.STATE_OFFSCREEN in states:
			return super(ProgressBar,self).event_valueChange()
		val=self.value
		try:
			percentage = min(max(0.0, float(val.strip("%\0"))), 100.0)
		except (AttributeError, ValueError):
			log.debugWarning("Invalid value: %r" % val)
			return super(ProgressBar, self).event_valueChange()
		braille.handler.handleUpdate(self)
		if not pbConf["reportBackgroundProgressBars"] and not self.isInForeground:
			return
		try:
			left,top,width,height=self.location
		except:
			left=top=width=height=0
		x=left+(width/2)
		y=top+(height/2)
		lastBeepProgressValue=self.progressValueCache.get("beep,%d,%d"%(x,y),None)
		if pbConf["progressBarOutputMode"] in ("beep","both") and (lastBeepProgressValue is None or abs(percentage-lastBeepProgressValue)>=pbConf["beepPercentageInterval"]):
			tones.beep(pbConf["beepMinHZ"]*2**(percentage/25.0),40)
			self.progressValueCache["beep,%d,%d"%(x,y)]=percentage
		lastSpeechProgressValue=self.progressValueCache.get("speech,%d,%d"%(x,y),None)
		if pbConf["progressBarOutputMode"] in ("speak","both") and (lastSpeechProgressValue is None or abs(percentage-lastSpeechProgressValue)>=pbConf["speechPercentageInterval"]):
			queueHandler.queueFunction(queueHandler.eventQueue,speech.speakMessage,_("%d percent")%percentage)
			self.progressValueCache["speech,%d,%d"%(x,y)]=percentage

class Dialog(NVDAObject):
	"""Overrides the description property to obtain dialog text.
	"""

	@classmethod
	def getDialogText(cls,obj,allowFocusedDescendants=True):
		"""This classmethod walks through the children of the given object, and collects up and returns any text that seems to be  part of a dialog's message text.
		@param obj: the object who's children you want to collect the text from
		@type obj: L{IAccessible}
		@param allowFocusedDescendants: if false no text will be returned at all if one of the descendants is focused.
		@type allowFocusedDescendants: boolean
		"""
		children=obj.children
		textList=[]
		childCount=len(children)
		for index in xrange(childCount):
			child=children[index]
			childStates=child.states
			childRole=child.role
			#We don't want to handle invisible or unavailable objects
			if controlTypes.STATE_INVISIBLE in childStates or controlTypes.STATE_UNAVAILABLE in childStates: 
				continue
			#For particular objects, we want to descend in to them and get their children's message text
			if childRole in (controlTypes.ROLE_PROPERTYPAGE,controlTypes.ROLE_PANE,controlTypes.ROLE_PANEL,controlTypes.ROLE_WINDOW,controlTypes.ROLE_GROUPING,controlTypes.ROLE_PARAGRAPH,controlTypes.ROLE_SECTION,controlTypes.ROLE_TEXTFRAME,controlTypes.ROLE_UNKNOWN):
				#Grab text from descendants, but not for a child which inherits from Dialog and has focusable descendants
				#Stops double reporting when focus is in a property page in a dialog
				childText=cls.getDialogText(child,not isinstance(child,Dialog))
				if childText:
					textList.append(childText)
				elif childText is None:
					return None
				continue
			#If the child is focused  we should just stop and return None
			if not allowFocusedDescendants and controlTypes.STATE_FOCUSED in child.states:
				return None
			# We only want text from certain controls.
			if not (
				 # Static text, labels and links
				 childRole in (controlTypes.ROLE_STATICTEXT,controlTypes.ROLE_LABEL,controlTypes.ROLE_LINK)
				# Read-only, non-multiline edit fields
				or (childRole==controlTypes.ROLE_EDITABLETEXT and controlTypes.STATE_READONLY in childStates and controlTypes.STATE_MULTILINE not in childStates)
			):
				continue
			#We should ignore a text object directly after a grouping object, as it's probably the grouping's description
			if index>0 and children[index-1].role==controlTypes.ROLE_GROUPING:
				continue
			#Like the last one, but a graphic might be before the grouping's description
			if index>1 and children[index-1].role==controlTypes.ROLE_GRAPHIC and children[index-2].role==controlTypes.ROLE_GROUPING:
				continue
			childName=child.name
			if childName and index<(childCount-1) and children[index+1].role not in (controlTypes.ROLE_GRAPHIC,controlTypes.ROLE_STATICTEXT,controlTypes.ROLE_SEPARATOR,controlTypes.ROLE_WINDOW,controlTypes.ROLE_PANE,controlTypes.ROLE_BUTTON) and children[index+1].name==childName:
				# This is almost certainly the label for the next object, so skip it.
				continue
			isNameIncluded=child.TextInfo is NVDAObjectTextInfo or childRole in (controlTypes.ROLE_LABEL,controlTypes.ROLE_STATICTEXT)
			childText=child.makeTextInfo(textInfos.POSITION_ALL).text
			if not childText or childText.isspace() and child.TextInfo is not NVDAObjectTextInfo:
				childText=child.basicText
				isNameIncluded=True
			if not isNameIncluded:
				# The label isn't in the text, so explicitly include it first.
				if childName:
					textList.append(childName)
			if childText:
				textList.append(childText)
		return "\n".join(textList)

	def _get_description(self):
		superDesc = super(Dialog, self).description
		if superDesc and not superDesc.isspace():
			# The object already provides a useful description, so don't override it.
			return superDesc
		return self.getDialogText(self)

	value = None

	def _get_isPresentableFocusAncestor(self):
		# Only fetch this the first time it is requested,
		# as it is very slow due to getDialogText and the answer shouldn't change anyway.
		self.isPresentableFocusAncestor = res = super(Dialog, self).isPresentableFocusAncestor
		return res

class EditableText(editableText.EditableText, NVDAObject):
	"""Provides scripts to report appropriately when moving the caret in editable text fields.
	This does not handle selection changes.
	To handle selection changes, use either L{EditableTextWithAutoSelectDetection} or L{EditableTextWithoutAutoSelectDetection}.
	"""

	shouldFireCaretMovementFailedEvents = True

	def initOverlayClass(self):
		# #4264: the caret_newLine script can only be bound for processes other than NVDA's process
		# As Pressing enter on an edit field can cause modal dialogs to appear, yet gesture.send and api.processPendingEvents may call.wx.yield which ends in a freeze. 
		if self.announceNewLineText and self.processID!=os.getpid():
			self.bindGesture("kb:enter","caret_newLine")

class EditableTextWithAutoSelectDetection(EditableText):
	"""In addition to L{EditableText}, handles reporting of selection changes for objects which notify of them.
	To have selection changes reported, the object must notify of selection changes via the caret event.
	Optionally, it may notify of changes to content via the textChange, textInsert and textRemove events.
	If the object supports selection but does not notify of selection changes, L{EditableTextWithoutAutoSelectDetection} should be used instead.
	"""

	def event_gainFocus(self):
		super(EditableText, self).event_gainFocus()
		self.initAutoSelectDetection()

	def event_caret(self):
		super(EditableText, self).event_caret()
		if self is api.getFocusObject():
			self.detectPossibleSelectionChange()

	def event_textChange(self):
		self.hasContentChangedSinceLastSelection = True

	def event_textInsert(self):
		self.hasContentChangedSinceLastSelection = True

	def event_textRemove(self):
		self.hasContentChangedSinceLastSelection = True

class EditableTextWithoutAutoSelectDetection(editableText.EditableTextWithoutAutoSelectDetection, EditableText):
	"""In addition to L{EditableText}, provides scripts to report appropriately when the selection changes.
	This should be used when an object does not notify of selection changes.
	"""

	initOverlayClass = editableText.EditableTextWithoutAutoSelectDetection.initClass

class LiveText(NVDAObject):
	"""An object for which new text should be reported automatically.
	These objects present text as a single chunk
	and only fire an event indicating that some part of the text has changed; i.e. they don't provide the new text.
	Monitoring must be explicitly started and stopped using the L{startMonitoring} and L{stopMonitoring} methods.
	The object should notify of text changes using the textChange event.
	"""
	#: The time to wait before fetching text after a change event.
	STABILIZE_DELAY = 0
	# If the text is live, this is definitely content.
	presentationType = NVDAObject.presType_content

	announceNewLineText=False

	def initOverlayClass(self):
		self._event = threading.Event()
		self._monitorThread = None
		self._keepMonitoring = False

	def startMonitoring(self):
		"""Start monitoring for new text.
		New text will be reported when it is detected.
		@note: If monitoring has already been started, this will have no effect.
		@see: L{stopMonitoring}
		"""
		if self._monitorThread:
			return
		thread = self._monitorThread = threading.Thread(target=self._monitor)
		thread.daemon = True
		self._keepMonitoring = True
		self._event.clear()
		thread.start()

	def stopMonitoring(self):
		"""Stop monitoring previously started with L{startMonitoring}.
		@note: If monitoring has not been started, this will have no effect.
		@see: L{startMonitoring}
		"""
		if not self._monitorThread:
			return
		self._keepMonitoring = False
		self._event.set()
		self._monitorThread = None

	def event_textChange(self):
		"""Fired when the text changes.
		@note: It is safe to call this directly from threads other than the main thread.
		"""
		self._event.set()

	def _getTextLines(self):
		"""Retrieve the text of this object in lines.
		This will be used to determine the new text to speak.
		The base implementation uses the L{TextInfo}.
		However, subclasses should override this if there is a better way to retrieve the text.
		@return: The current lines of text.
		@rtype: list of str
		"""
		return list(self.makeTextInfo(textInfos.POSITION_ALL).getTextInChunks(textInfos.UNIT_LINE))

	def _reportNewText(self, line):
		"""Report a line of new text.
		"""
		speech.speakText(line)

	def _monitor(self):
		try:
			oldLines = self._getTextLines()
		except:
			log.exception("Error getting initial lines")
			oldLines = []

		while self._keepMonitoring:
			self._event.wait()
			if not self._keepMonitoring:
				break
			if self.STABILIZE_DELAY > 0:
				# wait for the text to stabilise.
				time.sleep(self.STABILIZE_DELAY)
				if not self._keepMonitoring:
					# Monitoring was stopped while waiting for the text to stabilise.
					break
			self._event.clear()

			try:
				newLines = self._getTextLines()
				if config.conf["presentation"]["reportDynamicContentChanges"]:
					outLines = self._calculateNewText(newLines, oldLines)
					if len(outLines) == 1 and len(outLines[0]) == 1:
						# This is only a single character,
						# which probably means it is just a typed character,
						# so ignore it.
						del outLines[0]
					for line in outLines:
						queueHandler.queueFunction(queueHandler.eventQueue, self._reportNewText, line)
				oldLines = newLines
			except:
				log.exception("Error getting lines or calculating new text")

	def _calculateNewText(self, newLines, oldLines):
		outLines = []

		prevLine = None
		for line in difflib.ndiff(oldLines, newLines):
			if line[0] == "?":
				# We're never interested in these.
				continue
			if line[0] != "+":
				# We're only interested in new lines.
				prevLine = line
				continue
			text = line[2:]
			if not text or text.isspace():
				prevLine = line
				continue

			if prevLine and prevLine[0] == "-" and len(prevLine) > 2:
				# It's possible that only a few characters have changed in this line.
				# If so, we want to speak just the changed section, rather than the entire line.
				prevText = prevLine[2:]
				textLen = len(text)
				prevTextLen = len(prevText)
				# Find the first character that differs between the two lines.
				for pos in xrange(min(textLen, prevTextLen)):
					if text[pos] != prevText[pos]:
						start = pos
						break
				else:
					# We haven't found a differing character so far and we've hit the end of one of the lines.
					# This means that the differing text starts here.
					start = pos + 1
				# Find the end of the differing text.
				if textLen != prevTextLen:
					# The lines are different lengths, so assume the rest of the line changed.
					end = textLen
				else:
					for pos in xrange(textLen - 1, start - 1, -1):
						if text[pos] != prevText[pos]:
							end = pos + 1
							break

				if end - start < 15:
					# Less than 15 characters have changed, so only speak the changed chunk.
					text = text[start:end]

			if text and not text.isspace():
				outLines.append(text)
			prevLine = line

		return outLines

class Terminal(LiveText, EditableText):
	"""An object which both accepts text input and outputs text which should be reported automatically.
	This is an L{EditableText} object,
	as well as a L{liveText} object for which monitoring is automatically enabled and disabled based on whether it has focus.
	"""
	role = controlTypes.ROLE_TERMINAL

	def event_gainFocus(self):
		super(Terminal, self).event_gainFocus()
		self.startMonitoring()

	def event_loseFocus(self):
		self.stopMonitoring()

class CandidateItem(NVDAObject):

	def getFormattedCandidateName(self,number,candidate):
		if config.conf["inputComposition"]["alwaysIncludeShortCharacterDescriptionInCandidateName"]:
			describedSymbols=[]
			for symbol in candidate:
				try:
					symbolDescriptions=characterProcessing.getCharacterDescription(speech.getCurrentLanguage(),symbol) or []
				except TypeError:
					symbolDescriptions=[]
				if len(symbolDescriptions)>=1:
					description=symbolDescriptions[0]
					if description.startswith('(') and description.endswith(')'):
						describedSymbols.append(description[1:-1])
					else:
						# Translators: a message announcing a candidate's character and description.
						describedSymbols.append(_(u"{symbol} as in {description}").format(symbol=symbol,description=description))
				else:
					describedSymbols.append(symbol)
			candidate=u", ".join(describedSymbols)
		# Translators: a formatted message announcing a candidate's number and candidate text.
		return _(u"{number} {candidate}").format(number=number,candidate=candidate)

	def getFormattedCandidateDescription(self,candidate):
		descriptions=[]
		numSymbols=len(candidate) if candidate else 0
		if numSymbols!=1: return u""
		symbol=candidate[0]
		try:
			symbolDescriptions=characterProcessing.getCharacterDescription(speech.getCurrentLanguage(),symbol) or []
		except TypeError:
			symbolDescriptions=[]
		if config.conf["inputComposition"]["alwaysIncludeShortCharacterDescriptionInCandidateName"]:
			symbolDescriptions=symbolDescriptions[1:]
		if len(symbolDescriptions)<1: return u""
		return u", ".join(symbolDescriptions)

	def reportFocus(self):
		if not config.conf["inputComposition"]["announceSelectedCandidate"]: return
		text=self.name
		desc=self.description
		if desc:
			text+=u", "+desc
		speech.speakText(text)

	def _get_visibleCandidateItemsText(self):
		obj=self
		textList=[]
		while isinstance(obj,CandidateItem) and isinstance(obj.candidateNumber,int) and controlTypes.STATE_INVISIBLE not in obj.states:
			textList.append(obj.name)
			obj=obj.previous
		textList.reverse()
		obj=self.next
		while isinstance(obj,CandidateItem) and isinstance(obj.candidateNumber,int) and controlTypes.STATE_INVISIBLE not in obj.states:
			textList.append(obj.name)
			obj=obj.next
		if len(textList)<=1: return None
		self.visibleCandidateItemsText=(u", ".join(textList))+u", "
		return self.visibleCandidateItemsText

class RowWithFakeNavigation(NVDAObject):
	"""Provides table navigation commands for a row which doesn't support them natively.
	The cells must be exposed as children and they must support the table cell properties.
	"""

	_savedColumnNumber = None

	def _moveToColumn(self, obj):
		if not obj:
			ui.message(_("edge of table"))
			return
		if obj is not self:
			# Use the focused copy of the row as the parent for all cells to make comparison faster.
			obj.parent = self
		api.setNavigatorObject(obj)
		speech.speakObject(obj, reason=controlTypes.REASON_FOCUS)

	def _moveToColumnNumber(self, column):
		child = column - 1
		if child >= self.childCount:
			return
		cell = self.getChild(child)
		self._moveToColumn(cell)

	def script_moveToNextColumn(self, gesture):
		cur = api.getNavigatorObject()
		if cur == self:
			new = self.firstChild
		elif cur.parent != self:
			new = self
		else:
			new = cur.next
		self._moveToColumn(new)
	script_moveToNextColumn.canPropagate = True
	# Translators: The description of an NVDA command.
	script_moveToNextColumn.__doc__ = _("Moves the navigator object to the next column")

	def script_moveToPreviousColumn(self, gesture):
		cur = api.getNavigatorObject()
		if cur == self:
			new = None
		elif cur.parent != self or cur.columnNumber == 1:
			new = self
		else:
			new = cur.previous
		self._moveToColumn(new)
	script_moveToPreviousColumn.canPropagate = True
	# Translators: The description of an NVDA command.
	script_moveToPreviousColumn.__doc__ = _("Moves the navigator object to the previous column")

	def reportFocus(self):
		col = self._savedColumnNumber
		if not col:
			return super(RowWithFakeNavigation, self).reportFocus()
		self.__class__._savedColumnNumber = None
		self._moveToColumnNumber(col)

	def _moveToRow(self, row):
		if not row:
			return self._moveToColumn(None)
		nav = api.getNavigatorObject()
		if nav != self and nav.parent == self:
			self.__class__._savedColumnNumber = nav.columnNumber
		row.setFocus()

	def script_moveToNextRow(self, gesture):
		self._moveToRow(self.next)
	script_moveToNextRow.canPropagate = True
	# Translators: The description of an NVDA command.
	script_moveToNextRow.__doc__ = _("Moves the navigator object and focus to the next row")

	def script_moveToPreviousRow(self, gesture):
		self._moveToRow(self.previous)
	script_moveToPreviousRow.canPropagate = True
	# Translators: The description of an NVDA command.
	script_moveToPreviousRow.__doc__ = _("Moves the navigator object and focus to the previous row")

	__gestures = {
		"kb:control+alt+rightArrow": "moveToNextColumn",
		"kb:control+alt+leftArrow": "moveToPreviousColumn",
		"kb:control+alt+downArrow": "moveToNextRow",
		"kb:control+alt+upArrow": "moveToPreviousRow",
	}

class RowWithoutCellObjects(NVDAObject):
	"""An abstract class which creates cell objects for table rows which don't natively expose them.
	Subclasses must override L{_getColumnContent} and can optionally override L{_getColumnHeader}
	to retrieve information about individual columns.
	The parent (table) must support the L{columnCount} property.
	"""

	def _get_childCount(self):
		return self.parent.columnCount

	def _getColumnLocation(self,column):
		"""Get the screen location for the given column.
		Subclasses may optionally  override this method.
		@param column: The index of the column, starting at 1.
		@type column: int
		@rtype: tuple
		"""
		raise NotImplementedError

	def _getColumnContent(self, column):
		"""Get the text content for a given column of this row.
		Subclasses must override this method.
		@param column: The index of the column, starting at 1.
		@type column: int
		@rtype: str
		"""
		raise NotImplementedError

	def _getColumnHeader(self, column):
		"""Get the header text for this column.
		@param column: The index of the column, starting at 1.
		@type column: int
		@rtype: str
		"""
		raise NotImplementedError

	def _makeCell(self, column):
		if column == 0 or column > self.childCount:
			return None
		return _FakeTableCell(parent=self, column=column)

	def _get_firstChild(self):
		return self._makeCell(1)

	def _get_children(self):
		return [self._makeCell(column) for column in xrange(1, self.childCount + 1)]

	def getChild(self, index):
		return self._makeCell(index + 1)

class _FakeTableCell(NVDAObject):

	role = controlTypes.ROLE_TABLECELL

	def __init__(self, parent=None, column=None):
		super(_FakeTableCell, self).__init__()
		self.parent = parent
		self.columnNumber = column
		try:
			self.rowNumber = self.parent.positionInfo["indexInGroup"]
		except KeyError:
			pass
		self.processID = parent.processID
		try:
			# HACK: Some NVDA code depends on window properties, even for non-Window objects.
			self.windowHandle = parent.windowHandle
			self.windowClassName = parent.windowClassName
			self.windowControlID = parent.windowControlID
		except AttributeError:
			pass

	def _get_next(self):
		return self.parent._makeCell(self.columnNumber + 1)

	def _get_previous(self):
		return self.parent._makeCell(self.columnNumber - 1)

	firstChild = None

	def _get_location(self):
		try:
			return self.parent._getColumnLocation(self.columnNumber)
		except NotImplementedError:
			return None

	def _get_name(self):
		return self.parent._getColumnContent(self.columnNumber)

	def _get_columnHeaderText(self):
		return self.parent._getColumnHeader(self.columnNumber)

	def _get_tableID(self):
		return id(self.parent.parent)

	def _get_states(self):
		return self.parent.states

class FocusableUnfocusableContainer(NVDAObject):
	"""Makes an unfocusable container focusable using its first focusable descendant.
	One instance where this is useful is ARIA applications on the web where the author hasn't set a tabIndex.
	"""
	isFocusable = True

	def setFocus(self):
		for obj in self.recursiveDescendants:
			if obj.isFocusable:
				obj.setFocus()
				break

class ToolTip(NVDAObject):
	"""Provides information about an item over which the user is hovering a cursor.
	The object should fire a show event when it appears.
	"""
	role = controlTypes.ROLE_TOOLTIP

	def event_show(self):
		if not config.conf["presentation"]["reportTooltips"]:
			return
		speech.speakObject(self, reason=controlTypes.REASON_FOCUS)
		# Ideally, we wouldn't use getBrailleTextForProperties directly.
		braille.handler.message(braille.getBrailleTextForProperties(name=self.name, role=self.role))

class Notification(NVDAObject):
	"""Informs the user of non-critical information that does not require immediate action.
	This is primarily for notifications displayed in the system notification area.
	The object should fire a alert or show event when the user should be notified.
	"""

	def event_alert(self):
		if not config.conf["presentation"]["reportHelpBalloons"]:
			return
		speech.speakObject(self, reason=controlTypes.REASON_FOCUS)
		# Ideally, we wouldn't use getBrailleTextForProperties directly.
		braille.handler.message(braille.getBrailleTextForProperties(name=self.name, role=self.role))

	event_show = event_alert
