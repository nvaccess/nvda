from typing import List, Callable

from braille import BrailleDisplayDriver
from .brailleViewerGui import BrailleViewerFrame

BRAILLE_UNICODE_PATTERNS_START = 0x2800
SPACE_CHARACTER = u" "


class BrailleViewerDriver(BrailleDisplayDriver):
	name = "brailleViewer"
	# Translators: Description of the braille viewer tool
	description: str = _("Braille viewer")
	numCells: int  # Overridden to match an active braille display
	_brailleGui = None  # A BrailleViewer instance

	@classmethod
	def check(cls):
		return True

	def __init__(
			self,
			numCells: int,
			onUpdated: Callable[[str, str], None]
	):
		super(BrailleViewerDriver, self).__init__()
		self.numCells = numCells
		self._hasTerminated = False
		self._updateValues: Callable[[str, str], None] = onUpdated

	def display(
			self,
			cells: List[int],
			rawText: str = u""
	):
		if self._hasTerminated:
			return
		brailleUnicodeChars = (chr(BRAILLE_UNICODE_PATTERNS_START + cell) for cell in cells)
		# replace braille "space" with regular space because the width of the braille space
		# does not match the other braille characters, the result is better, but not perfect.
		brailleSpace = chr(BRAILLE_UNICODE_PATTERNS_START)
		spaceReplaced = (
			cell.replace(brailleSpace, SPACE_CHARACTER)
			for cell in brailleUnicodeChars
		)
		self._updateValues(u"".join(spaceReplaced), rawText)

	def saveSettings(self):
		# prevent base class driverHandler.saveSettings from running
		pass

	def onBrailleGuiDestroyed(self):
		self._hasTerminated = True
		# Todo: should this call super.Terminate()?