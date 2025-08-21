# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 Bill Dengler
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

*** Settings ***
Documentation	Visual Studio Code tests
Force Tags	NVDA	smoke test	vscode
Library	NvdaLib.py
Library	WindowsLib.py
Library	ScreenCapLibrary
Library	VSCodeLib.py
Library	vscodeTests.py

Test Setup	default setup
Test Teardown	default teardown

*** Keywords ***
default setup
	logForegroundWindowTitle
	start NVDA    standard-dontShowWelcomeDialog.ini
	logForegroundWindowTitle
	enable_verbose_debug_logging_if_requested

default teardown
	logForegroundWindowTitle
	${screenshotName}=    create_preserved_test_output_filename    failedTest.png
	Run Keyword If Test Failed    Take Screenshot    ${screenshotName}
	dump_speech_to_log
	dump_braille_to_log
	close vscode
	quit NVDA

*** Test Cases ***
VS Code status line is available
	[Documentation]    Start Visual Studio Code and ensure NVDA+end does not report "no status line found".
	vs_code_status_line_is_available
