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
#include <cstddef>
#include <vector>

struct EventData {
	DWORD idEvent;
	HWND hwnd;
	LONG idObject;
	LONG idChild;
	DWORD dwEventThread;
	DWORD dwmsEventTime;
	// Events explicitly injected by NVDA have already been selected for delivery and
	// must match the in-process limiter, which does not apply hook-event preprocessing.
	bool bypassesPreprocessing = false;
};
using EventBuffer = std::vector<EventData>;

// The focused object (#11520): its events are exempt from the per thread limit and are
// preferred survivors of the overflow trims. All consumers treat all zeros as cleared.
struct AlwaysAllowedObject {
	HWND hwnd;
	LONG idObject;
	LONG idChild;
};

bool operator == (const EventData& lhs, const EventData & rhs);

// Hasher for EventData, consistent with operator==: dwmsEventTime is deliberately excluded.
struct EventDataHasher {
	std::size_t operator()(const EventData& e) const noexcept;
};
