# selectableText.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2006-2019 NV Access Limited, Davy Kager, Babbage B.V.

"""Common support for selectable text."""

from documentBase import TextContainerObject
import braille
import speech
import textInfos
from logHandler import log


class SelectableText(TextContainerObject):
	"""
	An object that contains text in which the selection can be fetched and changed.
	This doesn't necessarily mean that the text is editable.

	If the object notifies of selection changes, the following should be done:
		* When the object gains focus, L{initAutoSelectDetection} must be called.
		* When the object notifies of a possible selection change, L{detectPossibleSelectionChange} must be called.
		* Optionally, if the object notifies of changes to its content,
		L{hasContentChangedSinceLastSelection} should be set to C{True}.
	@ivar hasContentChangedSinceLastSelection: Whether the content has changed
		since the last selection occurred.
	@type hasContentChangedSinceLastSelection: bool
	"""

	#: Whether to speak the unselected content after new content has been selected.
	#: If C{False}, the old selection is ignored,
	#: and the new selection is reported without the redundant selected state.
	speakUnselected: bool = True

	def initAutoSelectDetection(self):
		"""Initialise automatic detection of selection changes.
		This should be called when the object gains focus.
		"""
		try:
			self._lastSelectionPos = self.makeTextInfo(textInfos.POSITION_SELECTION)
		except Exception:
			self._lastSelectionPos = None
		self.isTextSelectionAnchoredAtStart = True
		self.hasContentChangedSinceLastSelection = False

	def reportSelection(
			self,
			oldInfo: textInfos.TextInfo,
			newInfo: textInfos.TextInfo,
			generalize: bool = False
	):
		"""Announces selection changes with speech and updates the braille display accordingly.

		@param oldInfo: a TextInfo instance representing what the selection was before.
		@param newInfo: a TextInfo instance representing what the selection is now.
		@param generalize: if True, then this function knows that the text may have changed
			between the creation of the oldInfo and newInfo objects, meaning that changes need to be spoken
			more generally, rather than speaking the specific text, as the bounds may be all wrong.
		"""
		speech.speakSelectionChange(
			oldInfo,
			newInfo,
			speakUnselected=self.speakUnselected,
			# Do not speak redundant "selected" word if we only speak selected text.
			speakStates=self.speakUnselected,
			generalize=generalize
		)

		# Import late to avoid circular import
		from editableText import EditableText
		if not isinstance(self, EditableText):
			# This object has no caret.
			# Yet, handleUpdate does not scroll the display to the selection when it has to.
			# handleCaretMove is also suitable to cover selection changes.
			braille.handler.handleCaretMove(self)

	def detectPossibleSelectionChange(self):
		"""Detects if the selection has been changed, and if so it speaks the change.
		"""
		try:
			newInfo = self.makeTextInfo(textInfos.POSITION_SELECTION)
		except Exception:
			# Just leave the old selection, which is usually better than nothing.
			# We want to know what happened, though.
			log.debugWarning(
				f"{self!s} assumed new selection, but fetching failed",
				exc_info=True
			)
			return
		oldInfo = getattr(self, '_lastSelectionPos', None)
		self._lastSelectionPos = newInfo.copy()
		if not oldInfo:
			# There's nothing we can do, but at least the last selection will be right next time.
			self.isTextSelectionAnchoredAtStart = True
			log.debug(f"No old textInfo for {self!s} to calculate possible selection change")
			return
		self._updateSelectionAnchor(oldInfo, newInfo)
		hasContentChanged = getattr(self, 'hasContentChangedSinceLastSelection', False)
		self.hasContentChangedSinceLastSelection = False
		self.reportSelectionChange(oldInfo, newInfo, generalize=hasContentChanged)

	def _updateSelectionAnchor(self, oldInfo, newInfo):
		# Only update the value if the selection changed.
		if newInfo.compareEndPoints(oldInfo, "startToStart") != 0:
			self.isTextSelectionAnchoredAtStart = False
		elif newInfo.compareEndPoints(oldInfo, "endToEnd") != 0:
			self.isTextSelectionAnchoredAtStart = True
