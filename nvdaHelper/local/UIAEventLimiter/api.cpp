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

#include <set>
#include <windows.h>
#include <common/log.h>
#include "rateLimitedEventHandler.h"

std::set<RateLimitedEventHandler*> activeRateLimitedEventHandlers;

HRESULT rateLimitedUIAEventHandler_create(IUnknown* pExistingHandler, RateLimitedEventHandler** ppRateLimitedEventHandler) {
	LOG_DEBUG(L"rateLimitedUIAEventHandler_create called");
	if(!pExistingHandler || !ppRateLimitedEventHandler) {
		LOG_ERROR(L"rateLimitedUIAEventHandler_create: one or more NULL arguments"); 
		return E_INVALIDARG;
	}

	// Create the RateLimitedEventHandler instance
	*ppRateLimitedEventHandler = new RateLimitedEventHandler(pExistingHandler);
	if (!(*ppRateLimitedEventHandler)) {
		LOG_ERROR(L"rateLimitedUIAEventHandler_create: Could not create RateLimitedUIAEventHandler. Returning");
		return E_OUTOFMEMORY;
	}
	LOG_DEBUG(L"rateLimitedUIAEventHandler_create: done");
	activeRateLimitedEventHandlers.insert(*ppRateLimitedEventHandler);
	return S_OK;
}

// @brief Terminates a RateLimitedEventHandler instance's flusher thread and removes it from the activeRateLimitedEventHandlers set.
// @param pRateLimitedEventHandler the RateLimitedEventHandler instance to terminate.
// @note This function will block until the RateLimitedEventHandler's flusher thread has terminated. 
// @return S_OK on success or a failure code otherwise
HRESULT rateLimitedUIAEventHandler_terminate(RateLimitedEventHandler* pRateLimitedEventHandler) {
	if (activeRateLimitedEventHandlers.find(pRateLimitedEventHandler) == activeRateLimitedEventHandlers.end()) {
		LOG_ERROR(L"rateLimitedUIAEventHandler_terminate: pRateLimitedEventHandler not found in activeRateLimitedEventHandlers");
		return E_INVALIDARG;
	}
	activeRateLimitedEventHandlers.erase(pRateLimitedEventHandler);
	pRateLimitedEventHandler->terminate();
	return S_OK;
}
