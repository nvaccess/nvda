#editableText.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2010 Michael Curran <mick@kulgan.net>, James Teh <jamie@jantrid.net>

"""Common support for editable text.
"""

import time
import api
from baseObject import ScriptableObject
import speech
import config
import eventHandler
from scriptHandler import isScriptWaiting
import textInfos

class EditableText(ScriptableObject):
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

	def _hasCaretMoved(self, bookmark, retryInterval=0.01, timeout=0.03):
		elapsed = 0
		while elapsed < timeout:
			if isScriptWaiting():
				return False
			api.processPendingEvents(processEventQueue=False)
			if eventHandler.isPendingEvents("gainFocus"):
				return True
			#The caret may stop working as the focus jumps, we want to stay in the while loop though
			try:
				newBookmark = self.makeTextInfo(textInfos.POSITION_CARET).bookmark
			except (RuntimeError,NotImplementedError):
				pass
			else:
				if newBookmark!=bookmark:
					return True
			time.sleep(retryInterval)
			elapsed += retryInterval
		return False

	def _caretScriptPostMovedHelper(self, speakUnit):
		if isScriptWaiting():
			return
		try:
			info = self.makeTextInfo(textInfos.POSITION_CARET)
		except:
			return
		if config.conf["reviewCursor"]["followCaret"]:
			api.setReviewPosition(info.copy())
		if speakUnit:
			info.expand(speakUnit)
			speech.speakTextInfo(info, unit=speakUnit, reason=speech.REASON_CARET)

	def _caretMovementScriptHelper(self, gesture, unit):
		try:
			info=self.makeTextInfo(textInfos.POSITION_CARET)
		except:
			gesture.send()
			return
		bookmark=info.bookmark
		gesture.send()
		if not self._hasCaretMoved(bookmark) and self.shouldFireCaretMovementFailedEvents:
			eventHandler.executeEvent("caretMovementFailed", self, gesture=gesture)
		self._caretScriptPostMovedHelper(unit)

	def script_caret_moveByLine(self,gesture):
		self._caretMovementScriptHelper(gesture, textInfos.UNIT_LINE)

	def script_caret_moveByCharacter(self,gesture):
		self._caretMovementScriptHelper(gesture, textInfos.UNIT_CHARACTER)

	def script_caret_moveByWord(self,gesture):
		self._caretMovementScriptHelper(gesture, textInfos.UNIT_WORD)

	def script_caret_moveByParagraph(self,gesture):
		self._caretMovementScriptHelper(gesture, textInfos.UNIT_PARAGRAPH)

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
		if not self._hasCaretMoved(oldBookmark):
			return
		if len(delChunk)>1:
			speech.speakMessage(delChunk)
		else:
			speech.speakSpelling(delChunk)
		self._caretScriptPostMovedHelper(None)

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
		gesture.send()
		# We'll try waiting for the caret to move, but we don't care if it doesn't.
		self._hasCaretMoved(bookmark)
		self._caretScriptPostMovedHelper(textInfos.UNIT_CHARACTER)

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
		"kb:home": "caret_moveByCharacter",
		"kb:end": "caret_moveByCharacter",
		"kb:control+home": "caret_moveByLine",
		"kb:control+end": "caret_moveByLine",
		"kb:delete": "caret_delete",
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
			return
		hasContentChanged=getattr(self,'hasContentChangedSinceLastSelection',False)
		self.hasContentChangedSinceLastSelection=False
		speech.speakSelectionChange(oldInfo,newInfo,generalize=hasContentChanged)

class EditableTextWithoutAutoSelectDetection(EditableText):
	"""In addition to L{EditableText}, provides scripts to report appropriately when the selection changes.
	This should be used when an object does not notify of selection changes.
	"""

	def script_caret_changeSelection(self,gesture):
		try:
			oldInfo=self.makeTextInfo(textInfos.POSITION_SELECTION)
		except:
			gesture.send()
			return
		gesture.send()
		if isScriptWaiting() or eventHandler.isPendingEvents("gainFocus"):
			return
		api.processPendingEvents(processEventQueue=False)
		try:
			newInfo=self.makeTextInfo(textInfos.POSITION_SELECTION)
		except:
			return
		speech.speakSelectionChange(oldInfo,newInfo)

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
