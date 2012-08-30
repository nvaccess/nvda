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

#ifndef VIRTUALBUFFER_BACKENDS_EXAMPLE_H
#define VIRTUALBUFFER_BACKENDS_EXAMPLE_H

#include <vbufBase/backend.h>

class GeckoVBufBackend_t: public VBufBackend_t {
	private:

	VBufStorage_fieldNode_t* fillVBuf(IAccessible2* pacc,
		VBufStorage_buffer_t* buffer, VBufStorage_controlFieldNode_t* parentNode, VBufStorage_fieldNode_t* previousNode,
		IAccessibleTable* paccTable=NULL, IAccessibleTable2* paccTable2=NULL, long tableID=0,
		bool ignoreInteractiveUnlabelledGraphics=false
	);

	void versionSpecificInit(IAccessible2* pacc);

	void fillTableCellInfo_IATable2(VBufStorage_controlFieldNode_t* node, IAccessibleTableCell* paccTableCell);

	bool shouldDisableTableHeaders;
	bool hasEncodedAccDescription;

	protected:

	static void CALLBACK renderThread_winEventProcHook(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time);

	virtual void renderThread_initialize();

	virtual void renderThread_terminate();

	virtual void render(VBufStorage_buffer_t* buffer, int docHandle, int ID, VBufStorage_controlFieldNode_t* oldNode=NULL);

	virtual ~GeckoVBufBackend_t();

	public:

	GeckoVBufBackend_t(int docHandle, int ID);

};

#endif
