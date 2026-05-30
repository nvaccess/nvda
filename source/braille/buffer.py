# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2008-2026 NV Access Limited, Joseph Lee, Babbage B.V., Davy Kager, Bram Duvigneau,
# Leonard de Ruijter, Burman's Computer and Education Ltd., Julien Cochuyt

from __future__ import annotations

import dataclasses
from typing import (
	TYPE_CHECKING,
	Generator,
	List,
	NamedTuple,
	Optional,
)

import textUtils
import textUtils.hyphenation
import baseObject
import config
from config.featureFlagEnums import (
	BrailleTextWrapFlag,
)
from logHandler import log
import api
from utils.security import objectBelowLockScreenAndWindowsIsLocked

if TYPE_CHECKING:
	from NVDAObjects import NVDAObject
	from . import BrailleHandler

from .labels import (
	TEXT_SEPARATOR,
	CONTINUATION_SHAPE,
	CONTEXTPRES_CHANGEDCONTEXT,
	CONTEXTPRES_SCROLL,
)
from .regions import (
	Region,
	RegionWithPositions,
	NVDAObjectRegion,
	NVDAObjectHasUsefulText,
	TextInfoRegion,
	CursorManagerRegion,
	ReviewCursorManagerRegion,
	ReviewNVDAObjectRegion,
	ReviewTextInfoRegion,
	rindex,
	getParagraphStartMarker,
)


@dataclasses.dataclass(frozen=True)
class _WindowRowPositions:
	"""Braille buffer positions for a single row of the braille window."""

	start: int
	"""Start position (inclusive) in the braille buffer."""
	end: int
	"""End position (exclusive) in the braille buffer."""
	showContinuationMark: bool = False
	"""Whether to append a continuation mark (`CONTINUATION_SHAPE`) after the row cells."""


