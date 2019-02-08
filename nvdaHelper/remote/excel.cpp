/*
This file is a part of the NVDA project.
Copyright 2018 NV Access Limited.
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

#include <comdef.h>
#include <atlcomcli.h>
#include <windows.h>
#include <common/log.h>
#include <common/COMUtils.h>
#include "inProcess.h"
#include "nvdaInProcUtils.h"

// Excel IDispatch IDs
const long XLDISPID_RANGE_ROW=257;
const long XLDISPID_RANGE_COLUMN=240;
const long XLDISPID_RANGE_ADDRESS=236;
const long XLDISPID_RANGE_MERGEAREA=1385;
const long XLDISPID_RANGE_NEXT=502;
const long XLDISPID_RANGE_WIDTH=122;
const long XLDISPID_RANGE_SHRINKTOFIT=209;
const long XLDISPID_RANGE_WRAPTEXT=276;
const long XLDISPID_RANGE_HYPERLINKS=1393;
const long XLDISPID_HYPERLINKS_COUNT=118;
const long XLDISPID_RANGE_ENTIREROW=247;
const long XLDISPID_RANGE_ROWS=258;
const long XLDISPID_ROWS_COUNT=118;
const long XLDISPID_ROWS_ITEM=170;
const long XLDISPID_ROW_SUMMARY=273;
const long XLDISPID_ROW_SHOWDETAIL=585;
const long XLDISPID_ROW_OUTLINELEVEL=271;
const long XLDISPID_RANGE_ENTIRECOLUMN=246;
const long XLDISPID_RANGE_COLUMNS=241;
const long XLDISPID_COLUMNS_COUNT=118;
const long XLDISPID_COLUMNS_ITEM=170;
const long XLDISPID_COLUMN_SUMMARY=273;
const long XLDISPID_COLUMN_SHOWDETAIL=585;
const long XLDISPID_COLUMN_OUTLINELEVEL=271;
const long XLDISPID_RANGE_COMMENT=910;
const long XLDISPID_RANGE_HASFORMULA=267;
const long XLDISPID_RANGE_VALIDATION=1387;
const long XLDISPID_VALIDATION_TYPE=108;
const long XLDISPID_VALIDATION_INPUTMESSAGE=1611;
const long XLDISPID_VALIDATION_INPUTTITLE=1612;
const long XLDISPID_RANGE_WORKSHEET=348;
const long XLDISPID_WORKSHEET_PROTECTCONTENTS=292;
const long XLDISPID_RANGE_LOCKED=269;
const long XLDISPID_RANGE_TEXT=138;
const long XLDISPID_RANGE_FONT=146;
const long XLDISPID_FONT_SIZE=104;
const long XLDISPID_FONT_BOLD=96;
const long XLDISPID_FONT_ITALIC=101;
const long XLDISPID_FONT_UNDERLINE=106;
const long XLDISPID_FONT_STRIKETHROUGH=105;
const long XLDISPID_FONT_NAME=110;
const long XLDISPID_RANGE_DISPLAYFORMAT=666;
const long XLDISPID_RANGE_OFFSET=254;

// NVDA states
const __int64 STATE_EXPANDED=0x100;
const __int64 STATE_COLLAPSED=0x200;
const __int64 STATE_LINKED=0x1000;
const __int64 STATE_HASPOPUP=0x2000;
const __int64 STATE_PROTECTED=0x4000;
const __int64 STATE_HASFORMULA=0x1000000000;
const __int64 STATE_HASCOMMENT=0x2000000000;
const __int64 STATE_CROPPED=0x8000000000;
const __int64 STATE_OVERFLOWING=0x10000000000;
const __int64 STATE_UNLOCKED=0x20000000000;

long getCellTextWidth(HWND hwnd, IDispatch* pDispatchRange) {
	CComBSTR sText;
	_com_dispatch_raw_propget(pDispatchRange,XLDISPID_RANGE_TEXT,VT_BSTR,&sText);
	long textLength=sText?sText.Length():0;
	if(textLength==0) {
		return 0;
	}
	CComPtr<IDispatch> pDispatchFont=nullptr;
	_com_dispatch_raw_propget(pDispatchRange,XLDISPID_RANGE_FONT,VT_DISPATCH,&pDispatchFont);
	if(!pDispatchFont) {
		LOG_ERROR(L"range.font failed");
		return 0;
	}
	double fontSize=11.0;
	_com_dispatch_raw_propget(pDispatchFont,XLDISPID_FONT_SIZE,VT_R8,&fontSize);
	long iFontHeight=static_cast<long>(fontSize)*-1;
	BOOL bold=false;
	_com_dispatch_raw_propget(pDispatchFont,XLDISPID_FONT_BOLD,VT_BOOL,&bold);
	long iFontWeight=bold?700:400;
	BOOL sFontItalic=false;
	_com_dispatch_raw_propget(pDispatchFont,XLDISPID_FONT_ITALIC,VT_BOOL,&sFontItalic);
	long sFontUnderline=0;
	_com_dispatch_raw_propget(pDispatchFont,XLDISPID_FONT_UNDERLINE,VT_I4,&sFontUnderline);
	BOOL sFontStrikeThrough=false;
	_com_dispatch_raw_propget(pDispatchFont,XLDISPID_FONT_STRIKETHROUGH,VT_BOOL,&sFontStrikeThrough);
	CComBSTR sFontName;
	_com_dispatch_raw_propget(pDispatchFont,XLDISPID_FONT_NAME,VT_BSTR,&sFontName);
	HDC windowDC=GetDC(hwnd);
	HDC tempDC=CreateCompatibleDC(windowDC);
	ReleaseDC(hwnd,windowDC);
	HBITMAP hBmp=CreateCompatibleBitmap(tempDC,1,1);
	HGDIOBJ hOldBmp=SelectObject(tempDC,hBmp);
	long dpi = GetDeviceCaps(tempDC, LOGPIXELSX);
	long iFontWidth=0;
	long iEscapement=0;
	long iOrientation=0;
	long iCharSet=0;
	long iOutputPrecision=0;
	long iClipPrecision=0;
	long iOutputQuality=0;
	long iPitchAndFamily=0;
	HFONT hFont=CreateFontW(iFontHeight, iFontWidth, iEscapement, iOrientation, iFontWeight, sFontItalic, sFontUnderline, sFontStrikeThrough, iCharSet, iOutputPrecision, iClipPrecision, iOutputQuality, iPitchAndFamily, sFontName);
	HGDIOBJ hOldFont=SelectObject(tempDC, hFont);
	SIZE sizl={0};
	GetTextExtentPoint32W(tempDC, sText, textLength,&sizl);
	SelectObject(tempDC, hOldFont);
	DeleteObject(hFont);
	SelectObject(tempDC, hOldBmp);
	DeleteObject(hBmp);
	DeleteDC(tempDC);
	return sizl.cx;
}

__int64 getCellStates(HWND hwnd, IDispatch* pDispatchRange) {
	__int64 states=0;
	// If the current row is a summary row, expose the collapsed or expanded states depending on wither the inner rows are showing or not.
	CComPtr<IDispatch> pDispatchRow=nullptr;
	HRESULT res=_com_dispatch_raw_propget(pDispatchRange,XLDISPID_RANGE_ENTIREROW,VT_DISPATCH,&pDispatchRow);
	if(res!=S_OK) {
		LOG_DEBUGWARNING(L"range.entireRow failed with code "<<res);
	}
	if(pDispatchRow) {
		BOOL summary=false;
		res=_com_dispatch_raw_propget(pDispatchRow,XLDISPID_ROW_SUMMARY,VT_BOOL,&summary);
		if(res!=S_OK) {
			LOG_DEBUGWARNING(L"row.summary failed with code "<<res);
		}
		if(summary) {
			BOOL showDetail=false;
			res=_com_dispatch_raw_propget(pDispatchRow,XLDISPID_ROW_SHOWDETAIL,VT_BOOL,&showDetail);
			if(res!=S_OK) {
				LOG_DEBUGWARNING(L"row.showDetail failed with code "<<res);
			}
			states+=(showDetail?STATE_EXPANDED:STATE_COLLAPSED);
		}
	}
	// If this row was neither collapsed or expanded, then try the same for columns instead. 
	if(!(states&STATE_EXPANDED)&&!(states&STATE_COLLAPSED)) {
		CComPtr<IDispatch> pDispatchColumn=nullptr;
		res=_com_dispatch_raw_propget(pDispatchRange,XLDISPID_RANGE_ENTIRECOLUMN,VT_DISPATCH,&pDispatchColumn);
		if(res!=S_OK) {
			LOG_DEBUGWARNING(L"range.entireColumn failed with code "<<res);
		}
		if(pDispatchColumn) {
			BOOL summary=false;
			res=_com_dispatch_raw_propget(pDispatchColumn,XLDISPID_COLUMN_SUMMARY,VT_BOOL,&summary);
			if(res!=S_OK) {
				LOG_DEBUGWARNING(L"column.summary failed with code "<<res);
			}
			if(summary) {
				BOOL showDetail=false;
				res=_com_dispatch_raw_propget(pDispatchColumn,XLDISPID_COLUMN_SHOWDETAIL,VT_BOOL,&showDetail);
				if(res!=S_OK) {
					LOG_DEBUGWARNING(L"column.showDetail failed with code "<<res);
				}
				states+=(showDetail?STATE_EXPANDED:STATE_COLLAPSED);
			}
		}
	}
	// Expose whether this cell has a formula
	BOOL hasFormula=false;
	res=_com_dispatch_raw_propget(pDispatchRange,XLDISPID_RANGE_HASFORMULA,VT_BOOL,&hasFormula);
	if(res!=S_OK) {
		LOG_DEBUGWARNING(L"range.hasFormula failed with code "<<res);
	}
	if(hasFormula) {
		states+=STATE_HASFORMULA;
	}
	// Expose whether this cell has a dropdown menu for choosing valid values
	CComPtr<IDispatch> pDispatchValidation=nullptr;
	res=_com_dispatch_raw_propget(pDispatchRange,XLDISPID_RANGE_VALIDATION,VT_DISPATCH,&pDispatchValidation);
	if(res!=S_OK) {
		LOG_DEBUGWARNING(L"range.validation failed with code "<<res);
	}
	if(pDispatchValidation) {
		long validationType=0;
		res=_com_dispatch_raw_propget(pDispatchValidation,XLDISPID_VALIDATION_TYPE,VT_I4,&validationType);
		if(res!=S_OK) {
			//LOG_DEBUGWARNING(L"validation.type failed with code "<<res);
		}
		if(validationType==3) {
			states+=STATE_HASPOPUP;
		}
	}
	// Expose whether this cell has comments
	CComPtr<IDispatch> pDispatchComment=nullptr;
	res=_com_dispatch_raw_propget(pDispatchRange,XLDISPID_RANGE_COMMENT,VT_DISPATCH,&pDispatchComment);
	if(res!=S_OK) {
		LOG_DEBUGWARNING(L"range.comment failed with code "<<res);
	}
	if(pDispatchComment) {
		states+=STATE_HASCOMMENT;
	}
	// Expose whether this cell is unlocked for editing
	BOOL locked=false;
	res=_com_dispatch_raw_propget(pDispatchRange,XLDISPID_RANGE_LOCKED,VT_BOOL,&locked);
	if(res!=S_OK) {
		LOG_DEBUGWARNING(L"range.locked failed with code "<<res);
	}
	if(!locked) {
		CComPtr<IDispatch> pDispatchWorksheet=nullptr;
		res=_com_dispatch_raw_propget(pDispatchRange,XLDISPID_RANGE_WORKSHEET,VT_DISPATCH,&pDispatchWorksheet);
		if(res!=S_OK) {
			LOG_DEBUGWARNING(L"range.worksheet failed with code "<<res);
		}
		if(pDispatchWorksheet) {
			BOOL protectContents=false;
			res=_com_dispatch_raw_propget(pDispatchWorksheet,XLDISPID_WORKSHEET_PROTECTCONTENTS,VT_BOOL,&protectContents);
			if(res!=S_OK) {
				LOG_DEBUGWARNING(L"worksheet.protectcontents failed with code "<<res);
			}
			if(protectContents) {
				states+=STATE_UNLOCKED;
			}
		}
	}
	// Expose whether this cell contains links
	CComPtr<IDispatch> pDispatchHyperlinks=nullptr;
	res=_com_dispatch_raw_propget(pDispatchRange,XLDISPID_RANGE_HYPERLINKS,VT_DISPATCH,&pDispatchHyperlinks);
	if(res!=S_OK) {
		LOG_DEBUGWARNING(L"range.hyperlinks failed with code "<<res);
	}
	if(pDispatchHyperlinks) {
		long count=0;
		res=_com_dispatch_raw_propget(pDispatchHyperlinks,XLDISPID_HYPERLINKS_COUNT,VT_I4,&count);
		if(res!=S_OK) {
			LOG_DEBUGWARNING(L"hyperlinks.count failed with code "<<res);
		}
		if(count>0) {
			states+=STATE_LINKED;
		}
	}
	// Expose whether this cell's content flows outside the cell, 
	// and if so, whether it is cropped by the next cell, or overflowing into the next cell. 
	BOOL shrinkToFit=false;
	res=_com_dispatch_raw_propget(pDispatchRange,XLDISPID_RANGE_SHRINKTOFIT,VT_BOOL,&shrinkToFit);
	if(res!=S_OK) {
		LOG_DEBUGWARNING(L"range.shrinkToFit failed with code "<<res);
	}
	if(!shrinkToFit) {
		BOOL wrapText=false;
		res=_com_dispatch_raw_propget(pDispatchRange,XLDISPID_RANGE_WRAPTEXT,VT_BOOL,&wrapText);
		if(res!=S_OK) {
			LOG_DEBUGWARNING(L"range.wrapText failed with code "<<res);
		}
		if(!wrapText) {
			long textWidth=getCellTextWidth(hwnd,pDispatchRange);
			if(textWidth>0) {
				long rangeWidth=0;
				CComPtr<IDispatch> pDispatchNextCell=nullptr;
				CComPtr<IDispatch> pDispatchMergeArea=nullptr;
				res=_com_dispatch_raw_propget(pDispatchRange,XLDISPID_RANGE_MERGEAREA,VT_DISPATCH,&pDispatchMergeArea);
				if(res!=S_OK) {
					LOG_DEBUGWARNING(L"range.mergeArea failed with code "<<res);
				}
				if(pDispatchMergeArea) {
					res=_com_dispatch_raw_propget(pDispatchMergeArea,XLDISPID_RANGE_WIDTH,VT_I4,&rangeWidth);
					if(res!=S_OK) {
						LOG_DEBUGWARNING(L"range.width failed with code "<<res);
					}
					CComPtr<IDispatch> pDispatchColumns=nullptr;
					res=_com_dispatch_raw_propget(pDispatchMergeArea,XLDISPID_RANGE_COLUMNS,VT_DISPATCH,&pDispatchColumns);
					if(res!=S_OK) {
						LOG_DEBUGWARNING(L"range.columns failed with code "<<res);
					}
					if(pDispatchColumns) {
						long colCount=0;
						res=_com_dispatch_raw_propget(pDispatchColumns,XLDISPID_COLUMNS_COUNT,VT_I4,&colCount);
						if(res!=S_OK) {
							LOG_DEBUGWARNING(L"columns.count failed with code "<<res);
						}
						if(colCount>0) {
							CComPtr<IDispatch> pDispatchLastColumn=nullptr;
							res=_com_dispatch_raw_method(pDispatchColumns,XLDISPID_COLUMNS_ITEM,DISPATCH_PROPERTYGET,VT_DISPATCH,&pDispatchLastColumn,L"\x0003",colCount);
							if(res!=S_OK) {
								LOG_DEBUGWARNING(L"columns.item "<<colCount<<L" failed with code "<<res);
							}
							if(pDispatchLastColumn) {
								res=_com_dispatch_raw_propget(pDispatchLastColumn,XLDISPID_RANGE_NEXT,VT_DISPATCH,&pDispatchNextCell);
								if(res!=S_OK) {
									LOG_DEBUGWARNING(L"range.next failed with code "<<res);
								}
							}
						}
					}
				}
				if(rangeWidth==0) { // could not get width from a merge area
					res=_com_dispatch_raw_propget(pDispatchRange,XLDISPID_RANGE_WIDTH,VT_I4,&rangeWidth);
					if(res!=S_OK) {
						LOG_DEBUGWARNING(L"range.width failed with code "<<res);
					}
				}
				if(textWidth>rangeWidth) {
					if(!pDispatchNextCell) {
						res=_com_dispatch_raw_propget(pDispatchRange,XLDISPID_RANGE_NEXT,VT_DISPATCH,&pDispatchNextCell);
						if(res!=S_OK) {
							LOG_DEBUGWARNING(L"range.next failed with code "<<res);
						}
					}
					if(pDispatchNextCell) {
						CComBSTR text;
						res=_com_dispatch_raw_propget(pDispatchNextCell,XLDISPID_RANGE_TEXT,VT_BSTR,&text);
						if(res!=S_OK) {
							LOG_DEBUGWARNING(L"range.text failed with code "<<res);
						}
						if(text&&text.Length()>0) {
							states+=STATE_CROPPED;
						}
					}
					if(!(states&STATE_CROPPED)) {
						states+=STATE_OVERFLOWING;
					}
				}
			}
		}
	}
	return states;
}

error_status_t nvdaInProcUtils_excel_getCellInfo(handle_t bindingHandle, const unsigned long windowHandle, IDispatch* arg_pDispatchRange, EXCEL_CELLINFO* cellInfo) {
	// DEFAULTS
	HWND hwnd=static_cast<HWND>(UlongToHandle(windowHandle));
	long threadID=GetWindowThreadProcessId(hwnd,nullptr);
	nvCOMUtils::InterfaceMarshaller im;
	HRESULT res=im.marshal(arg_pDispatchRange);
	if(res!=S_OK) {
		LOG_ERROR(L"Failed to marshal range object from rpc thread");
		return E_UNEXPECTED;
	}
	// Execute the following code in Excel's GUI thread. 
	execInThread(threadID,[&](){
		// Unmarshal the IDispatch pointer from the COM global interface table.
		CComPtr<IDispatch> pDispatchRange=im.unmarshal<IDispatch>();
		if(!pDispatchRange) {
			LOG_ERROR(L"Failed to unmarshal range object into Excel GUI thread");
			return;
		}
		res=_com_dispatch_raw_propget(pDispatchRange,XLDISPID_RANGE_TEXT,VT_BSTR,&cellInfo->text);
		if(res!=S_OK) {
			LOG_DEBUGWARNING(L"range.text failed with code "<<res);
		}
		CComPtr<IDispatch> pDispatchValidation=nullptr;
		res=_com_dispatch_raw_propget(pDispatchRange,XLDISPID_RANGE_VALIDATION,VT_DISPATCH,&pDispatchValidation);
		if(res!=S_OK) {
			LOG_DEBUGWARNING(L"range.validation failed with code "<<res);
		}
		if(pDispatchValidation) {
			_com_dispatch_raw_propget(pDispatchValidation,XLDISPID_VALIDATION_INPUTTITLE,VT_BSTR,&cellInfo->inputTitle);
			_com_dispatch_raw_propget(pDispatchValidation,XLDISPID_VALIDATION_INPUTMESSAGE,VT_BSTR,&cellInfo->inputMessage);
		}
		cellInfo->states=getCellStates(hwnd,pDispatchRange);
		_com_dispatch_raw_propget(pDispatchRange,XLDISPID_RANGE_ROW,VT_I4,&cellInfo->rowNumber);
		_com_dispatch_raw_propget(pDispatchRange,XLDISPID_RANGE_COLUMN,VT_I4,&cellInfo->columnNumber);
		CComPtr<IDispatch> pDispatchMergeArea=nullptr;
		_com_dispatch_raw_propget(pDispatchRange,XLDISPID_RANGE_MERGEAREA,VT_DISPATCH,&pDispatchMergeArea);
		if(pDispatchMergeArea) {
			_com_dispatch_raw_method(pDispatchMergeArea,XLDISPID_RANGE_ADDRESS,DISPATCH_PROPERTYGET,VT_BSTR,&cellInfo->address,L"\x000b\x000b\x0003\x000b",false,false,1,true);
			CComPtr<IDispatch> pDispatchRows=nullptr;
			_com_dispatch_raw_propget(pDispatchMergeArea,XLDISPID_RANGE_ROWS,VT_DISPATCH,&pDispatchRows);
			if(pDispatchRows) {
				_com_dispatch_raw_propget(pDispatchRows,XLDISPID_ROWS_COUNT,VT_I4,&cellInfo->rowSpan);
			}
			CComPtr<IDispatch> pDispatchColumns=nullptr;
			_com_dispatch_raw_propget(pDispatchMergeArea,XLDISPID_RANGE_COLUMNS,VT_DISPATCH,&pDispatchColumns);
			if(pDispatchColumns) {
				_com_dispatch_raw_propget(pDispatchColumns,XLDISPID_COLUMNS_COUNT,VT_I4,&cellInfo->columnSpan);
			}
		} else { // no merge area
			_com_dispatch_raw_method(pDispatchRange,XLDISPID_RANGE_ADDRESS,DISPATCH_PROPERTYGET,VT_BSTR,&cellInfo->address,L"\x000b\x000b\x0003\x000b",false,false,1,true);
		}
		CComPtr<IDispatch> pDispatchRow=nullptr;
		_com_dispatch_raw_propget(pDispatchRange,XLDISPID_RANGE_ENTIREROW,VT_DISPATCH,&pDispatchRow);
		if(pDispatchRow) {
			_com_dispatch_raw_propget(pDispatchRow,XLDISPID_ROW_OUTLINELEVEL,VT_I4,&cellInfo->outlineLevel);
		}
		if(cellInfo->outlineLevel==0) {
			CComPtr<IDispatch> pDispatchColumn=nullptr;
			_com_dispatch_raw_propget(pDispatchRange,XLDISPID_RANGE_ENTIRECOLUMN,VT_DISPATCH,&pDispatchColumn);
			if(pDispatchColumn) {
				_com_dispatch_raw_propget(pDispatchColumn,XLDISPID_COLUMN_OUTLINELEVEL,VT_I4,&cellInfo->outlineLevel);
			}
		}
	});
	return RPC_S_OK;
}
