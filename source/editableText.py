#editableText.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2017 NV Access Limited, Davy Kager

"""Common support for editable text.
@note: If you want editable text functionality for an NVDAObject,
	you should use the EditableText classes in L{NVDAObjects.behaviors}.
"""

import time
import sayAllHandler
import api
import review
from baseObject import ScriptableObject
from documentBase import TextContainerObject
import braille
import speech
import config
import eventHandler
from scriptHandler import isScriptWaiting, willSayAllResume
import textInfos
import controlTypes
from logHandler import log

class EditableText(TextContainerObject,ScriptableObject):
	"""Provides scripts to report appropriately when moving the caret in editable text fields.
	This does not handle the selection change keys.
	To have selection changes reported, the object must notify of selection changes.
	If the object supports selection but does not notify of selection changes, L{EditableTextWithoutAutoSelectDetection} should be used instead.
	
	If the object notifies of selection changes, the following should be done:
		* When the object gains focus, L{initAutoSelectDetection} must be called.
		* When the object notifies of a possible selection change, L{detectPossibleSelectionChange} must be called.
		* Optionally, if the object notifies of changes to its content, L{hasContentChangedSinceLastSelection} should be set to C{True}.
	@ivar hasContentChangedSinceLastSelection: Whether the content has changed since the last selection occurred.
	@type hasContentChangedSinceLastSelection: bool
	"""

	#: Whether to fire caretMovementFailed events when the caret doesn't move in response to a caret movement key.
	shouldFireCaretMovementFailedEvents = False

	#: Whether or not to announce text found before the caret on a new line (e.g. auto numbering)
	announceNewLineText=True
	#: When announcing new line text: should the entire line be announced, or just text after the caret?
	announceEntireNewLine=False

	_hasCaretMoved_minWordTimeoutMs=30 #: The minimum amount of time that should elapse before checking if the word under the caret has changed

	def _hasCaretMoved(self, bookmark, retryInterval=0.01, timeout=None, origWord=None):
		"""
		Waits for the caret to move, for a timeout to elapse, or for a new focus event or script to be queued.
		@param bookmark: a bookmark representing the position of the caret before  it was instructed to move
		@type bookmark: bookmark
		@param retryInterval: the interval of time in seconds this method should  wait before checking the caret each time.
		@type retryInterval: float 
		@param timeout: the over all amount of time in seconds the method should wait before giving up completely,
			C{None} to use the value from the configuration.
		@type timeout: float
		@param origWord: The word at the caret before the movement command,
			C{None} if the word at the caret should not be used to detect movement.
			This is intended for use with the delete key.
		@return: a tuple containing a boolean denoting whether this method timed out, and  a TextInfo representing the old or updated caret position or None if interupted by a script or focus event.
		@rtype: tuple
		"""
		if timeout is None:
			timeoutMs = config.conf["editableText"]["caretMoveTimeoutMs"]
		else:
			# This function's arguments are in seconds, but we want ms.
			timeoutMs = timeout * 1000
		# time.sleep accepts seconds, so retryInterval is in seconds.
		# Convert to integer ms to avoid floating point precision errors when adding to elapsed.
		retryMs = int(retryInterval * 1000)
		elapsed = 0
		newInfo=None
		while True:
			if isScriptWaiting():
				return (False,None)
			api.processPendingEvents(processEventQueue=False)
			if eventHandler.isPendingEvents("gainFocus"):
				log.debug("Focus event. Elapsed: %d ms" % elapsed)
				return (True,None)
			# If the focus changes after this point, fetching the caret may fail,
			# but we still want to stay in this loop.
			try:
				newInfo = self.makeTextInfo(textInfos.POSITION_CARET)
			except (RuntimeError,NotImplementedError):
				newInfo = None
			# Caret events are unreliable in some controls.
			# Try to detect with bookmarks.
			newBookmark = None
			if newInfo:
				try:
					newBookmark = newInfo.bookmark
				except (RuntimeError,NotImplementedError):
					pass
			if newBookmark and newBookmark!=bookmark:
				log.debug("Caret move detected using bookmarks. Elapsed: %d ms" % elapsed)
				return (True, newInfo)
			if origWord is not None and newInfo and elapsed >= self._hasCaretMoved_minWordTimeoutMs:
				# When pressing delete, bookmarks might not be enough to detect caret movement.
				# Therefore try detecting if the word under the caret has changed, such as when pressing delete.
				# some editors such as Mozilla Gecko can have text and units that get out of sync with eachother while a character is being deleted.
				# Therefore, only check if the word has changed after a particular amount of time has elapsed, allowing the text and units to settle down.
				wordInfo = newInfo.copy()
				wordInfo.expand(textInfos.UNIT_WORD)
				word = wordInfo.text
				if word != origWord:
					log.debug("Word at caret changed. Elapsed: %d ms" % elapsed)
					return (True, newInfo)
			if elapsed >= timeoutMs:
				break
			time.sleep(retryInterval)
			elapsed += retryMs
		log.debug("Caret didn't move before timeout. Elapsed: %d ms" % elapsed)
		return (False,newInfo)

	def _caretScriptPostMovedHelper(self, speakUnit, gesture, info=None):
		if isScriptWaiting():
			return
		if not info:
			try:
				info = self.makeTextInfo(textInfos.POSITION_CARET)
			except:
				return
		review.handleCaretMove(info)
		if speakUnit and not willSayAllResume(gesture):
			info.expand(speakUnit)
			speech.speakTextInfo(info, unit=speakUnit, reason=controlTypes.REASON_CARET)
		braille.handler.handleCaretMove(self)

	def _caretMovementScriptHelper(self, gesture, unit):
		try:
			info=self.makeTextInfo(textInfos.POSITION_CARET)
		except:
			gesture.send()
			return
		bookmark=info.bookmark
		gesture.send()
		caretMoved,newInfo=self._hasCaretMoved(bookmark) 
		if not caretMoved and self.shouldFireCaretMovementFailedEvents:
			eventHandler.executeEvent("caretMovementFailed", self, gesture=gesture)
		self._caretScriptPostMovedHelper(unit,gesture,newInfo)

	def script_caret_newLine(self,gesture):
		# #8065: We want to rely on text info to speak the word
		# that has been typed before pressing enter.
		# Therefore, speak the typed character/word before executing the actual gesture.
		speech.speakTypedCharacters(unichr(gesture.vkCode))
		# speech.speakTypedCharacters will be executed by event_typedCharacter as well.
		# Therefore, suppress speaking of the next typed character
		speech._suppressSpeakTypedCharacters(1)
		try:
			info=self.makeTextInfo(textInfos.POSITION_CARET)
		except:
			gesture.send()
			return
		bookmark=info.bookmark
		gesture.send()
		caretMoved,newInfo=self._hasCaretMoved(bookmark) 
		if not caretMoved or not newInfo:
			return
		# newInfo.copy should be good enough here, but in MS Word we get strange results.
		try:
			lineInfo=self.makeTextInfo(textInfos.POSITION_CARET)
		except (RuntimeError,NotImplementedError):
			return
		lineInfo.expand(textInfos.UNIT_LINE)
		if not self.announceEntireNewLine: 
			lineInfo.setEndPoint(newInfo,"endToStart")
		if lineInfo.isCollapsed:
			lineInfo.expand(textInfos.UNIT_CHARACTER)
			onlyInitial=True
		else:
			onlyInitial=False
		speech.speakTextInfo(lineInfo,unit=textInfos.UNIT_LINE,reason=controlTypes.REASON_CARET,onlyInitialFields=onlyInitial,suppressBlanks=True)

	def _caretMoveBySentenceHelper(self, gesture, direction):
		if isScriptWaiting():
			return
		try:
			info=self.makeTextInfo(textInfos.POSITION_CARET)
			info.move(textInfos.UNIT_SENTENCE, direction)
			info.updateCaret()
			self._caretScriptPostMovedHelper(textInfos.UNIT_SENTENCE,gesture,info)
		except:
			gesture.send()
			return

	def script_caret_moveByLine(self,gesture):
		self._caretMovementScriptHelper(gesture, textInfos.UNIT_LINE)
	script_caret_moveByLine.resumeSayAllMode=sayAllHandler.CURSOR_CARET

	def script_caret_moveByCharacter(self,gesture):
		self._caretMovementScriptHelper(gesture, textInfos.UNIT_CHARACTER)

	def script_caret_moveByWord(self,gesture):
		self._caretMovementScriptHelper(gesture, textInfos.UNIT_WORD)

	def script_caret_moveByParagraph(self,gesture):
		self._caretMovementScriptHelper(gesture, textInfos.UNIT_PARAGRAPH)
	script_caret_moveByParagraph.resumeSayAllMode=sayAllHandler.CURSOR_CARET

	def script_caret_previousSentence(self,gesture):
		self._caretMoveBySentenceHelper(gesture, -1)
	script_caret_previousSentence.resumeSayAllMode=sayAllHandler.CURSOR_CARET

	def script_caret_nextSentence(self,gesture):
		self._caretMoveBySentenceHelper(gesture, 1)
	script_caret_nextSentence.resumeSayAllMode=sayAllHandler.CURSOR_CARET

	def _backspaceScriptHelper(self,unit,gesture):
		try:
			oldInfo=self.makeTextInfo(textInfos.POSITION_CARET)
		except:
			gesture.send()
			return
		oldBookmark=oldInfo.bookmark
		testInfo=oldInfo.copy()
		res=testInfo.move(textInfos.UNIT_CHARACTER,-1)
		if res<0:
			testInfo.expand(unit)
			delChunk=testInfo.text
		else:
			delChunk=""
		gesture.send()
		caretMoved,newInfo=self._hasCaretMoved(oldBookmark)
		if not caretMoved:
			return
		if len(delChunk)>1:
			speech.speakMessage(delChunk)
		else:
			speech.speakSpelling(delChunk)
		self._caretScriptPostMovedHelper(None,gesture,newInfo)

	def script_caret_backspaceCharacter(self,gesture):
		self._backspaceScriptHelper(textInfos.UNIT_CHARACTER,gesture)

	def script_caret_backspaceWord(self,gesture):
		self._backspaceScriptHelper(textInfos.UNIT_WORD,gesture)

	def script_caret_delete(self,gesture):
		try:
			info=self.makeTextInfo(textInfos.POSITION_CARET)
		except:
			gesture.send()
			return
		bookmark=info.bookmark
		info.expand(textInfos.UNIT_WORD)
		word=info.text
		gesture.send()
		# We'll try waiting for the caret to move, but we don't care if it doesn't.
		caretMoved,newInfo=self._hasCaretMoved(bookmark,origWord=word)
		self._caretScriptPostMovedHelper(textInfos.UNIT_CHARACTER,gesture,newInfo)
		braille.handler.handleCaretMove(self)

	__gestures = {
		"kb:upArrow": "caret_moveByLine",
		"kb:downArrow": "caret_moveByLine",
		"kb:leftArrow": "caret_moveByCharacter",
		"kb:rightArrow": "caret_moveByCharacter",
		"kb:pageUp": "caret_moveByLine",
		"kb:pageDown": "caret_moveByLine",
		"kb:control+leftArrow": "caret_moveByWord",
		"kb:control+rightArrow": "caret_moveByWord",
		"kb:control+upArrow": "caret_moveByParagraph",
		"kb:control+downArrow": "caret_moveByParagraph",
		"kb:alt+upArrow": "caret_previousSentence",
		"kb:alt+downArrow": "caret_nextSentence",
		"kb:home": "caret_moveByCharacter",
		"kb:end": "caret_moveByCharacter",
		"kb:control+home": "caret_moveByLine",
		"kb:control+end": "caret_moveByLine",
		"kb:delete": "caret_delete",
		"kb:numpadDelete": "caret_delete",
		"kb:backspace": "caret_backspaceCharacter",
		"kb:control+backspace": "caret_backspaceWord",
	}

	def initAutoSelectDetection(self):
		"""Initialise automatic detection of selection changes.
		This should be called when the object gains focus.
		"""
		try:
			self._lastSelectionPos=self.makeTextInfo(textInfos.POSITION_SELECTION)
		except:
			self._lastSelectionPos=None
		self.isTextSelectionAnchoredAtStart=True
		self.hasContentChangedSinceLastSelection=False

	def detectPossibleSelectionChange(self):
		"""Detects if the selection has been changed, and if so it speaks the change.
		"""
		try:
			newInfo=self.makeTextInfo(textInfos.POSITION_SELECTION)
		except:
			# Just leave the old selection, which is usually better than nothing.
			return
		oldInfo=getattr(self,'_lastSelectionPos',None)
		self._lastSelectionPos=newInfo.copy()
		if not oldInfo:
			# There's nothing we can do, but at least the last selection will be right next time.
			self.isTextSelectionAnchoredAtStart=True
			return
		self._updateSelectionAnchor(oldInfo,newInfo)
		hasContentChanged=getattr(self,'hasContentChangedSinceLastSelection',False)
		self.hasContentChangedSinceLastSelection=False
		speech.speakSelectionChange(oldInfo,newInfo,generalize=hasContentChanged)

	def _updateSelectionAnchor(self,oldInfo,newInfo):
		# Only update the value if the selection changed.
		if newInfo.compareEndPoints(oldInfo,"startToStart")!=0:
			self.isTextSelectionAnchoredAtStart=False
		elif newInfo.compareEndPoints(oldInfo,"endToEnd")!=0:
			self.isTextSelectionAnchoredAtStart=True

