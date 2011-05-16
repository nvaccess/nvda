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

#include <set>
#include <sstream>
#include <iomanip>
#include <windows.h>
#include <oleacc.h>
#include <remote/nvdaHelperRemote.h>
#include <vbufBase/backend.h>
#include <remote/log.h>
#include <AcrobatAccess.h>
#include "adobeAcrobat.h"

using namespace std;

IAccessible* IAccessibleFromIdentifier(int docHandle, int ID) {
	int res;
	IAccessible* pacc=NULL;
	VARIANT varChild;
	LOG_DEBUG(L"Calling AccessibleObjectFromEvent");
	if((res=AccessibleObjectFromEvent((HWND)docHandle,OBJID_CLIENT,ID,&pacc,&varChild))!=S_OK) {
		LOG_DEBUG(L"AccessibleObjectFromEvent returned "<<res);
		return NULL;
	}
	LOG_DEBUG(L"Got IAccessible at "<<pacc);
	VariantClear(&varChild);
	return pacc;
}

long getAccID(IServiceProvider* servprov) {
	int res;
	IAccID* paccID = NULL;
	long ID;

	LOG_DEBUG(L"calling IServiceProvider::QueryService for IAccID");
	if((res=servprov->QueryService(SID_AccID,IID_IAccID,(void**)(&paccID)))!=S_OK) {
		LOG_DEBUG(L"IServiceProvider::QueryService returned "<<res);
		return 0;
	} 
	LOG_DEBUG(L"IAccID at "<<paccID);

	LOG_DEBUG(L"Calling get_accID");
	if((res=paccID->get_accID((long*)(&ID)))!=S_OK) {
		LOG_DEBUG(L"paccID->get_accID returned "<<res);
		ID = 0;
	}

	LOG_DEBUG("Releasing IAccID");
	paccID->Release();

	return ID;
}

IPDDomNode* getPDDomNode(VARIANT& varChild, IServiceProvider* servprov) {
	int res;
	IGetPDDomNode* pget = NULL;
	IPDDomNode* domNode = NULL;

	LOG_DEBUG(L"calling IServiceProvider::QueryService for IGetPDDomNode");
	if((res=servprov->QueryService(SID_GetPDDomNode,IID_IGetPDDomNode,(void**)(&pget)))!=S_OK) {
		LOG_DEBUG(L"IServiceProvider::QueryService returned "<<res);
		return NULL;
	} 
	LOG_DEBUG(L"IGetPDDomNode at "<<pget);

	LOG_DEBUG(L"Calling get_PDDomNode");
	if((res=pget->get_PDDomNode(varChild, &domNode))!=S_OK) {
		LOG_DEBUG(L"pget->get_PDDomNode returned "<<res);
		domNode = NULL;
	}

	LOG_DEBUG("Releasing IGetPDDomNode");
	pget->Release();

	return domNode;
}

inline void processText(BSTR inText, wstring& outText) {
	for (wchar_t* ch = inText; *ch; ++ch) {
		switch (*ch) {
			case L'\r':
			case L'\n':
				break;
			default:
				outText += *ch;
		}
	}
}

