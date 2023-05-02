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

#include <windows.h>
#include <uiautomation.h>
#include <numeric>
#include <variant>
#include <map>
#include <vector>
#include <functional>
#include <mutex>
#include <atomic>
#include <atlcomcli.h>
#include <comutil.h>
#include <common/log.h>
#include "eventRecord.h"
#include "rateLimitedEventHandler.h"

template<EventRecordConstraints EventRecordClass, typename... EventRecordArgTypes>
HRESULT RateLimitedEventHandler::queueEvent(EventRecordArgTypes&&... args) {
	LOG_DEBUG(L"RateLimitedUIAEventHandler::queueEvent called");
	FlushRequest flushRequest = FlushRequest::none;
	unsigned int flushTimeMS = 0;
	{ std::lock_guard lock(mtx);
		// work out whether we need to request a flush after inserting this event.
		if(!EventRecordClass::isCoalesceable) {
			// not a coalesceable event so requires a quick flush
			// if a quick flush has not been requested already.
			if(lastFlushRequest < FlushRequest::quick) {
				LOG_DEBUG(L"RateLimitedUIAEventHandler::queueEvent: requesting quick flush after queuing");
				lastFlushRequest = flushRequest = FlushRequest::quick;
			} else {
				LOG_DEBUG(L"RateLimitedUIAEventHandler::queueEvent: quick flush needed, but quick flush already requested.");
			}
		} else if(m_eventRecords.empty()) {
			// It is a coalesceable event and its the first event since the last flush,
			// so requires a delayed flush
			// if a delayed or quick flush is not requested already.
			if(lastFlushRequest < FlushRequest::delayed) {
				LOG_DEBUG(L"RateLimitedUIAEventHandler::queueEvent: requesting delayed flush after queuing");
				lastFlushRequest = flushRequest = FlushRequest::delayed;
				flushTimeMS = 30;
			} else {
				LOG_DEBUG(L"RateLimitedUIAEventHandler::queueEvent: delayed flush needed, but quick flush already requested.");
			}
		}
		LOG_DEBUG(L"RateLimitedUIAEventHandler::queueEvent: Inserting new event");
		auto& recordVar = m_eventRecords.emplace_back(std::in_place_type_t<EventRecordClass>{}, args...);
		auto recordVarIter = m_eventRecords.end();
		recordVarIter--;
		auto& record = std::get<EventRecordClass>(recordVar);
		if constexpr(EventRecordClass::isCoalesceable) {
			LOG_DEBUG(L"RateLimitedUIAEventHandler::queueEvent: Is a coalesceable event");
			auto coalescingKey = record.generateCoalescingKey();
			auto existingKeyIter = m_eventRecordsByKey.find(coalescingKey);
			if(existingKeyIter != m_eventRecordsByKey.end()) {
				LOG_DEBUG(L"RateLimitedUIAEventHandler::queueEvent: found existing event with same key"); 
				auto& [existingRecordVarIter,existingCoalesceCount] = existingKeyIter->second;
				LOG_DEBUG(L"RateLimitedUIAEventHandler::queueEvent: updating key and count to "<<(existingCoalesceCount+1));
				existingKeyIter->second = {recordVarIter, existingCoalesceCount + 1};
				LOG_DEBUG(L"RateLimitedUIAEventHandler::queueEvent: erasing old item"); 
				m_eventRecords.erase(existingRecordVarIter);
			} else {
				LOG_DEBUG(L"RateLimitedUIAEventHandler::queueEvent: Adding key");
				m_eventRecordsByKey.insert_or_assign(coalescingKey, std::pair(recordVarIter, 1));
			}
		}
	}
	if(flushRequest > FlushRequest::none) {
		LOG_DEBUG(L"RateLimitedUIAEventHandler::queueEvent: posting flush message with delay of "<<flushTimeMS);
		PostMessage(m_messageWindow, m_flushMessage, reinterpret_cast<WPARAM>(this), flushTimeMS);
	}
	return S_OK;
}

HRESULT RateLimitedEventHandler::emitEvent(const AutomationEventRecord_t& record) const {
	LOG_DEBUG(L"RateLimitedUIAEventHandler::emitAutomationEvent called");
	if(!m_pExistingAutomationEventHandler) {
		LOG_ERROR(L"RateLimitedUIAEventHandler::emitAutomationEvent: interface not supported.");
		return E_NOINTERFACE;
	}
	LOG_DEBUG(L"Emitting automationEvent for eventID "<<record.eventID);
	return m_pExistingAutomationEventHandler->HandleAutomationEvent(record.sender, record.eventID);
}

