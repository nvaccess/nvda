# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Extension points for the braille package."""

from __future__ import annotations

import extensionPoints

from .display import DisplayDimensions

pre_writeCells = extensionPoints.Action()
"""
Notifies when cells are about to be written to a braille display.
This allows components and add-ons to perform an action.
For example, when a system is controlled by a braille enabled remote system,
the remote system should know what cells to show on its display.
@param cells: The list of braille cells.
@type cells: List[int]
@param rawText: The raw text that corresponds with the cells.
@type rawText: str
@param currentCellCount: The current number of cells
@type currentCellCount: bool
"""

filter_displaySize = extensionPoints.Filter[int](
	_deprecationMessage="braille.filter_displaySize is deprecated. Use braille.filter_displayDimensions instead.",
)
"""
Note: filter_displayDimensions should now be used in place of this filter.
If this filter is used, NVDA will assume that the display has 1 row of `displaySize` cells.

Filter that allows components or add-ons to change the display size used for braille output.
For example, when a system has an 80 cell display, but is being controlled by a remote system with a 40 cell
display, the display size should be lowered to 40 .
:param value: the number of cells of the current display.
"""


filter_displayDimensions = extensionPoints.Filter[DisplayDimensions]()
"""
Filter that allows components or add-ons to change the number of rows and columns used for braille output.
For example, when a system has a display with 10 rows and 20 columns, but is being controlled by a remote system with a display of 5 rows and 40 coluns, the display number of rows should be lowered to 5.
:param value: a DisplayDimensions namedtuple with the number of rows and columns of the current display.
Note: this should be used in place of filter_displaySize.
"""

displaySizeChanged = extensionPoints.Action()
"""
Action that allows components or add-ons to be notified of display size changes.
For example, when a system is controlled by a remote system and the remote system swaps displays,
The local system should be notified about display size changes at the remote system.
:param displaySize: The current display size used by the braille handler.
:type displaySize: int
:param displayDimensions.numRows: The current number of rows used by the braille handler.
:type displayDimensions.numRows: int
:param displayDimensions.numCols: The current number of columns used by the braille handler.
:type displayDimensions.numCols: int
"""

displayChanged = extensionPoints.Action()
"""
Action that allows components or add-ons to be notified of braille display changes.
For example, when a system is controlled by a remote system and the remote system swaps displays,
The local system should be notified about display parameters at the remote system,
e.g. name and cellcount.
@param display: The new braille display driver
@type display: L{BrailleDisplayDriver}
@param isFallback: Whether the display is set as fallback display due to another display's failure
@type isFallback: bool
@param detected: If the display was set by auto detection, the device match that matched the driver
@type detected: bdDetect.DeviceMatch or C{None}
"""

decide_enabled = extensionPoints.Decider()
"""
Allows components or add-ons to decide whether the braille handler should be forcefully disabled.
For example, when a system is controlling a remote system with braille,
the local braille handler should be disabled as long as the system is in control of the remote system.
Handlers are called without arguments.
"""

_decide_disabledIncludesMessages = extensionPoints.Decider()
"""
Allows Remote Access to decide whether an exception should be made for showing ui.message.
Handlers are called without arguments.
"""

_pre_showBrailleMessage = extensionPoints.Action()
"""
Called before a `ui.message` is shown,
to allow Remote Access to show local messages to users who are controlling a remote computer.
Handlers are called without arguments.
"""

_post_dismissBrailleMessage = extensionPoints.Action()
"""
Called after a `ui.message` is dismissed,
to allow Remote Access to show local messages to users who are controlling a remote computer.
Handlers are called without arguments.
"""
