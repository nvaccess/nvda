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

// WinEventLogger.cpp : This file contains the 'main' function. Program execution begins and ends there.

#include "pch.h"
#include <iostream>
#include <string>
#include <iomanip>
#include <map>
#include <ostream>
#include <sstream>
#include <future>
#include <thread>
#include <vector>
#include <chrono>

#include <winEventLimiterDll.h>
#include <Windows.h>

namespace {

constexpr DWORD IA2_EVENT_DOCUMENT_LOAD_COMPLETE = 261;
constexpr DWORD IA2_EVENT_OBJECT_ATTRIBUTE_CHANGED = 272;
constexpr DWORD IA2_EVENT_PAGE_CHANGED = 273;
constexpr DWORD IA2_EVENT_TEXT_CARET_MOVED = 283;
#ifndef EVENT_OBJECT_LIVEREGIONCHANGED
// Not defined in Windows SDK headers before 10.0.14393
constexpr DWORD EVENT_OBJECT_LIVEREGIONCHANGED = 0x8019;
#endif

// Display names for winEvent IDs, and the set of IDs this tool hooks.
// NVDA uses the mapping at source/IAccessibleHandler/internalWinEventHandler.py, which it passes to
// winEventLimiter_start; this copy only serves this standalone diagnostic tool.
const std::map<DWORD, std::string> eventIdsToNames = {
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

std::string getEventName(DWORD eventID) {
	const auto itr = eventIdsToNames.find(eventID);
	return itr != eventIdsToNames.end() ? itr->second : "";
}

}  // namespace

HWND doCreateWindow();
void blocking_messagePump();

std::atomic<bool> g_keepPrinting = true;
std::atomic<bool> g_glitch = false;
void printFromBuffer();
void printEvent(unsigned int eventIndex, bool fromDestroyBuffer = false);


void onNewEvent(int includesFocusEvent) {
	// Callback from the winEventLimiter dll
}

int main() {
	std::cout << "Starting\n";
	std::vector<DWORD> eventIds;
	eventIds.reserve(eventIdsToNames.size());
	for (const auto& [id, name] : eventIdsToNames) {
		eventIds.push_back(id);
	}
	winEventLimiter_start(onNewEvent, eventIds.data(), static_cast<unsigned int>(eventIds.size()));
	auto printThread = std::thread(printFromBuffer);
	doCreateWindow();
	blocking_messagePump();
	g_keepPrinting = false; // stops the print thread.
	printThread.join();
	winEventLimiter_stop();
	return 0;
}

void printFromBuffer() {
	while (g_keepPrinting) {
		std::cout << "-- flush --" << '\n';
		winEventLimiter_flushDestroyEvents();
		winEventLimiter_flushEvents();
		const auto numDestroys = winEventLimiter_getDestroyEventCount();
		for (auto i = 0u; i < numDestroys; ++i) {
			std::cout << "Destroy: ";
			printEvent(i, true);
		}
		if (g_glitch.exchange(false)) {
			auto numEvents = winEventLimiter_getEventCount();
			std::cout << "Glitch Event: ";
			printEvent(numEvents+1);
		}
		else {
			auto numEvents = winEventLimiter_getEventCount();
			for (auto i = 0u; i < numEvents; ++i) {
				printEvent(i);
			}
		}

		using namespace std::chrono_literals;
		std::this_thread::sleep_for(100ms); // mimic cadence of updates from NVDA
	}
}

void printEvent(unsigned int eventIndex, bool fromDestroyBuffer) {
	EventData e;
	std::stringstream sstream;
	auto constexpr MAX_EVENTS = 1u;
	const auto gotCount = fromDestroyBuffer
		? winEventLimiter_getDestroyEvents(eventIndex, MAX_EVENTS, &e)
		: winEventLimiter_getEvents(eventIndex, MAX_EVENTS, &e);
	if (0u < gotCount && gotCount <= MAX_EVENTS) {
		const auto eName = getEventName(e.idEvent);
		sstream << std::hex << std::showbase <<
			" eventID: " << e.idEvent <<
			" eventName: " << eName <<
			" hwnd: " << e.hwnd <<
			" idObject: " << e.idObject <<
			" idChild: " << e.idChild <<
			" eventThread: " << e.dwEventThread <<
			" eventTime: " << e.dwmsEventTime
			<< '\n';
	}
	else {
		const auto eCount = fromDestroyBuffer
			? winEventLimiter_getDestroyEventCount()
			: winEventLimiter_getEventCount();
		sstream << "failed to get event at index: " << eventIndex << " from outBuffer with size: " << eCount << '\n';
	}
	std::cout << sstream.str();
}

LRESULT CALLBACK WndProc(HWND hwnd, UINT message, WPARAM wparam, LPARAM lparam) {
	switch (message) {
	case WM_CHAR:
		if (wparam == VK_ESCAPE) {
			DestroyWindow(hwnd);
		}
		if (wparam == 'g') {
			g_glitch = true;
		}
		break;
	case WM_DESTROY:
		PostQuitMessage(0);
		break;
	}
	return DefWindowProc(hwnd, message, wparam, lparam);
}

HWND doCreateWindow() {
	WNDCLASS windowClass = { 0 };
	windowClass.hbrBackground = static_cast<HBRUSH>(GetStockObject(WHITE_BRUSH));
	windowClass.hCursor = LoadCursor(nullptr, IDC_ARROW);
	windowClass.hInstance = nullptr;
	windowClass.lpfnWndProc = WndProc;
	windowClass.lpszClassName = L"Window in Console"; //needs to be the same name when creating the window as well
	windowClass.style = CS_HREDRAW | CS_VREDRAW;
	//also register the class
	if (!RegisterClass(&windowClass)) {
		std::cout << "Could not register class\n";
		exit(-1);
	}

	HWND windowHandle = CreateWindow(
		L"Window in Console", // lpClassName
		nullptr, // lpWindowName
		WS_OVERLAPPEDWINDOW, // dwStyle
		// coordinate of window start point
		0, // x
		0, // y
		// window size
		500, // width
		100, // height
		nullptr, // hWndParent
		nullptr, // hMenu
		nullptr, // hInstance
		nullptr // lpParam
	);
	ShowWindow(windowHandle, SW_RESTORE);
	return windowHandle;
}

void blocking_messagePump() {
	// Keep this app running until we're told to stop
	MSG msg;
	while (0 < GetMessage(&msg, NULL, NULL, NULL)
		) {
		TranslateMessage(&msg);
		DispatchMessage(&msg);
	}
}
