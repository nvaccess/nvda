# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2012-2026 NV Access Limited, Rui Batista, Babbage B.V., Julien Cochuyt, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Backward compatibility module for braille input.

This module is deprecated.
Braille input handling now lives in the :mod:`braille.input` package.
"""

from utils._deprecate import handleDeprecations, MovedSymbol

# Deprecated in 2026.3.
__getattr__ = handleDeprecations(
	MovedSymbol("handler", "braille.input"),
	MovedSymbol("initialize", "braille.input"),
	MovedSymbol("terminate", "braille.input"),
	MovedSymbol("FALLBACK_TABLE", "braille.input.constants"),
	MovedSymbol("DOT7", "braille.input.constants"),
	MovedSymbol("DOT8", "braille.input.constants"),
	MovedSymbol("LOUIS_DOTS_IO_START", "braille.input.constants"),
	MovedSymbol("UNICODE_BRAILLE_START", "braille.input.constants"),
	MovedSymbol("UNICODE_BRAILLE_PROTECTED", "braille.input.constants"),
	MovedSymbol("formatDotNumbers", "braille.input.gesture"),
	MovedSymbol("BrailleInputGesture", "braille.input.gesture"),
	MovedSymbol("BrailleInputHandler", "braille.input.inputHandler"),
	MovedSymbol("speakDots", "braille.input.inputHandler"),
)
"""Module level `__getattr__` used to preserve backward compatibility."""