HRESULT RateLimitedEventHandler::emitEvent(const FocusChangedEventRecord_t& record) const {
	LOG_DEBUG(L"RateLimitedUIAEventHandler::emitFocusChangedEvent called");
	if(!m_pExistingFocusChangedEventHandler) {
		LOG_ERROR(L"RateLimitedUIAEventHandler::emitFocusChangedEvent: interface not supported.");
		return E_NOINTERFACE;
	}
	return m_pExistingFocusChangedEventHandler->HandleFocusChangedEvent(record.sender);
}

HRESULT RateLimitedEventHandler::emitEvent(const PropertyChangedEventRecord_t& record) const {
	LOG_DEBUG(L"RateLimitedUIAEventHandler::emitPropertyChangedEvent called");
	if(!m_pExistingPropertyChangedEventHandler) {
		LOG_ERROR(L"RateLimitedUIAEventHandler::emitPropertyChangedEvent: interface not supported.");
		return E_NOINTERFACE;
	}
	return m_pExistingPropertyChangedEventHandler->HandlePropertyChangedEvent(record.sender, record.propertyID, record.newValue);
}

HRESULT RateLimitedEventHandler::emitEvent(const NotificationEventRecord_t& record) const {
	LOG_DEBUG(L"RateLimitedUIAEventHandler::emitNotificationEvent called");
	if(!m_pExistingNotificationEventHandler) {
		LOG_ERROR(L"RateLimitedUIAEventHandler::emitNotificationChangedEvent: interface not supported.");
		return E_NOINTERFACE;
	}
	return m_pExistingNotificationEventHandler->HandleNotificationEvent(record.sender, record.notificationKind, record.notificationProcessing, record.displayString, record.activityID);
}

HRESULT RateLimitedEventHandler::emitEvent(const ActiveTextPositionChangedEventRecord_t& record) const {
	LOG_DEBUG(L"RateLimitedUIAEventHandler::emitActiveTextPositionChangedEvent called");
	if(!m_pExistingActiveTextPositionChangedEventHandler) {
		LOG_ERROR(L"RateLimitedUIAEventHandler::emitActiveTextPositionChangedEvent: interface not supported.");
		return E_NOINTERFACE;
	}
	return m_pExistingActiveTextPositionChangedEventHandler->HandleActiveTextPositionChangedEvent(record.sender, record.range);
}

RateLimitedEventHandler::~RateLimitedEventHandler() {
	LOG_DEBUG(L"RateLimitedUIAEventHandler::~RateLimitedUIAEventHandler called");
}

RateLimitedEventHandler::RateLimitedEventHandler(IUnknown* pExistingHandler, HWND messageWindow, UINT flushMessage)
	: m_messageWindow(messageWindow), m_flushMessage(flushMessage), m_refCount(1), m_pExistingAutomationEventHandler(pExistingHandler), m_pExistingFocusChangedEventHandler(pExistingHandler), m_pExistingPropertyChangedEventHandler(pExistingHandler), m_pExistingNotificationEventHandler(pExistingHandler), m_pExistingActiveTextPositionChangedEventHandler(pExistingHandler) {
	LOG_DEBUG(L"RateLimitedUIAEventHandler::RateLimitedUIAEventHandler called");
}

// IUnknown methods
ULONG STDMETHODCALLTYPE RateLimitedEventHandler::AddRef() {
	return InterlockedIncrement(&m_refCount);
}

ULONG STDMETHODCALLTYPE RateLimitedEventHandler::Release() {
	ULONG refCount = InterlockedDecrement(&m_refCount);
	if (refCount == 0) {
		delete this;
	}
	return refCount;
}

