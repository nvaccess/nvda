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
#include "vbufRemote.h"
#include <vbufBase/backend.h>
#include "dllmain.h"

using namespace std;

map<VBufBackend_t*,HINSTANCE> backendLibHandles;

extern "C" {

VBufRemote_bufferHandle_t VBufRemote_createBuffer(handle_t bindingHandle, int docHandle, int ID, const wchar_t* backendName) {
	wchar_t backendPath[MAX_PATH];
	wsprintf(backendPath,L"%s\\VBufBackend_%s.dll",dllDirectory,backendName);
	HINSTANCE backendLibHandle=LoadLibrary(backendPath);
	if(backendLibHandle==NULL) return NULL;
	VBufBackend_create_proc createBackend=(VBufBackend_create_proc)GetProcAddress((HMODULE)(backendLibHandle),"VBufBackend_create");
	if(createBackend==NULL) {
		FreeLibrary(backendLibHandle);
		return NULL;
	} 
	VBufBackend_t* backend=createBackend(docHandle,ID);
	if(backend==NULL) {
		FreeLibrary(backendLibHandle);
		return NULL;
	}
	backendLibHandles[backend]=backendLibHandle;
	backend->initialize();
	return (VBufRemote_bufferHandle_t)backend;
}

void VBufRemote_destroyBuffer(VBufRemote_bufferHandle_t* buffer) {
	#ifndef NDEBUG
	Beep(4000,80);
	#endif
	VBufBackend_t* backend=(VBufBackend_t*)*buffer;
	backend->terminate();
	map<VBufBackend_t*,HINSTANCE>::iterator i=backendLibHandles.find(backend);
	if(i==backendLibHandles.end()) return;
	HINSTANCE backendLibHandle=i->second;
	backendLibHandles.erase(i); 
	backend->lock.acquire();
	backend->destroy();
	FreeLibrary(backendLibHandle);
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
	VBufStorage_textContainer_t* textContainer=backend->getTextInRange(startOffset,endOffset,useMarkup!=false);
	backend->lock.release();
	if(textContainer==NULL) {
		return false;
	}
	*text=SysAllocString(textContainer->getString().c_str());
	textContainer->destroy();
	return true;
}

int VBufRemote_getLineOffsets(VBufRemote_bufferHandle_t buffer, int offset, int maxLineLength, boolean useScreenLayout, int *startOffset, int *endOffset) {
	VBufBackend_t* backend=(VBufBackend_t*)buffer;
	backend->lock.acquire();
	int res=backend->getLineOffsets(offset,maxLineLength,useScreenLayout!=false,startOffset,endOffset);
	backend->lock.release();
	return res;
}

int VBufRemote_getNativeHandleForNode(VBufRemote_bufferHandle_t buffer, VBufRemote_nodeHandle_t node) {
	VBufBackend_t* backend=(VBufBackend_t*)buffer;
	VBufStorage_controlFieldNode_t* realNode=(VBufStorage_controlFieldNode_t*)node;
	backend->lock.acquire();
	int res=backend->getNativeHandleForNode(realNode);
	backend->lock.release();
	return res;
}

int VBufRemote_getNodeForNativeHandle(VBufRemote_bufferHandle_t buffer, int nativeHandle, VBufRemote_nodeHandle_t* node) {
	VBufBackend_t* backend=(VBufBackend_t*)buffer;
	backend->lock.acquire();
	*node=(VBufRemote_nodeHandle_t)(backend->getNodeForNativeHandle(nativeHandle));
	backend->lock.release();
	return (*node)!=0;
}

//Special cleanup method for VBufRemote when client is lost
void __RPC_USER VBufRemote_bufferHandle_t_rundown(VBufRemote_bufferHandle_t buffer) {
	VBufRemote_destroyBuffer(&buffer);
}

}
