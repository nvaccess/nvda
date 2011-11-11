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
#include <comdef.h>
#include <windows.h>
#include <oleacc.h>
#include "log.h"
#include "nvdaHelperRemote.h"
#include "nvdaInProcUtils.h"
#include "nvdaInProcUtils.h"
#include "winword.h"

using namespace std;

#define DISPID_DOCUMENT_RANGE 2000
#define DISPID_WINDOW_DOCUMENT 2
#define DISPID_WINDOW_APPLICATION 1000
#define DISPID_APPLICATION_SELECTION 5
#define DISPID_APPLICATION_SCREENUPDATING 26
#define DISPID_SELECTION_RANGE 400
#define DISPID_SELECTION_SETRANGE 100
#define DISPID_RANGE_MOVEEND 111
#define DISPID_RANGE_COLLAPSE 101
#define DISPID_RANGE_TEXT 0
#define DISPID_RANGE_EXPAND 129
#define DISPID_RANGE_SELECT 65535
#define DISPID_RANGE_START 3
#define DISPID_RANGE_END 4
#define DISPID_RANGE_INFORMATION 313
#define DISPID_RANGE_SPELLINGERRORS 316
#define DISPID_SPELLINGERRORS_COUNT 1

#define wdWord 2
#define wdLine 5
#define wdCharacterFormatting 13

#define wdCollapseEnd 0
#define wdCollapseStart 1

#define wdActiveEndAdjustedPageNumber 1
#define wdFirstCharacterLineNumber 10
#define wdWithInTable 12
#define wdStartOfRangeRowNumber 13
#define wdMaximumNumberOfRows 15
#define wdStartOfRangeColumnNumber 16
#define wdMaximumNumberOfColumns 18

UINT wm_winword_expandToLine=0;
typedef struct {
	int offset;
	int lineStart;
	int lineEnd;
} winword_expandToLine_args;
void winword_expandToLine_helper(HWND hwnd, winword_expandToLine_args* args) {
	//Fetch all needed objects
	IDispatchPtr pDispatchWindow=NULL;
	if(AccessibleObjectFromWindow(hwnd,OBJID_NATIVEOM,IID_IDispatch,(void**)&pDispatchWindow)!=S_OK) {
		LOG_DEBUGWARNING(L"AccessibleObjectFromWindow failed");
		return;
	}
	IDispatchPtr pDispatchApplication=NULL;
	if(_com_dispatch_propget(pDispatchWindow,DISPID_WINDOW_APPLICATION,VT_DISPATCH,&pDispatchApplication)!=S_OK) {
		LOG_DEBUGWARNING(L"window.application failed");
		return;
	}
	IDispatchPtr pDispatchSelection=NULL;
	if(_com_dispatch_propget(pDispatchApplication,DISPID_APPLICATION_SELECTION,VT_DISPATCH,&pDispatchSelection)!=S_OK||!pDispatchSelection) {
		LOG_DEBUGWARNING(L"application.selection failed");
		return;
	}
	IDispatch* pDispatchOldSelRange=NULL;
	if(_com_dispatch_propget(pDispatchSelection,DISPID_SELECTION_RANGE,VT_DISPATCH,&pDispatchOldSelRange)!=S_OK) {
		LOG_DEBUGWARNING(L"selection.range failed");
		return;
	}
	//Disable screen updating as we will be moving the selection temporarily
	_com_dispatch_propput(pDispatchApplication,DISPID_APPLICATION_SCREENUPDATING,VT_BOOL,false);
	//Move the selection to the given range
	_com_dispatch_method(pDispatchSelection,DISPID_SELECTION_SETRANGE,DISPATCH_METHOD,VT_EMPTY,NULL,L"\x0003\x0003",args->offset,args->offset);
	//Expand the selection to the line
	_com_dispatch_method(pDispatchSelection,DISPID_RANGE_EXPAND,DISPATCH_METHOD,VT_EMPTY,NULL,L"\x0003",wdLine);
	//Collect the start and end offsets of the selection
	_com_dispatch_propget(pDispatchSelection,DISPID_RANGE_START,VT_I4,&(args->lineStart));
	_com_dispatch_propget(pDispatchSelection,DISPID_RANGE_END,VT_I4,&(args->lineEnd));
	//Move the selection back to its original location
	_com_dispatch_method(pDispatchOldSelRange,DISPID_RANGE_SELECT,DISPATCH_METHOD,VT_EMPTY,NULL,NULL);
	//Reenable screen updating
	_com_dispatch_propput(pDispatchApplication,DISPID_APPLICATION_SCREENUPDATING,VT_BOOL,true);
}

