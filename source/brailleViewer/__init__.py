# brailleViewer.py
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2014-2017 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
from typing import Optional

import braille
import gui
from logHandler import log
import extensionPoints
from .brailleViewerDriver import BrailleViewerDriver
from .brailleViewerGui import BrailleViewerFrame

"""
This package contains the components for a "Braille Viewer". A window, that shows the braille dots that
would be displayed on a hardware device. The raw text for each cell is also shown.
This tool consists of:
- A braille driver, this receives special treatment from BrailleHandler L{BrailleHandler.viewerTool} so that
	it can work along side a hardware braille display. When used in conjunction with a hardware braille display,
	the number of cells in the braille viewer tool must be adjusted to match the hardware display.
- A GUI for the viewer.
- Construction / destruction helpers.

- Constructing / showing the BrailleViewer
	- On startup via L{core.doStartupDialogs}
	- Via NVDA (tools) menu via L{Mainframe.onToggleSpeechViewerCommand}
- Hiding / destroying the BrailleViewer 
	- On exit of NVDA.
	- Via NVDA (tools) menu via L{Mainframe.onToggleSpeechViewerCommand}
	- When the Window receives a close event. This means the GUI must be able to call-back to clean up
	BrailleHandler and the NVDA tools menu. This callback happens via the L{postBrailleViewerToolToggledAction}
"""

# global braille viewer driver:
_brailleDriver: Optional[BrailleViewerDriver] = None
_brailleGui: Optional[BrailleViewerFrame] = None

# Extension points action:
# Triggered every time the Braille Viewer is created / shown or hidden / destroyed.
# Callback definition: Callable(created: bool) -> None
#   created - True for created/shown, False for hidden/destructed.
postBrailleViewerToolToggledAction = extensionPoints.Action()


def isBrailleViewerActive() -> bool:
	return bool(_brailleDriver)


def getBrailleViewerDriver() -> Optional[BrailleViewerDriver]:
	return _brailleDriver

def _destroyDriver():
	global _brailleDriver
	d: Optional[BrailleViewerDriver] = _brailleDriver
	_brailleDriver = None
	if d:
		try:
			d.terminate()
		except:  # noqa: E722 # Bare except
			log.error("Error terminating braille viewer tool", exc_info=True)


def _destroyGUI():
	global _brailleGui
	d: Optional[BrailleViewerFrame] = _brailleGui
	_brailleGui = None
	if d and not d.isDestroyed:
		d.savePositionInformation()
		d.doDestroy()


def destroyBrailleViewer():
	_destroyDriver()
	_destroyGUI()
	postBrailleViewerToolToggledAction.notify(created=False)


def _onGuiDestroyed():
	global _brailleGui, _brailleDriver
	if _brailleGui:  # this wasn't initiated from L{_destroyGUI}
		destroyBrailleViewer()


def createBrailleViewerTool():
	if not gui.mainFrame:
		raise RuntimeError("Can not initialise the BrailleViewerGui: gui.mainFrame not yet initialised")
	if not braille.handler:
		raise RuntimeError("Can not initialise the BrailleViewerGui: braille.handler not yet initialised")

	DEFAULT_NUM_CELLS = 40
	numCells = DEFAULT_NUM_CELLS
	if braille.handler.displaySize:
		numCells = braille.handler.displaySize

	global _brailleGui
	if _brailleGui:
		_destroyGUI()
	_brailleGui = BrailleViewerFrame(numCells, _onGuiDestroyed)

	def onUpdated(cells: str, raw: str):
		global _brailleGui
		if _brailleGui:
			_brailleGui.updateValues(braille=cells, text=raw)

	global _brailleDriver
	if _brailleDriver:
		_brailleDriver.__init__(numCells, _brailleGui)
	else:
		_brailleDriver = BrailleViewerDriver(numCells, onUpdated)
	postBrailleViewerToolToggledAction.notify(created=True)

