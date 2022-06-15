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
#include <vector>
#include <map>
#include <optional>
#include <windows.h>
#include <set>
#include <string>
#include <sstream>
#include <atlcomcli.h>
#include <ia2.h>
#include <common/ia2utils.h>
#include <remote/nvdaHelperRemote.h>
#include <vbufBase/backend.h>
#include <vbufBase/storage.h>
#include <common/log.h>
#include <vbufBase/utils.h>
#include "gecko_ia2.h"

using namespace std;

map<wstring,wstring> createMapOfIA2AttributesFromPacc(IAccessible2* pacc) {
	map<wstring,wstring> IA2AttribsMap;
	CComBSTR IA2Attributes;
	if(pacc->get_attributes(&IA2Attributes) == S_OK) {
		IA2AttribsToMap(IA2Attributes.m_str,IA2AttribsMap);
	}
	return IA2AttribsMap;
}

bool hasXmlRoleAttribContainingValue(const map<wstring,wstring>& attribsMap, const wstring roleName) {
	const auto attribsMapIt = attribsMap.find(L"xml-roles");
	return attribsMapIt != attribsMap.end() && attribsMapIt->second.find(roleName) != wstring::npos;
}

CComPtr<IAccessible2> GeckoVBufBackend_t::getRelationElement(
	LPCOLESTR ia2TargetRelation,
	IAccessible2_2* element
) {
	IUnknown** ppUnk=nullptr;
	long nTargets=0;
	// We only need to request one relation target
	int numRelations=1;
	// However, a bug in Chrome causes a buffer overrun if numRelations is less than the total number of targets the node has.
	// Therefore, If this is Chrome, request all targets (by setting numRelations to 0) as this works around the bug.
	// There is no major performance hit to fetch all targets in Chrome as Chrome is already fetching all targets either way.
	// In Firefox there would be extra cross-proc calls.
	if(this->toolkitName.compare(L"Chrome")==0) {
		numRelations=0;
	}
	// the relation type string *must* be passed correctly as a BSTR otherwise we can see crashes in 32 bit Firefox.
	CComBSTR relationAsBSTR(ia2TargetRelation);
	HRESULT res = element->get_relationTargetsOfType(
		relationAsBSTR,
		numRelations,
		&ppUnk,
		&nTargets
	);
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
		LOG_DEBUG(L"relationTargetsOfType for " << relationAsBSTR.m_str << L" found no targets");
		return nullptr;
	}
	return CComQIPtr<IAccessible2>(ppUnk_smart[0]);
}

const wchar_t EMBEDDED_OBJ_CHAR = 0xFFFC;
// Always render a space for "empty" / metadata only
// text leaf nodes so the user can access them.
constexpr wchar_t* EMPTY_TEXT_NODE {L" "};

