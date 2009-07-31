#include <remoteApi/remoteApi.h>
#include "container.h"

extern "C" {

VBufRemote_bufferHandle_t VBufRemote_createBuffer(handle_t bindingHandle, int docHandle, int ID, const unsigned char* backendPath) {
	return (VBufRemote_bufferHandle_t)new VBufContainer_t(docHandle,ID,(char*)backendPath);
}

void VBufRemote_destroyBuffer(VBufRemote_bufferHandle_t* buffer) {
	VBufContainer_t* realBuf=(VBufContainer_t*)*buffer;
	realBuf->lock.acquire();
	delete realBuf;
	*buffer=NULL;
}

int VBufRemote_getFieldNodeOffsets(VBufRemote_bufferHandle_t buffer, VBufRemote_nodeHandle_t node, int *startOffset, int *endOffset) {
	VBufContainer_t* realBuf=(VBufContainer_t*)buffer;
	VBufStorage_fieldNode_t* realNode=(VBufStorage_fieldNode_t*)node;
	realBuf->lock.acquire();
	int res=realBuf->getFieldNodeOffsets(realNode,startOffset,endOffset);
	realBuf->lock.release();
	return res;
}

int VBufRemote_isFieldNodeAtOffset(VBufRemote_bufferHandle_t buffer, VBufRemote_nodeHandle_t node, int offset) {
	VBufContainer_t* realBuf=(VBufContainer_t*)buffer;
	VBufStorage_fieldNode_t* realNode=(VBufStorage_fieldNode_t*)node;
	realBuf->lock.acquire();
	int res=realBuf->isFieldNodeAtOffset(realNode,offset);
	realBuf->lock.release();
	return res;
}

VBufRemote_nodeHandle_t VBufRemote_locateTextFieldNodeAtOffset(VBufRemote_bufferHandle_t buffer, int offset, int *nodeStartOffset, int *nodeEndOffset) {
	VBufContainer_t* realBuf=(VBufContainer_t*)buffer;
	realBuf->lock.acquire();
	VBufRemote_nodeHandle_t res=(VBufRemote_nodeHandle_t)(realBuf->locateTextFieldNodeAtOffset(offset,nodeStartOffset,nodeEndOffset));
	realBuf->lock.release();
	return res;
}

VBufRemote_nodeHandle_t VBufRemote_locateControlFieldNodeAtOffset(VBufRemote_bufferHandle_t buffer, int offset, int *nodeStartOffset, int *nodeEndOffset, int *docHandle, int *ID) {
	VBufContainer_t* realBuf=(VBufContainer_t*)buffer;
	realBuf->lock.acquire();
	VBufRemote_nodeHandle_t res=(VBufRemote_nodeHandle_t)(realBuf->locateControlFieldNodeAtOffset(offset,nodeStartOffset,nodeEndOffset,docHandle,ID));
	realBuf->lock.release();
	return res;
}

VBufRemote_nodeHandle_t VBufRemote_getControlFieldNodeWithIdentifier(VBufRemote_bufferHandle_t buffer, int docHandle, int ID) { 
	VBufContainer_t* realBuf=(VBufContainer_t*)buffer;
	realBuf->lock.acquire();
	VBufRemote_nodeHandle_t res=(VBufRemote_nodeHandle_t)(realBuf->getControlFieldNodeWithIdentifier(docHandle,ID));
	realBuf->lock.release();
	return res;
}

VBufRemote_nodeHandle_t VBufRemote_findNodeByAttributes(VBufRemote_bufferHandle_t buffer, int offset, int direction, const wchar_t* attribsString, int *startOffset, int *endOffset) { 
	VBufContainer_t* realBuf=(VBufContainer_t*)buffer;
	realBuf->lock.acquire();
	VBufRemote_nodeHandle_t res=(VBufRemote_nodeHandle_t)(realBuf->findNodeByAttributes(offset,(VBufStorage_findDirection_t)direction,attribsString,startOffset,endOffset));
	realBuf->lock.release();
	return res;
}

int VBufRemote_getSelectionOffsets(VBufRemote_bufferHandle_t buffer, int *startOffset, int *endOffset) {
	VBufContainer_t* realBuf=(VBufContainer_t*)buffer;
	realBuf->lock.acquire();
	int res=realBuf->getSelectionOffsets(startOffset,endOffset);
	realBuf->lock.release();
	return res;
}

int VBufRemote_setSelectionOffsets(VBufRemote_bufferHandle_t buffer, int startOffset, int endOffset) {
	VBufContainer_t* realBuf=(VBufContainer_t*)buffer;
	realBuf->lock.acquire();
	int res=realBuf->setSelectionOffsets(startOffset,endOffset);
	realBuf->lock.release();
	return res;
}

int VBufRemote_getTextLength(VBufRemote_bufferHandle_t buffer) {
	VBufContainer_t* realBuf=(VBufContainer_t*)buffer;
	realBuf->lock.acquire();
	int res=realBuf->getTextLength();
	realBuf->lock.release();
	return res;
}

int VBufRemote_getTextInRange(VBufRemote_bufferHandle_t buffer, int startOffset, int endOffset, wchar_t** text, int useMarkup) {
	VBufContainer_t* realBuf=(VBufContainer_t*)buffer;
	std::wstring s;
	realBuf->lock.acquire();
	int res=realBuf->getTextInRange(startOffset,endOffset,s,useMarkup);
	realBuf->lock.release();
	*text=_wcsdup(s.c_str());
	return res;
}

int VBufRemote_getLineOffsets(VBufRemote_bufferHandle_t buffer, int offset, int maxLineLength, int useScreenLayout, int *startOffset, int *endOffset) {
	VBufContainer_t* realBuf=(VBufContainer_t*)buffer;
	realBuf->lock.acquire();
	int res=realBuf->getLineOffsets(offset,maxLineLength,useScreenLayout,startOffset,endOffset);
	realBuf->lock.release();
	return res;
}

}