class BrailleBuffer(baseObject.AutoPropertyObject):
	handler: "BrailleHandler"
	regions: list[Region]
	"""The regions in this buffer."""

	def __init__(self, handler):
		self.handler = handler
		self.regions = []
		#: The raw text of the entire buffer.
		self.rawText = ""
		#: The position of the cursor in L{brailleCells}, C{None} if no region contains the cursor.
		#: @type: int
		self.cursorPos = None
		#: The translated braille representation of the entire buffer.
		#: @type: [int, ...]
		self.brailleCells = []
		self._windowRowBufferOffsets: list[_WindowRowPositions] = [_WindowRowPositions(0, 0)]
		"""
		A list representing the rows in the braille window,
		each item containing start and end braille buffer offsets and whether a continuation mark should appear.
		Splitting the window into independent rows allows for optional avoidance of splitting words across rows.
		"""

	def clear(self):
		"""Clear the entire buffer.
		This removes all regions and resets the window position to 0.
		"""
		self.regions = []
		self.rawText = ""
		self.cursorPos = None
		self.brailleCursorPos = None
		self.brailleCells = []
		self.windowStartPos = 0

	def _get_visibleRegions(self):
		if not self.regions:
			return
		if self.regions[-1].hidePreviousRegions:
			yield self.regions[-1]
			return
		for region in self.regions:
			yield region

	def _get_regionsWithPositions(self):
		start = 0
		for region in self.visibleRegions:
			end = start + len(region.brailleCells)
			yield RegionWithPositions(region, start, end)
			start = end

	rawToBraillePos: list[int]
	"""Type definition for auto prop '_get_rawToBraillePos'"""

	def _get_rawToBraillePos(self) -> list[int]:
		""":return: a list mapping positions in L{rawText} to positions in L{brailleCells} for the entire buffer."""
		rawToBraillePos = []
		for region, regionStart, regionEnd in self.regionsWithPositions:
			rawToBraillePos.extend(p + regionStart for p in region.rawToBraillePos)
		return rawToBraillePos

	brailleToRawPos: list[int]
	"""Type definition for auto prop '_get_brailleToRawPos'"""

	def _get_brailleToRawPos(self) -> list[int]:
		""":return: a list mapping positions in L{brailleCells} to positions in L{rawText} for the entire buffer."""
		brailleToRawPos = []
		start = 0
		for region in self.visibleRegions:
			brailleToRawPos.extend(p + start for p in region.brailleToRawPos)
			start += len(region.rawText)
		return brailleToRawPos

	def bufferPosToRegionPos(self, bufferPos: int) -> tuple[Region, int]:
		"""Converts a position relative to the braille buffer to a position relative to the region it is in.
		:param bufferPos: The position relative to the braille buffer.
		:return: A tuple of the region and the position relative to that region.
		"""
		for region, start, end in self.regionsWithPositions:
			if end > bufferPos:
				return region, bufferPos - start
		raise LookupError("No such position")

	def _getLanguageAtBufferPos(self, pos: int) -> str:
		"""Gets the language at the given braille buffer position."""
		region, regionPos = self.bufferPosToRegionPos(pos)
		return region._getLanguageAtPos(regionPos)

	def regionPosToBufferPos(self, region: Region, pos: int, allowNearest: bool = False) -> int:
		"""Converts a position relative to a region to a position relative to the braille buffer.
		:param region: The region the position is relative to.
		:param pos: The position relative to the region.
		:param allowNearest: If True, if the position is outside the region, return the nearest position within the region. If False, raise LookupError if the position is outside the region.
		:return: The position relative to the braille buffer.
		"""
		start: int = 0
		for testRegion, start, end in self.regionsWithPositions:
			if region == testRegion:
				if pos < end - start:
					# The requested position is still valid within the region.
					return start + pos
				elif allowNearest:
					# The position within the region isn't valid,
					# but the region is valid, so return its start.
					return start
				break
		if allowNearest:
			# Resort to the start of the last region.
			return start
		raise LookupError("No such position")

	def bufferPositionsToRawText(self, startPos: int, endPos: int) -> str:
		"""
		Converts a range of positions in the braille buffer to the corresponding raw text.
		:param startPos: The start position in the braille buffer.
		:param endPos: The end position in the braille buffer.
		:return: The corresponding raw text.
		"""
		brailleToRawPos = self.brailleToRawPos
		if not brailleToRawPos or not self.rawText:
			# if either are empty, just return an empty string.
			return ""
		try:
			lastIndex = len(brailleToRawPos) - 1
			rawTextStart = brailleToRawPos[min(lastIndex, startPos)]
			rawTextEnd = brailleToRawPos[min(lastIndex, endPos)] + 1
			lastIndex = len(self.rawText)
			return self.rawText[rawTextStart : min(lastIndex, rawTextEnd)]
		except IndexError:
			log.debugWarning(
				f"Unable to get raw text for buffer positions"
				f"(startPos-endPos): {startPos}-{endPos}, "
				f"for rawText: {self.rawText}, "
				f"with brailleToRawPos: {brailleToRawPos}",
				exc_info=True,
			)
			return ""

	def bufferPosToWindowPos(self, bufferPos: int) -> int:
		"""
		Converts a position relative to the braille buffer to a position relative to the braille window.
		:param bufferPos: The position relative to the braille buffer.
		:return: The position relative to the braille window.
		"""
		for row, rowPositions in enumerate(self._windowRowBufferOffsets):
			if rowPositions.start <= bufferPos < rowPositions.end:
				return row * self.handler.displayDimensions.numCols + (bufferPos - rowPositions.start)
		raise LookupError("buffer pos not in window")

	def windowPosToBufferPos(self, windowPos: int) -> int:
		"""
		Converts a position relative to the braille window to a position relative to the braille buffer.
		"""
		if self.handler.displaySize == 0:
			return 0
		windowPos = max(min(windowPos, self.handler.displaySize), 0)
		row, col = divmod(windowPos, self.handler.displayDimensions.numCols)
		if row < len(self._windowRowBufferOffsets):
			rowPositions = self._windowRowBufferOffsets[row]
			return max(min(rowPositions.start + col, rowPositions.end - 1), 0)
		raise ValueError("Position outside window")

	windowStartPos: int
	"""The start position of the braille window in the braille buffer."""

	def _get_windowStartPos(self) -> int:
		return self.windowPosToBufferPos(0)

	def _set_windowStartPos(self, pos: int) -> None:
		self._calculateWindowRowBufferOffsets(pos)

	def _isMidWordCut(self, end: int, bufferEnd: int) -> bool:
		"""Return True when the cut at `end` falls in the middle of a word (both adjacent cells are non-space)."""
		return end < bufferEnd and all(self.brailleCells[end - 1 : end + 1])

	def _calculateWindowRowBufferOffsets(self, pos: int) -> None:
		"""
		Calculates the start and end positions of each row in the braille window.
		Ensures that words are not split across rows when text wrap is enabled.
		Ensures that the window does not extend past the end of the braille buffer.
		:param pos: The start position of the braille window.
		"""
		self._windowRowBufferOffsets.clear()
		if len(self.brailleCells) == 0:
			# Initialising with no actual braille content.
			self._windowRowBufferOffsets = [_WindowRowPositions(0, 0)]
			return
		textWrap: BrailleTextWrapFlag = config.conf["braille"]["textWrap"].calculated()
		bufferEnd = len(self.brailleCells)
		start = pos
		clippedEnd = False
		for row in range(self.handler.displayDimensions.numRows):
			showContinuationMark = False
			end = start + self.handler.displayDimensions.numCols
			if end > bufferEnd:
				end = bufferEnd
				clippedEnd = True
			elif textWrap == BrailleTextWrapFlag.MARK_WORD_CUTS and self._isMidWordCut(end, bufferEnd):
				end -= 1
				showContinuationMark = True
			elif textWrap in (
				BrailleTextWrapFlag.AT_WORD_BOUNDARIES,
				BrailleTextWrapFlag.AT_WORD_OR_SYLLABLE_BOUNDARIES,
			):
				try:
					lastSpaceIndex = rindex(self.brailleCells, 0, start, end + 1)
					if lastSpaceIndex < end:
						# lastSpaceIndex < end proves brailleCells[end] is non-zero,
						# so searching [start, end) yields the same lastSpaceIndex.
						oldEnd = end
						end = lastSpaceIndex + 1
						if end < oldEnd and textWrap == BrailleTextWrapFlag.AT_WORD_OR_SYLLABLE_BOUNDARIES:
							# Prefer splitting the word at a syllable boundary closer to the display edge.
							# Note that, when the below index call fails, it is appropriately handled by the except block,
							# which means that we won't split at a syllable boundary in this case.
							nextSpace = self.brailleCells.index(0, oldEnd, bufferEnd)
							word = self.bufferPositionsToRawText(end, nextSpace - 1)
							if word:
								language = self._getLanguageAtBufferPos(end)
								rawPos = self.brailleToRawPos[end]
								positions = textUtils.hyphenation.getHyphenPositions(word, language)
								for posInWord in reversed(positions):
									if (newEnd := self.rawToBraillePos[posInWord + rawPos]) < oldEnd:
										end = newEnd
										showContinuationMark = True
										break
				except (ValueError, IndexError):
					# No space on line - fall back to display-edge cut.
					if self._isMidWordCut(end, bufferEnd):
						end -= 1
						showContinuationMark = True
			self._windowRowBufferOffsets.append(_WindowRowPositions(start, end, showContinuationMark))
			if clippedEnd:
				break
			start = end

	windowEndPos: int
	"""The end position of the braille window in the braille buffer."""

	def _get_windowEndPos(self) -> int:
		return self._windowRowBufferOffsets[-1].end

	def _set_windowEndPos(self, endPos: int) -> None:
		"""Sets the end position for the braille window and recalculates the window start position based on several variables.
		1. Braille display size.
		2. Whether one of the regions should be shown hard left on the braille display;
			i.e. because of The configuration setting for focus context representation
			or whether the braille region that corresponds with the focus represents a multi line edit box.
		3. Whether text wrap is enabled."""
		startPos = endPos - self.handler.displaySize
		# Loop through the currently displayed regions in reverse order
		# If focusToHardLeft is set for one of the regions, the display shouldn't scroll further back than the start of that region
		for region, regionStart, regionEnd in reversed(list(self.regionsWithPositions)):
			if regionStart < endPos:
				if region.focusToHardLeft:
					# Only scroll to the start of this region.
					restrictPos = regionStart
					break
				elif config.conf["braille"]["focusContextPresentation"] != CONTEXTPRES_CHANGEDCONTEXT:
					# We aren't currently dealing with context change presentation
					# thus, we only need to consider the last region
					# since it doesn't have focusToHardLeftSet, the window start position isn't restricted
					restrictPos = 0
					break
		else:
			restrictPos = 0
		if startPos <= restrictPos:
			self.windowStartPos = restrictPos
			return
		if config.conf["braille"]["textWrap"].calculated() in (
			BrailleTextWrapFlag.NONE,
			BrailleTextWrapFlag.MARK_WORD_CUTS,
		):
			self.windowStartPos = startPos
			return
		try:
			# Try not to split words across windows.
			# To do this, break after the furthest possible block of spaces.
			# Find the start of the first block of spaces.
			# Search from 1 cell before in case startPos is just after a space.
			startPos = self.brailleCells.index(0, startPos - 1, endPos)
			# Skip past spaces.
			for startPos in range(startPos, endPos):
				if self.brailleCells[startPos] != 0:
					break
		except ValueError:
			pass
		# When text wrap is enabled, the first block of spaces may be removed from the current window.
		# This may prevent displaying the start of paragraphs.
		paragraphStartMarker = getParagraphStartMarker()
		if paragraphStartMarker and self.regions[-1].rawText.startswith(
			paragraphStartMarker + TEXT_SEPARATOR,
		):
			region, regionStart, regionEnd = list(self.regionsWithPositions)[-1]
			# Show paragraph start indicator if it is now at the left of the current braille window
			if startPos <= len(paragraphStartMarker) + 1:
				startPos = self.regionPosToBufferPos(region, regionStart)
		self.windowStartPos = startPos

	def _nextWindow(self):
		oldStart = self.windowStartPos
		end = self.windowEndPos
		if end < len(self.brailleCells):
			self.windowStartPos = end
		return self.windowStartPos != oldStart

	def scrollForward(self):
		if not self._nextWindow():
			# The window could not be scrolled, so try moving to the next line.
			if self.regions:
				self.regions[-1].nextLine()
		else:
			# Scrolling succeeded.
			self.updateDisplay()

	def _previousWindow(self):
		start = self.windowStartPos
		if start > 0:
			self.windowEndPos = start
		return self.windowStartPos != start

	def scrollBack(self):
		if not self._previousWindow():
			# The window could not be scrolled, so try moving to the previous line.
			if self.regions:
				self.regions[-1].previousLine()
		else:
			# Scrolling succeeded.
			self.updateDisplay()

	def scrollTo(self, region, pos):
		pos = self.regionPosToBufferPos(region, pos)
		while pos >= self.windowEndPos:
			if not self._nextWindow():
				break
		while pos < self.windowStartPos:
			if not self._previousWindow():
				break

	def focus(self, region):
		"""Bring the specified region into focus.
		The region is placed at the start of the display.
		However, if the region has not set L{Region.focusToHardLeft} and there is extra space at the end of the display, the display is scrolled left so that as much as possible is displayed.
		@param region: The region to focus.
		@type region: L{Region}
		"""
		pos = self.regionPosToBufferPos(region, 0)
		self.windowStartPos = pos
		if region.focusToHardLeft or config.conf["braille"]["focusContextPresentation"] == CONTEXTPRES_SCROLL:
			return
		end = self.windowEndPos
		if end - pos < self.handler.displaySize:
			# We can fit more on the display while still keeping pos visible.
			# Force windowStartPos to be recalculated based on windowEndPos.
			self.windowEndPos = end

	def update(self):
		self.rawText = ""
		self.brailleCells = []
		self.cursorPos = None
		start = 0
		if log.isEnabledFor(log.IO):
			logRegions = []
		for region in self.visibleRegions:
			rawText = region.rawText
			if log.isEnabledFor(log.IO):
				logRegions.append(rawText)
			cells = region.brailleCells
			self.rawText += rawText
			self.brailleCells.extend(cells)
			if region.brailleCursorPos is not None:
				self.cursorPos = start + region.brailleCursorPos
			start += len(cells)
		if log.isEnabledFor(log.IO):
			log.io("Braille regions text: %r" % logRegions)
		self._calculateWindowRowBufferOffsets(self.windowStartPos)

	def updateDisplay(self):
		if self is self.handler.buffer:
			self.handler.update()

	def _get_cursorWindowPos(self):
		if self.cursorPos is None:
			return None
		try:
			return self.bufferPosToWindowPos(self.cursorPos)
		except LookupError:
			return None

	def _get_windowRawText(self):
		return self.bufferPositionsToRawText(self.windowStartPos, self.windowEndPos)

	def _get_windowBrailleCells(self) -> list[int]:
		windowCells = []
		for row, rowPositions in enumerate(self._windowRowBufferOffsets):
			rowCells = self.brailleCells[rowPositions.start : rowPositions.end]
			remaining = self.handler.displayDimensions.numCols - len(rowCells)
			if remaining > 0 and rowPositions.showContinuationMark:
				rowCells.append(CONTINUATION_SHAPE)
				remaining -= 1
			if remaining > 0:
				rowCells.extend([0] * remaining)
			windowCells.extend(rowCells)
		return windowCells

	def routeTo(self, windowPos):
		pos = self.windowPosToBufferPos(windowPos)
		if pos >= self.windowEndPos:
			return
		region, pos = self.bufferPosToRegionPos(pos)
		region.routeTo(pos)

	def getTextInfoForWindowPos(self, windowPos):
		pos = self.windowPosToBufferPos(windowPos)
		if pos >= self.windowEndPos:
			return None
		region, pos = self.bufferPosToRegionPos(pos)
		if not isinstance(region, TextInfoRegion):
			return None
		return region.getTextInfoForBraillePos(pos)

	def saveWindow(self):
		"""Save the current window so that it can be restored after the buffer is updated.
		The window start position is saved as a position relative to a region.
		This allows it to be restored even after other regions are added, removed or updated.
		It can be restored with L{restoreWindow}.
		@postcondition: The window is saved and can be restored with L{restoreWindow}.
		"""
		self._savedWindow = self.bufferPosToRegionPos(self.windowStartPos)

	def restoreWindow(self):
		"""Restore the window saved by L{saveWindow}.
		@precondition: L{saveWindow} has been called.
		@postcondition: If the saved position is valid, the window is restored.
			Otherwise, the nearest position is restored.
		"""
		region, pos = self._savedWindow
		self.windowStartPos = self.regionPosToBufferPos(region, pos, allowNearest=True)


