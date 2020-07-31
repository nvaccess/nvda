/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2007-2016 NV Access Limited
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
#define WIN32_LEAN_AND_MEAN 
#include <windows.h>
#include <remote/nvdaHelperRemote.h>
#include <common/log.h>
#include <remote/nvdaControllerInternal.h>
#include <remote/inProcess.h>
#include "storage.h"
#include "backend.h"

using namespace std;

VBufBackendSet_t VBufBackend_t::runningBackends;

VBufBackend_t::VBufBackend_t(int docHandleArg, int IDArg): renderThreadID(GetWindowThreadProcessId((HWND)UlongToHandle(docHandleArg),NULL)), rootDocHandle(docHandleArg), rootID(IDArg), lock(), renderThreadTimerID(0) {
	LOG_DEBUG(L"Initializing backend with docHandle "<<docHandleArg<<L", ID "<<IDArg);
}

void VBufBackend_t::initialize() {
	int renderThreadID=GetWindowThreadProcessId((HWND)UlongToHandle(rootDocHandle),NULL);
	LOG_DEBUG(L"render threadID "<<renderThreadID);
	registerWindowsHook(WH_CALLWNDPROC,destroy_callWndProcHook);
	auto func = [&] {
		LOG_DEBUG(L"Calling renderThread_initialize on backend at "<<this);
		this->renderThread_initialize();
	};
	LOG_DEBUG(L"Calling execInThread");
	if(!execInThread(renderThreadID,func)) {
		LOG_ERROR(L"Could not execute renderThread_initialize in UI thread");
	} else {
		LOG_DEBUG(L"execInThread complete");
	}
}

void VBufBackend_t::forceUpdate() {
	this->cancelPendingUpdate();
	this->update();
}

LRESULT CALLBACK VBufBackend_t::destroy_callWndProcHook(int code, WPARAM wParam,LPARAM lParam) {
	CWPSTRUCT* pcwp=(CWPSTRUCT*)lParam;
	if((pcwp->message==WM_DESTROY)) {
		LOG_DEBUG(L"WM_DESTROY for "<<(pcwp->hwnd));
		// Copy the set, as it might be mutated by renderThread_terminate() during iteration.
		VBufBackendSet_t backends=runningBackends;
		for(VBufBackendSet_t::iterator i=backends.begin();i!=backends.end();++i) {
			HWND backendHwnd=(HWND)UlongToHandle(((*i)->rootDocHandle));
			if(pcwp->hwnd==backendHwnd) {
				LOG_DEBUG(L"calling renderThread_terminate for WM_DESTROY");
				(*i)->renderThread_terminate();
			}
		}
	}
	return 0;
}

void CALLBACK VBufBackend_t::renderThread_winEventProcHook(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time) {
	if(eventID==EVENT_OBJECT_DESTROY&&objectID==0&&childID==0) {
		LOG_DEBUG(L"Detected destruction of window "<<hwnd);
		// Copy the set, as it might be mutated by renderThread_terminate() during iteration.
		VBufBackendSet_t backends=runningBackends;
		for(VBufBackendSet_t::iterator i=backends.begin();i!=backends.end();++i) {
			if(hwnd==(HWND)UlongToHandle(((*i)->rootDocHandle))||IsChild(hwnd,(HWND)UlongToHandle(((*i)->rootDocHandle)))) {
				LOG_DEBUG(L"Calling renderThread_terminate for backend at "<<*i);
				(*i)->renderThread_terminate();
			}
		}
	}
}

void VBufBackend_t::requestUpdate() {
	if(renderThreadTimerID==0) {
		renderThreadTimerID=SetTimer(0,0,100,renderThread_timerProc);
		nhAssert(renderThreadTimerID);
		LOG_DEBUG(L"Set timer with ID "<<renderThreadTimerID);
	}
}

