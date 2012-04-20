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

#include <windows.h>
#include <set>
#include <string>
#include <sstream>
#include <ia2.h>
#include <common/ia2utils.h>
#include <remote/nvdaHelperRemote.h>
#include <vbufBase/backend.h>
#include <common/log.h>
#include <vbufBase/utils.h>
#include "gecko_ia2.h"

using namespace std;

#define IGNORE_NONINTERACTIVE_UNLABELED_GRAPHICS 1
#define IGNORE_UNNEEDED_GRAPHICS_IN_LINKS 1

#define NAVRELATION_NODE_CHILD_OF 0x1005

HWND findRealMozillaWindow(HWND hwnd) {
	LOG_DEBUG(L"Finding real window for window "<<hwnd);
	if(hwnd==0||!IsWindow(hwnd)) {
		LOG_DEBUG(L"Invalid window");
		return (HWND)0;
	}
	wchar_t className[256];
	bool foundWindow=false;
	HWND tempWindow=hwnd;
	do {
		if(GetClassName(tempWindow,className,256)==0) {
			LOG_DEBUG(L"Could not get class name for window "<<hwnd);
			return hwnd;
		}
		LOG_DEBUG(L"class name for window "<<tempWindow<<L" is "<<className);
		if(wcscmp(L"MozillaWindowClass",className)!=0) {
			foundWindow=true;
		} else {
			tempWindow=GetAncestor(tempWindow,GA_PARENT);
		}
	} while(tempWindow&&!foundWindow);
	if(GetClassName(tempWindow,className,256)!=0&&wcsstr(className,L"Mozilla")==className) { 
		hwnd=tempWindow;
	}
	LOG_DEBUG(L"Found window "<<hwnd);
	return hwnd;
}

IAccessible2* IAccessible2FromIdentifier(int docHandle, int ID) {
	int res;
	IAccessible* pacc=NULL;
	IServiceProvider* pserv=NULL;
	IAccessible2* pacc2=NULL;
	VARIANT varChild;
	LOG_DEBUG(L"calling AccessibleObjectFromEvent");
	if((res=AccessibleObjectFromEvent((HWND)docHandle,OBJID_CLIENT,ID,&pacc,&varChild))!=S_OK) {
		LOG_DEBUG(L"AccessibleObjectFromEvent returned "<<res);
		return NULL;
	}
	LOG_DEBUG(L"got IAccessible at "<<pacc);
	VariantClear(&varChild);
	LOG_DEBUG(L"calling IAccessible::QueryInterface with IID_IServiceProvider");
	if((res=pacc->QueryInterface(IID_IServiceProvider,(void**)(&pserv)))!=S_OK) {
		LOG_DEBUG(L"IAccessible::QueryInterface returned "<<res);
		pacc->Release();
		return NULL;
	}  
	LOG_DEBUG(L"IServiceProvider at "<<pserv);
	LOG_DEBUG(L"releasing IAccessible");
	pacc->Release();
	LOG_DEBUG(L"calling IServiceProvider::QueryService with IID_IAccessible2");
	if((res=pserv->QueryService(IID_IAccessible,IID_IAccessible2,(void**)(&pacc2)))!=S_OK) {
		LOG_DEBUG(L"IServiceProvider::QueryService returned "<<res);
		pacc2=NULL;
	}  else {
		LOG_DEBUG(L"IAccessible2 at "<<pacc2);
	}
	LOG_DEBUG(L"releasingIServiceProvider");
	pserv->Release();
	return pacc2;
}

template<typename TableType> inline void fillTableCounts(VBufStorage_controlFieldNode_t* node, IAccessible2* pacc, TableType* paccTable) {
	int res;
	wostringstream s;
	long count = 0;
	LOG_DEBUG(L"Getting row count");
	if ((res = paccTable->get_nRows(&count)) == S_OK) {
		LOG_DEBUG(L"row count is " << count);
		s << count;
		node->addAttribute(L"table-rowcount", s.str());
		s.str(L"");
	} else
		LOG_DEBUG(L"IAccessibleTable*::get_nRows failed, result " << res);
	if ((res = paccTable->get_nColumns(&count)) == S_OK) {
		LOG_DEBUG(L"column count is " << count);
		s << count;
		node->addAttribute(L"table-columncount", s.str());
	} else
		LOG_DEBUG(L"IAccessibleTable*::get_nColumns failed, result " << res);
}

inline void fillTableCellInfo_IATable(VBufStorage_controlFieldNode_t* node, IAccessibleTable* paccTable, const wstring& cellIndexStr) {
	int res;
	wostringstream s;
	long cellIndex = _wtoi(cellIndexStr.c_str());
	long row, column, rowExtents, columnExtents;
	boolean isSelected;
	if ((res = paccTable->get_rowColumnExtentsAtIndex(cellIndex, &row, &column, &rowExtents, &columnExtents, &isSelected)) == S_OK) {
		LOG_DEBUG(L"IAccessibleTable::get_rowColumnExtentsAtIndex succeeded, adding attributes");
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
	} else
		LOG_DEBUG(L"IAccessibleTable::get_rowColumnExtentsAtIndex failed, result " << res);
}

