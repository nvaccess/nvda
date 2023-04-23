#include <vector>
#include <map>
#include <list>
#include <mutex>
#include <uiautomation.h>
#include "eventRecord.h"

class RateLimitedEventHandler: public IUIAutomationEventHandler, public IUIAutomationFocusChangedEventHandler, public IUIAutomationPropertyChangedEventHandler, public IUIAutomationNotificationEventHandler, public IUIAutomationActiveTextPositionChangedEventHandler {
private:
	unsigned long m_refCount;
	CComQIPtr<IUIAutomationEventHandler> m_pExistingAutomationEventHandler;
	CComQIPtr<IUIAutomationFocusChangedEventHandler> m_pExistingFocusChangedEventHandler;
	CComQIPtr<IUIAutomationPropertyChangedEventHandler> m_pExistingPropertyChangedEventHandler;
	CComQIPtr<IUIAutomationNotificationEventHandler> m_pExistingNotificationEventHandler;
	CComQIPtr<IUIAutomationActiveTextPositionChangedEventHandler> m_pExistingActiveTextPositionChangedEventHandler;
	HWND m_messageWindow;
	UINT m_flushMessage;
	std::mutex mtx;
	std::list<AnyEventRecord_t> m_eventRecords;
	std::map<std::vector<int>, std::pair<decltype(m_eventRecords)::iterator, int>> m_eventRecordsByKey;

	template<EventRecordConstraints EventRecordClass, typename... EventRecordArgTypes> HRESULT queueEvent(EventRecordArgTypes&&... args);

	HRESULT emitEvent(const AutomationEventRecord_t& record) const;
	HRESULT emitEvent(const FocusChangedEventRecord_t& record) const;
	HRESULT emitEvent(const PropertyChangedEventRecord_t& record) const;
	HRESULT emitEvent(const NotificationEventRecord_t& record) const;
	HRESULT emitEvent(const ActiveTextPositionChangedEventRecord_t& record) const;

	~RateLimitedEventHandler();

	public:

	RateLimitedEventHandler(IUnknown* pExistingHandler, HWND messageWindow, UINT flushMessage);

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

	void flush();

};