void VBufBackend_t::cancelPendingUpdate() {
	if(renderThreadTimerID>0) {
		KillTimer(0,renderThreadTimerID);
		renderThreadTimerID=0;
		LOG_DEBUG(L"Killed timer with ID "<<renderThreadTimerID);
	}
}


void CALLBACK VBufBackend_t::renderThread_timerProc(HWND hwnd, UINT msg, UINT_PTR timerID, DWORD time) {
	LOG_DEBUG(L"Timer fired");
	KillTimer(0,timerID);
	int threadID=GetCurrentThreadId();
	VBufBackend_t* backend=NULL;
	for(VBufBackendSet_t::iterator i=runningBackends.begin();i!=runningBackends.end();++i) {
		if((*i)->renderThreadID==threadID&&(*i)->renderThreadTimerID==timerID) {
			backend=*i;
			break;
		}
	}
	if(!backend) {
		// This timer is not associated with any backend.
		// This probably means the timer message was queued before we killed the timer, so just ignore it.
		return;
	}
	LOG_DEBUG(L"Calling update on backend at "<<backend);
	backend->update();
	backend->renderThreadTimerID=0;
}

void VBufBackend_t::renderThread_initialize() {
	LOG_DEBUG(L"Registering winEvent hook for window destructions");
	registerWinEventHook(renderThread_winEventProcHook);
	LOG_DEBUG(L"Calling update on backend at "<<this);
	this->update();
	runningBackends.insert(this);
}

void VBufBackend_t::renderThread_terminate() {
	cancelPendingUpdate();
	unregisterWinEventHook(renderThread_winEventProcHook);
	LOG_DEBUG(L"Unregistered winEvent hook for window destructions");
	LOG_DEBUG(L"Calling clearBuffer on backend at "<<this);
	this->clearBuffer();
	runningBackends.erase(this);
}

bool markNodeAsNonreusableIfInAncestor(VBufStorage_controlFieldNode_t* node, VBufStorage_controlFieldNode_t* ancestor) {
	auto parent=node->getParent();
	if(!parent) {
		return false;
	} else if(parent==ancestor||markNodeAsNonreusableIfInAncestor(parent,ancestor)) {
		node->allowReuseInAncestorUpdate=false;
		return true;
	}
	return false;
}

bool VBufBackend_t::invalidateSubtree(VBufStorage_controlFieldNode_t* node) {
	auto lock=this->lock.scopedAcquire();
	if(!isNodeInBuffer(node)) {
		LOG_DEBUGWARNING(L"Node at "<<node<<L" not in buffer at "<<this);
		return false;
	}
	// If this node requires its parent to be updated, Invalidate the closest ancestor that does not require its parent to be updated. 
	while(node->requiresParentUpdate) {
		node->allowReuseInAncestorUpdate=false;
		auto parent=node->getParent();
		if(!parent) break;
		node=parent;
		LOG_DEBUG(L"node requiresParentUpdate, therefore trying to invalidate parent at "<<node);
	}
	// If this node is already invalidated, do nothing.
	// If this node is the descendant of a node that is already invalidated,
	// Ensure that this node and any of its ancestors (up to but not including) the already invalid node, are marked as non-reusable.
	for(auto i: pendingInvalidSubtreesList) {
		if(i==node) {
			return true;
		} else if(markNodeAsNonreusableIfInAncestor(node,i)) {
			return true;
		}
	}
	// If this node is an ancestor of one or more already invalid nodes,
	// Ensure that the already invalid node and any of its ancestors (up to but not including) this node, are marked as non-reusable. 
	// Then remove those nodes from the invalidation list.
	pendingInvalidSubtreesList.remove_if([node](auto i){
		return markNodeAsNonreusableIfInAncestor(i,node);
	});
	// Now mark this node as invalid.
	pendingInvalidSubtreesList.push_back(node);
	LOG_DEBUG(L"Invalidated node "<<node->getDebugInfo());
	this->requestUpdate();
	return true;
}

