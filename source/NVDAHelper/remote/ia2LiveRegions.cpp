#include <string>
#include <sstream>
#include <windows.h>
#include <ia2/ia2.h>
#include <interfaces/nvdaController/nvdaController.h>
#include <common/ia2utils.h>
#include "nvdaHelperRemote.h"

using namespace std;

handle_t bindingHandle;

void speakText(const wchar_t* text) {
	RpcTryExcept {
		nvdaController_speakText(bindingHandle,text);
	} RpcExcept(1) {
		return;
	} RpcEndExcept; 
}

void getTextFromIAccessible(wstring& textBuf, IAccessible2* pacc2, bool useNewText=false, bool recurse=true) {
	IAccessibleText* paccText=NULL;
	if(pacc2->QueryInterface(IID_IAccessibleText,(void**)&paccText)!=S_OK||!paccText) {
		long childCount=0;
		if(pacc2->get_accChildCount(&childCount)!=S_OK) {
			textBuf.append(L"unknown");
			return;
		}
		VARIANT* varChildren=new VARIANT[childCount];
		AccessibleChildren(pacc2,0,childCount,varChildren,&childCount);
		for(int i=0;i<childCount;i++) {
			if(varChildren[i].vt==VT_DISPATCH) {
				IAccessible2* pacc2Child=NULL;
				if(varChildren[i].pdispVal->QueryInterface(IID_IAccessible2,(void**)&pacc2Child)==S_OK) {
					getTextFromIAccessible(textBuf,pacc2Child,false,true);
					pacc2Child->Release();
				}
			}
			VariantClear(varChildren+i);
		}
		delete varChildren;
		return;
	}
	//We can use IAccessibleText because it exists
	BSTR bstrText=NULL;
	long startOffset=0;
	//If requested, get the text from IAccessibleText::newText rather than just IAccessibleText::text.
	if(useNewText) {
		IA2TextSegment newSeg={0};
		if(paccText->get_newText(&newSeg)==S_OK&&newSeg.text) {
			bstrText=newSeg.text;
			startOffset=newSeg.start;
		}
	} else {
		paccText->get_text(0,-1,&bstrText);
	}
	//If we got text, add it to  the string provided, however if there are embedded objects in the text, recurse in to these
	if(bstrText) {
		long textLength=SysStringLen(bstrText);
		IAccessibleHypertext* paccHypertext=NULL;
		if(!recurse||pacc2->QueryInterface(IID_IAccessibleHypertext,(void**)&paccHypertext)!=S_OK) paccHypertext=NULL;
		if(!paccHypertext) {
			textBuf.append(bstrText);
		} else {
			for(long index=0;index<textLength;index++) {
				wchar_t realChar=bstrText[index];
				bool charAdded=false;
				if(realChar==L'\xfffc') {
					long hyperlinkIndex;
					if(paccHypertext&&paccHypertext->get_hyperlinkIndex(startOffset+index,&hyperlinkIndex)==S_OK) {
						IAccessibleHyperlink* paccHyperlink=NULL;
						if(paccHypertext->get_hyperlink(hyperlinkIndex,&paccHyperlink)==S_OK) {
							IAccessible2* pacc2Child=NULL;
							if(paccHyperlink->QueryInterface(IID_IAccessible2,(void**)&pacc2Child)==S_OK) {
								getTextFromIAccessible(textBuf,pacc2Child);
								charAdded=true;
								pacc2Child->Release();
							}
							paccHyperlink->Release();
						}
					}
				}
				if(!charAdded) {
					textBuf.append(1,realChar);
					charAdded=true;
				}
			}
			paccHypertext->Release();
		}
		SysFreeString(bstrText);
		textBuf.append(1,L' ');
	}
	paccText->Release();
}

