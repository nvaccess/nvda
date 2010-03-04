#include <cassert>
#include <map>
#include <windows.h>
#include "apiHook.h"
#include "displayModel.h"
#include <common/log.h>
#include "nvdaControllerInternal.h"

using namespace std;

CRITICAL_SECTION criticalSection_displayModelsByWindow;
BOOL allowDisplayModelsByWindow=FALSE;
map<HWND,displayModel_t*> displayModelsByWindow;

inline displayModel_t* acquireDisplayModel(HDC hdc) {
	HWND hwnd=WindowFromDC(hdc);
	if(hwnd==NULL) return NULL;
	LOG_DEBUG(L"window from DC is "<<hwnd);
	EnterCriticalSection(&criticalSection_displayModelsByWindow);
	if(!allowDisplayModelsByWindow) {
		LeaveCriticalSection(&criticalSection_displayModelsByWindow);
		return NULL;
	}
	map<HWND,displayModel_t*>::iterator i=displayModelsByWindow.find(hwnd);
	displayModel_t* model=NULL;
	if(i!=displayModelsByWindow.end()) {
		model=i->second;
	} else {
		model=new displayModel_t();
		displayModelsByWindow.insert(make_pair(hwnd,model));
	}
	return model;
}

inline void releaseDisplayModel(displayModel_t* model) {
	LeaveCriticalSection(&criticalSection_displayModelsByWindow);
}

void ExtTextOutWHelper(displayModel_t* model, HDC hdc, int x, int y, const RECT* lprc,UINT fuOptions,wchar_t* lpString, int cbCount) {
	if(!lpString||cbCount==0) return;
	wstring newText(lpString,cbCount);
	//are we writing a transparent background?
	if(!(fuOptions&ETO_OPAQUE)&&(GetBkMode(hdc)==TRANSPARENT)) {
		//Find out if the text we're writing is just whitespace
		BOOL whitespace=TRUE;
		for(wstring::iterator i=newText.begin();i!=newText.end()&&(whitespace=iswspace(*i));i++);
		//Because the bacground is transparent, if the text is only whitespace, then return -- don't bother to record anything at all
		if(whitespace) return;
	}
	SIZE textSize;
	GetTextExtentPoint32(hdc,lpString,cbCount,&textSize);
	int xOffset=x;
	int yOffset=y;
	int textAlign=GetTextAlign(hdc);
	if(textAlign&TA_UPDATECP) {
		POINT curPos;
		GetCurrentPositionEx(hdc,&curPos);
		xOffset=curPos.x;
		yOffset=curPos.y;
		LOG_DEBUG(L"TA_UPDATECP set");
	}
	if(textAlign&TA_CENTER) {
		LOG_DEBUG(L"TA_CENTER set");
		xOffset-=(textSize.cx/2);
	} else if(textAlign&TA_RIGHT) {
		LOG_DEBUG(L"TA_RIGHT set");
		xOffset-=textSize.cx;
	}
	if(textAlign&TA_BOTTOM) {
		LOG_DEBUG(L"TA_BOTTOM set");
		yOffset-=textSize.cy;
	}
	LOG_DEBUG(L"using offset of "<<xOffset<<L","<<yOffset);
	RECT textRect={xOffset,yOffset,xOffset+textSize.cx,yOffset+textSize.cy};
	LPtoDP(hdc,(LPPOINT)&textRect,2);
	RECT clearRect;
	if(lprc&&(fuOptions&ETO_OPAQUE)) {
		clearRect=*lprc;
		LPtoDP(hdc,(LPPOINT)&clearRect,2);
	} else {
		LOG_DEBUG(L"Clearing with text's rectangle");
		clearRect=textRect;
	}
	model->clearRectangle(clearRect);
	model->insertChunk(textRect,newText);
}

typedef BOOL(__stdcall *TextOutW_funcType)(HDC,int,int,wchar_t*,int);
TextOutW_funcType real_TextOutW;
BOOL __stdcall fake_TextOutW(HDC hdc, int x, int y, wchar_t* lpString, int cbCount) {
	displayModel_t* model=acquireDisplayModel(hdc);
	if(model) {
		ExtTextOutWHelper(model,hdc,x,y,NULL,0,lpString,cbCount);
		releaseDisplayModel(model);
	}
	return real_TextOutW(hdc,x,y,lpString,cbCount);
}

typedef BOOL(__stdcall *ExtTextOutW_funcType)(HDC,int,int,UINT,const RECT*,wchar_t*,int,const int*);
ExtTextOutW_funcType real_ExtTextOutW;
BOOL __stdcall fake_ExtTextOutW(HDC hdc, int x, int y, UINT fuOptions, const RECT* lprc, wchar_t* lpString, int cbCount, const int* lpDx) {
	if(!(fuOptions&ETO_GLYPH_INDEX)) {
		displayModel_t* model=acquireDisplayModel(hdc);
		if(model) {
			ExtTextOutWHelper(model,hdc,x,y,lprc,fuOptions,lpString,cbCount);
			releaseDisplayModel(model);
		}
	}
	return real_ExtTextOutW(hdc,x,y,fuOptions,lprc,lpString,cbCount,lpDx);
}

