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
	bool needsFlush = false;
	{ // scoped lock
		std::lock_guard lock(m_mtx);
		// work out whether we need to request a flush after inserting this event.
		needsFlush = m_eventRecords.empty();
		LOG_DEBUG(L"RateLimitedUIAEventHandler::queueEvent: Inserting new event");
		auto& recordVar = m_eventRecords.emplace_back(std::in_place_type_t<EventRecordClass>{}, args...);
		auto recordVarIter = m_eventRecords.end();
		recordVarIter--;
		auto& record = std::get<EventRecordClass>(recordVar);
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
		if(needsFlush) {
			LOG_DEBUG(L"RateLimitedUIAEventHandler::queueEvent: requesting flush");
			m_needsFlush = true;
			m_flushConditionVar.notify_one();
		}
	} // m_mtx released. 
	return S_OK;
}

void RateLimitedEventHandler::flusherThreadFunc(std::stop_token stopToken) {
	LOG_DEBUG(L"flusherThread started");
	// If this thread is requested to stop, we need to ensure we wake up.
	std::stop_callback stopCallback{stopToken, [this](){
		LOG_DEBUG(L"flusherThreadFunc stop callback: stop requested")
		this->m_flushConditionVar.notify_all();
	}};
	do { // thread main loop
		bool needsFlush = false;
		{ std::unique_lock lock(m_mtx);
			// sleep until a flush is needed or this thread should stop.
			LOG_DEBUG(L"flusherThreadFunc sleeping...");
			m_flushConditionVar.wait(lock, [this, stopToken](){
				LOG_DEBUG(L"FLUSHER THREAD notified, CHECKING WAKE CONDITION");
				if (this->m_needsFlush) {
					LOG_DEBUG(L"Will wake as needsFlush is true");
					return true;
				} else if (stopToken.stop_requested()) {
					LOG_DEBUG(L"Will wake as stop requested");
					return true;
				}
				LOG_DEBUG(L"Spurious wake, will sleep again");
				return false;
			});
			LOG_DEBUG(L"flusherThread woke up");
			if (this->m_needsFlush) {
				m_needsFlush = false;
				needsFlush = true;
			}
		} // m_mtx released here.
		if (needsFlush) {
			LOG_DEBUG(L"flusherThreadFunc: Flushing events...");
			flushEvents();
		}
	} while(!stopToken.stop_requested());
	LOG_DEBUG(L"flusherThread returning as stop requested");
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
	LOG_DEBUG(L"Emitting focus changed event");
	return m_pExistingFocusChangedEventHandler->HandleFocusChangedEvent(record.sender);
}

HRESULT RateLimitedEventHandler::emitEvent(const PropertyChangedEventRecord_t& record) const {
	LOG_DEBUG(L"RateLimitedUIAEventHandler::emitPropertyChangedEvent called");
	if(!m_pExistingPropertyChangedEventHandler) {
		LOG_ERROR(L"RateLimitedUIAEventHandler::emitPropertyChangedEvent: interface not supported.");
		return E_NOINTERFACE;
	}
	LOG_DEBUG(L"Emitting property changed event for property "<<(record.propertyID));
	return m_pExistingPropertyChangedEventHandler->HandlePropertyChangedEvent(record.sender, record.propertyID, record.newValue);
}

HRESULT RateLimitedEventHandler::emitEvent(const NotificationEventRecord_t& record) const {
	LOG_DEBUG(L"RateLimitedUIAEventHandler::emitNotificationEvent called");
	if(!m_pExistingNotificationEventHandler) {
		LOG_ERROR(L"RateLimitedUIAEventHandler::emitNotificationChangedEvent: interface not supported.");
		return E_NOINTERFACE;
	}
	LOG_DEBUG(L"Emitting notification event");
	return m_pExistingNotificationEventHandler->HandleNotificationEvent(record.sender, record.notificationKind, record.notificationProcessing, record.displayString, record.activityID);
}

HRESULT RateLimitedEventHandler::emitEvent(const ActiveTextPositionChangedEventRecord_t& record) const {
	LOG_DEBUG(L"RateLimitedUIAEventHandler::emitActiveTextPositionChangedEvent called");
	if(!m_pExistingActiveTextPositionChangedEventHandler) {
		LOG_ERROR(L"RateLimitedUIAEventHandler::emitActiveTextPositionChangedEvent: interface not supported.");
		return E_NOINTERFACE;
	}
	LOG_DEBUG(L"Emitting active text position changed event");
	return m_pExistingActiveTextPositionChangedEventHandler->HandleActiveTextPositionChangedEvent(record.sender, record.range);
}

RateLimitedEventHandler::~RateLimitedEventHandler() {
	LOG_DEBUG(L"RateLimitedUIAEventHandler::~RateLimitedUIAEventHandler called");
}

RateLimitedEventHandler::RateLimitedEventHandler(IUnknown* pExistingHandler):
	m_pExistingAutomationEventHandler(pExistingHandler),
	m_pExistingFocusChangedEventHandler(pExistingHandler), 
	m_pExistingPropertyChangedEventHandler(pExistingHandler),
	m_pExistingNotificationEventHandler(pExistingHandler), 
	m_pExistingActiveTextPositionChangedEventHandler(pExistingHandler),
	m_flusherThread([this](std::stop_token st){ this->flusherThreadFunc(st); })
{
	LOG_DEBUG(L"RateLimitedUIAEventHandler::RateLimitedUIAEventHandler called");
}

// IUnknown methods
ULONG STDMETHODCALLTYPE RateLimitedEventHandler::AddRef() {
	auto refCount = InterlockedIncrement(&m_refCount);
	LOG_DEBUG(L"AddRef: "<<refCount)
	return refCount;
}

ULONG STDMETHODCALLTYPE RateLimitedEventHandler::Release() {
	auto refCount = InterlockedDecrement(&m_refCount);
	if (refCount == 0) {
		delete this;
	}
	LOG_DEBUG(L"Release: "<<refCount)
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

void RateLimitedEventHandler::flushEvents() {
	LOG_DEBUG(L"RateLimitedEventHandler::flushEvents called");
	decltype(m_eventRecords) eventRecordsCopy;
	decltype(m_eventRecordsByKey) eventRecordsByKeyCopy;
	{ std::lock_guard lock{m_mtx};
		eventRecordsCopy.swap(m_eventRecords);
		eventRecordsByKeyCopy.swap(m_eventRecordsByKey);
	} // m_mtx released here.
	// Emit events
	LOG_DEBUG(L"RateLimitedUIAEventHandler::flusherThreadFunc: Emitting events...");
	for(const auto& recordVar: eventRecordsCopy) {
		std::visit([this](const auto& record) {
			this->emitEvent(record);
		}, recordVar);
	}
		LOG_DEBUG(L"RateLimitedUIAEventHandler::flusherThreadFunc: Done emitting events");
}

void RateLimitedEventHandler::terminate() {
	LOG_DEBUG(L"RateLimitedUIAEventHandler::terminate called");
	// Stop the flusher thread.
	m_flusherThread.request_stop();
	m_flusherThread.join();
}