VBufStorage_fieldNode_t* renderText(VBufStorage_buffer_t* buffer,
	VBufStorage_controlFieldNode_t* parentNode, VBufStorage_fieldNode_t* previousNode,
	IPDDomNode* domNode,
	bool fallBackToName
) {
	HRESULT res;
	VBufStorage_fieldNode_t* tempNode;

	// Grab the font info for this node.
	long fontStatus, fontFlags;
	BSTR fontName = NULL;
	float fontSize, red, green, blue;
	if ((res = domNode->GetFontInfo(&fontStatus, &fontName, &fontSize, &fontFlags, &red, &green, &blue)) != S_OK) {
		LOG_DEBUG(L"IPDDomNode::GetFontInfo returned " << res);
		fontStatus = FontInfo_NoInfo;
	}

	long childCount;
	if (fontStatus == FontInfo_MixedInfo) {
		// This node contains text in more than one font.
		// We need to descend further to get font information.
		LOG_DEBUG(L"Mixed font info, descending");
		if ((res = domNode->GetChildCount(&childCount)) != S_OK) {
			LOG_DEBUG(L"IPDDomNode::GetChildCount returned " << res);
			childCount = 0;
		}
		if (childCount == 0) {
			// HACK: Child count really shouldn't be 0 if fontStatus is FontInfo_MixedInfo, but it sometimes is.
			// Therefore, ignore FontInfo_MixedInfo in this case.
			// Otherwise, the node will be rendered as empty.
			LOG_DEBUG(L"Child count is 0, ignoring mixed font info");
			fontStatus = FontInfo_NoInfo;
		}
	}

	if (fontStatus == FontInfo_MixedInfo) {
		// Iterate through the children.
		for (long childIndex = 0; childIndex < childCount; ++childIndex) {
			IPDDomNode* domChild;
			if ((res = domNode->GetChild(childIndex, &domChild)) != S_OK) {
				LOG_DEBUG(L"IPDDomNode::GetChild returned " << res);
				continue;
			}
			// Recursive call: render text for this child and its descendants.
			if (tempNode = renderText(buffer, parentNode, previousNode, domChild, fallBackToName))
				previousNode = tempNode;
			domChild->Release();
		}
	} else {

		// We don't need to descend, so add the font info and text for this node.
		BSTR text = NULL;
		if ((res = domNode->GetTextContent(&text)) != S_OK) {
			LOG_DEBUG(L"IPDDomNode::GetTextContent returned " << res);
			text = NULL;
		}
		if (text && SysStringLen(text) == 0) {
			SysFreeString(text);
			text = NULL;
		}

		if (!text) {
			// GetTextContent() failed or returned nothing.
			// This should mean there is no text.
			// However, GetValue() or GetName() sometimes works nevertheless, so try it.
			if (fallBackToName)
				res = domNode->GetName(&text);
			else
				res = domNode->GetValue(&text);
			if (res != S_OK) {
				LOG_DEBUG(L"IPDDomNode::GetName/Value returned " << res);
				text = NULL;
			}
			if (text && SysStringLen(text) == 0) {
				SysFreeString(text);
				text = NULL;
			}
		}

		if (text) {
			wstring procText;
			processText(text, procText);
			previousNode = buffer->addTextFieldNode(parentNode, previousNode, procText);
			if (previousNode && fontStatus == FontInfo_Valid) {
				previousNode->addAttribute(L"font-name", fontName);
				wostringstream s;
				s.setf(ios::fixed);
				s << setprecision(1) << fontSize << "pt";
				previousNode->addAttribute(L"font-size", s.str());
				if (fontFlags&PDDOM_FONTATTR_ITALIC==PDDOM_FONTATTR_ITALIC) previousNode->addAttribute(L"italic", L"1");
				if (fontFlags&PDDOM_FONTATTR_BOLD==PDDOM_FONTATTR_BOLD) previousNode->addAttribute(L"bold", L"1");
			}
			SysFreeString(text);
		} else {
			// No text to add, so communicate this to the caller.
			previousNode = NULL;
		}
	}

	if (fontName)
		SysFreeString(fontName);

	return previousNode;
}

