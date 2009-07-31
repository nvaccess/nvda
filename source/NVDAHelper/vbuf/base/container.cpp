/**
 * base/container.cpp
 * Part of the NV  Virtual Buffer Library
 * This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
 * This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
 * http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
 */

#ifdef _WIN32
#include <windows.h>
#endif
#ifdef _POSIX
#include <dlfcn.h>
#endif
#include "debug.h"
#include "storage.h"
#include "backend.h"
#include "container.h"

VBufContainer_t::VBufContainer_t(int docHandle, int ID, const char* backendPath): VBufStorage_buffer_t(), backendLib(NULL), backend(NULL) {
	DEBUG_MSG(L"initializing container with docHandle "<<docHandle<<L", ID "<<ID<<L", backendPath \""<<backendPath<<L"\"");
	#ifdef _WIN32
	this->backendLib=LoadLibrary(backendPath);
	#endif
	#ifdef _POSIX
	this->backendLib=dlopen(backendPath,RTLD_LAZY);
	#endif
	if(this->backendLib) {
		DEBUG_MSG(L"backend library loaded at address "<<this->backendLib);
		#ifdef _WIN32
		VBufBackend_create_proc createBackend=(VBufBackend_create_proc)GetProcAddress((HMODULE)(this->backendLib),"VBufBackend_create");
		#endif
		#ifdef _POSIX
		VBufBackend_create_proc createBackend=(VBufBackend_create_proc)dlsym(this->backendLib,"VBufBackend_create");
		#endif
		if(createBackend) {
			DEBUG_MSG(L"found VBufBackend_create at address "<<createBackend);
			this->backend=createBackend(docHandle,ID,this);
			DEBUG_MSG(L"backend is at "<<this->backend);
		} else {
			DEBUG_MSG(L"could not find VBufBackend_create in backend library");
		}
	} else {
		DEBUG_MSG(L"Could not load backend library");
	}
}

VBufContainer_t::~VBufContainer_t() {
	DEBUG_MSG(L"container being destroied");
	if(this->backend) {
		DEBUG_MSG(L"deleting backend");
		delete backend;
	}
	if(this->backendLib) {
		DEBUG_MSG(L"Freeing backend library");
		#ifdef _WIN32
		FreeLibrary((HMODULE)backendLib);
		#endif
		#ifdef _POSIX
		dlclose(backendLib);
		#endif
	}
}
