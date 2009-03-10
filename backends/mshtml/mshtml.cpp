/**
 * backends/ie_mshtml/ie_mshtml.cpp
 * Part of the NV  Virtual Buffer Library
 * This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
 * This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
 * http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
 */

#define UNICODE
 #include <cassert>
#include <windows.h>
#include <oleacc.h>
#include <mshtml.h>
#include <set>
#include <string>
#include <sstream>
#include <base/base.h>
#include "mshtml.h"

using namespace std;

HINSTANCE backendLibHandle=NULL;
UINT wmMainThreadSetup=0;
UINT wmMainThreadTerminate=0;
UINT WM_HTML_GETOBJECT;
VBufBackendSet_t runningBackends;
UINT_PTR mainThreadTimerID=0;

#pragma comment(linker,"/entry:_DllMainCRTStartup@12")
BOOL WINAPI DllMain(HINSTANCE hModule,DWORD reason,LPVOID lpReserved) {
	if(reason==DLL_PROCESS_ATTACH) {
		backendLibHandle=hModule;
		wmMainThreadSetup=RegisterWindowMessage(L"VBufBackend_ie_mshtml_mainThreadSetup");
		wmMainThreadTerminate=RegisterWindowMessage(L"VBufBackend_ie_mshtml_mainThreadTerminate");
		WM_HTML_GETOBJECT=RegisterWindowMessage(L"WM_HTML_GETOBJECT");
	}
	return TRUE;
}

VBufStorage_fieldNode_t* fillVBuf(VBufStorage_buffer_t* buffer, VBufStorage_controlFieldNode_t* parentNode, VBufStorage_fieldNode_t* previousNode, IHTMLDOMNode* pHTMLDOMNode) {
	IHTMLDOMTextNode* pHTMLDOMTextNode=NULL;
	DEBUG_MSG(L"Trying to get an IHTMLDOMTextNode interface pointer");
	if(pHTMLDOMNode->QueryInterface(IID_IHTMLDOMTextNode,(void**)&pHTMLDOMTextNode)==S_OK) {
		VBufStorage_textFieldNode_t* textNode=NULL;
		DEBUG_MSG(L"Fetch data of DOMTextNode");
		BSTR data=NULL;
		if(pHTMLDOMTextNode->get_data(&data)!=S_OK) {
			DEBUG_MSG(L"Could not get IHTMLDOMTextNode::data");
			pHTMLDOMTextNode->Release();
			return NULL;
		}
		DEBUG_MSG(L"Got data from IHTMLDOMTextNode");
		if(data) {
			textNode=buffer->addTextFieldNode(parentNode,previousNode,data);
			SysFreeString(data);
		}
		pHTMLDOMTextNode->Release();
		return textNode;
	}
	IHTMLUniqueName* pHTMLUniqueName=NULL;
	DEBUG_MSG(L"Try to get IHTMLUniqueName");
	if(pHTMLDOMNode->QueryInterface(IID_IHTMLUniqueName,(void**)&pHTMLUniqueName)!=S_OK) {
		DEBUG_MSG(L"Failed to get IHTMLUniqueName");
		return NULL;
	}
	DEBUG_MSG(L"Got IHTMLUniqueName");
	int docHandle=0;
	int ID=0;
	DEBUG_MSG(L"Getting IHTMLUniqueName::uniqueNumber");
	if(pHTMLUniqueName->get_uniqueNumber((long*)&ID)!=S_OK) {
		DEBUG_MSG(L"IHTMLUniqueName::get_uniqueNumber failed");
		pHTMLUniqueName->Release();
		return NULL;
	}
	DEBUG_MSG(L"Got uniqueNumber of "<<ID);
	pHTMLUniqueName->Release();
	BSTR nodeName=NULL;
	DEBUG_MSG(L"Trying to get IHTMLDOMNode::nodeName");
	if(pHTMLDOMNode->get_nodeName(&nodeName)!=S_OK) {
		DEBUG_MSG(L"Failed to get IHTMLDOMNode::nodeName");
		return NULL;
	}
	assert(nodeName); //Should never be NULL;
	DEBUG_MSG(L"Got IHTMLDOMNode::nodeName of "<<nodeName);
	if(wcscmp(nodeName,L"#comment")==0||wcscmp(nodeName,L"script")==0) {
		DEBUG_MSG(L"nodeName not supported");
		SysFreeString(nodeName);
		return NULL;
	}
	parentNode=buffer->addControlFieldNode(parentNode,previousNode,docHandle,ID,true);
	assert(parentNode);
	previousNode=NULL;
	parentNode->addAttribute(L"IHTMLDOMNode::nodeName",nodeName);
	IHTMLDOMChildrenCollection* pHTMLDOMChildrenCollection=NULL;
	DEBUG_MSG(L"Getting IHTMLDOMNode::childNodes");
	IDispatch* pDispatch=NULL;
	if(pHTMLDOMNode->get_childNodes(&pDispatch)==S_OK) {
		IHTMLDOMChildrenCollection* pHTMLDOMChildrenCollection=NULL;
		if(pDispatch->QueryInterface(IID_IHTMLDOMChildrenCollection,(void**)&pHTMLDOMChildrenCollection)==S_OK) {
			DEBUG_MSG(L"Got IHTMLDOMNode::childNodes");
			DEBUG_MSG(L"Getting IHTMLDOMChildrenCollection::length");
			long length=0;
			pHTMLDOMChildrenCollection->get_length(&length);
			DEBUG_MSG(L"length "<<length);
			for(int i=0;i<length;i++) {
				DEBUG_MSG(L"Fetching child "<<i);
				IDispatch* childPDispatch=NULL;
				if(pHTMLDOMChildrenCollection->item(i,&childPDispatch)!=S_OK) {
					continue;
				}
				IHTMLDOMNode* childPHTMLDOMNode=NULL;
				if(childPDispatch->QueryInterface(IID_IHTMLDOMNode,(void**)&childPHTMLDOMNode)==S_OK) {
					VBufStorage_fieldNode_t* tempNode=fillVBuf(buffer,parentNode,previousNode,childPHTMLDOMNode);
					if(tempNode) {
						previousNode=tempNode;
					}
					childPHTMLDOMNode->Release();
				}
				childPDispatch->Release();
			}
			pHTMLDOMChildrenCollection->Release();
		}
		pDispatch->Release();
	}
	SysFreeString(nodeName);
	return parentNode;
}

