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

#include <string>
#include <map>
#include "displayModelRemote.h"
#include "gdiHooks.h"

using namespace std;

BOOL CALLBACK EnumChildWindowsProc(HWND hwnd, LPARAM lParam) {
	((deque<HWND>*)lParam)->push_back(hwnd);
	return TRUE;
}

error_status_t displayModelRemote_getWindowTextInRect(handle_t bindingHandle, const long windowHandle, const int left, const int top, const int right, const int bottom, const int minHorizontalWhitespace, const int minVerticalWhitespace, BSTR* textBuf, BSTR* characterRectsBuf) {
	const HWND hwnd=(HWND)windowHandle;
	deque<HWND> windowDeque;
	EnumChildWindows(hwnd,EnumChildWindowsProc,(LPARAM)&windowDeque);
	windowDeque.push_back(hwnd);
	displayModel_t* tempModel=new displayModel_t;
	RECT textRect={left,top,right,bottom};
	for(deque<HWND>::reverse_iterator i=windowDeque.rbegin();i!=windowDeque.rend();i++) {
		displayModelsByWindow.acquire();
		displayModelsMap_t<HWND>::iterator j=displayModelsByWindow.find(*i);
		if(j!=displayModelsByWindow.end()) {
			j->second->acquire();
			j->second->copyRectangleToOtherModel(textRect,tempModel,FALSE,textRect.left,textRect.top);
			j->second->release();
		}
		displayModelsByWindow.release();
	}
	wstring text;
	deque<RECT> characterRects;
	tempModel->renderText(textRect,minHorizontalWhitespace,minVerticalWhitespace,text,characterRects);
	tempModel->requestDelete();
	*textBuf=SysAllocStringLen(text.c_str(),text.size());
	size_t cpBufSize=characterRects.size()*4;
	// Hackishly use a BSTR to contain points.
	wchar_t* cpTempBuf=(wchar_t*)malloc(cpBufSize*sizeof(wchar_t));
	wchar_t* cpTempBufIt=cpTempBuf;
	for(deque<RECT>::const_iterator cpIt=characterRects.begin();cpIt!=characterRects.end();cpIt++) {
		*(cpTempBufIt++)=(wchar_t)cpIt->left;
		*(cpTempBufIt++)=(wchar_t)cpIt->top;
		*(cpTempBufIt++)=(wchar_t)cpIt->right;
		*(cpTempBufIt++)=(wchar_t)cpIt->bottom;
	}
	*characterRectsBuf=SysAllocStringLen(cpTempBuf,cpBufSize);
	free(cpTempBuf);
	return 0;
}