typedef HRESULT(STDMETHODCALLTYPE IAccessibleTableCell::*IATableCellGetHeaderCellsFunc)(IUnknown***, long*);
inline void fillTableHeaders(VBufStorage_controlFieldNode_t* node, IAccessibleTableCell* paccTableCell, const IATableCellGetHeaderCellsFunc getHeaderCells, const wstring& attribName) {
	int res;
	wostringstream s;
	IUnknown** headerCells;
	long nHeaderCells;
	IAccessible2* headerCellPacc = NULL;
	int headerCellDocHandle, headerCellID;

	if ((paccTableCell->*getHeaderCells)(&headerCells, &nHeaderCells) == S_OK) {
		LOG_DEBUG(L"Get header cells succeeded, adding header IDs");
		for (int hci = 0; hci < nHeaderCells; hci++) {
			if ((res = headerCells[hci]->QueryInterface(IID_IAccessible2, (void**)(&headerCellPacc))) != S_OK) {
				LOG_DEBUG(L"QueryInterface header cell " << hci << " to IAccessible2 failed with " << res);
				headerCells[hci]->Release();
				continue;
			}
			headerCells[hci]->Release();
			if ((res = headerCellPacc->get_windowHandle((HWND*)&headerCellDocHandle)) != S_OK) {
				LOG_DEBUG("IAccessible2::get_windowHandle on header cell " << hci << " failed with " << res);
				headerCellPacc->Release();
				continue;
			}
			headerCellDocHandle = (int)findRealMozillaWindow((HWND)headerCellDocHandle);
			if ((res = headerCellPacc->get_uniqueID((long*)&headerCellID)) != S_OK) {
				LOG_DEBUG("IAccessible2::get_uniqueID on header cell " << hci << " failed with " << res);
				headerCellPacc->Release();
				continue;
			}
			s << headerCellDocHandle << L"," << headerCellID << L";";
			headerCellPacc->Release();
		}
		if (!s.str().empty())
			node->addAttribute(attribName, s.str());
	}
}

