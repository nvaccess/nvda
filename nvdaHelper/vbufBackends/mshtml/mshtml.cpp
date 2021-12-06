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

#include <map>
#include <algorithm>
#include <windows.h>
#include <oleacc.h>
#include <oleidl.h>
#include <atlcomcli.h>
#include <mshtml.h>
#include <set>
#include <string>
#include <sstream>
#include <vbufBase/backend.h>
#include <vbufBase/utils.h>
#include <remote/dllmain.h>
#include <common/log.h>
#include "node.h"
#include "mshtml.h"

using namespace std;

void incBackendLibRefCount() {
	HMODULE h=NULL;
	BOOL res=GetModuleHandleEx(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS,(LPCTSTR)dllHandle,&h);
	nhAssert(res); //Result of upping backend lib ref count
	LOG_DEBUG(L"Increased  remote lib ref count");
}

void decBackendLibRefCount() {
	BOOL res=FreeLibrary(dllHandle);
	nhAssert(res); //Result of freeing backend lib
	LOG_DEBUG(L"Decreased remote lib ref count");
}

VBufStorage_controlFieldNode_t* MshtmlVBufBackend_t::getDeepestControlFieldNodeForHTMLElement(IHTMLElement* pHTMLElement) {
	bool elementNeedsRelease=false;
	while(pHTMLElement) {
		IHTMLUniqueName* pHTMLUniqueName=NULL;
		pHTMLElement->QueryInterface(IID_IHTMLUniqueName,(void**)&pHTMLUniqueName);
		if(pHTMLUniqueName) {
			int ID=0;
			pHTMLUniqueName->get_uniqueNumber((long*)&ID);
			pHTMLUniqueName->Release();
			if(ID!=0) {
				VBufStorage_controlFieldNode_t* node=this->getControlFieldNodeWithIdentifier(this->rootDocHandle,ID); 
				if(node) {
					if(elementNeedsRelease) pHTMLElement->Release();
					return node;
				} else {
					LOG_DEBUG(L"No node for element");
				}
			} else {
				LOG_DEBUG(L"Could not get unique number from IHTMLUniqueName");
			}
		} else {
			LOG_DEBUG(L"Could not queryInterface from IHTMLElement to IHTMLUniqueName");
		}
		IHTMLElement* parentPHTMLElement=NULL;
		pHTMLElement->get_parentElement(&parentPHTMLElement);
		if(elementNeedsRelease) pHTMLElement->Release();
		pHTMLElement=parentPHTMLElement;
		elementNeedsRelease=true;
	}
	return NULL;
}

/**
	* A utility template function to queryService from a given IUnknown to the given service with the given service ID and interface eing returned.
	* @param siid the service iid
	*/
template<typename toInterface> inline HRESULT queryService(IUnknown* pUnknown, const IID& siid, toInterface** pIface) {
	if (pIface == nullptr) {
		LOG_DEBUG(L"pIface should not be a nullptr");
		constexpr unsigned int CUSTOMER_FLAG = 1;
		return MAKE_HRESULT(SEVERITY_ERROR, CUSTOMER_FLAG, 0);
	}
	HRESULT hRes;
	IServiceProvider* pServProv = nullptr;
	hRes=pUnknown->QueryInterface(IID_IServiceProvider,(void**)&pServProv);
	if(hRes!=S_OK||!pServProv) {
		LOG_DEBUG(L"Could not queryInterface to IServiceProvider");
		return hRes;
	}
	hRes=pServProv->QueryService(siid,__uuidof(toInterface),(void**)pIface);
	pServProv->Release();
	if( hRes != S_OK || *pIface == nullptr) {
		LOG_DEBUG(L"Could not get requested interface");
		*pIface = nullptr;  // if hres is not ok
		return hRes;
	}
	return hRes;
}

inline void getIAccessibleInfo(IAccessible* pacc, wstring* name, int* role, wstring* value, int* states, wstring* description, wstring* keyboardShortcut) {
	*role=0;
	*states=0;
	int res=0;
	VARIANT varChild;
	varChild.vt=VT_I4;
	varChild.lVal=0;
	BSTR bstrVal=NULL;
	if(pacc->get_accName(varChild,&bstrVal)==S_OK&&bstrVal!=NULL) {
		name->append(bstrVal);
		SysFreeString(bstrVal);
		bstrVal=NULL;
	} else {
		LOG_DEBUG(L"IAccessible::get_accName failed");
	}
	VARIANT varRole;
	VariantInit(&varRole);
	res=pacc->get_accRole(varChild,&varRole);
	if(res==S_OK&&varRole.vt==VT_I4) {
		*role=varRole.lVal;
	} else {
		LOG_DEBUG(L"Failed to get role");
	}
	VariantClear(&varRole);
	if(pacc->get_accValue(varChild,&bstrVal)==S_OK&&bstrVal!=NULL) {
		value->append(bstrVal);
		SysFreeString(bstrVal);
		bstrVal=NULL;
	} else {
		LOG_DEBUG(L"IAccessible::get_accValue failed");
	}
	VARIANT varState;
	VariantInit(&varState);
	res=pacc->get_accState(varChild,&varState);
	if(res==S_OK&&varState.vt==VT_I4) {
		*states=varState.lVal;
	} else {
		LOG_DEBUG(L"Failed to get states");
	}
	VariantClear(&varState);
	if(pacc->get_accDescription(varChild,&bstrVal)==S_OK&&bstrVal!=NULL) {
		description->append(bstrVal);
		SysFreeString(bstrVal);
		bstrVal=NULL;
	} else {
		LOG_DEBUG(L"IAccessible::get_accDescription failed");
	}
	if(pacc->get_accKeyboardShortcut(varChild,&bstrVal)==S_OK&&bstrVal!=NULL) {
		keyboardShortcut->append(bstrVal);
		SysFreeString(bstrVal);
	} else {
		LOG_DEBUG(L"IAccessible::get_accKeyboardShortcut failed");
	}
}

template<typename toInterface> inline HRESULT getHTMLSubdocumentBodyFromIAccessibleFrame(IAccessible* pacc, toInterface** pIface) {
HRESULT hRes=0;
	VARIANT varChild;
	varChild.vt=VT_I4;
	varChild.lVal=1;
	IDispatch* pDispatch=NULL;
	if((hRes=pacc->get_accChild(varChild,&pDispatch))!=S_OK) {
		LOG_DEBUG(L"IAccessible::accChild failed with return code "<<hRes);
		return hRes;
	}
	hRes=queryService(pDispatch,IID_IHTMLElement,pIface);
	pDispatch->Release();
	return hRes;
}