static IAccessible2* IAccessible2FromIdentifier(int docHandle, int ID) {
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
			const int headerCellDocHandle = HandleToUlong(hwnd);
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
	if (paccTableCell->get_rowColumnExtents(&row, &column, &rowExtents, &columnExtents, &isSelected) == S_OK) {
		s << row + 1;
		node->addAttribute(L"table-rownumber", s.str());
		s.str(L"");
		s << column + 1;
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

	fillTableHeaders(node, paccTableCell, &IAccessibleTableCell::get_columnHeaderCells, L"table-columnheadercells");
	fillTableHeaders(node, paccTableCell, &IAccessibleTableCell::get_rowHeaderCells, L"table-rowheadercells");
}

void GeckoVBufBackend_t::versionSpecificInit(IAccessible2* pacc) {
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
	if(toolkitName) {
		this->toolkitName = std::wstring(toolkitName, SysStringLen(toolkitName));
	}
	iaApp->Release();
	SysFreeString(toolkitName);
}

optional<int>
getIAccessible2UniqueID(IAccessible2* targetAcc) {
	int ID = 0;
	//Get ID -- IAccessible2 uniqueID
	if (targetAcc->get_uniqueID((long*)&ID) != S_OK) {
		LOG_DEBUG(L"pacc->get_uniqueID failed");
		return optional<int>();
	}
	return ID;
}

class LabelInfo {
public:
	bool isVisible;
	optional<int> ID;
};

using OptionalLabelInfo = optional< LabelInfo >;
OptionalLabelInfo GeckoVBufBackend_t::getLabelInfo(IAccessible2* pacc2) {
	CComQIPtr<IAccessible2_2> pacc2_2=pacc2;
	if (!pacc2_2) return OptionalLabelInfo();
	auto targetAcc = getRelationElement(IA2_RELATION_LABELLED_BY, pacc2_2);
	if(!targetAcc) return OptionalLabelInfo();
	CComVariant child;
	child.vt = VT_I4;
	child.lVal = 0;
	CComVariant state;
	HRESULT res = targetAcc->get_accState(child, &state);
	bool isVisible = res == S_OK && !(state.lVal & STATE_SYSTEM_INVISIBLE);
	auto ID = getIAccessible2UniqueID(targetAcc);
	return LabelInfo { isVisible, ID } ;
}

std::optional<int> GeckoVBufBackend_t::getRelationId(LPCOLESTR ia2TargetRelation, IAccessible2* pacc2) {
	CComQIPtr<IAccessible2_2> pacc2_2 = pacc2;
	if (pacc2_2 == nullptr) return std::optional<int>();
	auto targetAcc = getRelationElement(ia2TargetRelation, pacc2_2);
	if (targetAcc == nullptr) return std::optional<int>();
	auto ID = getIAccessible2UniqueID(targetAcc);
	return ID;
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

std::optional<wstring> getAccDescription(IAccessible2* pacc, VARIANT childID) {
	std::optional<wstring> desc;
	CComBSTR rawDesc;
	if (S_OK == pacc->get_accDescription(childID, &rawDesc)) {
		desc = rawDesc;
	}
	return desc;
}

/**
 * Get the selected item or the first item if no item is selected.
 */
CComPtr<IAccessible2> GeckoVBufBackend_t::getSelectedItem(
	IAccessible2* container, const map<wstring, wstring>& attribs
) {
	CComVariant selection;
	HRESULT hr = container->get_accSelection(&selection);
	if (FAILED(hr)) {
		LOG_DEBUGWARNING(L"accSelection failed with " << hr);
		return nullptr;
	}

	if (selection.vt == VT_DISPATCH) {
		// Single selected item, so just return it.
		return CComQIPtr<IAccessible2>(selection.pdispVal);
	}

	if (selection.vt == VT_UNKNOWN) {
		// One or more selected items in an IEnumVARIANT.
		auto enumVar = CComQIPtr<IEnumVARIANT>(selection.punkVal);
		if (!enumVar) {
			return nullptr;
		}
		// We only care about the first selected item.
		CComVariant items[1];
		if (FAILED(enumVar->Next(1, items, nullptr))) {
			return nullptr;
		}
		if (items[0].vt != VT_DISPATCH) {
			return nullptr;
		}
		return CComQIPtr<IAccessible2>(items[0].pdispVal);
	}

	// No selection, so return the first child.
	CComPtr<IDispatch> child;
	if (SUCCEEDED(container->get_accChild(CComVariant(1), &child))) {
		return CComQIPtr<IAccessible2>(child);
	}

	return nullptr;
}

/**
 * Get the text box inside a combo box, if any.
 */
CComPtr<IAccessible2> getTextBoxInComboBox(
	IAccessible2* comboBox
) {
	CComPtr<IDispatch> childDisp;
	// We only check the first child.
	if (FAILED(comboBox->get_accChild(CComVariant(1), &childDisp))) {
		return nullptr;
	}
	CComQIPtr<IAccessible2> child = childDisp;
	if (!child) {
		return nullptr;
	}
	long role;
	if (FAILED(child->role(&role))) {
		return nullptr;
	}
	if (role != ROLE_SYSTEM_TEXT) {
		return nullptr;
	}
	CComVariant state;
	if (FAILED(child->get_accState(CComVariant(CHILDID_SELF), &state))) {
		return nullptr;
	}
	if (state.vt != VT_I4 || !(state.lVal & STATE_SYSTEM_FOCUSABLE)) {
		return nullptr;
	}
	return child;
}

const vector<wstring>ATTRLIST_ROLES(1, L"IAccessible2::attribute_xml-roles");
const wregex REGEX_PRESENTATION_ROLE(L"IAccessible2\\\\:\\\\:attribute_xml-roles:.*\\bpresentation\\b.*;");

VBufStorage_fieldNode_t* GeckoVBufBackend_t::fillVBuf(
	IAccessible2* pacc,
	VBufStorage_buffer_t* buffer,
	VBufStorage_controlFieldNode_t* parentNode,
	VBufStorage_fieldNode_t* previousNode,
	IAccessibleTable2* paccTable2,
	long tableID,
	const wchar_t* parentPresentationalRowNumber,
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
	const int docHandle=HandleToUlong(docHwnd);
	if(!docHandle) {
		LOG_DEBUG(L"bad docHandle");
		return NULL;
	}
	//Get ID -- IAccessible2 uniqueID
	int ID;
	{
		auto opt_id = getIAccessible2UniqueID(pacc);
		if (!opt_id){
			return nullptr;
		}
		ID = opt_id.value();
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

	//get IA2Attributes -- IAccessible2 attributes;
	map<wstring,wstring>::const_iterator IA2AttribsMapIt;
	auto IA2AttribsMap = createMapOfIA2AttributesFromPacc(pacc);
	// Add all IA2 attributes on the node
	for(const auto& [key, val]: IA2AttribsMap) {
		wstring attribName = L"IAccessible2::attribute_";
		attribName += key;
		parentNode->addAttribute(attribName, val);
	}

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

	// Specifically force the role of ARIA treegrids from outline to table.
	// We do this very early on in the rendering so that all our table logic applies.
	if(role == ROLE_SYSTEM_OUTLINE) {
		if(hasXmlRoleAttribContainingValue(IA2AttribsMap, L"treegrid")) {
			role = ROLE_SYSTEM_TABLE;
		}
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
	// Remove state_editable from tables as Gecko exposes it for ARIA grids which is not in the ARIA spec. 
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

	//Check IA2Attributes, and or the role etc to work out if this object is a block element
	bool isBlockElement=TRUE;
	if(IA2States&IA2_STATE_MULTI_LINE) {
		// Multiline nodes should always be block.
		isBlockElement=TRUE;
	} else if((IA2AttribsMapIt=IA2AttribsMap.find(L"display"))!=IA2AttribsMap.end()) {
		// If there is a display attribute, we can rely solely on this to determine whether this is a block element or not.
		isBlockElement = IA2AttribsMapIt->second != L"inline"
			&& IA2AttribsMapIt->second != L"inline-block"
			&& IA2AttribsMapIt->second != L"inline-flex";
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

	std::optional<wstring> description{ getAccDescription(pacc, varChild) };
	if (description.has_value()) {
		parentNode->addAttribute(L"description", description.value());
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
	optional<LabelInfo> labelInfo_;
	// A version of the getIdForVisibleLabel function that caches its result
	auto isLabelVisibleCached = [&]() {
		if (!labelInfo_) {
			labelInfo_ = getLabelInfo(pacc);
		}
		bool isVisible = false;
		if (labelInfo_) {
			isVisible = labelInfo_->isVisible;
		}
		return isVisible;
	};
	auto getLabelIDCached = [&]() {
		if (!labelInfo_) {
			labelInfo_ = getLabelInfo(pacc);
		}
		optional<int> id;
		if (labelInfo_) {
			id = labelInfo_->ID;
		}
		return id;
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
	// Whether this is a selection container for which only the selected item should be rendered;
	// currently, list boxes and trees.
	bool renderSelectedItemOnly = false;
	if (isAriaHidden) {
		// aria-hidden
		isVisible = false;
	} else {
		// If a node has children, it's visible.
		isVisible = width > 0 && height > 0 || childCount > 0;
		// Only render the selected item for interactive lists.
		if (role == ROLE_SYSTEM_LIST && !(states & STATE_SYSTEM_READONLY)) {
			renderSelectedItemOnly = true;
		} else if(role == ROLE_SYSTEM_OUTLINE) {
			renderSelectedItemOnly = true;
		}
		if (IA2TextIsUnneededSpace
			|| role == ROLE_SYSTEM_COMBOBOX
			|| renderSelectedItemOnly
			|| isEmbeddedApp
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
	IAccessibleTableCell* paccTableCell = nullptr;
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
			// Note that we however do not want to set this on table rows as if this row alone is invalidated, none of the other row coordinates would be affected. 
			if(role!=ROLE_SYSTEM_ROW) {
				LOG_DEBUG(L"Setting node's requiresParentUpdate to true");
				parentNode->requiresParentUpdate=true;
			}
			// Setting alwaysRerenderChildren ensures that if this node is rerendered, none of its children are reused.
			// For example, if this is a table row that is rerendered (perhaps due to a previous table row being added),
			// this row's cells can't be reused because their coordinates would now be out of date.
			LOG_DEBUG(L"Setting node's alwaysRerenderChildren to true");
			parentNode->alwaysRerenderChildren=true;
		}
	}

	// For IAccessibleTable2, we can always obtain the cell interface,
	// which allows us to handle updates to table cells.
	if (paccTableCell) {
		this->fillTableCellInfo_IATable2(parentNode, paccTableCell);
		if (!paccTable2) {
			// This is an update; we're not rendering the entire table.
			tableID = getTableIDFromCell(paccTableCell);
		}
		paccTableCell->Release();
		paccTableCell = nullptr;
		// tableID is the IAccessible2::uniqueID for paccTable.
		s << tableID;
		parentNode->addAttribute(L"table-id", s.str());
		s.str(L"");
		// We're now within a cell, so descendant nodes shouldn't refer to this table anymore.
		paccTable2 = nullptr;
		tableID = 0;
	}
	// Handle table information.
	// Don't release the table unless it was created in this call.
	IAccessibleTable2* curNodePaccTable2 = nullptr;
	// If paccTable2 is not NULL, we're within a table but not yet within a cell, so don't bother to query for table info.
	if (!paccTable2) {
		// Try to get table information.
		pacc->QueryInterface(IID_IAccessibleTable2, (void**)&curNodePaccTable2);
		if (curNodePaccTable2) {
			// This is a table, so add its information as attributes.
			if((IA2AttribsMapIt = IA2AttribsMap.find(L"layout-guess")) != IA2AttribsMap.end()) {
				parentNode->addAttribute(L"table-layout",L"1");
			}
			tableID = ID;
			s << ID;
			parentNode->addAttribute(L"table-id", s.str());
			s.str(L"");
			// Fetch row and column counts and add them as attributes on the vbuf node.
			long rowCount = 0;
			if (curNodePaccTable2->get_nRows(&rowCount) == S_OK) {
				s << rowCount;
				parentNode->addAttribute(L"table-rowcount", s.str());
				s.str(L"");
			}
			long colCount = 0;
			if (curNodePaccTable2->get_nColumns(&colCount) == S_OK) {
				s << colCount;
				parentNode->addAttribute(L"table-columncount", s.str());
				s.str(L"");
			}
			if (rowCount > 0 || colCount > 0) {
				// This table has rows and columns.
				// Maintain curNodePaccTable2 for child rendering until any table cells are found.
				paccTable2 = curNodePaccTable2;
			}

			
			{ // Add the table summary if one is present and the table is visible.
				VBufStorage_fieldNode_t* summaryTempNode = nullptr;
				if (isVisible && description.has_value()) {
					tempNode = summaryTempNode = buffer->addTextFieldNode(parentNode, previousNode, description.value());
				}
				else if (
						// If there is no caption, the summary (if any) is the name.
						// There is no caption if the label isn't visible.
						name && !labelVisible
					) {
					tempNode = summaryTempNode = buffer->addTextFieldNode(parentNode, previousNode, name);
				}
				if (summaryTempNode != nullptr) {
					if (!locale.empty()) {
						summaryTempNode->addAttribute(L"language", locale);
					}
					previousNode = summaryTempNode;
				}
			}
		}
	}

	// Add some presentational table attributes
	// Note these are only for reporting, the physical table attributes (table-rownumber etc) for aiding in navigation etc are added  later on.
	// propagate table-rownumber-presentational down to the cell as Gecko only includes it on the row itself
	if(parentPresentationalRowNumber) {
		parentNode->addAttribute(L"table-rownumber-presentational",parentPresentationalRowNumber);
	}
	const wchar_t* presentationalRowNumber=NULL;
	IA2AttribsMapIt = IA2AttribsMap.find(L"rowindex");
	if(IA2AttribsMapIt != IA2AttribsMap.end()) {
		parentNode->addAttribute(L"table-rownumber-presentational",IA2AttribsMapIt->second);
		presentationalRowNumber=IA2AttribsMapIt->second.c_str();
	}
	IA2AttribsMapIt = IA2AttribsMap.find(L"colindex");
	if(IA2AttribsMapIt != IA2AttribsMap.end()) {
		parentNode->addAttribute(L"table-columnnumber-presentational",IA2AttribsMapIt->second);
	}
	IA2AttribsMapIt = IA2AttribsMap.find(L"rowcount");
	if(IA2AttribsMapIt != IA2AttribsMap.end()) {
		parentNode->addAttribute(L"table-rowcount-presentational",IA2AttribsMapIt->second);
	}
	IA2AttribsMapIt = IA2AttribsMap.find(L"colcount");
	if(IA2AttribsMapIt != IA2AttribsMap.end()) {
		parentNode->addAttribute(L"table-columncount-presentational",IA2AttribsMapIt->second);
	}

	BSTR value=NULL;
	if(pacc->get_accValue(varChild,&value)==S_OK) {
		if(value&&SysStringLen(value)==0) {
			SysFreeString(value);
			value=NULL;
		}
	}

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
					CComPtr<IAccessibleHyperlink> link = linkGetter->next();
					CComQIPtr<IAccessible2> childPacc = link;
					if(!childPacc) {
						continue;
					}
					tempNode = this->fillVBuf(
						childPacc,
						buffer,
						parentNode,
						previousNode,
						paccTable2,
						tableID,
						presentationalRowNumber,
						ignoreInteractiveUnlabelledGraphics
					);
					if (tempNode) {
						previousNode=tempNode;
					} else {
						LOG_DEBUG(L"Error in fillVBuf");
					}
				}
			}

		} else if (renderChildren && childCount > 0) {
			// The object has no text, but we do want to render its children.
			auto [varChildren, accChildRes] = getAccessibleChildren(pacc, 0, childCount);
			if (S_OK != accChildRes || varChildren.size() == 0) {
				std::wstringstream msg;
				msg << L"AccessibleChildren failed (count: " << childCount << L"), res: " << accChildRes;
				switch (accChildRes) {
				case E_NOINTERFACE:
					msg << L" (E_NOINTERFACE, No such interface supported)";
					LOG_ERROR(msg.str());  // Indicates a bug in the IA2 provider.
					break;
				case RPC_E_DISCONNECTED:
					msg << L" (RPC_E_DISCONNECTED, object invoked has disconnected from its clients.)";
					// RPC_E_DISCONNECTED indicates that the parent died since the query to accChildCount.
					LOG_DEBUG(msg.str());  // This is expected to occur in dynamic content.
					break;
				case CO_E_OBJNOTCONNECTED:
					msg << L" (CO_E_OBJNOTCONNECTED, Object is not connected to server)";
					LOG_DEBUG(msg.str());
					break;
				case S_FALSE:  // Success, but unexpeced number of children were returned.
					msg << L" (S_FALSE, expected childcount, got "
						<< varChildren.size()
						<< L". Children may have been removed from document.)";
					// Returning no children indicates that all children died since the call to accChildCount.
					// Even if the children had been rendered, they were removed immediately thereafter.
					LOG_DEBUG(msg.str());  // This is expected to occur in dynamic content.
					break;
				default:
					// Other unknown failures, log at error.
					LOG_ERROR(msg.str());
				}
			}
			LOG_DEBUG(L"got " << varChildren.size() << L" children");

			for(CComVariant& child : varChildren) {
				if (child.vt != VT_DISPATCH || !child.pdispVal) {
					child.Clear();
					continue;
				}
				CComQIPtr< IAccessible2, &IID_IAccessible2> childPacc(child.pdispVal);
				if (!childPacc) {
					child.Clear();
					continue;
				}
				tempNode = this->fillVBuf(
					childPacc,
					buffer,
					parentNode,
					previousNode,
					paccTable2,
					tableID,
					presentationalRowNumber,
					ignoreInteractiveUnlabelledGraphics
				);
				if (tempNode) {
					previousNode = tempNode;
				}
				else
					LOG_DEBUG(L"Error in calling fillVBuf");
				child.Clear();
			}
		} else if (renderSelectedItemOnly) {
			CComPtr<IAccessible2> item = this->getSelectedItem(pacc, IA2AttribsMap);
			if (item) {
				tempNode = this->fillVBuf(
					item,
					buffer,
					parentNode,
					previousNode,
					paccTable2,
					tableID,
					presentationalRowNumber,
					ignoreInteractiveUnlabelledGraphics
				);
				if (tempNode) {
					previousNode=tempNode;
					// The container itself might not always fire selection events.
					// Therefore, we rely on a stateChange event on the item (since
					// these fire for both selection and unselection) and have the item
					// re-render its parent.
					static_cast<VBufStorage_controlFieldNode_t*>(tempNode)->requiresParentUpdate = true;
				} else {
					LOG_DEBUG(L"Error in calling fillVBuf");
				}
			}

		} else if (role == ROLE_SYSTEM_COMBOBOX) {
			CComPtr<IAccessible2> textBox = getTextBoxInComboBox(pacc);
			if (textBox) {
				// ARIA 1.1 combobox. Render the text box child.
				tempNode = this->fillVBuf(
					textBox,
					buffer,
					parentNode,
					previousNode,
					paccTable2,
					tableID,
					presentationalRowNumber,
					ignoreInteractiveUnlabelledGraphics
				);
				if (tempNode) {
					previousNode=tempNode;
				} else {
					LOG_DEBUG(L"Error in calling fillVBuf");
				}
			} else if (value) {
				previousNode=buffer->addTextFieldNode(parentNode,previousNode,value);
				if(previousNode && !locale.empty()) {
					previousNode->addAttribute(L"language", locale);
				}
			}
		} else if(role == ROLE_SYSTEM_GRAPHIC) {
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
		} else if (role == ROLE_SYSTEM_PROGRESSBAR && states & STATE_SYSTEM_INDETERMINATE){
			// ROLE_SYSTEM_PROGRESSBAR with STATE_SYSTEM_INDETERMINATE is an
			// indeterminate progress bar (maps to NVDA Role BUSY_INDICATOR).
			// Value is meaningless (always zero), don't use it as the text node, use space instead.
			previousNode=buffer->addTextFieldNode(parentNode,previousNode, EMPTY_TEXT_NODE);
			if (previousNode && !locale.empty()) {
				previousNode->addAttribute(L"language", locale);
			}
		} else if (!nameIsContent && value) {
			previousNode = buffer->addTextFieldNode(parentNode, previousNode, value);
			if (previousNode && !locale.empty()) {
				previousNode->addAttribute(L"language", locale);
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
			previousNode = buffer->addTextFieldNode( parentNode, previousNode, EMPTY_TEXT_NODE);
			if(previousNode&&!locale.empty()) previousNode->addAttribute(L"language",locale);
			parentNode->isBlock=false;
		}

		if ((isInteractive || role == ROLE_SYSTEM_SEPARATOR) && parentNode->getLength() == 0) {
			// If the node is interactive or otherwise relevant even when empty
			// and it still has no content, render a space so the user can access the node.
			previousNode = buffer->addTextFieldNode(parentNode, previousNode, EMPTY_TEXT_NODE);
			if(previousNode&&!locale.empty()) previousNode->addAttribute(L"language",locale);
		}
	}

	//If the name isn't being rendered as the content, then add the name as a field attribute.
	if (!nameIsContent && name) {
		parentNode->addAttribute(L"name", name);
		// Determine whether this node is labelled by its content. We only need to do
		// this if the node has a name and the name is explicit, since this is what
		// browsers expose in this case.
		if (nameIsExplicit) {
			auto labelId = getLabelIDCached();
			if (labelId) {
				auto labelControlFieldNode = buffer->getControlFieldNodeWithIdentifier(docHandle, labelId.value());
				if (labelControlFieldNode) {
					bool isDescendant = buffer->isDescendantNode(parentNode, labelControlFieldNode);
					if (isDescendant) {
						parentNode->addAttribute(L"labelledByContent", L"true");
					}
				}
			}
		}
	}

	//If the description matches the content, notify NVDA to prevent duplicate reporting
	const bool descriptionIsContent = (
		description.has_value()
		&& nodeContentMatchesString(parentNode, description.value())
	);
	if (descriptionIsContent){
		parentNode->addAttribute(L"descriptionIsContent", L"true");
	}


	/* Set the details summary by checking for both IA2_RELATION_DETAILS and IA2_RELATION_DETAILS_FOR as one
	of the nodes in the relationship will not be in the buffer yet */
	std::optional<int> detailsId = getRelationId(IA2_RELATION_DETAILS, pacc);
	if (detailsId) {
		parentNode->addAttribute(L"hasDetails", L"true");
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
	if (curNodePaccTable2) {
		curNodePaccTable2->Release();
		curNodePaccTable2 = nullptr;
	}
	return parentNode;
}

void CALLBACK GeckoVBufBackend_t::renderThread_winEventProcHook(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time) {
	switch(eventID) {
		case EVENT_OBJECT_FOCUS:
		case IA2_EVENT_DOCUMENT_LOAD_COMPLETE:
		case EVENT_SYSTEM_ALERT:
		case IA2_EVENT_TEXT_UPDATED:
		case IA2_EVENT_TEXT_INSERTED:
		case IA2_EVENT_TEXT_REMOVED:
		case EVENT_OBJECT_REORDER:
		case EVENT_OBJECT_NAMECHANGE:
		case EVENT_OBJECT_VALUECHANGE:
		case EVENT_OBJECT_DESCRIPTIONCHANGE:
		case EVENT_OBJECT_STATECHANGE:
		case EVENT_OBJECT_SELECTIONADD:
		case EVENT_OBJECT_SELECTIONREMOVE:
		case EVENT_OBJECT_SELECTIONWITHIN:
		case IA2_EVENT_OBJECT_ATTRIBUTE_CHANGED:
		case IA2_EVENT_TEXT_ATTRIBUTE_CHANGED:
		case EVENT_OBJECT_HIDE:
		break;
		default:
		return;
	}
	if(childID>=0||objectID!=OBJID_CLIENT)
		return;
	LOG_DEBUG(L"winEvent for window "<<hwnd);
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

		//For focus, documentLoadComplete and alert events, force any nodes already marked as invalid  to be updated right now,
		if(
			eventID == EVENT_OBJECT_FOCUS
			|| eventID == IA2_EVENT_DOCUMENT_LOAD_COMPLETE
			|| eventID==EVENT_SYSTEM_ALERT
		) {
			backend->forceUpdate();
			continue;
		}

		//Ignore state change events on the root node (document) as it can cause rerendering when the document goes busy
		if(eventID==EVENT_OBJECT_STATECHANGE&&hwnd==(HWND)UlongToHandle(backend->rootDocHandle)&&childID==backend->rootID)
			return;

		VBufStorage_controlFieldNode_t* node=backend->getControlFieldNodeWithIdentifier(docHandle,ID);
		if(!node)
			continue;
		if (eventID == EVENT_OBJECT_HIDE) {
			// When an accessible is moved, events are fired as if the accessible were
			// removed and then inserted. The insertion events are fired as if it were
			// a new subtree; i.e. only one insertion for the root of the subtree.
			// This means that if new descendants are inserted at the same time as the
			// root is moved, we don't get specific events for those insertions.
			// Because of that, we mustn't reuse the subtree. Otherwise, we wouldn't
			// walk inside it and thus wouldn't know about the new descendants.
			node->alwaysRerenderDescendants = true;
			// We'll get a text removed event for the parent, so no need to invalidate
			// this node.
			continue;
		}
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
	if(!this->fillVBuf(pacc, buffer, nullptr, nullptr)) {
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

VBufBackend_t* GeckoVBufBackend_t_createInstance(int docHandle, int ID) {
	VBufBackend_t* backend=new GeckoVBufBackend_t(docHandle,ID);
	return backend;
}
