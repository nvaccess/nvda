# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2012-2026 NV Access Limited, Rui Batista, Babbage B.V., Julien Cochuyt, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Constants for handling braille input."""

import config

FALLBACK_TABLE = config.conf.getConfigValidation(("braille", "inputTable")).default
"""Table to use if the input table configuration is invalid."""

DOT7 = 1 << 6
DOT8 = 1 << 7

LOUIS_DOTS_IO_START = 0x8000
"""This bit flag must be added to all braille cells when using liblouis with dotsIO."""

UNICODE_BRAILLE_START = 0x2800
"""The start of the Unicode braille range."""

UNICODE_BRAILLE_PROTECTED = "⣿"  # All dots down
"""The Unicode braille character to use when masking cells in protected fields."""
