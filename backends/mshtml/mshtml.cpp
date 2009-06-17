/**
 * backends/mshtml/mshtml.cpp
 * Part of the NV  Virtual Buffer Library
 * This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
 * This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
 * http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
 */

#define UNICODE
 #include <cassert>
#include <windows.h>
#include <oleacc.h>
#include <oleidl.h>
#include <mshtml.h>
#include <set>
#include <string>
#include <sstream>
#include <base/base.h>
#include "node.h"
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

void CALLBACK mainThreadTimerProc(HWND hwnd, UINT msg, UINT_PTR timerID, DWORD time) {
	DEBUG_MSG(L"timer firing!");
	KillTimer(0,mainThreadTimerID);
	mainThreadTimerID=0;
	DEBUG_MSG(L"Updating "<<runningBackends.size()<<L" backends");
	for(VBufBackendSet_t::iterator i=runningBackends.begin();i!=runningBackends.end();i++) {
		DEBUG_MSG(L"Updating backend at "<<(*i));
		(*i)->update();
	}
	DEBUG_MSG(L"All updated");
}

inline IAccessible* getIAccessibleFromHTMLDOMNode(IHTMLDOMNode* pHTMLDOMNode) {
	int res=0;
	IServiceProvider* pServProv=NULL;
	res=pHTMLDOMNode->QueryInterface(IID_IServiceProvider,(void**)&pServProv);
	if(res!=S_OK||!pServProv) {
		DEBUG_MSG(L"Could not queryInterface to IServiceProvider");
		return NULL;
	}
	IAccessible* pacc=NULL;
	res=pServProv->QueryService(IID_IAccessible,IID_IAccessible,(void**)&pacc);
	pServProv->Release();
	if(res!=S_OK||!pacc) {
		DEBUG_MSG(L"Could not get IAccessible interface");
		return NULL;
	}
	return pacc;
}

inline void getIAccessibleInfo(IAccessible* pacc, int* role, int* states, wstring* keyboardShortcut) {
	*role=0;
	*states=0;
	int res=0;
	VARIANT varChild;
	varChild.vt=VT_I4;
	varChild.lVal=0;
	BSTR bstrVal=NULL;
	VARIANT varRole;
	VariantInit(&varRole);
	res=pacc->get_accRole(varChild,&varRole);
	if(res==S_OK&&varRole.vt==VT_I4) {
		*role=varRole.lVal;
	} else {
		DEBUG_MSG(L"Failed to get role");
	}
	VariantClear(&varRole);
	VARIANT varState;
	VariantInit(&varState);
	res=pacc->get_accState(varChild,&varState);
	if(res==S_OK&&varState.vt==VT_I4) {
		*states=varState.lVal;
	} else {
		DEBUG_MSG(L"Failed to get states");
	}
	VariantClear(&varState);
	if(pacc->get_accKeyboardShortcut(varChild,&bstrVal)==S_OK&&bstrVal!=NULL) {
		keyboardShortcut->append(bstrVal);
		SysFreeString(bstrVal);
	} else {
		DEBUG_MSG(L"IAccessible::get_accKeyboardShortcut failed");
	}
}

inline IHTMLDOMNode* getRootDOMNodeFromIAccessibleFrame(IAccessible* pacc) {
int res=0;
	VARIANT varChild;
	varChild.vt=VT_I4;
	varChild.lVal=1;
	IDispatch* pDispatch=NULL;
	if((res=pacc->get_accChild(varChild,&pDispatch))!=S_OK) {
		DEBUG_MSG(L"IAccessible::accChild failed with return code "<<res);
		return NULL;
	}
	IServiceProvider* pServProv=NULL;
	res=pDispatch->QueryInterface(IID_IServiceProvider,(void**)&pServProv);
	pDispatch->Release();
	if(res!=S_OK) {
		DEBUG_MSG(L"QueryInterface to IServiceProvider failed");
		return NULL;
	}
	IHTMLDOMNode* pHTMLDOMNode=NULL;
	res=pServProv->QueryService(IID_IHTMLElement,IID_IHTMLDOMNode,(void**)&pHTMLDOMNode);
	pServProv->Release();
	if(res!=S_OK) {
		DEBUG_MSG(L"QueryService to IHTMLDOMNode failed");
		return NULL;
	}
	return pHTMLDOMNode;
}

