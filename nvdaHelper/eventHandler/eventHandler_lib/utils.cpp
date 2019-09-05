#include "stdafx.h"
#include "utils.h"
#include "eventData.h"
#include "internalConstants.h"
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

template <typename T>
bool _in(const T& value, const std::vector<T>& container) {
	const auto itr = std::find(
		container.cbegin(),
		container.cend(),
		value
	);
	return itr != container.cend();
}

template <typename T, typename U>
bool _in(T& value, const std::map<T, U>& container) {
	return container.find(value) != container.cend();
}

bool _test() {
	std::vector<unsigned long> v = { 1L, 2L, 3L };
	auto is = _in<unsigned long>(2, v);


	std::vector<long> v2 = { 1L, 2L, 3L };
	auto isit = _in<long>(2L, v2);
	return  false;
}

bool _startsWith(const std::wstring & str, const std::wstring & substr) {
	return str.compare(0, substr.length(), substr) == 0;
}

const std::string getEventName(DWORD eventID) {
	if (_in(eventID, winEventIDsToNVDAEventNames)) {
		return winEventIDsToNVDAEventNames.at(eventID);
	}
	return "";
}

LONG _getWindowStyle(HWND hwnd) {
	return GetWindowLongW(hwnd, GWL_STYLE);
}

std::wstring _getClassName(HWND hwnd) {
	constexpr int BUF_SIZE = 512;
	WCHAR buf[BUF_SIZE] = { 0 };
	GetClassNameW(hwnd, buf, BUF_SIZE);
	return std::wstring(buf);
}

