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

#include <cassert>
#include <windows.h>
#include <remote/nvdaHelperRemote.h>
#include <remote/log.h>
#include "storage.h"
#include "backend.h"

const UINT VBufBackend_t::wmRenderThreadInitialize=RegisterWindowMessage(L"VBufBackend_t::wmRenderThreadInitialize");
const UINT VBufBackend_t::wmRenderThreadTerminate=RegisterWindowMessage(L"VBufBackend_t::wmRenderThreadTerminate");

VBufBackendSet_t VBufBackend_t::runningBackends;

VBufBackend_t::VBufBackend_t(int docHandleArg, int IDArg): renderThreadID(GetWindowThreadProcessId((HWND)docHandleArg,NULL)), rootDocHandle(docHandleArg), rootID(IDArg), lock(), renderThreadTimerID(0), invalidSubtrees() {
	LOG_DEBUG(L"Initializing backend with docHandle "<<docHandleArg<<L", ID "<<IDArg);
}

void VBufBackend_t::initialize() {
	int renderThreadID=GetWindowThreadProcessId((HWND)rootDocHandle,NULL);
	LOG_DEBUG(L"render threadID "<<renderThreadID);
	registerWindowsHook(WH_CALLWNDPROC,renderThread_callWndProcHook);
	LOG_DEBUG(L"Registered hook, sending message...");
	SendMessage((HWND)rootDocHandle,wmRenderThreadInitialize,(WPARAM)this,0);
	LOG_DEBUG(L"Message sent, unregistering hook");
	unregisterWindowsHook(WH_CALLWNDPROC,renderThread_callWndProcHook);
}

LRESULT CALLBACK VBufBackend_t::renderThread_callWndProcHook(int code, WPARAM wParam,LPARAM lParam) {
	CWPSTRUCT* pcwp=(CWPSTRUCT*)lParam;
	if((pcwp->message==wmRenderThreadInitialize)) {
		LOG_DEBUG(L"Calling renderThread_initialize on backend at "<<pcwp->wParam);
		((VBufBackend_t*)(pcwp->wParam))->renderThread_initialize();
	} else if((pcwp->message==wmRenderThreadTerminate)) {
		LOG_DEBUG(L"Calling renderThread_terminate on backend at "<<pcwp->wParam);
		((VBufBackend_t*)(pcwp->wParam))->renderThread_terminate();
	}
	return 0;
}

void CALLBACK VBufBackend_t::renderThread_winEventProcHook(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time) {
	if(eventID==EVENT_OBJECT_DESTROY&&objectID==0&&childID==0) {
		LOG_DEBUG(L"Detected destruction of window "<<hwnd);
		// Copy the set, as it might be mutated by renderThread_terminate() during iteration.
		VBufBackendSet_t backends=runningBackends;
		for(VBufBackendSet_t::iterator i=backends.begin();i!=backends.end();++i) {
			if(hwnd==(HWND)((*i)->rootDocHandle)||IsChild(hwnd,(HWND)((*i)->rootDocHandle))) {
				LOG_DEBUG(L"Calling renderThread_terminate for backend at "<<*i);
				(*i)->renderThread_terminate();
			}
		}
	}
}

void VBufBackend_t::requestUpdate() {
	if(renderThreadTimerID==0) {
		renderThreadTimerID=SetTimer(0,0,250,renderThread_timerProc);
		assert(renderThreadTimerID);
		LOG_DEBUG(L"Set timer with ID "<<renderThreadTimerID);
	}
}

void VBufBackend_t::cancelPendingUpdate() {
	if(renderThreadTimerID>0) {
		KillTimer(0,renderThreadTimerID);
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

void VBufBackend_t::invalidateSubtree(VBufStorage_controlFieldNode_t* node) {
	assert(node); //node can not be NULL
	LOG_DEBUG(L"Invalidating node "<<node->getDebugInfo());
	for(VBufStorage_controlFieldNodeSet_t::iterator i=invalidSubtrees.begin();i!=invalidSubtrees.end();) {
		VBufStorage_fieldNode_t* existingNode=*i;
		if(node==existingNode) {
			LOG_DEBUG(L"Node already invalidated");
			return;
		} else if(isDescendantNode(existingNode,node)) {
			LOG_DEBUG(L"An ancestor is already invalidated, returning");
			return;
		} else if(isDescendantNode(node,existingNode)) {
			LOG_DEBUG(L"removing a descendant node from the invalid nodes");
			invalidSubtrees.erase(i++);
		} else {
			++i;
		}
	}
	LOG_DEBUG(L"Adding node to invalid nodes");
	invalidSubtrees.insert(node);
	LOG_DEBUG(L"invalid subtree count now "<<invalidSubtrees.size());
	this->requestUpdate();
}

void VBufBackend_t::update() {
	if(this->hasContent()) {
		LOG_DEBUG(L"Updating "<<invalidSubtrees.size()<<L" subtrees");
		for(VBufStorage_controlFieldNodeSet_t::iterator i=invalidSubtrees.begin();i!=invalidSubtrees.end();++i) {
			VBufStorage_controlFieldNode_t* node=*i;
			LOG_DEBUG(L"re-rendering subtree at "<<node);
			VBufStorage_buffer_t* tempBuf=new VBufStorage_buffer_t();
			assert(tempBuf); //tempBuf can't be NULL
			LOG_DEBUG(L"Created temp buffer at "<<tempBuf);
			int docHandle=0, ID=0;
			node->getIdentifier(&docHandle,&ID);
			LOG_DEBUG(L"subtree node has docHandle "<<docHandle<<L" and ID "<<ID);
			LOG_DEBUG(L"Rendering content");
			render(tempBuf,docHandle,ID,node);
			LOG_DEBUG(L"Rendered content in temp buffer");
			this->lock.acquire();
			LOG_DEBUG(L"Replacing node with content of temp buffer");
			this->replaceSubtree(node,tempBuf);
			LOG_DEBUG(L"Merged");
			this->lock.release();
			LOG_DEBUG(L"Deleting temp buffer");
			delete tempBuf;
			LOG_DEBUG(L"Re-rendered subtree");
		}
		LOG_DEBUG(L"Clearing invalid subtree set");
		invalidSubtrees.clear();
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
		int renderThreadID=GetWindowThreadProcessId((HWND)rootDocHandle,NULL);
		LOG_DEBUG(L"render threadID "<<renderThreadID);
		registerWindowsHook(WH_CALLWNDPROC,renderThread_callWndProcHook);
		LOG_DEBUG(L"Registered hook, sending message...");
		SendMessage((HWND)rootDocHandle,wmRenderThreadTerminate,(WPARAM)this,0);
		LOG_DEBUG(L"Message sent, unregistering hook");
		unregisterWindowsHook(WH_CALLWNDPROC,renderThread_callWndProcHook);
	} else {
		LOG_DEBUG(L"render thread already terminated");
	}
}

void VBufBackend_t::destroy() {
	delete this;
}

VBufBackend_t::~VBufBackend_t() {
	LOG_DEBUG(L"base Backend destructor called"); 
	assert(runningBackends.count(this) == 0);
}
