# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2008-2026 NV Access Limited, Joseph Lee, Babbage B.V., Davy Kager, Bram Duvigneau, Leonard de Ruijter, Burman's Computer and Education Ltd., Julien Cochuyt
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from __future__ import annotations

import config
from logHandler import log

from . import brailleHandler as _brailleHandler
from utils._deprecate import handleDeprecations, MovedSymbol

handler: _brailleHandler.BrailleHandler | None = None


def initialize():
	global handler
	import louis

	log.info("Using liblouis version %s" % louis.version())
	import serial

	log.info("Using pySerial version %s" % serial.VERSION)
	handler = _brailleHandler.BrailleHandler()
	handler.handlePostConfigProfileSwitch()
	config.post_configProfileSwitch.register(handler.handlePostConfigProfileSwitch)


def pumpAll():
	"""Runs tasks at the end of each core cycle. For now just region updates, e.g. for caret movement."""
	handler._handlePendingUpdate()


def terminate():
	global handler
	handler.terminate()
	handler = None


# Deprecated in 2026.3.
__getattr__ = handleDeprecations(
	MovedSymbol("BrailleDisplayDriver", "braille.display.driver"),
	MovedSymbol("BrailleDisplayGesture", "braille.display.gesture"),
	MovedSymbol("getSerialPorts", "braille.display"),
	MovedSymbol("getDisplayList", "braille.display"),
	MovedSymbol("getDisplayDrivers", "braille.display"),
	MovedSymbol("RENAMED_DRIVERS", "braille.display"),
	MovedSymbol("DisplayDimensions", "braille.display"),
	MovedSymbol("Region", "braille.regions.base"),
	MovedSymbol("RegionWithPositions", "braille.regions.base"),
	MovedSymbol("TextRegion", "braille.regions.base"),
	MovedSymbol("rindex", "braille.regions.base"),
	MovedSymbol("NVDAObjectRegion", "braille.regions.NVDAObject"),
	MovedSymbol("ReviewNVDAObjectRegion", "braille.regions.NVDAObject"),
	MovedSymbol("NVDAObjectHasUsefulText", "braille.regions.NVDAObject"),
	MovedSymbol("TextInfoRegion", "braille.regions.textInfo"),
	MovedSymbol("CursorManagerRegion", "braille.regions.textInfo"),
	MovedSymbol("ReviewTextInfoRegion", "braille.regions.textInfo"),
	MovedSymbol("ReviewCursorManagerRegion", "braille.regions.textInfo"),
	MovedSymbol("getControlFieldBraille", "braille.regions.properties"),
	MovedSymbol("getFormatFieldBraille", "braille.regions.properties"),
	MovedSymbol("getPropertiesBraille", "braille.regions.properties"),
	MovedSymbol("getFocusContextRegions", "braille.regions.focus"),
	MovedSymbol("getFocusRegions", "braille.regions.focus"),
	MovedSymbol("invalidateCachedFocusAncestors", "braille.regions.focus"),
	MovedSymbol("BrailleBuffer", "braille.buffers"),
	MovedSymbol("BrailleHandler", "braille.brailleHandler"),
	MovedSymbol("formatCellsForLog", "braille.brailleHandler"),
	MovedSymbol("FALLBACK_TABLE", "braille.brailleHandler"),
	MovedSymbol("roleLabels", "braille.labels"),
	MovedSymbol("positiveStateLabels", "braille.labels"),
	MovedSymbol("negativeStateLabels", "braille.labels"),
	MovedSymbol("landmarkLabels", "braille.labels"),
	MovedSymbol("FormatTagDelimiter", "braille.formatting"),
	MovedSymbol("FormattingMarker", "braille.formatting"),
	MovedSymbol("fontAttributeFormattingMarkers", "braille.formatting"),
	MovedSymbol("getParagraphStartMarker", "braille.formatting"),
	MovedSymbol("AUTO_DISPLAY_NAME", "braille.constants"),
	MovedSymbol("AUTOMATIC_PORT", "braille.constants"),
	MovedSymbol("BLUETOOTH_PORT", "braille.constants"),
	MovedSymbol("USB_PORT", "braille.constants"),
	MovedSymbol("NO_BRAILLE_DISPLAY_NAME", "braille.constants"),
	MovedSymbol("CONTINUATION_SHAPE", "braille.constants"),
	MovedSymbol("CURSOR_SHAPES", "braille.constants"),
	MovedSymbol("SELECTION_SHAPE", "braille.constants"),
	MovedSymbol("END_OF_BRAILLE_OUTPUT_SHAPE", "braille.constants"),
	MovedSymbol("INPUT_START_IND", "braille.constants"),
	MovedSymbol("INPUT_END_IND", "braille.constants"),
	MovedSymbol("TEXT_SEPARATOR", "braille.constants"),
	MovedSymbol("CONTEXTPRES_CHANGEDCONTEXT", "braille.constants"),
	MovedSymbol("CONTEXTPRES_FILL", "braille.constants"),
	MovedSymbol("CONTEXTPRES_SCROLL", "braille.constants"),
	MovedSymbol("focusContextPresentations", "braille.constants"),
	MovedSymbol("pre_writeCells", "braille.extensions"),
	MovedSymbol("filter_displaySize", "braille.extensions"),
	MovedSymbol("filter_displayDimensions", "braille.extensions"),
	MovedSymbol("displaySizeChanged", "braille.extensions"),
	MovedSymbol("displayChanged", "braille.extensions"),
	MovedSymbol("decide_enabled", "braille.extensions"),
	MovedSymbol("BrailleMode", "config.configFlags"),
	MovedSymbol("TetherTo", "config.configFlags"),
)
"""Module level `__getattr__` used to preserve backward compatibility."""
