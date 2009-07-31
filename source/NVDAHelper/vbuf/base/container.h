/**
 * base/container.h
 * Part of the NV  Virtual Buffer Library
 * This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
 * This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
 * http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
 */

#ifndef VIRTUALBUFFER_CONTAINER_H
#define VIRTUALBUFFER_CONTAINER_H

#include "libEntry.h"
#include "storage.h"
#include "backend.h"
#include "container.h"

/**
 * Holds together a storage buffer, along with a backend, and locking methods, to make a virtual buffer.
 */
class VBUFLIBENTRY VBufContainer_t : public VBufStorage_buffer_t  {
	private:
/**
 * a handle to the backend's library
 */
	void* backendLib;

/**
 * The backend for this virtual buffer
 */
	VBufBackend_t* backend;

	public:

/**
 * Constructor
 * @param docHandle uniquely identifies the window or document the virtual buffer is for
 * @param ID uniquely identifies the object with in the window or document the virtual buffer will start rendering from
 * @param backendPath an absolute path to the backend library you wish to manage the virtual buffer
 */
	VBufContainer_t(int docHandle, int ID, const char* backendPath);

/**
 * destructor
 */
	~VBufContainer_t();

};

#endif
 