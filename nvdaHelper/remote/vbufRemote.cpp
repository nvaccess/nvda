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

#include <map>
#include <remote/vbufRemote.h>
#include <vbufBase/backend.h>
#include "dllmain.h"
#include <common/log.h>

using namespace std;

const map<wstring,VBufBackend_create_proc> VBufBackendFactoryMap {
	{L"adobeAcrobat",AdobeAcrobatVBufBackend_t_createInstance},
	{L"gecko_ia2",GeckoVBufBackend_t_createInstance},
	{L"mshtml",MshtmlVBufBackend_t_createInstance},
	{L"lotusNotesRichText",lotusNotesRichTextVBufBackend_t_createInstance},
	{L"webKit",WebKitVBufBackend_t_createInstance}
};

extern "C" {

VBufRemote_bufferHandle_t VBufRemote_createBuffer(handle_t bindingHandle, int docHandle, int ID, const wchar_t* backendName) {
	if(!backendName) {
		LOG_ERROR(L"backendName is NULL");
		return nullptr;
	}
	auto i=VBufBackendFactoryMap.find(backendName);
	if(i==VBufBackendFactoryMap.end()) {
		LOG_ERROR(L"Unknown backend: "<<backendName);
		return nullptr;
	}
	VBufBackend_create_proc createBackend=i->second;
	VBufBackend_t* backend=createBackend(docHandle,ID);
	if(backend==NULL) {
		return NULL;
	}
	backend->initialize();
	// Stop nvdaHelperRemote from being unloaded while a backend exists.
	HINSTANCE tempHandle=nullptr;
	if(!GetModuleHandleEx(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS,reinterpret_cast<LPCWSTR>(dllHandle),&tempHandle)) {
		LOG_ERROR(L"Could not keep nvdaHelperRemote loaded for backend!");
	}
	return (VBufRemote_bufferHandle_t)backend;
}

void VBufRemote_destroyBuffer(VBufRemote_bufferHandle_t* buffer) {
	#ifndef NDEBUG
	Beep(4000,80);
	#endif
	VBufBackend_t* backend=(VBufBackend_t*)*buffer;
	backend->terminate();
	backend->lock.acquire();
	backend->destroy();
	FreeLibrary(dllHandle);
	*buffer=NULL;
}

int VBufRemote_getFieldNodeOffsets(VBufRemote_bufferHandle_t buffer, VBufRemote_nodeHandle_t node, int *startOffset, int *endOffset) {
	VBufBackend_t* backend=(VBufBackend_t*)buffer;
	VBufStorage_fieldNode_t* realNode=(VBufStorage_fieldNode_t*)node;
	backend->lock.acquire();
	int res=backend->getFieldNodeOffsets(realNode,startOffset,endOffset);
	backend->lock.release();
	return res;
}

int VBufRemote_isFieldNodeAtOffset(VBufRemote_bufferHandle_t buffer, VBufRemote_nodeHandle_t node, int offset) {
	VBufBackend_t* backend=(VBufBackend_t*)buffer;
	VBufStorage_fieldNode_t* realNode=(VBufStorage_fieldNode_t*)node;
	backend->lock.acquire();
	int res=backend->isFieldNodeAtOffset(realNode,offset);
	backend->lock.release();
	return res;
}

int VBufRemote_locateTextFieldNodeAtOffset(VBufRemote_bufferHandle_t buffer, int offset, int *nodeStartOffset, int *nodeEndOffset, VBufRemote_nodeHandle_t* foundNode) {
	VBufBackend_t* backend=(VBufBackend_t*)buffer;
	backend->lock.acquire();
	*foundNode=(VBufRemote_nodeHandle_t)(backend->locateTextFieldNodeAtOffset(offset,nodeStartOffset,nodeEndOffset));
	backend->lock.release();
	return (*foundNode)!=NULL;
}

int VBufRemote_locateControlFieldNodeAtOffset(VBufRemote_bufferHandle_t buffer, int offset, int *nodeStartOffset, int *nodeEndOffset, int *docHandle, int *ID, VBufRemote_nodeHandle_t* foundNode) {
	VBufBackend_t* backend=(VBufBackend_t*)buffer;
	backend->lock.acquire();
	*foundNode=(VBufRemote_nodeHandle_t)(backend->locateControlFieldNodeAtOffset(offset,nodeStartOffset,nodeEndOffset,docHandle,ID));
	backend->lock.release();
	return (*foundNode)!=0;
}

int VBufRemote_getControlFieldNodeWithIdentifier(VBufRemote_bufferHandle_t buffer, int docHandle, int ID, VBufRemote_nodeHandle_t* foundNode) { 
	VBufBackend_t* backend=(VBufBackend_t*)buffer;
	backend->lock.acquire();
	*foundNode=(VBufRemote_nodeHandle_t)(backend->getControlFieldNodeWithIdentifier(docHandle,ID));
	backend->lock.release();
	return (*foundNode)!=0;
}

int VBufRemote_getIdentifierFromControlFieldNode(VBufRemote_bufferHandle_t buffer, VBufRemote_nodeHandle_t node, int* docHandle, int* ID) { 
	VBufBackend_t* backend=(VBufBackend_t*)buffer;
	backend->lock.acquire();
	int res=backend->getIdentifierFromControlFieldNode((VBufStorage_controlFieldNode_t*)node,docHandle,ID);
	backend->lock.release();
	return res;
}

int VBufRemote_findNodeByAttributes(VBufRemote_bufferHandle_t buffer, int offset, int direction, const wchar_t* attribs, const wchar_t* regexp, int *startOffset, int *endOffset, VBufRemote_nodeHandle_t* foundNode) { 
	VBufBackend_t* backend=(VBufBackend_t*)buffer;
	backend->lock.acquire();
	*foundNode=(VBufRemote_nodeHandle_t)(backend->findNodeByAttributes(offset,(VBufStorage_findDirection_t)direction,attribs,regexp,startOffset,endOffset));
	backend->lock.release();
	return (*foundNode)!=0;
}

int VBufRemote_getSelectionOffsets(VBufRemote_bufferHandle_t buffer, int *startOffset, int *endOffset) {
	VBufBackend_t* backend=(VBufBackend_t*)buffer;
	backend->lock.acquire();
	int res=backend->getSelectionOffsets(startOffset,endOffset);
	backend->lock.release();
	return res;
}

int VBufRemote_setSelectionOffsets(VBufRemote_bufferHandle_t buffer, int startOffset, int endOffset) {
	VBufBackend_t* backend=(VBufBackend_t*)buffer;
	backend->lock.acquire();
	int res=backend->setSelectionOffsets(startOffset,endOffset);
	backend->lock.release();
	return res;
}

int VBufRemote_getTextLength(VBufRemote_bufferHandle_t buffer) {
	VBufBackend_t* backend=(VBufBackend_t*)buffer;
	backend->lock.acquire();
	int res=backend->getTextLength();
	backend->lock.release();
	return res;
}

int VBufRemote_getTextInRange(VBufRemote_bufferHandle_t buffer, int startOffset, int endOffset, wchar_t** text, boolean useMarkup) {
	VBufBackend_t* backend=(VBufBackend_t*)buffer;
	backend->lock.acquire();
	 wstring textString;
	 backend->getTextInRange(startOffset,endOffset,textString,useMarkup!=false);
	backend->lock.release();
	if(textString.empty()) {
		return false;
	}
	*text=SysAllocString(textString.c_str());
	return true;
}

int VBufRemote_getLineOffsets(VBufRemote_bufferHandle_t buffer, int offset, int maxLineLength, boolean useScreenLayout, int *startOffset, int *endOffset) {
	VBufBackend_t* backend=(VBufBackend_t*)buffer;
	backend->lock.acquire();
	int res=backend->getLineOffsets(offset,maxLineLength,useScreenLayout!=false,startOffset,endOffset);
	backend->lock.release();
	return res;
}

//Special cleanup method for VBufRemote when client is lost
void __RPC_USER VBufRemote_bufferHandle_t_rundown(VBufRemote_bufferHandle_t buffer) {
	VBufRemote_destroyBuffer(&buffer);
}

}
