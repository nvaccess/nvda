/**
 * backends/mshtml/mshtml.cpp
 * Part of the NV  Virtual Buffer Library
 * This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
 * This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
 * http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
 */

#include <cassert>
#include <windows.h>
#include <oleacc.h>
#include <oleidl.h>
#include <mshtml.h>
#include <set>
#include <string>
#include <sstream>
#include <vbufBase/backend.h>
#include <vbufBase/utils.h>
#include <vbufBase/debug.h>
#include "node.h"
#include "mshtml.h"

using namespace std;

HINSTANCE backendLibHandle=NULL;
UINT WM_HTML_GETOBJECT;

BOOL WINAPI DllMain(HINSTANCE hModule,DWORD reason,LPVOID lpReserved) {
	if(reason==DLL_PROCESS_ATTACH) {
		backendLibHandle=hModule;
		WM_HTML_GETOBJECT=RegisterWindowMessage(L"WM_HTML_GETOBJECT");
	}
	return TRUE;
}

void incBackendLibRefCount() {
	HMODULE h=NULL;
	bool res=GetModuleHandleEx(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS,(LPCTSTR)backendLibHandle,&h);
	assert(res); //Result of upping backend lib ref count
	DEBUG_MSG(L"Increased backend lib ref count");
}

void decBackendLibRefCount() {
	bool res=FreeLibrary(backendLibHandle);
	assert(res); //Result of freeing backend lib
	DEBUG_MSG(L"Decreased backend lib ref count");
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
					DEBUG_MSG(L"No node for element");
				}
			} else {
				DEBUG_MSG(L"Could not get unique number from IHTMLUniqueName");
			}
		} else {
			DEBUG_MSG(L"Could not queryInterface from IHTMLElement to IHTMLUniqueName");
		}
		IHTMLElement* parentPHTMLElement=NULL;
		pHTMLElement->get_parentElement(&parentPHTMLElement);
		if(elementNeedsRelease) pHTMLElement->Release();
		pHTMLElement=parentPHTMLElement;
		elementNeedsRelease=true;
	}
	return NULL;
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

