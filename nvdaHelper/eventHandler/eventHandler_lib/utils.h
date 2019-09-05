#pragma once

#include "stdafx.h"

#include <map>
#include <vector>
#include <algorithm>


template <typename T>
bool _in(const T& value, const std::vector<T>& container);

template <typename T, typename U>
bool _in(const T& value, const std::map<T, U>& container);

bool _startsWith(const std::wstring &str, const std::wstring &substr);

const std::string getEventName(DWORD eventID);

LONG _getWindowStyle(HWND hwnd);

std::wstring _getClassName(HWND hwnd);

