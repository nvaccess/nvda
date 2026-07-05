/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2019-2026 NV Access Limited, Bill Dengler
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 2.0, as published by
the Free Software Foundation.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#pragma once

#include "stdafx.h"
#include <vector>
#include <string>

inline const std::vector<DWORD> VALID_EVENTS_FOR_NON_WINDOWS({
	EVENT_SYSTEM_SWITCHSTART,
	EVENT_SYSTEM_SWITCHEND,
	EVENT_SYSTEM_MENUEND,
	EVENT_SYSTEM_MENUPOPUPEND,
	});
inline const std::vector<DWORD> MENU_EVENTIDS({
	EVENT_SYSTEM_MENUSTART,
	EVENT_SYSTEM_MENUEND,
	EVENT_SYSTEM_MENUPOPUPSTART,
	EVENT_SYSTEM_MENUPOPUPEND,
	});
inline const std::vector<long> MENU_OBJECTS({
	OBJID_SYSMENU,
	OBJID_MENU
	});

// We never want to see foreground events for the Program Manager or Shell(task bar)
inline const std::vector<std::wstring> UNWANTED_FOREGROUND_EVENTS({
	L"Progman",
	L"Shell_TrayWnd",
	});
