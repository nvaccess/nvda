/**
 * base/backend.cpp
 * Part of the NV  Virtual Buffer Library
 * This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
 * This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
 * http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
 */

#include <cassert>
 #include "debug.h"
#include "storage.h"
#include "backend.h"

VBufBackend_t::VBufBackend_t(int docHandleArg, int IDArg): rootDocHandle(docHandleArg), rootID(IDArg), VBufStorage_buffer_t(), invalidSubtrees() {
	DEBUG_MSG(L"Initializing backend with docHandle "<<docHandleArg<<L", ID "<<IDArg<<L", storageBuffer "<<storageBufferArg);
}

int VBufBackend_t::getRootDocHandle() {
	return rootDocHandle;
}

int VBufBackend_t::getRootID() {
	return rootID;
}

void VBufBackend_t::invalidateSubtree(VBufStorage_controlFieldNode_t* node) {
	assert(node); //node can not be NULL
	DEBUG_MSG(L"Invalidating node "<<node->getDebugInfo());
	for(VBufStorage_controlFieldNodeSet_t::iterator i=invalidSubtrees.begin();i!=invalidSubtrees.end();) {
		VBufStorage_fieldNode_t* existingNode=*i;
		if(node==existingNode) {
			DEBUG_MSG(L"Node already invalidated");
			return;
		} else if(storageBuffer->isDescendantNode(existingNode,node)) {
			DEBUG_MSG(L"An ancestor is already invalidated, returning");
			return;
		} else if(storageBuffer->isDescendantNode(node,existingNode)) {
			DEBUG_MSG(L"removing a descendant node from the invalid nodes");
			invalidSubtrees.erase(i++);
		} else {
			i++;
		}
	}
	DEBUG_MSG(L"Adding node to invalid nodes");
	invalidSubtrees.insert(node);
	DEBUG_MSG(L"invalid subtree count now "<<invalidSubtrees.size());
}

void VBufBackend_t::update() {
	if(this->storageBuffer->hasContent()) {
		DEBUG_MSG(L"Updating "<<invalidSubtrees.size()<<L" subtrees");
		for(VBufStorage_controlFieldNodeSet_t::iterator i=invalidSubtrees.begin();i!=invalidSubtrees.end();i++) {
			VBufStorage_controlFieldNode_t* node=*i;
			DEBUG_MSG(L"re-rendering subtree at "<<node);
			VBufStorage_buffer_t* tempBuf=new VBufStorage_buffer_t();
			assert(tempBuf); //tempBuf can't be NULL
			DEBUG_MSG(L"Created temp buffer at "<<tempBuf);
			int docHandle=0, ID=0;
			node->getIdentifier(&docHandle,&ID);
			DEBUG_MSG(L"subtree node has docHandle "<<docHandle<<L" and ID "<<ID);
			DEBUG_MSG(L"Rendering content");
			render(tempBuf,docHandle,ID,node);
			DEBUG_MSG(L"Rendered content in temp buffer");
			this->storageBuffer->lock.acquire();
			DEBUG_MSG(L"Replacing node with content of temp buffer");
			this->storageBuffer->replaceSubtree(node,tempBuf);
			DEBUG_MSG(L"Merged");
			this->storageBuffer->lock.release();
			DEBUG_MSG(L"Deleting temp buffer");
			delete tempBuf;
			DEBUG_MSG(L"Re-rendered subtree");
		}
		DEBUG_MSG(L"Clearing invalid subtree set");
		invalidSubtrees.clear();
	} else {
		DEBUG_MSG(L"Initial render");
		this->storageBuffer->lock.acquire();
		render(this->storageBuffer,rootDocHandle,rootID);
		this->storageBuffer->lock.release();
	}
	DEBUG_MSG(L"Update complete");
}

VBufBackend_t::~VBufBackend_t() {
	DEBUG_MSG(L"Backend being destroied");
}
