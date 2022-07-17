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

#ifndef VIRTUALBUFFER_BACKENDS_ADOBEACROBAT_H
#define VIRTUALBUFFER_BACKENDS_ADOBEACROBAT_H

#include <map>
#include <string>
#include <list>
#include <vbufBase/backend.h>
#include <AcrobatAccess.h>

class AdobeAcrobatVBufStorage_controlFieldNode_t;

typedef struct {
	int uniqueId;
	int type;
} TableHeaderInfo;

typedef struct TableInfo_t {
	long tableID{ 0 };
	int curRowNumber{ 0 };
	int curColumnNumber{ 0 };
	// Maps column numbers to remaining row spans.
	std::map<int, int> columnRowSpans;
	// Maps column numbers to table-columnheadercells attribute values.
	std::map<int, std::wstring> columnHeaders;
	// Maps row numbers to table-rowheadercells attribute values.
	std::map<int, std::wstring> rowHeaders;
	// Maps node id strings to TableHeaderInfo.
	std::map<std::wstring, TableHeaderInfo> headersInfo;
	// Lists nodes with explicit headers along with their Headers attribute string.
	std::list<std::pair<AdobeAcrobatVBufStorage_controlFieldNode_t*, std::wstring>> nodesWithExplicitHeaders;
} TableInfo;

class AdobeAcrobatVBufBackend_t: public VBufBackend_t {
	private:

	std::wstring* getPageNum(IPDDomNode* domNode);

	AdobeAcrobatVBufStorage_controlFieldNode_t* fillVBuf(int docHandle, IAccessible* pacc, VBufStorage_buffer_t* buffer,
		AdobeAcrobatVBufStorage_controlFieldNode_t* parentNode, VBufStorage_fieldNode_t* previousNode,
		AdobeAcrobatVBufStorage_controlFieldNode_t* oldNode,
		TableInfo* tableInfo = NULL, std::wstring* pageNum = NULL
	);

	bool isXFA = true;

	IPDDomDocPagination* docPagination = nullptr;

	protected:

	static void CALLBACK renderThread_winEventProcHook(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time);

	virtual void renderThread_initialize();

	virtual void renderThread_terminate();

	virtual void render(VBufStorage_buffer_t* buffer, int docHandle, int ID, VBufStorage_controlFieldNode_t* oldNode);

	virtual ~AdobeAcrobatVBufBackend_t();

	public:

	AdobeAcrobatVBufBackend_t(int docHandle, int ID);

};

#endif