void generateXMLAttribsForFormatting(IDispatch* pDispatchRange, wostringstream& s) {
	int iVal=0;
	_com_dispatch_method(pDispatchRange,DISPID_RANGE_INFORMATION,DISPATCH_PROPERTYGET,VT_I4,&iVal,L"\x0003",wdActiveEndAdjustedPageNumber);
	s<<L"page-number=\""<<iVal<<L"\" ";
	iVal=0;
	_com_dispatch_method(pDispatchRange,DISPID_RANGE_INFORMATION,DISPATCH_PROPERTYGET,VT_I4,&iVal,L"\x0003",wdFirstCharacterLineNumber);
	s<<L"line-number=\""<<iVal<<L"\" ";
	iVal=0;
	{
		IDispatchPtr pDispatchSpellingErrors=NULL;
		if(_com_dispatch_propget(pDispatchRange,DISPID_RANGE_SPELLINGERRORS,VT_DISPATCH,&pDispatchSpellingErrors)==S_OK&&pDispatchSpellingErrors) {
			_com_dispatch_propget(pDispatchSpellingErrors,DISPID_SPELLINGERRORS_COUNT,VT_I4,&iVal);
			if(iVal>0) {
				s<<L"invalid-spelling=\""<<iVal<<L"\" ";
			}
		}
	} 
}

UINT wm_winword_getTextInRange=0;
typedef struct {
	int startOffset;
	int endOffset;
	long flags;
	BSTR text;
} winword_getTextInRange_args;
void winword_getTextInRange_helper(HWND hwnd, winword_getTextInRange_args* args) {
	//Fetch all needed objects
	//Get the window object
	IDispatchPtr pDispatchWindow=NULL;
	if(AccessibleObjectFromWindow(hwnd,OBJID_NATIVEOM,IID_IDispatch,(void**)&pDispatchWindow)!=S_OK) {
		LOG_DEBUGWARNING(L"AccessibleObjectFromWindow failed");
		return;
	}
	//Get the active document for the window
	IDispatchPtr pDispatchDocument=NULL;
	if(_com_dispatch_propget(pDispatchWindow,DISPID_WINDOW_DOCUMENT,VT_DISPATCH,&pDispatchDocument)!=S_OK) {
		LOG_DEBUGWARNING(L"window.document failed");
		return;
	}
	//Create a range of the document using the given start and end offsets
	IDispatchPtr pDispatchRange=NULL;
	if(_com_dispatch_method(pDispatchDocument,DISPID_DOCUMENT_RANGE,DISPATCH_METHOD,VT_DISPATCH,&pDispatchRange,L"\x0003\x0003",args->startOffset,args->endOffset)!=S_OK) {
		LOG_DEBUGWARNING(L"document.range("<<(args->startOffset)<<L","<<(args->endOffset)<<L") failed");
		return;
	}
	//Start writing the output xml to a stringstream
	wostringstream s;
	s<<L"<control>";
	//Collapse the range
	_com_dispatch_method(pDispatchRange,DISPID_RANGE_COLLAPSE,DISPATCH_METHOD,VT_EMPTY,NULL,L"\x0003",wdCollapseStart);
	int chunkEndOffset=args->startOffset;
	int unitsMoved=0;
	BSTR text=NULL;
	//Walk the range from the given start to end by characterFormatting or word units
	//And grab any text and formatting and generate appropriate xml
	do {
		//Try moving
		//But if characterFormatting doesn't work, and word doesn't work, or no units were moved then break out of the loop
		if((
			_com_dispatch_method(pDispatchRange,DISPID_RANGE_MOVEEND,DISPATCH_METHOD,VT_I4,&unitsMoved,L"\x0003\x0003",wdCharacterFormatting,1)!=S_OK&&
			_com_dispatch_method(pDispatchRange,DISPID_RANGE_MOVEEND,DISPATCH_METHOD,VT_I4,&unitsMoved,L"\x0003\x0003",wdWord,1)!=S_OK
		)||unitsMoved<=0) {
			break;
		}
		_com_dispatch_propget(pDispatchRange,DISPID_RANGE_END,VT_I4,&chunkEndOffset);
		//Make sure  that the end is not past the requested end after the move
		if(chunkEndOffset>(args->endOffset)) {
			_com_dispatch_propput(pDispatchRange,DISPID_RANGE_END,VT_I4,args->endOffset);
			chunkEndOffset=args->endOffset;
		}
		s<<L"<text ";
		generateXMLAttribsForFormatting(pDispatchRange,s);
		s<<L">";
		_com_dispatch_propget(pDispatchRange,DISPID_RANGE_TEXT,VT_BSTR,&text);
		if(text) {
			s<<text;
			SysFreeString(text);
			text=NULL;
		}
		s<<L"</text>";
		_com_dispatch_method(pDispatchRange,DISPID_RANGE_COLLAPSE,DISPATCH_METHOD,VT_EMPTY,NULL,L"\x0003",wdCollapseEnd);
	} while(chunkEndOffset<(args->endOffset));
	s<<L"</control>";
	args->text=SysAllocString(s.str().c_str());
}