inline void fillAttributes(VBufStorage_fieldNode_t* parentNode, IHTMLDOMNode* pHTMLDOMNode, const BSTR nodeName) {
	int res=0;
	IDispatch* pDispatch=NULL;
	DEBUG_MSG(L"Getting IHTMLDOMNode::attributes");
	if(pHTMLDOMNode->get_attributes(&pDispatch)!=S_OK||!pDispatch) {
		DEBUG_MSG(L"pHTMLDOMNode->get_attributes failed");
		return;
	}
	IHTMLAttributeCollection* pHTMLAttributeCollection=NULL;
	res=pDispatch->QueryInterface(IID_IHTMLAttributeCollection,(void**)&pHTMLAttributeCollection);
	pDispatch->Release();
	if(res!=S_OK) {
		DEBUG_MSG(L"Could not get IHTMLAttributesCollection");
		return;
	}
	DEBUG_MSG(L"Got IHTMLDOMNode::attributes");
	LONG length=0;
	DEBUG_MSG(L"Getting IHTMLAttributeCollection::length");
	if(pHTMLAttributeCollection->get_length(&length)!= S_OK) {
		DEBUG_MSG(L"length failed");
		length=0;
	}
	VARIANT vACIndex;
	vACIndex.vt = VT_I4;
	for(int i=0;i<length;i++) {
		IHTMLDOMAttribute* pAttr=0;
		DEBUG_MSG(L"Fetching attribute "<<i);
		    vACIndex.lVal = i;
		IDispatch* childPDispatch=NULL;
		if(pHTMLAttributeCollection->item(&vACIndex,&childPDispatch)!=S_OK) {
			DEBUG_MSG(L"pHTMLAttributeCollection->item failed");
			continue;
		}
		res = childPDispatch->QueryInterface(IID_IHTMLDOMAttribute, (void**)&pAttr);
		childPDispatch->Release();
		if(res!=S_OK) {
			DEBUG_MSG("childPDispatch->QueryInterface of IID_IHTMLDOMAttribute failed");
			continue;
		}
		DEBUG_MSG(L"Got IHTMLAttribute");
		BSTR attrName=NULL;
		VARIANT attrValue ;
		VARIANT_BOOL vbSpecified;
		if (pAttr->get_specified(&vbSpecified)!=S_OK) {
			DEBUG_MSG(L"pAttr->get_specified failed");
			pAttr->Release();
			continue;
		}
		DEBUG_MSG(L"Got specified");
		//ie6 does not return specified=true for value attributes of input fields. Microsoft sucks
		bool isInputField=false;
		if (!vbSpecified) {
			if (wcsicmp(nodeName,L"input")==0)  {
				isInputField=true;
			} else {
				pAttr->Release();
				continue;
			}
		}
		if (pAttr->get_nodeName(&attrName)!=S_OK) {
			DEBUG_MSG(L"pAttr->get_nodeName failed");
			pAttr->Release();
			continue;
		}
		DEBUG_MSG(L"Got AttrName "<<attrName);
		if (isInputField && wcsicmp(attrName,L"value")!=0) { //this is input field, it isn't specified (fake!) but current fetched attribute isn't 'value', so skip it
			SysFreeString(attrName);
			pAttr->Release();
			continue;
		}
		if (pAttr->get_nodeValue(&attrValue)!=S_OK) {
			DEBUG_MSG(L"pAttr->get_nodeValue failed");
			SysFreeString(attrName);
			pAttr->Release();
			continue;
		}
		DEBUG_MSG(L"Got AttrValue");
		wostringstream nameStream;
		nameStream << L"IHTMLAttribute::" << attrName;
		SysFreeString(attrName);
		wostringstream valueStream;
		if (attrValue.vt ==VT_I4) {
			DEBUG_MSG(L"attrValue.vt ==VT_I4");
			valueStream << attrValue.lVal;
		} else if(attrValue.vt==VT_BSTR && attrValue.bstrVal) {
			DEBUG_MSG(L"attrValue.vt==VT_BSTR");
			valueStream << attrValue.bstrVal;
		}
		parentNode->addAttribute(nameStream.str().c_str(),valueStream.str().c_str());
		VariantClear(&attrValue);
		pAttr->Release();
	}
	pHTMLAttributeCollection->Release();
}

