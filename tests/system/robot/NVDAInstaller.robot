# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html
*** Settings ***
Documentation	Smoke test the installation process
Force Tags	smoke test	installer
Suite Setup	Run Keyword If	not r'${installDir}'	Fail	"--installDir not supplied"

# for start & quit in Test Setup and Test Teardown
Library	NvdaLib.py
Library	NVDAInstaller.py
Library	ScreenCapLibrary

Test Setup	default startup
Test Teardown	default teardown

*** Keywords ***

default teardown
	${screenshotName}=	create_preserved_test_output_filename	failedTest.png
	Run Keyword If Test Failed	Take Screenshot	${screenShotName}
	quit NVDAInstaller

default startup
	start NVDAInstaller	standard-dontShowWelcomeDialog.ini

default pass execution

*** Test Cases ***

Read install dialog
	[Documentation]	Ensure that the install dialog can be read in full
	read_install_dialog	# run test

Read install dialog portable copy
	[Documentation]	Ensure that the portable copy install dialog can be read in full
	read_portable_copy_dialog	# run test
