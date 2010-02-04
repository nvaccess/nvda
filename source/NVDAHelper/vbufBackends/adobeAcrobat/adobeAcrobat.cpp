/**
 * backends/adobeAcrobat/adobeAcrobat.cpp
 * Part of the NV  Virtual Buffer Library
 * This library is copyright 2007-2008 NV Virtual Buffer Library Contributors
 * This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
 * http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
 */

#include <set>
 #include <sstream>
 #include <iomanip>
 #include <cassert>
#include <windows.h>
#include <oleacc.h>
#include <remote/nvdaHelperRemote.h>
#include <vbufBase/backend.h>
#include <common/debug.h>
#include <AcrobatAccess/AcrobatAccess.h>
#include <AcrobatAccess/IPDDom.h>
#include "adobeAcrobat.h"

using namespace std;

IAccessible* IAccessibleFromIdentifier(int docHandle, int ID) {
	int res;
	IAccessible* pacc=NULL;
	VARIANT varChild;
	DEBUG_MSG(L"Calling AccessibleObjectFromEvent");
	if((res=AccessibleObjectFromEvent((HWND)docHandle,OBJID_CLIENT,ID,&pacc,&varChild))!=S_OK) {
		DEBUG_MSG(L"AccessibleObjectFromEvent returned "<<res);
		return NULL;
	}
	DEBUG_MSG(L"Got IAccessible at "<<pacc);
	VariantClear(&varChild);
	return pacc;
}

long getAccID(IServiceProvider* servprov) {
	int res;
	IAccID* paccID = NULL;
	long ID;

	DEBUG_MSG(L"calling IServiceProvider::QueryService for IAccID");
	if((res=servprov->QueryService(SID_AccID,IID_IAccID,(void**)(&paccID)))!=S_OK) {
		DEBUG_MSG(L"IServiceProvider::QueryService returned "<<res);
		return 0;
	} 
	DEBUG_MSG(L"IAccID at "<<paccID);

	DEBUG_MSG(L"Calling get_accID");
	if((res=paccID->get_accID((long*)(&ID)))!=S_OK) {
		DEBUG_MSG(L"paccID->get_accID returned "<<res);
		ID = 0;
	}

	DEBUG_MSG("Releasing IAccID");
	paccID->Release();

	return ID;
}

IPDDomNode* getPDDomNode(VARIANT& varChild, IServiceProvider* servprov) {
	int res;
	IGetPDDomNode* pget = NULL;
	IPDDomNode* domNode = NULL;

	DEBUG_MSG(L"calling IServiceProvider::QueryService for IGetPDDomNode");
	if((res=servprov->QueryService(SID_GetPDDomNode,IID_IGetPDDomNode,(void**)(&pget)))!=S_OK) {
		DEBUG_MSG(L"IServiceProvider::QueryService returned "<<res);
		return NULL;
	} 
	DEBUG_MSG(L"IGetPDDomNode at "<<pget);

	DEBUG_MSG(L"Calling get_PDDomNode");
	if((res=pget->get_PDDomNode(varChild, &domNode))!=S_OK) {
		DEBUG_MSG(L"pget->get_PDDomNode returned "<<res);
		domNode = NULL;
	}

	DEBUG_MSG("Releasing IGetPDDomNode");
	pget->Release();

	return domNode;
}

