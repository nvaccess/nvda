#include <string>
#include <map>
#include "displayModelRemote.h"
#include "gdiHooks.h"

using namespace std;

BOOL CALLBACK EnumChildWindowsProc(HWND hwnd, LPARAM lParam) {
	((deque<HWND>*)lParam)->push_back(hwnd);
	return TRUE;
}

error_status_t displayModelRemote_getWindowTextInRect(handle_t bindingHandle, const long windowHandle, const int left, const int top, const int right, const int bottom, BSTR* textBuf, BSTR* characterPointsBuf) {
	const HWND hwnd=(HWND)windowHandle;
	deque<HWND> windowDeque;
	EnumChildWindows(hwnd,EnumChildWindowsProc,(LPARAM)&windowDeque);
	windowDeque.push_back(hwnd);
	displayModel_t tempModel;
	RECT textRect={left,top,right,bottom};
	RECT curWindowRect;
	for(deque<HWND>::reverse_iterator i=windowDeque.rbegin();i!=windowDeque.rend();i++) {
		GetWindowRect(*i,&curWindowRect);
		//tempModel.clearRectangle(curWindowRect);
		displayModelsByWindow_t::iterator j=displayModelsByWindow.find(*i);
		if(j!=displayModelsByWindow.end()) {
			j->second->copyRectangleToOtherModel(textRect,&tempModel,FALSE,textRect.left,textRect.top);
		}
	}
	wstring text;
	deque<POINT> characterPoints;
	tempModel.renderText(&textRect,text,characterPoints);
	*textBuf=SysAllocString(text.c_str());
	size_t cpBufSize=characterPoints.size()*2;
	// Hackishly use a BSTR to contain points.
	wchar_t* cpTempBuf=(wchar_t*)malloc(cpBufSize*sizeof(wchar_t));
	wchar_t* cpTempBufIt=cpTempBuf;
	for(deque<POINT>::const_iterator cpIt=characterPoints.begin();cpIt!=characterPoints.end();cpIt++) {
		*(cpTempBufIt++)=(wchar_t)cpIt->x;
		*(cpTempBufIt++)=(wchar_t)cpIt->y;
	}
	*characterPointsBuf=SysAllocStringLen(cpTempBuf,cpBufSize);
	free(cpTempBuf);
	return 0;
}