inline int getIDFromHTMLDOMNode(IHTMLDOMNode* pHTMLDOMNode) {
	int res;
	IHTMLUniqueName* pHTMLUniqueName=NULL;
	DEBUG_MSG(L"Try to get IHTMLUniqueName");
	if(pHTMLDOMNode->QueryInterface(IID_IHTMLUniqueName,(void**)&pHTMLUniqueName)!=S_OK) {
		DEBUG_MSG(L"Failed to get IHTMLUniqueName");
		return 0;
	}
	DEBUG_MSG(L"Got IHTMLUniqueName");
	int ID=0;
	DEBUG_MSG(L"Getting IHTMLUniqueName::uniqueNumber");
	res=pHTMLUniqueName->get_uniqueNumber((long*)&ID);
	pHTMLUniqueName->Release();
	if(res!=S_OK||!ID) {
		DEBUG_MSG(L"Failed to get IHTMLUniqueName::uniqueNumber");
		return 0;
	}
	DEBUG_MSG(L"Got uniqueNumber of "<<ID);
	return ID;
}

inline BSTR getTextFromHTMLDOMNode(IHTMLDOMNode* pHTMLDOMNode) {
	int res=0;
	IHTMLDOMTextNode* pHTMLDOMTextNode=NULL;
	DEBUG_MSG(L"Trying to get an IHTMLDOMTextNode interface pointer");
	if(pHTMLDOMNode->QueryInterface(IID_IHTMLDOMTextNode,(void**)&pHTMLDOMTextNode)!=S_OK) {
		DEBUG_MSG(L"Not a text node");
		return NULL;
	}
	VBufStorage_textFieldNode_t* textNode=NULL;
	DEBUG_MSG(L"Fetch data of DOMTextNode");
	BSTR data=NULL;
	res=pHTMLDOMTextNode->get_data(&data);
	pHTMLDOMTextNode->Release();
	if(res!=S_OK||!data) {
		DEBUG_MSG(L"Failed to get IHTMLDOMTextNode::data");
		return NULL;
	}
	DEBUG_MSG(L"Got data from IHTMLDOMTextNode");
	return data;
}

