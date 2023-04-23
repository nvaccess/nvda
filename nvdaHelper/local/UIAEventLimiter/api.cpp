#include <windows.h>
#include <common/log.h>
#include "rateLimitedEventHandler.h"

HRESULT rateLimitedUIAEventHandler_create(IUnknown* pExistingHandler, HWND messageWindow, UINT flushMessage, RateLimitedEventHandler** ppRateLimitedEventHandler) {
	LOG_DEBUG(L"rateLimitedUIAEventHandler_create called");
	if(!pExistingHandler || !messageWindow || !ppRateLimitedEventHandler) {
		LOG_ERROR(L"rateLimitedUIAEventHandler_create: one or more NULL arguments"); 
		return E_INVALIDARG;
	}

	// Create the RateLimitedEventHandler instance
	*ppRateLimitedEventHandler = new RateLimitedEventHandler(pExistingHandler, messageWindow, flushMessage);
	if (!(*ppRateLimitedEventHandler)) {
		LOG_ERROR(L"rateLimitedUIAEventHandler_create: Could not create RateLimitedUIAEventHandler. Returning");
		return E_OUTOFMEMORY;
	}
	LOG_DEBUG(L"rateLimitedUIAEventHandler_create: done");
	return S_OK;
}

HRESULT rateLimitedUIAEventHandler_flush(RateLimitedEventHandler* pRateLimitedEventHandler) {
	LOG_DEBUG(L"rateLimitedUIAEventHandler_flush called");
	if(!pRateLimitedEventHandler) {
		LOG_ERROR(L"rateLimitedUIAEventHandler_flush: invalid argument. Returning");
		return E_INVALIDARG;
	}
	pRateLimitedEventHandler->flush();
	return S_OK;
}
