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
	int uniqueId;
	int type;
} TableHeaderInfo;

typedef struct {
	long tableID;
	int curRowNumber;
	int curColumnNumber;
	// Maps column numbers to remaining row spans.
	std::map<int, int> columnRowSpans;
	// Maps column numbers to table-columnheadercells attribute values.
	std::map<int, std::wstring> columnHeaders;
	// Maps row numbers to table-rowheadercells attribute values.
	std::map<int, std::wstring> rowHeaders;
	// Maps node id strings to TableHeaderInfo.
	std::map<std::wstring, TableHeaderInfo> headersInfo;
	// Lists nodes with explicit headers along with their Headers attribute string.
	std::list<std::pair<VBufStorage_controlFieldNode_t*, std::wstring>> nodesWithExplicitHeaders;
	bool definitData;
	VBufStorage_controlFieldNode_t* tableNode;
} fillVBuf_tableInfo;

void incBackendLibRefCount();
void decBackendLibRefCount();

// gets the window message registered by MSHTML which is used to fetch the MSHTML object model from its window. 
UINT getHTMLWindowMessage();

class MshtmlVBufBackend_t: public VBufBackend_t {
	protected:

	virtual void render(VBufStorage_buffer_t* buffer, int docHandle, int ID, VBufStorage_controlFieldNode_t* oldNode=NULL);

	VBufStorage_fieldNode_t* fillVBuf(VBufStorage_buffer_t* buffer, VBufStorage_controlFieldNode_t* parentNode, VBufStorage_fieldNode_t* previousNode, VBufStorage_controlFieldNode_t* oldNode, IHTMLDOMNode* pHTMLDOMNode, int docHandle, fillVBuf_tableInfo* tableInfoPtr, int* LIIndexPtr, bool ignoreInteractiveUnlabelledGraphics, bool allowPreformattedText, bool shouldSkipText, bool inNewSubtree, std::set<VBufStorage_controlFieldNode_t*>& atomicNodes);

	virtual ~MshtmlVBufBackend_t();

	public:

	MshtmlVBufBackend_t(int docHandle, int ID);

	VBufStorage_controlFieldNode_t* getDeepestControlFieldNodeForHTMLElement(IHTMLElement* pHTMLElement);

};

#endif
