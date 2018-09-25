/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2007-2017 NV Access Limited, Mozilla Corporation
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#include <memory>
#include <functional>
#include <boost/optional.hpp>
#include <windows.h>
#include <set>
#include <string>
#include <sstream>
#include <atlcomcli.h>
#include <ia2.h>
#include <common/ia2utils.h>
#include <remote/nvdaHelperRemote.h>
#include <vbufBase/backend.h>
#include <common/log.h>
#include <vbufBase/utils.h>
#include "gecko_ia2.h"

using namespace std;

CComPtr<IAccessible2> getLabelElement(IAccessible2_2* element) {
	IUnknown** ppUnk=nullptr;
	long nTargets=0;
	constexpr int numRelations=2;
	// the relation type string *must* be passed correctly as a BSTR otherwise we can see crashes in 32 bit Firefox.
	HRESULT res=element->get_relationTargetsOfType(CComBSTR(IA2_RELATION_LABELLED_BY),numRelations,&ppUnk,&nTargets);
	if(res!=S_OK) return nullptr;
	// Grab all the returned IUnknowns and store them as smart pointers within a smart pointer array 
	// so that any further returns will correctly release all the objects. 
	auto ppUnk_smart=make_unique<CComPtr<IUnknown>[]>(nTargets);
	for(int i=0;i<nTargets;++i) {
		ppUnk_smart[i].Attach(ppUnk[i]);
	}
	// we can now free the memory that Gecko  allocated to give us  the IUnknowns
	CoTaskMemFree(ppUnk);
	if(nTargets==0) {
		LOG_DEBUG(L"relationTargetsOfType for IA2_RELATION_LABELLED_BY found no targets");
		return nullptr;
	}
	return CComQIPtr<IAccessible2>(ppUnk_smart[0]);
}

#define NAVRELATION_LABELLED_BY 0x1003
#define NAVRELATION_NODE_CHILD_OF 0x1005
const wchar_t EMBEDDED_OBJ_CHAR = 0xFFFC;

HWND findRealMozillaWindow(HWND hwnd) {
	if(hwnd==0||!IsWindow(hwnd))
		return (HWND)0;

	wchar_t className[256];
	bool foundWindow=false;
	HWND tempWindow=hwnd;
	do {
		if(GetClassName(tempWindow,className,256)==0)
			return hwnd;
		if(wcscmp(L"MozillaWindowClass",className)!=0)
			foundWindow=true;
		else
			tempWindow=GetAncestor(tempWindow,GA_PARENT);
	} while(tempWindow&&!foundWindow);
	if(GetClassName(tempWindow,className,256)!=0&&wcsstr(className,L"Mozilla")==className)
		hwnd=tempWindow;
	return hwnd;
}

IAccessible2* IAccessible2FromIdentifier(int docHandle, int ID) {
	IAccessible* pacc=NULL;
	IServiceProvider* pserv=NULL;
	IAccessible2* pacc2=NULL;
	VARIANT varChild;
	if(AccessibleObjectFromEvent((HWND)UlongToHandle(docHandle),OBJID_CLIENT,ID,&pacc,&varChild)!=S_OK) {
		LOG_DEBUG(L"AccessibleObjectFromEvent failed");
		return NULL;
	}
	if (varChild.lVal!=CHILDID_SELF) {
		// IAccessible2 can't be implemented on a simple child,
		// so this object is invalid.
		pacc->Release();
		return NULL;
	}
	VariantClear(&varChild);
	if(pacc->QueryInterface(IID_IServiceProvider,(void**)&pserv)!=S_OK) {
		pacc->Release();
		return NULL;
	}  
	pacc->Release();
	pserv->QueryService(IID_IAccessible,IID_IAccessible2,(void**)&pacc2);
	pserv->Release();
	return pacc2;
}

template<typename TableType> inline void fillTableCounts(VBufStorage_controlFieldNode_t* node, IAccessible2* pacc, TableType* paccTable) {
	wostringstream s;
	long count = 0;
	// Fetch row and column counts and add them as two sets of attributes on this vbuf node.
	// The first set: table-physicalrowcount and table-physicalcolumncount represent the physical topology of the table and can be used programmatically to understand table limits.
	// The second set: table-rowcount and table-columncount are duplicates of the physical ones, however may be overridden later on in fillVBuf with ARIA attributes. They are what is reported to the user.
	if (paccTable->get_nRows(&count) == S_OK) {
		s << count;
		node->addAttribute(L"table-physicalrowcount", s.str());
		node->addAttribute(L"table-rowcount", s.str());
		s.str(L"");
	}
	if (paccTable->get_nColumns(&count) == S_OK) {
		s << count;
		node->addAttribute(L"table-physicalcolumncount", s.str());
		node->addAttribute(L"table-columncount", s.str());
	}
}

inline int getTableIDFromCell(IAccessibleTableCell* tableCell) {
	IUnknown* unk = NULL;
	if (tableCell->get_table(&unk) != S_OK || !unk)
		return 0;
	IAccessible2* acc = NULL;
	HRESULT res;
	res = unk->QueryInterface(IID_IAccessible2, (void**)&acc);
	unk->Release();
	if (res != S_OK || !acc)
		return 0;
	int id=0;
	acc->get_uniqueID((long*)&id);
	acc->Release();
	return id;
}

inline void fillTableCellInfo_IATable(VBufStorage_controlFieldNode_t* node, IAccessibleTable* paccTable, const wstring& cellIndexStr) {
	wostringstream s;
	long cellIndex = _wtoi(cellIndexStr.c_str());
	long row, column, rowExtents, columnExtents;
	boolean isSelected;
	// Fetch row and column extents and add them as attributes on this node.
	// for rowNumber and columnNumber, store these as two sets of attributes.
	// The first set: table-physicalrownumber and table-physicalcolumnnumber represent the physical topology of the table and can be used programmatically to fetch other table cells with IAccessibleTable etc.
	// The second set: table-rownumber and table-columnnumber are duplicates of the physical ones, however may be overridden later on in fillVBuf with ARIA attributes. They are what is reported to the user.
	if (paccTable->get_rowColumnExtentsAtIndex(cellIndex, &row, &column, &rowExtents, &columnExtents, &isSelected) == S_OK) {
		s << row + 1;
		node->addAttribute(L"table-physicalrownumber", s.str());
		node->addAttribute(L"table-rownumber", s.str());
		s.str(L"");
		s << column + 1;
		node->addAttribute(L"table-physicalcolumnnumber", s.str());
		node->addAttribute(L"table-columnnumber", s.str());
		if (columnExtents > 1) {
			s.str(L"");
			s << columnExtents;
			node->addAttribute(L"table-columnsspanned", s.str());
		}
		if (rowExtents > 1) {
			s.str(L"");
			s << rowExtents;
			node->addAttribute(L"table-rowsspanned", s.str());
		}
	}
}

