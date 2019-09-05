#pragma once
#include "stdafx.h"
#include <vector>

struct EventData {
	DWORD idEvent;
	HWND hwnd;
	LONG idObject;
	LONG idChild;
	DWORD dwEventThread;
	DWORD dwmsEventTime;
};
using EventBuffer = std::vector<EventData>;

bool operator == (const EventData& lhs, const EventData & rhs);