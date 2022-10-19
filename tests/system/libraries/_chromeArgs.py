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
		" --force-renderer-accessibility"  # don't rely on chrome detecting a screen reader.
		" --suppress-message-center-popups"  # prevent popups that may interfere with automated tests.
		" --disable-notifications"  # prevent notifications that may interfere with automated tests.
		" --no-experiments"  # Stable behavior is preferred.
		" --no-default-browser-check"  # Don't bother to check if Chrome is the default browser.
		" --lang=en-US"
	)


if __name__ == '__main__':
	# See usage in appveyor/scripts/tests/beforeTests.ps1
	print(getChromeArgs())
