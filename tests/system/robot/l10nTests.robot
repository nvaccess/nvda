# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

*** Settings ***
Documentation	Localization startup tests
Force Tags	NVDA	smoke test	l10n

Library	NvdaLib.py
Library	l10nTests.py

Test Teardown	Run Keyword And Ignore Error	quit NVDA

*** Test Cases ***

Starts with every source locale
	[Documentation]	Ensure NVDA starts successfully with each language found under source/locale.
	@{localeCodes}=	Get Source Locale Codes
	@{failedLocales}=	Create List
	FOR	${localeCode}	IN	@{localeCodes}
		Log	Testing NVDA startup with language: ${localeCode}
		${startStatus}	${startMessage}=	Run Keyword And Ignore Error	start NVDA	standard-dontShowWelcomeDialog.ini	language=${localeCode}
		Run Keyword If	"${startStatus}"=="FAIL"	Run Keyword And Ignore Error	quit NVDA
		@{failedLocales}=	Run Keyword If	"${startStatus}"=="FAIL"	Append Failed Locale	${failedLocales}	${localeCode}	${startMessage}	ELSE	Set Variable	${failedLocales}
		Run Keyword If	"${startStatus}"=="FAIL"	Log	NVDA failed to start for locale: ${localeCode}. Error: ${startMessage}	ERROR
		quit NVDA
	END
	${failedCount}=	Get Length	${failedLocales}
	Run Keyword If	${failedCount} > 0	Fail	NVDA failed to start for the following locales: ${failedLocales}
