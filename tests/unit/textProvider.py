#tests/unit/textProvider.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017-2019 NV Access Limited

"""Fake text provider implementation for testing of code which uses TextInfos.
See the L{BasicTextProvider} class.
"""

from NVDAObjects import NVDAObject, NVDAObjectTextInfo
import textInfos
from textInfos.offsets import Offsets
import textUtils

class BasicTextInfo(NVDAObjectTextInfo):
	# NVDAHelper is not initialized, so we can't use Uniscribe.
	useUniscribe = False
	# Most of our code use UTF-16 as internal encoding.
	# Mimic this behavior, so we can also implicitly test textUtils module code
	encoding = textUtils.WCHAR_ENCODING

	def _getStoryLength(self):
		# NVDAObjectTextInfo will just return the str length of the story text,.
		# As we are using UTF-16 as the internal encoding for this TextInfo, this is incorrect.
		return textUtils.WideStringOffsetConverter(self._getStoryText()).wideStringLength

	def _get_offsets(self):
		return (self._startOffset, self._endOffset)

	def updateCaret(self):
		self.obj.selectionOffsets = (self._startOffset, self._startOffset)

	def updateSelection(self):
		self.obj.selectionOffsets = self.offsets

class BasicTextProvider(NVDAObject):
	"""An NVDAObject which makes TextInfos based on a provided string of text.
	Example usage:
	>>> obj = BasicTextProvider(text="abcd")
	>>> ti = obj.makeTextInfo(textInfos.POSITION_CARET)
	>>> ti.offsets
	(0, 0)
	>>> ti.expand(textInfos.UNIT_CHARACTER)
	>>> ti.text
	"a"
	>>> ti.offsets
	(0, 1)
	>>> ti.updateSelection()
	>>> obj.selectionOffsets
	(0, 1)
	"""

	processID = None # Must be implemented to instantiate.
	TextInfo = BasicTextInfo

	def __init__(self, text=None, selection=(0, 0)):
		"""
		@param text: The text to provide via TextInfos.
		@type text: str
		@param selection: The start and end offsets of the initial selection;
			same start and end is caret with no selection.
		@type selection: tuple of (int, int)
		"""
		super(BasicTextProvider, self).__init__()
		self.basicText = text
		self.selectionOffsets = selection

	def makeTextInfo(self, position):
		if position in (textInfos.POSITION_CARET, textInfos.POSITION_SELECTION):
			start, end = self.selectionOffsets
			position = Offsets(start, end)
		return super(BasicTextProvider, self).makeTextInfo(position)
