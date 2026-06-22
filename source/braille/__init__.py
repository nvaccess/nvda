# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2008-2026 NV Access Limited, Joseph Lee, Babbage B.V., Davy Kager, Bram Duvigneau, Leonard de Ruijter, Burman's Computer and Education Ltd., Julien Cochuyt
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from __future__ import annotations

from typing import Optional

import config
from config.configFlags import (
	BrailleMode,
	TetherTo as TetherTo,
)
from logHandler import log

from .brailleHandler import (
	FALLBACK_TABLE,
	BrailleHandler,
	formatCellsForLog,
)
from .buffers import (
	BrailleBuffer,
)
from .constants import (
	AUTO_DISPLAY_NAME,
	AUTOMATIC_PORT,
	BLUETOOTH_PORT,
	CONTEXTPRES_CHANGEDCONTEXT,
	CONTEXTPRES_FILL,
	CONTEXTPRES_SCROLL,
	CONTINUATION_SHAPE,
	CURSOR_SHAPES,
	END_OF_BRAILLE_OUTPUT_SHAPE,
	INPUT_END_IND,
	INPUT_START_IND,
	NO_BRAILLE_DISPLAY_NAME,
	SELECTION_SHAPE,
	TEXT_SEPARATOR,
	USB_PORT,
	focusContextPresentations,
)
from .display import (
	DisplayDimensions,
	RENAMED_DRIVERS,
	getDisplayDrivers,
	getDisplayList,
	getSerialPorts,
)
from .display.driver import BrailleDisplayDriver
from .display.gesture import BrailleDisplayGesture
from .extensions import (
	decide_enabled,
	displayChanged,
	displaySizeChanged,
	filter_displayDimensions,
	filter_displaySize,
	pre_writeCells,
)
from .formatting import (
	FormatTagDelimiter,
	FormattingMarker,
	fontAttributeFormattingMarkers,
	getParagraphStartMarker,
)
from .labels import (
	landmarkLabels,
	negativeStateLabels,
	positiveStateLabels,
	roleLabels,
)
from .regions.base import Region, RegionWithPositions, TextRegion, rindex
from .regions.properties import getControlFieldBraille, getFormatFieldBraille, getPropertiesBraille
from .regions.NVDAObject import NVDAObjectHasUsefulText, NVDAObjectRegion, ReviewNVDAObjectRegion
from .regions.textInfo import (
	CursorManagerRegion,
	ReviewCursorManagerRegion,
	ReviewTextInfoRegion,
	TextInfoRegion,
)
from .regions.focus import getFocusContextRegions, getFocusRegions, invalidateCachedFocusAncestors

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
