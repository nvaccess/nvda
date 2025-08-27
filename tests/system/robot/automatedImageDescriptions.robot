# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Tianze
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html
*** Settings ***
Documentation	Local captioner tests
Force Tags	NVDA	smoke test	imageDescriptions

Library	NvdaLib.py
Library	automatedImageDescriptions.py
Library	ScreenCapLibrary

Test Setup	start NVDA	standard-doLoadMockModel.ini
Test Teardown	default teardown

*** Keywords ***
default teardown
	${screenshotName}=	create_preserved_test_output_filename	failedTest.png
	Run Keyword If Test Failed	Take Screenshot	${screenShotName}
	quit NVDA

*** Test Cases ***
automatedImageDescriptions
	[Documentation]	Ensure that local captioner work
	[Setup]	start NVDA	standard-doLoadMockModel.ini
	NVDA_Caption	# run test