inline void processText(BSTR inText, wstring& outText) {
	for (wchar_t* ch = inText; *ch; ch++) {
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
	IPDDomNode* domNode
) {
	HRESULT res;
	VBufStorage_fieldNode_t* tempNode;

	// Grab the font info for this node.
	long fontStatus, fontFlags;
	BSTR fontName = NULL;
	float fontSize, red, green, blue;
	if ((res = domNode->GetFontInfo(&fontStatus, &fontName, &fontSize, &fontFlags, &red, &green, &blue)) != S_OK) {
		DEBUG_MSG(L"IPDDomNode::GetFontInfo returned " << res);
		fontStatus = FontInfo_NoInfo;
	}

	if (fontStatus == FontInfo_MixedInfo) {
		// This node contains text in more than one font.
		// We need to descend further to get font information.
		DEBUG_MSG(L"Mixed font info, descending");
		long childCount;
		if ((res = domNode->GetChildCount(&childCount)) != S_OK) {
			DEBUG_MSG(L"IPDDomNode::GetChildCount returned " << res);
			childCount = 0;
		}
		if (childCount == 0) {
			DEBUG_MSG(L"Child count is 0");
		}

		// Iterate through the children.
		for (long childIndex = 0; childIndex < childCount; childIndex++) {
			IPDDomNode* domChild;
			if ((res = domNode->GetChild(childIndex, &domChild)) != S_OK) {
				DEBUG_MSG(L"IPDDomNode::GetChild returned " << res);
				continue;
			}
			// Recursive call: render text for this child and its descendants.
			if (tempNode = renderText(buffer, parentNode, previousNode, domChild))
				previousNode = tempNode;
			domChild->Release();
		}
	} else {

		// We don't need to descend, so add the font info and text for this node.
		BSTR text = NULL;
		if ((res = domNode->GetTextContent(&text)) != S_OK) {
			DEBUG_MSG(L"IPDDomNode::GetTextContent returned " << res);
			text = NULL;
		}
		if (text && SysStringLen(text) == 0) {
			SysFreeString(text);
			text = NULL;
		}

		if (!text) {
			// GetTextContent() failed or returned nothing.
			// This should mean there is no text, but GetValue() sometimes works nevertheless, so try it.
			if ((res = domNode->GetValue(&text)) != S_OK) {
				DEBUG_MSG(L"IPDDomNode::GetTextContent returned " << res);
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
	DEBUG_MSG(L"Entered fillVBuf, with pacc at "<<pacc<<L", parentNode at "<<parentNode<<L", previousNode "<<previousNode);
	assert(buffer); //buffer can't be NULL
	assert(!parentNode||buffer->isNodeInBuffer(parentNode)); //parent node must be in buffer
	assert(!previousNode||buffer->isNodeInBuffer(previousNode)); //Previous node must be in buffer
	VBufStorage_fieldNode_t* tempNode;

	//all IAccessible methods take a variant for childID, get one ready
	VARIANT varChild;
	varChild.vt=VT_I4;
	varChild.lVal=0;

	IServiceProvider* servprov = NULL;
	DEBUG_MSG(L"calling IAccessible::QueryInterface with IID_IServiceProvider");
	if((res=pacc->QueryInterface(IID_IServiceProvider,(void**)(&servprov)))!=S_OK) {
		DEBUG_MSG(L"IAccessible::QueryInterface returned "<<res);
		return NULL;
	}  
	DEBUG_MSG(L"IServiceProvider at "<<servprov);

	// GET ID
	int ID = getAccID(servprov);
	assert(ID);

	//Make sure that we don't already know about this object -- protect from loops
	if(buffer->getControlFieldNodeWithIdentifier(docHandle,ID)!=NULL) {
		DEBUG_MSG(L"A node with this docHandle and ID already exists, returning NULL");
		servprov->Release();
		return NULL;
	}

	//Add this node to the buffer
	DEBUG_MSG(L"Adding Node to buffer");
	parentNode=buffer->addControlFieldNode(parentNode,previousNode,docHandle,ID,TRUE);
	assert(parentNode); //new node must have been created
	previousNode=NULL;
	DEBUG_MSG(L"Added  node at "<<parentNode);

	// Get role with accRole
	long role = 0;
	DEBUG_MSG(L"Get role with accRole");
	{
		wostringstream s;
		VARIANT varRole;
		VariantInit(&varRole);
		if((res=pacc->get_accRole(varChild,&varRole))!=S_OK) {
			DEBUG_MSG(L"accRole returned code "<<res);
			s<<0;
		} else if(varRole.vt==VT_BSTR) {
			DEBUG_MSG(L"Got role string of " << varRole.bstrVal);
			s << varRole.bstrVal;
		} else if(varRole.vt==VT_I4) {
			DEBUG_MSG(L"Got role of " << varRole.lVal);
			s << varRole.lVal;
			role = varRole.lVal;
		}
		parentNode->addAttribute(L"IAccessible::role",s.str().c_str());
		VariantClear(&varRole);
	}

	// Get states with accState
	DEBUG_MSG(L"get states with IAccessible::get_accState");
	varChild.lVal=0;
	VARIANT varState;
	VariantInit(&varState);
	if((res=pacc->get_accState(varChild,&varState))!=S_OK) {
		DEBUG_MSG(L"pacc->get_accState returned "<<res);
		varState.vt=VT_I4;
		varState.lVal=0;
	}
	int states=varState.lVal;
	VariantClear(&varState);
	DEBUG_MSG(L"states is "<<states);
	//Add each state that is on, as an attrib
	for(int i=0;i<32;i++) {
		int state=1<<i;
		if(state&states) {
			wostringstream nameStream;
			nameStream<<L"IAccessible::state_"<<state;
			parentNode->addAttribute(nameStream.str().c_str(),L"1");
		}
	}

	IPDDomNode* domNode = getPDDomNode(varChild, servprov);

	IPDDomElement* domElement = NULL;
	DEBUG_MSG(L"Trying to get IPDDomElement");
	if (domNode && (res = domNode->QueryInterface(IID_IPDDomElement, (void**)(&domElement))) != S_OK) {
		DEBUG_MSG(L"QueryInterface to IPDDomElement returned " << res);
		domElement = NULL;
	}

	// Get stdName.
	BSTR stdName = NULL;
	if (domElement) {
		if ((res = domElement->GetStdName(&stdName)) != S_OK) {
			DEBUG_MSG(L"IPDDomElement::GetStdName returned " << res);
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
		DEBUG_MSG(L"get childCount with IAccessible::get_accChildCount");
		if((res=pacc->get_accChildCount((long*)(&childCount)))!=S_OK) {
			DEBUG_MSG(L"pacc->get_accChildCount returned "<<res);
			childCount=0;
		}
	}
	DEBUG_MSG(L"childCount is "<<childCount);

	// Handle table information.
	if (role == ROLE_SYSTEM_TABLE) {
		DEBUG_MSG(L"This is a table, adding table-id attribute");
		wostringstream s;
		s << ID;
		parentNode->addAttribute(L"table-id", s.str());
		tableID = ID;
	} else if (role == ROLE_SYSTEM_ROW) {
		DEBUG_MSG(L"This is a table row, setting rowNumber");
		rowNumber = indexInParent + 1;
	} else if (role == ROLE_SYSTEM_CELL || role == ROLE_SYSTEM_COLUMNHEADER) {
		DEBUG_MSG(L"This is a table cell, adding attributes");
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
		DEBUG_MSG(L"Allocate memory to hold children");
		VARIANT* varChildren;
		if((varChildren=(VARIANT*)malloc(sizeof(VARIANT)*childCount))==NULL) {
			DEBUG_MSG(L"Error allocating varChildren memory");
			if (stdName)
				SysFreeString(stdName);
			return NULL;
		}
		DEBUG_MSG(L"Fetch children with AccessibleChildren");
		if((res=AccessibleChildren(pacc,0,childCount,varChildren,(long*)(&childCount)))!=S_OK) {
			DEBUG_MSG(L"AccessibleChildren returned "<<res);
			childCount=0;
		}
		DEBUG_MSG(L"got "<<childCount<<L" children");
		for(int i=0;i<childCount;i++) {
			DEBUG_MSG(L"child "<<i);
			if(varChildren[i].vt==VT_DISPATCH) {
				DEBUG_MSG(L"QueryInterface dispatch child to IID_IAccesible");
				IAccessible* childPacc=NULL;
				if((res=varChildren[i].pdispVal->QueryInterface(IID_IAccessible,(void**)(&childPacc)))!=S_OK) {
					DEBUG_MSG(L"varChildren["<<i<<L"].pdispVal->QueryInterface to IID_iAccessible returned "<<res);
					childPacc=NULL;
				}
				if(childPacc) {
					if (this->isXFA) {
						// HACK: If this is an XFA document, we must call WindowFromAccessibleObject() so that AccessibleObjectFromEvent() will work for this node.
						HWND tempHwnd;
						WindowFromAccessibleObject(childPacc, &tempHwnd);
					}
					DEBUG_MSG(L"calling filVBuf with child object ");
					if((tempNode=this->fillVBuf(docHandle,childPacc,buffer,parentNode,previousNode,i,tableID,rowNumber))!=NULL) {
						previousNode=tempNode;
					} else {
						DEBUG_MSG(L"Error in calling fillVBuf");
					}
					DEBUG_MSG(L"releasing child IAccessible object");
					childPacc->Release();
				}
			}
			VariantClear(&(varChildren[i]));
		}
		DEBUG_MSG(L"Freeing memory holding children");
		free(varChildren);
	} else {

		// No children, so this is a text leaf node.
		if (!stdName) {
			// Text leaf nodes with no stdName are inline.
			parentNode->setIsBlock(false);
		}

		// Get the name.
		BSTR name = NULL;
		if (states & STATE_SYSTEM_FOCUSABLE && (res = pacc->get_accName(varChild, &name)) != S_OK) {
			DEBUG_MSG(L"IAccessible::get_accName returned " << res);
			name = NULL;
		}
		if(name && SysStringLen(name) == 0) {
			SysFreeString(name);
			name = NULL;
		}

		// If there is a name, render it before this node, except for certain controls.
		if (name && role != ROLE_SYSTEM_LINK && role != ROLE_SYSTEM_PUSHBUTTON && role != ROLE_SYSTEM_RADIOBUTTON && role != ROLE_SYSTEM_CHECKBUTTON) {
			buffer->addTextFieldNode(parentNode->getParent(), parentNode->getPrevious(), name);
		}

		if (role == ROLE_SYSTEM_RADIOBUTTON || role == ROLE_SYSTEM_CHECKBUTTON) {
			// Acrobat renders "Checked"/"Unchecked" as the text for radio buttons/check boxes, which is not what we want.
			// Render the name (if any) as the text for radio buttons and check boxes.
			if (name && (tempNode = buffer->addTextFieldNode(parentNode, previousNode, name)))
				previousNode = tempNode;
			else
				tempNode = NULL; // Signal no text.
		} else if (tempNode = renderText(buffer, parentNode, previousNode, domNode))
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
		DEBUG_MSG(L"Releasing IPDDomElement");
		domElement->Release();
	}
	if (domNode) {
		DEBUG_MSG(L"Releasing IPDDomNode");
		domNode->Release();
	}
	DEBUG_MSG(L"Releasing IServiceProvider");
	servprov->Release();

	DEBUG_MSG(L"Returning node at "<<parentNode);
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

	DEBUG_MSG(L"winEvent for window "<<hwnd);

	int docHandle=(int)hwnd;
	int ID=(objectID>0)?objectID:childID;
	VBufBackend_t* backend=NULL;
	DEBUG_MSG(L"Searching for backend in collection of "<<backends.size()<<L" running backends");
	for(VBufBackendSet_t::iterator i=runningBackends.begin();i!=runningBackends.end();i++) {
		HWND rootWindow=(HWND)((*i)->rootDocHandle);
		DEBUG_MSG(L"Comparing backend's root window "<<rootWindow<<L" with window "<<hwnd);
		if(rootWindow==hwnd) {
			backend=(*i);
		}
	}
	if(!backend) {
		DEBUG_MSG(L"No matching backend found");
		return;
	}
	DEBUG_MSG(L"found active backend for this window at "<<backend);

	VBufStorage_buffer_t* buffer=backend;
	VBufStorage_controlFieldNode_t* node=buffer->getControlFieldNodeWithIdentifier(docHandle,ID);
	if(!node) {
		DEBUG_MSG(L"No nodes to use, returning");
		return;
	}

	backend->invalidateSubtree(node);
}

void AdobeAcrobatVBufBackend_t::renderThread_initialize() {
	registerWinEventHook(renderThread_winEventProcHook);
	DEBUG_MSG(L"Registered win event callback");
	VBufBackend_t::renderThread_initialize();
}

void AdobeAcrobatVBufBackend_t::renderThread_terminate() {
	unregisterWinEventHook(renderThread_winEventProcHook);
	DEBUG_MSG(L"Unregistered winEvent hook");
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
	DEBUG_MSG(L"Rendering from docHandle "<<docHandle<<L", ID "<<ID<<L", in to buffer at "<<buffer);
	IAccessible* pacc=IAccessibleFromIdentifier(docHandle,ID);
	assert(pacc); //must get a valid IAccessible object
	if (!oldNode) {
		// This is the root node.
		this->isXFA = checkIsXFA(pacc);
	}
	this->fillVBuf(docHandle,pacc,buffer,NULL,NULL);
	pacc->Release();
	DEBUG_MSG(L"Rendering done");
}

AdobeAcrobatVBufBackend_t::AdobeAcrobatVBufBackend_t(int docHandle, int ID): VBufBackend_t(docHandle,ID) {
	DEBUG_MSG(L"AdobeAcrobat backend constructor");
}

AdobeAcrobatVBufBackend_t::~AdobeAcrobatVBufBackend_t() {
	DEBUG_MSG(L"AdobeAcrobat backend destructor");
}

extern "C" __declspec(dllexport) VBufBackend_t* VBufBackend_create(int docHandle, int ID) {
	VBufBackend_t* backend=new AdobeAcrobatVBufBackend_t(docHandle,ID);
	DEBUG_MSG(L"Created new backend at "<<backend);
	return backend;
}