void CALLBACK winEventProcHook(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time) { 
	HWND fgHwnd=GetForegroundWindow();
	//Ignore events for windows that are invisible or are not in the foreground
	if(!IsWindowVisible(hwnd)||(hwnd!=fgHwnd&&!IsChild(fgHwnd,hwnd))) return;
	//Ignore all events but a few types
	switch(eventID) {
		case EVENT_OBJECT_SHOW:
		case EVENT_OBJECT_HIDE:
		case IA2_EVENT_TEXT_INSERTED:
		break;
		default:
		return;
	}
	IAccessible* pacc=NULL;
	IServiceProvider* pserv=NULL;
	IAccessible2* pacc2=NULL;
	VARIANT varChild;
	//Try getting the IAccessible from the event
	if(AccessibleObjectFromEvent(hwnd,objectID,childID,&pacc,&varChild)!=S_OK) {
		return;
	}
	//Retreave the object states, and if its invisible or offscreen ignore the event.
	VARIANT varState;
	pacc->get_accState(varChild,&varState);
	VariantClear(&varChild);
	if(varState.vt==VT_I4&&(varState.lVal&STATE_SYSTEM_INVISIBLE)) {
		VariantClear(&varState);
		pacc->Release();
		return;
	}
	VariantClear(&varState);
	//Retreave an IAccessible2 via IServiceProvider if it exists.
	pacc->QueryInterface(IID_IServiceProvider,(void**)(&pserv));
	pacc->Release();
	if(!pserv) return; 
	pserv->QueryService(IID_IAccessible,IID_IAccessible2,(void**)(&pacc2));
	pserv->Release();
	if(!pacc2) return;
	//Retreave the IAccessible2 attributes, and if the object is not a live region then ignore the event.
	BSTR attribs=NULL;
	pacc2->get_attributes(&attribs);
	if(!attribs) {
		pacc2->Release();
		return;
	}
	map<wstring,wstring> attribsMap;
	IA2AttribsToMap(attribs,attribsMap);
	SysFreeString(attribs);
	map<wstring,wstring>::iterator i;
	i=attribsMap.find(L"container-live");
	bool live=(i!=attribsMap.end()&&(i->second.compare(L"polite")==0||i->second.compare(L"assertive")==0||i->second.compare(L"rude")==0));
	if(!live) {
		pacc2->Release();
		return;
	}
	i=attribsMap.find(L"container-relevant");
	bool allowAdditions=false;
	bool allowText=false;
	//If relevant is not specify we will default to additions and text, if all is specified then we also use additions and text
	if(i==attribsMap.end()||i->second.compare(L"all")==0) {
		allowText=allowAdditions=true;
	} else { //we support additions if its specified, we support text if its specified
		allowText=(i->second.find(L"text",0)!=wstring::npos);
		allowAdditions=(i->second.find(L"additions",0)!=wstring::npos);
	} 
	//If additions and text are specified, and this is a show event, turn off allowText if this IAccessible's parent doesn't support accessibleText.
	//This is necessary so that we still announce additions via the show event, rather than waiting for the textInserted event which will never arrive.
	if(allowText&&allowAdditions&&eventID==EVENT_OBJECT_SHOW) {
		IDispatch* pdispParent=NULL;
		pacc2->get_accParent(&pdispParent);
		if(pdispParent) {
			IAccessibleText* paccTextParent=NULL;
			if(pdispParent->QueryInterface(IID_IAccessibleText,(void**)&paccTextParent)!=S_OK) {
				allowText=false;
			} else {
				paccTextParent->Release();
			}
			pdispParent->Release();
		}
	}
	wstring textBuf;
	if(!allowText&&allowAdditions&&eventID==EVENT_OBJECT_SHOW) {
		getTextFromIAccessible(textBuf,pacc2,false,true);
	} else if(allowText&&eventID==IA2_EVENT_TEXT_INSERTED) {
 		getTextFromIAccessible(textBuf,pacc2,true,allowAdditions);
	}
	if(!textBuf.empty()) speakText(textBuf.c_str());
}

void ia2LiveRegions_inProcess_initialize() {
	RpcBindingFromStringBinding((RPC_WSTR)L"ncalrpc:[nvdaController]",&bindingHandle);
	registerWinEventHook(winEventProcHook);
}

void ia2LiveRegions_inProcess_terminate() {
	unregisterWinEventHook(winEventProcHook);
	RpcBindingFree(&bindingHandle);
}