_cachedFocusAncestorsEnd = 0


def invalidateCachedFocusAncestors(index):
	"""Invalidate cached focus ancestors from a given index.
	This will cause regions to be generated for the focus ancestors >= index next time L{getFocusContextRegions} is called,
	rather than using cached regions for those ancestors.
	@param index: The index from which cached focus ancestors should be invalidated.
	@type index: int
	"""
	global _cachedFocusAncestorsEnd
	# There could be multiple calls to this function before getFocusContextRegions() is called.
	_cachedFocusAncestorsEnd = min(_cachedFocusAncestorsEnd, index)


def getFocusContextRegions(
	obj: "NVDAObject",
	oldFocusRegions: Optional[List[Region]] = None,
) -> Generator[Region, None, None]:
	if objectBelowLockScreenAndWindowsIsLocked(obj):
		return
	global _cachedFocusAncestorsEnd
	# Late import to avoid circular import.
	from treeInterceptorHandler import TreeInterceptor

	ancestors = api.getFocusAncestors()

	ancestorsEnd = len(ancestors)
	if isinstance(obj, TreeInterceptor):
		obj = obj.rootNVDAObject
		# We only want the ancestors of the buffer's root NVDAObject.
		if obj != api.getFocusObject():
			# Search backwards through the focus ancestors to find the index of obj.
			for index, ancestor in zip(range(len(ancestors) - 1, 0, -1), reversed(ancestors)):
				if obj == ancestor:
					ancestorsEnd = index
					break

	if oldFocusRegions:
		# We have the regions from the previous focus, so use them as a cache to avoid rebuilding regions which are the same.
		# We need to generate new regions from _cachedFocusAncestorsEnd onwards.
		# However, we must ensure that it is not beyond the last ancestor we wish to consider.
		# Also, we don't ever want to fetch ancestor 0 (the desktop).
		newAncestorsStart = max(min(_cachedFocusAncestorsEnd, ancestorsEnd), 1)
		# Search backwards through the old regions to find the last common region.
		for index, region in zip(range(len(oldFocusRegions) - 1, -1, -1), reversed(oldFocusRegions)):
			ancestorIndex = getattr(region, "_focusAncestorIndex", None)
			if ancestorIndex is None:
				continue
			if ancestorIndex < newAncestorsStart:
				# This is the last common region.
				# An ancestor may have been skipped and not have a region, which means that we need to grab new ancestors from this point.
				newAncestorsStart = ancestorIndex + 1
				commonRegionsEnd = index + 1
				break
		else:
			# No common regions were found.
			commonRegionsEnd = 0
			newAncestorsStart = 1
		# Yield the common regions.
		for region in oldFocusRegions[0:commonRegionsEnd]:
			# We are setting focusToHardLeft to False for every cached region.
			# This is necessary as BrailleHandler._doNewObject checks focusToHardLeft on every region
			# and sets it to True for the first focus region if the context didn't change.
			# If we don't do this, BrailleHandler._doNewObject can't set focusToHardLeft properly.
			region.focusToHardLeft = False
			yield region
	else:
		# Fetch all ancestors.
		newAncestorsStart = 1

	focusToHardLeftSet = False
	for index, parent in enumerate(ancestors[newAncestorsStart:ancestorsEnd], newAncestorsStart):
		if not parent.isPresentableFocusAncestor:
			continue
		region = NVDAObjectRegion(parent, appendText=TEXT_SEPARATOR)
		region._focusAncestorIndex = index
		if (
			config.conf["braille"]["focusContextPresentation"] == CONTEXTPRES_CHANGEDCONTEXT
			and not focusToHardLeftSet
		):
			# We are presenting context changes to the user
			# Thus, only scroll back as far as the start of the first new focus ancestor
			# focusToHardLeftSet is used since the first new ancestor isn't always represented by a region
			region.focusToHardLeft = True
			focusToHardLeftSet = True
		region.update()
		yield region

	_cachedFocusAncestorsEnd = ancestorsEnd