void VBufBackend_t::update() {
	if(this->hasContent()) {
		this->lock.acquire();
		LOG_DEBUG(L"Updating "<<pendingInvalidSubtreesList.size()<<L" subtrees");
		pendingInvalidSubtreesList.swap(workingInvalidSubtreesList);
		this->lock.release();
		map<VBufStorage_fieldNode_t*,VBufStorage_buffer_t*> replacementSubtreeMap;
		//render all invalid subtrees, storing each subtree in its own buffer
		for(auto i=workingInvalidSubtreesList.begin();i!=workingInvalidSubtreesList.end();) {
			VBufStorage_controlFieldNode_t* node=*i;
			LOG_DEBUG(L"re-rendering subtree from "<<node->getDebugInfo());
			VBufStorage_buffer_t* tempBuf=new VBufStorage_buffer_t();
			nhAssert(tempBuf); //tempBuf can't be NULL
			LOG_DEBUG(L"Created temp buffer at "<<tempBuf);
			int docHandle=0, ID=0;
			node->getIdentifier(&docHandle,&ID);
			LOG_DEBUG(L"subtree node has docHandle "<<docHandle<<L" and ID "<<ID);
			LOG_DEBUG(L"Rendering content");
			render(tempBuf,docHandle,ID,node);
			LOG_DEBUG(L"Rendered content in temp buffer");
			replacementSubtreeMap.insert(make_pair(node,tempBuf));
			workingInvalidSubtreesList.erase(i++);
		}
		workingInvalidSubtreesList.clear();
		this->lock.acquire();
		LOG_DEBUG(L"Replacing nodes with content of temp buffers");
		if(!this->replaceSubtrees(replacementSubtreeMap)) {
			LOG_DEBUGWARNING(L"Error replacing one or more subtrees");
		}
		this->lock.release();
		nvdaControllerInternal_vbufChangeNotify(this->rootDocHandle,this->rootID);
	} else {
		LOG_DEBUG(L"Initial render");
		this->lock.acquire();
		render(this,rootDocHandle,rootID);
		this->lock.release();
	}
	LOG_DEBUG(L"Update complete");
}

void VBufBackend_t::terminate() {
	if(runningBackends.count(this)>0) {
		LOG_DEBUG(L"Render thread not terminated yet");
		int renderThreadID=GetWindowThreadProcessId((HWND)UlongToHandle(rootDocHandle),NULL);
		LOG_DEBUG(L"render threadID "<<renderThreadID);
		auto func = [&] {
			LOG_DEBUG(L"Calling renderThread_terminate on backend at "<<this);
			this->renderThread_terminate();
		};
		LOG_DEBUG(L"Calling execInThread");
		if(!execInThread(renderThreadID,func)) {
			LOG_ERROR(L"Could not execute renderThread_terminate in UI thread");
		} else {
			LOG_DEBUG(L"execInThread complete");
		}
	} else {
		LOG_DEBUG(L"render thread already terminated");
	}
	unregisterWindowsHook(WH_CALLWNDPROC,destroy_callWndProcHook);
}

void VBufBackend_t::destroy() {
	delete this;
}

VBufBackend_t::~VBufBackend_t() {
	LOG_DEBUG(L"base Backend destructor called"); 
	nhAssert(runningBackends.count(this) == 0);
}