typedef HRESULT(STDMETHODCALLTYPE IAccessibleTableCell::*IATableCellGetHeaderCellsFunc)(IUnknown***, long*);
inline void fillTableHeaders(VBufStorage_controlFieldNode_t* node, IAccessibleTableCell* paccTableCell, const IATableCellGetHeaderCellsFunc getHeaderCells, const wstring& attribName) {
	wostringstream s;
	IUnknown** headerCells;
	long nHeaderCells;

	if ((paccTableCell->*getHeaderCells)(&headerCells, &nHeaderCells) == S_OK && headerCells) {
		for (int hci = 0; hci < nHeaderCells; hci++) {
			IAccessible2* headerCellPacc = NULL;
			if (headerCells[hci]->QueryInterface(IID_IAccessible2, (void**)&headerCellPacc) != S_OK) {
				headerCells[hci]->Release();
				continue;
			}
			headerCells[hci]->Release();
			HWND hwnd;
			if (headerCellPacc->get_windowHandle(&hwnd) != S_OK) {
				headerCellPacc->Release();
				continue;
			}
			const int headerCellDocHandle = HandleToUlong(findRealMozillaWindow(hwnd));
			int headerCellID;
			if (headerCellPacc->get_uniqueID((long*)&headerCellID) != S_OK) {
				headerCellPacc->Release();
				continue;
			}
			s << headerCellDocHandle << L"," << headerCellID << L";";
			headerCellPacc->Release();
		}
		if (!s.str().empty())
			node->addAttribute(attribName, s.str());
		CoTaskMemFree(headerCells);
	}
}

inline void GeckoVBufBackend_t::fillTableCellInfo_IATable2(VBufStorage_controlFieldNode_t* node, IAccessibleTableCell* paccTableCell) {
	wostringstream s;

	long row, column, rowExtents, columnExtents;
	boolean isSelected;
	// Fetch row and column extents and add them as attributes on this node.
	// for rowNumber and columnNumber, store these as two sets of attributes.
	// The first set: table-physicalrownumber and table-physicalcolumnnumber represent the physical topology of the table and can be used programmatically to fetch other table cells with IAccessibleTable etc.
	// The second set: table-rownumber and table-columnnumber are duplicates of the physical ones, however may be overridden later on in fillVBuf with ARIA attributes. They are what is reported to the user.
	if (paccTableCell->get_rowColumnExtents(&row, &column, &rowExtents, &columnExtents, &isSelected) == S_OK) {
		s << row + 1;
		node->addAttribute(L"table-physicalrownumber", s.str());
		node->addAttribute(L"table-rownumber", s.str());
		s.str(L"");
		s << column + 1;
		node->addAttribute(L"table-physicalcolumnnumber", s.str());
		node->addAttribute(L"table-columnnumber", s.str());
		if (columnExtents > 1) {
			s.str(L"");
			s << columnExtents;
			node->addAttribute(L"table-columnsspanned", s.str());
		}
		if (rowExtents > 1) {
			s.str(L"");
			s << rowExtents;
			node->addAttribute(L"table-rowsspanned", s.str());
		}
	}

	if (this->shouldDisableTableHeaders)
		return;

	fillTableHeaders(node, paccTableCell, &IAccessibleTableCell::get_columnHeaderCells, L"table-columnheadercells");
	fillTableHeaders(node, paccTableCell, &IAccessibleTableCell::get_rowHeaderCells, L"table-rowheadercells");
}

void GeckoVBufBackend_t::versionSpecificInit(IAccessible2* pacc) {
	// Defaults.
	this->shouldDisableTableHeaders = false;
	this->hasEncodedAccDescription = false;

	IServiceProvider* serv = NULL;
	if (pacc->QueryInterface(IID_IServiceProvider, (void**)&serv) != S_OK)
		return;
	IAccessibleApplication* iaApp = NULL;
	if (serv->QueryService(IID_IAccessibleApplication, IID_IAccessibleApplication, (void**)&iaApp) != S_OK) {
		serv->Release();
		return;
	}
	serv->Release();

	BSTR toolkitName = NULL;
	if (iaApp->get_toolkitName(&toolkitName) != S_OK) {
		iaApp->Release();
		return;
	}
	BSTR toolkitVersion = NULL;
	if (iaApp->get_toolkitVersion(&toolkitVersion) != S_OK) {
		iaApp->Release();
		SysFreeString(toolkitName);
		return;
	}
	iaApp->Release();
	iaApp = NULL;

	if (wcscmp(toolkitName, L"Gecko") == 0) {
		if (wcsncmp(toolkitVersion, L"1.", 2) == 0) {
			if (wcsncmp(toolkitVersion, L"1.9.2.", 6) == 0) {
				// Gecko 1.9.2.x.
				// Retrieve the digits for the final part of the main version number.
				wstring verPart;
				for (wchar_t* c = &toolkitVersion[6]; iswdigit(*c); c++)
					verPart += *c;
				if (_wtoi(verPart.c_str()) <= 10) {
					// Gecko <= 1.9.2.10 will crash if we try to retrieve headers on some table cells, so disable them.
					this->shouldDisableTableHeaders = true;
				}
			}
			// Gecko 1.x uses accDescription to encode position info as well as the description.
			this->hasEncodedAccDescription = true;
		}
	}

	SysFreeString(toolkitName);
	SysFreeString(toolkitVersion);
}

bool isLabelVisible(IAccessible2* pacc2) {
	CComQIPtr<IAccessible2_2> pacc2_2=pacc2;
	if(!pacc2_2) return false;
	auto targetAcc=getLabelElement(pacc2_2);
	if(!targetAcc) return false;
	CComVariant child;
	child.vt = VT_I4;
	child.lVal = 0;
	CComVariant state;
	HRESULT res = targetAcc->get_accState(child, &state);
	if (res != S_OK)
		return false;
	if (state.lVal & STATE_SYSTEM_INVISIBLE)
		return false;
	return true;
}