#define macro_addHTMLCurrentStyleToMap(styleNameArg,currentStyleObjArg,styleMapArg,tempBSTRArg) {\
	currentStyleObjArg->get_##styleNameArg(&tempBSTRArg);\
	if(tempBSTRArg) {\
		DEBUG_MSG(L"Got "<<L#styleNameArg);\
		styleInfo[L#styleNameArg]=tempBSTRArg;\
		SysFreeString(tempBSTRArg);\
		tempBSTRArg=NULL;\
	} else {\
		DEBUG_MSG(L"Failed to get "<<L#styleNameArg);\
	}\
}

inline void getCurrentStyleInfoFromHTMLDOMNode(IHTMLDOMNode* pHTMLDOMNode, map<wstring,wstring>& styleInfo) {
	int res=0;
	BSTR tempBSTR=NULL;
	IHTMLElement2* pHTMLElement2=NULL;
	res=pHTMLDOMNode->QueryInterface(IID_IHTMLElement2,(void**)&pHTMLElement2);
	if(res!=S_OK||!pHTMLElement2) {
		DEBUG_MSG(L"Could not get IHTMLElement2");
		return;
	}
	IHTMLCurrentStyle* pHTMLCurrentStyle=NULL;
	res=pHTMLElement2->get_currentStyle(&pHTMLCurrentStyle);
	pHTMLElement2->Release();
	if(res!=S_OK||!pHTMLCurrentStyle) {
		DEBUG_MSG(L"Could not get IHTMLCurrentStyle");
		return;
	}
	macro_addHTMLCurrentStyleToMap(display,pHTMLCurrentStyle,styleInfo,tempBSTR);
	macro_addHTMLCurrentStyleToMap(visibility,pHTMLCurrentStyle,styleInfo,tempBSTR);
	pHTMLCurrentStyle->Release();
}

#define macro_addHTMLAttributeToMap(attribName,attribsObj,attribsMap,tempVar,tempAttrObj) {\
	attribsObj->getNamedItem(attribName,&tempAttrObj);\
	if(tempAttribNode) {\
		VariantInit(&tempVar);\
	tempAttribNode->get_nodeValue(&tempVar);\
		if(tempVar.vt==VT_BSTR&&tempVar.bstrVal) {\
			attribsMap[attribName]=tempVar.bstrVal;\
		}\
		VariantClear(&tempVar);\
		tempAttribNode->Release();\
		tempAttribNode=NULL;\
	}\
}

inline void getAttributesFromHTMLDOMNode(IHTMLDOMNode* pHTMLDOMNode,wstring& nodeName, map<wstring,wstring>& attribsMap) {
	int res=0;
	IDispatch* pDispatch=NULL;
	DEBUG_MSG(L"Getting IHTMLDOMNode::attributes");
	if(pHTMLDOMNode->get_attributes(&pDispatch)!=S_OK||!pDispatch) {
		DEBUG_MSG(L"pHTMLDOMNode->get_attributes failed");
		return;
	}
	IHTMLAttributeCollection2* pHTMLAttributeCollection2=NULL;
	res=pDispatch->QueryInterface(IID_IHTMLAttributeCollection2,(void**)&pHTMLAttributeCollection2);
	pDispatch->Release();
	if(res!=S_OK) {
		DEBUG_MSG(L"Could not get IHTMLAttributesCollection2");
		return;
	}
	IHTMLDOMAttribute* tempAttribNode=NULL;
	VARIANT tempVar;
	if(nodeName.compare(L"TABLE")==0) {
		macro_addHTMLAttributeToMap(L"summary",pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	} else if(nodeName.compare(L"INPUT")==0) {
		macro_addHTMLAttributeToMap(L"type",pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
		macro_addHTMLAttributeToMap(L"value",pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	}
	macro_addHTMLAttributeToMap(L"alt",pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"title",pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"src",pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	pHTMLAttributeCollection2->Release();
}

VBufStorage_fieldNode_t* MshtmlVBufBackend_t::fillVBuf(VBufStorage_buffer_t* buffer, VBufStorage_controlFieldNode_t* parentNode, VBufStorage_fieldNode_t* previousNode, IHTMLDOMNode* pHTMLDOMNode, int docHandle) {
	//Handle text nodes
	{ 
		BSTR text=getTextFromHTMLDOMNode(pHTMLDOMNode);
		if(text!=NULL) {
			DEBUG_MSG(L"Got text from node");
			VBufStorage_textFieldNode_t* textNode=buffer->addTextFieldNode(parentNode,previousNode,text);
			SysFreeString(text);
			return textNode;
		}
	}
	//Get node's ID
	int ID=getIDFromHTMLDOMNode(pHTMLDOMNode);
	if(ID==0) {
		DEBUG_MSG(L"Could not get ID");
		return NULL;
	}
	if(buffer->getControlFieldNodeWithIdentifier(docHandle,ID)!=NULL) {
		DEBUG_MSG(L"Node already exists with docHandle "<<docHandle<<L" and ID "<<ID<<L", not adding to buffer");
		return NULL;
	}
	map<wstring,wstring> currentStyleMap;
	getCurrentStyleInfoFromHTMLDOMNode(pHTMLDOMNode,currentStyleMap);
	map<wstring,wstring>::iterator tempIter;
	tempIter=currentStyleMap.find(L"visibility");
	bool invisible=false;
	if(tempIter!=currentStyleMap.end()&&(tempIter->second).compare(0,6,L"hidden")==0) {
		DEBUG_MSG(L"visibility is hidden, not rendering node");
		invisible=true;
	} else {
		tempIter=currentStyleMap.find(L"display");
		if(tempIter!=currentStyleMap.end()&&(tempIter->second).compare(0,4,L"none")==0) {
			DEBUG_MSG(L"Display is None, not rendering node");
			invisible=true;
		}
	}
	bool isBlock=true;
	if(tempIter!=currentStyleMap.end()&&(tempIter->second).compare(0,6,L"inline")==0) {
		DEBUG_MSG(L"node is inline, setting isBlock to false");
		isBlock=false;
	}
	map<wstring,wstring> HTMLAttribsMap;
	BSTR tempBSTR=NULL;
	DEBUG_MSG(L"Trying to get IHTMLDOMNode::nodeName");
	if(pHTMLDOMNode->get_nodeName(&tempBSTR)!=S_OK||!tempBSTR) {
		DEBUG_MSG(L"Failed to get IHTMLDOMNode::nodeName");
		return NULL;
	}
	wstring nodeName=tempBSTR;
	SysFreeString(tempBSTR);
	DEBUG_MSG(L"Got IHTMLDOMNode::nodeName of "<<nodeName);
	getAttributesFromHTMLDOMNode(pHTMLDOMNode,nodeName,HTMLAttribsMap);
	if(nodeName.compare(L"#COMMENT")==0||nodeName.compare(L"SCRIPT")==0) {
		DEBUG_MSG(L"nodeName not supported");
		return NULL;
	}
	int IARole=0;
	int IAStates=0;
	wstring IAKeyboardShortcut;
	IAccessible* pacc=getIAccessibleFromHTMLDOMNode(pHTMLDOMNode);
	if(pacc) {
		getIAccessibleInfo(pacc,&IARole,&IAStates,&IAKeyboardShortcut);
	}
	VBufStorage_controlFieldNode_t* node=new MshtmlVBufStorage_controlFieldNode_t(docHandle,ID,isBlock,this,pHTMLDOMNode);
	parentNode=buffer->addControlFieldNode(parentNode,previousNode,node);
	assert(parentNode);
	previousNode=NULL;
	parentNode->addAttribute(L"IHTMLDOMNode::nodeName",nodeName);
	if(!IAKeyboardShortcut.empty()) {
		parentNode->addAttribute(L"keyboardShortcut",IAKeyboardShortcut);
	}
	wostringstream tempStringStream;
	tempStringStream.str(L"");
	tempStringStream<<IARole;
	parentNode->addAttribute(L"IAccessible::role",tempStringStream.str());
	for(int i=0;i<32;i++) {
		int state=1<<i;
		if(state&IAStates) {
			tempStringStream.str(L"");
			tempStringStream<<L"IAccessible::state_"<<state;
			parentNode->addAttribute(tempStringStream.str(),L"1");
		}
	}
	for(tempIter=HTMLAttribsMap.begin();tempIter!=HTMLAttribsMap.end();tempIter++) {
		tempStringStream.str(L"");
		tempStringStream<<L"HTMLAttrib::"<<tempIter->first;
		parentNode->addAttribute(tempStringStream.str(),tempIter->second);
	}
	for(tempIter=currentStyleMap.begin();tempIter!=currentStyleMap.end();tempIter++) {
		tempStringStream.str(L"");
		tempStringStream<<L"HTMLStyle::"<<tempIter->first;
		parentNode->addAttribute(tempStringStream.str(),tempIter->second);
	}
	tempIter=HTMLAttribsMap.find(L"summary");
	if(!invisible&&nodeName.compare(L"TABLE")==0&&tempIter!=HTMLAttribsMap.end()&&!tempIter->second.empty()) {
		previousNode=buffer->addTextFieldNode(parentNode,previousNode,tempIter->second);
	}
	if(invisible) {
		DEBUG_MSG(L"Node is invisible, not rendering any content");
	} else if(nodeName.compare(L"IMG")==0) {
		bool isURL=False;
		tempIter=HTMLAttribsMap.find(L"alt");
		if(tempIter==HTMLAttribsMap.end()||tempIter->second.empty()) {
			tempIter=HTMLAttribsMap.find(L"title");
			if(tempIter==HTMLAttribsMap.end()||tempIter->second.empty()) {
				tempIter=HTMLAttribsMap.find(L"src");
				isURL=True;
			}
		}
		if(tempIter!=HTMLAttribsMap.end()&&!tempIter->second.empty()) {
			if(isURL) {
				wstring src=getNameForURL(tempIter->second);
				previousNode=buffer->addTextFieldNode(parentNode,previousNode,src);
			} else {
				previousNode=buffer->addTextFieldNode(parentNode,previousNode,tempIter->second);
			}
		}
	} else if(nodeName.compare(L"INPUT")==0) {
		tempIter=HTMLAttribsMap.find(L"type");
		if(tempIter!=HTMLAttribsMap.end()&&tempIter->second.compare(L"hidden")==0) {
			DEBUG_MSG(L"Node is input of type hidden, ignoring");
			return parentNode;
		}
		tempIter=HTMLAttribsMap.find(L"value");
		if(tempIter!=HTMLAttribsMap.end()&&!tempIter->second.empty()) {
			previousNode=buffer->addTextFieldNode(parentNode,previousNode,tempIter->second);
		} else {
			previousNode=buffer->addTextFieldNode(parentNode,previousNode,L" ");
		}
	} else if(nodeName.compare(L"SELECT")==0) {
		bool gotSelection=false;
		IHTMLSelectElement* pHTMLSelectElement=NULL;
		pHTMLDOMNode->QueryInterface(IID_IHTMLSelectElement,(void**)&pHTMLSelectElement);
		if(pHTMLSelectElement) {
			long selectedIndex=-1;
			pHTMLSelectElement->get_selectedIndex(&selectedIndex);
			if(selectedIndex>=0) {
				IDispatch* pDispatch=NULL;
				VARIANT varItem;
				varItem.vt=VT_I4;
				varItem.lVal=selectedIndex;
				VARIANT varSubItem;
				varSubItem.vt=VT_I4;
				varSubItem.lVal=0;
				pHTMLSelectElement->item(varItem,varSubItem,&pDispatch);
				if(pDispatch) {
					IHTMLDOMNode* selectedPHTMLDOMNode=NULL;
					pDispatch->QueryInterface(IID_IHTMLDOMNode,(void**)&selectedPHTMLDOMNode);
					if(selectedPHTMLDOMNode) {
						previousNode=this->fillVBuf(buffer,parentNode,previousNode,selectedPHTMLDOMNode,docHandle);
						selectedPHTMLDOMNode->Release();
						gotSelection=(previousNode&&(previousNode->getLength()>0));
					}
					pDispatch->Release();
				}
			}
			pHTMLSelectElement->Release();
		}
		if(!gotSelection) {
			previousNode=buffer->addTextFieldNode(parentNode,previousNode,L" ");
		}
	} else if(nodeName.compare(L"BR")==0) {
		DEBUG_MSG(L"node is a br tag, adding a line feed as its text.");
		previousNode=buffer->addTextFieldNode(parentNode,previousNode,L"\n");
	} else if(nodeName.compare(L"FRAME")==0||nodeName.compare(L"IFRAME")==0) {
		DEBUG_MSG(L"using getRoodDOMNodeOfHTMLFrame to get the frame's child");
		if(pacc) {
			IHTMLDOMNode* childPHTMLDOMNode=getRootDOMNodeFromIAccessibleFrame(pacc);
			if(childPHTMLDOMNode) {
				previousNode=this->fillVBuf(buffer,parentNode,previousNode,childPHTMLDOMNode,docHandle);
				childPHTMLDOMNode->Release();
			}
		}
	} else {
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
						VBufStorage_fieldNode_t* tempNode=this->fillVBuf(buffer,parentNode,previousNode,childPHTMLDOMNode,docHandle);
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
	}
	if(pacc) pacc->Release();
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

void mainThreadTerminate(VBufBackend_t* backend, HANDLE e) {
	if(mainThreadTimerID!=0) {
		KillTimer(0,mainThreadTimerID);
	}
	backend->getStorageBuffer()->clearBuffer();
	SetEvent(e);
	#ifdef DEBUG
	Beep(880,70);
	#endif
}

LRESULT CALLBACK mainThreadGetMessageHook(int code, WPARAM wParam,LPARAM lParam) {
	MSG* pmsg=(MSG*)lParam;
	if((code==HC_ACTION)&&(pmsg->message==wmMainThreadTerminate)) {
		mainThreadTerminate((VBufBackend_t*)(pmsg->wParam),(HANDLE)(pmsg->lParam));
		DEBUG_MSG(L"Removing hook");
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
	this->fillVBuf(buffer,NULL,NULL,pHTMLDOMNode,docHandle);
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
HANDLE handles[2];
	handles[0]=CreateEvent(NULL,true,false,NULL);
	PostThreadMessage(rootThreadID,wmMainThreadTerminate,(WPARAM)this,(LPARAM)(handles[0]));
	DEBUG_MSG(L"Message sent");
	handles[1]=OpenThread(SYNCHRONIZE,false,rootThreadID);
	WaitForMultipleObjects(2,handles,false,5000);
	res=UnhookWindowsHookEx((HHOOK)(mainThreadGetMessageHookID));
	assert(res!=0); //unHookWindowsHookEx must return non-0
	CloseHandle(handles[0]);
	CloseHandle(handles[1]);
	DEBUG_MSG(L"MSHTML backend terminated");
}

void MshtmlVBufBackend_t::invalidateSubtree(VBufStorage_controlFieldNode_t* node) {
	this->VBufBackend_t::invalidateSubtree(node);
	if(mainThreadTimerID==0) {
		mainThreadTimerID=SetTimer(0,0,100,mainThreadTimerProc);
		DEBUG_MSG(L"Set timer for update with ID of "<<mainThreadTimerID);
	}
}

extern "C" __declspec(dllexport) VBufBackend_t* VBufBackend_create(int docHandle, int ID, VBufStorage_buffer_t* storageBuffer) {
	VBufBackend_t* backend=new MshtmlVBufBackend_t(docHandle,ID,storageBuffer);
	DEBUG_MSG(L"Created new backend at "<<backend);
	return backend;
}
