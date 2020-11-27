/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2006-2015 NVDA contributers.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#ifndef VIRTUALBUFFER_BACKENDS_NODE_H
#define VIRTUALBUFFER_BACKENDS_NODE_H

#include <mshtml.h>
#include <vbufBase/storage.h>
#include <vbufBase/backend.h>
#include "mshtml.h"

class MshtmlVBufStorage_controlFieldNode_t : public VBufStorage_controlFieldNode_t {

	public:
	MshtmlVBufBackend_t* backend;
	IHTMLDOMNode* pHTMLDOMNode;
	IDispatch* propChangeSink;
	IDispatch* loadSink;
	IMarkupContainer2* pMarkupContainer2;
	IHTMLChangeSink* pHTMLChangeSink;
	DWORD HTMLChangeSinkCookey;
	std::wstring language;
	VBufStorage_controlFieldNode_t*  ariaLiveNode;
	unsigned int formatState;
	bool ariaLiveIsTextRelevant;
	bool ariaLiveIsAdditionsRelevant;
	bool ariaLiveIsBusy;
	VBufStorage_controlFieldNode_t*  ariaLiveAtomicNode;
	void reportLiveText(std::wstring& text);
	void reportLiveAddition();
	void preProcessLiveRegion(const MshtmlVBufStorage_controlFieldNode_t* parent, const std::map<std::wstring,std::wstring>& attribsMap);
	void postProcessLiveRegion(VBufStorage_controlFieldNode_t* oldNode, std::set<VBufStorage_controlFieldNode_t*>& atomicNodes);
	virtual void generateAttributesForMarkupOpeningTag(std::wstring& text, int startOffset, int endOffset);
	bool isRootNode;
	MshtmlVBufStorage_controlFieldNode_t(int docHandle, int ID, bool isBlock, MshtmlVBufBackend_t* backend, bool isRootNode, IHTMLDOMNode* pHTMLDOMNode, const std::wstring& lang);
	~MshtmlVBufStorage_controlFieldNode_t();

};

#endif
