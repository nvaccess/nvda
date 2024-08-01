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

// The following structs are used to represent UI Automation event params.
// Apart from holding the params,
// each struct also contains a method for generating a comparison key
// which is used to detect and remove duplicate events.
// The key is made up of the element's runtime ID,
// plus any extra event params that make the event unique,
// E.g. event ID, property ID etc.

struct AutomationEventRecord_t {
	CComPtr<IUIAutomationElement> sender;
	EVENTID eventID;
	std::vector<int> generateCoalescingKey() const {
		auto key = getRuntimeIDFromElement(sender);
		key.push_back(eventID);
		return key;
	}
};

struct PropertyChangedEventRecord_t {
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
	CComPtr<IUIAutomationElement> sender;
	std::vector<int> generateCoalescingKey() const {
		auto key = getRuntimeIDFromElement(sender);
		key.push_back(UIA_AutomationFocusChangedEventId);
		return key;
	}
};

struct NotificationEventRecord_t {
	CComPtr<IUIAutomationElement> sender;
	NotificationKind notificationKind;
	NotificationProcessing notificationProcessing;
	CComBSTR displayString;
	CComBSTR activityID;
	std::vector<int> generateCoalescingKey() const {
		auto key = getRuntimeIDFromElement(sender);
		key.push_back(UIA_NotificationEventId);
		key.push_back(notificationKind);
		key.push_back(notificationProcessing);
		// Include the activity ID in the key also,
		// by converting it to a sequence of ints.
		if(activityID.m_str) {
			for(int c: std::wstring_view(activityID.m_str)) {
				key.push_back(c);
			}
		} else {
			key.push_back(0);
		}
		return key;
	}
};

struct ActiveTextPositionChangedEventRecord_t {
	CComPtr<IUIAutomationElement> sender;
	CComPtr<IUIAutomationTextRange> range;
	std::vector<int> generateCoalescingKey() const {
		auto key = getRuntimeIDFromElement(sender);
		key.push_back(UIA_ActiveTextPositionChangedEventId);
		return key;
	}
};

// @brief a variant type that holds all possible UI Automation event records we support.
using EventRecordVariant_t = std::variant<AutomationEventRecord_t, FocusChangedEventRecord_t, PropertyChangedEventRecord_t, NotificationEventRecord_t, ActiveTextPositionChangedEventRecord_t>;

// @brief A concept to be used with the above event record types
// that ensures the type has a generateCoalescingKey method,
// and that the type appears in the EventRecordVariant_t type.
template<typename T>
concept EventRecordConstraints = requires(T t) {
	{ t.generateCoalescingKey() } -> std::same_as<std::vector<int>>;
	// The type must be supported by the EventRecordVariant_t variant type
	 requires supports_alternative<T, EventRecordVariant_t>;
};