VBufStorage_fieldNode_t* AdobeAcrobatVBufBackend_t::fillVBuf(int docHandle, IAccessible* pacc, VBufStorage_buffer_t* buffer,
	VBufStorage_controlFieldNode_t* parentNode, VBufStorage_fieldNode_t* previousNode,
	int indexInParent, long tableID, int rowNumber
) {
	int res;
	LOG_DEBUG(L"Entered fillVBuf, with pacc at "<<pacc<<L", parentNode at "<<parentNode<<L", previousNode "<<previousNode);
	nhAssert(buffer); //buffer can't be NULL
	nhAssert(!parentNode||buffer->isNodeInBuffer(parentNode)); //parent node must be in buffer
	nhAssert(!previousNode||buffer->isNodeInBuffer(previousNode)); //Previous node must be in buffer
	VBufStorage_fieldNode_t* tempNode;

	//all IAccessible methods take a variant for childID, get one ready
	VARIANT varChild;
	varChild.vt=VT_I4;
	varChild.lVal=0;

	IServiceProvider* servprov = NULL;
	LOG_DEBUG(L"calling IAccessible::QueryInterface with IID_IServiceProvider");
	if((res=pacc->QueryInterface(IID_IServiceProvider,(void**)(&servprov)))!=S_OK) {
		LOG_DEBUG(L"IAccessible::QueryInterface returned "<<res);
		return NULL;
	}  
	LOG_DEBUG(L"IServiceProvider at "<<servprov);

	// GET ID
	int ID = getAccID(servprov);
	nhAssert(ID);

	//Make sure that we don't already know about this object -- protect from loops
	if(buffer->getControlFieldNodeWithIdentifier(docHandle,ID)!=NULL) {
		LOG_DEBUG(L"A node with this docHandle and ID already exists, returning NULL");
		servprov->Release();
		return NULL;
	}

	//Add this node to the buffer
	LOG_DEBUG(L"Adding Node to buffer");
	parentNode=buffer->addControlFieldNode(parentNode,previousNode,docHandle,ID,TRUE);
	nhAssert(parentNode); //new node must have been created
	previousNode=NULL;
	LOG_DEBUG(L"Added  node at "<<parentNode);

	// Get role with accRole
	long role = 0;
	LOG_DEBUG(L"Get role with accRole");
	{
		wostringstream s;
		VARIANT varRole;
		VariantInit(&varRole);
		if((res=pacc->get_accRole(varChild,&varRole))!=S_OK) {
			LOG_DEBUG(L"accRole returned code "<<res);
			s<<0;
		} else if(varRole.vt==VT_BSTR) {
			LOG_DEBUG(L"Got role string of " << varRole.bstrVal);
			s << varRole.bstrVal;
		} else if(varRole.vt==VT_I4) {
			LOG_DEBUG(L"Got role of " << varRole.lVal);
			s << varRole.lVal;
			role = varRole.lVal;
		}
		parentNode->addAttribute(L"IAccessible::role",s.str().c_str());
		VariantClear(&varRole);
	}

	// Get states with accState
	LOG_DEBUG(L"get states with IAccessible::get_accState");
	varChild.lVal=0;
	VARIANT varState;
	VariantInit(&varState);
	if((res=pacc->get_accState(varChild,&varState))!=S_OK) {
		LOG_DEBUG(L"pacc->get_accState returned "<<res);
		varState.vt=VT_I4;
		varState.lVal=0;
	}
	int states=varState.lVal;
	VariantClear(&varState);
	LOG_DEBUG(L"states is "<<states);
	//Add each state that is on, as an attrib
	for(int i=0;i<32;++i) {
		int state=1<<i;
		if(state&states) {
			wostringstream nameStream;
			nameStream<<L"IAccessible::state_"<<state;
			parentNode->addAttribute(nameStream.str().c_str(),L"1");
		}
	}

	IPDDomNode* domNode = getPDDomNode(varChild, servprov);

	IPDDomElement* domElement = NULL;
	LOG_DEBUG(L"Trying to get IPDDomElement");
	if (domNode && (res = domNode->QueryInterface(IID_IPDDomElement, (void**)(&domElement))) != S_OK) {
		LOG_DEBUG(L"QueryInterface to IPDDomElement returned " << res);
		domElement = NULL;
	}

	// Get stdName.
	BSTR stdName = NULL;
	if (domElement) {
		if ((res = domElement->GetStdName(&stdName)) != S_OK) {
			LOG_DEBUG(L"IPDDomElement::GetStdName returned " << res);
			stdName = NULL;
		}
		if (stdName) {
			parentNode->addAttribute(L"acrobat::stdname", stdName);
			if (wcscmp(stdName, L"Span") == 0 || wcscmp(stdName, L"Link") == 0 || wcscmp(stdName, L"Quote") == 0) {
				// This is an inline element.
				parentNode->setIsBlock(false);
			}
		}
	}

	//Get the child count
	int childCount=0;
	// We don't want to descend into lists and combo boxes.
	// Besides, Acrobat reports the child count, but the children can't be accessed.
	if (role != ROLE_SYSTEM_LIST && role != ROLE_SYSTEM_COMBOBOX) {
		LOG_DEBUG(L"get childCount with IAccessible::get_accChildCount");
		if((res=pacc->get_accChildCount((long*)(&childCount)))!=S_OK) {
			LOG_DEBUG(L"pacc->get_accChildCount returned "<<res);
			childCount=0;
		}
	}
	LOG_DEBUG(L"childCount is "<<childCount);

	// Handle table information.
	if (role == ROLE_SYSTEM_TABLE) {
		LOG_DEBUG(L"This is a table, adding table-id attribute");
		wostringstream s;
		s << ID;
		parentNode->addAttribute(L"table-id", s.str());
		tableID = ID;
	} else if (role == ROLE_SYSTEM_ROW) {
		LOG_DEBUG(L"This is a table row, setting rowNumber");
		rowNumber = indexInParent + 1;
	} else if (role == ROLE_SYSTEM_CELL || role == ROLE_SYSTEM_COLUMNHEADER) {
		LOG_DEBUG(L"This is a table cell, adding attributes");
		wostringstream s;
		s << tableID;
		parentNode->addAttribute(L"table-id", s.str());
		s.str(L"");
		s << ((role == ROLE_SYSTEM_COLUMNHEADER) ? 0 : rowNumber);
		parentNode->addAttribute(L"table-rownumber", s.str());
		s.str(L"");
		// The parent is a row, so indexInParent is the column number.
		s << indexInParent + 1;
		parentNode->addAttribute(L"table-columnnumber", s.str());
	}

	// Iterate through the children.
	if (childCount > 0) {
		LOG_DEBUG(L"Allocate memory to hold children");
		VARIANT* varChildren;
		if((varChildren=(VARIANT*)malloc(sizeof(VARIANT)*childCount))==NULL) {
			LOG_DEBUG(L"Error allocating varChildren memory");
			if (stdName)
				SysFreeString(stdName);
			return NULL;
		}
		LOG_DEBUG(L"Fetch children with AccessibleChildren");
		if((res=AccessibleChildren(pacc,0,childCount,varChildren,(long*)(&childCount)))!=S_OK) {
			LOG_DEBUG(L"AccessibleChildren returned "<<res);
			childCount=0;
		}
		LOG_DEBUG(L"got "<<childCount<<L" children");
		for(int i=0;i<childCount;++i) {
			LOG_DEBUG(L"child "<<i);
			if(varChildren[i].vt==VT_DISPATCH) {
				LOG_DEBUG(L"QueryInterface dispatch child to IID_IAccesible");
				IAccessible* childPacc=NULL;
				if((res=varChildren[i].pdispVal->QueryInterface(IID_IAccessible,(void**)(&childPacc)))!=S_OK) {
					LOG_DEBUG(L"varChildren["<<i<<L"].pdispVal->QueryInterface to IID_iAccessible returned "<<res);
					childPacc=NULL;
				}
				if(childPacc) {
					if (this->isXFA) {
						// HACK: If this is an XFA document, we must call WindowFromAccessibleObject() so that AccessibleObjectFromEvent() will work for this node.
						HWND tempHwnd;
						WindowFromAccessibleObject(childPacc, &tempHwnd);
					}
					LOG_DEBUG(L"calling filVBuf with child object ");
					if((tempNode=this->fillVBuf(docHandle,childPacc,buffer,parentNode,previousNode,i,tableID,rowNumber))!=NULL) {
						previousNode=tempNode;
					} else {
						LOG_DEBUG(L"Error in calling fillVBuf");
					}
					LOG_DEBUG(L"releasing child IAccessible object");
					childPacc->Release();
				}
			}
			VariantClear(&(varChildren[i]));
		}
		LOG_DEBUG(L"Freeing memory holding children");
		free(varChildren);
	} else {

		// No children, so this is a leaf node.
		if (!this->isXFA && !stdName) {
			// Non-XFA leaf nodes with no stdName are inline.
			parentNode->setIsBlock(false);
		}

		// Get the name.
		BSTR name = NULL;
		if (states & STATE_SYSTEM_FOCUSABLE && (res = pacc->get_accName(varChild, &name)) != S_OK) {
			LOG_DEBUG(L"IAccessible::get_accName returned " << res);
			name = NULL;
		}
		if(name && SysStringLen(name) == 0) {
			SysFreeString(name);
			name = NULL;
		}

		bool useNameAsContent = role == ROLE_SYSTEM_LINK || role == ROLE_SYSTEM_PUSHBUTTON || role == ROLE_SYSTEM_RADIOBUTTON || role == ROLE_SYSTEM_CHECKBUTTON;

		if (name && !useNameAsContent) {
			parentNode->addAttribute(L"name", name);
			// Render the name before this node,
			// as the label is often not a separate node and thus won't be rendered into the buffer.
			buffer->addTextFieldNode(parentNode->getParent(), parentNode->getPrevious(), name);
		}

		if (role == ROLE_SYSTEM_RADIOBUTTON || role == ROLE_SYSTEM_CHECKBUTTON) {
			// Acrobat renders "Checked"/"Unchecked" as the text for radio buttons/check boxes, which is not what we want.
			// Render the name (if any) as the text for radio buttons and check boxes.
			if (name && (tempNode = buffer->addTextFieldNode(parentNode, previousNode, name)))
				previousNode = tempNode;
			else
				tempNode = NULL; // Signal no text.
		} else if (tempNode = renderText(buffer, parentNode, previousNode, domNode, useNameAsContent))
			previousNode = tempNode;

		if (name)
			SysFreeString(name);

		if (!tempNode && states & STATE_SYSTEM_FOCUSABLE) {
			// This node is focusable, but contains no text.
			// Therefore, add it with a space so that the user can get to it.
			if (tempNode = buffer->addTextFieldNode(parentNode, previousNode, L" "))
				previousNode=tempNode;
		}
	}

	if (stdName)
		SysFreeString(stdName);
	if (domElement) {
		LOG_DEBUG(L"Releasing IPDDomElement");
		domElement->Release();
	}
	if (domNode) {
		LOG_DEBUG(L"Releasing IPDDomNode");
		domNode->Release();
	}
	LOG_DEBUG(L"Releasing IServiceProvider");
	servprov->Release();

	LOG_DEBUG(L"Returning node at "<<parentNode);
	return parentNode;
}

