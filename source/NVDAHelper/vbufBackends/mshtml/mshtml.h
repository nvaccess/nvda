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

#ifndef VIRTUALBUFFER_BACKENDS_MSHTML_H
#define VIRTUALBUFFER_BACKENDS_MSHTML_H

#include <vbufBase/storage.h>
#include <vbufBase/backend.h>

typedef struct {
	int tableID;
	long curRowIndex;
	bool definitData;
} fillVBuf_tableInfo;

void incBackendLibRefCount();
void decBackendLibRefCount();

class MshtmlVBufBackend_t: public VBufBackend_t {
	protected:

	virtual void render(VBufStorage_buffer_t* buffer, int docHandle, int ID, VBufStorage_controlFieldNode_t* oldNode=NULL);

	VBufStorage_fieldNode_t* fillVBuf(VBufStorage_buffer_t* buffer, VBufStorage_controlFieldNode_t* parentNode, VBufStorage_fieldNode_t* previousNode, IHTMLDOMNode* pHTMLDOMNode, int docHandle, fillVBuf_tableInfo* tableInfoPtr, int* LIIndexPtr, bool parentHasContent);

	virtual ~MshtmlVBufBackend_t();

	public:

	MshtmlVBufBackend_t(int docHandle, int ID);

	VBufStorage_controlFieldNode_t* getDeepestControlFieldNodeForHTMLElement(IHTMLElement* pHTMLElement);

};

#endif
