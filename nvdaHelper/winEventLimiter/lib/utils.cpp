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

#include "stdafx.h"
#include "utils.h"
#include "eventData.h"
#include <functional>
#include <vector>

bool operator== (const EventData& lhs, const EventData& rhs) {
	return (
		lhs.idEvent == rhs.idEvent
		&& lhs.hwnd == rhs.hwnd
		&& lhs.idObject == rhs.idObject
		&& lhs.idChild == rhs.idChild
		&& lhs.dwEventThread == rhs.dwEventThread
		// do not compare dwmsEventTime meta information.
		);
}

std::size_t EventDataHasher::operator()(const EventData& e) const noexcept {
	// Combines the same fields operator== compares; dwmsEventTime is meta information.
	std::size_t seed = std::hash<DWORD>{}(e.idEvent);
	const auto combine = [&seed](std::size_t value) {
		seed ^= value + static_cast<std::size_t>(0x9e3779b97f4a7c15ull)
			+ (seed << 6) + (seed >> 2);
	};
	combine(std::hash<void*>{}(e.hwnd));
	combine(std::hash<LONG>{}(e.idObject));
	combine(std::hash<LONG>{}(e.idChild));
	combine(std::hash<DWORD>{}(e.dwEventThread));
	return seed;
}

std::wstring _getClassName(HWND hwnd) {
	constexpr int BUF_SIZE = 512;
	WCHAR buf[BUF_SIZE] = { 0 };
	GetClassNameW(hwnd, buf, BUF_SIZE);
	return std::wstring(buf);
}