void CALLBACK AdobeAcrobatVBufBackend_t::renderThread_winEventProcHook(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time) {
	if (eventID != EVENT_OBJECT_STATECHANGE && eventID != EVENT_OBJECT_VALUECHANGE)
		return;
	if (eventID == EVENT_OBJECT_VALUECHANGE && objectID == OBJID_CLIENT && childID == CHILDID_SELF) {
		// This indicates that a new document or page replaces this one.
		// The client will ditch this buffer and create a new one, so there's no point rendering it here.
		return;
	}

	LOG_DEBUG(L"winEvent for window "<<hwnd);

	int docHandle=(int)hwnd;
	int ID=(objectID>0)?objectID:childID;
	VBufBackend_t* backend=NULL;
	LOG_DEBUG(L"Searching for backend in collection of "<<runningBackends.size()<<L" running backends");
	for(VBufBackendSet_t::iterator i=runningBackends.begin();i!=runningBackends.end();++i) {
		HWND rootWindow=(HWND)((*i)->rootDocHandle);
		LOG_DEBUG(L"Comparing backend's root window "<<rootWindow<<L" with window "<<hwnd);
		if(rootWindow==hwnd) {
			backend=(*i);
		}
	}
	if(!backend) {
		LOG_DEBUG(L"No matching backend found");
		return;
	}
	LOG_DEBUG(L"found active backend for this window at "<<backend);

	VBufStorage_buffer_t* buffer=backend;
	VBufStorage_controlFieldNode_t* node=buffer->getControlFieldNodeWithIdentifier(docHandle,ID);
	if(!node) {
		LOG_DEBUG(L"No nodes to use, returning");
		return;
	}

	backend->invalidateSubtree(node);
}

