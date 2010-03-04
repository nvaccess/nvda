#include <cassert>
#include <map>
#include <windows.h>
#include <usp10.h>
#include "apiHook.h"
#include "displayModel.h"
#include <common/log.h>
#include "nvdaControllerInternal.h"
#include "gdiHooks.h"

using namespace std;

displayModelsByWindow_t displayModelsByWindow;
CRITICAL_SECTION criticalSection_displayModelsByWindow;
BOOL allowDisplayModelsByWindow=FALSE;

/**
 * Fetches and or creates a new displayModel for the window of the given device context.
 * If this function returns a displayModel, you must call releaseDisplayModel when finished with it.
 * @param hdc a handle of the device context who's window the displayModel is for.
 * @return a pointer to the  new/existing displayModel, NULL if gdiHooks is not initialized or has been terminated. 
 */
inline displayModel_t* acquireDisplayModel(HDC hdc) {
	HWND hwnd=WindowFromDC(hdc);
	if(hwnd==NULL) return NULL;
	LOG_DEBUG(L"window from DC is "<<hwnd);
	EnterCriticalSection(&criticalSection_displayModelsByWindow);
	if(!allowDisplayModelsByWindow) {
		LeaveCriticalSection(&criticalSection_displayModelsByWindow);
		return NULL;
	}
	displayModelsByWindow_t::iterator i=displayModelsByWindow.find(hwnd);
	displayModel_t* model=NULL;
	if(i!=displayModelsByWindow.end()) {
		model=i->second;
	} else {
		model=new displayModel_t();
		displayModelsByWindow.insert(make_pair(hwnd,model));
	}
	return model;
}

/**
 * Tells gdiHooks that you are finished with the given displayModel. It is very important that you call releaseDisplayModel for every call to acquireDisplayModel.
 * @param a pointer to the displayModel to release.
 */
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

typedef struct {
	HDC hdc;
	const void* pString;
	int cString;
	int iCharset;
} ScriptStringAnalyseArgs_t;

typedef map<SCRIPT_STRING_ANALYSIS,ScriptStringAnalyseArgs_t> ScriptStringAnalyseArgsByAnalysis_t;
ScriptStringAnalyseArgsByAnalysis_t ScriptStringAnalyseArgsByAnalysis;
CRITICAL_SECTION criticalSection_ScriptStringAnalyseArgsByAnalysis;
BOOL allowScriptStringAnalyseArgsByAnalysis=FALSE;

typedef HRESULT(WINAPI *ScriptStringAnalyse_funcType)(HDC,const void*,int,int,int,DWORD,int,SCRIPT_CONTROL*,SCRIPT_STATE*,const int*,SCRIPT_TABDEF*,const BYTE*,SCRIPT_STRING_ANALYSIS*);
ScriptStringAnalyse_funcType real_ScriptStringAnalyse=NULL;
HRESULT WINAPI fake_ScriptStringAnalyse(HDC hdc,const void* pString, int cString, int cGlyphs, int iCharset, DWORD dwFlags, int iRectWidth, SCRIPT_CONTROL* psControl, SCRIPT_STATE* psState, const int* piDx, SCRIPT_TABDEF* pTabdef, const BYTE* pbInClass, SCRIPT_STRING_ANALYSIS* pssa) {
	HRESULT res=real_ScriptStringAnalyse(hdc,pString,cString,cGlyphs,iCharset,dwFlags,iRectWidth,psControl,psState,piDx,pTabdef,pbInClass,pssa);
	if(res==S_OK&&pssa&&allowScriptStringAnalyseArgsByAnalysis) {
		EnterCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
		ScriptStringAnalyseArgs_t args={hdc,pString,cString,iCharset};
		ScriptStringAnalyseArgsByAnalysis[*pssa]=args;
		LeaveCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
	}
	return res;
}

