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
import controlTypes

class SelectableText(TextContainerObject):
	"""
	An object that contains text in which the selection can be fetched and changed.
	This doesn't necessarily mean that the text is editable.

	If the object notifies of selection changes, the following should be done:
		* When the object gains focus, L{initAutoSelectDetection} must be called.
		* When the object notifies of a possible selection change, L{detectPossibleSelectionChange} must be called.
		* Optionally, if the object notifies of changes to its content, L{hasContentChangedSinceLastSelection} should be set to C{True}.
	@ivar hasContentChangedSinceLastSelection: Whether the content has changed since the last selection occurred.
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

	def detectPossibleSelectionChange(self):
		"""Detects if the selection has been changed, and if so it speaks the change.
		"""
		try:
			newInfo = self.makeTextInfo(textInfos.POSITION_SELECTION)
		except Exception:
			# Just leave the old selection, which is usually better than nothing.
			return
		oldInfo = getattr(self, '_lastSelectionPos', None)
		self._lastSelectionPos = newInfo.copy()
		if not oldInfo:
			# There's nothing we can do, but at least the last selection will be right next time.
			self.isTextSelectionAnchoredAtStart = True
			return
		self._updateSelectionAnchor(oldInfo,newInfo)
		hasContentChanged = getattr(self, 'hasContentChangedSinceLastSelection', False)
		self.hasContentChangedSinceLastSelection = False
		if not self.speakUnselected:
			# As the unselected state is not relevant here and all spoken content is selected,
			# use speech.speakTextInfo to make sure the new selection is spoken.
			speech.speakTextInfo(newInfo,reason=controlTypes.REASON_CARET)
		else:
			speech.speakSelectionChange(oldInfo,newInfo,generalize=hasContentChanged)

		# Import late to avoid circular import
		from editableText import EditableText
		if not isinstance(self, EditableText):
			# This object has no caret, manually trigger a braille update.
			braille.handler.handleUpdate(self)

	def _updateSelectionAnchor(self, oldInfo, newInfo):
		# Only update the value if the selection changed.
		if newInfo.compareEndPoints(oldInfo, "startToStart") != 0:
			self.isTextSelectionAnchoredAtStart = False
		elif newInfo.compareEndPoints(oldInfo, "endToEnd") != 0:
			self.isTextSelectionAnchoredAtStart = True
