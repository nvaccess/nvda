#include <sstream>
#include <cassert>
#include <windows.h>
#include <oleacc.h>
#include <remote/nvdaHelperRemote.h>
#include <vbufBase/backend.h>
#include "adobeFlash.h"

using namespace std;

int idCounter = 10000;

IAccessible* IAccessibleFromIdentifier(int docHandle, int ID) {
	int res;
	IAccessible* pacc=NULL;
	VARIANT varChild;
	if((res=AccessibleObjectFromEvent((HWND)docHandle,OBJID_CLIENT,ID,&pacc,&varChild))!=S_OK) {
		return NULL;
	}
	VariantClear(&varChild);
	return pacc;
}

VBufStorage_fieldNode_t* AdobeFlashVBufBackend_t::fillVBuf(int docHandle, IAccessible* pacc, VBufStorage_buffer_t* buffer,
	VBufStorage_controlFieldNode_t* parentNode, VBufStorage_fieldNode_t* previousNode
) {
	assert(buffer);

	int res;
	VBufStorage_fieldNode_t* tempNode;
	//all IAccessible methods take a variant for childID, get one ready
	VARIANT varChild;
	varChild.vt=VT_I4;
	varChild.lVal=0;

	int id = idCounter++;
	//Make sure that we don't already know about this object -- protect from loops
	if(buffer->getControlFieldNodeWithIdentifier(docHandle,id)!=NULL) {
		return NULL;
	}

	//Add this node to the buffer
	parentNode=buffer->addControlFieldNode(parentNode,previousNode,docHandle,id,TRUE);
	assert(parentNode); //new node must have been created
	previousNode=NULL;

	wostringstream s;

	// Get role with accRole
	long role = 0;
	VARIANT varRole;
	VariantInit(&varRole);
	if((res=pacc->get_accRole(varChild,&varRole))!=S_OK) {
		s<<0;
	} else if(varRole.vt==VT_BSTR) {
		s << varRole.bstrVal;
	} else if(varRole.vt==VT_I4) {
		s << varRole.lVal;
		role = varRole.lVal;
	}
	parentNode->addAttribute(L"IAccessible::role",s.str());
	VariantClear(&varRole);

	// Get states with accState
	varChild.lVal=0;
	VARIANT varState;
	VariantInit(&varState);
	if((res=pacc->get_accState(varChild,&varState))!=S_OK) {
		varState.vt=VT_I4;
		varState.lVal=0;
	}
	int states=varState.lVal;
	VariantClear(&varState);
	//Add each state that is on, as an attrib
	for(int i=0;i<32;i++) {
		int state=1<<i;
		if(state&states) {
			s.str(L"");
			s<<L"IAccessible::state_"<<state;
			parentNode->addAttribute(s.str(),L"1");
		}
	}

	//Get the child count
	int childCount=0;
	if((res=pacc->get_accChildCount((long*)(&childCount)))!=S_OK) {
		childCount=0;
	}

	// Iterate through the children.
	if (childCount > 0) {
		VARIANT* varChildren;
		if((varChildren=(VARIANT*)malloc(sizeof(VARIANT)*childCount))==NULL) {
			return NULL;
		}
		if((res=AccessibleChildren(pacc,0,childCount,varChildren,(long*)(&childCount)))!=S_OK) {
			childCount=0;
		}
		for(int i=0;i<childCount;i++) {
			if(varChildren[i].vt==VT_DISPATCH) {
				IAccessible* childPacc=NULL;
				if((res=varChildren[i].pdispVal->QueryInterface(IID_IAccessible,(void**)(&childPacc)))!=S_OK) {
					childPacc=NULL;
				}
				if(childPacc) {
					if((tempNode=this->fillVBuf(docHandle,childPacc,buffer,parentNode,previousNode))!=NULL) {
						previousNode=tempNode;
					}
					childPacc->Release();
				}
			}
			VariantClear(&(varChildren[i]));
		}
		free(varChildren);
	} else {

		// No children, so this is a text leaf node.
		BSTR tempBstr = NULL;
		wstring content;

		if (states & STATE_SYSTEM_FOCUSABLE && (res = pacc->get_accName(varChild, &tempBstr)) == S_OK) {
			content = tempBstr;
			SysFreeString(tempBstr);
		} else if ((res = pacc->get_accValue(varChild, &tempBstr)) == S_OK) {
			content = tempBstr;
			SysFreeString(tempBstr);
		} else if (states & STATE_SYSTEM_FOCUSABLE) {
			// This node is focusable, but contains no text.
			// Therefore, add it with a space so that the user can get to it.
			content = L" ";
		}

		if (!content.empty()) {
			if (tempNode = buffer->addTextFieldNode(parentNode, previousNode, content))
				previousNode=tempNode;
		}
	}

	return parentNode;
}

void AdobeFlashVBufBackend_t::render(VBufStorage_buffer_t* buffer, int docHandle, int ID, VBufStorage_controlFieldNode_t* oldNode) {
	IAccessible* pacc=IAccessibleFromIdentifier(docHandle,ID);
	assert(pacc); //must get a valid IAccessible object
	this->fillVBuf(docHandle,pacc,buffer,NULL,NULL);
	pacc->Release();
}

AdobeFlashVBufBackend_t::AdobeFlashVBufBackend_t(int docHandle, int ID): VBufBackend_t(docHandle,ID) {
}

extern "C" __declspec(dllexport) VBufBackend_t* VBufBackend_create(int docHandle, int ID) {
	VBufBackend_t* backend=new AdobeFlashVBufBackend_t(docHandle,ID);
	return backend;
}