long getChildCount(const bool isAriaHidden, IAccessible2 * const pacc){
	long rawChildCount = 0;
	if(!isAriaHidden){
		auto res = pacc->get_accChildCount(&rawChildCount);
		if(res != S_OK){
			rawChildCount = 0;
		}
	}
	return rawChildCount;
}

bool hasAriaHiddenAttribute(const map<wstring,wstring>& IA2AttribsMap){
	const auto IA2AttribsMapIt = IA2AttribsMap.find(L"hidden");
	return (IA2AttribsMapIt != IA2AttribsMap.end() && IA2AttribsMapIt->second == L"true");
}

const vector<wstring>ATTRLIST_ROLES(1, L"IAccessible2::attribute_xml-roles");
const wregex REGEX_PRESENTATION_ROLE(L"IAccessible2\\\\:\\\\:attribute_xml-roles:.*\\bpresentation\\b.*;");

VBufStorage_fieldNode_t* GeckoVBufBackend_t::fillVBuf(IAccessible2* pacc,
	VBufStorage_buffer_t* buffer, VBufStorage_controlFieldNode_t* parentNode, VBufStorage_fieldNode_t* previousNode,
	IAccessibleTable* paccTable, IAccessibleTable2* paccTable2, long tableID, const wchar_t* parentPresentationalRowNumber,
	bool ignoreInteractiveUnlabelledGraphics
) {
	nhAssert(buffer); //buffer can't be NULL
	nhAssert(!parentNode||buffer->isNodeInBuffer(parentNode)); //parent node must be in buffer
	nhAssert(!previousNode||buffer->isNodeInBuffer(previousNode)); //Previous node must be in buffer
	VBufStorage_fieldNode_t* tempNode;
	//all IAccessible methods take a variant for childID, get one ready
	VARIANT varChild;
	varChild.vt=VT_I4;
	varChild.lVal=0;
	wostringstream s;

	//get docHandle -- IAccessible2 windowHandle
	HWND docHwnd;
	if(pacc->get_windowHandle(&docHwnd)!=S_OK) {
		LOG_DEBUG(L"pacc->get_windowHandle failed");
		return NULL;
	}
	const int docHandle=HandleToUlong(findRealMozillaWindow(docHwnd));
	if(!docHandle) {
		LOG_DEBUG(L"bad docHandle");
		return NULL;
	}
	//Get ID -- IAccessible2 uniqueID
	int ID;
	if(pacc->get_uniqueID((long*)&ID)!=S_OK) {
		LOG_DEBUG(L"pacc->get_uniqueID failed");
		return NULL;
	}

	//Make sure that we don't already know about this object -- protect from loops
	if(buffer->getControlFieldNodeWithIdentifier(docHandle,ID)) {
		LOG_DEBUG(L"a node with this docHandle and ID already exists, returning NULL");
		return NULL;
	}

	if(buffer!=this&&parentNode) {
		// We are rendering a subtree of a temp buffer
		auto existingNode=this->reuseExistingNodeInRender(parentNode,previousNode,docHandle,ID);
		if(existingNode) {
			// This child already exists on the backend, we can reuse it.
			return buffer->addReferenceNodeToBuffer(parentNode,previousNode,existingNode);
		}
	}

	//Add this node to the buffer
	parentNode=buffer->addControlFieldNode(parentNode,previousNode,docHandle,ID,TRUE);
	nhAssert(parentNode); //new node must have been created
	previousNode=NULL;

	//Get role -- IAccessible2 role
	long role=0;
	BSTR roleString=NULL;
	if(pacc->role(&role)!=S_OK)
		role=IA2_ROLE_UNKNOWN;
	VARIANT varRole;
	VariantInit(&varRole);
	if(role==0) {
		if(pacc->get_accRole(varChild,&varRole)!=S_OK) {
			LOG_DEBUG(L"accRole failed");
		}
		if(varRole.vt==VT_I4)
			role=varRole.lVal;
		else if(varRole.vt==VT_BSTR)
			roleString=varRole.bstrVal;
	}
	//Add role as an attrib
	if(roleString)
		s<<roleString;
	else
		s<<role;
	parentNode->addAttribute(L"IAccessible::role",s.str());
	s.str(L"");
	VariantClear(&varRole);

	//get states -- IAccessible accState
	VARIANT varState;
	VariantInit(&varState);
	if(pacc->get_accState(varChild,&varState)!=S_OK) {
		LOG_DEBUG(L"pacc->get_accState failed");
		varState.vt=VT_I4;
		varState.lVal=0;
	}
	int states=varState.lVal;
	VariantClear(&varState);
	//Add each state that is on, as an attrib
	for(int i=0;i<32;++i) {
		int state=1<<i;
		if(state&states) {
			s<<L"IAccessible::state_"<<state;
			parentNode->addAttribute(s.str(),L"1");
			s.str(L"");
		}
	}
	//get IA2States -- IAccessible2 states
	AccessibleStates IA2States;
	if(pacc->get_states(&IA2States)!=S_OK) {
		LOG_DEBUG(L"pacc->get_states failed");
		IA2States=0;
	}
	// Remove state_editible from tables as Gecko exposes it for ARIA grids which is not in the ARIA spec. 
	if(IA2States&IA2_STATE_EDITABLE&&role==ROLE_SYSTEM_TABLE) {
			IA2States-=IA2_STATE_EDITABLE;
	}
	//Add each state that is on, as an attrib
	for(int i=0;i<32;++i) {
		int state=1<<i;
		if(state&IA2States) {
			s<<L"IAccessible2::state_"<<state;
			parentNode->addAttribute(s.str(),L"1");
			s.str(L"");
		}
	}

	//get keyboardShortcut -- IAccessible accKeyboardShortcut;
	BSTR keyboardShortcut;
	if(pacc->get_accKeyboardShortcut(varChild,&keyboardShortcut)==S_OK) {
		parentNode->addAttribute(L"keyboardShortcut",keyboardShortcut);
		//Free keyboardShortcut string memory
		SysFreeString(keyboardShortcut);
	} else
		parentNode->addAttribute(L"keyboardShortcut",L"");

	//get IA2Attributes -- IAccessible2 attributes;
	BSTR IA2Attributes;
	map<wstring,wstring> IA2AttribsMap;
	if(pacc->get_attributes(&IA2Attributes)==S_OK) {
		IA2AttribsToMap(IA2Attributes,IA2AttribsMap);
		SysFreeString(IA2Attributes);
		// Add each IA2 attribute as an attrib.
		for(map<wstring,wstring>::const_iterator it=IA2AttribsMap.begin();it!=IA2AttribsMap.end();++it) {
			s<<L"IAccessible2::attribute_"<<it->first;
			parentNode->addAttribute(s.str(),it->second);
			s.str(L"");
		}
	} else
		LOG_DEBUG(L"pacc->get_attributes failed");
	map<wstring,wstring>::const_iterator IA2AttribsMapIt;

	//Check IA2Attributes, and or the role etc to work out if this object is a block element
	bool isBlockElement=TRUE;
	if(IA2States&IA2_STATE_MULTI_LINE) {
		// Multiline nodes should always be block.
		isBlockElement=TRUE;
	} else if((IA2AttribsMapIt=IA2AttribsMap.find(L"display"))!=IA2AttribsMap.end()) {
		// If there is a display attribute, we can rely solely on this to determine whether this is a block element or not.
		isBlockElement=(IA2AttribsMapIt->second!=L"inline"&&IA2AttribsMapIt->second!=L"inline-block");
	} else if((IA2AttribsMapIt=IA2AttribsMap.find(L"formatting"))!=IA2AttribsMap.end()&&IA2AttribsMapIt->second==L"block") {
		isBlockElement=TRUE;
	} else if(role==ROLE_SYSTEM_TABLE||role==ROLE_SYSTEM_CELL||role==IA2_ROLE_SECTION||role==ROLE_SYSTEM_DOCUMENT||role==IA2_ROLE_INTERNAL_FRAME||role==IA2_ROLE_UNKNOWN||role==ROLE_SYSTEM_SEPARATOR) {
		isBlockElement=TRUE;
	} else {
		isBlockElement=FALSE;
	}
	parentNode->isBlock=isBlockElement;

	// force   isHidden to True if this has an ARIA role of presentation but its focusble -- Gecko does not hide this itself.
	if((states&STATE_SYSTEM_FOCUSABLE)&&parentNode->matchAttributes(ATTRLIST_ROLES, REGEX_PRESENTATION_ROLE)) {
		parentNode->isHidden=true;
	}
	BSTR name=NULL;
	if(pacc->get_accName(varChild,&name)!=S_OK)
		name=NULL;

	wstring description;
	BSTR rawDesc=NULL;
	if(pacc->get_accDescription(varChild,&rawDesc)==S_OK) {
		if(this->hasEncodedAccDescription) {
			if(wcsncmp(rawDesc,L"Description: ",13)==0)
				description=&rawDesc[13];
		} else
			description=rawDesc;
		parentNode->addAttribute(L"description",description);
		SysFreeString(rawDesc);
	}

	wstring locale;
	IA2Locale ia2Locale={0};
	if(pacc->get_locale(&ia2Locale)==S_OK) {
		if(ia2Locale.language) {
			locale.append(ia2Locale.language);
			SysFreeString(ia2Locale.language);
		}
		if(ia2Locale.country) {
			if(!locale.empty()) {
				locale.append(L"-");
				locale.append(ia2Locale.country);
			}
			SysFreeString(ia2Locale.country);
		}
		if(ia2Locale.variant) {
			SysFreeString(ia2Locale.variant);
		}
	}

	long left=0, top=0, width=0, height=0;
	if(pacc->accLocation(&left,&top,&width,&height,varChild)!=S_OK) {
		LOG_DEBUG(L"Error getting accLocation");
	}

	// Whether this node is editable text.
	bool isEditable = (role == ROLE_SYSTEM_TEXT && (states & STATE_SYSTEM_FOCUSABLE || states & STATE_SYSTEM_UNAVAILABLE)) || IA2States & IA2_STATE_EDITABLE;
	// Whether this node is a link or inside a link.
	int inLink = states & STATE_SYSTEM_LINKED;
	// Whether this is the root node.
	bool isRoot = ID == this->rootID;
	// Whether this is an embedded application.
		bool isEmbeddedApp = role == IA2_ROLE_EMBEDDED_OBJECT
			|| (!isRoot && (role == ROLE_SYSTEM_APPLICATION || role == ROLE_SYSTEM_DIALOG));
	// Whether this node is interactive.
	// Certain objects are never interactive, even if other checks are true.
	bool isNeverInteractive = parentNode->isHidden||(!isEditable && (isRoot || role == ROLE_SYSTEM_DOCUMENT || role == IA2_ROLE_INTERNAL_FRAME));
	bool isInteractive = !isNeverInteractive && (isEditable || inLink || states & STATE_SYSTEM_FOCUSABLE || states & STATE_SYSTEM_UNAVAILABLE || isEmbeddedApp || role == ROLE_SYSTEM_EQUATION);
	// We aren't finished calculating isInteractive yet; actions are handled below.

	const bool isAriaHidden = hasAriaHiddenAttribute(IA2AttribsMap);
	const long childCount = getChildCount(isAriaHidden, pacc);

	const bool isImgMap = role == ROLE_SYSTEM_GRAPHIC && childCount > 0;
	IA2AttribsMapIt = IA2AttribsMap.find(L"explicit-name");
	// Whether the name of this node has been explicitly set (as opposed to calculated by descendant)
	const bool nameIsExplicit = IA2AttribsMapIt != IA2AttribsMap.end() && IA2AttribsMapIt->second == L"true";
	// Whether the name is the content of this node.
	std::experimental::optional<bool> isLabelVisibleVal_;
	// A version of the isLabelVisible function that caches its result
	auto isLabelVisibleCached=[&]() {
		if(!isLabelVisibleVal_) {
			isLabelVisibleVal_=isLabelVisible(pacc);
		}
		return *isLabelVisibleVal_;
	};
	const bool nameIsContent = isEmbeddedApp
		|| role == ROLE_SYSTEM_LINK 
		|| role == ROLE_SYSTEM_PUSHBUTTON 
		|| role == IA2_ROLE_TOGGLE_BUTTON 
		|| role == ROLE_SYSTEM_MENUITEM 
		|| (role == ROLE_SYSTEM_GRAPHIC && !isImgMap) 
		|| (role == ROLE_SYSTEM_TEXT && !isEditable) 
		|| role == IA2_ROLE_HEADING 
		|| role == ROLE_SYSTEM_PAGETAB 
		|| role == ROLE_SYSTEM_BUTTONMENU
		|| ((role == ROLE_SYSTEM_CHECKBUTTON || role == ROLE_SYSTEM_RADIOBUTTON) && !isLabelVisibleCached());
	// Whether this node has a visible label somewhere else in the tree
	const bool labelVisible = nameIsExplicit && name && name[0] //this node must actually have an explicit name, and not be just an empty string
		&&(!nameIsContent||role==ROLE_SYSTEM_TABLE) // We only need to know if the name won't be used as content or if it is a table (for table summary)
		&&isLabelVisibleCached(); // actually do the check
	// If the node is explicitly labeled for accessibility, and we haven't used the label as the node's content, and the label does not visibly appear anywhere else in the tree (E.g. aria-label on an edit field)
	// then ensure that the label is always reported along withe the node
	// We must exclude tables from this though as table summaries / captions are handled very specifically
	if(nameIsExplicit && !nameIsContent && (role != ROLE_SYSTEM_TABLE) && !labelVisible) {
		parentNode->addAttribute(L"alwaysReportName",L"true");
	}

	IAccessibleText* paccText=NULL;
	//get IAccessibleText interface
	pacc->QueryInterface(IID_IAccessibleText,(void**)&paccText);
	//Get the text from the IAccessibleText interface
	BSTR IA2Text=NULL;
	int IA2TextLength=0;
	if (paccText && paccText->get_text(0, IA2_TEXT_OFFSET_LENGTH, &IA2Text) == S_OK && IA2Text)
		IA2TextLength=SysStringLen(IA2Text);
	// Determine whether the text is extraneous whitespace.
	bool IA2TextIsUnneededSpace=true;
	// Whitespace isn't extraneous in editable controls.
	if (IA2TextLength > 0 && !isEditable) {
		for(int i=0;i<IA2TextLength;++i) {
			if(IA2Text[i]==L'\n'||IA2Text[i]==L'\xfffc'||!iswspace(IA2Text[i])) {
				IA2TextIsUnneededSpace=false;
				break;
			}
		}
	} else
		IA2TextIsUnneededSpace=false;

	// Whether a node is visible.
	// An invisible node should not be rendered, but will have a presence in the buffer.
	bool isVisible = true;
	// Whether to render children, including text content.
	// Note that we may still render the name, value, etc. even if we don't render children.
	bool renderChildren = true;
	if (isAriaHidden) {
		// aria-hidden
		isVisible = false;
	} else {
		// If a node has children, it's visible.
		isVisible = width > 0 && height > 0 || childCount > 0;
		if (IA2TextIsUnneededSpace
			|| role == ROLE_SYSTEM_COMBOBOX
			|| (role == ROLE_SYSTEM_LIST && !(states & STATE_SYSTEM_READONLY))
			|| isEmbeddedApp
			|| role == ROLE_SYSTEM_OUTLINE
			|| role == ROLE_SYSTEM_EQUATION
			|| (nameIsContent && nameIsExplicit)
		) {
			renderChildren = false;
		}
	}

	//Expose all available actions
	IAccessibleAction* paccAction=NULL;
	pacc->QueryInterface(IID_IAccessibleAction,(void**)&paccAction);
	if(paccAction) {
		long nActions=0;
		paccAction->nActions(&nActions);
		for(int i=0;i<nActions;++i) {
			BSTR actionName=NULL;
			paccAction->get_name(i,&actionName);
			if(actionName) {
				wstring attribName=L"IAccessibleAction_";
				attribName+=actionName;
				s<<i;
				parentNode->addAttribute(attribName,s.str());
				s.str(L"");
				if(!isNeverInteractive&&(wcscmp(actionName, L"click")==0||wcscmp(actionName, L"showlongdesc")==0)) {
					isInteractive=true;
				}
				SysFreeString(actionName);
			}
		}
		paccAction->Release();
	}

	// Handle table cell information.
	IAccessibleTableCell* paccTableCell = NULL;
	if(pacc->QueryInterface(IID_IAccessibleTableCell, (void**)&paccTableCell)!=S_OK) {
		paccTableCell=nullptr;
	}

	if(paccTable2) {
		// We are rendering a node that is part of a table (row group, row or cell).
		// Set some properties to ensure that this and other nodes in the table aare correctly re-rendered if the table changes,
		// so that the table's row and column cordinates remain accurate.
		// setting denyReuseIfPreviousSiblingsChange ensures that if any part of the table is added or removed previous to this node,
		// this node will not be reused (as its row / column coordinates would now be out of date).
		LOG_DEBUG(L"Setting node's denyReuseIfPreviousSiblingsChanged to true");
		parentNode->denyReuseIfPreviousSiblingsChanged=true;
		if(!paccTableCell) { // just rows and row groups
			// setting requiresParentUpdate ensures that if this node is specifically invalidated,
			// its parent will also be invalidated.
			// For example, if this is a table row group, its rerendering may change the number of rows inside. 
			// this in turn would affect the coordinates of all table cells in table rows after this row group.
			// Thus, ensuring we rerender this node's parent, gives a chance to rerender other table rows.
			LOG_DEBUG(L"Setting node's requiresParentUpdate to true");
			parentNode->requiresParentUpdate=true;
			// Setting alwaysRerenderChildren ensures that if this node is rerendered, none of its children are reused.
			// For example, if this is a table row that is rerendered (perhaps due to a previous table row being added),
			// this row's cells can't be reused because their coordinates would now be out of date.
			LOG_DEBUG(L"Setting node's alwaysRerenderChildren to true");
			parentNode->alwaysRerenderChildren=true;
		}
	}

	// For IAccessibleTable, we must always be passed the table interface by the caller.
	// For IAccessibleTable2, we can always obtain the cell interface,
	// which allows us to handle updates to table cells.
	if (
		 paccTableCell || // IAccessibleTable2
		(paccTable && (IA2AttribsMapIt = IA2AttribsMap.find(L"table-cell-index")) != IA2AttribsMap.end()) // IAccessibleTable
	) {
		if (paccTableCell) {
			// IAccessibleTable2
			this->fillTableCellInfo_IATable2(parentNode, paccTableCell);
			if (!paccTable2) {
				// This is an update; we're not rendering the entire table.
				tableID = getTableIDFromCell(paccTableCell);
			}
			paccTableCell->Release();
			paccTableCell = NULL;
		} else // IAccessibleTable
			fillTableCellInfo_IATable(parentNode, paccTable, IA2AttribsMapIt->second);
		// tableID is the IAccessible2::uniqueID for paccTable.
		s << tableID;
		parentNode->addAttribute(L"table-id", s.str());
		s.str(L"");
		// We're now within a cell, so descendant nodes shouldn't refer to this table anymore.
		paccTable = NULL;
		paccTable2 = NULL;
		tableID = 0;
	}
	// Handle table information.
	// Don't release the table unless it was created in this call.
	bool releaseTable = false;
	// If paccTable is not NULL, we're within a table but not yet within a cell, so don't bother to query for table info.
	if (!paccTable2 && !paccTable) {
		// Try to get table information.
		pacc->QueryInterface(IID_IAccessibleTable2,(void**)&paccTable2);
		if(!paccTable2)
			pacc->QueryInterface(IID_IAccessibleTable,(void**)&paccTable);
		if (paccTable2||paccTable) {
			// We did the QueryInterface for paccTable, so we must release it after all calls that use it are done.
			releaseTable = true;
			// This is a table, so add its information as attributes.
			if((IA2AttribsMapIt = IA2AttribsMap.find(L"layout-guess")) != IA2AttribsMap.end())
				parentNode->addAttribute(L"table-layout",L"1");
			tableID = ID;
			s << ID;
			parentNode->addAttribute(L"table-id", s.str());
			s.str(L"");
			if(paccTable2)
				fillTableCounts<IAccessibleTable2>(parentNode, pacc, paccTable2);
			else
				fillTableCounts<IAccessibleTable>(parentNode, pacc, paccTable);
			// Add the table summary if one is present and the table is visible.
			if (isVisible &&
				(!description.empty() && (tempNode = buffer->addTextFieldNode(parentNode, previousNode, description))) ||
				// If there is no caption, the summary (if any) is the name.
				// There is no caption if the label isn't visible.
				(name && !labelVisible && (tempNode = buffer->addTextFieldNode(parentNode, previousNode, name)))
			) {
				if(!locale.empty()) tempNode->addAttribute(L"language",locale);
				previousNode = tempNode;
			}
		}
	}

	// Add some presentational table attributes
	// Note these are only for reporting, the physical table attributes (table-physicalrownumber etc) for aiding in navigation etc are added  later on.
	// propagate table-rownumber down to the cell as Gecko only includes it on the row itself
	if(parentPresentationalRowNumber) 
		parentNode->addAttribute(L"table-rownumber",parentPresentationalRowNumber);
	const wchar_t* presentationalRowNumber=NULL;
	if((IA2AttribsMapIt = IA2AttribsMap.find(L"rowindex")) != IA2AttribsMap.end()) {
		parentNode->addAttribute(L"table-rownumber",IA2AttribsMapIt->second);
		presentationalRowNumber=IA2AttribsMapIt->second.c_str();
	}
	if((IA2AttribsMapIt = IA2AttribsMap.find(L"colindex")) != IA2AttribsMap.end())
		parentNode->addAttribute(L"table-columnnumber",IA2AttribsMapIt->second);
	if((IA2AttribsMapIt = IA2AttribsMap.find(L"rowcount")) != IA2AttribsMap.end())
		parentNode->addAttribute(L"table-rowcount",IA2AttribsMapIt->second);
	if((IA2AttribsMapIt = IA2AttribsMap.find(L"colcount")) != IA2AttribsMap.end())
		parentNode->addAttribute(L"table-columncount",IA2AttribsMapIt->second);

	BSTR value=NULL;
	if(pacc->get_accValue(varChild,&value)==S_OK) {
		if(value&&SysStringLen(value)==0) {
			SysFreeString(value);
			value=NULL;
		}
	}

	//If the name isn't being rendered as the content, then add the name as a field attribute.
	if (!nameIsContent && name)
		parentNode->addAttribute(L"name", name);

	if(nameIsContent) {
		// We may render an accessible name for this node if it has been explicitly set or it has no useful content. 
		parentNode->alwaysRerenderDescendants=true;
	}

	if (isVisible) {
		if ( isImgMap && name ) {
			// This is an image map with a name. Render the name first.
			previousNode=buffer->addTextFieldNode(parentNode,previousNode,name);
			if(previousNode&&!locale.empty()) previousNode->addAttribute(L"language",locale);
		}

		if (isInteractive && !ignoreInteractiveUnlabelledGraphics) {
			// Don't render interactive unlabelled graphic descendants if this node has a name,
			// as author supplied names are preferred.
			ignoreInteractiveUnlabelledGraphics = name != NULL;
		}

		if (renderChildren && IA2TextLength > 0) {
			// Process IAccessibleText.
			int chunkStart=0;
			long attribsStart = 0;
			long attribsEnd = 0;
			map<wstring,wstring> textAttribs;
			auto linkGetter = makeHyperlinkGetter(pacc);
			for(int i=0;;++i) {
				if(i!=chunkStart&&(i==IA2TextLength||i==attribsEnd||IA2Text[i]==EMBEDDED_OBJ_CHAR)) {
					// We've reached the end of the current chunk of text.
					// (A chunk ends at the end of the text, at the end of an attributes run
					// or at an embedded object char.)
					// Add the chunk to the buffer.
					if(tempNode=buffer->addTextFieldNode(parentNode,previousNode,wstring(IA2Text+chunkStart,i-chunkStart))) {
						previousNode=tempNode;
						// Add the IA2Text start offset as an attribute on the node.
						s << chunkStart;
						previousNode->addAttribute(L"ia2TextStartOffset", s.str());
						s.str(L"");
						// Add text attributes.
						for(map<wstring,wstring>::const_iterator it=textAttribs.begin();it!=textAttribs.end();++it)
							previousNode->addAttribute(it->first,it->second);
						#define copyObjectAttribute(attr) if ((IA2AttribsMapIt = IA2AttribsMap.find(attr)) != IA2AttribsMap.end()) \
							previousNode->addAttribute(attr, IA2AttribsMapIt->second);
						copyObjectAttribute(L"text-align");
						#undef copyObjectAttribute
					}
				}
				if(i==IA2TextLength)
					break;
				if(i==attribsEnd) {
					// We've hit the end of the last attributes run and thus the start of the next.
					textAttribs.clear();
					chunkStart=i;
					BSTR attribsStr;
					if(paccText->get_attributes(attribsEnd,&attribsStart,&attribsEnd,&attribsStr)==S_OK) {
						if(attribsStr) {
							IA2AttribsToMap(attribsStr,textAttribs);
							SysFreeString(attribsStr);
						}
					} else {
						// If attributes fails, assume it'll fail for the entire text.
						attribsEnd=IA2TextLength;
					}
				}
				if (IA2Text[i] == EMBEDDED_OBJ_CHAR && linkGetter) {
					// Embedded object char.
					// The next chunk of text shouldn't include this char.
					chunkStart=i+1;
					// In Gecko, hyperlinks correspond to embedded object chars,
					// so there's no need to call IAHyperlink::hyperlinkIndex.
					IAccessibleHyperlinkPtr link = move(linkGetter->next());
					IAccessible2Ptr childPacc = link;
					if(!childPacc) {
						continue;
					}
					if (tempNode = this->fillVBuf(childPacc, buffer, parentNode, previousNode, paccTable, paccTable2, tableID, presentationalRowNumber, ignoreInteractiveUnlabelledGraphics)) {
						previousNode=tempNode;
					} else {
						LOG_DEBUG(L"Error in fillVBuf");
					}
				}
			}

		} else if (renderChildren && childCount > 0) {
			// The object has no text, but we do want to render its children.
			VARIANT* varChildren;
			if(!(varChildren=(VARIANT*)malloc(sizeof(VARIANT)*childCount))) {
				LOG_DEBUG(L"Error allocating varChildren memory");
				return NULL;
			}
			long accessibleChildrenCount = 0;
			if(AccessibleChildren(pacc,0,childCount,varChildren,&accessibleChildrenCount)!=S_OK) {
				LOG_DEBUG(L"AccessibleChildren failed");
				accessibleChildrenCount=0;
			}
			for(long i=0;i<accessibleChildrenCount;++i) {
				if (varChildren[i].vt != VT_DISPATCH) {
					VariantClear(&(varChildren[i]));
					continue;
				}
				IAccessible2* childPacc=NULL;
				if(varChildren[i].pdispVal) varChildren[i].pdispVal->QueryInterface(IID_IAccessible2,(void**)&childPacc);
				if (!childPacc) {
					VariantClear(&(varChildren[i]));
					continue;
				}
				if (tempNode = this->fillVBuf(childPacc, buffer, parentNode, previousNode, paccTable, paccTable2, tableID, presentationalRowNumber, ignoreInteractiveUnlabelledGraphics))
					previousNode=tempNode;
				else
					LOG_DEBUG(L"Error in calling fillVBuf");
				childPacc->Release();
				VariantClear(&(varChildren[i]));
			}
			free(varChildren);

		} else {
			// There were no children to render.
			if(role==ROLE_SYSTEM_GRAPHIC) {
				if (name && name[0]) {
					// The graphic has a label, so use it.
					previousNode=buffer->addTextFieldNode(parentNode,previousNode,name);
					if(previousNode&&!locale.empty()) previousNode->addAttribute(L"language",locale);
				} else if ((name && !name[0]) || ignoreInteractiveUnlabelledGraphics) {
					// alt="" or we've determined that all unlabelled graphics should be ignored,
					// so don't render the graphic at all.
					isInteractive = false;
				} else if (isInteractive) {
					// The graphic is unlabelled, but we should try to derive a name for it.
					if (inLink && value) {
						// derive the label from the link URL.
						previousNode = buffer->addTextFieldNode(parentNode, previousNode, getNameForURL(value));
					} else if ((IA2AttribsMapIt = IA2AttribsMap.find(L"src")) != IA2AttribsMap.end()) {
						// Derive the label from the graphic URL.
						previousNode = buffer->addTextFieldNode(parentNode, previousNode, getNameForURL(IA2AttribsMap[L"src"]));
					}
				}
			} else if (!nameIsContent && value) {
				previousNode=buffer->addTextFieldNode(parentNode,previousNode,value);
				if(previousNode&&!locale.empty()) previousNode->addAttribute(L"language",locale);
			}
		}

		if (!isEditable && (nameIsContent || role == IA2_ROLE_SECTION || role == IA2_ROLE_TEXT_FRAME) && !nodeHasUsefulContent(parentNode)) {
			// If there is no useful content and the name can be the content,
			// render the name if there is one.
			if(name) {
				tempNode = buffer->addTextFieldNode(parentNode, NULL, name);
				if(tempNode && !locale.empty()) tempNode->addAttribute(L"language", locale);
			} else if(role==ROLE_SYSTEM_LINK&&value) {
				// If a link has no name, derive it from the URL.
				buffer->addTextFieldNode(parentNode, NULL, getNameForURL(value));
			}
		}

		if ((role == ROLE_SYSTEM_CELL || role == ROLE_SYSTEM_ROWHEADER || role == ROLE_SYSTEM_COLUMNHEADER||role==IA2_ROLE_UNKNOWN) && parentNode->getLength() == 0) {
			// Always render a space for empty table cells and unknowns.
			previousNode=buffer->addTextFieldNode(parentNode,previousNode,L" ");
			if(previousNode&&!locale.empty()) previousNode->addAttribute(L"language",locale);
			parentNode->isBlock=false;
		}

		if ((isInteractive || role == ROLE_SYSTEM_SEPARATOR) && parentNode->getLength() == 0) {
			// If the node is interactive or otherwise relevant even when empty
			// and it still has no content, render a space so the user can access the node.
			previousNode=buffer->addTextFieldNode(parentNode,previousNode,L" ");
			if(previousNode&&!locale.empty()) previousNode->addAttribute(L"language",locale);
		}
	}

	// Clean up.
	if(name)
		SysFreeString(name);
	if(value)
		SysFreeString(value);
	if (IA2Text)
		SysFreeString(IA2Text);
	if(paccText)
		paccText->Release();
	if (releaseTable) {
		if(paccTable2)
			paccTable2->Release();
		else
			paccTable->Release();
	}

	return parentNode;
}

