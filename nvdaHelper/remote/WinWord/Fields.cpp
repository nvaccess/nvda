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
#define WIN32_LEAN_AND_MEAN 

#include <sstream>
#include <vector>
#include <utility>
#include <comdef.h>
#include <windows.h>
#include <common/log.h>
#include <remote/nvdaInProcUtils.h>

#include "Fields.h"
#include <remote/WinWord/Constants.h>

namespace WinWord {

/* Overview of the structures being accessed:
	pRange.Fields property
	pRange.Fields.Count property
	pRange.Fields.Item method - takes an int (starting at 1) to give item 1 up to item Count. Returns a Field
	Field.Type property
	Field.Result property - the range for the ref / hyperlink object. This is the displayed range.
	Field.Code property - Not used, but gives the hidden part of the ref / hyperlink.
	Field.Result.Start property
	Field.Result.End property
*/
Fields::Fields(IDispatch* pRange) {
	IDispatchPtr pDispatchFields = nullptr;
	auto res = _com_dispatch_raw_propget( pRange, wdDISPID_RANGE_FIELDS, VT_DISPATCH, &pDispatchFields);
	if( res != S_OK || !pDispatchFields ) {
		LOG_DEBUGWARNING(L"error getting fields from range");
		return;
	}

	int count = 0;
	res = _com_dispatch_raw_propget( pDispatchFields, wdDISPID_FIELDS_COUNT, VT_I4, &count);
	if( res != S_OK || count <= 0 ) {
		return;
	}

	for(int i = 1; i <= count; ++i) {
		IDispatchPtr pDispatchItem = nullptr;
		res = _com_dispatch_raw_method( pDispatchFields, wdDISPID_FIELDS_ITEM, DISPATCH_METHOD, VT_DISPATCH, &pDispatchItem, L"\x0003", i);
		if( res != S_OK || !pDispatchItem){
			LOG_DEBUGWARNING(L"error getting field item");
			continue;
		}
		/*
		Fields can be of many types, to get this we look at Type property. We care about:
		  Ref - a Reference to some other part of the file
		  Hyperlink - a link to another part of the file or to an external URL
		
		The following are defined on msdn (WdFieldType Enumeration - https://msdn.microsoft.com/en-us/library/office/ff192211.aspx)
		*/
		const int CROSS_REFERENCE_TYPE_VALUE = 3; // wdFieldRef 
		const int HYPERLINK_TYPE_VALUE = 88; // wdFieldHyperlink
		const int PAGE_NUMBER_TYPE_VALUE = 33; // wdFieldPage
		int type = -1;
		res = _com_dispatch_raw_propget( pDispatchItem, wdDISPID_FIELDS_ITEM_TYPE, VT_I4, &type);
		if( res != S_OK || !(type == CROSS_REFERENCE_TYPE_VALUE || type == HYPERLINK_TYPE_VALUE || type == PAGE_NUMBER_TYPE_VALUE) ){
			continue;
		}

		IDispatchPtr pDispatchFieldResult = nullptr;
		res = _com_dispatch_raw_propget( pDispatchItem, wdDISPID_FIELDS_ITEM_RESULT, VT_DISPATCH, &pDispatchFieldResult);
		if( res != S_OK || !pDispatchFieldResult){
			LOG_DEBUGWARNING(L"error getting the result from the field item.");
			continue;
		}

		long resultStart = 0, resultEnd = 0;
		auto ok = S_OK == _com_dispatch_raw_propget( pDispatchFieldResult, wdDISPID_RANGE_START, VT_I4, &resultStart)
		       && S_OK == _com_dispatch_raw_propget( pDispatchFieldResult, wdDISPID_RANGE_END, VT_I4, &resultEnd);
		if(!ok){
			LOG_DEBUGWARNING(L"error getting range start and end points");
			continue;
		}

		auto itemRange = std::make_pair(resultStart, resultEnd);
		switch(type){
			case CROSS_REFERENCE_TYPE_VALUE: // intentional fall through to hyperlink case
			case HYPERLINK_TYPE_VALUE:
				m_links.push_back(itemRange);
				break;
			case PAGE_NUMBER_TYPE_VALUE:
				m_pageNumbers.push_back(itemRange);
				break;
		}
	}
}

bool inRange (long index, long start, long end) {
		return index >= start && index <= end;
	};

bool Fields::hasLinks(const int rangeStart, const int rangeEnd){
	for( auto&& link : m_links) {
		if( inRange(link.first, rangeStart, rangeEnd) ||
			inRange(link.second, rangeStart, rangeEnd) ||
			inRange(rangeStart, link.first, link.second) ||
			inRange(rangeEnd, link.first, link.second) ){
			return true;
		}
	}
	return false;
}

bool Fields::hasLinks(){
	return false == m_links.empty();
}


std::optional<int> Fields::getEndOfPageNumberFieldAtIndex(const int index){
	for( auto&& pageNum : m_pageNumbers ){
		if(inRange(index, pageNum.first, pageNum.second)){
			return pageNum.second;
		}
	}
	return std::optional<int>();
}

} // end namespace WinWord