HRESULT STDMETHODCALLTYPE RateLimitedEventHandler::QueryInterface(REFIID riid, void** ppInterface) {
	if (riid == __uuidof(IUnknown)) {
		*ppInterface = static_cast<IUIAutomationEventHandler*>(this);
		AddRef();
		return S_OK;
	} else if (riid == __uuidof(IUIAutomationEventHandler)) {
		*ppInterface = static_cast<IUIAutomationEventHandler*>(this);
		AddRef();
		return S_OK;
	} else if (riid == __uuidof(IUIAutomationFocusChangedEventHandler)) {
		*ppInterface = static_cast<IUIAutomationFocusChangedEventHandler*>(this);
		AddRef();
		return S_OK;
	} else if (riid == __uuidof(IUIAutomationPropertyChangedEventHandler)) {
		*ppInterface = static_cast<IUIAutomationPropertyChangedEventHandler*>(this);
		AddRef();
		return S_OK;
	} else if (riid == __uuidof(IUIAutomationNotificationEventHandler)) {
		*ppInterface = static_cast<IUIAutomationNotificationEventHandler*>(this);
		AddRef();
		return S_OK;
	} else if (riid == __uuidof(IUIAutomationActiveTextPositionChangedEventHandler)) {
		*ppInterface = static_cast<IUIAutomationActiveTextPositionChangedEventHandler*>(this);
		AddRef();
		return S_OK;
	}
	*ppInterface = nullptr;
	return E_NOINTERFACE;
}

// IUIAutomationEventHandler method
HRESULT STDMETHODCALLTYPE RateLimitedEventHandler::HandleAutomationEvent(IUIAutomationElement* sender, EVENTID eventID) {
	LOG_DEBUG(L"RateLimitedUIAEventHandler::HandleAutomationEvent called");
	LOG_DEBUG(L"Queuing automationEvent for eventID "<<eventID);
	return queueEvent<AutomationEventRecord_t>(sender, eventID);
}

// IUIAutomationFocusEventHandler method
HRESULT STDMETHODCALLTYPE RateLimitedEventHandler::HandleFocusChangedEvent(IUIAutomationElement* sender) {
	LOG_DEBUG(L"RateLimitedUIAEventHandler::HandleFocusChangedEvent called");
	return queueEvent<FocusChangedEventRecord_t>(sender);
}

// IUIAutomationPropertyChangedEventHandler method
HRESULT STDMETHODCALLTYPE RateLimitedEventHandler::HandlePropertyChangedEvent(IUIAutomationElement* sender, PROPERTYID propertyID, VARIANT newValue) {
	LOG_DEBUG(L"RateLimitedUIAEventHandler::HandlePropertyChangedEvent called");
	return queueEvent<PropertyChangedEventRecord_t>(sender, propertyID, newValue);
}

// IUIAutomationNotificationEventHandler method
HRESULT STDMETHODCALLTYPE RateLimitedEventHandler::HandleNotificationEvent(IUIAutomationElement* sender, NotificationKind notificationKind, NotificationProcessing notificationProcessing, BSTR displayString, BSTR activityID) {
	LOG_DEBUG(L"RateLimitedUIAEventHandler::HandleNotificationEvent called");
	return queueEvent<NotificationEventRecord_t>(sender, notificationKind, notificationProcessing, displayString, activityID);
}

// IUIAutomationActiveTextPositionchangedEventHandler method
HRESULT STDMETHODCALLTYPE RateLimitedEventHandler::HandleActiveTextPositionChangedEvent(IUIAutomationElement* sender, IUIAutomationTextRange* range) {
	LOG_DEBUG(L"RateLimitedUIAEventHandler::HandleActiveTextPositionChangedEvent called");
	return queueEvent<ActiveTextPositionChangedEventRecord_t>(sender, range);
}

void RateLimitedEventHandler::flush() {
	LOG_DEBUG(L"RateLimitedUIAEventHandler::flush called");
	decltype(m_eventRecords) eventRecordsCopy;
	decltype(m_eventRecordsByKey) eventRecordsByKeyCopy;
	{ std::lock_guard lock(mtx);
		eventRecordsCopy.swap(m_eventRecords);
		eventRecordsByKeyCopy.swap(m_eventRecordsByKey);
		lastFlushRequest = FlushRequest::none;
	}

	// Emit events
	LOG_DEBUG(L"RateLimitedUIAEventHandler::flush: Emitting events...");
	for(const auto& recordVar: eventRecordsCopy) {
		std::visit([this](const auto& record) {
			this->emitEvent(record);
		}, recordVar);
	}
	/*
	unsigned int count = std::accumulate(eventRecordsByKeyCopy.begin(), eventRecordsByKeyCopy.end(), 0, [](const auto& acc, const auto& i) {
		auto count = i.second.second;
		if(count > 1) {
			return acc + count;
		}
		return acc;
	});
	if(count > 0) {
		Beep(440 + (count*10), 40);
	}
	*/
	LOG_DEBUG(L"RateLimitedUIAEventHandler::flush: done emitting events"); 
}
