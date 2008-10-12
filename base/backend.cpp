/**
 * base/backend.cpp
 * Part of the NV  Virtual Buffer Library
 * This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
 * This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
 * http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
 */

#include "debug.h"
#include "storage.h"
#include "backend.h"

VBufBackend_t::VBufBackend_t(int docHandleArg, int IDArg, VBufStorage_buffer_t* storageBufferArg): rootDocHandle(docHandleArg), rootID(IDArg), storageBuffer(storageBufferArg) {
	DEBUG_MSG(L"Initializing backend with docHandle "<<docHandleArg<<L", ID "<<IDArg<<L", storageBuffer "<<storageBufferArg);
}

VBufBackend_t::~VBufBackend_t() {
	DEBUG_MSG(L"Backend being destroied");
}
