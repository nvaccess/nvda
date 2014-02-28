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

#include <string>
#include <sstream>
#include <map>
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <oleacc.h>
#include <common/log.h>
#include "nvdaController.h"
#include "nvdaHelperRemote.h"

using namespace std;

#define EVENT_OBJECT_LIVEREGIONCHANGED 0x8019 

bool getTextFromIAccessible(wstring& textBuf, IAccessible* pacc, VARIANT varChild) {
	bool gotText=false;
	long childCount=0;
	LOG_INFO(L"getTextFromIAccessible: pacc "<<pacc<<L", varChild lVal "<<(varChild.lVal));
	if(varChild.lVal==0&&pacc->get_accChildCount(&childCount)==S_OK&&childCount>0) {
		VARIANT* varChildren=new VARIANT[childCount];
		AccessibleChildren(pacc,0,childCount,varChildren,&childCount);
		for(int i=0;i<childCount;++i) {
			if(varChildren[i].vt==VT_DISPATCH) {
				IAccessible* paccChild=NULL;
				if(varChildren[i].pdispVal&&varChildren[i].pdispVal->QueryInterface(IID_IAccessible,(void**)&paccChild)==S_OK) {
					if(getTextFromIAccessible(textBuf,paccChild,varChild)) {
						gotText=true;
					}
					paccChild->Release();
				}
			} else if(varChildren[i].vt==VT_I4) {
				if(getTextFromIAccessible(textBuf,pacc,varChildren[i])) gotText=true;
			}
			VariantClear(varChildren+i);
		}
		delete [] varChildren;
	}
	if(!gotText) {
		//We got no text from  children, so try name and/or description
		BSTR val=NULL;
		bool valEmpty=true;
		pacc->get_accName(varChild,&val);
		if(val) {
			for(int i=0;val[i]!=L'\0';++i) {
				if(val[i]!=L'\xfffc'&&!iswspace(val[i])) {
					valEmpty=false;
					break;
				}
			}
			if(!valEmpty) {
				gotText=true;
				textBuf.append(val);
				textBuf.append(L" ");
			}
			SysFreeString(val);
			val=NULL;
		}
		valEmpty=true;
		pacc->get_accDescription(varChild,&val);
		if(val) {
			for(int i=0;val[i]!=L'\0';++i) {
				if(val[i]!=L'\xfffc'&&!iswspace(val[i])) {
					valEmpty=false;
					break;
				}
			}
			if(!valEmpty) {
				gotText=true;
				textBuf.append(val);
			}
			SysFreeString(val);
		}
	}
	return gotText;
}

map<long,long> childCountCache;

static void CALLBACK winEventProcHook(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time) {
	HWND fgHwnd=GetForegroundWindow();
	//Ignore events for windows that are invisible or are not in the foreground
	if(!IsWindowVisible(hwnd)||(hwnd!=fgHwnd&&!IsChild(fgHwnd,hwnd))) return;
	wchar_t className[256];
	// Don't handle any windows other than Internet Explorer documents
	if(!GetClassName(hwnd,className,256)||wcscmp(className,L"Internet Explorer_Server")!=0) return;
	//Ignore all events but a few types
	if(eventID!=EVENT_OBJECT_LIVEREGIONCHANGED) return;
	IAccessible* pacc=NULL;
	VARIANT varChild;
	//Try getting the IAccessible from the event
	if(AccessibleObjectFromEvent(hwnd,objectID,childID,&pacc,&varChild)!=S_OK) {
		return;
	}
	wstring textBuf;
	bool gotText=false;
	if(varChild.lVal>0) {
		// The event is for an MSAA simpl child element so just announce it
		gotText=getTextFromIAccessible(textBuf,pacc,varChild);
	} else {
		// The event is for a real IAccessible.
		// Either speak any added children, or all of it.
		long& oldChildCount=childCountCache[objectID];
		long newChildCount=0;
		pacc->get_accChildCount(&newChildCount);
		LOG_INFO(L"objectID "<<objectID<<L", newChildCount "<<newChildCount<<L", oldChildCount "<<oldChildCount);
		if(newChildCount>oldChildCount) {
			for(int i=oldChildCount+1;i<=newChildCount;++i) {
				LOG_INFO(L"trying accChild "<<i);
				varChild.lVal=i;
				IDispatch* childDisp=NULL;
				pacc->get_accChild(varChild,&childDisp);
				if(childDisp) {
					LOG_INFO(L"got childDisp "<<childDisp);
					IAccessible* childPacc=NULL;
					childDisp->QueryInterface(IID_IAccessible,(void**)&childPacc);
					if(childPacc) {
						LOG_INFO(L"Got childPacc "<<childPacc);
						varChild.lVal=0;
						if(getTextFromIAccessible(textBuf,childPacc,varChild)) gotText=true;
						childPacc->Release();
					}
					childDisp->Release();
				} else {
					varChild.lVal=i;
					LOG_INFO(L"call getTextFromIAccessible with i "<<i);
					if(getTextFromIAccessible(textBuf,pacc,varChild)) gotText=true;
				}
			}
			oldChildCount=newChildCount;
		} else {
			if(getTextFromIAccessible(textBuf,pacc,varChild)) gotText=true; 
		}
	}
	if(gotText&&!textBuf.empty()) nvdaController_speakText(textBuf.c_str());
}

void mshtmlLiveRegions_inProcess_initialize() {
	registerWinEventHook(winEventProcHook);
}

void mshtmlLiveRegions_inProcess_terminate() {
	unregisterWinEventHook(winEventProcHook);
}
