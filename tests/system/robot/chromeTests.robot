# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2019 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html
*** Settings ***
Documentation	HTML test cases in Chrome
Force Tags	NVDA	smoke test	browser	chrome

# for start & quit in Test Setup and Test Test Teardown
Library	NvdaLib.py
# for test cases
Library	chromeTests.py

Test Setup	start NVDA	standard-dontShowWelcomeDialog.ini
Test Teardown	quit NVDA

*** Test Cases ***

checkbox labelled by inner element
	[Documentation]	A checkbox labelled by an inner element should not read the label element twice.
	# Excluded due to intermittent failure: #11053
	[Tags]	excluded_from_build
	checkbox_labelled_by_inner_element
