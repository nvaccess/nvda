/**
 * base/backend.cpp
 * Part of the NV  Virtual Buffer Library
 * This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
 * This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
 * http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
 */

#include <cassert>
#include <windows.h>
#include <remote/nvdaHelperRemote.h>
#include "debug.h"
#include "storage.h"
#include "backend.h"

const UINT VBufBackend_t::wmRenderThreadInitialize=RegisterWindowMessage(L"VBufBackend_t::wmRenderThreadInitialize");
const UINT VBufBackend_t::wmRenderThreadTerminate=RegisterWindowMessage(L"VBufBackend_t::wmRenderThreadTerminate");

VBufBackendSet_t VBufBackend_t::runningBackends;

VBufBackend_t::VBufBackend_t(int docHandleArg, int IDArg): renderThreadID(GetWindowThreadProcessId((HWND)docHandleArg,NULL)), rootDocHandle(docHandleArg), rootID(IDArg), lock(), renderThreadTimerID(0), invalidSubtrees() {
	DEBUG_MSG(L"Initializing backend with docHandle "<<docHandleArg<<L", ID "<<IDArg);
}

void VBufBackend_t::initialize() {
	int renderThreadID=GetWindowThreadProcessId((HWND)rootDocHandle,NULL);
	DEBUG_MSG(L"render threadID "<<renderThreadID);
	registerWindowsHook(WH_CALLWNDPROC,renderThread_callWndProcHook);
	DEBUG_MSG(L"Registered hook, sending message...");
	SendMessage((HWND)rootDocHandle,wmRenderThreadInitialize,(WPARAM)this,0);
	DEBUG_MSG(L"Message sent, unregistering hook");
	unregisterWindowsHook(WH_CALLWNDPROC,renderThread_callWndProcHook);
}

LRESULT CALLBACK VBufBackend_t::renderThread_callWndProcHook(int code, WPARAM wParam,LPARAM lParam) {
	CWPSTRUCT* pcwp=(CWPSTRUCT*)lParam;
	if((pcwp->message==wmRenderThreadInitialize)) {
		DEBUG_MSG(L"Calling renderThread_initialize on backend at "<<pcwp->wParam);
		((VBufBackend_t*)(pcwp->wParam))->renderThread_initialize();
	} else if((pcwp->message==wmRenderThreadTerminate)) {
		DEBUG_MSG(L"Calling renderThread_terminate on backend at "<<pcwp->wParam);
		((VBufBackend_t*)(pcwp->wParam))->renderThread_terminate();
	}
	return 0;
}

void CALLBACK VBufBackend_t::renderThread_winEventProcHook(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time) {
	if(eventID==EVENT_OBJECT_DESTROY&&objectID==0&&childID==0) {
		DEBUG_MSG(L"Detected destruction of window "<<hwnd);
		for(VBufBackendSet_t::iterator i=runningBackends.begin();i!=runningBackends.end();i++) {
			if(hwnd==(HWND)((*i)->rootDocHandle)||IsChild(hwnd,(HWND)((*i)->rootDocHandle))) {
				DEBUG_MSG(L"Calling renderThread_terminate for backend at "<<*i);
				(*i)->renderThread_terminate();
			}
		}
	}
}

void VBufBackend_t::requestUpdate() {
	if(renderThreadTimerID==0) {
		renderThreadTimerID=SetTimer(0,0,250,renderThread_timerProc);
		assert(renderThreadTimerID);
		DEBUG_MSG(L"Set timer with ID "<<renderThreadTimerID);
	}
}

void VBufBackend_t::cancelPendingUpdate() {
	if(renderThreadTimerID>0) {
		KillTimer(0,renderThreadTimerID);
		DEBUG_MSG(L"Killed timer with ID "<<renderThreadTimerID);
	}
}


