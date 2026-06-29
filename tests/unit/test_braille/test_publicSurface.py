# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Regression tests guarding the public attribute surface of the braille package.

Splitting braille.py into a package must not drop or hide any symbol that external
code (add-ons, drivers, other NVDA modules, tests) reaches as ``braille.X``.
After the facade rewrite, resident names are directly on the module, deprecated names
are served via ``__getattr__`` with a log warning.
"""

import unittest
from unittest.mock import patch

import braille
import braille.brailleHandler
import braille.buffers
import braille.constants
import braille.display
import braille.display.driver
import braille.display.gesture
import braille.extensions
import braille.formatting
import braille.labels
import braille.regions.base
import braille.regions.NVDAObject
import braille.regions.focus
import braille.regions.properties
import braille.regions.textInfo
import config.configFlags


#: Names that live directly on ``braille`` and must NOT emit a deprecation warning.
RESIDENT = {"handler", "initialize", "pumpAll", "terminate"}

#: Mapping of deprecated name -> the object it should resolve to.
#: Import the canonical objects here so we can do an ``is`` check.
DEPRECATED = {
	# display
	"BrailleDisplayDriver": braille.display.driver.BrailleDisplayDriver,
	"BrailleDisplayGesture": braille.display.gesture.BrailleDisplayGesture,
	"getSerialPorts": braille.display.getSerialPorts,
	"getDisplayList": braille.display.getDisplayList,
	"getDisplayDrivers": braille.display.getDisplayDrivers,
	"RENAMED_DRIVERS": braille.display.RENAMED_DRIVERS,
	"DisplayDimensions": braille.display.DisplayDimensions,
	# regions.base
	"Region": braille.regions.base.Region,
	"RegionWithPositions": braille.regions.base.RegionWithPositions,
	"TextRegion": braille.regions.base.TextRegion,
	"rindex": braille.regions.base.rindex,
	# regions.NVDAObject
	"NVDAObjectRegion": braille.regions.NVDAObject.NVDAObjectRegion,
	"ReviewNVDAObjectRegion": braille.regions.NVDAObject.ReviewNVDAObjectRegion,
	"NVDAObjectHasUsefulText": braille.regions.NVDAObject.NVDAObjectHasUsefulText,
	# regions.textInfo
	"TextInfoRegion": braille.regions.textInfo.TextInfoRegion,
	"CursorManagerRegion": braille.regions.textInfo.CursorManagerRegion,
	"ReviewTextInfoRegion": braille.regions.textInfo.ReviewTextInfoRegion,
	"ReviewCursorManagerRegion": braille.regions.textInfo.ReviewCursorManagerRegion,
	# regions.properties
	"getControlFieldBraille": braille.regions.properties.getControlFieldBraille,
	"getFormatFieldBraille": braille.regions.properties.getFormatFieldBraille,
	"getPropertiesBraille": braille.regions.properties.getPropertiesBraille,
	# regions.focus
	"getFocusContextRegions": braille.regions.focus.getFocusContextRegions,
	"getFocusRegions": braille.regions.focus.getFocusRegions,
	"invalidateCachedFocusAncestors": braille.regions.focus.invalidateCachedFocusAncestors,
	# buffers
	"BrailleBuffer": braille.buffers.BrailleBuffer,
	# brailleHandler
	"BrailleHandler": braille.brailleHandler.BrailleHandler,
	"formatCellsForLog": braille.brailleHandler.formatCellsForLog,
	"FALLBACK_TABLE": braille.brailleHandler.FALLBACK_TABLE,
	# labels
	"roleLabels": braille.labels.roleLabels,
	"positiveStateLabels": braille.labels.positiveStateLabels,
	"negativeStateLabels": braille.labels.negativeStateLabels,
	"landmarkLabels": braille.labels.landmarkLabels,
	# formatting
	"FormatTagDelimiter": braille.formatting.FormatTagDelimiter,
	"FormattingMarker": braille.formatting.FormattingMarker,
	"fontAttributeFormattingMarkers": braille.formatting.fontAttributeFormattingMarkers,
	"getParagraphStartMarker": braille.formatting.getParagraphStartMarker,
	# constants
	"AUTO_DISPLAY_NAME": braille.constants.AUTO_DISPLAY_NAME,
	"AUTOMATIC_PORT": braille.constants.AUTOMATIC_PORT,
	"BLUETOOTH_PORT": braille.constants.BLUETOOTH_PORT,
	"USB_PORT": braille.constants.USB_PORT,
	"NO_BRAILLE_DISPLAY_NAME": braille.constants.NO_BRAILLE_DISPLAY_NAME,
	"CONTINUATION_SHAPE": braille.constants.CONTINUATION_SHAPE,
	"CURSOR_SHAPES": braille.constants.CURSOR_SHAPES,
	"SELECTION_SHAPE": braille.constants.SELECTION_SHAPE,
	"END_OF_BRAILLE_OUTPUT_SHAPE": braille.constants.END_OF_BRAILLE_OUTPUT_SHAPE,
	"INPUT_START_IND": braille.constants.INPUT_START_IND,
	"INPUT_END_IND": braille.constants.INPUT_END_IND,
	"TEXT_SEPARATOR": braille.constants.TEXT_SEPARATOR,
	"CONTEXTPRES_CHANGEDCONTEXT": braille.constants.CONTEXTPRES_CHANGEDCONTEXT,
	"CONTEXTPRES_FILL": braille.constants.CONTEXTPRES_FILL,
	"CONTEXTPRES_SCROLL": braille.constants.CONTEXTPRES_SCROLL,
	"focusContextPresentations": braille.constants.focusContextPresentations,
	# extensions
	"pre_writeCells": braille.extensions.pre_writeCells,
	"filter_displaySize": braille.extensions.filter_displaySize,
	"filter_displayDimensions": braille.extensions.filter_displayDimensions,
	"displaySizeChanged": braille.extensions.displaySizeChanged,
	"displayChanged": braille.extensions.displayChanged,
	"decide_enabled": braille.extensions.decide_enabled,
	# config.configFlags
	"BrailleMode": config.configFlags.BrailleMode,
	"TetherTo": config.configFlags.TetherTo,
}


class TestBraillePublicSurface(unittest.TestCase):
	def test_residentNamesAccessibleWithoutWarning(self):
		"""RESIDENT names must be reachable via getattr without any deprecation warning."""
		with patch("logHandler.log") as mockLog:
			for name in RESIDENT:
				with self.subTest(name=name):
					self.assertTrue(
						hasattr(braille, name),
						f"braille.{name} missing",
					)
			mockLog.warning.assert_not_called()

	def test_deprecatedNamesReturnCorrectObject(self):
		"""Each deprecated name must resolve to the same object as the new-home import."""
		for name, expected in DEPRECATED.items():
			with self.subTest(name=name):
				with patch("logHandler.log") as mockLog:
					actual = getattr(braille, name)
					self.assertIs(
						actual,
						expected,
						f"braille.{name} returned wrong object",
					)
					mockLog.warning.assert_called_once()