bool getDocumentFrame(HWND* hwnd, long* childID) {
	IAccessible2* pacc=IAccessible2FromIdentifier(HandleToUlong(*hwnd),*childID);
	if (!pacc)
		return false;

	IAccessible2* parentPacc=NULL;
	VARIANT varChild;
	varChild.vt=VT_I4;
	varChild.lVal=*childID;
	VARIANT varDisp;
	if(pacc->accNavigate(NAVRELATION_NODE_CHILD_OF,varChild,&varDisp)!=S_OK) {
		pacc->Release();
		return false;
	}
	pacc->Release();

	if(varDisp.vt!=VT_DISPATCH) {
		VariantClear(&varDisp);
		return false;
	}

	if(varDisp.pdispVal->QueryInterface(IID_IAccessible2,(void**)&parentPacc)!=S_OK) {
		VariantClear(&varDisp);
		return false;
	}
	VariantClear(&varDisp);

	if(parentPacc==pacc) {
		parentPacc->Release();
		return false;
	}

	long role;
	if(parentPacc->role(&role)!=S_OK||role!=IA2_ROLE_INTERNAL_FRAME) {
		parentPacc->Release();
		return false;
	}

	if(parentPacc->get_uniqueID(childID)!=S_OK||*childID>=0) {
		parentPacc->Release();
		return false;
	}

	if(parentPacc->get_windowHandle(hwnd)!=S_OK) {
		parentPacc->Release();
		return false;
	}

	parentPacc->Release();

	return true;
}

