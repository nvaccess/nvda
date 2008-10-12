/**
 * backends/example/example.cpp
 * Part of the NV  Virtual Buffer Library
 * This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
 * This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
 * http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
 */

#include "../../base/base.h"

class __declspec(dllexport) TestVBufBackend_t: public VBufBackend_t {
	public:

	TestVBufBackend_t(int docHandle, int ID, VBufStorage_buffer_t* storageBuffer): VBufBackend_t(docHandle,ID,storageBuffer) {
		DEBUG_MSG(L"Initializing Test backend");
		storageBuffer->lock.acquire();
		VBufStorage_controlFieldNode_t* nodeA=storageBuffer->addControlFieldNode(NULL,NULL,1,1,true);
		nodeA->addAttribute(L"role",L"document");
		VBufStorage_controlFieldNode_t* nodeAA=storageBuffer->addControlFieldNode(nodeA,NULL,1,2,true);
		nodeAA->addAttribute(L"role",L"heading");
		nodeAA->addAttribute(L"level",L"1");
		VBufStorage_textFieldNode_t* nodeAAA=storageBuffer->addTextFieldNode(nodeAA,NULL,L"Test for Virtual Buffer Library");
		VBufStorage_controlFieldNode_t* nodeAB=storageBuffer->addControlFieldNode(nodeA,nodeAA,1,3,true);
		nodeAB->addAttribute(L"role",L"paragraph");
		VBufStorage_textFieldNode_t* nodeABA=storageBuffer->addTextFieldNode(nodeAB,NULL,L"This content has been rendered by the Test backend. For a much better example of how the Virtual buffer library can be used, please visit the ");
		VBufStorage_controlFieldNode_t* nodeABB=storageBuffer->addControlFieldNode(nodeAB,nodeABA,1,4,false);
		nodeABB->addAttribute(L"role",L"link");
		nodeABB->addAttribute(L"value",L"http://www.nvda-project.org/");
		VBufStorage_textFieldNode_t* nodeABBA=storageBuffer->addTextFieldNode(nodeABB,NULL,L"NVDA website");
		VBufStorage_textFieldNode_t* nodeABC=storageBuffer->addTextFieldNode(nodeAB,nodeABB,L"where you can find the NVDA screen reader.");
		VBufStorage_controlFieldNode_t* nodeAC=storageBuffer->addControlFieldNode(nodeA,nodeAB,1,5,true);
		nodeAC->addAttribute(L"role",L"paragraph");
		VBufStorage_textFieldNode_t* nodeACA=storageBuffer->addTextFieldNode(nodeAC,NULL,L"Copyright (c)2008 NV Access");
		storageBuffer->lock.release();
		DEBUG_MSG(L"Test backend initialized");
	}

	~TestVBufBackend_t() {
		DEBUG_MSG(L"Test backend being destroied");
	}

};

extern "C" __declspec(dllexport) VBufBackend_t* VBufBackend_create(int docHandle, int ID, VBufStorage_buffer_t* storageBuffer) {
	VBufBackend_t* backend=new TestVBufBackend_t(docHandle,ID,storageBuffer);
	DEBUG_MSG(L"Created new backend at "<<backend);
	return backend;
}
