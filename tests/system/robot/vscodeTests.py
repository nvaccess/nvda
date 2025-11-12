# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2025 NV Access Limited, Bill Dengler
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from robot.libraries.BuiltIn import BuiltIn
from SystemTestSpy import _getLib
import NvdaLib as _NvdaLib
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from VSCodeLib import VSCodeLib

_builtIn: BuiltIn = BuiltIn()
_vscode: VSCodeLib = _getLib("VSCodeLib")


def status_line_is_available():
	"""Start Visual Studio Code and ensure NVDA+end does not report "no status line found"."""
	_vscode.start_vscode()
	speech = _NvdaLib.getSpeechAfterKey("NVDA+end")
	_builtIn.should_not_contain(speech, "no status line found")

def sidebar_toggle_announced():
	"""Start Visual Studio Code and ensure NVDA+end does not report "no status line found"."""
	_vscode.start_vscode()
	speech = _NvdaLib.getSpeechAfterKey("control+b")
	_builtIn.should_contain(speech, "sidebar shown")
	speech = _NvdaLib.getSpeechAfterKey("control+b")
	_builtIn.should_contain(speech, "sidebar hidden")

def command_palette_opens():
	"""Start Visual Studio Code and ensure NVDA+end does not report "no status line found"."""
	_vscode.start_vscode()
	speech = _NvdaLib.getSpeechAfterKey("control+shift+p")
	_builtIn.should_contain(speech, "type the name of a command")
	_NvdaLib.getSpeechAfterKey("escape")
	speech = _NvdaLib.getSpeechAfterKey("f1")
	_builtIn.should_contain(speech, "type the name of a command")

def file_navigation():
	"""Start Visual Studio Code and ensure NVDA+end does not report "no status line found"."""
	_vscode.start_vscode()
	# create 2 new files
	_NvdaLib.getSpeechAfterKey("control+n")
	# navigate to file
	speech = _NvdaLib.getSpeechAfterKey("control+tab")
	_builtIn.should_contain(speech, "Untitled-1")
	# Create second file
	_NvdaLib.getSpeechAfterKey("control+n")
	speech = _NvdaLib.getSpeechAfterKey("control+tab")
	_builtIn.should_contain(speech, "Untitled-2")
	# Go to file explorer
	speech = _NvdaLib.getSpeechAfterKey("control+shift+e")
	_builtIn.should_contain(speech, "Files Explorer")

def search_panel_focus():
	"""Start Visual Studio Code and ensure NVDA+end does not report "no status line found"."""
	_vscode.start_vscode()
	speech = _NvdaLib.getSpeechAfterKey("control+shift+f")
	_builtIn.should_contain(speech, "Search")