LRESULT CALLBACK winword_callWndProcHook(int code, WPARAM wParam, LPARAM lParam) {
	CWPSTRUCT* pcwp=(CWPSTRUCT*)lParam;
	if(pcwp->message==wm_winword_expandToLine) {
		winword_expandToLine_helper(pcwp->hwnd,reinterpret_cast<winword_expandToLine_args*>(pcwp->wParam));
	} else if(pcwp->message==wm_winword_getTextInRange) {
		winword_getTextInRange_helper(pcwp->hwnd,reinterpret_cast<winword_getTextInRange_args*>(pcwp->wParam));
		winword_expandToLine_helper(pcwp->hwnd,reinterpret_cast<winword_expandToLine_args*>(pcwp->wParam));
	}
	return 0;
}

error_status_t nvdaInProcUtils_winword_expandToLine(handle_t bindingHandle, const long windowHandle, const int offset, int* lineStart, int* lineEnd) {
	winword_expandToLine_args args={offset,3,4};
	DWORD_PTR wmRes=0;
	SendMessageTimeout((HWND)windowHandle,wm_winword_expandToLine,(WPARAM)&args,0,SMTO_ABORTIFHUNG,2000,&wmRes);
	*lineStart=args.lineStart;
	*lineEnd=args.lineEnd;
	return RPC_S_OK;
}

error_status_t nvdaInProcUtils_winword_getTextInRange(handle_t bindingHandle, const long windowHandle, const int startOffset, const int endOffset, const long flags, BSTR* text) { 
	winword_getTextInRange_args args={startOffset,endOffset,flags,NULL};
	DWORD_PTR wmRes=0;
	SendMessageTimeout((HWND)windowHandle,wm_winword_getTextInRange,(WPARAM)&args,0,SMTO_ABORTIFHUNG,2000,&wmRes);
	*text=args.text;
	return RPC_S_OK;
}

void winword_inProcess_initialize() {
	wm_winword_expandToLine=RegisterWindowMessage(L"wm_winword_expandToLine");
	wm_winword_getTextInRange=RegisterWindowMessage(L"wm_winword_getTextInRange");
	registerWindowsHook(WH_CALLWNDPROC,winword_callWndProcHook);
}

void winword_inProcess_terminate() {
	unregisterWindowsHook(WH_CALLWNDPROC,winword_callWndProcHook);
}
