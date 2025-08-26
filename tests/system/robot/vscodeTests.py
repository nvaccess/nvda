# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 Bill Dengler
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.


from robot.libraries.BuiltIn import BuiltIn
from SystemTestSpy import _getLib
import NvdaLib as _NvdaLib

_builtIn: BuiltIn = BuiltIn()
_vscode = _getLib("VSCodeLib")


def vs_code_status_line_is_available():
	"""Start Visual Studio Code and ensure NVDA+end does not report "no status line found"."""
	_vscode.start_vscode()
	speech = _NvdaLib.getSpeechAfterKey("NVDA+end")
	_builtIn.should_not_contain(speech, "no status line found")
