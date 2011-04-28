/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2006-2010 NVDA contributers.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#ifdef _WIN32
#include <windows.h>
#endif
#include <remote/log.h>
#include "lock.h"

VBufLock_t::VBufLock_t() {
	LOG_DEBUG(L"initializing lock");
	#ifdef _WIN32
	lockHandle=new CRITICAL_SECTION;
	LOG_DEBUG(L"critical section at address "<<lockHandle);
	InitializeCriticalSection(static_cast<LPCRITICAL_SECTION>(lockHandle));
	#endif
}

void VBufLock_t::acquire() {
	LOG_DEBUG(L"acquiring lock...");
	#ifdef _WIN32
	EnterCriticalSection(static_cast<LPCRITICAL_SECTION>(lockHandle));
	#endif
	LOG_DEBUG(L"acquired.");
}

void VBufLock_t::release() {
	LOG_DEBUG(L"Releasing lock...");
	#ifdef _WIN32
	LeaveCriticalSection(static_cast<LPCRITICAL_SECTION>(lockHandle));
	#endif
	LOG_DEBUG(L"Released.");
}

VBufLock_t::~VBufLock_t() {
	LOG_DEBUG(L"Lock being destroied");
	LOG_DEBUG(L"Deleting critical section");
	#ifdef _WIN32
	DeleteCriticalSection(static_cast<LPCRITICAL_SECTION>(lockHandle));
	delete lockHandle;
	#endif
}
