/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2011 NV Access Inc
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#ifndef VIRTUALBUFFER_BACKENDS_WEBKIT_H
#define VIRTUALBUFFER_BACKENDS_WEBKIT_H

#include <map>
#include <vbufBase/backend.h>

class WebKitVBufBackend_t: public VBufBackend_t {
	private:

	VBufStorage_fieldNode_t* fillVBuf(int docHandle, IAccessible2* pacc, VBufStorage_buffer_t* buffer,
		VBufStorage_controlFieldNode_t* parentNode, VBufStorage_fieldNode_t* previousNode
	);

	protected:

	static void CALLBACK renderThread_winEventProcHook(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time);

	virtual void renderThread_initialize();

	virtual void renderThread_terminate();

	virtual void render(VBufStorage_buffer_t* buffer, int docHandle, int ID, VBufStorage_controlFieldNode_t* oldNode);

	public:

	WebKitVBufBackend_t(int docHandle, int ID);

};

#endif
