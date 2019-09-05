#pragma once
#include "stdafx.h"
#include <optional>
#include <mutex>
#include "eventData.h"

constexpr unsigned int MAX_FOREGROUND_DEFERS = 2;
class DeferredForegourndWindowEventHandler {

public:
	struct DeferUntilHwndForeground {
		HWND hwnd;
		unsigned int deferCount;
	};

	void Track(EventData& e);

	bool ShouldDeferEvents();

private:
	std::mutex m_deferMutex;
	std::optional<DeferUntilHwndForeground> m_deferUntilForegroundWindow;
};
