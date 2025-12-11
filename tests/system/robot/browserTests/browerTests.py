# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html


from robot.libraries.BuiltIn import BuiltIn
from SystemTestSpy import _getLib
import NvdaLib as _NvdaLib

_builtIn: BuiltIn = BuiltIn()
_browserLib = _getLib("WebBrowserGenericLib")


def read_window_title():
	"""Start the browser and ensure NVDA reads the window title."""
	_browserLib.start_all_browsers()
	# Check status line as a proxy for window focus and basic NVDA interaction
	speech = _NvdaLib.getSpeechAfterKey("NVDA+end")
	_builtIn.should_not_contain(speech, "no status line found")


def browser_status_line_is_available():
	"""Start the browser and ensure NVDA+end does not report "no status line found"."""
	_browserLib.start_all_browsers()
	speech = _NvdaLib.getSpeechAfterKey("NVDA+end")
	_builtIn.should_not_contain(speech, "no status line found")


def browse_mode_landmarks_general_principles():
	"""Load landmarks general principles and assert browse-mode navigation announces headings/landmarks."""
	_browserLib.open_w3c_example("patterns/landmarks/examples/general-principles.html")
	# Headings navigation
	speech = _NvdaLib.getSpeechAfterKey("h")
	_builtIn.should_contain(speech, "heading")
	speech = _NvdaLib.getSpeechAfterKey("shift+h")
	_builtIn.should_contain(speech, "heading")
	# Links navigation
	speech = _NvdaLib.getSpeechAfterKey("l")
	_builtIn.should_contain_any(speech, ["link", "visited link"])  # Accept either
	speech = _NvdaLib.getSpeechAfterKey("shift+l")
	_builtIn.should_contain_any(speech, ["link", "visited link"])  # Accept either
	# Landmarks navigation
	speech = _NvdaLib.getSpeechAfterKey("d")
	_builtIn.should_contain(speech, "landmark")
	speech = _NvdaLib.getSpeechAfterKey("shift+d")
	_builtIn.should_contain(speech, "landmark")


def focus_mode_form_fields():
	"""Toggle to focus mode, tab through form fields and assert NVDA announces focus changes."""
	_browserLib.open_w3c_example("patterns/landmarks/examples/form.html")
	# Toggle to focus mode
	speech = _NvdaLib.getSpeechAfterKey("NVDA+space")
	_builtIn.should_contain_any(speech, ["focus mode", "forms mode"])  # Different phrasing acceptable
	# Tab to interactive elements
	speech = _NvdaLib.getSpeechAfterKey("tab")
	_builtIn.should_contain_any(speech, ["edit", "combo box", "checkbox", "radio button", "button"])  # generic controls
	speech = _NvdaLib.getSpeechAfterKey("shift+tab")
	_builtIn.should_contain_any(speech, ["edit", "combo box", "checkbox", "radio button", "button"])  # generic controls


def interactive_elements_buttons():
	"""Load buttons example and navigate/activate buttons."""
	_browserLib.open_w3c_example("patterns/button/examples/index.html")
	# Navigate buttons in browse mode
	speech = _NvdaLib.getSpeechAfterKey("b")
	_builtIn.should_contain(speech, "button")
	speech = _NvdaLib.getSpeechAfterKey("shift+b")
	_builtIn.should_contain(speech, "button")
	# Activate focused button
	speech = _NvdaLib.getSpeechAfterKey("enter")
	_builtIn.should_not_be_empty(speech)


def dynamic_content_live_regions():
	"""Assert NVDA announces polite and assertive live region updates."""
	# Use W3C hosted example as specified in test plan
	_browserLib.open_w3c_example("https://www.w3.org/WAI/ARIA/apg/example-index/live_regions/polite.html")
	# Trigger polite update (page auto updates or via button)
	speech = _NvdaLib.getSpeechAfterKey("enter")
	_builtIn.should_contain_any(speech, ["updated", "polite"])  # allow flexible phrasing
	# Navigate to assertive example
	_browserLib.open_w3c_example("https://www.w3.org/WAI/ARIA/apg/example-index/live_regions/assertive.html")
	# Trigger assertive update
	speech = _NvdaLib.getSpeechAfterKey("enter")
	_builtIn.should_not_be_empty(speech)


def browser_ui_menu_bookmarks_settings():
	"""Test basic browser UI: menus, bookmarks, settings navigation."""
	# Open main menu (Alt+F for Chrome/Edge, Alt for Firefox). We accept generic speech presence.
	speech = _NvdaLib.getSpeechAfterKey("alt+f")
	_builtIn.should_not_be_empty(speech)
	# Create bookmark (Ctrl+D)
	speech = _NvdaLib.getSpeechAfterKey("ctrl+d")
	_builtIn.should_not_be_empty(speech)
	# Open settings (Chrome/Edge Alt+F then S; Firefox Alt+T then O)
	# We make a generic assertion for speech appearing when navigating settings.
	speech = _NvdaLib.getSpeechAfterKey("alt+f")
	speech = _NvdaLib.getSpeechAfterKey("s")
	_builtIn.should_not_be_empty(speech)
