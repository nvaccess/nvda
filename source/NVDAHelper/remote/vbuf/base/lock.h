/**
 * base/lock.h
 * Part of the NV  Virtual Buffer Library
 * This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
 * This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
 * http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
 */

#ifndef VIRTUALBUFFER_LOCK_H
#define VIRTUALBUFFER_LOCK_H

#include "libEntry.h"

/**
 * a generic locking interface
 */
class VBUFLIBENTRY VBufLock_t {
	private:

/**
 * points to the platform-specific locking handle
 */
	void* lockHandle;

	public:

/**
 * Constructor
 * initializes the lock handle;
 */
	VBufLock_t();

/**
 * acquires the lock for the caller, until release is called.
 */
	void acquire();

/**
 * Releases the lock from the caller
 */
	void release();

/**
 * destructor
 * cleans up the platform-specific locking handle
 */
	~VBufLock_t();

};

#endif
