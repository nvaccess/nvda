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
#include <common/log.h>
#include "rateLimitedEventHandler.h"

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
	return S_OK;
}
