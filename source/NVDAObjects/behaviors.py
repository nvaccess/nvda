# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2006-2020 NV Access Limited, Peter Vágner, Joseph Lee, Bill Dengler

"""Mix-in classes which provide common behaviour for particular types of controls across different APIs.
Behaviors described in this mix-in include providing table navigation commands for certain table rows, terminal input and output support, announcing notifications and suggestion items and so on.
"""

import os
import time
import threading
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
from scriptHandler import script
import api
import ui
import braille
import core
import nvwave
import globalVars
from typing import List, Union
import diffHandler


class ProgressBar(NVDAObject):

	progressValueCache={} #key is made of "speech" or "beep" and an x,y coordinate, value is the last percentage

	def event_valueChange(self):
		pbConf=config.conf["presentation"]["progressBarUpdates"]
		states=self.states
		if pbConf["progressBarOutputMode"]=="off" or controlTypes.State.INVISIBLE in states or controlTypes.State.OFFSCREEN in states:
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
		x = left + (width // 2)
		y = top+ (height // 2)
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
		for index in range(childCount):
			child=children[index]
			childStates=child.states
			childRole=child.role
			#We don't want to handle invisible or unavailable objects
			if controlTypes.State.INVISIBLE in childStates or controlTypes.State.UNAVAILABLE in childStates: 
				continue
			#For particular objects, we want to descend in to them and get their children's message text
			if childRole in (
				controlTypes.Role.OPTIONPANE,
				controlTypes.Role.PROPERTYPAGE,
				controlTypes.Role.PANE,
				controlTypes.Role.PANEL,
				controlTypes.Role.WINDOW,
				controlTypes.Role.GROUPING,
				controlTypes.Role.PARAGRAPH,
				controlTypes.Role.SECTION,
				controlTypes.Role.TEXTFRAME,
				controlTypes.Role.UNKNOWN
			):
				#Grab text from descendants, but not for a child which inherits from Dialog and has focusable descendants
				#Stops double reporting when focus is in a property page in a dialog
				childText=cls.getDialogText(child,not isinstance(child,Dialog))
				if childText:
					textList.append(childText)
				elif childText is None:
					return None
				continue
			#If the child is focused  we should just stop and return None
			if not allowFocusedDescendants and controlTypes.State.FOCUSED in child.states:
				return None
			# We only want text from certain controls.
			if not (
				 # Static text, labels and links
				 childRole in (controlTypes.Role.STATICTEXT,controlTypes.Role.LABEL,controlTypes.Role.LINK)
				# Read-only, non-multiline edit fields
				or (childRole==controlTypes.Role.EDITABLETEXT and controlTypes.State.READONLY in childStates and controlTypes.State.MULTILINE not in childStates)
			):
				continue
			#We should ignore a text object directly after a grouping object, as it's probably the grouping's description
			if index>0 and children[index-1].role==controlTypes.Role.GROUPING:
				continue
			#Like the last one, but a graphic might be before the grouping's description
			if index>1 and children[index-1].role==controlTypes.Role.GRAPHIC and children[index-2].role==controlTypes.Role.GROUPING:
				continue
			childName=child.name
			if childName and index<(childCount-1) and children[index+1].role not in (controlTypes.Role.GRAPHIC,controlTypes.Role.STATICTEXT,controlTypes.Role.SEPARATOR,controlTypes.Role.WINDOW,controlTypes.Role.PANE,controlTypes.Role.BUTTON) and children[index+1].name==childName:
				# This is almost certainly the label for the next object, so skip it.
				continue
			isNameIncluded=child.TextInfo is NVDAObjectTextInfo or childRole in (controlTypes.Role.LABEL,controlTypes.Role.STATICTEXT)
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
			self.bindGesture("kb:numpadEnter","caret_newLine")

	def _caretScriptPostMovedHelper(self, speakUnit, gesture, info=None):
		if eventHandler.isPendingEvents("gainFocus"):
			return
		super()._caretScriptPostMovedHelper(speakUnit, gesture, info)

	def _reportErrorInPreviousWord(self):
		try:
			# self might be a descendant of the text control; e.g. Symphony.
			# We want to deal with the entire text, so use the caret object.
			info = api.getCaretObject().makeTextInfo(textInfos.POSITION_CARET)
			# This gets called for characters which might end a word; e.g. space.
			# The character before the caret is the word end.
			# The one before that is the last of the word, which is what we want.
			info.move(textInfos.UNIT_CHARACTER, -2)
			info.expand(textInfos.UNIT_CHARACTER)
		except Exception:
			# Focus probably moved.
			log.debugWarning("Error fetching last character of previous word", exc_info=True)
			return

		# Fetch the formatting for the last word to see if it is marked as a spelling error,
		# However perform the fetch and check in a future core cycle
		# To give the content control more time to detect and mark the error itself.
		# #12161: MS Word's UIA implementation certainly requires this delay.
		def _delayedDetection():
			try:
				fields = info.getTextWithFields()
			except Exception:
				log.debugWarning("Error fetching formatting for last character of previous word", exc_info=True)
				return
			for command in fields:
				if (
					isinstance(command, textInfos.FieldCommand)
					and command.command == "formatChange"
					and command.field.get("invalid-spelling")
				):
					break
			else:
				# No error.
				return
			nvwave.playWaveFile(os.path.join(globalVars.appDir, "waves", "textError.wav"))
		core.callLater(50, _delayedDetection)

	def event_typedCharacter(self, ch: str):
		if(
			config.conf["documentFormatting"]["reportSpellingErrors"]
			and config.conf["keyboard"]["alertForSpellingErrors"]
			and (
				# Not alpha, apostrophe or control.
				ch.isspace() or (ch >= " " and ch not in "'\x7f" and not ch.isalpha())
			)
		):
			# Reporting of spelling errors is enabled and this character ends a word.
			self._reportErrorInPreviousWord()
		super().event_typedCharacter(ch)


class EditableTextWithAutoSelectDetection(EditableText):
	"""In addition to L{EditableText}, handles reporting of selection changes for objects which notify of them.
	To have selection changes reported, the object must notify of selection changes via the caret event.
	Optionally, it may notify of changes to content via the textChange, textInsert and textRemove events.
	If the object supports selection but does not notify of selection changes, L{EditableTextWithoutAutoSelectDetection} should be used instead.
	"""

	def event_gainFocus(self):
		super().event_gainFocus()
		self.initAutoSelectDetection()

	def event_loseFocus(self):
		self.terminateAutoSelectDetection()
		super().event_loseFocus()

	def event_caret(self):
		super(EditableText, self).event_caret()
		if self is api.getFocusObject() and not eventHandler.isPendingEvents('gainFocus'):
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
		thread = self._monitorThread = threading.Thread(
			name=f"{self.__class__.__qualname__}._monitorThread",
			target=self._monitor
		)
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

	def _get_diffAlgo(self) -> Union[diffHandler.prefer_difflib, diffHandler.prefer_dmp]:
		"""
			This property controls which diffing algorithm should be used by
			this object. If the object contains a strictly contiguous
			span of text (i.e. textInfos.POSITION_ALL refers to the entire
			contents of the object and not just one visible screen of text),
			then diffHandler.prefer_dmp (character-based diffing) is suitable.
			Otherwise, use diffHandler.prefer_difflib.
			
			@Note: Return either diffHandler.prefer_dmp() or
			diffHandler.prefer_difflib() so that the diffAlgo user
			preference can override this choice.
		"""
		return diffHandler.prefer_dmp()

	def _get_devInfo(self):
		info = super().devInfo
		info.append(f"diffing algorithm: {self.diffAlgo}")
		return info

	def _getText(self) -> str:
		"""Retrieve the text of this object.
		This will be used to determine the new text to speak.
		The base implementation uses the L{TextInfo}.
		However, subclasses should override this if there is a better way to retrieve the text.
		"""
		ti = self.makeTextInfo(textInfos.POSITION_ALL)
		return self.diffAlgo._getText(ti)

	def _reportNewLines(self, lines):
		"""
		Reports new lines of text using _reportNewText for each new line.
		Subclasses may override this method to provide custom filtering of new text,
		where logic depends on multiple lines.
		"""
		for line in lines:
			self._reportNewText(line)

	def _reportNewText(self, line):
		"""Report a line of new text.
		"""
		speech.speakText(line)

	def _monitor(self):
		try:
			oldText = self._getText()
		except:
			log.exception("Error getting initial text")
			oldText = ""

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
				newText = self._getText()
				if config.conf["presentation"]["reportDynamicContentChanges"]:
					outLines = self._calculateNewText(newText, oldText)
					if len(outLines) == 1 and len(outLines[0].strip()) == 1:
						# This is only a single character,
						# which probably means it is just a typed character,
						# so ignore it.
						del outLines[0]
					if outLines:
						queueHandler.queueFunction(queueHandler.eventQueue, self._reportNewLines, outLines)
				oldText = newText
			except:
				log.exception("Error getting or calculating new text")

	def _calculateNewText(self, newText: str, oldText: str) -> List[str]:
		return self.diffAlgo.diff(newText, oldText)


class Terminal(LiveText, EditableText):
	"""An object which both accepts text input and outputs text which should be reported automatically.
	This is an L{EditableText} object,
	as well as a L{liveText} object for which monitoring is automatically enabled and disabled based on whether it has focus.
	"""
	role = controlTypes.Role.TERMINAL

	def event_gainFocus(self):
		super(Terminal, self).event_gainFocus()
		self.startMonitoring()

	def event_loseFocus(self):
		super(Terminal, self).event_loseFocus()
		self.stopMonitoring()

	def _get_caretMovementDetectionUsesEvents(self):
		"""Using caret events in consoles sometimes causes the last character of the
		prompt to be read when quickly deleting text."""
		return False


class EnhancedTermTypedCharSupport(Terminal):
	"""A Terminal object with keyboard support enhancements for console applications.
	Notably, it suppresses duplicate typed character announcements and can
	hold typed characters in a queue and only dispatch once the screen updates.
	This is useful for suppression of passwords, etc."""
	#: Whether this object quickly and reliably sends textChange events
	#: when its contents update.
	#: Timely and reliable textChange events are required
	#: to support password suppression.
	_supportsTextChange = True
	#: A queue of typed characters, to be dispatched on C{textChange}.
	#: This queue allows NVDA to suppress typed passwords when needed.
	_queuedChars = []
	#: Whether the last typed character is a tab.
	#: If so, we should temporarily disable filtering as completions may
	#: be short.
	_hasTab = False

	def _reportNewLines(self, lines):
		# Perform typed character filtering, as typed characters are handled with events.
		if (
			len(lines) == 1
			and not self._hasTab
			and len(lines[0].strip()) < max(len(speech.speech._curWordChars) + 1, 3)
		):
			return
		# Clear the typed word buffer for new text lines.
		speech.clearTypedWordBuffer()
		self._queuedChars = []
		super()._reportNewLines(lines)

	def event_typedCharacter(self, ch):
		if ch == '\t':
			self._hasTab = True
			# Clear the typed word buffer for tab completion.
			speech.clearTypedWordBuffer()
		else:
			self._hasTab = False
		if (
			(
				config.conf['keyboard']['speakTypedCharacters']
				or config.conf['keyboard']['speakTypedWords']
			)
			and not config.conf['terminals']['speakPasswords']
			and self._supportsTextChange
		):
			self._queuedChars.append(ch)
		else:
			super().event_typedCharacter(ch)

	def event_textChange(self):
		self._dispatchQueue()
		super().event_textChange()

	@script(gestures=[
		"kb:enter",
		"kb:numpadEnter",
		"kb:tab",
		"kb:control+c",
		"kb:control+d",
		"kb:control+pause"
	])
	def script_flush_queuedChars(self, gesture):
		"""
		Flushes the typed word buffer and queue of typedCharacter events if present.
		Since these gestures clear the current word/line, we should flush the
		queue to avoid erroneously reporting these chars.
		"""
		self._queuedChars = []
		speech.clearTypedWordBuffer()
		gesture.send()


	def _dispatchQueue(self):
		"""Sends queued typedCharacter events through to NVDA."""
		while self._queuedChars:
			ch = self._queuedChars.pop(0)
			super().event_typedCharacter(ch)


class KeyboardHandlerBasedTypedCharSupport(EnhancedTermTypedCharSupport):
	"""An EnhancedTermTypedCharSupport object that provides typed character support for
	console applications via keyboardHandler events.
	These events are queued from NVDA's global keyboard hook.
	Therefore, an event is fired for every single character that is being typed,
	even when a character is not written to the console (e.g. in read only console applications).
	This approach is an alternative to monitoring the console output for
	characters close to the caret, or injecting in-process with NVDAHelper.
	This class does not implement any specific functionality by itself.
	Rather, it instructs keyboardHandler to use the toUnicodeEx Windows function, in particular
	the flag to preserve keyboard state available in Windows 10 1607
	and later."""
	pass


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
		while isinstance(obj,CandidateItem) and isinstance(obj.candidateNumber,int) and controlTypes.State.INVISIBLE not in obj.states:
			textList.append(obj.name)
			obj=obj.previous
		textList.reverse()
		obj=self.next
		while isinstance(obj,CandidateItem) and isinstance(obj.candidateNumber,int) and controlTypes.State.INVISIBLE not in obj.states:
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
			ui.message(_("Edge of table"))
			return
		if obj is not self:
			# Use the focused copy of the row as the parent for all cells to make comparison faster.
			obj.parent = self
		api.setNavigatorObject(obj)
		speech.speakObject(obj, reason=controlTypes.OutputReason.FOCUS)

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
			self._moveToColumn(self)
			return
		else:
			new = cur.next
		while new and new.location and new.location.width == 0:
			new = new.next
		self._moveToColumn(new)
	script_moveToNextColumn.canPropagate = True
	# Translators: The description of an NVDA command.
	script_moveToNextColumn.__doc__ = _("Moves the navigator object to the next column")

	def script_moveToPreviousColumn(self, gesture):
		cur = api.getNavigatorObject()
		if cur == self:
			new = None
		elif cur.parent != self or not cur.previous:
			new = self
		else:
			new = cur.previous
			while new and new.location and new.location.width == 0:
				new = new.previous
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

	@script(
		description=_(
			# Translators: The description of an NVDA command.
			"Moves the navigator object to the first column"
		),
		gesture="kb:Control+Alt+Home",
		canPropagate=True,
	)
	def script_moveToFirstColumn(self, gesture):
		new = self.firstChild
		while new and new.location and new.location.width == 0:
			new = new.next
		self._moveToColumn(new)

	@script(
		description=_(
			# Translators: The description of an NVDA command.
			"Moves the navigator object to the last column"
		),
		gesture="kb:Control+Alt+End",
		canPropagate=True,
	)
	def script_moveToLastColumn(self, gesture):
		new = self.lastChild
		# In some cases, e.g. in NVDA symbol pronounciation llist view lastChild returns none.
		if not new and len(self.children) > 0:
			new = self.children[-1]
		while new and new.location and new.location.width == 0:
			new = new.previous
		self._moveToColumn(new)

	@script(
		description=_(
			# Translators: The description of an NVDA command.
			"Moves the navigator object to the first row"
		),
		gesture="kb:Control+Alt+PageUp",
		canPropagate=True,
	)
	def script_moveToFirstRow(self, gesture):
		self._moveToRow(self.parent.firstChild)

	@script(
		description=_(
			# Translators: The description of an NVDA command.
			"Moves the navigator object to the last row"
		),
		gesture="kb:Control+Alt+PageDown",
		canPropagate=True,
	)
	def script_moveToLastRow(self, gesture):
		self._moveToRow(self.parent.lastChild)

	__gestures = {
		"kb:control+alt+rightArrow": "moveToNextColumn",
		"kb:control+alt+leftArrow": "moveToPreviousColumn",
		"kb:control+alt+downArrow": "moveToNextRow",
		"kb:control+alt+upArrow": "moveToPreviousRow",
	}

class RowWithoutCellObjects(NVDAObject):
	"""An abstract class which creates cell objects for table rows which don't natively expose them.
	Subclasses must override L{_getColumnContent} and can optionally override L{_getColumnHeader}
	to retrieve information about individual columns and L{_getColumnLocation} to support mouse or
	magnification tracking or highlighting.
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
		return [self._makeCell(column) for column in range(1, self.childCount + 1)]

	def getChild(self, index):
		return self._makeCell(index + 1)

class _FakeTableCell(NVDAObject):

	role = controlTypes.Role.TABLECELL

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
		states = self.parent.states.copy()
		if self.location and self.location.width == 0:
			states.add(controlTypes.State.INVISIBLE)
		states.discard(controlTypes.State.CHECKED)
		return states


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
	role = controlTypes.Role.TOOLTIP

	def event_show(self):
		if not config.conf["presentation"]["reportTooltips"]:
			return
		speech.speakObject(self, reason=controlTypes.OutputReason.FOCUS)
		# Ideally, we wouldn't use getPropertiesBraille directly.
		braille.handler.message(braille.getPropertiesBraille(name=self.name, role=self.role))

class Notification(NVDAObject):
	"""Informs the user of non-critical information that does not require immediate action.
	This is primarily for notifications displayed in the system notification area, and for Windows 8 and later, toasts.
	The object should fire a alert or show event when the user should be notified.
	"""

	def event_alert(self):
		if not config.conf["presentation"]["reportHelpBalloons"]:
			return
		speech.speakObject(self, reason=controlTypes.OutputReason.FOCUS)
		# Ideally, we wouldn't use getPropertiesBraille directly.
		braille.handler.message(braille.getPropertiesBraille(name=self.name, role=self.role))

	event_show = event_alert

class EditableTextWithSuggestions(NVDAObject):
	"""Allows NvDA to announce appearance/disappearance of suggestions as text is entered.
	This is used in various places, including Windows 10 search edit fields and others.
	Subclasses should provide L{event_suggestionsOpened} and can optionally override L{event_suggestionsClosed}.
	These events are fired when suggestions appear and disappear, respectively.
	"""

	def event_suggestionsOpened(self):
		"""Called when suggestions appear when text is entered e.g. search suggestions.
		Subclasses should provide custom implementations if possible.
		By default NVDA will announce appearance of suggestions using speech, braille or a sound will be played.
		"""
		# Translators: Announced in braille when suggestions appear when search term is entered in various search fields such as Start search box in Windows 10.
		braille.handler.message(_("Suggestions"))
		if config.conf["presentation"]["reportAutoSuggestionsWithSound"]:
			nvwave.playWaveFile(os.path.join(globalVars.appDir, "waves", "suggestionsOpened.wav"))

	def event_suggestionsClosed(self):
		"""Called when suggestions list or container is closed.
		Subclasses should provide custom implementations if possible.
		By default NVDA will announce this via speech, braille or via a sound.
		"""
		if config.conf["presentation"]["reportAutoSuggestionsWithSound"]:
			nvwave.playWaveFile(os.path.join(globalVars.appDir, "waves", "suggestionsClosed.wav"))

class WebDialog(NVDAObject):
	"""
	A dialog that will use a treeInterceptor if its parent currently does.
	This  can be used to ensure that dialogs on the web get browseMode by default, unless inside an ARIA application
	"""

	def _get_shouldCreateTreeInterceptor(self):
		if self.parent.treeInterceptor:
			return True
		return False
