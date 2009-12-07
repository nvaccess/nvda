/**
 * base/lock.cpp
 * Part of the NV  Virtual Buffer Library
 * This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
 * This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
 * http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
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
