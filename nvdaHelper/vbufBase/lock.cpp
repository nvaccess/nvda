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
#include <common/debug.h>
#include "lock.h"

VBufLock_t::VBufLock_t() {
	DEBUG_MSG(L"initializing lock");
	#ifdef _WIN32
	lockHandle=new CRITICAL_SECTION;
	DEBUG_MSG(L"critical section at address "<<lockHandle);
	InitializeCriticalSection(static_cast<LPCRITICAL_SECTION>(lockHandle));
	#endif
}

void VBufLock_t::acquire() {
	DEBUG_MSG(L"acquiring lock...");
	#ifdef _WIN32
	EnterCriticalSection(static_cast<LPCRITICAL_SECTION>(lockHandle));
	#endif
	DEBUG_MSG(L"acquired.");
}

void VBufLock_t::release() {
	DEBUG_MSG(L"Releasing lock...");
	#ifdef _WIN32
	LeaveCriticalSection(static_cast<LPCRITICAL_SECTION>(lockHandle));
	#endif
	DEBUG_MSG(L"Released.");
}

VBufLock_t::~VBufLock_t() {
	DEBUG_MSG(L"Lock being destroied");
	DEBUG_MSG(L"Deleting critical section");
	#ifdef _WIN32
	DeleteCriticalSection(static_cast<LPCRITICAL_SECTION>(lockHandle));
	delete lockHandle;
	#endif
}