class EditableTextWithoutAutoSelectDetection(EditableText):
	"""In addition to L{EditableText}, provides scripts to report appropriately when the selection changes.
	This should be used when an object does not notify of selection changes.
	"""

	def reportSelectionChange(self, oldTextInfo):
		api.processPendingEvents(processEventQueue=False)
		newInfo=self.makeTextInfo(textInfos.POSITION_SELECTION)
		self._updateSelectionAnchor(oldTextInfo,newInfo)
		speech.speakSelectionChange(oldTextInfo,newInfo)
		braille.handler.handleCaretMove(self)

	def script_caret_changeSelection(self,gesture):
		try:
			oldInfo=self.makeTextInfo(textInfos.POSITION_SELECTION)
		except:
			gesture.send()
			return
		gesture.send()
		if isScriptWaiting() or eventHandler.isPendingEvents("gainFocus"):
			return
		try:
			self.reportSelectionChange(oldInfo)
		except:
			return

	__changeSelectionGestures = (
		"kb:shift+upArrow",
		"kb:shift+downArrow",
		"kb:shift+leftArrow",
		"kb:shift+rightArrow",
		"kb:shift+pageUp",
		"kb:shift+pageDown",
		"kb:shift+control+leftArrow",
		"kb:shift+control+rightArrow",
		"kb:shift+control+upArrow",
		"kb:shift+control+downArrow",
		"kb:shift+home",
		"kb:shift+end",
		"kb:shift+control+home",
		"kb:shift+control+end",
		"kb:control+a",
	)

	def initClass(self):
		for gesture in self.__changeSelectionGestures:
			self.bindGesture(gesture, "caret_changeSelection")