IHTMLElement* LocateHTMLElementInDocument(IHTMLDocument3* pHTMLDocument3, const wstring& ID) { 
	HRESULT hRes;
	IHTMLElement* pHTMLElement=NULL;
	//First try getting the element directly from this document
	hRes=pHTMLDocument3->getElementById((wchar_t*)(ID.c_str()),&pHTMLElement);
	if(hRes==S_OK&&pHTMLElement) {
		return pHTMLElement;
	}
	//As it was not in this document, we need to search for it in all subdocuments
	//If the body is a frameset then we need to search all frames
	//If the body is just body, we need to search all iframes
	IHTMLDocument2* pHTMLDocument2=NULL;
	hRes=pHTMLDocument3->QueryInterface(IID_IHTMLDocument2,(void**)&pHTMLDocument2);
	if(hRes!=S_OK||!pHTMLDocument2) {
		LOG_DEBUG(L"Could not get IHTMLDocument2");
		return NULL;
	}
	hRes=pHTMLDocument2->get_body(&pHTMLElement);
	pHTMLDocument2->Release();
	if(hRes!=S_OK||!pHTMLElement) {
		LOG_DEBUGWARNING(L"Could not get body element from IHTMLDocument2 at "<<pHTMLDocument2);
		return NULL;
	}
	BSTR tagName=NULL;
	hRes=pHTMLElement->get_tagName(&tagName);
	wchar_t* embeddingTagName=(tagName&&(wcscmp(tagName,L"FRAMESET"))==0)?L"FRAME":L"IFRAME";
	SysFreeString(tagName);
	IHTMLElement2* pHTMLElement2=NULL;
	hRes=pHTMLElement->QueryInterface(IID_IHTMLElement2,(void**)&pHTMLElement2);
	pHTMLElement->Release();
	if(hRes!=S_OK||!pHTMLElement2) {
		LOG_DEBUG(L"Could not queryInterface to IHTMLElement2");
		return NULL;
	}
	IHTMLElementCollection* pHTMLElementCollection=NULL;
	hRes=pHTMLElement2->getElementsByTagName(embeddingTagName,&pHTMLElementCollection);
	pHTMLElement2->Release();
	if(hRes!=S_OK||!pHTMLElementCollection) {
		LOG_DEBUG(L"Could not get collection from getElementsByName");
		return NULL;
	}
	long numElements=0;
	hRes=pHTMLElementCollection->get_length(&numElements);
	if(hRes!=S_OK) {
		LOG_DEBUG(L"Error getting length of collection");
		numElements=0;
	}
	IHTMLElement* pHTMLElementChild=NULL;
	for(long index=0;index<numElements;++index) {
		IDispatch* pDispatch=NULL;
		VARIANT vID;
		vID.vt=VT_I4;
		vID.lVal=index;
		VARIANT vResIndex;
		vResIndex.vt=VT_I4;
		vResIndex.lVal=0;
		hRes=pHTMLElementCollection->item(vID,vResIndex,&pDispatch);
		if(hRes!=S_OK||!pDispatch) {
			LOG_DEBUG(L"Could not retreave item "<<index<<L" from collection");
			continue;
		}
		IAccessible* pacc=NULL;
		queryService(pDispatch,IID_IAccessible,&pacc);
		pDispatch->Release();
		pDispatch=NULL;
		if(!pacc) {
			LOG_DEBUG(L"Could not queryService to IAccessible");
			continue;
		}
		IHTMLElement* pHTMLElementSubBody=NULL;
		getHTMLSubdocumentBodyFromIAccessibleFrame(pacc,&pHTMLElementSubBody);
		pacc->Release();
		if(!pHTMLElementSubBody) {
			LOG_DEBUG(L"Could not get IHTMLElement body from frame's subdocument");
			continue;
		}
		hRes=pHTMLElementSubBody->get_document(&pDispatch);
		pHTMLElementSubBody->Release();
		if(hRes!=S_OK||!pDispatch) {
			LOG_DEBUG(L"Could not get document from IHTMLElement");
			return NULL;
		}
		IHTMLDocument3* pHTMLDocument3sub=NULL;
		hRes=pDispatch->QueryInterface(IID_IHTMLDocument3,(void**)&pHTMLDocument3sub);
		pDispatch->Release();
		if(hRes!=S_OK||!pHTMLDocument3sub) {
			LOG_DEBUG(L"Could not queryInterface to IHTMLDocument3 for document");
			continue;
		}
		pHTMLElementChild=LocateHTMLElementInDocument(pHTMLDocument3sub,ID);
		pHTMLDocument3sub->Release();
		if(pHTMLElementChild) {
			break;
		}
	}
	pHTMLElementCollection->Release();
	return pHTMLElementChild;
}

inline int getIDFromHTMLDOMNode(IHTMLDOMNode* pHTMLDOMNode) {
	int res;
	IHTMLUniqueName* pHTMLUniqueName=NULL;
	LOG_DEBUG(L"Try to get IHTMLUniqueName");
	if(pHTMLDOMNode->QueryInterface(IID_IHTMLUniqueName,(void**)&pHTMLUniqueName)!=S_OK) {
		LOG_DEBUG(L"Failed to get IHTMLUniqueName");
		return 0;
	}
	LOG_DEBUG(L"Got IHTMLUniqueName");
	int ID=0;
	LOG_DEBUG(L"Getting IHTMLUniqueName::uniqueNumber");
	res=pHTMLUniqueName->get_uniqueNumber((long*)&ID);
	pHTMLUniqueName->Release();
	if(res!=S_OK||!ID) {
		LOG_DEBUG(L"Failed to get IHTMLUniqueName::uniqueNumber");
		return 0;
	}
	LOG_DEBUG(L"Got uniqueNumber of "<<ID);
	return ID;
}

inline wstring getTextFromHTMLDOMNode(IHTMLDOMNode* pHTMLDOMNode, bool allowPreformattedText, bool isStartOfBlock) {
	int res=0;
	IHTMLDOMTextNode* pHTMLDOMTextNode=NULL;
	LOG_DEBUG(L"Trying to get an IHTMLDOMTextNode interface pointer");
	if(pHTMLDOMNode->QueryInterface(IID_IHTMLDOMTextNode,(void**)&pHTMLDOMTextNode)!=S_OK) {
		LOG_DEBUG(L"Not a text node");
		return L"";
	}
	LOG_DEBUG(L"Fetch data of DOMTextNode");
	BSTR data=NULL;
	res=pHTMLDOMTextNode->get_data(&data);
	pHTMLDOMTextNode->Release();
	if(res!=S_OK||!data) {
		LOG_DEBUG(L"Failed to get IHTMLDOMTextNode::data");
		return L"";
	}
	LOG_DEBUG(L"Got data from IHTMLDOMTextNode");
	wstring s;
	bool notAllWhitespace=false;
	if(allowPreformattedText) {
		s.append(data);
	} else {
		bool lastNotWhitespace=false;
		bool strippingLeft=isStartOfBlock;
		for(wchar_t* c=data;*c;++c) {
			if(!iswspace(*c)) {
				s+=*c;
				lastNotWhitespace=TRUE;
				notAllWhitespace=true;
				strippingLeft=false;
			} else if(lastNotWhitespace||!strippingLeft) {
				s+=L' ';
				lastNotWhitespace=FALSE;
			} 
		}
	}
	SysFreeString(data);
	if(!allowPreformattedText&&!notAllWhitespace) {
		return L"";
	}
	return s;
}