inline void GeckoVBufBackend_t::fillTableCellInfo_IATable2(VBufStorage_controlFieldNode_t* node, IAccessibleTableCell* paccTableCell) {
	wostringstream s;

	long row, column, rowExtents, columnExtents;
	boolean isSelected;
	if (paccTableCell->get_rowColumnExtents(&row, &column, &rowExtents, &columnExtents, &isSelected) == S_OK) {
		LOG_DEBUG(L"IAccessibleTableCell::get_rowColumnExtents succeeded, adding attributes");
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
	serv = NULL;

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

VBufStorage_fieldNode_t* GeckoVBufBackend_t::fillVBuf(IAccessible2* pacc, VBufStorage_buffer_t* buffer, VBufStorage_controlFieldNode_t* parentNode, VBufStorage_fieldNode_t* previousNode, IAccessibleTable* paccTable, IAccessibleTable2* paccTable2, long tableID) {
	int res;
	LOG_DEBUG(L"Entered fillVBuf, with pacc at "<<pacc<<L", parentNode at "<<parentNode<<L", previousNode "<<previousNode);
	nhAssert(buffer); //buffer can't be NULL
	nhAssert(!parentNode||buffer->isNodeInBuffer(parentNode)); //parent node must be in buffer
	nhAssert(!previousNode||buffer->isNodeInBuffer(previousNode)); //Previous node must be in buffer
	VBufStorage_fieldNode_t* tempNode;
	bool isBlockElement=TRUE;
	//all IAccessible methods take a variant for childID, get one ready
	VARIANT varChild;
	varChild.vt=VT_I4;
	long left=0, top=0, width=0, height=0;
	varChild.lVal=0;
	if((res=pacc->accLocation(&left,&top,&width,&height,varChild))!=S_OK) {
		LOG_DEBUG(L"Error getting accLocation");
	}
	//get docHandle -- IAccessible2 windowHandle
	LOG_DEBUG(L"get docHandle with IAccessible2::get_windowHandle");
	int docHandle;
	if((res=pacc->get_windowHandle((HWND*)(&docHandle)))!=S_OK) {
		LOG_DEBUG(L"pacc->get_windowHandle returned "<<res);
		docHandle=0;
		return NULL;
	}
	docHandle=(int)findRealMozillaWindow((HWND)docHandle);
	if(docHandle==0) {
		LOG_DEBUG(L"bad docHandle");
		return NULL;
	}
	LOG_DEBUG(L"docHandle is "<<docHandle);
	//Get ID -- IAccessible2 uniqueID
	LOG_DEBUG(L"get ID with IAccessible2::get_uniqueID");
	int ID;
	if((res=pacc->get_uniqueID((long*)(&ID)))!=S_OK) {
		LOG_DEBUG(L"pacc->get_uniqueID returned "<<res);
		ID=0;
		return NULL;
	}
	LOG_DEBUG(L"ID is "<<ID);
	//Make sure that we don't already know about this object -- protect from loops
	if(buffer->getControlFieldNodeWithIdentifier(docHandle,ID)!=NULL) {
		LOG_DEBUG(L"a node with this docHandle and ID already exists, returning NULL");
		return NULL;
	}
	//Add this node to the buffer
	LOG_DEBUG(L"Adding Node to buffer");
	parentNode=buffer->addControlFieldNode(parentNode,previousNode,docHandle,ID,TRUE);
	nhAssert(parentNode); //new node must have been created
	previousNode=NULL;
	LOG_DEBUG(L"Added  node at "<<parentNode);
	//Get role -- IAccessible2 role
	LOG_DEBUG(L"get role with IAccessible2::role");
	long role=0;
	BSTR roleString=NULL;
	if((res=pacc->role(&role))!=S_OK) {
		LOG_DEBUG(L"pacc->get_role returned "<<res);
		role=IA2_ROLE_UNKNOWN;
	}
	VARIANT varRole;
	VariantInit(&varRole);
	if(role==0) {
		if((res=pacc->get_accRole(varChild,&varRole))!=S_OK) {
			LOG_DEBUG(L"accRole returned code "<<res);
		}
		if(varRole.vt==VT_I4) {
			role=varRole.lVal;
			LOG_DEBUG(L"Got role of "<<role);
		} else if(varRole.vt==VT_BSTR) {
			roleString=varRole.bstrVal;
			LOG_DEBUG(L"Got role string of "<<roleString);
		}
	} else {
		LOG_DEBUG(L"role is "<<role);
	}
	//Add role as an attrib
	{
		wostringstream s;
		if(roleString!=NULL) {
			s<<roleString;
		} else {
			s<<role;
		}
		parentNode->addAttribute(L"IAccessible::role",s.str().c_str());
	}
	VariantClear(&varRole);
	//get states -- IAccessible accState
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
	//get IA2States -- IAccessible2 states
	LOG_DEBUG(L"get IA2States with IAccessible2::get_states");
	int IA2States;
	if((res=pacc->get_states((AccessibleStates*)(&IA2States)))!=S_OK) {
		LOG_DEBUG(L"pacc->get_states returned "<<res);
		IA2States=0;
	}
	LOG_DEBUG(L"IA2States is "<<IA2States);
	//Add each state that is on, as an attrib
	for(int i=0;i<32;++i) {
		int state=1<<i;
		if(state&IA2States) {
			wostringstream nameStream;
			nameStream<<L"IAccessible2::state_"<<state;
			parentNode->addAttribute(nameStream.str().c_str(),L"1");
		}
	}
	//get keyboardShortcut -- IAccessible accKeyboardShortcut;
	LOG_DEBUG(L"get keyboardShortcut with IAccessible::get_accKeyboardShortcut");
	BSTR keyboardShortcut;
	varChild.lVal=0;
	if((res=pacc->get_accKeyboardShortcut(varChild,&keyboardShortcut))!=S_OK) {
		LOG_DEBUG(L"pacc->get_accKeyboardShortcut returned "<<res);
		keyboardShortcut=NULL;
	}
	if(keyboardShortcut!=NULL) {
		LOG_DEBUG(L"keyboardShortcut is "<<keyboardShortcut);
	} else {
		LOG_DEBUG(L"keyboardShortcut is NULL");
	}
	//Add keyboardShortcut as an attrib
	if(keyboardShortcut!=NULL) {
		parentNode->addAttribute(L"keyboardShortcut",keyboardShortcut);
		//Free keyboardShortcut string memory
		SysFreeString(keyboardShortcut);
	} else {
		parentNode->addAttribute(L"keyboardShortcut",L"");
	}
	//get IA2Attributes -- IAccessible2 attributes;
	LOG_DEBUG(L"get IA2Attributes with IAccessible2::get_attributes");
	BSTR IA2Attributes;
	if((res=pacc->get_attributes(&IA2Attributes))!=S_OK) {
		LOG_DEBUG(L"pacc->get_attributes returned "<<res);
		IA2Attributes=NULL;
	}
	map<wstring,wstring> IA2AttribsMap;
	if(IA2Attributes!=NULL) {
		LOG_DEBUG(L"IA2Attributes is "<<IA2Attributes);
		IA2AttribsToMap(IA2Attributes,IA2AttribsMap);
	} else {
		LOG_DEBUG(L"IA2Attributes is NULL");
	}
	if(IA2Attributes!=NULL) {
		// Add each IA2 attribute as an attrib.
		for(map<wstring,wstring>::const_iterator it=IA2AttribsMap.begin();it!=IA2AttribsMap.end();++it) {
			wostringstream nameStream;
			nameStream<<L"IAccessible2::attribute_"<<it->first;
			parentNode->addAttribute(nameStream.str().c_str(),it->second.c_str());
		}
	} else {
		parentNode->addAttribute(L"IAccessible2::attributes",L"");
	}
	LOG_DEBUG(L"getting accDefaultAction");
	BSTR defaction=NULL;
	if((res=pacc->get_accDefaultAction(varChild,&defaction))!=S_OK) {
		LOG_DEBUG(L"IAccessible::get_accDefaultAction returned "<<res);
		defaction=NULL;
	}
	if(defaction!=NULL&&SysStringLen(defaction)==0) {
		SysFreeString(defaction);
		defaction=NULL;
	}
	if(defaction!=NULL) {
		parentNode->addAttribute(L"defaultAction",defaction);
	}
	{
		//Check IA2Attributes, and or the role etc to work out if this object is a block element
		LOG_DEBUG(L"Is this object a block element?");
		map<wstring,wstring>::const_iterator it;
		if(IA2States&IA2_STATE_MULTI_LINE) {
			// Multiline nodes should always be block.
			isBlockElement=TRUE;
		} else if((it=IA2AttribsMap.find(L"display"))!=IA2AttribsMap.end()) {
			// If there is a display attribute, we can rely solely on this to determine whether this is a block element or not.
			LOG_DEBUG(L"IA2Attributes contains display, value "<<it->second);
			isBlockElement=(it->second!=L"inline"&&it->second!=L"inline-block");
		} else if((it=IA2AttribsMap.find(L"formatting"))!=IA2AttribsMap.end()&&it->second==L"block") {
			LOG_DEBUG(L"IA2Attributes contains formatting:block, this is a block element");
			isBlockElement=TRUE;
		} else if(role==ROLE_SYSTEM_TABLE||role==ROLE_SYSTEM_CELL||role==IA2_ROLE_SECTION||role==ROLE_SYSTEM_DOCUMENT||role==IA2_ROLE_INTERNAL_FRAME||role==IA2_ROLE_UNKNOWN||role==ROLE_SYSTEM_SEPARATOR) {
			LOG_DEBUG(L"role is a known block element role so we should treet this object as a block element");
			isBlockElement=TRUE;
		} else {
			LOG_DEBUG(L"This object is not a block element");
			isBlockElement=FALSE;
		}
	}
	parentNode->setIsBlock(isBlockElement);
	LOG_DEBUG(L"getting accName");
	BSTR name=NULL;
	if((res=pacc->get_accName(varChild,&name))!=S_OK) {
		LOG_DEBUG(L"IAccessible::get_accName returned "<<res);
		name=NULL;
	}
	LOG_DEBUG(L"getting accDescription");
	BSTR description=NULL;
	if((res=pacc->get_accDescription(varChild,&description))==S_OK) {
		if(this->hasEncodedAccDescription) {
			if(wcsncmp(description,L"Description: ",13)==0)
				parentNode->addAttribute(L"description",&description[13]);
		} else
			parentNode->addAttribute(L"description",description);
		SysFreeString(description);
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
	// Handle table cell information.
	IAccessibleTableCell* paccTableCell = NULL;
	map<wstring,wstring>::const_iterator IA2AttribsMapIt;
	// If paccTable is not NULL, it is the table interface for the table above this object.
	if ((paccTable2 || paccTable) && (
		(res = pacc->QueryInterface(IID_IAccessibleTableCell, (void**)(&paccTableCell))) == S_OK || // IAccessibleTable2
		(IA2AttribsMapIt = IA2AttribsMap.find(L"table-cell-index")) != IA2AttribsMap.end() // IAccessibleTable
	)) {
		wostringstream s;
		// tableID is the IAccessible2::uniqueID for paccTable.
		s << tableID;
		parentNode->addAttribute(L"table-id", s.str());
		if (res == S_OK) {
			// IAccessibleTable2
			this->fillTableCellInfo_IATable2(parentNode, paccTableCell);
			paccTableCell->Release();
			paccTableCell = NULL;
		} else // IAccessibleTable
			fillTableCellInfo_IATable(parentNode, paccTable, IA2AttribsMapIt->second);
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
		LOG_DEBUG(L"paccTable is NULL, trying to get table information");
		if((res=pacc->QueryInterface(IID_IAccessibleTable2,(void**)(&paccTable2)))!=S_OK&&res!=E_NOINTERFACE) {
			LOG_DEBUG(L"pacc->QueryInterface, with IID_IAccessibleTable2, returned "<<res);
			paccTable2=NULL;
		}
		if(!paccTable2&&(res=pacc->QueryInterface(IID_IAccessibleTable,(void**)(&paccTable)))!=S_OK&&res!=E_NOINTERFACE) {
			LOG_DEBUG(L"pacc->QueryInterface, with IID_IAccessibleTable, returned "<<res);
			paccTable=NULL;
		}
		LOG_DEBUG(L"paccTable2 is "<<paccTable2<<", paccTable is "<<paccTable);
		if (paccTable2||paccTable) {
			// We did the QueryInterface for paccTable, so we must release it after all calls that use it are done.
			releaseTable = true;
			// This is a table, so add its information as attributes.
			if((IA2AttribsMapIt = IA2AttribsMap.find(L"layout-guess")) != IA2AttribsMap.end()) {
				LOG_DEBUG(L"Found a layout table, setting table-layout attrib");
				parentNode->addAttribute(L"table-layout",L"1");
			}
			wostringstream s;
			tableID = ID;
			s << ID;
			parentNode->addAttribute(L"table-id", s.str());
			s.str(L"");
			if(paccTable2)
				fillTableCounts<IAccessibleTable2>(parentNode, pacc, paccTable2);
			else
				fillTableCounts<IAccessibleTable>(parentNode, pacc, paccTable);
			// Add the table summary if one is present and the table is visible.
			if (name && width > 0 && height > 0 && (tempNode = buffer->addTextFieldNode(parentNode, previousNode, name))) {
				if(!locale.empty()) tempNode->addAttribute(L"language",locale);
				previousNode = tempNode;
			}
		}
	}
	IAccessibleText* paccText=NULL;
	IAccessibleHypertext* paccHypertext=NULL;
	//get IAccessibleText interface
	LOG_DEBUG(L"get paccText with IAccessible2::QueryInterface and IID_IAccessibleText");
	 if((res=pacc->QueryInterface(IID_IAccessibleText,(void**)(&paccText)))!=S_OK&&res!=E_NOINTERFACE) {
		LOG_DEBUG(L"pacc->QueryInterface, with IID_IAccessibleText, returned "<<res);
		paccText=NULL;
	}
	LOG_DEBUG(L"paccText is "<<paccText);
	//Get IAccessibleHypertext interface
	LOG_DEBUG(L"get paccHypertext with IAccessible2::QueryInterface and IID_IAccessibleHypertext");
	 if((res=pacc->QueryInterface(IID_IAccessibleHypertext,(void**)(&paccHypertext)))!=S_OK&&res!=E_NOINTERFACE) {
		LOG_DEBUG(L"pacc->QueryInterface, with IID_IAccessibleHypertext, returned "<<res);
		paccHypertext=NULL;
	}
	LOG_DEBUG(L"paccHypertext is "<<paccHypertext);
	//Get the text from the IAccessibleText interface
	LOG_DEBUG(L"LGet IA2Text with IAccessibleText::text");
	BSTR IA2Text=NULL;
	if(paccText&&(res=paccText->get_text(0,-1,&IA2Text))!=S_OK) {
		LOG_DEBUG(L"paccText->text, from 0 to -1 (end), returned "<<res);
		IA2Text=NULL;
	}
	if(IA2Text!=NULL) {
		LOG_DEBUG(L"got IA2Text");
	} else {
		LOG_DEBUG(L"IA2Text is NULL");
	}
	//Get the text length
	LOG_DEBUG(L"get IA2TextLength with SysStringLen");
	int IA2TextLength=0;
	if(IA2Text!=NULL) {
		IA2TextLength=SysStringLen(IA2Text);
	}
	LOG_DEBUG(L"IA2TextLength is "<<IA2TextLength);
	int IA2TextIsUnneededSpace=1;
	if(IA2TextLength>0&&(role!=ROLE_SYSTEM_TEXT||(states&STATE_SYSTEM_READONLY))&&!(IA2States&IA2_STATE_EDITABLE)) {
		for(int i=0;i<IA2TextLength;++i) {
			if(IA2Text[i]==L'\n'||IA2Text[i]==L'\xfffc'||!iswspace(IA2Text[i])) {
				LOG_DEBUG(L"IA2Text is not whitespace");
				IA2TextIsUnneededSpace=0;
				break;
			}
		}
		if(IA2TextIsUnneededSpace) {
			LOG_DEBUG(L"IA2Text is whitespace");
		}
	} else {
		IA2TextIsUnneededSpace=0;
	}
	LOG_DEBUG(L"getting accValue");
	BSTR value=NULL;
	if((res=pacc->get_accValue(varChild,&value))!=S_OK) {
		LOG_DEBUG(L"IAccessible::get_accValue returned "<<res);
		value=NULL;
	}
	if(value!=NULL&&SysStringLen(value)==0) {
		SysFreeString(value);
		value=NULL;
	}
	//Get the child count
	int childCount=0;
	if(IA2TextIsUnneededSpace||role==ROLE_SYSTEM_COMBOBOX||(role==ROLE_SYSTEM_LIST&&!(states&STATE_SYSTEM_READONLY))||role==IA2_ROLE_EMBEDDED_OBJECT) {
		LOG_DEBUG(L"Forcing childCount to 0 as we don't want this node's children");
		childCount=0;
	} else {
		LOG_DEBUG(L"get childCount with IAccessible::get_accChildCount");
		if((res=pacc->get_accChildCount((long*)(&childCount)))!=S_OK) {
		LOG_DEBUG(L"pacc->get_accChildCount returned "<<res);
			childCount=0;
		}
		LOG_DEBUG(L"childCount is "<<childCount);
	}
	//If this isn't a button or a graphic, then add the name as a field attribute
	if(role!=ROLE_SYSTEM_LINK&&role!=ROLE_SYSTEM_PUSHBUTTON&&role!=ROLE_SYSTEM_GRAPHIC&&name!=NULL) {
		parentNode->addAttribute(L"name",name);
	}
	if(childCount>0||(width>0&&height>0)) {
		if(IA2Text!=NULL&&IA2TextLength>0&&!IA2TextIsUnneededSpace) {
			// Process IAccessibleText.
			LOG_DEBUG(L"scanning text");
			int chunkStart=0;
			long attribsStart = 0;
			long attribsEnd = 0;
			map<wstring,wstring> textAttribs;
			for(int i=0;;++i) {
				if(i!=chunkStart&&(i==IA2TextLength||i==attribsEnd||IA2Text[i]==0xfffc)) {
					// We've reached the end of the current chunk of text.
					// (A chunk ends at the end of the text, at the end of an attributes run
					// or at an embedded object char.)
					// Add the chunk to the buffer.
					LOG_DEBUG("Adding text chunk, start="<<chunkStart<<" end="<<i);
					if((tempNode=buffer->addTextFieldNode(parentNode,previousNode,wstring(IA2Text+chunkStart,i-chunkStart)))!=NULL) {
						previousNode=tempNode;
						// Add text attributes.
						for(map<wstring,wstring>::const_iterator it=textAttribs.begin();it!=textAttribs.end();++it)
							previousNode->addAttribute(it->first,it->second);
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
						LOG_DEBUG("Start of new attributes run at "<<i);
						if(attribsStr) {
							IA2AttribsToMap(attribsStr,textAttribs);
							SysFreeString(attribsStr);
						}
					} else {
						// If attributes fails, assume it'll fail for the entire text.
						attribsEnd=IA2TextLength;
					}
				}
				if(paccHypertext&&IA2Text[i]==0xfffc) {
					// Embedded object char.
					LOG_DEBUG(L"embedded object char at "<<i);
					// The next chunk of text shouldn't include this char.
					chunkStart=i+1;
					LOG_DEBUG(L"get hyperlinkIndex with IAccessibleHypertext::get_hyperlinkIndex and offset "<<i);
					int hyperlinkIndex;
					if((res=paccHypertext->get_hyperlinkIndex(i,(long*)(&hyperlinkIndex)))!=S_OK) {
						LOG_DEBUG(L"paccHypertext->hyperlinkIndex with offset "<<i<<L" returned "<<res);
						continue;
					}
					LOG_DEBUG(L"hyperlinkIndex is "<<hyperlinkIndex);
					LOG_DEBUG(L"get paccHyperlink with IAccessibleHypertext::get_hyperlink and index "<<hyperlinkIndex);
					IAccessibleHyperlink* paccHyperlink=NULL;
					if((res=paccHypertext->get_hyperlink(hyperlinkIndex,&paccHyperlink))!=S_OK) {
						LOG_DEBUG(L"pacc->hyperlink with index of "<<hyperlinkIndex<<L" returned "<<res);
						continue;
					}
					LOG_DEBUG(L"get childPacc with IAccessibleHyperlink::QueryInterface and IID_IAccessible2");
					IAccessible2* childPacc=NULL;
					if((res=paccHyperlink->QueryInterface(IID_IAccessible2,(void**)(&childPacc)))!=S_OK) {
						LOG_DEBUG(L"paccHyperlink->QueryInterface with IID_IAccessible2, returned "<<res);
						paccHyperlink->Release();
						continue;
					}
					LOG_DEBUG(L"Release paccHyperlink");
					paccHyperlink->Release();
					#if IGNORE_UNNEEDED_GRAPHICS_IN_LINKS&&IGNORE_NONINTERACTIVE_UNLABELED_GRAPHICS
					long childRole;
					BSTR childName=NULL;
					BSTR childDefaction=NULL;
						//role must be link, must have name, 
					//childRole must be graphic, must have no or empty childName, childDefaction can't be click.
					if(role==ROLE_SYSTEM_LINK&&name!=NULL&&!isWhitespace(name)&&childPacc->role(&childRole)==S_OK&&childRole==ROLE_SYSTEM_GRAPHIC&&(childPacc->get_accName(varChild,&childName)!=S_OK||childName==NULL||SysStringLen(childName)==0)&&(childPacc->get_accDefaultAction(varChild,&childDefaction)==S_OK||wcscmp(childDefaction?childDefaction:L"",L"click")!=0)) {
						LOG_DEBUG(L"Ignoring unneeded graphic in link");
						if(childName) SysFreeString(childName);
						if(childDefaction) SysFreeString(childDefaction);
					childPacc->Release();
						continue;
					}
					if(childName) SysFreeString(childName);
					if(childDefaction) SysFreeString(childDefaction);
					#endif
					LOG_DEBUG(L"calling fillVBuf with childPacc ");
					if((tempNode=this->fillVBuf(childPacc,buffer,parentNode,previousNode,paccTable,paccTable2,tableID))!=NULL) {
						previousNode=tempNode;
					} else {
						LOG_DEBUG(L"Error in fillVBuf");
					}
					childPacc->Release();
				}
			}
			LOG_DEBUG(L"End of scan");
		} else if (role==ROLE_SYSTEM_GRAPHIC&&childCount>0&&name) {
			// This is an image map with a name, so render the name.
			previousNode=buffer->addTextFieldNode(parentNode,previousNode,name);
			if(previousNode&&!locale.empty()) previousNode->addAttribute(L"language",locale);
		}
		if(IA2Text!=NULL) {
			LOG_DEBUG(L"Freeing IA2Text");
			SysFreeString(IA2Text);
		}
		if(IA2TextLength==0||IA2TextIsUnneededSpace) {
			LOG_DEBUG(L"object had no text");
			//If the object has no text at all then we need to get children the ol' fassion way
			if(childCount>0) {
				LOG_DEBUG(L"Allocate memory to hold children");
				VARIANT* varChildren;
				if((varChildren=(VARIANT*)malloc(sizeof(VARIANT)*childCount))==NULL) {
					LOG_DEBUG(L"Error allocating varChildren memory");
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
						LOG_DEBUG(L"QueryInterface dispatch child to IID_IAccesible2");
						IAccessible2* childPacc=NULL;
						if((res=varChildren[i].pdispVal->QueryInterface(IID_IAccessible2,(void**)(&childPacc)))!=S_OK) {
							LOG_DEBUG(L"varChildren["<<i<<L"].pdispVal->QueryInterface to IID_iAccessible2 returned "<<res);
							childPacc=NULL;
						}
						if(childPacc) {
							LOG_DEBUG(L"calling _filVBufHelper with child object ");
							if((tempNode=this->fillVBuf(childPacc,buffer,parentNode,previousNode,paccTable,paccTable2,tableID))!=NULL) {
								previousNode=tempNode;
							} else {
								LOG_DEBUG(L"Error in calling fillVBuf");
							}
							LOG_DEBUG(L"releasing child IAccessible2 object");
							childPacc->Release();
						}
					}
					VariantClear(&(varChildren[i]));
				}
				LOG_DEBUG(L"Freeing memory holding children");
				free(varChildren);
			}
			if(childCount==0) {
				LOG_DEBUG(L"ChildCount is 0, so add accessible value or name as text");
				if(role==ROLE_SYSTEM_LINK||role==ROLE_SYSTEM_PUSHBUTTON||role==IA2_ROLE_TOGGLE_BUTTON||role==ROLE_SYSTEM_MENUITEM||(role==ROLE_SYSTEM_TEXT&&(states&STATE_SYSTEM_READONLY)&&!(states&STATE_SYSTEM_FOCUSABLE))) {
					LOG_DEBUG(L"For buttons and links we use the name as the text");
					if(name!=NULL) {
						LOG_DEBUG(L"adding name to buffer");
						previousNode=buffer->addTextFieldNode(parentNode,previousNode,name);
						if(previousNode&&!locale.empty()) previousNode->addAttribute(L"language",locale);
					} else if((role==ROLE_SYSTEM_LINK)&&(value!=NULL)) {
						wchar_t* newValue=_wcsdup(getNameForURL(value).c_str());
						previousNode=buffer->addTextFieldNode(parentNode,previousNode,newValue);
						free(newValue);
					} else if(value!=NULL) {
						previousNode=buffer->addTextFieldNode(parentNode,previousNode,value);
						if(previousNode&&!locale.empty()) previousNode->addAttribute(L"language",locale);
					} else if(width>0||height>0) {
						previousNode=buffer->addTextFieldNode(parentNode,previousNode,L" ");
						if(previousNode&&!locale.empty()) previousNode->addAttribute(L"language",locale);
					}
				} else if(role==ROLE_SYSTEM_GRAPHIC) {
					LOG_DEBUG(L"For graphics we use the name as the text");
					int isClickable=(wcscmp(defaction?defaction:L"",L"click")==0);
					int inLink=(states&STATE_SYSTEM_LINKED);
					// Unneeded graphics in links are handled elsewhere, so if we see alt="" here, we should ignore alt and fall back.
					// However, if we see alt="" for a clickable, use the alt and don't fall back.
					if(name!=NULL&&(SysStringLen(name)>0||isClickable)) {
						LOG_DEBUG(L"adding name to buffer");
						previousNode=buffer->addTextFieldNode(parentNode,previousNode,name);
						if(previousNode&&!locale.empty()) previousNode->addAttribute(L"language",locale);
					} else if((value!=NULL)&&(!IGNORE_NONINTERACTIVE_UNLABELED_GRAPHICS||(!isClickable&&inLink))) {
						wchar_t* newValue=_wcsdup(getNameForURL(value).c_str());
						previousNode=buffer->addTextFieldNode(parentNode,previousNode,newValue);
						free(newValue);
					} else if((IA2AttribsMap.count(L"src")>0)&&(!IGNORE_NONINTERACTIVE_UNLABELED_GRAPHICS||(isClickable||inLink))) {
						wchar_t* newValue=_wcsdup(getNameForURL(IA2AttribsMap[L"src"]).c_str());
						previousNode=buffer->addTextFieldNode(parentNode,previousNode,newValue);
						free(newValue);
					}
				} else {
					if(value!=NULL) {
						LOG_DEBUG(L"adding value to buffer");
						previousNode=buffer->addTextFieldNode(parentNode,previousNode,value);
						if(previousNode&&!locale.empty()) previousNode->addAttribute(L"language",locale);
					} else if(role!=ROLE_SYSTEM_CELL&&role!=IA2_ROLE_SECTION&&(width>0&&height>0)) {
						previousNode=buffer->addTextFieldNode(parentNode,previousNode,L" ");
						if(previousNode&&!locale.empty()) previousNode->addAttribute(L"language",locale);
					}
				}
			}
		}
		if ((role == ROLE_SYSTEM_CELL || role == ROLE_SYSTEM_ROWHEADER || role == ROLE_SYSTEM_COLUMNHEADER||role==IA2_ROLE_UNKNOWN) && parentNode->getLength() == 0) {
			// Always render a space for empty table cells and unknowns.
			previousNode=buffer->addTextFieldNode(parentNode,previousNode,L" ");
			if(previousNode&&!locale.empty()) previousNode->addAttribute(L"language",locale);
			parentNode->setIsBlock(false);
		}
	}
	//Free any objects and text etc we don't need, before doing any recursion to save memory
	if(name!=NULL) {
		SysFreeString(name);
	}
	if(value!=NULL) {
		SysFreeString(value);
	}
	if(defaction!=NULL) {
		SysFreeString(defaction);
		defaction=NULL;
	}
	LOG_DEBUG(L"Release pacc");
	if(paccText!=NULL) {
		LOG_DEBUG(L"Release paccText");
		paccText->Release();
	}
	if(paccHypertext!=NULL) {
		LOG_DEBUG(L"Release paccHypertext");
		paccHypertext->Release();
	}
	if (releaseTable) {
		LOG_DEBUG(L"Release paccTable/paccTable2");
		if(paccTable2)
			paccTable2->Release();
		else
			paccTable->Release();
	}
	LOG_DEBUG(L"Returning node at "<<parentNode);
	return parentNode;
}

bool getDocumentFrame(HWND* hwnd, long* childID) {
	int res;
	IAccessible2* pacc=IAccessible2FromIdentifier((int)*hwnd,*childID);
	if (!pacc) {
		LOG_DEBUG(L"Could not get IAccessible2 object");
		return false;
	}
	LOG_DEBUG(L"got IAccessible2 object at "<<pacc);

	IAccessible2* parentPacc=NULL;
	VARIANT varChild;
	varChild.vt=VT_I4;
	varChild.lVal=*childID;
	VARIANT varDisp;
	if((res=pacc->accNavigate(NAVRELATION_NODE_CHILD_OF,varChild,&varDisp))!=S_OK) {
		LOG_DEBUG(L"failed to get object from node_child_of relation");
		pacc->Release();
		return false;
	}

	if(varDisp.vt!=VT_DISPATCH) {
		LOG_DEBUG(L"variant from node_child_of relation does not hold an IDispatch");
		VariantClear(&varDisp);
		pacc->Release();
		return false;
	}
	LOG_DEBUG(L"got IDispatch object at "<<varDisp.pdispVal<<L" for node_child_of relation");

	if((res=varDisp.pdispVal->QueryInterface(IID_IAccessible2,(void**)&parentPacc))!=S_OK) {
		LOG_DEBUG(L"Could not queryInterface to IAccessible2 from IDispatch for node_child_of relation");
		VariantClear(&varDisp);
		pacc->Release();
		return false;
	}
	LOG_DEBUG(L"got IAccessible2 object at "<<parentPacc<<L" from node_child_of relation");
	VariantClear(&varDisp);

	if(parentPacc==pacc) {
		LOG_DEBUG(L"parentPacc and pacc are equal, bad relation");
		parentPacc->Release();
		pacc->Release();
		return false;
	}

	long role;
	if((res=parentPacc->role(&role))!=S_OK||role!=IA2_ROLE_INTERNAL_FRAME) {
		LOG_DEBUG(L"parentPacc is not a frame");
		parentPacc->Release();
		pacc->Release();
		return false;
	}

	if(((res=parentPacc->get_uniqueID((long*)childID))!=S_OK)||*childID>=0) {
		LOG_DEBUG(L"could not get valid uniqueID from parentPacc");
		parentPacc->Release();
		pacc->Release();
		return false;
	}
	LOG_DEBUG(L"got uniqueID "<<*childID<<L" from parentPacc");

	if((res=parentPacc->get_windowHandle(hwnd))!=S_OK) {
		LOG_DEBUG(L"Could not get valid window handle from parentPacc");
		parentPacc->Release();
		pacc->Release();
		return false;
	}
	LOG_DEBUG(L"got windowhandle "<<*hwnd<<L" from parentPacc");

	parentPacc->Release();
	pacc->Release();

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
	if(childID>=0||objectID!=OBJID_CLIENT) {
		return;
	}
	LOG_DEBUG(L"winEvent for window "<<hwnd);
	hwnd=findRealMozillaWindow(hwnd);
	if(hwnd==0) {
		LOG_DEBUG(L"Invalid window");
		return;
	}
	int docHandle=(int)hwnd;
	int ID=childID;
	VBufBackend_t* backend=NULL;
	LOG_DEBUG(L"Searching for backend in collection of "<<runningBackends.size()<<L" running backends");
	for(VBufBackendSet_t::iterator i=runningBackends.begin();i!=runningBackends.end();++i) {
		HWND rootWindow=(HWND)((*i)->rootDocHandle);
		LOG_DEBUG(L"Comparing backends root window "<<rootWindow<<L" with window "<<hwnd);
		if(rootWindow==hwnd||IsChild(rootWindow,hwnd)) {
			backend=(*i);
		} else {
			continue;
		}
		LOG_DEBUG(L"found active backend for this window at "<<backend);

		//For focus and alert events, force any invalid nodes to be updaed right now
		if(eventID==EVENT_OBJECT_FOCUS||eventID==EVENT_SYSTEM_ALERT) {
			backend->forceUpdate();
			continue;
		}

		//Ignore state change events on the root node (document) as it can cause rerendering when the document goes busy
		if(eventID==EVENT_OBJECT_STATECHANGE&&hwnd==(HWND)(backend->rootDocHandle)&&childID==backend->rootID) return;
		VBufStorage_controlFieldNode_t* node=backend->getControlFieldNodeWithIdentifier(docHandle,ID);
		if(node==NULL&&eventID==EVENT_OBJECT_STATECHANGE) {
			// This event is possibly due to a new document loading in a subframe.
			// Gecko doesn't fire a reorder on the iframe (Mozilla bug 420845), so we need to use NODE_CHILD_OF in this case so that frames will reload.
			LOG_DEBUG(L"State change on an unknown node in a subframe, try NODE_CHILD_OF");
			if (getDocumentFrame(&hwnd, &childID)) {
				#ifdef DEBUG
				Beep(2000,50);
				#endif
				LOG_DEBUG(L"Got NODE_CHILD_OF, recursing");
				renderThread_winEventProcHook(hookID,eventID,hwnd,OBJID_CLIENT,childID,threadID,time);
			} else {
				LOG_DEBUG(L"NODE_CHILD_OF failed, returning");
			}
			continue;
		}
		if(node==NULL) {
			LOG_DEBUG(L"No nodes to use, returning");
			continue;
		}
		LOG_DEBUG(L"Invalidating subtree with node at "<<node);
		backend->invalidateSubtree(node);
	}
}

void GeckoVBufBackend_t::renderThread_initialize() {
	registerWinEventHook(renderThread_winEventProcHook);
	LOG_DEBUG(L"Registered win event callback");
	VBufBackend_t::renderThread_initialize();
}

void GeckoVBufBackend_t::renderThread_terminate() {
	unregisterWinEventHook(renderThread_winEventProcHook);
	LOG_DEBUG(L"Unregistered winEvent hook");
	VBufBackend_t::renderThread_terminate();
}

void GeckoVBufBackend_t::render(VBufStorage_buffer_t* buffer, int docHandle, int ID, VBufStorage_controlFieldNode_t* oldNode) {
	LOG_DEBUG(L"Rendering from docHandle "<<docHandle<<L", ID "<<ID<<L", in to buffer at "<<buffer);
	IAccessible2* pacc=IAccessible2FromIdentifier(docHandle,ID);
	if(pacc==NULL) {
		LOG_DEBUG(L"Could not get IAccessible2, returning");
		return;
	}
	if (!oldNode) {
		// This is the root node.
		this->versionSpecificInit(pacc);
	}
	LOG_DEBUG(L"Calling fillVBuf");
	this->fillVBuf(pacc, buffer, NULL, NULL);
	pacc->Release();
	LOG_DEBUG(L"Rendering done");
}

GeckoVBufBackend_t::GeckoVBufBackend_t(int docHandle, int ID): VBufBackend_t(docHandle,ID) {
	LOG_DEBUG(L"Gecko backend constructor");
}

GeckoVBufBackend_t::~GeckoVBufBackend_t() {
	LOG_DEBUG(L"Gecko backend destructor");
}

extern "C" __declspec(dllexport) VBufBackend_t* VBufBackend_create(int docHandle, int ID) {
	VBufBackend_t* backend=new GeckoVBufBackend_t(docHandle,ID);
	LOG_DEBUG(L"Created new backend at "<<backend);
	return backend;
}

BOOL WINAPI DllMain(HINSTANCE hModule,DWORD reason,LPVOID lpReserved) {
	if(reason==DLL_PROCESS_ATTACH) {
		_CrtSetReportHookW2(_CRT_RPTHOOK_INSTALL,(_CRT_REPORT_HOOKW)NVDALogCrtReportHook);
	}
	return true;
}