void mainThreadSetup(VBufBackend_t* backend) {
	backend->update();
	#ifdef DEBUG
	Beep(220,70);
	#endif
}

LRESULT CALLBACK mainThreadCallWndProcHook(int code, WPARAM wParam,LPARAM lParam) {
	CWPSTRUCT* pcwp=(CWPSTRUCT*)lParam;
	if((code==HC_ACTION)&&(pcwp->message==wmMainThreadSetup)) {
		mainThreadSetup((VBufBackend_t*)(pcwp->wParam));
	}
	return CallNextHookEx(0,code,wParam,lParam);
}

void mainThreadTerminate(VBufBackend_t* backend) {
	#ifdef DEBUG
	Beep(880,70);
	#endif
}

LRESULT CALLBACK mainThreadGetMessageHook(int code, WPARAM wParam,LPARAM lParam) {
	MSG* pmsg=(MSG*)lParam;
	if((code==HC_ACTION)&&(pmsg->message==wmMainThreadTerminate)) {
		mainThreadTerminate((VBufBackend_t*)(pmsg->wParam));
		DEBUG_MSG(L"Removing hook");
		int res=UnhookWindowsHookEx((HHOOK)(pmsg->lParam));
		assert(res!=0); //unHookWindowsHookEx must return non-0
	}
	return CallNextHookEx(0,code,wParam,lParam);
}