#define macro_addHTMLCurrentStyleToNodeAttrs(styleName,attrName,node,currentStyleObj,tempBSTR) {\
	currentStyleObj->get_##styleName(&tempBSTR);\
	if(tempBSTR) {\
		LOG_DEBUG(L"Got "<<L#styleName);\
		node->addAttribute(L#attrName,tempBSTR);\
		SysFreeString(tempBSTR);\
		tempBSTR=NULL;\
	} else {\
		LOG_DEBUG(L"Failed to get "<<L#styleName);\
	}\
}

#define macro_addHTMLCurrentStyleToNodeAttrs_var(styleName,attrName,node,currentStyleObj,tempVar) {\
	currentStyleObj->get_##styleName(&tempVar);\
	if(tempVar.vt==VT_BSTR && tempVar.bstrVal) {\
		LOG_DEBUG(L"Got "<<L#styleName);\
		node->addAttribute(L#attrName,tempVar.bstrVal);\
		VariantClear(&tempVar);\
	} else {\
		LOG_DEBUG(L"Failed to get "<<L#styleName);\
	}\
}

inline void getCurrentStyleInfoFromHTMLDOMNode(IHTMLDOMNode* pHTMLDOMNode, bool& dontRender, bool& isBlock, bool& hidden, wstring& listStyle) {
	BSTR tempBSTR=NULL;
	IHTMLElement2* pHTMLElement2=NULL;
	int res=pHTMLDOMNode->QueryInterface(IID_IHTMLElement2,(void**)&pHTMLElement2);
	if(res!=S_OK||!pHTMLElement2) {
		LOG_DEBUG(L"Could not get IHTMLElement2");
		return;
	}
	IHTMLCurrentStyle* pHTMLCurrentStyle=NULL;
	res=pHTMLElement2->get_currentStyle(&pHTMLCurrentStyle);
	pHTMLElement2->Release();
	if(res!=S_OK||!pHTMLCurrentStyle) {
		LOG_DEBUG(L"Could not get IHTMLCurrentStyle");
		return;
	}
	//get visibility
	pHTMLCurrentStyle->get_visibility(&tempBSTR);
	if(tempBSTR) {
		LOG_DEBUG(L"Got visibility");
		hidden=(_wcsicmp(tempBSTR,L"hidden")==0);
		SysFreeString(tempBSTR);
		tempBSTR=NULL;
	} else {
		LOG_DEBUG(L"Failed to get visibility");\
	}
	//get display
	pHTMLCurrentStyle->get_display(&tempBSTR);
	if(tempBSTR) {
		LOG_DEBUG(L"Got display");
		if (_wcsicmp(tempBSTR,L"none")==0) {
			dontRender=true;
			isBlock=false;
		}
		if (_wcsicmp(tempBSTR,L"inline")==0||_wcsicmp(tempBSTR,L"inline-block")==0) isBlock=false;
		SysFreeString(tempBSTR);
		tempBSTR=NULL;
	} else {
		LOG_DEBUG(L"Failed to get display");
	}
	BSTR _listStyle;
	pHTMLCurrentStyle->get_listStyleType(&_listStyle);
	if(_listStyle) {
		listStyle.append(_listStyle);
		SysFreeString(_listStyle);
	}
	if (pHTMLCurrentStyle) pHTMLCurrentStyle->Release();
}

// #8976: the string in the following macro  must be passed to the COM method as a BSTR 
// otherwise the COM marshaller will try and read the BSTR length and hit either inaccessible memory or get back junk. 
// This is seen in optimized builds of NVDA when accessing some CHM files in hh.exe.
#define macro_addHTMLAttributeToMap(attribName,allowEmpty,attribsObj,attribsMap,tempVar,tempAttrObj) {\
	attribsObj->getNamedItem(CComBSTR(attribName),&tempAttrObj);\
	if(tempAttrObj) {\
		VariantInit(&tempVar);\
		tempAttrObj->get_nodeValue(&tempVar);\
		if(tempVar.vt==VT_BSTR&&tempVar.bstrVal&&(allowEmpty||SysStringLen(tempVar.bstrVal)>0)) {\
			attribsMap[L"HTMLAttrib::" attribName]=tempVar.bstrVal;\
		} else if(tempVar.vt==VT_I2||tempVar.vt==VT_I4) {\
			wostringstream* s=new wostringstream;\
			(*s)<<((tempVar.vt==VT_I2)?tempVar.iVal:tempVar.lVal);\
			attribsMap[L"HTMLAttrib::" attribName]=s->str();\
			delete s;\
		}\
		VariantClear(&tempVar);\
		tempAttrObj->Release();\
		tempAttrObj=NULL;\
	}\
}

inline void getAttributesFromHTMLDOMNode(IHTMLDOMNode* pHTMLDOMNode,wstring& nodeName, map<wstring,wstring>& attribsMap) {
	int res=0;
	IDispatch* pDispatch=NULL;
	LOG_DEBUG(L"Getting IHTMLDOMNode::attributes");
	if(pHTMLDOMNode->get_attributes(&pDispatch)!=S_OK||!pDispatch) {
		LOG_DEBUG(L"pHTMLDOMNode->get_attributes failed");
		return;
	}
	IHTMLAttributeCollection2* pHTMLAttributeCollection2=NULL;
	res=pDispatch->QueryInterface(IID_IHTMLAttributeCollection2,(void**)&pHTMLAttributeCollection2);
	pDispatch->Release();
	if(res!=S_OK) {
		LOG_DEBUG(L"Could not get IHTMLAttributesCollection2");
		return;
	}
	IHTMLDOMAttribute* tempAttribNode=NULL;
	VARIANT tempVar;
	macro_addHTMLAttributeToMap(L"id",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	if(nodeName.compare(L"TABLE")==0) {
		macro_addHTMLAttributeToMap(L"summary",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	} else if(nodeName.compare(L"A")==0) {
		macro_addHTMLAttributeToMap(L"href",true,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	} else if(nodeName.compare(L"INPUT")==0) {
		macro_addHTMLAttributeToMap(L"type",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
		macro_addHTMLAttributeToMap(L"value",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	} else if(nodeName.compare(L"TD")==0||nodeName.compare(L"TH")==0) {
		macro_addHTMLAttributeToMap(L"headers",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
		macro_addHTMLAttributeToMap(L"colspan",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
		macro_addHTMLAttributeToMap(L"rowspan",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
		macro_addHTMLAttributeToMap(L"scope",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	} else if (nodeName.compare(L"OL") == 0) {
		macro_addHTMLAttributeToMap(L"start", false, pHTMLAttributeCollection2, attribsMap, tempVar, tempAttribNode);
	}
	macro_addHTMLAttributeToMap(L"longdesc",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"alt",true,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"title",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"src",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	// Truncate the value of "src" if it contains base64 data
	map<wstring,wstring>::iterator attribsMapIt;
	if ((attribsMapIt = attribsMap.find(L"HTMLAttrib::src")) != attribsMap.end()) {
		wstring str = attribsMapIt->second;
		const wstring prefix = L"data:";
		if (str.substr(0, prefix.length()) == prefix) {
			const wstring needle = L"base64,";
			wstring::size_type pos = str.find(needle);
			if (pos != wstring::npos) {
				str.replace(pos + needle.length(), wstring::npos, L"<truncated>");
				attribsMap[L"HTMLAttrib::src"] = str;
			}
		}
	}
	macro_addHTMLAttributeToMap(L"onclick",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"onmousedown",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"onmouseup",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"required",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"class",true,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	//ARIA properties:
	macro_addHTMLAttributeToMap(L"role",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"aria-roledescription",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"aria-valuenow",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"aria-sort",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"aria-labelledby",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"aria-describedby",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"aria-expanded",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"aria-selected",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"aria-level",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"aria-required",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"aria-dropeffect",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"aria-grabbed",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"aria-invalid",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"aria-multiline",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"aria-label",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"aria-hidden",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"aria-live",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"aria-relevant",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"aria-busy",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"aria-atomic",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"aria-current",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"aria-placeholder",false,pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	pHTMLAttributeCollection2->Release();
}

inline void fillTextFormatting_helper(IHTMLElement2* pHTMLElement2, VBufStorage_fieldNode_t* node) {
	MshtmlVBufStorage_controlFieldNode_t* parentNode=static_cast<MshtmlVBufStorage_controlFieldNode_t*>(node->getParent());
	if(parentNode&&!parentNode->language.empty()) {
		node->addAttribute(L"language",parentNode->language);
	}
	wostringstream s;
	s<<(parentNode->formatState);
	node->addAttribute(L"formatState",s.str());
	IHTMLCurrentStyle* pHTMLCurrentStyle=NULL;
	if(pHTMLElement2->get_currentStyle(&pHTMLCurrentStyle)!=S_OK||!pHTMLCurrentStyle) {
		LOG_DEBUG(L"Could not get IHTMLCurrentStyle");
		return;
	}
	BSTR tempBSTR=NULL;
	macro_addHTMLCurrentStyleToNodeAttrs(textAlign,text-align,node,pHTMLCurrentStyle,tempBSTR);
	VARIANT tempVar;
	macro_addHTMLCurrentStyleToNodeAttrs_var(fontSize,font-size,node,pHTMLCurrentStyle,tempVar);
	macro_addHTMLCurrentStyleToNodeAttrs_var(verticalAlign,text-position,node,pHTMLCurrentStyle,tempVar);
	macro_addHTMLCurrentStyleToNodeAttrs(fontFamily,font-family,node,pHTMLCurrentStyle,tempBSTR);
	//font style
	pHTMLCurrentStyle->get_fontStyle(&tempBSTR);
	if(tempBSTR) {
		LOG_DEBUG(L"Got fontStyle");
		if (_wcsicmp(tempBSTR,L"normal")!=0) {
			node->addAttribute((_wcsicmp(tempBSTR,L"oblique")!=0) ? tempBSTR : L"italic", L"1");
		}
		SysFreeString(tempBSTR);
		tempBSTR=NULL;
	} else {
		LOG_DEBUG(L"Failed to get fontStyle");
	}
	//font weight
	if (pHTMLCurrentStyle->get_fontWeight(&tempVar)==S_OK && tempVar.vt==VT_I4) {
		LOG_DEBUG(L"Got fontWeight");
		if (tempVar.lVal >=700) {
			node->addAttribute(L"bold",L"1");
		}
		VariantClear(&tempVar);
	} else {
		LOG_DEBUG(L"Failed to get fontWeight");
	}
	//textDecoration
	pHTMLCurrentStyle->get_textDecoration(&tempBSTR);
	if(tempBSTR) {
		LOG_DEBUG(L"Got textDecoration");
		if (_wcsicmp(tempBSTR,L"none")!=0) {
			// textDecoration may contain multiple values separated by spaces.
			wchar_t *token, *tokenContext;
			token = wcstok_s(tempBSTR, L" ", &tokenContext);
			while (token) {
				node->addAttribute((_wcsicmp(token,L"line-through")!=0) ? token : L"strikethrough", L"1");
				token = wcstok_s(NULL, L" ", &tokenContext);
			}
		}
		SysFreeString(tempBSTR);
		tempBSTR=NULL;
	} else {
		LOG_DEBUG(L"Failed to get textDecoration");
	}
	pHTMLCurrentStyle->Release();
}

inline void fillTextFormattingForNode(IHTMLDOMNode* pHTMLDOMNode, VBufStorage_fieldNode_t* node) {
	IHTMLElement2* pHTMLElement2=NULL;
	int res=pHTMLDOMNode->QueryInterface(IID_IHTMLElement2,(void**)&pHTMLElement2);
	if(res!=S_OK||!pHTMLElement2) {
		LOG_DEBUG(L"Could not get IHTMLElement2");
		return;
	}
	fillTextFormatting_helper(pHTMLElement2,node);
	pHTMLElement2->Release();
}

inline void fillTextFormattingForTextNode(VBufStorage_controlFieldNode_t* parentNode, VBufStorage_textFieldNode_t* textNode)
	//text nodes don't support IHTMLElement2 interface, so using style information from parent node
	{
	IHTMLElement2* pHTMLElement2=NULL; 
	static_cast<MshtmlVBufStorage_controlFieldNode_t*>(parentNode)->pHTMLDOMNode->QueryInterface(IID_IHTMLElement2,(void**)&pHTMLElement2);
	if(pHTMLElement2) {
		fillTextFormatting_helper(pHTMLElement2,textNode);
		pHTMLElement2->Release();
	}
}

const int TABLEHEADER_COLUMN = 0x1;
const int TABLEHEADER_ROW = 0x2;

inline void fillExplicitTableHeadersForCell(VBufStorage_controlFieldNode_t& cell, int docHandle, wstring& headersAttr, fillVBuf_tableInfo& tableInfo) {
	wostringstream colHeaders, rowHeaders;

	// The Headers attribute string is in the form "id id ..."
	// Loop through all the ids.
	size_t lastPos = headersAttr.length();
	size_t startPos = 0;
	while (startPos < lastPos) {
		// Search for a space, which indicates the end of this id.
		size_t endPos = headersAttr.find(L' ', startPos);
		if (endPos == wstring::npos)
			endPos=lastPos;
		// headersAttr[startPos:endPos] is the id of a single header.
		// Find the info for the header associated with this id string.
		map<wstring, TableHeaderInfo>::const_iterator it = tableInfo.headersInfo.find(headersAttr.substr(startPos, endPos - startPos));
		startPos = endPos + 1;
		if (it == tableInfo.headersInfo.end())
			continue;

		if (it->second.type & TABLEHEADER_COLUMN)
			colHeaders << docHandle << L"," << it->second.uniqueId << L";";
		if (it->second.type & TABLEHEADER_ROW)
			rowHeaders<< docHandle << L"," << it->second.uniqueId << L";";
	}

	if (colHeaders.tellp() > 0)
		cell.addAttribute(L"table-columnheadercells", colHeaders.str());
	if (rowHeaders.tellp() > 0)
		cell.addAttribute(L"table-rowheadercells", rowHeaders.str());
}

/*
 * Adjusts the current column number to skip past columns spanned by previous rows,
 * decrementing row spans as they are encountered.
 */
inline void handleColsSpannedByPrevRows(fillVBuf_tableInfo& tableInfo) {
	for (; ; ++tableInfo.curColumnNumber) {
		map<int, int>::iterator it = tableInfo.columnRowSpans.find(tableInfo.curColumnNumber);
		if (it == tableInfo.columnRowSpans.end()) {
			// This column is not spanned by a previous row.
			return;
		}
		nhAssert(it->second != 0); // 0 row span should never occur.
		// This row has been covered, so decrement the row span.
		--it->second;
		if (it->second == 0)
			tableInfo.columnRowSpans.erase(it);
	}
	nhAssert(false); // Code should never reach this point.
}

inline fillVBuf_tableInfo* fillVBuf_helper_collectAndUpdateTableInfo(VBufStorage_controlFieldNode_t* parentNode, wstring nodeName, int docHandle, int ID, fillVBuf_tableInfo* tableInfo, map<wstring,wstring>& attribsMap) {
	map<wstring,wstring>::const_iterator tempIter;
wostringstream tempStringStream;
	//Many in-table elements identify a data table
	if((nodeName.compare(L"THEAD")==0||nodeName.compare(L"TFOOT")==0||nodeName.compare(L"TH")==0||nodeName.compare(L"CAPTION")==0||nodeName.compare(L"COLGROUP")==0||nodeName.compare(L"ROWGROUP")==0)) {
		if(tableInfo) tableInfo->definitData=true;
	}
	if(nodeName.compare(L"TABLE")==0) {
		tableInfo=new fillVBuf_tableInfo;
		tableInfo->tableNode=parentNode;
		tableInfo->tableID=ID;
		tableInfo->curRowNumber=0;
		tableInfo->curColumnNumber=0;
		tableInfo->definitData=false;
		//summary attribute suggests a data table
		tempIter=attribsMap.find(L"HTMLAttrib::summary");
		if(tempIter!=attribsMap.end()) {
			tableInfo->definitData=true;
		}
		//Collect tableID, and row and column counts
		tempStringStream.str(L"");
		tempStringStream<<ID;
		attribsMap[L"table-id"]=tempStringStream.str();
	} else if(tableInfo&&nodeName.compare(L"TR")==0) {
		++tableInfo->curRowNumber;
		tableInfo->curColumnNumber = 0;
	} if(tableInfo&&(nodeName.compare(L"TD")==0||nodeName.compare(L"TH")==0)) {
		++tableInfo->curColumnNumber;
		handleColsSpannedByPrevRows(*tableInfo);
		tempStringStream.str(L"");
		tempStringStream<<tableInfo->tableID;
		attribsMap[L"table-id"]=tempStringStream.str();
		tempStringStream.str(L"");
		tempStringStream<<tableInfo->curRowNumber;
		attribsMap[L"table-rownumber"]=tempStringStream.str();
		int startCol = tableInfo->curColumnNumber;
		tempStringStream.str(L"");
		tempStringStream<<startCol;
		attribsMap[L"table-columnnumber"]=tempStringStream.str();
		tempIter=attribsMap.find(L"HTMLAttrib::headers");
		if(tempIter!=attribsMap.end()) {
			//A cell with the headers attribute is definitly a data table
			tableInfo->definitData=true;
			//Explicit headers must be recorded later as they may not have been rendered yet.
			tableInfo->nodesWithExplicitHeaders.push_back(make_pair(parentNode, tempIter->second));
		} else {
			map<int, wstring>::const_iterator headersIt;
			// Add implicit column headers for this cell.
			if ((headersIt = tableInfo->columnHeaders.find(startCol)) != tableInfo->columnHeaders.end())
				attribsMap[L"table-columnheadercells"]=headersIt->second;
			// Add implicit row headers for this cell.
			if ((headersIt = tableInfo->rowHeaders.find(tableInfo->curRowNumber)) != tableInfo->rowHeaders.end())
				attribsMap[L"table-rowheadercells"]=headersIt->second;
		}
		// The last row spanned by this cell.
		// This will be updated below if there is a row span.
		int endRow = tableInfo->curRowNumber;
		tempIter=attribsMap.find(L"HTMLAttrib::colspan");
		if(tempIter!=attribsMap.end()) {
			attribsMap[L"table-columnsspanned"]=tempIter->second;
			tableInfo->curColumnNumber += max(_wtoi(tempIter->second.c_str()) - 1, 0);
		}
		tempIter=attribsMap.find(L"HTMLAttrib::rowspan");
		if(tempIter!=attribsMap.end()) {
			attribsMap[L"table-rowsspanned"]=tempIter->second;
			// Keep trakc of how many rows after this one are spanned by this cell.
			int span = _wtoi(tempIter->second.c_str()) - 1;
			if (span > 0) {
				// The row span needs to be recorded for each spanned column.
				for (int col = startCol; col <= tableInfo->curColumnNumber; ++col)
					tableInfo->columnRowSpans[col] = span;
					endRow += span;
			}
		}
		if(nodeName.compare(L"TH")==0) {
			int headerType = 0;
			tempIter=attribsMap.find(L"HTMLAttrib::scope");
			if(tempIter!=attribsMap.end()) {
				if (wcscmp(tempIter->second.c_str(), L"col") == 0)
					headerType = TABLEHEADER_COLUMN;
				else if (wcscmp(tempIter->second.c_str(), L"row") == 0)
					headerType = TABLEHEADER_ROW;
				else if (wcscmp(tempIter->second.c_str(), L"Both") == 0)
					headerType = TABLEHEADER_COLUMN | TABLEHEADER_ROW;
			}
			if (!headerType) {
				if(tableInfo->curColumnNumber==1) headerType=TABLEHEADER_ROW;
				if(tableInfo->curRowNumber==1) headerType|=TABLEHEADER_COLUMN;
			}
			if (headerType & TABLEHEADER_COLUMN) {
				// Record this as a column header for each spanned column.
				tempStringStream.str(L"");
				tempStringStream << docHandle << L"," << ID << L";";
				for (int col = startCol; col <= tableInfo->curColumnNumber; ++col)
					tableInfo->columnHeaders[col] += tempStringStream.str();
			}
			if (headerType & TABLEHEADER_ROW) {
				// Record this as a row header for each spanned row.
				tempStringStream.str(L"");
				tempStringStream << docHandle << L"," << ID << L";";
				for (int row = tableInfo->curRowNumber; row <= endRow; ++row)
					tableInfo->rowHeaders[row] += tempStringStream.str();
			}
			tempIter=attribsMap.find(L"HTMLAttrib::id");
		if(tempIter!=attribsMap.end()) {
				// Record the id string and associated header info for use when handling explicitly defined headers.
				TableHeaderInfo& headerInfo = tableInfo->headersInfo[tempIter->second];
				headerInfo.uniqueId = ID;
				headerInfo.type = headerType;
			}
		}
	}
	return tableInfo;
}

const unsigned int FORMATSTATE_INSERTED=1;
const unsigned int FORMATSTATE_DELETED=2;
const unsigned int FORMATSTATE_MARKED=4;
const unsigned int FORMATSTATE_STRONG=8;
const unsigned int FORMATSTATE_EMPH=16;

VBufStorage_fieldNode_t* MshtmlVBufBackend_t::fillVBuf(VBufStorage_buffer_t* buffer, VBufStorage_controlFieldNode_t* parentNode, VBufStorage_fieldNode_t* previousNode, VBufStorage_controlFieldNode_t* oldNode, IHTMLDOMNode* pHTMLDOMNode, int docHandle, fillVBuf_tableInfo* tableInfo, int* LIIndexPtr, bool ignoreInteractiveUnlabelledGraphics, bool allowPreformattedText, bool shouldSkipText, bool inNewSubtree,set<VBufStorage_controlFieldNode_t*>& atomicNodes) {
	BSTR tempBSTR=NULL;
	wostringstream tempStringStream;

	//Handle text nodes
	if(!shouldSkipText) { 
		wstring s=getTextFromHTMLDOMNode(pHTMLDOMNode,allowPreformattedText,(parentNode&&parentNode->isBlock&&!previousNode));
		if(!s.empty()) {
			LOG_DEBUG(L"Got text from node");
			VBufStorage_textFieldNode_t* textNode=buffer->addTextFieldNode(parentNode,previousNode,s);
			fillTextFormattingForTextNode(parentNode,textNode);
			return textNode;
		}
	}

	//Get node's ID
	int ID=getIDFromHTMLDOMNode(pHTMLDOMNode);
	if(ID==0) {
		LOG_DEBUG(L"Could not get ID");
		return NULL;
	}
	if(buffer->getControlFieldNodeWithIdentifier(docHandle,ID)!=NULL) {
		LOG_DEBUG(L"Node already exists with docHandle "<<docHandle<<L" and ID "<<ID<<L", not adding to buffer");
		return NULL;
	}

	//Find out block and visibility style
	bool dontRender=false;
	bool hidden=false;
	bool isBlock=true;
	wstring listStyle;
	getCurrentStyleInfoFromHTMLDOMNode(pHTMLDOMNode, dontRender, isBlock,hidden,listStyle);
	// #4031: nodes hidden due to style (not role="presentation") should have their direct text nodes skipped
	if(hidden) shouldSkipText=true;
	LOG_DEBUG(L"Trying to get IHTMLDOMNode::nodeName");
	if(pHTMLDOMNode->get_nodeName(&tempBSTR)!=S_OK||!tempBSTR) {
		LOG_DEBUG(L"Failed to get IHTMLDOMNode::nodeName");
		return NULL;
	}
	wstring nodeName=tempBSTR;
	SysFreeString(tempBSTR);
	tempBSTR=NULL;
	for(wstring::iterator i=nodeName.begin();i!=nodeName.end();++i) 
		*i=towupper(*i);
	LOG_DEBUG(L"Got IHTMLDOMNode::nodeName of "<<nodeName);

	//We can safely ignore script and comment tags
	if(nodeName.compare(L"#COMMENT")==0||nodeName.compare(L"SCRIPT")==0) {
		LOG_DEBUG(L"nodeName not supported");
		return NULL;
	}

	//We only allow linebreaks for 'PRE' tags
	if(nodeName.compare(L"PRE")==0) {
		allowPreformattedText=TRUE;
	}
	map<wstring,wstring> attribsMap;
	map<wstring,wstring>::const_iterator tempIter;
	attribsMap[L"IHTMLDOMNode::nodeName"]=nodeName;

	//Collect needed HTML attributes
	getAttributesFromHTMLDOMNode(pHTMLDOMNode,nodeName,attribsMap);

	//Find out if this node is editable
	BOOL isEditable=false;
	IHTMLElement3* pHTMLElement3=NULL;
	if(pHTMLDOMNode->QueryInterface(IID_IHTMLElement3,(void**)&pHTMLElement3)==S_OK) {
		VARIANT_BOOL varEditable=VARIANT_FALSE;
		pHTMLElement3->get_isContentEditable(&varEditable);
		isEditable=(varEditable==VARIANT_TRUE);
		if(isEditable) attribsMap[L"IHTMLElement::isContentEditable"]=L"1";
	}

	if((tempIter=attribsMap.find(L"HTMLAttrib::aria-hidden"))!=attribsMap.end()&&tempIter->second==L"true") {
		// aria-hidden
		dontRender=true;
	}

	//input nodes of type hidden must be treeted as being dontRender.
	if(!dontRender&&nodeName.compare(L"INPUT")==0) {
		tempIter=attribsMap.find(L"HTMLAttrib::type");
		if(tempIter!=attribsMap.end()&&tempIter->second.compare(L"hidden")==0) {
			dontRender=true;
		}
	}

	//Find out the language
	wstring language=L"";
	//Try getting it from this DOMNode,
	//Else if this is the root of our buffer, then keep going up the actual DOM
	//E.g. will hit HTML tag etc
	IHTMLDOMNode* pHTMLDOMNodeTemp=pHTMLDOMNode;
	pHTMLDOMNodeTemp->AddRef();
	while(pHTMLDOMNodeTemp) {
		IHTMLElement* pHTMLElement=NULL;
		if(pHTMLDOMNodeTemp->QueryInterface(IID_IHTMLElement,(void**)&pHTMLElement)==S_OK&&pHTMLElement) {
			VARIANT v;
			if(pHTMLElement->getAttribute(L"lang",2,&v)==S_OK) {
				if(v.vt==VT_BSTR&&v.bstrVal) {
					language=v.bstrVal;
				}
				VariantClear(&v);
			}
			pHTMLElement->Release();
		}
		if(!parentNode&&language.empty()) {
			IHTMLDOMNode* pHTMLDOMNodeTempParent=NULL;
			if(pHTMLDOMNodeTemp->get_parentNode(&pHTMLDOMNodeTempParent)==S_OK&&pHTMLDOMNodeTempParent) {
				pHTMLDOMNodeTemp->Release();
				pHTMLDOMNodeTemp=pHTMLDOMNodeTempParent;
				continue;
			}
		}
		pHTMLDOMNodeTemp->Release();
		pHTMLDOMNodeTemp=NULL;
	}
	if(parentNode&&language.empty()) {
		language=static_cast<MshtmlVBufStorage_controlFieldNode_t*>(parentNode)->language;
	}

	// get parent's formatState
	unsigned int formatState=0;
	if(parentNode) {
		formatState=((MshtmlVBufStorage_controlFieldNode_t*)parentNode)->formatState;
	} else if(oldNode&&oldNode->getParent()) {
		formatState=((MshtmlVBufStorage_controlFieldNode_t*)(oldNode->getParent()))->formatState;
	}
	if(!(formatState&FORMATSTATE_INSERTED)&&nodeName.compare(L"INS")==0) {
		formatState|=FORMATSTATE_INSERTED;
	}
	if(!(formatState&FORMATSTATE_DELETED)&&nodeName.compare(L"DEL")==0) {
		formatState|=FORMATSTATE_DELETED;
	}
	if(!(formatState&FORMATSTATE_MARKED)&&nodeName.compare(L"MARK")==0) {
		formatState|=FORMATSTATE_MARKED;
	}
	if(!(formatState&FORMATSTATE_STRONG)&&nodeName.compare(L"STRONG")==0) {
		formatState|=FORMATSTATE_STRONG;
	}
	if(!(formatState&FORMATSTATE_EMPH)&&nodeName.compare(L"EM")==0) {
		formatState|=FORMATSTATE_EMPH;
	}
	
	bool isDocRoot=!parentNode&&(!oldNode||!oldNode->getParent());
	VBufStorage_controlFieldNode_t* node=new MshtmlVBufStorage_controlFieldNode_t(docHandle,ID,isBlock,this,isDocRoot,pHTMLDOMNode,language);
	((MshtmlVBufStorage_controlFieldNode_t*)node)->formatState=formatState;
	((MshtmlVBufStorage_controlFieldNode_t*)node)->preProcessLiveRegion((MshtmlVBufStorage_controlFieldNode_t*)(oldNode?oldNode->getParent():parentNode),attribsMap);
	bool wasInNewSubtree=inNewSubtree;
	if(!wasInNewSubtree&&!oldNode) {
		oldNode=this->getControlFieldNodeWithIdentifier(docHandle,ID);
		if(oldNode&&oldNode->isHidden) oldNode=NULL;
		inNewSubtree=!oldNode;
	}
	//Add the node to the buffer
	parentNode=buffer->addControlFieldNode(parentNode,previousNode,node);
	nhAssert(parentNode);
	previousNode=NULL;

	//All inner parts of a table (rows, cells etc) if they are changed must re-render the entire table.
	//This must be done even for nodes with display:none.
	if(tableInfo&&(nodeName.compare(L"THEAD")==0||nodeName.compare(L"TBODY")==0||nodeName.compare(L"TFOOT")==0||nodeName.compare(L"TR")==0||nodeName.compare(L"TH")==0||nodeName.compare(L"TD")==0)) {
		parentNode->requiresParentUpdate=true;
		parentNode->allowReuseInAncestorUpdate=false;
	}

	//We do not want to render any content for dontRender nodes
	if(dontRender) {
		parentNode->isHidden=true;
		return parentNode;
	}

	//Collect available IAccessible information
	wstring IAName=L"";
	int IARole=0;
	wstring IAValue=L"";
	int IAStates=0;
	wstring IADescription=L"";
	wstring IAKeyboardShortcut=L"";
	IAccessible* pacc=NULL;
	queryService(pHTMLDOMNode,IID_IAccessible,&pacc);
	if(pacc) {
		getIAccessibleInfo(pacc,&IAName,&IARole,&IAValue,&IAStates,&IADescription,&IAKeyboardShortcut);
	}

	//IE incorrectly places ROLE_SYSTEM_TEXT and no readonly state on unsupported or future tags that have an explicit ARIA role
	//If this is the case then set the IARole to staticText so we don't class it as editable text.
	if(IARole==ROLE_SYSTEM_TEXT&&!(IAStates&STATE_SYSTEM_READONLY)) {
		tempIter=attribsMap.find(L"HTMLAttrib::role");
		if(tempIter!=attribsMap.end()&&tempIter->second.compare(L"textbox")!=0) {
			IARole=ROLE_SYSTEM_STATICTEXT;
		}
	}

	//IE sometimes sets the readonly state on editable nodes, this does not make sence
	if(isEditable&&IAStates&STATE_SYSTEM_READONLY) {
		IAStates-=STATE_SYSTEM_READONLY;
	}

	wstring ariaRole;
	tempIter=attribsMap.find(L"HTMLAttrib::role");
	if(tempIter!=attribsMap.end()) {
		ariaRole=tempIter->second;
		if(ariaRole.compare(L"description")==0||ariaRole.compare(L"search")==0) {
			//IE gives elements with an ARIA role of description and search a role of edit, probably should be staticText
			IARole=ROLE_SYSTEM_STATICTEXT;
		} else if(ariaRole.compare(L"list")==0) {
			IARole=ROLE_SYSTEM_LIST;
			IAStates|=STATE_SYSTEM_READONLY;
		} else if(ariaRole.compare(L"slider")==0) {
			IARole=ROLE_SYSTEM_SLIDER;
			IAStates|=STATE_SYSTEM_FOCUSABLE;
			tempIter=attribsMap.find(L"aria-valuenow");
			if(tempIter!=attribsMap.end()) {
				IAValue=tempIter->second;
			}
		} else if(ariaRole.compare(L"progressbar")==0) {
			IARole=ROLE_SYSTEM_PROGRESSBAR;
			tempIter=attribsMap.find(L"aria-valuenow");
			if(tempIter!=attribsMap.end()) {
				IAValue=tempIter->second;
			}
		} else if(ariaRole.compare(L"application")==0) {
			IARole=ROLE_SYSTEM_APPLICATION;
		} else if(ariaRole.compare(L"button")==0) {
			//IE does not override accRole for links with an ARIA role of button (#2750)
			IARole=ROLE_SYSTEM_PUSHBUTTON;
		} else if(ariaRole.compare(L"dialog")==0) {
			IARole=ROLE_SYSTEM_DIALOG;
		} else if(!hidden&&ariaRole.compare(L"presentation")==0) {
			hidden=true;
		}
	} 
	//IE doesn't seem to support aria-label yet so we want to override IAName with it
	tempIter=attribsMap.find(L"HTMLAttrib::aria-label");
	if(tempIter!=attribsMap.end()) {
		IAName=tempIter->second;
	}

	//IE exposes state_linked for anchors with no href, this is wrong
	if((nodeName.compare(L"A")==0)&&(attribsMap.find(L"HTMLAttrib::href")==attribsMap.end())) {
		if(IAStates&STATE_SYSTEM_LINKED) IAStates-=STATE_SYSTEM_LINKED;
		if(IAStates&STATE_SYSTEM_FOCUSABLE) IAStates-=STATE_SYSTEM_FOCUSABLE;
	}

	// Whether this is the root node.
	bool isRoot=ID==this->rootID;
	//Is this node interactive?
	bool isInteractive=isEditable||(!isRoot&&IAStates&STATE_SYSTEM_FOCUSABLE&&nodeName!=L"BODY"&&nodeName!=L"IFRAME")||(IAStates&STATE_SYSTEM_LINKED)||(attribsMap.find(L"HTMLAttrib::onclick")!=attribsMap.end())||(attribsMap.find(L"HTMLAttrib::onmouseup")!=attribsMap.end())||(attribsMap.find(L"HTMLAttrib::onmousedown")!=attribsMap.end())||(attribsMap.find(L"HTMLAttrib::longdesc")!=attribsMap.end());
	//Set up numbering for lists
	int LIIndex=0;
	constexpr auto ORDERED_LIST_TAG_NODE_NAME = L"OL";
	constexpr auto UNORDERED_LIST_TAG_NODE_NAME = L"UL";
	constexpr auto DEFINITION_LIST_TAG_NODE_NAME = L"DL";
	if (0 == nodeName.compare(ORDERED_LIST_TAG_NODE_NAME)
	){
		//Ordered lists should number their list items
		LIIndex=1;
		// set the list index if list has start attribute
		auto startIter = attribsMap.find(L"HTMLAttrib::start");
		if (startIter != attribsMap.end()
			&& !startIter->second.empty()
		){
			try {
				LIIndex = stoi(startIter->second);
			}
			catch (std::invalid_argument&) {
				// if no conversion could be performed
				constexpr auto errorStr = L"invalid_argument - Unable to convert HTMLAttrib::start value to int: ";
				LOG_ERROR(errorStr << startIter->second)
			}
			catch (std::out_of_range&) {
				// if the converted value would fall out of the range of the result type
				// or if the underlying function(std::strtol or std::strtoll) sets errno to ERANGE.)
				constexpr auto errorStr = L"out_of_range - Unable to convert HTMLAttrib::start value to int: ";
				LOG_ERROR(errorStr << startIter->second)
			}
		}
		LIIndexPtr=&LIIndex;
	} else if (0 == nodeName.compare(UNORDERED_LIST_TAG_NODE_NAME)
		|| 0 == nodeName.compare(DEFINITION_LIST_TAG_NODE_NAME)
	) {
		//Definition lists and unordered lists should not be numbered
		LIIndexPtr=nullptr;
	}

	parentNode->isHidden=hidden;

	if(!hidden) {
		//Collect and update table information
		tableInfo=fillVBuf_helper_collectAndUpdateTableInfo(parentNode, nodeName, docHandle,ID, tableInfo, attribsMap); 
	}

	// Whether the name is the content of this node.
	bool nameIsContent = (IARole == ROLE_SYSTEM_LINK || IARole == ROLE_SYSTEM_PUSHBUTTON || IARole == ROLE_SYSTEM_MENUITEM || IARole == ROLE_SYSTEM_GRAPHIC || IARole == ROLE_SYSTEM_PAGETAB
		|| ariaRole == L"heading" || (nodeName[0] == L'H' && iswdigit(nodeName[1]))
		|| nodeName == L"OBJECT" || nodeName == L"APPLET" || (!isRoot && (IARole == ROLE_SYSTEM_APPLICATION || IARole == ROLE_SYSTEM_DIALOG)));
	// True if the name definitely came from the author.
	bool nameFromAuthor=false;

	//Add opening quote for <Q> elements
	if(nodeName.compare(L"Q")==0) {
		VBufStorage_textFieldNode_t* textNode=buffer->addTextFieldNode(parentNode,previousNode,L"\x201c");
		fillTextFormattingForNode(pHTMLDOMNode,textNode);
		previousNode=textNode;
	}

	//Generate content for nodes
	wstring contentString=L"";
	bool renderChildren=false;
	if (nameIsContent && (attribsMap.find(L"HTMLAttrib::aria-label") != attribsMap.end() || attribsMap.find(L"HTMLAttrib::aria-labelledby") != attribsMap.end())) {
		// Explicitly override any content with aria-label(ledby).
		contentString = IAName;
	} else if (nodeName.compare(L"HR")==0) {
		contentString=L" ";
		isBlock=true;
		IARole=ROLE_SYSTEM_SEPARATOR;
	} else if(IARole==ROLE_SYSTEM_SLIDER||IARole==ROLE_SYSTEM_PROGRESSBAR) {
		contentString=IAValue;
	} else if ((nodeName.compare(L"OBJECT")==0 || nodeName.compare(L"APPLET")==0)) {
		isBlock=true;
		contentString=L" ";
	} else if(nodeName.compare(L"LI")==0) {
		renderChildren=true;
		if(listStyle.compare(L"disc")==0||listStyle.compare(L"circle")==0||listStyle.compare(L"square")==0) {
			tempStringStream.str(L"");
			tempStringStream<<L"\x2022 "; //Bullet
			contentString=tempStringStream.str();
		} else if(LIIndexPtr!=NULL&&!listStyle.empty()&&listStyle.compare(L"none")!=0) {
			tempStringStream.str(L"");
			tempStringStream<<*LIIndexPtr<<L". ";
			contentString=tempStringStream.str();
			++(*LIIndexPtr);
		}
	} else if(nodeName.compare(L"TABLE")==0) {
		renderChildren=true;
 		tempIter=attribsMap.find(L"HTMLAttrib::summary");
		if(tempIter!=attribsMap.end()) {
			contentString=tempIter->second;
		}
	} else if(nodeName.compare(L"IMG")==0) {
		if ((tempIter = attribsMap.find(L"HTMLAttrib::alt")) != attribsMap.end()) {
			if (tempIter->second.empty()) {
				// alt="", so don't render this at all.
				isInteractive = false;
			} else {
				// There is alt text, so use it.
				contentString = tempIter->second;
			}
		} else if ((tempIter = attribsMap.find(L"HTMLAttrib::title")) != attribsMap.end()) {
			// There is a title, so use it.
			contentString = tempIter->second;
		} else if (ignoreInteractiveUnlabelledGraphics)
			isInteractive = false;
		else if (isInteractive && !IAValue.empty()) {
			// The graphic is unlabelled, but we should try to derive a name for it.
			contentString=getNameForURL(IAValue);
		} 
	} else if(nodeName.compare(L"INPUT")==0) {
		tempIter=attribsMap.find(L"HTMLAttrib::type");
		if(tempIter!=attribsMap.end()&&tempIter->second.compare(L"file")==0) {
			contentString=IAValue;
			contentString.append(L"...");
			IARole=ROLE_SYSTEM_PUSHBUTTON;
		} else if(IARole==ROLE_SYSTEM_TEXT) {
			//Sometimes IAccessible::accValue can fail on protected fields, so fall back to value attribute if it exists.
			tempIter=attribsMap.find(L"HTMLAttrib::value");
			if(IAValue.empty()&&tempIter!=attribsMap.end()) {
				contentString=tempIter->second;
			} else {
				contentString=IAValue;
			}
			if(IAStates&STATE_SYSTEM_PROTECTED) {
				fill(contentString.begin(),contentString.end(),L'*');
			}
			nameFromAuthor=true;
		} else if(IARole==ROLE_SYSTEM_PUSHBUTTON) {
			contentString=IAName;
		} else if(IARole==ROLE_SYSTEM_RADIOBUTTON||IARole==ROLE_SYSTEM_CHECKBUTTON) {
			nameFromAuthor=true;
		}
		if(contentString.empty()) {
			contentString=L" ";
		}
	} else if(nodeName.compare(L"SELECT")==0) {
		if(!IAValue.empty()) {
			contentString=IAValue;
		} else {
			contentString=L" ";
		}
		nameFromAuthor=true;
	} else if(nodeName.compare(L"TEXTAREA")==0) {
		isBlock=true;
		if(!IAValue.empty()) {
			contentString=IAValue;
		} else {
			contentString=L" ";
		}
		nameFromAuthor=true;
	} else if(nodeName.compare(L"BR")==0) {
		LOG_DEBUG(L"node is a br tag, adding a line feed as its text.");
		contentString=L"\n";
	} else if((!isRoot&&(IARole==ROLE_SYSTEM_APPLICATION||IARole==ROLE_SYSTEM_DIALOG))
		||IARole==ROLE_SYSTEM_OUTLINE
		||nodeName.compare(L"MATH")==0
	) {
		contentString=L" ";
	} else {
		renderChildren=true;
	}

	//If the name isn't being rendered as the content, add the name as a field attribute
	// if it came from the author (not content).
	if (!nameIsContent && !IAName.empty() && (nameFromAuthor || (
		attribsMap.find(L"HTMLAttrib::aria-label") != attribsMap.end() || attribsMap.find(L"HTMLAttrib::aria-labelledby") != attribsMap.end()
		|| attribsMap.find(L"HTMLAttrib::title") != attribsMap.end() || attribsMap.find(L"HTMLAttrib::alt") != attribsMap.end()
	))) {
		attribsMap[L"name"]=IAName;
		attribsMap[L"alwaysReportName"]=L"true";
	}

	//Add a textNode to the buffer containing any special content retreaved
	if(!hidden&&!contentString.empty()) {
		previousNode=buffer->addTextFieldNode(parentNode,previousNode,contentString);
		fillTextFormattingForNode(pHTMLDOMNode,previousNode);
	}

	//record IAccessible information as attributes
	if(!IAKeyboardShortcut.empty()) {
		attribsMap[L"keyboardShortcut"]=IAKeyboardShortcut;
	}
	tempStringStream.str(L"");
	tempStringStream<<IARole;
	attribsMap[L"IAccessible::role"]=tempStringStream.str();
	for(int i=0;i<32;++i) {
		int state=1<<i;
		if(state&IAStates) {
			tempStringStream.str(L"");
			tempStringStream<<L"IAccessible::state_"<<state;
			attribsMap[tempStringStream.str()]=L"1";
		}
	}

	//Render content of children if we are allowed to
	if(renderChildren) {
		if (isInteractive && !ignoreInteractiveUnlabelledGraphics) {
			// Don't render interactive unlabelled graphic descendants if this node has a name,
			// as author supplied names are preferred.
			ignoreInteractiveUnlabelledGraphics = !IAName.empty();
		}

		//For children of frames we must get the child document via IAccessible
		if(nodeName.compare(L"FRAME")==0||nodeName.compare(L"IFRAME")==0) {
			LOG_DEBUG(L"using getRoodDOMNodeOfHTMLFrame to get the frame's child");
			if(pacc) {
				IHTMLDOMNode* childPHTMLDOMNode=NULL;
				getHTMLSubdocumentBodyFromIAccessibleFrame(pacc,&childPHTMLDOMNode);
				if(childPHTMLDOMNode) {
					previousNode=this->fillVBuf(buffer,parentNode,previousNode,NULL,childPHTMLDOMNode,docHandle,tableInfo,LIIndexPtr,ignoreInteractiveUnlabelledGraphics,allowPreformattedText,shouldSkipText,inNewSubtree,atomicNodes);
					childPHTMLDOMNode->Release();
				}
			}
		} else { //use childNodes
			IHTMLDOMChildrenCollection* pHTMLDOMChildrenCollection=NULL;
			LOG_DEBUG(L"Getting IHTMLDOMNode::childNodes");
			IDispatch* pDispatch=NULL;
			if(pHTMLDOMNode->get_childNodes(&pDispatch)==S_OK) {
				IHTMLDOMChildrenCollection* pHTMLDOMChildrenCollection=NULL;
				if(pDispatch->QueryInterface(IID_IHTMLDOMChildrenCollection,(void**)&pHTMLDOMChildrenCollection)==S_OK) {
					LOG_DEBUG(L"Got IHTMLDOMNode::childNodes");
					LOG_DEBUG(L"Getting IHTMLDOMChildrenCollection::length");
					long length=0;
					pHTMLDOMChildrenCollection->get_length(&length);
					LOG_DEBUG(L"length "<<length);
					for(int i=0;i<length;++i) {
						LOG_DEBUG(L"Fetching child "<<i);
						IDispatch* childPDispatch=NULL;
						if(pHTMLDOMChildrenCollection->item(i,&childPDispatch)!=S_OK) {
							continue;
						}
						IHTMLDOMNode* childPHTMLDOMNode=NULL;
						if(childPDispatch->QueryInterface(IID_IHTMLDOMNode,(void**)&childPHTMLDOMNode)==S_OK) {
							VBufStorage_fieldNode_t* tempNode=this->fillVBuf(buffer,parentNode,previousNode,NULL,childPHTMLDOMNode,docHandle,tableInfo,LIIndexPtr,ignoreInteractiveUnlabelledGraphics,allowPreformattedText,shouldSkipText,inNewSubtree,atomicNodes);
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

		//A node who's rendered children produces no content, or only a small amount of whitespace should render its title or URL
		if(!hidden&&!nodeHasUsefulContent(parentNode)) {
			contentString=L"";
			if(!IAName.empty()) {
				contentString=IAName;
			}
			if(contentString.empty()) {
				tempIter=attribsMap.find(L"HTMLAttrib::title");
				if(tempIter!=attribsMap.end()) {
					contentString=tempIter->second;
				}
			}
			if(contentString.empty()) {
				tempIter=attribsMap.find(L"HTMLAttrib::href");
				if(tempIter!=attribsMap.end()&&!tempIter->second.empty()) {
					contentString=getNameForURL(tempIter->second);
				}
			}
			if(!contentString.empty()) {
				previousNode=buffer->addTextFieldNode(parentNode,NULL,contentString);
				fillTextFormattingForNode(pHTMLDOMNode,previousNode);
			}
			// If any descendant is invalidated, this may change whether this node has no useful content.
			parentNode->alwaysRerenderDescendants=true;
		}
	}


	//We no longer need the IAccessible
	if(pacc) {
		pacc->Release();
		pacc=NULL;
	}

	//Update attributes with table info
	if(!hidden&&nodeName.compare(L"TABLE")==0) {
		nhAssert(tableInfo);
		if(!tableInfo->definitData) {
			attribsMap[L"table-layout"]=L"1";
		}
		for (list<pair<VBufStorage_controlFieldNode_t*, wstring>>::iterator it = tableInfo->nodesWithExplicitHeaders.begin(); it != tableInfo->nodesWithExplicitHeaders.end(); ++it)
			fillExplicitTableHeadersForCell(*it->first, docHandle, it->second, *tableInfo);
		wostringstream s;
		s << tableInfo->curRowNumber;
		parentNode->addAttribute(L"table-rowcount", s.str());
		s.str(L"");
		s << tableInfo->curColumnNumber;
		parentNode->addAttribute(L"table-columncount", s.str());
		delete tableInfo;
		tableInfo=NULL;
	}

	if(!hidden) {
		//Table cells should always be represented by at least a space, but if a space, then they should not be block.
		if((nodeName.compare(L"TD")==0||nodeName.compare(L"TH")==0)) {
			if(parentNode->getLength()==0) {
				isBlock=false;
				buffer->addTextFieldNode(parentNode,previousNode,L" ");
			}
		}

		//If a node is interactive, and still has no content, add a space
		if(isInteractive&&parentNode->getLength()==0) {
			buffer->addTextFieldNode(parentNode,previousNode,L" ");
		}
	}

	//Update block setting on node
	parentNode->isBlock=isBlock;

	//Add all the collected attributes to the node
	for(tempIter=attribsMap.begin();tempIter!=attribsMap.end();++tempIter) {
		parentNode->addAttribute(tempIter->first,tempIter->second);
	}

	// Closing quote for <Q> elements
	if(nodeName.compare(L"Q")==0) {
		VBufStorage_textFieldNode_t* textNode=buffer->addTextFieldNode(parentNode,previousNode,L"\x201d");
		fillTextFormattingForNode(pHTMLDOMNode,textNode);
	}

	// Report any live region update for this node
	if(!wasInNewSubtree&&!hidden) {
		((MshtmlVBufStorage_controlFieldNode_t*)parentNode)->postProcessLiveRegion(oldNode,atomicNodes);
		auto i=atomicNodes.find(parentNode);
		if(i!=atomicNodes.end()) {
			((MshtmlVBufStorage_controlFieldNode_t*)(*i))->reportLiveAddition();
			atomicNodes.erase(i);
		}
	}

	return parentNode;
}

UINT getHTMLWindowMessage() {
	static UINT wm=RegisterWindowMessage(L"WM_HTML_GETOBJECT");
	return wm;
}

void MshtmlVBufBackend_t::render(VBufStorage_buffer_t* buffer, int docHandle, int ID, VBufStorage_controlFieldNode_t* oldNode) {
	LOG_DEBUG(L"Rendering from docHandle "<<docHandle<<L", ID "<<ID<<L", in to buffer at "<<buffer);
	LOG_DEBUG(L"Getting document from window "<<docHandle);
	LRESULT res=SendMessage((HWND)UlongToHandle(docHandle),getHTMLWindowMessage(),0,0);
	if(res==0) {
		LOG_DEBUG(L"Error getting document using WM_HTML_GETOBJECT");
		return;
	}
	IHTMLDOMNode* pHTMLDOMNode=NULL;
	if(oldNode!=NULL) {
		pHTMLDOMNode=(static_cast<MshtmlVBufStorage_controlFieldNode_t*>(oldNode))->pHTMLDOMNode;
		nhAssert(pHTMLDOMNode);
		pHTMLDOMNode->AddRef();
	} else {
		IHTMLDocument3* pHTMLDocument3=NULL;
		if(ObjectFromLresult(res,IID_IHTMLDocument3,0,(void**)&pHTMLDocument3)!=S_OK) {
			LOG_DEBUG(L"Error in ObjectFromLresult");
			return;
		}
		LOG_DEBUG(L"Locating DOM node with ID");
		wostringstream s;
		s<<L"ms__id"<<ID;
		IHTMLElement* pHTMLElement=LocateHTMLElementInDocument(pHTMLDocument3,s.str());
		pHTMLDocument3->Release();
		if(!pHTMLElement) {
			LOG_DEBUG(L"Could not locate HTML element in document");
			return;
		}
		LOG_DEBUG(L"queryInterface to IHTMLDOMNode from IHTMLElement");
		if(pHTMLElement->QueryInterface(IID_IHTMLDOMNode,(void**)&pHTMLDOMNode)!=S_OK) {
			LOG_DEBUG(L"Could not get IHTMLDOMNode");
			pHTMLElement->Release();
			return;
		}
		pHTMLElement->Release();
	}
	nhAssert(pHTMLDOMNode);
	set<VBufStorage_controlFieldNode_t*> atomicNodes;
	this->fillVBuf(buffer,NULL,NULL,oldNode,pHTMLDOMNode,docHandle,NULL,NULL,false,false,false,false,atomicNodes);
	for(auto& i: atomicNodes) {
		((MshtmlVBufStorage_controlFieldNode_t*)i)->reportLiveAddition();
	}
	pHTMLDOMNode->Release();
}

MshtmlVBufBackend_t::MshtmlVBufBackend_t(int docHandle, int ID): VBufBackend_t(docHandle,ID) {
	LOG_DEBUG(L"Mshtml backend constructor");
}

MshtmlVBufBackend_t::~MshtmlVBufBackend_t() {
	LOG_DEBUG(L"Mshtml backend destructor");
}

VBufBackend_t* MshtmlVBufBackend_t_createInstance(int docHandle, int ID) {
	VBufBackend_t* backend=new MshtmlVBufBackend_t(docHandle,ID);
	LOG_DEBUG(L"Created new backend at "<<backend);
	return backend;
}
