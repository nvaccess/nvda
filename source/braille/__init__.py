# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2008-2026 NV Access Limited, Joseph Lee, Babbage B.V., Davy Kager, Bram Duvigneau,
# Leonard de Ruijter, Burman's Computer and Education Ltd., Julien Cochuyt

from __future__ import annotations

from typing import Optional

import config
from config.configFlags import BrailleMode, TetherTo as TetherTo
from logHandler import log

from .labels import (
	roleLabels,
	positiveStateLabels,
	negativeStateLabels,
	landmarkLabels,
	CURSOR_SHAPES,
	SELECTION_SHAPE,
	CONTINUATION_SHAPE,
	END_OF_BRAILLE_OUTPUT_SHAPE,
	INPUT_START_IND,
	INPUT_END_IND,
	FormatTagDelimiter,
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
	FormattingMarker,
	fontAttributeFormattingMarkers,
)
from .regions import (
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
from .buffer import (
	BrailleBuffer,
	invalidateCachedFocusAncestors,
	getFocusContextRegions,
	getFocusRegions,
	formatCellsForLog,
	DisplayDimensions,
	_WindowRowPositions as _WindowRowPositions,
)
from .display import (
	getDisplayList,
	RENAMED_DRIVERS,
	BrailleDisplayDriver,
	BrailleDisplayGesture,
	getSerialPorts,
	getDisplayDrivers,
	_getDisplayDriver as _getDisplayDriver,
)

from ._handler import (
	FALLBACK_TABLE,
	BrailleHandler,
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
