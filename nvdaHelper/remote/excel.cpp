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

const long XLDISPID_RANGE_TEXT=138;
const long XLDISPID_RANGE_FONT=146;
const long XLDISPID_FONT_SIZE=104;
const long XLDISPID_FONT_BOLD=96;
const long XLDISPID_FONT_ITALIC=101;
const long XLDISPID_FONT_UNDERLINE=106;
const long XLDISPID_FONT_STRIKETHROUGH=105;
const long XLDISPID_FONT_NAME=110;
const long XLDISPID_RANGE_DISPLAYFORMAT=666;

error_status_t nvdaInProcUtils_excel_getCellTextWidth(handle_t bindingHandle, const unsigned long windowHandle, IDispatch* arg_pDispatchRange, long* width) {
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
		CComBSTR sText;
		_com_dispatch_raw_propget(pDispatchRange,XLDISPID_RANGE_TEXT,VT_BSTR,&sText);
		long textLength=sText?sText.Length():0;
		if(textLength==0) {
			*width=0;
			return;
		}
		CComPtr<IDispatch> pDispatchFont=nullptr;
		_com_dispatch_raw_propget(pDispatchRange,XLDISPID_RANGE_FONT,VT_DISPATCH,&pDispatchFont);
		if(!pDispatchFont) {
			LOG_ERROR(L"range.font failed");
			return;
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
		*width=sizl.cx;
		SelectObject(tempDC, hOldFont);
		DeleteObject(hFont);
		SelectObject(tempDC, hOldBmp);
		DeleteObject(hBmp);
		DeleteDC(tempDC);
	});
	return RPC_S_OK;
}
