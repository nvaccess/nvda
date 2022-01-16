/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2008-2013 NV Access Limited, Aleksey Sadovoy.
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
#include <common/ia2utils.h>
#include <remote/nvdaHelperRemote.h>
#include <vbufBase/backend.h>
#include <common/log.h>
#include "adobeAcrobat.h"

const int TEXTFLAG_UNDERLINE = 0x1;
const int TEXTFLAG_STRIKETHROUGH = 0x2;
const int TABLEHEADER_COLUMN = 0x1;
const int TABLEHEADER_ROW = 0x2;

using namespace std;

IAccessible* IAccessibleFromIdentifier(int docHandle, int ID) {
	int res;
	IAccessible* pacc=NULL;
	VARIANT varChild;
	LOG_DEBUG(L"Calling AccessibleObjectFromEvent");
	if((res=AccessibleObjectFromEvent((HWND)UlongToHandle(docHandle),OBJID_CLIENT,ID,&pacc,&varChild))!=S_OK) {
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

inline void nullifyEmpty(BSTR* text) {
	if (*text && SysStringLen(*text) == 0) {
		SysFreeString(*text);
		*text = NULL;
	}
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
	IPDDomNode* domNode, IPDDomElement* domElement,
	bool nameIsContent, wstring& lang, int flags, wstring* pageNum
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

	BSTR text = NULL;
	if (domElement) {
		// #2174: Alt or actual text should override any other text content.
		// Unfortunately, GetTextContent() still includes the text of descendants,
		// so handle this ourselves.
		domElement->GetAttribute(L"Alt", NULL, &text);
		if (!text)
			domElement->GetAttribute(L"ActualText", NULL, &text);
	}

	long childCount = 0;
	if (!text)
		domNode->GetChildCount(&childCount);

	long nodeType = 0;
	if (fontStatus == FontInfo_NoInfo && childCount > 0
		// We never want to descend beneath word nodes,
		// as word segments sometimes seem to double characters.
		&& domNode->GetType(&nodeType) == S_OK && nodeType != CPDDomNode_Word
	) {
		// HACK: #2175: Reader 10.1 and later report FontInfo_NoInfo even when there is mixed font info.
		// Therefore, we must assume FontInfo_MixedInfo.
		fontStatus = FontInfo_MixedInfo;
	} else if (fontStatus == FontInfo_MixedInfo && childCount == 0) {
		// HACK: Child count really shouldn't be 0 if fontStatus is FontInfo_MixedInfo, but it sometimes is.
		// Therefore, ignore FontInfo_MixedInfo in this case.
		// Otherwise, the node will be rendered as empty.
		fontStatus = FontInfo_NoInfo;
	}

	if (fontStatus == FontInfo_MixedInfo) {
		// This node contains text in more than one font.
		// We need to descend further to get font information.
		// Iterate through the children.
		for (long childIndex = 0; childIndex < childCount; ++childIndex) {
			IPDDomNode* domChild;
			if ((res = domNode->GetChild(childIndex, &domChild)) != S_OK) {
				LOG_DEBUG(L"IPDDomNode::GetChild returned " << res);
				continue;
			}
			// Recursive call: render text for this child and its descendants.
			if (tempNode = renderText(buffer, parentNode, previousNode, domChild, NULL, nameIsContent, lang, flags, pageNum))
				previousNode = tempNode;
			domChild->Release();
		}
	} else {

		// We don't need to descend, so add the font info and text for this node.
		if (!text) {
			if (nameIsContent) {
				// #3640: For nodes where the name is generally the content,
				// explicitly use the name, as GetTextContent might return something else.
				domNode->GetName(&text);
				nullifyEmpty(&text);
			}
			if (!text) {
				domNode->GetTextContent(&text);
				nullifyEmpty(&text);
			}
			if (!nameIsContent && !text) {
				// GetTextContent() failed or returned nothing.
				// This should mean there is no text.
				// However, GetValue() sometimes works nevertheless, so try it.
				domNode->GetValue(&text);
				nullifyEmpty(&text);
			}
		}

		if (text) {
			wstring procText;
			processText(text, procText);
			previousNode = buffer->addTextFieldNode(parentNode, previousNode, procText);
			if (previousNode) {
				if (fontStatus == FontInfo_Valid) {
					previousNode->addAttribute(L"font-name", fontName);
					if (fontSize > 0) {
						wostringstream s;
						s.setf(ios::fixed);
						s << setprecision(1) << fontSize << "pt";
						previousNode->addAttribute(L"font-size", s.str());
					}
					if ((fontFlags&PDDOM_FONTATTR_ITALIC)==PDDOM_FONTATTR_ITALIC) previousNode->addAttribute(L"italic", L"1");
					if ((fontFlags&PDDOM_FONTATTR_BOLD)==PDDOM_FONTATTR_BOLD) previousNode->addAttribute(L"bold", L"1");
				}
				previousNode->addAttribute(L"language", lang);
				if (flags & TEXTFLAG_UNDERLINE)
					previousNode->addAttribute(L"underline", L"1");
				else if (flags & TEXTFLAG_STRIKETHROUGH)
					previousNode->addAttribute(L"strikethrough", L"1");
				if (pageNum)
					previousNode->addAttribute(L"page-number", *pageNum);
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

class AdobeAcrobatVBufStorage_controlFieldNode_t: public VBufStorage_controlFieldNode_t {
	public:
	AdobeAcrobatVBufStorage_controlFieldNode_t(int docHandle, int ID, bool isBlock): VBufStorage_controlFieldNode_t(docHandle, ID, isBlock) {
	}

	protected:
	wstring language;
	friend class AdobeAcrobatVBufBackend_t;
};

/*
 * Adjusts the current column number to skip past columns spanned by previous rows,
 * decrementing row spans as they are encountered.
 */
inline void handleColsSpannedByPrevRows(TableInfo& tableInfo) {
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

/*
 * Adds table header info for a single cell which explicitly defines headers
 * using the Headers attribute.
 */
inline void fillExplicitTableHeadersForCell(AdobeAcrobatVBufStorage_controlFieldNode_t& cell, int docHandle, wstring& headersAttr, TableInfo& tableInfo) {
	wostringstream colHeaders, rowHeaders;

	// The Headers attribute string is in the form "[[id id ... ]]"
	// Loop through all the ids.
	// Ignore the "[[" prefix and the " ]]" suffix.
	size_t lastPos = headersAttr.length() - 3;
	size_t startPos = 2;
	while (startPos < lastPos) {
		// Search for a space, which indicates the end of this id.
		size_t endPos = headersAttr.find(L' ', startPos);
		if (endPos == wstring::npos)
			break;
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

wstring* AdobeAcrobatVBufBackend_t::getPageNum(IPDDomNode* domNode) {
	// Get the page number.
	IPDDomNodeExt* domNodeExt;
	if (domNode->QueryInterface(IID_IPDDomNodeExt, (void**)&domNodeExt) != S_OK) 
		return NULL;
	long firstPage, lastPage;
	// The page number is only useful if the first and last pages are the same.
	if (domNodeExt->GetPageNum(&firstPage, &lastPage) != S_OK || firstPage != lastPage) {
		domNodeExt->Release();
		return NULL;
	}
	domNodeExt->Release();

	// Use the page label if possible.
	BSTR label;
	if (this->docPagination && this->docPagination->LabelForPageNum(firstPage, &label) == S_OK) {
		wstring* ret = new wstring(label);
		SysFreeString(label);
		return ret;
	}
	
	// If the label couldn't be retrieved, use the page number.
	wostringstream s;
	// GetPageNum returns 0-based numbers, but we want 1-based.
	s << firstPage + 1;
	return new wstring(s.str());
}

AdobeAcrobatVBufStorage_controlFieldNode_t* AdobeAcrobatVBufBackend_t::fillVBuf(int docHandle, IAccessible* pacc, VBufStorage_buffer_t* buffer,
	AdobeAcrobatVBufStorage_controlFieldNode_t* parentNode, VBufStorage_fieldNode_t* previousNode,
	AdobeAcrobatVBufStorage_controlFieldNode_t* oldNode,
	TableInfo* tableInfo, wstring* pageNum
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
	AdobeAcrobatVBufStorage_controlFieldNode_t* oldParentNode = parentNode;
	parentNode = static_cast<AdobeAcrobatVBufStorage_controlFieldNode_t*>(buffer->addControlFieldNode(parentNode, previousNode, 
		new AdobeAcrobatVBufStorage_controlFieldNode_t(docHandle, ID, true)));
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
	if (!domNode) {
		LOG_DEBUGWARNING(L"Couldn't get IPDDomNode for docHandle " << docHandle << L" id " << ID);
	}

	IPDDomElement* domElement = NULL;
	LOG_DEBUG(L"Trying to get IPDDomElement");
	if (domNode && (res = domNode->QueryInterface(IID_IPDDomElement, (void**)(&domElement))) != S_OK) {
		LOG_DEBUG(L"QueryInterface to IPDDomElement returned " << res);
		domElement = NULL;
	}

	BSTR stdName = NULL;
	int textFlags = 0;
	// Whether to render just a space in place of the content.
	bool renderSpace = false;
	BSTR tempBstr = NULL;
	if (domElement) {
		// Get stdName.
		if ((res = domElement->GetStdName(&stdName)) != S_OK) {
			LOG_DEBUG(L"IPDDomElement::GetStdName returned " << res);
			stdName = NULL;
		}
		if (stdName) {
			parentNode->addAttribute(L"acrobat::stdname", stdName);
			if (wcscmp(stdName, L"Span") == 0 || wcscmp(stdName, L"Link") == 0 || wcscmp(stdName, L"Quote") == 0) {
				// This is an inline element.
				parentNode->isBlock=false;
			}
			if (wcscmp(stdName, L"Formula") == 0) {
				// We don't want the content of formulas,
				// but we still want a space so the user can get at them.
				renderSpace = true;
			}
		}

		// Get language.
		if (domElement->GetAttribute(L"Lang", NULL, &tempBstr) == S_OK && tempBstr) {
			parentNode->language = tempBstr;
			SysFreeString(tempBstr);
		}

		// Determine whether the text has underline or strikethrough.
		if (domElement->GetAttribute(L"TextDecorationType", L"Layout", &tempBstr) == S_OK && tempBstr) {
			if (wcscmp(tempBstr, L"Underline") == 0)
				textFlags |= TEXTFLAG_UNDERLINE;
			else if (wcscmp(tempBstr, L"LineThrough") == 0)
				textFlags |= TEXTFLAG_STRIKETHROUGH;
			SysFreeString(tempBstr);
		}
	}

	// If this node has no language, inherit it from its parent node.
	if (parentNode->language.empty()) {
		if (oldParentNode)
			parentNode->language = oldParentNode->language;
		// If this node was updated, we're rendering into a temporary buffer,
		// so try getting the parent from the old node.
		else if (oldNode && oldNode->getParent())
			parentNode->language = static_cast<AdobeAcrobatVBufStorage_controlFieldNode_t*>(oldNode->getParent())->language;
	}

	//Get the child count
	int childCount=0;
	// We don't want to descend into lists and combo boxes.
	// Besides, Acrobat reports the child count, but the children can't be accessed.
	if (!renderSpace && role != ROLE_SYSTEM_LIST && role != ROLE_SYSTEM_COMBOBOX) {
		LOG_DEBUG(L"get childCount with IAccessible::get_accChildCount");
		if((res=pacc->get_accChildCount((long*)(&childCount)))!=S_OK) {
			LOG_DEBUG(L"pacc->get_accChildCount returned "<<res);
			childCount=0;
		}
	}
	LOG_DEBUG(L"childCount is "<<childCount);

	bool deletePageNum = false;
	if (!pageNum && domNode && (pageNum = this->getPageNum(domNode))) {
		deletePageNum = true;
	}

	#define addAttrsToTextNode(node) { \
		node->addAttribute(L"language", parentNode->language); \
		if (pageNum) \
			node->addAttribute(L"page-number", *pageNum); \
		}

	// Handle tables.
	if (role == ROLE_SYSTEM_TABLE) {
		tableInfo = new TableInfo;
		tableInfo->tableID = ID;
		tableInfo->curRowNumber = 0;
		tableInfo->curColumnNumber = 0;
		wostringstream s;
		s << ID;
		parentNode->addAttribute(L"table-id", s.str());
		if (domElement && domElement->GetAttribute(L"Summary", L"Table", &tempBstr) == S_OK && tempBstr) {
			if (tempNode = buffer->addTextFieldNode(parentNode, previousNode, tempBstr)) {
				addAttrsToTextNode(tempNode);
				previousNode = tempNode;
			}
			SysFreeString(tempBstr);
		}
	} else if (role == ROLE_SYSTEM_ROW&&tableInfo) {
		++tableInfo->curRowNumber;
		tableInfo->curColumnNumber = 0;
	} else if ((role == ROLE_SYSTEM_CELL || role == ROLE_SYSTEM_COLUMNHEADER || role == ROLE_SYSTEM_ROWHEADER)&&tableInfo) {
		++tableInfo->curColumnNumber;
		handleColsSpannedByPrevRows(*tableInfo);
		wostringstream s;
		s << tableInfo->tableID;
		parentNode->addAttribute(L"table-id", s.str());
		s.str(L"");
		s << tableInfo->curRowNumber;
		parentNode->addAttribute(L"table-rownumber", s.str());
		s.str(L"");
		int startCol = tableInfo->curColumnNumber;
		s << startCol;
		parentNode->addAttribute(L"table-columnnumber", s.str());
		if (domElement && domElement->GetAttribute(L"Headers", L"Table", &tempBstr) == S_OK && tempBstr) {
			// This node has explicitly defined headers.
			// Some of the referenced nodes might not be rendered yet,
			// so handle these later.
			// Note that IPDDomNode::GetFromID() doesn't work, but even if it did,
			// retrieving header info this way would probably be a bit slow.
			tableInfo->nodesWithExplicitHeaders.push_back(make_pair(parentNode, tempBstr));
			SysFreeString(tempBstr);
		} else {
			map<int, wstring>::const_iterator headersIt;
			// Add implicit column headers for this cell.
			if ((headersIt = tableInfo->columnHeaders.find(startCol)) != tableInfo->columnHeaders.end())
				parentNode->addAttribute(L"table-columnheadercells", headersIt->second);
			// Add implicit row headers for this cell.
			if ((headersIt = tableInfo->rowHeaders.find(tableInfo->curRowNumber)) != tableInfo->rowHeaders.end())
				parentNode->addAttribute(L"table-rowheadercells", headersIt->second);
		}
		// The last row spanned by this cell.
		// This will be updated below if there is a row span.
		int endRow = tableInfo->curRowNumber;
		if (domElement) {
			if (domElement->GetAttribute(L"ColSpan", L"Table", &tempBstr) == S_OK && tempBstr) {
				parentNode->addAttribute(L"table-columnsspanned", tempBstr);
				tableInfo->curColumnNumber += max(_wtoi(tempBstr) - 1, 0);
				SysFreeString(tempBstr);
			}
			if (domElement->GetAttribute(L"RowSpan", L"Table", &tempBstr) == S_OK && tempBstr) {
				parentNode->addAttribute(L"table-rowsspanned", tempBstr);
				// Keep trakc of how many rows after this one are spanned by this cell.
				int span = _wtoi(tempBstr) - 1;
				if (span > 0) {
					// The row span needs to be recorded for each spanned column.
					for (int col = startCol; col <= tableInfo->curColumnNumber; ++col)
						tableInfo->columnRowSpans[col] = span;
					endRow += span;
				}
				SysFreeString(tempBstr);
			}
		}
		if (role == ROLE_SYSTEM_COLUMNHEADER || role == ROLE_SYSTEM_ROWHEADER) {
			int headerType = 0;
			if (domElement && domElement->GetAttribute(L"Scope", L"Table", &tempBstr) == S_OK && tempBstr) {
				if (wcscmp(tempBstr, L"Column") == 0)
					headerType = TABLEHEADER_COLUMN;
				else if (wcscmp(tempBstr, L"Row") == 0)
					headerType = TABLEHEADER_ROW;
				else if (wcscmp(tempBstr, L"Both") == 0)
					headerType = TABLEHEADER_COLUMN | TABLEHEADER_ROW;
				SysFreeString(tempBstr);
			}
			if (!headerType)
				headerType = (role == ROLE_SYSTEM_COLUMNHEADER) ? TABLEHEADER_COLUMN : TABLEHEADER_ROW;
			if (headerType & TABLEHEADER_COLUMN) {
				// Record this as a column header for each spanned column.
				s.str(L"");
				s << docHandle << L"," << ID << L";";
				for (int col = startCol; col <= tableInfo->curColumnNumber; ++col)
					tableInfo->columnHeaders[col] += s.str();
			}
			if (headerType & TABLEHEADER_ROW) {
				// Record this as a row header for each spanned row.
				s.str(L"");
				s << docHandle << L"," << ID << L";";
				for (int row = tableInfo->curRowNumber; row <= endRow; ++row)
					tableInfo->rowHeaders[row] += s.str();
			}
			if (domElement && domElement->GetID(&tempBstr) == S_OK && tempBstr) {
				// Record the id string and associated header info for use when handling explicitly defined headers.
				TableHeaderInfo& headerInfo = tableInfo->headersInfo[tempBstr];
				headerInfo.uniqueId = ID;
				headerInfo.type = headerType;
				SysFreeString(tempBstr);
			}
		}
	}

	if (renderSpace) {
		// Just render a space.
		if (tempNode = buffer->addTextFieldNode(parentNode, previousNode, L" ")) {
			addAttrsToTextNode(tempNode);
			previousNode=tempNode;
		}

	} else if (childCount > 0) {
		// Iterate through the children.
		LOG_DEBUG(L"Fetch children with AccessibleChildren");
		auto[varChildren, accChildRes] = getAccessibleChildren(pacc, 0, childCount);
		if(S_OK != accChildRes || varChildren.size() == 0) {
			LOG_DEBUG(L"Failed to get AccessibleChildren (count: " << childCount << L"), res: " << accChildRes);
			childCount=0;
		}
		LOG_DEBUG(L"got "<< varChildren.size() << L" children");
		for(auto i = 0u; i < varChildren.size(); ++i) {
			LOG_DEBUG(L"child " << i);
			if(VT_DISPATCH == varChildren[i].vt) {
				LOG_DEBUG(L"QueryInterface dispatch child to IID_IAccesible");
				CComQIPtr<IAccessible, &IID_IAccessible> childPacc(varChildren[i].pdispVal);
				if(!childPacc) {
					LOG_DEBUG(L"varChildren[" << i << L"]: QueryInterface to IID_iAccessible failed.");
				}
				else {
					if (this->isXFA) {
						// HACK: If this is an XFA document, we must call WindowFromAccessibleObject() so that AccessibleObjectFromEvent() will work for this node.
						HWND tempHwnd;
						WindowFromAccessibleObject(childPacc, &tempHwnd);
					}
					LOG_DEBUG(L"calling filVBuf with child object ");
					if ((tempNode = this->fillVBuf(docHandle, childPacc, buffer, parentNode, previousNode, NULL, tableInfo, pageNum))!=NULL) {
						previousNode=tempNode;
					} else {
						LOG_DEBUG(L"Error in calling fillVBuf");
					}
				}
			}
		}
	} else {
		// No children, so this is a leaf node.
		if (!this->isXFA && !stdName) {
			// Non-XFA leaf nodes with no stdName are inline.
			parentNode->isBlock=false;
		}

		// Get the name.
		BSTR name = NULL;
		// #3645: We need to test accName for graphics.
		if ((states & STATE_SYSTEM_FOCUSABLE || role == ROLE_SYSTEM_GRAPHIC) && (res = pacc->get_accName(varChild, &name)) != S_OK) {
			LOG_DEBUG(L"IAccessible::get_accName returned " << res);
			name = NULL;
		}
		nullifyEmpty(&name);

		bool useNameAsContent = role == ROLE_SYSTEM_LINK || role == ROLE_SYSTEM_PUSHBUTTON ||
			role == ROLE_SYSTEM_RADIOBUTTON || role == ROLE_SYSTEM_CHECKBUTTON ||
			// #3645: Test accName, as IPDDomNode::GetName might return meaningless "mc-ref"
			// but accName doesn't.
			(role == ROLE_SYSTEM_GRAPHIC && name);

		if (name && !useNameAsContent) {
			parentNode->addAttribute(L"name", name);
			// Render the name before this node,
			// as the label is often not a separate node and thus won't be rendered into the buffer.
			// We can't do this if this node is being updated,
			// but in this case, the name has already been rendered before anyway.
			if (oldParentNode && (tempNode = buffer->addTextFieldNode(oldParentNode, parentNode->getPrevious(), name)))
				addAttrsToTextNode(tempNode);
		}

		// Hereafter, tempNode is the text node (if any).
		if (domNode) {
			tempNode = renderText(buffer, parentNode, previousNode, domNode, domElement, useNameAsContent, parentNode->language, textFlags, pageNum);
			if (tempNode) {
				// There was text.
				previousNode = tempNode;
			}
		} else {
			tempNode = NULL;
		}

		if (name)
			SysFreeString(name);

		if (!tempNode && states & STATE_SYSTEM_FOCUSABLE) {
			// This node is focusable, but contains no text.
			// Therefore, add it with a space so that the user can get to it.
			if (tempNode = buffer->addTextFieldNode(parentNode, previousNode, L" ")) {
				addAttrsToTextNode(tempNode);
				previousNode=tempNode;
			}
		}
	}

	// Finalise tables.
	if ((role == ROLE_SYSTEM_CELL || role == ROLE_SYSTEM_COLUMNHEADER || role == ROLE_SYSTEM_ROWHEADER) && parentNode->getLength() == 0) {
		// Always render a space for empty table cells.
		previousNode=buffer->addTextFieldNode(parentNode,previousNode,L" ");
		addAttrsToTextNode(previousNode);
		parentNode->isBlock=false;
	} else if (role == ROLE_SYSTEM_TABLE) {
		nhAssert(tableInfo);
		for (list<pair<AdobeAcrobatVBufStorage_controlFieldNode_t*, wstring>>::iterator it = tableInfo->nodesWithExplicitHeaders.begin(); it != tableInfo->nodesWithExplicitHeaders.end(); ++it)
			fillExplicitTableHeadersForCell(*it->first, docHandle, it->second, *tableInfo);
		wostringstream s;
		s << tableInfo->curRowNumber;
		parentNode->addAttribute(L"table-rowcount", s.str());
		s.str(L"");
		s << tableInfo->curColumnNumber;
		parentNode->addAttribute(L"table-columncount", s.str());
		delete tableInfo;
	}

	if (deletePageNum)
		delete pageNum;
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

	#undef addAttrsToTextNode

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

	int docHandle=HandleToUlong(hwnd);
	int ID=(objectID>0)?objectID:childID;
	VBufBackend_t* backend=NULL;
	LOG_DEBUG(L"Searching for backend in collection of "<<runningBackends.size()<<L" running backends");
	for(VBufBackendSet_t::iterator i=runningBackends.begin();i!=runningBackends.end();++i) {
		HWND rootWindow=(HWND)UlongToHandle((*i)->rootDocHandle);
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
	if (this->docPagination)
		this->docPagination->Release();
	VBufBackend_t::renderThread_terminate();
}

bool checkIsXFA(IAccessible* rootPacc, VARIANT& varChild) {
	VARIANT varState;
	VariantInit(&varState);
	if (rootPacc->get_accState(varChild, &varState) != S_OK) {
		return false;
	}
	int states = varState.lVal;
	VariantClear(&varState);

	// If the root accessible is read-only, this is not an XFA document.
	return !(states & STATE_SYSTEM_READONLY);
}

IPDDomDocPagination* getDocPagination(IAccessible* pacc, VARIANT& varChild) {
	IServiceProvider* servProv;
	if (pacc->QueryInterface(IID_IServiceProvider, (void**)&servProv) != S_OK)
		return NULL;
	IPDDomNode* domNode = getPDDomNode(varChild, servProv);
	servProv->Release();
	if (!domNode)
		return NULL;
	IPDDomDocPagination* ret;
	if (domNode->QueryInterface(IID_IPDDomDocPagination, (void**)&ret) != S_OK)
		ret = NULL;
	domNode->Release();
	return ret;
}

void AdobeAcrobatVBufBackend_t::render(VBufStorage_buffer_t* buffer, int docHandle, int ID, VBufStorage_controlFieldNode_t* oldNode) {
	LOG_DEBUG(L"Rendering from docHandle "<<docHandle<<L", ID "<<ID<<L", in to buffer at "<<buffer);
	IAccessible* pacc=IAccessibleFromIdentifier(docHandle,ID);
	nhAssert(pacc); //must get a valid IAccessible object
	if (!oldNode) {
		// This is the root node.
		VARIANT varChild;
		varChild.vt = VT_I4;
		varChild.lVal = 0;
		this->isXFA = checkIsXFA(pacc, varChild);
		this->docPagination = getDocPagination(pacc, varChild);
	}
	this->fillVBuf(docHandle, pacc, buffer, NULL, NULL, static_cast<AdobeAcrobatVBufStorage_controlFieldNode_t*>(oldNode));
	pacc->Release();
	LOG_DEBUG(L"Rendering done");
}

AdobeAcrobatVBufBackend_t::AdobeAcrobatVBufBackend_t(int docHandle, int ID)
	: VBufBackend_t(docHandle,ID)
	, isXFA(true)
	, docPagination(nullptr)
{
	LOG_DEBUG(L"AdobeAcrobat backend constructor");
}

AdobeAcrobatVBufBackend_t::~AdobeAcrobatVBufBackend_t() {
	LOG_DEBUG(L"AdobeAcrobat backend destructor");
}

VBufBackend_t* AdobeAcrobatVBufBackend_t_createInstance(int docHandle, int ID) {
	VBufBackend_t* backend=new AdobeAcrobatVBufBackend_t(docHandle,ID);
	LOG_DEBUG(L"Created new backend at "<<backend);
	return backend;
}