void CALLBACK VBufBackend_t::renderThread_timerProc(HWND hwnd, UINT msg, UINT_PTR timerID, DWORD time) {
	DEBUG_MSG(L"Timer fired");
	KillTimer(0,timerID);
	int threadID=GetCurrentThreadId();
	VBufBackend_t* backend=NULL;
	for(VBufBackendSet_t::iterator i=runningBackends.begin();i!=runningBackends.end();i++) {
		if((*i)->renderThreadID==threadID&&(*i)->renderThreadTimerID==timerID) {
			backend=*i;
			break;
		}
	}
	assert(backend); //Timer must be associated with a backend
	DEBUG_MSG(L"Calling update on backend at "<<backend);
	backend->update();
	backend->renderThreadTimerID=0;
}

void VBufBackend_t::renderThread_initialize() {
	DEBUG_MSG(L"Registering winEvent hook for window destructions");
	registerWinEventHook(renderThread_winEventProcHook);
	DEBUG_MSG(L"Calling update on backend at "<<backend);
	this->update();
	runningBackends.insert(this);
}

void VBufBackend_t::renderThread_terminate() {
	cancelPendingUpdate();
	unregisterWinEventHook(renderThread_winEventProcHook);
	DEBUG_MSG(L"Unregistered winEvent hook for window destructions");
	DEBUG_MSG(L"Calling clearBuffer on backend at "<<backend);
	this->clearBuffer();
	runningBackends.erase(this);
}

void VBufBackend_t::invalidateSubtree(VBufStorage_controlFieldNode_t* node) {
	assert(node); //node can not be NULL
	DEBUG_MSG(L"Invalidating node "<<node->getDebugInfo());
	for(VBufStorage_controlFieldNodeSet_t::iterator i=invalidSubtrees.begin();i!=invalidSubtrees.end();) {
		VBufStorage_fieldNode_t* existingNode=*i;
		if(node==existingNode) {
			DEBUG_MSG(L"Node already invalidated");
			return;
		} else if(isDescendantNode(existingNode,node)) {
			DEBUG_MSG(L"An ancestor is already invalidated, returning");
			return;
		} else if(isDescendantNode(node,existingNode)) {
			DEBUG_MSG(L"removing a descendant node from the invalid nodes");
			invalidSubtrees.erase(i++);
		} else {
			i++;
		}
	}
	DEBUG_MSG(L"Adding node to invalid nodes");
	invalidSubtrees.insert(node);
	DEBUG_MSG(L"invalid subtree count now "<<invalidSubtrees.size());
	this->requestUpdate();
}

void VBufBackend_t::update() {
	if(this->hasContent()) {
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
			this->lock.acquire();
			DEBUG_MSG(L"Replacing node with content of temp buffer");
			this->replaceSubtree(node,tempBuf);
			DEBUG_MSG(L"Merged");
			this->lock.release();
			DEBUG_MSG(L"Deleting temp buffer");
			delete tempBuf;
			DEBUG_MSG(L"Re-rendered subtree");
		}
		DEBUG_MSG(L"Clearing invalid subtree set");
		invalidSubtrees.clear();
	} else {
		DEBUG_MSG(L"Initial render");
		this->lock.acquire();
		render(this,rootDocHandle,rootID);
		this->lock.release();
	}
	DEBUG_MSG(L"Update complete");
}

void VBufBackend_t::terminate() {
	if(runningBackends.count(this)>0) {
		DEBUG_MSG(L"Render thread not terminated yet");
		int renderThreadID=GetWindowThreadProcessId((HWND)rootDocHandle,NULL);
		DEBUG_MSG(L"render threadID "<<renderThreadID);
		registerWindowsHook(WH_CALLWNDPROC,renderThread_callWndProcHook);
		DEBUG_MSG(L"Registered hook, sending message...");
		SendMessage((HWND)rootDocHandle,wmRenderThreadTerminate,(WPARAM)this,0);
		DEBUG_MSG(L"Message sent, unregistering hook");
		unregisterWindowsHook(WH_CALLWNDPROC,renderThread_callWndProcHook);
	} else {
		DEBUG_MSG(L"render thread already terminated");
	}
}

void VBufBackend_t::destroy() {
	delete this;
}

VBufBackend_t::~VBufBackend_t() {
	DEBUG_MSG(L"base Backend destructor called"); 
}