void MshtmlVBufBackend_t::render(VBufStorage_buffer_t* buffer, int docHandle, int ID) {
	DEBUG_MSG(L"Rendering from docHandle "<<docHandle<<L", ID "<<ID<<L", in to buffer at "<<buffer);
	DEBUG_MSG(L"Getting document from window "<<docHandle);
	int res=SendMessage((HWND)docHandle,WM_HTML_GETOBJECT,0,0);
	if(res==0) {
		DEBUG_MSG(L"Error getting document using WM_HTML_GETOBJECT");
		return;
	}
	IHTMLDocument3* pHTMLDocument3=NULL;
	if(ObjectFromLresult(res,IID_IHTMLDocument3,0,(void**)&pHTMLDocument3)!=S_OK) {
		DEBUG_MSG(L"Error in ObjectFromLresult");
		return;
	}
	DEBUG_MSG(L"Locating DOM node with ID");
	IHTMLElement* pHTMLElement=NULL;
	wostringstream s;
	s<<L"ms__id"<<ID;
	if(pHTMLDocument3->getElementById((wchar_t*)(s.str().c_str()),(IHTMLElement**)&pHTMLElement)!=S_OK||!pHTMLElement) {
		DEBUG_MSG(L"Failed to find element with ID"<<s.str().c_str());
		pHTMLDocument3->Release();
		return;
	}
	pHTMLDocument3->Release();
	DEBUG_MSG(L"queryInterface to IHTMLDOMNode from IHTMLElement");
	IHTMLDOMNode* pHTMLDOMNode=NULL;
	if(pHTMLElement->QueryInterface(IID_IHTMLDOMNode,(void**)&pHTMLDOMNode)!=S_OK) {
		DEBUG_MSG(L"Could not get IHTMLDOMNode");
		pHTMLElement->Release();
		return;
	}
	pHTMLElement->Release();
	fillVBuf(buffer,NULL,NULL,pHTMLDOMNode);
	pHTMLDOMNode->Release();
}

MshtmlVBufBackend_t::MshtmlVBufBackend_t(int docHandle, int ID, VBufStorage_buffer_t* storageBuffer): VBufBackend_t(docHandle,ID,storageBuffer) {
	int res;
	DEBUG_MSG(L"Initializing MSHTML backend");
	runningBackends.insert(this);
	DEBUG_MSG(L"Setting hook");
	HWND rootWindow=(HWND)rootDocHandle;
	rootThreadID=GetWindowThreadProcessId(rootWindow,NULL);
	HHOOK mainThreadCallWndProcHookID=SetWindowsHookEx(WH_CALLWNDPROC,(HOOKPROC)mainThreadCallWndProcHook,backendLibHandle,rootThreadID);
	assert(mainThreadCallWndProcHookID!=0); //valid hooks are not 0
	DEBUG_MSG(L"Hook set with ID "<<mainThreadCallWndProcHookID);
	DEBUG_MSG(L"Sending wmMainThreadSetup to window, docHandle "<<rootDocHandle<<L", ID "<<rootID<<L", backend "<<this);
	SendMessage(rootWindow,wmMainThreadSetup,(WPARAM)this,0);
	DEBUG_MSG(L"Message sent");
	DEBUG_MSG(L"Removing hook");
	res=UnhookWindowsHookEx(mainThreadCallWndProcHookID);
	assert(res!=0); //unHookWindowsHookEx must return non-0
	DEBUG_MSG(L"MSHTML backend initialized");
}

MshtmlVBufBackend_t::~MshtmlVBufBackend_t() {
	int res;
	DEBUG_MSG(L"MSHTML backend being destroied");
	runningBackends.erase(this);
	DEBUG_MSG(L"Setting hook");
	HHOOK mainThreadGetMessageHookID=SetWindowsHookEx(WH_GETMESSAGE,(HOOKPROC)mainThreadGetMessageHook,backendLibHandle,rootThreadID);
	assert(mainThreadGetMessageHookID!=0); //valid hooks are not 0
	DEBUG_MSG(L"Hook set with ID "<<mainThreadGetMessageHookID);
	DEBUG_MSG(L"Sending wmMainThreadTerminate to thread "<<rootThreadID<<", docHandle "<<rootDocHandle<<L", ID "<<rootID<<L", backend "<<this);
	PostThreadMessage(rootThreadID,wmMainThreadTerminate,(WPARAM)this,(LPARAM)mainThreadGetMessageHookID);
	DEBUG_MSG(L"Message sent");
	DEBUG_MSG(L"MSHTML backend terminated");
}

extern "C" __declspec(dllexport) VBufBackend_t* VBufBackend_create(int docHandle, int ID, VBufStorage_buffer_t* storageBuffer) {
	VBufBackend_t* backend=new MshtmlVBufBackend_t(docHandle,ID,storageBuffer);
	DEBUG_MSG(L"Created new backend at "<<backend);
	return backend;
}