void DrawTextExWHelper(displayModel_t* model, HDC hdc, wchar_t* lpString, int cbCount, const RECT* lprc, UINT dwDTFormat, LPDRAWTEXTPARAMS lpDTParams) {
	if(cbCount==-1) cbCount=wcslen(lpString);
	wstring newText(lpString,cbCount);
	//are we writing a transparent background?
	if(GetBkMode(hdc)==TRANSPARENT) {
		//Find out if the text we're writing is just whitespace
		BOOL whitespace=TRUE;
		for(wstring::iterator i=newText.begin();i!=newText.end()&&(whitespace=iswspace(*i));i++);
		//Because the bacground is transparent, if the text is only whitespace, then return -- don't bother to record anything at all
		if(whitespace) return;
	}
	RECT textRect=*lprc;
	LPtoDP(hdc,(LPPOINT)&textRect,2);
	model->clearRectangle(textRect);
	model->insertChunk(textRect,newText);
}

typedef int(WINAPI *DrawTextW_funcType)(HDC,wchar_t*,int,const RECT*,UINT);
DrawTextW_funcType real_DrawTextW=NULL;
int WINAPI fake_DrawTextW(HDC hdc, wchar_t* lpString, int cbCount, const RECT* lprc, UINT dwDTFormat) {
	if(lpString&&(cbCount!=0)&&!(dwDTFormat&DT_CALCRECT)&&!(dwDTFormat&DT_PREFIXONLY)) {
		displayModel_t* model=acquireDisplayModel(hdc);
		if(model) {
			DrawTextExWHelper(model,hdc,lpString,cbCount,lprc,dwDTFormat,NULL);
			releaseDisplayModel(model);
		}
	}
	return real_DrawTextW(hdc,lpString,cbCount,lprc,dwDTFormat);
}

typedef int(WINAPI *DrawTextExW_funcType)(HDC,wchar_t*,int,const RECT*,UINT,LPDRAWTEXTPARAMS);
DrawTextExW_funcType real_DrawTextExW=NULL;
int WINAPI fake_DrawTextExW(HDC hdc, wchar_t* lpString, int cbCount, const RECT* lprc, UINT dwDTFormat, LPDRAWTEXTPARAMS lpDTParams) {
	if(lpString&&(cbCount!=0)&&!(dwDTFormat&DT_CALCRECT)&&!(dwDTFormat&DT_PREFIXONLY)) {
		displayModel_t* model=acquireDisplayModel(hdc);
		if(model) {
			DrawTextExWHelper(model,hdc,lpString,cbCount,lprc,dwDTFormat,lpDTParams);
			releaseDisplayModel(model);
		}
	}
	return real_DrawTextExW(hdc,lpString,cbCount,lprc,dwDTFormat,lpDTParams);
}

typedef BOOL(WINAPI *DestroyWindow_funcType)(HWND);
DestroyWindow_funcType real_DestroyWindow=NULL;
BOOL WINAPI fake_DestroyWindow(HWND hwnd) {
	BOOL res=real_DestroyWindow(hwnd);
	if(res) {
		EnterCriticalSection(&criticalSection_displayModelsByWindow);
		if(!allowDisplayModelsByWindow) {
			LeaveCriticalSection(&criticalSection_displayModelsByWindow);
			return res;
		}
		map<HWND,displayModel_t*>::iterator i=displayModelsByWindow.find(hwnd);
		if(i!=displayModelsByWindow.end()) {
			delete i->second;
			displayModelsByWindow.erase(i);
		}
		LeaveCriticalSection(&criticalSection_displayModelsByWindow);
	}
	return res;
}

void gdiHooks_inProcess_initialize() {
	InitializeCriticalSection(&criticalSection_displayModelsByWindow);
	allowDisplayModelsByWindow=TRUE;
	real_DestroyWindow=(DestroyWindow_funcType)apiHook_hookFunction("USER32.dll","DestroyWindow",fake_DestroyWindow);
	//real_TextOutW=(TextOutW_funcType)apiHook_hookFunction("GDI32.dll","TextOutW",fake_TextOutW);
	real_ExtTextOutW=(ExtTextOutW_funcType)apiHook_hookFunction("GDI32.dll","ExtTextOutW",fake_ExtTextOutW);
	//real_DrawTextW=(DrawTextW_funcType)apiHook_hookFunction("USER32.dll","DrawTextW",fake_DrawTextW);
	real_DrawTextExW=(DrawTextExW_funcType)apiHook_hookFunction("USER32.dll","DrawTextExW",fake_DrawTextExW);
}

void gdiHooks_inProcess_terminate() {
	apiHook_unhookFunction("GDI32.dll","TextOutW");
	apiHook_unhookFunction("GDI32.dll","ExtTextOutW");
	apiHook_unhookFunction("USER32.dll","DrawTextW");
	apiHook_unhookFunction("USER32.dll","DrawTextExW");
	apiHook_unhookFunction("USER32.dll","DestroyWindow");
	EnterCriticalSection(&criticalSection_displayModelsByWindow);
	allowDisplayModelsByWindow=FALSE;
	map<HWND,displayModel_t*>::iterator i=displayModelsByWindow.begin();
	while(i!=displayModelsByWindow.end()) {
		delete i->second;
		displayModelsByWindow.erase(i++);
	}  
	DeleteCriticalSection(&criticalSection_displayModelsByWindow);
}
