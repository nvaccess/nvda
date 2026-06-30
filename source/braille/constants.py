# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2008-2026 NV Access Limited, Joseph Lee, Babbage B.V., Davy Kager, Bram Duvigneau, Leonard de Ruijter, Burman's Computer and Education Ltd., Julien Cochuyt
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Constants for the braille package."""

from typing import Final

#: Cursor shapes
CURSOR_SHAPES = (
	# Translators: The description of a braille cursor shape.
	(0xC0, _("Dots 7 and 8")),
	# Translators: The description of a braille cursor shape.
	(0x80, _("Dot 8")),
	# Translators: The description of a braille cursor shape.
	(0xFF, _("All dots")),
)
SELECTION_SHAPE = 0xC0  #: Dots 7 and 8
CONTINUATION_SHAPE = 0xC0  #: Dots 7 and 8

END_OF_BRAILLE_OUTPUT_SHAPE = 0xFF  # All dots
"""
The braille shape shown on a braille display when
the number of cells used by the braille handler is lower than the actual number of cells.
The 0 based position of the shape is equal to the number of cells used by the braille handler.
"""

#: Unicode braille indicator at the start of untranslated braille input.
INPUT_START_IND = "⣏"
#: Unicode braille indicator at the end of untranslated braille input.
INPUT_END_IND = " ⣹"

# used to separate chunks of text when programmatically joined
TEXT_SEPARATOR = " "

#: Identifier for a focus context presentation setting that
#: only shows as much as possible focus context information when the context has changed.
CONTEXTPRES_CHANGEDCONTEXT = "changedContext"
#: Identifier for a focus context presentation setting that
#: shows as much as possible focus context information if the focus object doesn't fill up the whole display.
CONTEXTPRES_FILL = "fill"
#: Identifier for a focus context presentation setting that
#: always shows the object with focus at the very left of the braille display.
CONTEXTPRES_SCROLL = "scroll"
#: Focus context presentations associated with their user readable and translatable labels
focusContextPresentations = [
	# Translators: The label for a braille focus context presentation setting that
	# only shows as much as possible focus context information when the context has changed.
	(CONTEXTPRES_CHANGEDCONTEXT, _("Fill display for context changes")),
	# Translators: The label for a braille focus context presentation setting that
	# shows as much as possible focus context information if the focus object doesn't fill up the whole display.
	# This was the pre NVDA 2017.3 default.
	(CONTEXTPRES_FILL, _("Always fill display")),
	# Translators: The label for a braille focus context presentation setting that
	# always shows the object with focus at the very left of the braille display
	# (i.e. you will have to scroll back for focus context information).
	(CONTEXTPRES_SCROLL, _("Only when scrolling back")),
]

#: Automatic constant to be used by braille displays that support the "automatic" port
#: and automatic braille display detection
#: @type: tuple
# Translators: String representing automatic port selection for braille displays.
AUTOMATIC_PORT = ("auto", _("Automatic"))
#: Used in place of a specific braille display driver name to indicate that
#: braille displays should be automatically detected and used.
#: @type: str
AUTO_DISPLAY_NAME = AUTOMATIC_PORT[0]

NO_BRAILLE_DISPLAY_NAME: Final[str] = "noBraille"
"""The name of the noBraille display driver."""

#: A port name which indicates that USB should be used.
#: @type: tuple
# Translators: String representing the USB port selection for braille displays.
USB_PORT = ("usb", _("USB"))
#: A port name which indicates that Bluetooth should be used.
#: @type: tuple
# Translators: String representing the Bluetooth port selection for braille displays.
BLUETOOTH_PORT = ("bluetooth", _("Bluetooth"))
