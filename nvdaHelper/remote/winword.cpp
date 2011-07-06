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
#include "nvdaInProcUtils.h"
#include "nvdaInProcUtils.h"
#include "winword.h"

#define DISPID_WINDOW_APPLICATION 1000
#define DISPID_APPLICATION_SELECTION 5
#define DISPID_APPLICATION_SCREENUPDATING 26
#define DISPID_SELECTION_RANGE 400
#define DISPID_SELECTION_SETRANGE 100
#define DISPID_RANGE_EXPAND 129
#define DISPID_RANGE_SELECT 65535
#define DISPID_RANGE_START 3
#define DISPID_RANGE_END 4

#define wdLine 5

UINT wm_winword_expandToLine=0;

typedef struct {
	int offset;
	int lineStart;
	int lineEnd;
} winword_expandToLine_args;

LRESULT CALLBACK winword_callWndProcHook(int code, WPARAM wParam, LPARAM lParam) {
	CWPSTRUCT* pcwp=(CWPSTRUCT*)lParam;
	if(pcwp->message==wm_winword_expandToLine) {
		winword_expandToLine_args* args=reinterpret_cast<winword_expandToLine_args*>(pcwp->wParam);
		//Fetch all needed objects
		IDispatchPtr pDispatchWindow=NULL;
		if(AccessibleObjectFromWindow(pcwp->hwnd,OBJID_NATIVEOM,IID_IDispatch,(void**)&pDispatchWindow)!=S_OK) {
			LOG_DEBUGWARNING(L"AccessibleObjectFromWindow failed");
			return 0;
		}
		IDispatchPtr pDispatchApplication=NULL;
		if(_com_dispatch_propget(pDispatchWindow,DISPID_WINDOW_APPLICATION,VT_DISPATCH,&pDispatchApplication)!=S_OK) {
			LOG_DEBUGWARNING(L"window.application failed");
			return 0;
		}
		IDispatchPtr pDispatchSelection=NULL;
		if(_com_dispatch_propget(pDispatchApplication,DISPID_APPLICATION_SELECTION,VT_DISPATCH,&pDispatchSelection)!=S_OK||!pDispatchSelection) {
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

void winword_inProcess_initialize() {
	wm_winword_expandToLine=RegisterWindowMessage(L"wm_winword_expandToLine");
	registerWindowsHook(WH_CALLWNDPROC,winword_callWndProcHook);
}

void winword_inProcess_terminate() {
	unregisterWindowsHook(WH_CALLWNDPROC,winword_callWndProcHook);
}
