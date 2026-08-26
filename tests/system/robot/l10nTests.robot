# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

*** Settings ***
Documentation	Localization startup tests
Force Tags	NVDA	smoke test	l10n

Library	NvdaLib.py
Library	l10nTests.py

*** Test Cases ***

Starts with every source locale
	[Documentation]	Ensure NVDA starts successfully with each language found under source/locale.
	NVDA starts for all locales
