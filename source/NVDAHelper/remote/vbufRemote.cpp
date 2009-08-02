#define UNICODE
#include <map>
#include <windows.h>
#include <interfaces/vbuf/vbuf.h>
#include <vbufBase/backend.h>

using namespace std;

map<VBufBackend_t*,HINSTANCE> backendLibHandles;

extern "C" {

VBufRemote_bufferHandle_t VBufRemote_createBuffer(handle_t bindingHandle, int docHandle, int ID, const wchar_t* backendPath) {
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
	return (VBufRemote_bufferHandle_t)backend;
}

void VBufRemote_destroyBuffer(VBufRemote_bufferHandle_t* buffer) {
	VBufBackend_t* backend=(VBufBackend_t*)*buffer;
	map<VBufBackend_t*,HINSTANCE>::iterator i=backendLibHandles.find(backend);
	if(i==backendLibHandles.end()) return;
	HINSTANCE backendLibHandle=i->second;
	backendLibHandles.erase(i); 
	backend->lock.acquire();
	delete backend;
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

VBufRemote_nodeHandle_t VBufRemote_locateTextFieldNodeAtOffset(VBufRemote_bufferHandle_t buffer, int offset, int *nodeStartOffset, int *nodeEndOffset) {
	VBufBackend_t* backend=(VBufBackend_t*)buffer;
	backend->lock.acquire();
	VBufRemote_nodeHandle_t res=(VBufRemote_nodeHandle_t)(backend->locateTextFieldNodeAtOffset(offset,nodeStartOffset,nodeEndOffset));
	backend->lock.release();
	return res;
}

VBufRemote_nodeHandle_t VBufRemote_locateControlFieldNodeAtOffset(VBufRemote_bufferHandle_t buffer, int offset, int *nodeStartOffset, int *nodeEndOffset, int *docHandle, int *ID) {
	VBufBackend_t* backend=(VBufBackend_t*)buffer;
	backend->lock.acquire();
	VBufRemote_nodeHandle_t res=(VBufRemote_nodeHandle_t)(backend->locateControlFieldNodeAtOffset(offset,nodeStartOffset,nodeEndOffset,docHandle,ID));
	backend->lock.release();
	return res;
}

VBufRemote_nodeHandle_t VBufRemote_getControlFieldNodeWithIdentifier(VBufRemote_bufferHandle_t buffer, int docHandle, int ID) { 
	VBufBackend_t* backend=(VBufBackend_t*)buffer;
	backend->lock.acquire();
	VBufRemote_nodeHandle_t res=(VBufRemote_nodeHandle_t)(backend->getControlFieldNodeWithIdentifier(docHandle,ID));
	backend->lock.release();
	return res;
}

VBufRemote_nodeHandle_t VBufRemote_findNodeByAttributes(VBufRemote_bufferHandle_t buffer, int offset, int direction, const wchar_t* attribsString, int *startOffset, int *endOffset) { 
	VBufBackend_t* backend=(VBufBackend_t*)buffer;
	backend->lock.acquire();
	VBufRemote_nodeHandle_t res=(VBufRemote_nodeHandle_t)(backend->findNodeByAttributes(offset,(VBufStorage_findDirection_t)direction,attribsString,startOffset,endOffset));
	backend->lock.release();
	return res;
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

int VBufRemote_getTextInRange(VBufRemote_bufferHandle_t buffer, int startOffset, int endOffset, wchar_t** text, int useMarkup) {
	VBufBackend_t* backend=(VBufBackend_t*)buffer;
	std::wstring s;
	backend->lock.acquire();
	int res=backend->getTextInRange(startOffset,endOffset,s,useMarkup);
	backend->lock.release();
	*text=_wcsdup(s.c_str());
	return res;
}

int VBufRemote_getLineOffsets(VBufRemote_bufferHandle_t buffer, int offset, int maxLineLength, int useScreenLayout, int *startOffset, int *endOffset) {
	VBufBackend_t* backend=(VBufBackend_t*)buffer;
	backend->lock.acquire();
	int res=backend->getLineOffsets(offset,maxLineLength,useScreenLayout,startOffset,endOffset);
	backend->lock.release();
	return res;
}

//Special cleanup method for VBufRemote when client is lost
void __RPC_USER VBufRemote_bufferHandle_t_rundown(VBufRemote_bufferHandle_t buffer) {
	VBufRemote_destroyBuffer(&buffer);
}

}
