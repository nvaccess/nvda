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

using AnyEventRecord_t = std::variant<AutomationEventRecord_t, FocusChangedEventRecord_t, PropertyChangedEventRecord_t, NotificationEventRecord_t, ActiveTextPositionChangedEventRecord_t>;

template<typename T>
concept EventRecordConstraints = requires(T t) {
	{ t.isCoalesceable } -> std::same_as<const bool&>;
	requires (T::isCoalesceable == false) || requires(T t) {
		{ t.generateCoalescingKey() } -> std::same_as<std::vector<int>>;
	};
	{ AnyEventRecord_t(t)} -> std::same_as<AnyEventRecord_t>;
};
