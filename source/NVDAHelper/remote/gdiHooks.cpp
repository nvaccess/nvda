#include <cassert>
#include <map>
#include <windows.h>
#include "apiHook.h"
#include "displayModel.h"

using namespace std;

map<HWND,displayModel_t> displayModelsByWindow;

typedef BOOL(__stdcall *TextOutW_funcType)(HDC,int,int,wchar_t*,int);
TextOutW_funcType real_TextOutW;
BOOL __stdcall fake_TextOutW(HDC hdc, int x, int y, wchar_t* lpString, int cbCount) {
	HWND hwnd=WindowFromDC(hdc);
	if(lpString&&cbCount>0&&hwnd) {
		displayModel_t& model=displayModelsByWindow[hwnd];
		SIZE textSize;
		GetTextExtentPoint32(hdc,lpString,cbCount,&textSize);
		RECT textRect={x,y,x+textSize.cx,y+textSize.cy};
		//model.clearRectangle(textRect);
		wchar_t* newText=(wchar_t*)malloc(sizeof(wchar_t)*(cbCount+1));
		for(int i=0;i<cbCount;i++) {
			newText[i]=lpString[i];
		}
		newText[cbCount]=L'\0';
		model.insertChunk(textRect,newText);
		free(newText);
	}
	return real_TextOutW(hdc,x,y,lpString,cbCount);
}

typedef BOOL(__stdcall *ExtTextOutW_funcType)(HDC,int,int,UINT,const RECT*,wchar_t*,int,const int*);
ExtTextOutW_funcType real_ExtTextOutW;
BOOL __stdcall fake_ExtTextOutW(HDC hdc, int x, int y, UINT fuOptions, const RECT* lprc, wchar_t* lpString, int cbCount, const int* lpDx) {
	HWND hwnd=WindowFromDC(hdc);
	if(lpString&&cbCount>0&&hwnd) {
		displayModel_t& model=displayModelsByWindow[hwnd];
		SIZE textSize;
		GetTextExtentPoint32(hdc,lpString,cbCount,&textSize);
		RECT textRect={x,y,x+textSize.cx,y+textSize.cy};
		//model.clearRectangle(textRect);
		wchar_t* newText=(wchar_t*)malloc(sizeof(wchar_t)*(cbCount+1));
		for(int i=0;i<cbCount;i++) {
			newText[i]=lpString[i];
		}
		newText[cbCount]=L'\0';
		model.insertChunk(textRect,newText);
		free(newText);
	}
	return real_ExtTextOutW(hdc,x,y,fuOptions,lprc,lpString,cbCount,lpDx);
}

void gdiHooks_inProcess_initialize() {
	real_TextOutW=(TextOutW_funcType)apiHook_hookFunction("GDI32.dll","TextOutW",fake_TextOutW);
	real_ExtTextOutW=(ExtTextOutW_funcType)apiHook_hookFunction("GDI32.dll","ExtTextOutW",fake_ExtTextOutW);
}

void gdiHooks_inProcess_terminate() {
	apiHook_unhookFunction("GDI32.dll","TextOutW");
	apiHook_unhookFunction("GDI32.dll","ExtTextOutW");
}
