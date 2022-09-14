# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022 NV Access Limited, Burman's Computer and Education Ltd.

"""Braille display driver for Tivomatic Caiku albatross 46 and 80 displays.
Contains modules:

- constants.py
- driver.py
- gestures.py
- _threads.py
"""

# Imported here so that braille._getDisplayDriver can import
from .driver import BrailleDisplayDriver  # noqa: F401
