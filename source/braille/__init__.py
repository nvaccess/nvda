# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2008-2026 NV Access Limited, Joseph Lee, Babbage B.V., Davy Kager, Bram Duvigneau, Leonard de Ruijter, Burman's Computer and Education Ltd., Julien Cochuyt
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from __future__ import annotations

from enum import StrEnum
from typing import (
	TYPE_CHECKING,
	Generator,
	List,
	NamedTuple,
	Optional,
)

import api
import config
from config.configFlags import (
	BrailleMode,
	OutputMode,
	ReportSpellingErrors,
	TetherTo as TetherTo,
)
from logHandler import log
from utils.security import objectBelowLockScreenAndWindowsIsLocked

if TYPE_CHECKING:
	from NVDAObjects import NVDAObject

from .constants import (
	CURSOR_SHAPES,
	SELECTION_SHAPE,
	CONTINUATION_SHAPE,
	END_OF_BRAILLE_OUTPUT_SHAPE,
	INPUT_START_IND,
	INPUT_END_IND,
	TEXT_SEPARATOR,
	CONTEXTPRES_CHANGEDCONTEXT,
	CONTEXTPRES_FILL,
	CONTEXTPRES_SCROLL,
	focusContextPresentations,
	AUTOMATIC_PORT,
	AUTO_DISPLAY_NAME,
	NO_BRAILLE_DISPLAY_NAME,
	USB_PORT,
	BLUETOOTH_PORT,
)

FALLBACK_TABLE = config.conf.getConfigValidation(("braille", "translationTable")).default
"""Table to use if the output table configuration is invalid."""


class FormatTagDelimiter(StrEnum):
	"""Delimiters for the start and end of format tags.

	As these are shapes, they should be provided in unicode braille.
	"""

	START = "⣋"
	END = "⣙"


class FormattingMarker(NamedTuple):
	"""A pair of braille symbols that indicate the start and end of a particular type of font formatting.

	As these are shapes, they should be provided in unicode braille.
	"""

	start: str
	end: str

	def shouldBeUsed(self, key) -> bool:
		"""Determines if the formatting marker should be reported in braille.
		:param key: A key which represents an element that may be reported in braille.
		:return: `True` if the element should be reported, `False` otherwise.
		"""
		formatConfig = config.conf["documentFormatting"]
		if key in ("invalid-spelling", "invalid-grammar"):
			return bool(formatConfig["reportSpellingErrors2"] & ReportSpellingErrors.BRAILLE)
		return formatConfig["fontAttributeReporting"] & OutputMode.BRAILLE


fontAttributeFormattingMarkers: dict[str, FormattingMarker] = {
	"bold": FormattingMarker(
		# Translators: Brailled at the start of bold text.
		# This is the English letter "b" in braille.
		start=pgettext("braille formatting symbol", "⠃"),
		# Translators: Brailled at the end of bold text.
		# This is the English letter "b" plus dot 7 in braille.
		end=pgettext("braille formatting symbol", "⡃"),
	),
	"italic": FormattingMarker(
		# Translators: Brailled at the start of italic text.
		# This is the English letter "i" in braille.
		start=pgettext("braille formatting symbol", "⠊"),
		# Translators: Brailled at the end of italic text.
		# This is the English letter "i" plus dot 7 in braille.
		end=pgettext("braille formatting symbol", "⡊"),
	),
	"underline": FormattingMarker(
		# Translators: Brailled at the start of underlined text.
		# This is the English letter "u" in braille.
		start=pgettext("braille formatting symbol", "⠥"),
		# Translators: Brailled at the end of underlined text.
		# This is the English letter "u" plus dot 7 in braille.
		end=pgettext("braille formatting symbol", "⡥"),
	),
	"strikethrough": FormattingMarker(
		# Translators: Brailled at the start of strikethrough text.
		# This is the English letter "s" in braille.
		start=pgettext("braille formatting symbol", "⠎"),
		# Translators: Brailled at the end of strikethrough text.
		# This is the English letter "s" plus dot 7 in braille.
		end=pgettext("braille formatting symbol", "⡎"),
	),
	"invalid-spelling": FormattingMarker(
		# Translators: Brailled at the start of invalid spelling text.
		# This is the English letter "e" in braille.
		start=pgettext("braille formatting symbol", "⠑"),
		# Translators: Brailled at the end of invalid spelling text.
		# This is the English letter "e" plus dot 7 in braille.
		end=pgettext("braille formatting symbol", "⡑"),
	),
	"invalid-grammar": FormattingMarker(
		# Translators: Brailled at the start of invalid grammar text.
		# This is the English letter "g" in braille.
		start=pgettext("braille formatting symbol", "⠛"),
		# Translators: Brailled at the end of invalid grammar text.
		# This is the English letter "g" plus dot 7 in braille.
		end=pgettext("braille formatting symbol", "⡛"),
	),
}