void CALLBACK GeckoVBufBackend_t::renderThread_winEventProcHook(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time) {
	switch(eventID) {
		case EVENT_OBJECT_FOCUS:
		case EVENT_SYSTEM_ALERT:
		case IA2_EVENT_TEXT_UPDATED:
		case IA2_EVENT_TEXT_INSERTED:
		case IA2_EVENT_TEXT_REMOVED:
		case EVENT_OBJECT_REORDER:
		case EVENT_OBJECT_NAMECHANGE:
		case EVENT_OBJECT_VALUECHANGE:
		case EVENT_OBJECT_DESCRIPTIONCHANGE:
		case EVENT_OBJECT_STATECHANGE:
		case IA2_EVENT_OBJECT_ATTRIBUTE_CHANGED:
		break;
		default:
		return;
	}
	if(childID>=0||objectID!=OBJID_CLIENT)
		return;
	LOG_DEBUG(L"winEvent for window "<<hwnd);
	hwnd=findRealMozillaWindow(hwnd);
	if(!hwnd) {
		LOG_DEBUG(L"Invalid window");
		return;
	}
	int docHandle=HandleToUlong(hwnd);
	int ID=childID;
	VBufBackend_t* backend=NULL;
	for(VBufBackendSet_t::iterator i=runningBackends.begin();i!=runningBackends.end();++i) {
		HWND rootWindow=(HWND)UlongToHandle(((*i)->rootDocHandle));
		if(rootWindow==hwnd||IsChild(rootWindow,hwnd))
			backend=(*i);
		else
			continue;
		LOG_DEBUG(L"found active backend for this window at "<<backend);

		//For focus and alert events, force any invalid nodes to be updated right now
		if(eventID==EVENT_OBJECT_FOCUS||eventID==EVENT_SYSTEM_ALERT) {
			backend->forceUpdate();
			continue;
		}

		//Ignore state change events on the root node (document) as it can cause rerendering when the document goes busy
		if(eventID==EVENT_OBJECT_STATECHANGE&&hwnd==(HWND)UlongToHandle(backend->rootDocHandle)&&childID==backend->rootID)
			return;

		VBufStorage_controlFieldNode_t* node=backend->getControlFieldNodeWithIdentifier(docHandle,ID);
		if(!node&&eventID==EVENT_OBJECT_STATECHANGE) {
			// This event is possibly due to a new document loading in a subframe.
			// Gecko doesn't fire a reorder on the iframe (Mozilla bug 420845), so we need to use NODE_CHILD_OF in this case so that frames will reload.
			LOG_DEBUG(L"State change on an unknown node in a subframe, try NODE_CHILD_OF");
			if (getDocumentFrame(&hwnd, &childID)) {
				#ifdef DEBUG
				Beep(2000,50);
				#endif
				LOG_DEBUG(L"Got NODE_CHILD_OF, recursing");
				renderThread_winEventProcHook(hookID,eventID,hwnd,OBJID_CLIENT,childID,threadID,time);
			} else
				LOG_DEBUG(L"NODE_CHILD_OF failed, returning");
			continue;
		}
		if(!node)
			continue;
		backend->invalidateSubtree(node);
	}
}