def getFocusRegions(
	obj: "NVDAObject",
	review: bool = False,
) -> Generator[Region, None, None]:
	if objectBelowLockScreenAndWindowsIsLocked(obj):
		return
	# Allow objects to override normal behaviour.
	try:
		regions = obj.getBrailleRegions(review=review)
	except (AttributeError, NotImplementedError):
		pass
	else:
		for region in regions:
			region.update()
			yield region
		return

	# Late import to avoid circular import.
	from treeInterceptorHandler import TreeInterceptor, DocumentTreeInterceptor
	from cursorManager import CursorManager
	from NVDAObjects import NVDAObject

	if isinstance(obj, CursorManager):
		region2 = (ReviewCursorManagerRegion if review else CursorManagerRegion)(obj)
	elif isinstance(obj, DocumentTreeInterceptor) or (
		isinstance(obj, NVDAObject) and NVDAObjectHasUsefulText(obj)
	):
		region2 = (ReviewTextInfoRegion if review else TextInfoRegion)(obj)
	else:
		region2 = None
	if isinstance(obj, TreeInterceptor):
		obj = obj.rootNVDAObject
	region = (ReviewNVDAObjectRegion if review else NVDAObjectRegion)(
		obj,
		appendText=TEXT_SEPARATOR if region2 else "",
	)
	region.update()
	yield region
	if region2:
		region2.update()
		yield region2


def formatCellsForLog(cells: List[int]) -> str:
	"""Formats a sequence of braille cells so that it is suitable for logging.
	The output contains the dot numbers for each cell, with each cell separated by a space.
	A C{-} indicates an empty cell.
	@param cells: The cells to format.
	@return: The formatted cells.
	"""
	# optimisation: This gets called a lot, so needs to be as efficient as possible.
	# List comprehensions without function calls are faster than loops.
	# For str.join, list comprehensions are faster than generator comprehensions.
	return TEXT_SEPARATOR.join(
		["".join([str(dot + 1) for dot in range(8) if cell & (1 << dot)]) if cell else "-" for cell in cells],
	)


class DisplayDimensions(NamedTuple):
	numRows: int
	numCols: int

	@property
	def displaySize(self) -> int:
		return self.numCols * self.numRows
