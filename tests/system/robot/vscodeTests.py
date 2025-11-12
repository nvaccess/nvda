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
_vscode: "VSCodeLib" = _getLib("VSCodeLib")


def status_line_is_available():
	"""ensure NVDA+end does not report "no status line found"."""
	_vscode.start_vscode()
	speech = _NvdaLib.getSpeechAfterKey("NVDA+end")
	_builtIn.should_not_contain(speech, "no status line found")


def sidebar_toggle_announced():
	"""ensure control+b announces sidebar shown/hidden."""
	_vscode.start_vscode()
	speech = _NvdaLib.getSpeechAfterKey("control+b")
	_builtIn.should_contain(speech, "sidebar shown")
	speech = _NvdaLib.getSpeechAfterKey("control+b")
	_builtIn.should_contain(speech, "sidebar hidden")


def command_palette():
	"""ensure the command palette is announced when activated and can be navigated."""
	_vscode.start_vscode()
	spy = _NvdaLib.getSpyLib()
	speech = _NvdaLib.getSpeechAfterKey("control+shift+p")
	_builtIn.should_contain(speech, "type the name of a command")
	spy.emulateKeyPress("escape")
	speech = _NvdaLib.getSpeechAfterKey("f1")
	_builtIn.should_contain(speech, "type the name of a command")
	for c in "new file":
		spy.emulateKeyPress(c)
	speech = _NvdaLib.getSpeechAfterKey("downArrow")
	_builtIn.should_not_contain(speech, "Create: New File")
	speech = _NvdaLib.getSpeechAfterKey("upArrow")
	_builtIn.should_contain(speech, "Create: New File")
	spy.emulateKeyPress("enter")
	speech = _NvdaLib.getSpeechAfterKey("enter")
	_builtIn.should_contain(speech, "Untitled-1")


def file_navigation():
	"""ensure file navigation works correctly."""
	_vscode.start_vscode()
	spy = _NvdaLib.getSpyLib()
	# create 2 new files
	spy.emulateKeyPress("control+n")
	# navigate to file
	speech = _NvdaLib.getSpeechAfterKey("control+tab")
	_builtIn.should_contain(speech, "Untitled-1")
	# Create second file
	spy.emulateKeyPress("control+n")
	speech = _NvdaLib.getSpeechAfterKey("control+tab")
	_builtIn.should_contain(speech, "Untitled-2")
	# Go to file explorer
	speech = _NvdaLib.getSpeechAfterKey("control+shift+e")
	_builtIn.should_contain(speech, "Files Explorer")


def search_panel_focus():
	"""ensure the search panel is announced when activated."""
	_vscode.start_vscode()
	speech = _NvdaLib.getSpeechAfterKey("control+shift+f")
	_builtIn.should_contain(speech, "Search")


def file_editor_operations():
	"""ensure file editor operations such as navigation, undo, and redo work correctly."""
	_vscode.start_vscode()
	spy = _NvdaLib.getSpyLib()
	# create new file
	spy.emulateKeyPress("control+n")
	# type some text
	for c in "hello":
		spy.emulateKeyPress(c)
	# navigate with arrow keys
	speech = _NvdaLib.getSpeechAfterKey("leftArrow")
	_builtIn.should_contain(speech, "o")
	speech = _NvdaLib.getSpeechAfterKey("rightArrow")
	_builtIn.should_contain(speech, "blank")
	# jump to start of file
	spy.emulateKeyPress("control+home")
	speech = _NvdaLib.getSpeechAfterKey("NVDA+up")
	_builtIn.should_contain(speech, "hello")
	# jump to end of file
	spy.emulateKeyPress("control+end")
	speech = _NvdaLib.getSpeechAfterKey("leftArrow")
	_builtIn.should_contain(speech, "o")
	# open find bar and search
	spy.emulateKeyPress("control+f")
	spy.emulateKeyPress("h")
	spy.emulateKeyPress("e")
	speech = _NvdaLib.getSpeechAfterKey("l")
	_builtIn.should_contain(speech, "1 of 1")
	spy.emulateKeyPress("escape")
	# open replace bar
	speech = _NvdaLib.getSpeechAfterKey("control+h")
	_builtIn.should_contain(speech, "Find")
	spy.emulateKeyPress("escape")
	# type bracket for bracket matching test
	spy.emulateKeyPress("control+end")
	spy.emulateKeyPress("enter")
	spy.emulateKeyPress("leftParen")
	spy.emulateKeyPress("a")
	spy.emulateKeyPress("rightParen")
	# jump to matching bracket
	spy.emulateKeyPress("control+shift+backslash")
	speech = _NvdaLib.getSpeechAfterKey("NVDA+.")
	_builtIn.should_contain(speech, "(")
	# move line down
	spy.emulateKeyPress("control+home")
	speech = _NvdaLib.getSpeechAfterKey("alt+downArrow")
	_builtIn.should_contain(speech, "hello")
	# move line up
	speech = _NvdaLib.getSpeechAfterKey("alt+upArrow")
	_builtIn.should_contain(speech, "hello")
	# undo
	spy.emulateKeyPress("control+z")
	speech = _NvdaLib.getSpeechAfterKey("NVDA+up")
	_builtIn.should_contain(speech, "hello")
	# redo
	spy.emulateKeyPress("control+y")
	speech = _NvdaLib.getSpeechAfterKey("NVDA+up")
	_builtIn.should_contain(speech, "(a)")
