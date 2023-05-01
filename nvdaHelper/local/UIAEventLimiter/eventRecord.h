/*
This file is a part of the NVDA project.
URL: http://github.com/nvaccess/nvda/
Copyright 2023 NV Access Limited.
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

#include <vector>
#include <variant>
#include <atlcomcli.h>
#include <UIAutomation.h>
#include "utils.h"

struct AutomationEventRecord_t {
	static const bool isCoalesceable = true;
	CComPtr<IUIAutomationElement> sender;
	EVENTID eventID;
	std::vector<int> generateCoalescingKey() const {
		auto key = getRuntimeIDFromElement(sender);
		key.push_back(eventID);
		return key;
	}
};

struct PropertyChangedEventRecord_t {
	static const bool isCoalesceable = true;
	CComPtr<IUIAutomationElement> sender;
	PROPERTYID propertyID;
	CComVariant newValue;
	std::vector<int> generateCoalescingKey() const {
		auto key = getRuntimeIDFromElement(sender);
		key.push_back(UIA_AutomationPropertyChangedEventId);
		key.push_back(propertyID);
		return key;
	}
};

struct FocusChangedEventRecord_t {
	static const bool isCoalesceable = false;
	CComPtr<IUIAutomationElement> sender;
};

struct NotificationEventRecord_t {
	static const bool isCoalesceable = false;
	CComPtr<IUIAutomationElement> sender;
	NotificationKind notificationKind;
	NotificationProcessing notificationProcessing;
	CComBSTR displayString;
	CComBSTR activityID;
};

struct ActiveTextPositionChangedEventRecord_t {
	static const bool isCoalesceable = false;
	CComPtr<IUIAutomationElement> sender;
	CComPtr<IUIAutomationTextRange> range;
};

using EventRecordVariant_t = std::variant<AutomationEventRecord_t, FocusChangedEventRecord_t, PropertyChangedEventRecord_t, NotificationEventRecord_t, ActiveTextPositionChangedEventRecord_t>;

template<typename T>
concept EventRecordConstraints = requires(T t) {
	// type must have a static const bool member called 'isCoalesceable'
	{ t.isCoalesceable } -> std::same_as<const bool&>;
	// if 'isCoaleseable' is true, then the type must have a 'generateCoalescingKey' method.
	requires (T::isCoalesceable == false) || requires(T t) {
		{ t.generateCoalescingKey() } -> std::same_as<std::vector<int>>;
	};
	// The type must be supported by the EventRecordVariant_t variant type
	 requires supports_alternative<T, EventRecordVariant_t>;
};