VBufStorage_controlFieldNode_t* VBufBackend_t::reuseExistingNodeInRender(VBufStorage_controlFieldNode_t* parent, VBufStorage_fieldNode_t* previous, int docHandle, int ID) {
	LOG_DEBUG(L"Try to reuse node with docHandle "<<docHandle<<L", and ID "<<ID);
	if(!parent) {
		LOG_DEBUG(L"Cannot reuse a node at the root");
		return nullptr;
	}
	if(parent->alwaysRerenderDescendants||parent->alwaysRerenderChildren) {
		LOG_DEBUG(L"Won't  find a node to reuse as parent says always rerender children");
		return nullptr;
	}
	// Locate a possible existing node with the given docHandle and ID
	auto existingNode=this->getControlFieldNodeWithIdentifier(docHandle,ID);
	if(!existingNode) {
		LOG_DEBUG(L"Could not locate a node with docHandle "<<docHandle<<L", and ID "<<ID);
		return nullptr;
	}
	// Ensure the node allows us to reuse it
	if(!existingNode->allowReuseInAncestorUpdate) {
		LOG_DEBUG(L"Existing node refuses to be reused");
		return nullptr;
	}
	// Don't reuse the node if it has no parent (is the root of the buffer).
	auto existingParent=existingNode->getParent();
	if(!existingParent) {
		LOG_DEBUG(L"existing node has no parent. Not reusing.");
		return nullptr;
	}
	// alwaysRerenderDescendants can be set after rendering to indicate that we
	// must not reuse descendants.
	if (existingParent->alwaysRerenderDescendants) {
		// Propagate to descendants.
		existingNode->alwaysRerenderDescendants = true;
	}
	if ( existingNode->alwaysRerenderDescendants) {
		LOG_DEBUG(L"Existing node and its descendants must not be reused");
		return nullptr;
	}
	if(existingNode->denyReuseIfPreviousSiblingsChanged) {
		// This node is not allowed to be reused if any of its previous siblings have changed.
		// We work this out by walking back to the previous controlFieldNode in its siblings, and ensuring that it is a reference node that references the existing node's first previous controlFieldNode.
		// As we know that buffers are always rendered in a forward direction, we can garantee that if the previous controlFieldNode is correct,
		// then all previous nodes before that are also correct.
		VBufStorage_controlFieldNode_t* previousControlFieldNode=nullptr;
		for(auto tempNode=previous;tempNode!=nullptr;tempNode=tempNode->getPrevious()) {
			previousControlFieldNode=dynamic_cast<VBufStorage_controlFieldNode_t*>(tempNode);
			if(previousControlFieldNode) break;
		}
		VBufStorage_referenceNode_t* previousReferenceNode=dynamic_cast<VBufStorage_referenceNode_t*>(previousControlFieldNode);
		if(previousControlFieldNode&&!previousReferenceNode) {
			// This is a controlFieldNode but not a referenceNode.
			// Therefore this node has been newly added.
			LOG_DEBUG(L"Previous controlFieldNode was not a referenceNode");
			return nullptr;
		}
		if(previousReferenceNode) {
			previousControlFieldNode=previousReferenceNode->referenceNode;
		}
		VBufStorage_controlFieldNode_t* previousExistingControlFieldNode=nullptr;
		for(auto tempNode=existingNode->getPrevious();tempNode!=nullptr;tempNode=tempNode->getPrevious()) {
			previousExistingControlFieldNode=dynamic_cast<VBufStorage_controlFieldNode_t*>(tempNode);
			if(previousExistingControlFieldNode) break;
		}
		if(previousControlFieldNode!=previousExistingControlFieldNode) {
			// The previous node differs from the existing previous node.
			// We already know it's not because a node was added, therefore this must be either a removal or a move.
			// either way, this means that  the given node's previous siblings have changed.
			LOG_DEBUG(L"Previous controlFieldNodes differ");
			return nullptr;
		}
	}
	auto i=std::find(this->workingInvalidSubtreesList.begin(),this->workingInvalidSubtreesList.end(),existingNode);
	if(i!=this->workingInvalidSubtreesList.end()) {
		LOG_DEBUG(L"Existing node was already marked as invalid. Can't reuse it.");
		// This existing node was marked as invalid, so the caller must now re-render it.
		this->workingInvalidSubtreesList.erase(i);
		return nullptr;
	}
	// This existing node was not marked as invalid, therefore it can be re-used.
	LOG_DEBUG(L"Reusing existing node at "<<existingNode);
	return existingNode;
}
