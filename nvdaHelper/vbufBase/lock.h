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

#ifndef VIRTUALBUFFER_LOCK_H
#define VIRTUALBUFFER_LOCK_H

/**
 * a generic locking interface
 */
class VBufLock_t {
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
	virtual void acquire();

/**
 * Releases the lock from the caller
 */
	virtual void release();

/**
 * destructor
 * cleans up the platform-specific locking handle
 */
	~VBufLock_t();

};

#endif