void AdobeAcrobatVBufBackend_t::renderThread_initialize() {
	registerWinEventHook(renderThread_winEventProcHook);
	LOG_DEBUG(L"Registered win event callback");
	VBufBackend_t::renderThread_initialize();
}

void AdobeAcrobatVBufBackend_t::renderThread_terminate() {
	unregisterWinEventHook(renderThread_winEventProcHook);
	LOG_DEBUG(L"Unregistered winEvent hook");
	VBufBackend_t::renderThread_terminate();
}

bool checkIsXFA(IAccessible* rootPacc) {
	VARIANT varChild, varState;
	varChild.vt = VT_I4;
	varChild.lVal = 0;
	VariantInit(&varState);
	if (rootPacc->get_accState(varChild, &varState) != S_OK) {
		return false;
	}
	int states = varState.lVal;
	VariantClear(&varState);

	// If the root accessible is read-only, this is not an XFA document.
	return !(states & STATE_SYSTEM_READONLY);
}

void AdobeAcrobatVBufBackend_t::render(VBufStorage_buffer_t* buffer, int docHandle, int ID, VBufStorage_controlFieldNode_t* oldNode) {
	LOG_DEBUG(L"Rendering from docHandle "<<docHandle<<L", ID "<<ID<<L", in to buffer at "<<buffer);
	IAccessible* pacc=IAccessibleFromIdentifier(docHandle,ID);
	nhAssert(pacc); //must get a valid IAccessible object
	if (!oldNode) {
		// This is the root node.
		this->isXFA = checkIsXFA(pacc);
	}
	this->fillVBuf(docHandle,pacc,buffer,NULL,NULL);
	pacc->Release();
	LOG_DEBUG(L"Rendering done");
}

AdobeAcrobatVBufBackend_t::AdobeAcrobatVBufBackend_t(int docHandle, int ID): VBufBackend_t(docHandle,ID) {
	LOG_DEBUG(L"AdobeAcrobat backend constructor");
}

AdobeAcrobatVBufBackend_t::~AdobeAcrobatVBufBackend_t() {
	LOG_DEBUG(L"AdobeAcrobat backend destructor");
}

extern "C" __declspec(dllexport) VBufBackend_t* VBufBackend_create(int docHandle, int ID) {
	VBufBackend_t* backend=new AdobeAcrobatVBufBackend_t(docHandle,ID);
	LOG_DEBUG(L"Created new backend at "<<backend);
	return backend;
}

BOOL WINAPI DllMain(HINSTANCE hModule,DWORD reason,LPVOID lpReserved) {
	if(reason==DLL_PROCESS_ATTACH) {
		_CrtSetReportHookW2(_CRT_RPTHOOK_INSTALL,(_CRT_REPORT_HOOKW)NVDALogCrtReportHook);
	}
	return true;
}
