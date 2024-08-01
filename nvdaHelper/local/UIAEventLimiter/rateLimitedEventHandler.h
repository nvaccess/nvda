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

#include <vector>
#include <map>
#include <list>
#include <mutex>
#include <uiautomation.h>
#include "eventRecord.h"


// @brief a class that listens for various UI Automation events, 
// stores them in in an internal queue (removing any duplicates),
// and sends them onto an existing UI Automation event handler in a separate thread.
// This ensures that UI Automation core is never blocked while sending events to this class.
class RateLimitedEventHandler:
	public IUIAutomationEventHandler,
	public IUIAutomationFocusChangedEventHandler,
	public IUIAutomationPropertyChangedEventHandler,
	public IUIAutomationNotificationEventHandler,
	public IUIAutomationActiveTextPositionChangedEventHandler
{
private:
	unsigned long m_refCount = 1;
	CComQIPtr<IUIAutomationEventHandler> m_pExistingAutomationEventHandler;
	CComQIPtr<IUIAutomationFocusChangedEventHandler> m_pExistingFocusChangedEventHandler;
	CComQIPtr<IUIAutomationPropertyChangedEventHandler> m_pExistingPropertyChangedEventHandler;
	CComQIPtr<IUIAutomationNotificationEventHandler> m_pExistingNotificationEventHandler;
	CComQIPtr<IUIAutomationActiveTextPositionChangedEventHandler> m_pExistingActiveTextPositionChangedEventHandler;
	std::list<EventRecordVariant_t> m_eventRecords;
	std::map<std::vector<int>, std::pair<decltype(m_eventRecords)::iterator, int>> m_eventRecordsByKey;
	bool m_needsFlush = false;
	std::mutex m_mtx;
	std::condition_variable m_flushConditionVar;
	std::jthread m_flusherThread;

	/// @brief a thread function that wakes and flushes the event queue when one or more events have been added.
	/// @param stopToken used to check if the thread should stop.
	void flusherThreadFunc(std::stop_token stopToken);

	/// @brief a template function that queues a UI Automation event. 
	/// @tparam EventRecordClass the type of event record representing a UI Automation event. 
	/// @tparam ...EventRecordArgTypes the argument types required to construct the event record
	/// @param ...args the arguments to construct the event record.
	/// @return S_OK on success or a failure code otherwise.
	template<EventRecordConstraints EventRecordClass, typename... EventRecordArgTypes> HRESULT queueEvent(EventRecordArgTypes&&... args);

	/// @brief Emits a UI Automation event to its existing handler.
	/// @param record the event record representing the UI automation event. 
	/// @return  S_OK on success or a failure code otherwise.
	HRESULT emitEvent(const AutomationEventRecord_t& record) const;
	HRESULT emitEvent(const FocusChangedEventRecord_t& record) const;
	HRESULT emitEvent(const PropertyChangedEventRecord_t& record) const;
	HRESULT emitEvent(const NotificationEventRecord_t& record) const;
	HRESULT emitEvent(const ActiveTextPositionChangedEventRecord_t& record) const;

	/// @brief Removes all events from the queue, sending them on to the existing UI automation event handler.
	void flushEvents();

	~RateLimitedEventHandler();

	public:

	/// @brief class constructor. 
	/// @param pExistingHandler  a pointer to an existing UI Automation event handler where events should be sent after they are flushed from the queue.
	RateLimitedEventHandler(IUnknown* pExistingHandler);

	// IUnknown methods
	ULONG STDMETHODCALLTYPE AddRef();
	ULONG STDMETHODCALLTYPE Release();
	HRESULT STDMETHODCALLTYPE QueryInterface(REFIID riid, void** ppInterface);

	// IUIAutomationEventHandler methods
	HRESULT STDMETHODCALLTYPE HandleAutomationEvent(IUIAutomationElement* sender, EVENTID eventID);
	HRESULT STDMETHODCALLTYPE HandleFocusChangedEvent(IUIAutomationElement* sender);
	HRESULT STDMETHODCALLTYPE HandlePropertyChangedEvent(IUIAutomationElement* sender, PROPERTYID propertyID, VARIANT newValue);
	HRESULT STDMETHODCALLTYPE HandleNotificationEvent(IUIAutomationElement* sender, NotificationKind notificationKind, NotificationProcessing notificationProcessing, BSTR displayString, BSTR activityID);
	HRESULT STDMETHODCALLTYPE HandleActiveTextPositionChangedEvent(IUIAutomationElement* sender, IUIAutomationTextRange* range);

	/// @brief a function that stops the flusher thread.
	// @note This call will block until the flusher thread has stopped.
	void terminate();

};
