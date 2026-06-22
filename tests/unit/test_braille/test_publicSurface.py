# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Regression tests guarding the public attribute surface of the braille package.

Splitting braille.py into a package must not drop or hide any symbol that external
code (add-ons, drivers, other NVDA modules, tests) reaches as ``braille.X``.
"""

import unittest

import braille


#: Public symbols that must remain reachable as ``braille.<name>``.
EXPECTED_PUBLIC = frozenset(
	{
		# Classes
		"Region",
		"TextRegion",
		"NVDAObjectRegion",
		"ReviewNVDAObjectRegion",
		"TextInfoRegion",
		"CursorManagerRegion",
		"ReviewTextInfoRegion",
		"ReviewCursorManagerRegion",
		"BrailleBuffer",
		"DisplayDimensions",
		"BrailleHandler",
		"BrailleMode",
		"BrailleDisplayDriver",
		"BrailleDisplayGesture",
		"FormatTagDelimiter",
		"FormattingMarker",
		# Functions
		"NVDAObjectHasUsefulText",
		"getDisplayList",
		"getPropertiesBraille",
		"getControlFieldBraille",
		"getFormatFieldBraille",
		"getParagraphStartMarker",
		"invalidateCachedFocusAncestors",
		"getFocusContextRegions",
		"getFocusRegions",
		"formatCellsForLog",
		"initialize",
		"pumpAll",
		"terminate",
		"getSerialPorts",
		"getDisplayDrivers",
		"rindex",
		# Constants and module-level state
		"FALLBACK_TABLE",
		"roleLabels",
		"positiveStateLabels",
		"negativeStateLabels",
		"landmarkLabels",
		"CURSOR_SHAPES",
		"SELECTION_SHAPE",
		"CONTINUATION_SHAPE",
		"END_OF_BRAILLE_OUTPUT_SHAPE",
		"INPUT_START_IND",
		"INPUT_END_IND",
		"TEXT_SEPARATOR",
		"CONTEXTPRES_CHANGEDCONTEXT",
		"CONTEXTPRES_FILL",
		"CONTEXTPRES_SCROLL",
		"focusContextPresentations",
		"RegionWithPositions",
		"AUTOMATIC_PORT",
		"AUTO_DISPLAY_NAME",
		"NO_BRAILLE_DISPLAY_NAME",
		"USB_PORT",
		"BLUETOOTH_PORT",
		"fontAttributeFormattingMarkers",
		"RENAMED_DRIVERS",
		"handler",
		# Extension points
		"pre_writeCells",
		"filter_displaySize",
		"filter_displayDimensions",
		"displaySizeChanged",
		"displayChanged",
		"decide_enabled",
	},
)


class TestBraillePublicSurface(unittest.TestCase):
	def test_publicSymbolsPresent(self):
		missing = sorted(name for name in EXPECTED_PUBLIC if not hasattr(braille, name))
		self.assertEqual(missing, [], f"public braille symbols missing: {missing}")

	def test_publicSymbolsExported(self):
		notExported = sorted(EXPECTED_PUBLIC - set(braille.__all__))
		self.assertEqual(notExported, [], f"public symbols not in braille.__all__: {notExported}")
		unresolved = sorted(name for name in braille.__all__ if not hasattr(braille, name))
		self.assertEqual(unresolved, [], f"names in braille.__all__ that don't resolve: {unresolved}")