void GeckoVBufBackend_t::renderThread_initialize() {
	registerWinEventHook(renderThread_winEventProcHook);
	VBufBackend_t::renderThread_initialize();
}

void GeckoVBufBackend_t::renderThread_terminate() {
	unregisterWinEventHook(renderThread_winEventProcHook);
	VBufBackend_t::renderThread_terminate();
}

void GeckoVBufBackend_t::render(VBufStorage_buffer_t* buffer, int docHandle, int ID, VBufStorage_controlFieldNode_t* oldNode) {
	IAccessible2* pacc=IAccessible2FromIdentifier(docHandle,ID);
	if(!pacc) {
		LOG_DEBUGWARNING(L"Could not get IAccessible2, returning");
		return;
	}
	if (!oldNode) {
		// This is the root node.
		this->versionSpecificInit(pacc);
	}
	if(!this->fillVBuf(pacc, buffer, NULL, NULL)) {
		if(oldNode) {
			LOG_DEBUGWARNING(L"No content rendered in update");
		} else {
			LOG_DEBUGWARNING(L"No initial content rendered");
		}
	}
	pacc->Release();
}

GeckoVBufBackend_t::GeckoVBufBackend_t(int docHandle, int ID): VBufBackend_t(docHandle,ID) {
}

GeckoVBufBackend_t::~GeckoVBufBackend_t() {
}

extern "C" __declspec(dllexport) VBufBackend_t* VBufBackend_create(int docHandle, int ID) {
	VBufBackend_t* backend=new GeckoVBufBackend_t(docHandle,ID);
	return backend;
}

BOOL WINAPI DllMain(HINSTANCE hModule,DWORD reason,LPVOID lpReserved) {
	if(reason==DLL_PROCESS_ATTACH) {
		_CrtSetReportHookW2(_CRT_RPTHOOK_INSTALL,(_CRT_REPORT_HOOKW)NVDALogCrtReportHook);
	}
	return true;
}
