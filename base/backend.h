/**
 * base/backend.h
 * Part of the NV  Virtual Buffer Library
 * This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
 * This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
 * http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
 */

#ifndef VIRTUALBUFFER_BACKEND_H
#define VIRTUALBUFFER_BACKEND_H

#include "libEntry.h"
#include "storage.h"

/**
 * Renders content in to a storage buffer for linea access.
 */
class VBUFLIBENTRY VBufBackend_t {
	protected:
	int rootDocHandle;
	int rootID;
	VBufStorage_buffer_t* storageBuffer;

	public:

/**
 * 
/**
 * constructor
 * @param docHandle uniquely identifies the document or window containing the content to ve rendered
 * @param ID uniquely identifies where to start rendering from in the document or window
 * @param storageBuffer the storage buffer to render the content in
 */
	VBufBackend_t(int docHandle, int ID, VBufStorage_buffer_t* storageBuffer);

/*
 * Destructor
 */
	virtual ~VBufBackend_t();

};

typedef VBufBackend_t*(*VBufBackend_create_proc)(int,int,VBufStorage_buffer_t*);

#endif