typedef HRESULT(WINAPI *ScriptStringFree_funcType)(SCRIPT_STRING_ANALYSIS*);
ScriptStringFree_funcType real_ScriptStringFree=NULL;
HRESULT WINAPI fake_ScriptStringFree(SCRIPT_STRING_ANALYSIS* pssa) {
	HRESULT res=real_ScriptStringFree(pssa);
	if(res==S_OK&&pssa&&allowScriptStringAnalyseArgsByAnalysis) {
		EnterCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
		ScriptStringAnalyseArgsByAnalysis.erase(*pssa);
		LeaveCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
	}
	return res; 
}

typedef HRESULT(WINAPI *ScriptStringOut_funcType)(SCRIPT_STRING_ANALYSIS,int,int,UINT,const RECT*,int,int,BOOL);
ScriptStringOut_funcType real_ScriptStringOut=NULL;
HRESULT WINAPI fake_ScriptStringOut(SCRIPT_STRING_ANALYSIS ssa,int iX,int iY,UINT uOptions,const RECT *prc,int iMinSel,int iMaxSel,BOOL fDisabled) {
	HRESULT res=real_ScriptStringOut(ssa,iX,iY,uOptions,prc,iMinSel,iMaxSel,fDisabled);
	if(res==S_OK&&allowScriptStringAnalyseArgsByAnalysis) {
		EnterCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
		ScriptStringAnalyseArgsByAnalysis_t::iterator i=ScriptStringAnalyseArgsByAnalysis.find(ssa);
		if(i!=ScriptStringAnalyseArgsByAnalysis.end()&&i->second.iCharset==-1) {
			displayModel_t* model=acquireDisplayModel(i->second.hdc);
			if(model) {
				ExtTextOutWHelper(model,i->second.hdc,iX,iY,prc,uOptions,(wchar_t*)(i->second.pString),i->second.cString);
				releaseDisplayModel(model);
			}
		}
		LeaveCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
	}
	return res;
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
		displayModelsByWindow_t::iterator i=displayModelsByWindow.find(hwnd);
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
	InitializeCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
	allowScriptStringAnalyseArgsByAnalysis=TRUE;
	real_DestroyWindow=(DestroyWindow_funcType)apiHook_hookFunction("USER32.dll","DestroyWindow",fake_DestroyWindow);
	real_ExtTextOutW=(ExtTextOutW_funcType)apiHook_hookFunction("GDI32.dll","ExtTextOutW",fake_ExtTextOutW);
	real_ScriptStringAnalyse=(ScriptStringAnalyse_funcType)apiHook_hookFunction("USP10.dll","ScriptStringAnalyse",fake_ScriptStringAnalyse);
	real_ScriptStringFree=(ScriptStringFree_funcType)apiHook_hookFunction("USP10.dll","ScriptStringFree",fake_ScriptStringFree);
	real_ScriptStringOut=(ScriptStringOut_funcType)apiHook_hookFunction("USP10.dll","ScriptStringOut",fake_ScriptStringOut);
}

void gdiHooks_inProcess_terminate() {
	apiHook_unhookFunction("USER32.dll","DestroyWindow");
	apiHook_unhookFunction("GDI32.dll","ExtTextOutW");
	apiHook_unhookFunction("USP10.dll","ScriptStringAnalyse");
	apiHook_unhookFunction("USP10.dll","ScriptStringFree");
	apiHook_unhookFunction("USP10.dll","ScriptStringOut");
	EnterCriticalSection(&criticalSection_displayModelsByWindow);
	allowDisplayModelsByWindow=FALSE;
	displayModelsByWindow_t::iterator i=displayModelsByWindow.begin();
	while(i!=displayModelsByWindow.end()) {
		delete i->second;
		displayModelsByWindow.erase(i++);
	}  
	DeleteCriticalSection(&criticalSection_displayModelsByWindow);
	EnterCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
	allowScriptStringAnalyseArgsByAnalysis=FALSE;
	ScriptStringAnalyseArgsByAnalysis.clear();
	DeleteCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
}
