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

#include <comdef.h>
#include <windows.h>
#include <oleacc.h>
#include "log.h"
#include "nvdaHelperRemote.h"
#include "winword.h"

#define DISPID_APPLICATION_SELECTION 5
#define DISPID_APPLICATION_SCREENUPDATING 26
#define DISPID_SELECTION_RANGE 400
#define DISPID_RANGE_APPLICATION 1000
#define DISPID_RANGE_EXPAND 129
#define DISPID_RANGE_SELECT 65535
#define DISPID_RANGE_SETRANGE 100
#define DISPID_RANGE_START 3
#define DISPID_RANGE_END 4

#define wdLine 5

UINT wm_winword_expandToLine=0;

LRESULT CALLBACK winword_callWndProcHook(int code, WPARAM wParam, LPARAM lParam) {
	CWPSTRUCT* pcwp=(CWPSTRUCT*)lParam;
	if(pcwp->message==wm_winword_expandToLine) {
		//Fetch all needed objects
		IDispatchPtr pDispatchRange=NULL;
		if(ObjectFromLresult(pcwp->wParam,IID_IDispatch,0,(void**)&pDispatchRange)!=S_OK) {
			LOG_DEBUGWARNING(L"ObjectFromLresult failed");
			return 0;
		}
		IDispatchPtr pDispatchApplication=NULL;
		if(_com_dispatch_propget(pDispatchRange,DISPID_RANGE_APPLICATION,VT_DISPATCH,&pDispatchApplication)!=S_OK) {
			LOG_DEBUGWARNING(L"range.application failed");
			return 0;
		}
		IDispatchPtr pDispatchSelection=NULL;
		if(_com_dispatch_propget(pDispatchApplication,DISPID_APPLICATION_SELECTION,VT_DISPATCH,&pDispatchSelection)!=S_OK) {
			LOG_DEBUGWARNING(L"application.selection failed");
			return 0;
		}
		IDispatch* pDispatchOldSelRange=NULL;
		if(_com_dispatch_propget(pDispatchSelection,DISPID_SELECTION_RANGE,VT_DISPATCH,&pDispatchOldSelRange)!=S_OK) {
			LOG_DEBUGWARNING(L"selection.range failed");
			return 0;
		}
		//Disable screen updating as we will be moving the selection temporarily
		_com_dispatch_propput(pDispatchApplication,DISPID_APPLICATION_SCREENUPDATING,VT_BOOL,false);
		//Move the selection to the given range
		_com_dispatch_method(pDispatchRange,DISPID_RANGE_SELECT,DISPATCH_METHOD,VT_EMPTY,NULL,NULL);
		//Expand the selection to the line
		_com_dispatch_method(pDispatchSelection,DISPID_RANGE_EXPAND,DISPATCH_METHOD,VT_EMPTY,NULL,L"\x0003",wdLine);
		//Collect the start and end offsets of the selection
		long start=0;
		_com_dispatch_propget(pDispatchSelection,DISPID_RANGE_START,VT_I4,&start);
		long end=0;
		_com_dispatch_propget(pDispatchSelection,DISPID_RANGE_END,VT_I4,&end);
		//Update the range with the found line offsets from the selection
		_com_dispatch_method(pDispatchRange,DISPID_RANGE_SETRANGE,DISPATCH_METHOD,VT_EMPTY,NULL,L"\x0003\x0003",start,end);
		//Move the selection back to its original location
		_com_dispatch_method(pDispatchOldSelRange,DISPID_RANGE_SELECT,DISPATCH_METHOD,VT_EMPTY,NULL,NULL);
		//Reenable screen updating
		_com_dispatch_propput(pDispatchApplication,DISPID_APPLICATION_SCREENUPDATING,VT_BOOL,true);
	}
	return 0;
}

void winword_inProcess_initialize() {
	wm_winword_expandToLine=RegisterWindowMessage(L"wm_winword_expandToLine");
	registerWindowsHook(WH_CALLWNDPROC,winword_callWndProcHook);
}

void winword_inProcess_terminate() {
	unregisterWindowsHook(WH_CALLWNDPROC,winword_callWndProcHook);
}
