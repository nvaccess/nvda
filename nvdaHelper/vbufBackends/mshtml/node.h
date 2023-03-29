/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2006-2020 NV Access Limited, Google LLC, Leonard de Ruijter
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
	void reportLiveText(std::wstring& text, std::wstring& politeness);
	void reportLiveAddition();
	void preProcessLiveRegion(const MshtmlVBufStorage_controlFieldNode_t* parent, const std::map<std::wstring,std::wstring>& attribsMap);
	void postProcessLiveRegion(VBufStorage_controlFieldNode_t* oldNode, std::set<VBufStorage_controlFieldNode_t*>& atomicNodes);
	virtual void generateAttributesForMarkupOpeningTag(std::wstring& text, int startOffset, int endOffset);
	
	MshtmlVBufStorage_controlFieldNode_t(
		int docHandle,
		int ID,
		bool isBlock,
		MshtmlVBufBackend_t* backend,
		bool isRootNode,
		IHTMLDOMNode* pHTMLDOMNode,
		const std::wstring& lang
	);

	MshtmlVBufStorage_controlFieldNode_t() = delete;

	MshtmlVBufBackend_t* backend = nullptr;
	IHTMLDOMNode* pHTMLDOMNode = nullptr;
	IDispatch* propChangeSink = nullptr;
	IDispatch* loadSink = nullptr;
	IMarkupContainer2* pMarkupContainer2 = nullptr;
	IHTMLChangeSink* pHTMLChangeSink = nullptr;
	DWORD HTMLChangeSinkCookey = 0;
	std::wstring language;
	MshtmlVBufStorage_controlFieldNode_t* ariaLiveNode = nullptr;
	std::wstring ariaLivePoliteness;
	unsigned int formatState = 0;
	bool ariaLiveIsTextRelevant = false;
	bool ariaLiveIsAdditionsRelevant = false;
	bool ariaLiveIsBusy = false;
	VBufStorage_controlFieldNode_t* ariaLiveAtomicNode = nullptr;
	bool isRootNode = false;

protected:
	/*Destructor
	* @remark Protected: This and derived classes are always dynamically allocated and memory managed by friends.
	*/
	virtual ~MshtmlVBufStorage_controlFieldNode_t();
};

#endif