#define macro_addHTMLCurrentStyleToNodeAttrs(styleName,attrName,node,currentStyleObj,tempBSTR) {\
	currentStyleObj->get_##styleName(&tempBSTR);\
	if(tempBSTR) {\
		DEBUG_MSG(L"Got "<<L#styleName);\
		node->addAttribute(L#attrName,tempBSTR);\
		SysFreeString(tempBSTR);\
		tempBSTR=NULL;\
	} else {\
		DEBUG_MSG(L"Failed to get "<<L#styleName);\
	}\
}

#define macro_addHTMLCurrentStyleToNodeAttrs_var(styleName,attrName,node,currentStyleObj,tempVar) {\
	currentStyleObj->get_##styleName(&tempVar);\
	if(tempVar.vt==VT_BSTR && tempVar.bstrVal) {\
		DEBUG_MSG(L"Got "<<L#styleName);\
		node->addAttribute(L#attrName,tempVar.bstrVal);\
		VariantClear(&tempVar);\
	} else {\
		DEBUG_MSG(L"Failed to get "<<L#styleName);\
	}\
}

inline void getCurrentStyleInfoFromHTMLDOMNode(IHTMLDOMNode* pHTMLDOMNode, bool& invisible, bool& isBlock) {
	BSTR tempBSTR=NULL;
	IHTMLElement2* pHTMLElement2=NULL;
	int res=pHTMLDOMNode->QueryInterface(IID_IHTMLElement2,(void**)&pHTMLElement2);
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
	//get visibility
	pHTMLCurrentStyle->get_visibility(&tempBSTR);
	if(tempBSTR) {
		DEBUG_MSG(L"Got visibility");
		invisible=(wcsicmp(tempBSTR,L"hidden")==0);
		SysFreeString(tempBSTR);
		tempBSTR=NULL;
	} else {
		DEBUG_MSG(L"Failed to get visibility");\
	}
	//get display
	pHTMLCurrentStyle->get_display(&tempBSTR);
	if(tempBSTR) {
		DEBUG_MSG(L"Got display");
		if (wcsicmp(tempBSTR,L"none")==0) invisible=true;
		if (wcsicmp(tempBSTR,L"inline")==0) isBlock=false;
		SysFreeString(tempBSTR);
		tempBSTR=NULL;
	} else {
		DEBUG_MSG(L"Failed to get display");
	}
	if (pHTMLCurrentStyle) pHTMLCurrentStyle->Release();
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
	} else if(nodeName.compare(L"TD")==0||nodeName.compare(L"TH")==0) {
		macro_addHTMLAttributeToMap(L"headers",pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	}
	macro_addHTMLAttributeToMap(L"alt",pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"title",pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"src",pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	//ARIA properties:
	macro_addHTMLAttributeToMap(L"role",pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"aria-required",pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"aria-dropeffect",pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"aria-grabbed",pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"aria-invalid",pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"aria-multiline",pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	macro_addHTMLAttributeToMap(L"aria-label",pHTMLAttributeCollection2,attribsMap,tempVar,tempAttribNode);
	pHTMLAttributeCollection2->Release();
}

inline void fillTextFormatting_helper(IHTMLElement2* pHTMLElement2, VBufStorage_fieldNode_t* node) {
	IHTMLCurrentStyle* pHTMLCurrentStyle=NULL;
	if(pHTMLElement2->get_currentStyle(&pHTMLCurrentStyle)!=S_OK||!pHTMLCurrentStyle) {
		DEBUG_MSG(L"Could not get IHTMLCurrentStyle");
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
		DEBUG_MSG(L"Got fontStyle");
		if (wcsicmp(tempBSTR,L"normal")!=0) {
			node->addAttribute((wcsicmp(tempBSTR,L"oblique")!=0) ? tempBSTR : L"italic", L"1");
		}
		SysFreeString(tempBSTR);
		tempBSTR=NULL;
	} else {
		DEBUG_MSG(L"Failed to get fontStyle");
	}
	//font weight
	if (pHTMLCurrentStyle->get_fontWeight(&tempVar)==S_OK && tempVar.vt==VT_I4) {
		DEBUG_MSG(L"Got fontWeight");
		if (tempVar.lVal >=700) {
			node->addAttribute(L"bold",L"1");
		}
		VariantClear(&tempVar);
	} else {
		DEBUG_MSG(L"Failed to get fontWeight");
	}
	//textDecoration
	pHTMLCurrentStyle->get_textDecoration(&tempBSTR);
	if(tempBSTR) {
		DEBUG_MSG(L"Got textDecoration");
		if (wcsicmp(tempBSTR,L"none")!=0) {
			node->addAttribute((wcsicmp(tempBSTR,L"line-through")!=0) ? tempBSTR : L"strikethrough", L"1");
		}
		SysFreeString(tempBSTR);
		tempBSTR=NULL;
	} else {
		DEBUG_MSG(L"Failed to get textDecoration");
	}
	pHTMLCurrentStyle->Release();
}

inline void fillTextFormattingForNode(IHTMLDOMNode* pHTMLDOMNode, VBufStorage_fieldNode_t* node) {
	IHTMLElement2* pHTMLElement2=NULL;
	int res=pHTMLDOMNode->QueryInterface(IID_IHTMLElement2,(void**)&pHTMLElement2);
	if(res!=S_OK||!pHTMLElement2) {
		DEBUG_MSG(L"Could not get IHTMLElement2");
		return;
	}
	fillTextFormatting_helper(pHTMLElement2,node);
	pHTMLElement2->Release();
}

inline void fillTextFormattingForTextNode(VBufStorage_controlFieldNode_t* parentNode, VBufStorage_textFieldNode_t* textNode)
	//text nodes don't support IHTMLElement2 interface, so using style information from parent node
	{
	IHTMLElement2* pHTMLElement2=(static_cast<MshtmlVBufStorage_controlFieldNode_t*>(parentNode))->pHTMLElement2;
	fillTextFormatting_helper(pHTMLElement2,textNode);
}

VBufStorage_fieldNode_t* MshtmlVBufBackend_t::fillVBuf(VBufStorage_buffer_t* buffer, VBufStorage_controlFieldNode_t* parentNode, VBufStorage_fieldNode_t* previousNode, IHTMLDOMNode* pHTMLDOMNode, int docHandle, fillVBuf_tableInfo* tableInfoPtr, int* LIIndexPtr) {
	BSTR tempBSTR=NULL;
	IHTMLElement2* pHTMLElement2=NULL;
	IHTMLCurrentStyle* pHTMLCurrentStyle=NULL;
	//Handle text nodes
	{ 
		tempBSTR=getTextFromHTMLDOMNode(pHTMLDOMNode);
		if(tempBSTR!=NULL) {
			DEBUG_MSG(L"Got text from node");
			VBufStorage_textFieldNode_t* textNode=buffer->addTextFieldNode(parentNode,previousNode,tempBSTR);
			fillTextFormattingForTextNode(parentNode,textNode);
			SysFreeString(tempBSTR);
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
	bool invisible=false;
	bool isBlock=true;
	getCurrentStyleInfoFromHTMLDOMNode(pHTMLDOMNode, invisible, isBlock);
	map<wstring,wstring> HTMLAttribsMap;
	map<wstring,wstring>::const_iterator tempIter;
	DEBUG_MSG(L"Trying to get IHTMLDOMNode::nodeName");
	if(pHTMLDOMNode->get_nodeName(&tempBSTR)!=S_OK||!tempBSTR) {
		DEBUG_MSG(L"Failed to get IHTMLDOMNode::nodeName");
		return NULL;
	}
	wstring nodeName=tempBSTR;
	SysFreeString(tempBSTR);
	DEBUG_MSG(L"Got IHTMLDOMNode::nodeName of "<<nodeName);
	if(nodeName.compare(L"#COMMENT")==0||nodeName.compare(L"SCRIPT")==0) {
		DEBUG_MSG(L"nodeName not supported");
		return NULL;
	}
	getAttributesFromHTMLDOMNode(pHTMLDOMNode,nodeName,HTMLAttribsMap);
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
	if (nodeName.compare(L"HR")==0) {
		previousNode=buffer->addTextFieldNode(parentNode,previousNode,L" ");
		IARole=ROLE_SYSTEM_SEPARATOR;
		parentNode->setIsBlock(true);
	} else if (!invisible && (nodeName.compare(L"OBJECT")==0 || nodeName.compare(L"APPLET")==0)) {
		parentNode->setIsBlock(true);
		previousNode=buffer->addTextFieldNode(parentNode,previousNode,L" ");
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
	int LIIndex=0;
	if(!invisible&&nodeName.compare(L"OL")==0) {
		//Ordered lists should number their list items
		LIIndex=1;
		LIIndexPtr=&LIIndex;
	} else if(!invisible&&(nodeName.compare(L"UL")==0||nodeName.compare(L"DL")==0)) {
		//Unordered lists should not be numbered
		LIIndexPtr=NULL;
	}
	if(!invisible&&nodeName.compare(L"LI")==0) {
		if(LIIndexPtr!=NULL) {
			tempStringStream.str(L"");
			tempStringStream<<*LIIndexPtr<<L". ";
			previousNode=buffer->addTextFieldNode(parentNode,previousNode,tempStringStream.str());
			(*LIIndexPtr)++;
		} else {
			tempStringStream.str(L"");
			tempStringStream<<L"\x2022 "; //Bullet
			previousNode=buffer->addTextFieldNode(parentNode,previousNode,tempStringStream.str());
		}
		fillTextFormattingForTextNode(parentNode,static_cast<VBufStorage_textFieldNode_t*>(previousNode));
	}
	//Many in-table elements identify a data table
	if(!invisible&&(nodeName.compare(L"THEAD")==0||nodeName.compare(L"TFOOT")==0||nodeName.compare(L"TH")==0||nodeName.compare(L"CAPTION")==0||nodeName.compare(L"COLGROUP")==0||nodeName.compare(L"ROWGROUP")==0)) {
		if(tableInfoPtr) tableInfoPtr->definitData=true;
	}
	if(!invisible&&nodeName.compare(L"TABLE")==0) {
		tableInfoPtr=new fillVBuf_tableInfo;
		tableInfoPtr->tableID=ID;
		tableInfoPtr->curRowIndex=0;
		tableInfoPtr->definitData=false;
		//Find summary attribute and add it as a text node.
		tempIter=HTMLAttribsMap.find(L"summary");
		if(tempIter!=HTMLAttribsMap.end()&&!tempIter->second.empty()) {
			previousNode=buffer->addTextFieldNode(parentNode,previousNode,tempIter->second);
			fillTextFormattingForNode(pHTMLDOMNode,previousNode);
			tableInfoPtr->definitData=true;
		}
		//Collect tableID, and row and column counts
		IHTMLTable* pHTMLTable=NULL;
		pHTMLDOMNode->QueryInterface(IID_IHTMLTable,(void**)&pHTMLTable);
		if(pHTMLTable) {
			tempStringStream.str(L"");
			tempStringStream<<ID;
			parentNode->addAttribute(L"table-id",tempStringStream.str());
			long colCount=0;
			pHTMLTable->get_cols(&colCount);
			if(colCount>0) {
				tempStringStream.str(L"");
				tempStringStream<<colCount;
				parentNode->addAttribute(L"table-columncount",tempStringStream.str());
			}
			IHTMLElementCollection* pHTMLElementCollection=NULL;
			pHTMLTable->get_rows(&pHTMLElementCollection);
			if(pHTMLElementCollection) {
				long rowCount=0;
				pHTMLElementCollection->get_length(&rowCount);
				if(rowCount>0) {
					tempStringStream.str(L"");
					tempStringStream<<rowCount;
					parentNode->addAttribute(L"table-rowcount",tempStringStream.str());
				}
				pHTMLElementCollection->Release();
			}
			pHTMLTable->Release();
		}
	}
	//Collect row information
	if(tableInfoPtr&&!invisible&&nodeName.compare(L"TR")==0) {
		IHTMLTableRow* pHTMLTableRow=NULL;
		pHTMLDOMNode->QueryInterface(IID_IHTMLTableRow,(void**)&pHTMLTableRow);
		if(pHTMLTableRow) {
			pHTMLTableRow->get_rowIndex(&(tableInfoPtr->curRowIndex));
			(tableInfoPtr->curRowIndex)++;
			pHTMLTableRow->Release();
		}
	}
	//Collect table cell information
	if(tableInfoPtr&&!invisible&&(nodeName.compare(L"TD")==0||nodeName.compare(L"TH")==0)) {
		tempStringStream.str(L"");
		tempStringStream<<tableInfoPtr->tableID;
		parentNode->addAttribute(L"table-id",tempStringStream.str());
		//A cell with the headers attribute is definitly a data table
		tempIter=HTMLAttribsMap.find(L"headers");
		if(tempIter!=HTMLAttribsMap.end()&&!tempIter->second.empty()) {
			tableInfoPtr->definitData=true;
		}
		if(tableInfoPtr->curRowIndex>0) {
			tempStringStream.str(L"");
			tempStringStream<<tableInfoPtr->curRowIndex;
			parentNode->addAttribute(L"table-rownumber",tempStringStream.str());
		}
		IHTMLTableCell* pHTMLTableCell=NULL;
		pHTMLDOMNode->QueryInterface(IID_IHTMLTableCell,(void**)&pHTMLTableCell);
		if(pHTMLTableCell) {
			long columnIndex=0;
			pHTMLTableCell->get_cellIndex(&columnIndex);
			columnIndex++;
			if(columnIndex>0) {
				tempStringStream.str(L"");
				tempStringStream<<columnIndex;
				parentNode->addAttribute(L"table-columnnumber",tempStringStream.str());
			}
			long colSpan=0;
			pHTMLTableCell->get_colSpan(&colSpan);
			if(colSpan>1) {
				tempStringStream.str(L"");
				tempStringStream<<colSpan;
				parentNode->addAttribute(L"table-columnsspanned",tempStringStream.str());
			}
			long rowSpan=0;
			pHTMLTableCell->get_rowSpan(&rowSpan);
			if(rowSpan>1) {
				tempStringStream.str(L"");
				tempStringStream<<rowSpan;
				parentNode->addAttribute(L"table-rowsspanned",tempStringStream.str());
			}
			pHTMLTableCell->Release();
		}
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
			fillTextFormattingForNode(pHTMLDOMNode,previousNode);
		}
	} else if(nodeName.compare(L"INPUT")==0) {
		tempIter=HTMLAttribsMap.find(L"type");
		if(tempIter!=HTMLAttribsMap.end()&&tempIter->second.compare(L"hidden")==0) {
			DEBUG_MSG(L"Node is input of type hidden, ignoring");
			return parentNode;
		}
		bool usesValue=true;
		bool usesTitle=true;
		bool isProtected=false;
		bool isFileUpload=false;
		if(tempIter!=HTMLAttribsMap.end()) {
			if(tempIter->second.compare(L"password")==0) {
				isProtected=true;
				usesTitle=false;
			} else if(tempIter->second.compare(L"file")==0) {
				isFileUpload=true;
				usesTitle=false;
			} else if(tempIter->second.compare(L"text")==0) {
				usesTitle=false;
			} else if(tempIter->second.compare(L"checkbox")==0||tempIter->second.compare(L"radio")==0) {
				usesValue=false;
			}
		}
		if(usesValue) {
			tempIter=HTMLAttribsMap.find(L"value");
			wstring inputValue=(tempIter!=HTMLAttribsMap.end())?tempIter->second:L"";
			//IE does not keep the value of passwords secure
			if(isProtected) {
				for(wstring::iterator i=inputValue.begin();i!=inputValue.end();i++) {
					*i=L'*';
				}
			} else if(isFileUpload) {
				inputValue+=L"...";
				tempStringStream.str(L"");
				tempStringStream<<ROLE_SYSTEM_PUSHBUTTON;
				parentNode->addAttribute(L"IAccessible::role",tempStringStream.str());
			}
			if(!inputValue.empty()) {
				previousNode=buffer->addTextFieldNode(parentNode,previousNode,inputValue);
			}
		}
		if(previousNode==NULL&&usesTitle) {
			tempIter=HTMLAttribsMap.find(L"title");
			if(tempIter!=HTMLAttribsMap.end()&&!tempIter->second.empty()) {
				previousNode=buffer->addTextFieldNode(parentNode,previousNode,tempIter->second);
			}
		}
		if(previousNode==NULL) {
			previousNode=buffer->addTextFieldNode(parentNode,previousNode,L" ");
		}
		if(previousNode) {
			fillTextFormattingForNode(pHTMLDOMNode,previousNode);
		}
		return parentNode;
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
						previousNode=this->fillVBuf(buffer,parentNode,previousNode,selectedPHTMLDOMNode,docHandle,tableInfoPtr,LIIndexPtr);
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
				previousNode=this->fillVBuf(buffer,parentNode,previousNode,childPHTMLDOMNode,docHandle,tableInfoPtr,LIIndexPtr);
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
						VBufStorage_fieldNode_t* tempNode=this->fillVBuf(buffer,parentNode,previousNode,childPHTMLDOMNode,docHandle,tableInfoPtr,LIIndexPtr);
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
	if (!invisible && nodeName.compare(L"TEXTAREA")==0) {
		if(parentNode->getLength()==0) 
			buffer->addTextFieldNode(parentNode,previousNode,L" ");
	}
	if(!invisible&&nodeName.compare(L"TABLE")==0) {
		assert(tableInfoPtr);
		if(!tableInfoPtr->definitData) {
			parentNode->addAttribute(L"table-layout",L"1");
		}
		delete tableInfoPtr;
		tableInfoPtr=NULL;
	}
	//Table cells should always be represented by at least a space, but if a space, then they should not be block.
	if(!invisible&&(nodeName.compare(L"TD")==0||nodeName.compare(L"TH")==0)) {
		if(parentNode->getLength()==0) {
			parentNode->setIsBlock(false);
			buffer->addTextFieldNode(parentNode,previousNode,L" ");
		}
	}
	return parentNode;
}

void MshtmlVBufBackend_t::render(VBufStorage_buffer_t* buffer, int docHandle, int ID, VBufStorage_controlFieldNode_t* oldNode) {
	DEBUG_MSG(L"Rendering from docHandle "<<docHandle<<L", ID "<<ID<<L", in to buffer at "<<buffer);
	DEBUG_MSG(L"Getting document from window "<<docHandle);
	int res=SendMessage((HWND)docHandle,WM_HTML_GETOBJECT,0,0);
	if(res==0) {
		DEBUG_MSG(L"Error getting document using WM_HTML_GETOBJECT");
		return;
	}
IHTMLDOMNode* pHTMLDOMNode=NULL;
	if(oldNode!=NULL) {
		IHTMLElement2* pHTMLElement2=(static_cast<MshtmlVBufStorage_controlFieldNode_t*>(oldNode))->pHTMLElement2;
		assert(pHTMLElement2);
		pHTMLElement2->QueryInterface(IID_IHTMLDOMNode,(void**)&pHTMLDOMNode);
	} else {
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
		if(pHTMLElement->QueryInterface(IID_IHTMLDOMNode,(void**)&pHTMLDOMNode)!=S_OK) {
			DEBUG_MSG(L"Could not get IHTMLDOMNode");
			pHTMLElement->Release();
			return;
		}
		pHTMLElement->Release();
	}
	assert(pHTMLDOMNode);
	this->fillVBuf(buffer,NULL,NULL,pHTMLDOMNode,docHandle,NULL,NULL);
	pHTMLDOMNode->Release();
}

MshtmlVBufBackend_t::MshtmlVBufBackend_t(int docHandle, int ID): VBufBackend_t(docHandle,ID) {
	DEBUG_MSG(L"Mshtml backend constructor");
}

MshtmlVBufBackend_t::~MshtmlVBufBackend_t() {
	DEBUG_MSG(L"Mshtml backend destructor");
}

extern "C" __declspec(dllexport) VBufBackend_t* VBufBackend_create(int docHandle, int ID) {
	VBufBackend_t* backend=new MshtmlVBufBackend_t(docHandle,ID);
	DEBUG_MSG(L"Created new backend at "<<backend);
	return backend;
}
