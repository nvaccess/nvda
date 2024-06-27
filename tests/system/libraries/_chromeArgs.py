# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020-2022 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

""" This module provides a central location for arguments used to start Google Chrome.
"""


def getChromeArgs() -> str:
	"""Chrome and args to use for system tests
	Kept in a stand-alone file so the same args can be used where required.
	File path can be appended to this string.
	"""
	return (
		"chrome"  # Start Chrome
		" --no-first-run"  # Don't show intro pages for the first run of chrome
		" --force-renderer-accessibility"  # don't rely on chrome detecting a screen reader.
		" --ash-no-nudges"  # Prevents Chrome from showing nudge messages.
		" --browser-test"  # Enable browser test mode, helps reduce flakey tests
		" --disable-default-apps"  # Don't show default apps on the new tab page.
		" --keep-alive-for-test"  # Reduces start/stop time by keeping the app alive with no windows open.
		" --suppress-message-center-popups"  # prevent popups that may interfere with automated tests.
		" --disable-notifications"  # prevent notifications that may interfere with automated tests.
		" --no-experiments"  # Stable behavior is preferred.
		" --no-default-browser-check"  # Don't bother to check if Chrome is the default browser.
		" --lang=en-US"  # Set GUI lang to English to ensure tests pass on non-English systems. Must be supplied
		# to the first Chrome process started.
		" --disable-session-crashed-bubble"
		# --disable-session-crashed-bubble: If chrome crashes, don't cause subsequent tests to fail.
		# However, the config can be checked to determine if a crash occurred.
		# See https://superuser.com/a/1343331
		# Use %APPDATA%\Local\Google\Chrome\User Data\Default\Preference
		# Values:
		# "exit_type": "none",
		# "exited_cleanly": true,
		#
	)


if __name__ == '__main__':
	# See usage in appveyor/scripts/tests/beforeTests.ps1
	print(getChromeArgs())
