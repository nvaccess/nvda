#pragma once

#include "stdafx.h"
#include <vector>
#include <string>
#include <map>

const std::wstring MOZILLA(L"Mozilla");
const std::vector<DWORD> VALID_EVENTS_FOR_NON_WINDOWS({
	EVENT_SYSTEM_SWITCHSTART,
	EVENT_SYSTEM_SWITCHEND,
	EVENT_SYSTEM_MENUEND,
	EVENT_SYSTEM_MENUPOPUPEND,
	});
const std::vector<DWORD> MENU_EVENTIDS({
	EVENT_SYSTEM_MENUSTART,
	EVENT_SYSTEM_MENUEND,
	EVENT_SYSTEM_MENUPOPUPSTART,
	EVENT_SYSTEM_MENUPOPUPEND,
	});
const std::vector<DWORD> HIDE_SHOW_REORDER({
	EVENT_OBJECT_SHOW,
	EVENT_OBJECT_HIDE,
	EVENT_OBJECT_REORDER,
	});
const std::vector<long> MENU_OBJECTS({
	OBJID_SYSMENU,
	OBJID_MENU
	});

// We never want to see foreground events for the Program Manager or Shell(task bar)
const std::vector<std::wstring> UNWANTED_FORGROUND_EVENTS({
	L"Progman",
	L"Shell_TrayWnd",
	});

constexpr DWORD IA2_EVENT_DOCUMENT_LOAD_COMPLETE = 261;
constexpr DWORD IA2_EVENT_OBJECT_ATTRIBUTE_CHANGED = 272;
constexpr DWORD IA2_EVENT_PAGE_CHANGED = 273;
constexpr DWORD IA2_EVENT_TEXT_CARET_MOVED = 283;
constexpr DWORD EVENT_OBJECT_LIVEREGIONCHANGED = 0x8019;

/*
Matches the mapping of winEvent ID's in source/IAccessibleHandler.py:
*/
static const std::map<DWORD, std::string> winEventIDsToNVDAEventNames = {
	{EVENT_SYSTEM_DESKTOPSWITCH, "desktopSwitch"},
	{EVENT_SYSTEM_FOREGROUND, "gainFocus"},
	{EVENT_SYSTEM_ALERT, "alert"},
	{EVENT_SYSTEM_MENUSTART, "menuStart"},
	{EVENT_SYSTEM_MENUEND, "menuEnd"},
	{EVENT_SYSTEM_MENUPOPUPSTART, "menuStart"},
	{EVENT_SYSTEM_MENUPOPUPEND, "menuEnd"},
	{EVENT_SYSTEM_SCROLLINGSTART, "scrollingStart"},
	// We don't need switchStart.
	{EVENT_SYSTEM_SWITCHEND, "switchEnd"},
	{EVENT_OBJECT_FOCUS, "gainFocus"},
	{EVENT_OBJECT_SHOW, "show"},
	{EVENT_OBJECT_HIDE, "hide"},
	{EVENT_OBJECT_DESTROY, "destroy"},
	{EVENT_OBJECT_DESCRIPTIONCHANGE, "descriptionChange"},
	{EVENT_OBJECT_LOCATIONCHANGE, "locationChange"},
	{EVENT_OBJECT_NAMECHANGE, "nameChange"},
	{EVENT_OBJECT_REORDER, "reorder"},
	{EVENT_OBJECT_SELECTION, "selection"},
	{EVENT_OBJECT_SELECTIONADD, "selectionAdd"},
	{EVENT_OBJECT_SELECTIONREMOVE, "selectionRemove"},
	{EVENT_OBJECT_SELECTIONWITHIN, "selectionWithIn"},
	{EVENT_OBJECT_STATECHANGE, "stateChange"},
	{EVENT_OBJECT_VALUECHANGE, "valueChange"},
	{EVENT_OBJECT_LIVEREGIONCHANGED, "liveRegionChange"},
	{IA2_EVENT_TEXT_CARET_MOVED, "caret"},
	{IA2_EVENT_DOCUMENT_LOAD_COMPLETE, "documentLoadComplete"},
	{IA2_EVENT_OBJECT_ATTRIBUTE_CHANGED, "IA2AttributeChange"},
	{IA2_EVENT_PAGE_CHANGED, "pageChange"},
};

static const std::vector<DWORD> _createSortedEventIds() {
	std::vector<DWORD> eventIds;
	for (auto& [id, name] : winEventIDsToNVDAEventNames) {
		eventIds.push_back(id);
	}
	std::sort(eventIds.begin(), eventIds.end());
	return eventIds;
}
static const auto EVENT_IDS_TO_ACCEPT = _createSortedEventIds();