# The submodule imports below are intentionally not at the top of the file (hence noqa: E402).
# regions imports the constants and formatting markers defined above back from this package
# (e.g. `from . import FormattingMarker`), so those names must already exist on the package when
# the submodule is imported during this package's own (partial) initialisation.
from .labels import (  # noqa: E402
	roleLabels,
	positiveStateLabels,
	negativeStateLabels,
	landmarkLabels,
)
from .regions import (  # noqa: E402
	NVDAObjectHasUsefulText,
	RegionWithPositions,
	Region,
	TextRegion,
	getPropertiesBraille,
	NVDAObjectRegion,
	ReviewNVDAObjectRegion,
	getControlFieldBraille,
	getFormatFieldBraille,
	getParagraphStartMarker,
	TextInfoRegion,
	CursorManagerRegion,
	ReviewTextInfoRegion,
	ReviewCursorManagerRegion,
	rindex,
)
from .buffers import (  # noqa: E402
	BrailleBuffer,
	_WindowRowPositions as _WindowRowPositions,
)


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


class DisplayDimensions(NamedTuple):
	numRows: int
	numCols: int

	@property
	def displaySize(self) -> int:
		return self.numCols * self.numRows


# BrailleHandler imports FALLBACK_TABLE, DisplayDimensions and the
# focus helpers defined above back from this package, so they must be defined before it is imported.
from .display import (  # noqa: E402
	getDisplayList,
	RENAMED_DRIVERS,
	BrailleDisplayDriver,
	BrailleDisplayGesture,
	getSerialPorts,
	getDisplayDrivers,
	_getDisplayDriver as _getDisplayDriver,
)

from .brailleHandler import (  # noqa: E402
	BrailleHandler,
	formatCellsForLog,
)
from .extensions import (  # noqa: E402
	pre_writeCells,
	filter_displaySize,
	filter_displayDimensions,
	displaySizeChanged,
	displayChanged,
	decide_enabled,
	_decide_disabledIncludesMessages as _decide_disabledIncludesMessages,
	_pre_showBrailleMessage as _pre_showBrailleMessage,
	_post_dismissBrailleMessage as _post_dismissBrailleMessage,
)

handler: Optional[BrailleHandler] = None


def initialize():
	global handler
	import louis

	log.info("Using liblouis version %s" % louis.version())
	import serial

	log.info("Using pySerial version %s" % serial.VERSION)
	handler = BrailleHandler()
	handler.handlePostConfigProfileSwitch()
	config.post_configProfileSwitch.register(handler.handlePostConfigProfileSwitch)


def pumpAll():
	"""Runs tasks at the end of each core cycle. For now just region updates, e.g. for caret movement."""
	handler._handlePendingUpdate()


def terminate():
	global handler
	handler.terminate()
	handler = None


#: Public API of the braille package.
#: Keep in sync with tests/unit/test_braille/test_publicSurface.py::EXPECTED_PUBLIC.
__all__ = [
	"AUTOMATIC_PORT",
	"AUTO_DISPLAY_NAME",
	"BLUETOOTH_PORT",
	"BrailleBuffer",
	"BrailleDisplayDriver",
	"BrailleDisplayGesture",
	"BrailleHandler",
	"BrailleMode",
	"CONTEXTPRES_CHANGEDCONTEXT",
	"CONTEXTPRES_FILL",
	"CONTEXTPRES_SCROLL",
	"CONTINUATION_SHAPE",
	"CURSOR_SHAPES",
	"CursorManagerRegion",
	"DisplayDimensions",
	"END_OF_BRAILLE_OUTPUT_SHAPE",
	"FALLBACK_TABLE",
	"FormatTagDelimiter",
	"FormattingMarker",
	"INPUT_END_IND",
	"INPUT_START_IND",
	"NO_BRAILLE_DISPLAY_NAME",
	"NVDAObjectHasUsefulText",
	"NVDAObjectRegion",
	"Region",
	"RegionWithPositions",
	"RENAMED_DRIVERS",
	"ReviewCursorManagerRegion",
	"ReviewNVDAObjectRegion",
	"ReviewTextInfoRegion",
	"SELECTION_SHAPE",
	"TEXT_SEPARATOR",
	"TextInfoRegion",
	"TextRegion",
	"USB_PORT",
	"decide_enabled",
	"displayChanged",
	"displaySizeChanged",
	"filter_displayDimensions",
	"filter_displaySize",
	"focusContextPresentations",
	"fontAttributeFormattingMarkers",
	"formatCellsForLog",
	"getControlFieldBraille",
	"getDisplayDrivers",
	"getDisplayList",
	"getFocusContextRegions",
	"getFocusRegions",
	"getFormatFieldBraille",
	"getParagraphStartMarker",
	"getPropertiesBraille",
	"getSerialPorts",
	"handler",
	"initialize",
	"invalidateCachedFocusAncestors",
	"landmarkLabels",
	"negativeStateLabels",
	"positiveStateLabels",
	"pre_writeCells",
	"pumpAll",
	"rindex",
	"roleLabels",
	"terminate",
]
