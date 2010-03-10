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

size_t WA_strlen(const char* str) {
	return strlen(str);
}

size_t WA_strlen(const wchar_t* str) {
	return wcslen(str);
}

char* WA_strncpy(char* dest, const char* source, size_t size) {
	return strncpy(dest,source,size);
}

wchar_t* WA_strncpy(wchar_t* dest, const wchar_t* source, size_t size) {
	return wcsncpy(dest,source,size);
}

BOOL WINAPI WA_GetTextExtentPoint32(HDC hdc, char* lpString, int cbCount, LPSIZE size) {
	return GetTextExtentPoint32A(hdc,lpString,cbCount,size);
}

BOOL WINAPI WA_GetTextExtentPoint32(HDC hdc, wchar_t* lpString, int cbCount, LPSIZE size) {
	return GetTextExtentPoint32W(hdc,lpString,cbCount,size);
}

typedef map<HDC,displayModel_t*> displayModelsByDC_t;
displayModelsByDC_t displayModelsByMemoryDC;
displayModelsByWindow_t displayModelsByWindow;
CRITICAL_SECTION criticalSection_displayModelMaps;
BOOL allow_displayModelMaps=FALSE;

/**
 * Fetches and or creates a new displayModel for the window of the given device context.
 * If this function returns a displayModel, you must call releaseDisplayModel when finished with it.
 * @param hdc a handle of the device context who's window the displayModel is for.
 * @param noCreate If true a display model will not be created if it does not exist. 
 * @return a pointer to the  new/existing displayModel, NULL if gdiHooks is not initialized or has been terminated. 
 */
inline displayModel_t* acquireDisplayModel(HDC hdc, BOOL noCreate=FALSE) {
	//If we are allowed, acquire use of the displayModel maps
	if(!allow_displayModelMaps) return NULL;
	EnterCriticalSection(&criticalSection_displayModelMaps);
	if(!allow_displayModelMaps) {
		LeaveCriticalSection(&criticalSection_displayModelMaps);
		return NULL;
	}
	displayModel_t* model=NULL;
	//If the DC has a window, then either get an existing displayModel using the window, or create a new one and store it by its window.
	//If  the DC does not have a window, try and get the displayModel from our existing Memory DC displayModels. 
	HWND hwnd=WindowFromDC(hdc);
	LOG_DEBUG(L"window from DC is "<<hwnd);
	if(hwnd) {
		displayModelsByWindow_t::iterator i=displayModelsByWindow.find(hwnd);
		if(i!=displayModelsByWindow.end()) {
			model=i->second;
		} else if(!noCreate) {
			model=new displayModel_t();
			displayModelsByWindow.insert(make_pair(hwnd,model));
		}
	} else {
		displayModelsByDC_t::iterator i=displayModelsByMemoryDC.find(hdc);
		if(i!=displayModelsByMemoryDC.end()) {
			model=i->second;
		}
	}
	if(model) model->AddRef();
	LeaveCriticalSection(&criticalSection_displayModelMaps);
	return model;
}

/**
 * Tells gdiHooks that you are finished with the given displayModel. It is very important that you call releaseDisplayModel for every call to acquireDisplayModel.
 * @param a pointer to the displayModel to release.
 */
inline void releaseDisplayModel(displayModel_t* model) {
	if(model) model->Release();
}

/**
 * Given a displayModel, this function clears a rectangle, and inserts a chunk, for the given text, using the given offsets and rectangle etc.
 * This function is used by many of the hook functions.
 * @param model a pointer to a displayModel
 * @param hdc a handle to the device context that was used to write the text originally.
 * @param x the x coordinate (in device units) where the text should start from (depending on textAlign flags, this could be the left, center, or right of the text).
 * @param y the y coordinate (in device units) where the text should start from (depending on textAlign flags, this could be the top, or bottom of the text).
 * @param textSize a pointer to the size of the text (its width and height).
 * @param lprc a pointer to the rectangle that should be cleared. If lprc is NULL, or ETO_OPAQUE is not in fuOptions, then only the rectangle bounding the text will be cleared.
 * @param fuOptions flags accepted by GDI32's ExtTextOut.
 * @param textAlign possible flags returned by GDI32's GetTextAlign.
 * @param lpString the string of unicode text you wish to record.
 * @param cbCount the length of the string in characters.
  */
void ExtTextOutHelper(displayModel_t* model, HDC hdc, int x, int y, const SIZE* textSize, const RECT* lprc,UINT fuOptions,UINT textAlign, BOOL stripHotkeyIndicator, wchar_t* lpString, int cbCount) {
	wstring newText(lpString,cbCount);
	if(fuOptions&ETO_GLYPH_INDEX) { //The string only contained glyphs, not characters, rather useless to us.
		newText=L"glyphs";
	}
	//are we writing a transparent background?
	if(!(fuOptions&ETO_OPAQUE)&&(GetBkMode(hdc)==TRANSPARENT)) {
		//Find out if the text we're writing is just whitespace
		BOOL whitespace=TRUE;
		for(wstring::iterator i=newText.begin();i!=newText.end()&&(whitespace=iswspace(*i));i++);
		//Because the bacground is transparent, if the text is only whitespace, then return -- don't bother to record anything at all
		if(whitespace) return;
	}
	//Search for and remove the first & symbol if we have been requested to stip hotkey indicator.
	if(stripHotkeyIndicator) {
		unsigned int pos=newText.find(L'&');
		if(pos!=wstring::npos) newText.erase(pos,1);
	}
	int xOffset=x;
	int yOffset=y;
	//Correct x and y depending on the text alignment
	if(textAlign&TA_CENTER) {
		LOG_DEBUG(L"TA_CENTER set");
		xOffset-=(textSize->cx/2);
	} else if(textAlign&TA_RIGHT) {
		LOG_DEBUG(L"TA_RIGHT set");
		xOffset-=textSize->cx;
	}
	if(textAlign&TA_BOTTOM) {
		LOG_DEBUG(L"TA_BOTTOM set");
		yOffset-=textSize->cy;
	}
	LOG_DEBUG(L"using offset of "<<xOffset<<L","<<yOffset);
	RECT textRect={xOffset,yOffset,xOffset+textSize->cx,yOffset+textSize->cy};
	//We must store chunks using device coordinates, not logical coordinates, as its possible for the DC's viewport to move or resize.
	//For example, in Windows 7, menu items are always drawn at the same DC coordinates, but the DC is moved downward each time.
	//Device coordinates for a window DC are screen pixels  with 0,0 being the top left of the window's client area.
	LPtoDP(hdc,(LPPOINT)&textRect,2);
	RECT clearRect;
	//If a clearing rectangle was provided we'll use it, otherwise we'll use the text's bounding rectangle.
	if(lprc&&(fuOptions&ETO_OPAQUE)) {
		clearRect=*lprc;
		LPtoDP(hdc,(LPPOINT)&clearRect,2);
	} else {
		LOG_DEBUG(L"Clearing with text's rectangle");
		clearRect=textRect;
	}
	//Update the displayModel.
	model->clearRectangle(clearRect);
	model->insertChunk(textRect,newText);
}

/**
 * an overload of ExtTextOutHelper to work with ansi strings.
 * @param lpString the string of ansi text you wish to record.
  */
void ExtTextOutHelper(displayModel_t* model, HDC hdc, int x, int y, const SIZE* textSize, const RECT* lprc,UINT fuOptions,UINT textAlign, BOOL stripHotkeyIndicator, char* lpString, int cbCount) {
	if(lpString&&cbCount) {
		int newCount=MultiByteToWideChar(CP_THREAD_ACP,0,lpString,cbCount,NULL,0);
		if(newCount>0) {
			wchar_t* newString=(wchar_t*)calloc(newCount+1,sizeof(wchar_t));
			MultiByteToWideChar(CP_THREAD_ACP,0,lpString,cbCount,newString,newCount);
			ExtTextOutHelper(model,hdc,x,y,textSize,lprc,fuOptions,textAlign,stripHotkeyIndicator,newString,newCount);
			free(newString);
		}
	}
}

//TextOut hook class template
//Handles char or wchar_t
template<typename charType> class hookClass_TextOut {
	public:
	typedef bool(WINAPI *funcType)(HDC,int,int, charType*,int);
	static funcType realFunction;
	static BOOL  WINAPI fakeFunction(HDC hdc, int x, int y, charType* lpString, int cbCount);
};

template<typename charType> typename hookClass_TextOut<charType>::funcType hookClass_TextOut<charType>::realFunction=NULL;

template<typename charType> BOOL  WINAPI hookClass_TextOut<charType>::fakeFunction(HDC hdc, int x, int y, charType* lpString, int cbCount) {
	displayModel_t* model=acquireDisplayModel(hdc);
	if(model) {
		//Calculate the size of the text
		SIZE textSize;
		WA_GetTextExtentPoint32(hdc,lpString,cbCount,&textSize);
		//TextOut can either provide  specific coordinates, or it can be instructed to use the DC's current position and also update it.
		//if  text alignment does state that the current position must be used, we need to get it before the real ExtTextOut is called, and we need to also update our x,y that we will use for recording the text.
		POINT pos={x,y};
		UINT textAlign=GetTextAlign(hdc);
		if(textAlign&TA_UPDATECP) GetCurrentPositionEx(hdc,&pos);
		ExtTextOutHelper(model,hdc,pos.x,pos.y,&textSize,NULL,0,textAlign,FALSE,lpString,cbCount);
		releaseDisplayModel(model);
	}
	return realFunction(hdc,x,y,lpString,cbCount);
}

//TabbedTextOut hook class template
template<typename charType> class hookClass_TabbedTextOut {
	public:
	typedef LONG (WINAPI *funcType)(HDC,int,int,charType*,int,int,const LPINT,int);
	static funcType realFunction;
	static LONG WINAPI fakeFunction(HDC hdc, int x, int y, charType* lpString, int nCount, int nTabPositions, const LPINT lpnTabStopPositions, int nTabOrigin);
};

template<typename charType> typename hookClass_TabbedTextOut<charType>::funcType hookClass_TabbedTextOut<charType>::realFunction=NULL;

template<typename charType> LONG WINAPI hookClass_TabbedTextOut<charType>::fakeFunction(HDC hdc, int x, int y, charType* lpString, int nCount, int nTabPositions, const LPINT lpnTabStopPositions, int nTabOrigin) {
	//Collect text alignment and possibly current position
	UINT textAlign=GetTextAlign(hdc);
	POINT pos={x,y};
	if(textAlign&TA_UPDATECP) GetCurrentPositionEx(hdc,&pos);
	//Call the real function
	LONG res=realFunction(hdc,x,y,lpString,nCount,nTabPositions,lpnTabStopPositions,nTabOrigin);
	//If text could not be drawn, or  some arguments are not sane, then stop here.
	if(res==0||!lpString||nCount==0) return res;
	//Get or create a display model for this DC.
	//If we can't then stop here.
	displayModel_t* model=acquireDisplayModel(hdc);
	if(!model) return res;
	//TabbedTextOut returns the size of the text it wrote in its result
	SIZE textSize={HIWORD(res),LOWORD(res)};
	//X and Y need to be in device units
	LPtoDP(hdc,&pos,1);
	//Record the text
	ExtTextOutHelper(model,hdc,pos.x,pos.y,&textSize,NULL,0,textAlign,FALSE,lpString,nCount);
	model->Release();
	return res;
}
 
//DrawTextEx hook class template
//handles char or wchar_t
template <typename charType> class hookClass_DrawTextEx {
	public:
	typedef int(WINAPI *funcType)(HDC,charType*,int,const RECT*,UINT,LPDRAWTEXTPARAMS);
	static funcType realFunction;
	static int WINAPI fakeFunction(HDC hdc, charType* lpString, int cbCount, const RECT* lprc, UINT dwDTFormat, LPDRAWTEXTPARAMS lpDTParams);
};

template<typename charType> typename hookClass_DrawTextEx<charType>::funcType hookClass_DrawTextEx<charType>::realFunction=NULL;

template<typename charType> int WINAPI hookClass_DrawTextEx<charType>::fakeFunction(HDC hdc, charType* lpString, int cbCount, const RECT* lprc, UINT dwDTFormat, LPDRAWTEXTPARAMS lpDTParams) {
	charType* newString=lpString;
	int newCount=cbCount;
	UINT newFormat=dwDTFormat;
	//DrawTextEx sometimes will trunkate text and places "..." after it. 
	//However its up to the caller whether DrawTextEx should actually modify the given string buffer.
	//Because of this, if the caller did not request this, allocate a new copy of the string, large enough for the extra characters
	//And instruct DrawTextEx to modify the string.
	if(lpString&&cbCount!=0&&!(dwDTFormat&DT_CALCRECT)&&!(dwDTFormat&DT_PREFIXONLY)&&!(dwDTFormat&DT_MODIFYSTRING)) {
		if(cbCount==-1) newCount=WA_strlen(lpString);
		newString=(charType*)calloc(newCount+6,sizeof(charType));
		WA_strncpy(newString,lpString,newCount);
		newFormat|=DT_MODIFYSTRING;
	}
	//Call the real DrawTextExW
	int res=((funcType)realFunction)(hdc,newString,newCount,lprc,newFormat,lpDTParams);
	//If the draw did not work, or the caller did not wish to actually draw the text, then stop here.
	if(res==0||newCount==0||(newFormat&DT_CALCRECT)||(newFormat&DT_PREFIXONLY)) {
		if(newString!=lpString) free(newString);
		return res;
	}
	//Get or create a display model for this DC
	displayModel_t* model=acquireDisplayModel(hdc);
	if(model) {
		//Not only does DrawTextEx trunkate the text, it can support tabs of different widths.
		//This makes calculating an accurate text size very hard.
		//For now, just assume the text size takes up the entire rectangle given by the caller, and say that the text starts from the top left.
		//This may not be the case -- depending on the text alignment, and if the text doesn't take up the whole rectangle.
		//But this will do for now.
		int x=lprc->left;
		int y=lprc->top;
		SIZE textSize={(lprc->right-lprc->left),(lprc->bottom-lprc->top)};
		//Record the text
		ExtTextOutHelper(model,hdc,x,y,&textSize,NULL,0,0,!(newFormat&DT_NOPREFIX),newString,newCount);
		//Release the model, cleanup and return
		releaseDisplayModel(model);
	}
	if(newString!=lpString) free(newString);
	return res; 
}

//ExtTextOut hook class template
//Handles char or wchar_t
template<typename charType> class hookClass_ExtTextOut {
	public:
	typedef BOOL(__stdcall *funcType)(HDC,int,int,UINT,const RECT*,charType*,int,const int*);
	static funcType realFunction;
	static BOOL __stdcall fakeFunction(HDC hdc, int x, int y, UINT fuOptions, const RECT* lprc, charType* lpString, int cbCount, const int* lpDx);
};

template<typename charType> typename hookClass_ExtTextOut<charType>::funcType hookClass_ExtTextOut<charType>::realFunction=NULL;

template<typename charType> BOOL __stdcall hookClass_ExtTextOut<charType>::fakeFunction(HDC hdc, int x, int y, UINT fuOptions, const RECT* lprc, charType* lpString, int cbCount, const int* lpDx) {
	//We can only record stuff if a proper string is provided (I.e. its not NULL and its not glyphs)
	if(lpString&&cbCount>0&&!(fuOptions&ETO_GLYPH_INDEX)) {
		//try to get or create a displayModel for this device context
		displayModel_t* model=acquireDisplayModel(hdc);
		if(model) {
			//Calculate the size of the text
			SIZE textSize;
			WA_GetTextExtentPoint32(hdc,lpString,cbCount,&textSize);
			//ExtTextOut can either provide  specific coordinates, or it can be instructed to use the DC's current position and also update it.
			//if  text alignment does state that the current position must be used, we need to get it before the real ExtTextOut is called, and we need to also update our x,y that we will use for recording the text.
			POINT pos={x,y};
			UINT textAlign=GetTextAlign(hdc);
			if(textAlign&TA_UPDATECP) GetCurrentPositionEx(hdc,&pos);
			//Record the text in the displayModel
			ExtTextOutHelper(model,hdc,pos.x,pos.y,&textSize,lprc,fuOptions,textAlign,FALSE,lpString,cbCount);
			//Release the displayModel we got
			releaseDisplayModel(model);
		}
	}
	//Call the real ExtTextOutW
	return realFunction(hdc,x,y,fuOptions,lprc,lpString,cbCount,lpDx);
}

//CreateCompatibleDC hook function
//Hooked so we know when a memory DC is created, as its possible that its contents may at some point be bit blitted back to a window DC (double buffering).
typedef HDC(WINAPI *CreateCompatibleDC_funcType)(HDC);
CreateCompatibleDC_funcType real_CreateCompatibleDC=NULL;
HDC WINAPI fake_CreateCompatibleDC(HDC hdc) {
	//Call the real CreateCompatibleDC
	HDC newHdc=real_CreateCompatibleDC(hdc);
	//If the creation was successful, and the DC that was used in the creation process is a window DC, 
	//we should create a displayModel for this DC so that text writes can be tracked in case  its ever bit blitted to a window DC. 
	//We also need to acquire access to the model maps while we do this
	if(allow_displayModelMaps&&newHdc&&hdc&&WindowFromDC(hdc)) {
		EnterCriticalSection(&criticalSection_displayModelMaps);
		if(!allow_displayModelMaps) {
			LeaveCriticalSection(&criticalSection_displayModelMaps);
			return newHdc;
		}
		displayModel_t* model=new displayModel_t();
		displayModelsByMemoryDC.insert(make_pair(newHdc,model));
		LeaveCriticalSection(&criticalSection_displayModelMaps);
	}
	return newHdc;
}

//DeleteDC hook function
//Hooked so we can get rid of any memory DC no longer needed by the application.
typedef BOOL(WINAPI *DeleteDC_funcType)(HDC);
DeleteDC_funcType real_DeleteDC=NULL;
BOOL WINAPI fake_DeleteDC(HDC hdc) {
	//Call the real DeleteDC
	BOOL res=real_DeleteDC(hdc);
	//If the DC was successfully deleted, we should remove  the displayModel we have for it, if it exists.
	//Acquire access to the display model maps while we do this.
	if(res&&allow_displayModelMaps) {
		EnterCriticalSection(&criticalSection_displayModelMaps);
		if(!allow_displayModelMaps) {
			LeaveCriticalSection(&criticalSection_displayModelMaps);
			return res;
		}
		displayModelsByDC_t::iterator i=displayModelsByMemoryDC.find(hdc);
		if(i!=displayModelsByMemoryDC.end()) {
			i->second->Release();
			displayModelsByMemoryDC.erase(i);
		}
		LeaveCriticalSection(&criticalSection_displayModelMaps);
	}
	return res;
}

//BitBlt hook function
//Hooked so we can tell when content from one DC is being copied (bit blitted) to another (most likely from a memory DC to a window DC). 
typedef BOOL(WINAPI *BitBlt_funcType)(HDC,int,int,int,int,HDC,int,int,DWORD);
BitBlt_funcType real_BitBlt=NULL;
BOOL WINAPI fake_BitBlt(HDC hdcDest, int nXDest, int nYDest, int nWidth, int nHeight, HDC hdcSrc, int nXSrc, int nYSrc, DWORD dwRop) {
	//Call the real BitBlt
	BOOL res=real_BitBlt(hdcDest,nXDest,nYDest,nWidth,nHeight,hdcSrc,nXSrc,nYSrc,dwRop);
	//If bit blit didn't work, or its not a simple copy, we don't want to know about it
	if(!res||(dwRop!=SRCCOPY)) return res;
	//If there is a source DC, then try getting a display model for it.
	displayModel_t* srcModel=NULL;
	if(hdcSrc) {
		srcModel=acquireDisplayModel(hdcSrc,TRUE);
		//If we got a model but it doesn't actually contain any chunks, its no use in bit blitting.
		if(srcModel&&srcModel->getChunkCount()==0) {
			srcModel->Release();
			srcModel=NULL;
		}
		if(!srcModel) return res;
	}
	//Get or create a display model from the destination DC
	displayModel_t* destModel=acquireDisplayModel(hdcDest);
	if(destModel) {
		//If we still have no source model, its because a source DC was not given.
		//This tells us we should use the destination model as both the source and destination.
		if(!srcModel) srcModel=destModel;
		RECT srcRect={nXSrc,nYSrc,nXSrc+nWidth,nYSrc+nHeight};
		//we record chunks using device coordinates -- DCs can move/resize
		LPtoDP(hdcSrc,(LPPOINT)&srcRect,2);
		POINT destPos={nXDest,nYDest};
		LPtoDP(hdcDest,&destPos,1);
		//Copy the requested rectangle from the source model in to the destination model, at the given coordinates.
		srcModel->copyRectangleToOtherModel(srcRect,destModel,destPos.x,destPos.y);
		//release models and return
		destModel->Release();
	}
	if(srcModel!=destModel) releaseDisplayModel(srcModel);
	return res;
}

typedef struct {
	HDC hdc;
	const void* pString;
	int cString;
	int iCharset;
	DWORD dwFlags;
} ScriptStringAnalyseArgs_t;

typedef map<SCRIPT_STRING_ANALYSIS,ScriptStringAnalyseArgs_t> ScriptStringAnalyseArgsByAnalysis_t;
ScriptStringAnalyseArgsByAnalysis_t ScriptStringAnalyseArgsByAnalysis;
CRITICAL_SECTION criticalSection_ScriptStringAnalyseArgsByAnalysis;
BOOL allow_ScriptStringAnalyseArgsByAnalysis=FALSE;

//ScriptStringAnalyse hook function
//Hooked so we can detect when a character string is being converted in to glyphs.
//Much of Windows (from 2000 onwards) now passes text through uniscribe (this and other Script functions).
typedef HRESULT(WINAPI *ScriptStringAnalyse_funcType)(HDC,const void*,int,int,int,DWORD,int,SCRIPT_CONTROL*,SCRIPT_STATE*,const int*,SCRIPT_TABDEF*,const BYTE*,SCRIPT_STRING_ANALYSIS*);
ScriptStringAnalyse_funcType real_ScriptStringAnalyse=NULL;
HRESULT WINAPI fake_ScriptStringAnalyse(HDC hdc,const void* pString, int cString, int cGlyphs, int iCharset, DWORD dwFlags, int iRectWidth, SCRIPT_CONTROL* psControl, SCRIPT_STATE* psState, const int* piDx, SCRIPT_TABDEF* pTabdef, const BYTE* pbInClass, SCRIPT_STRING_ANALYSIS* pssa) {
	//Call the real ScriptStringAnalyse
	HRESULT res=real_ScriptStringAnalyse(hdc,pString,cString,cGlyphs,iCharset,dwFlags,iRectWidth,psControl,psState,piDx,pTabdef,pbInClass,pssa);
	//We only want to go on if  there's safe arguments
	//We also need to acquire access to our scriptString analysis map
	if(res==S_OK&&pString&&cString>0&&pssa&&allow_ScriptStringAnalyseArgsByAnalysis) {
		EnterCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
		if(!allow_ScriptStringAnalyseArgsByAnalysis) return res;
		//Record information such as the origianl string and a way we can identify it later.
		ScriptStringAnalyseArgs_t args={hdc,pString,cString,iCharset,dwFlags};
		ScriptStringAnalyseArgsByAnalysis[*pssa]=args;
		LeaveCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
	}
	return res;
}

//ScriptStringFree hook function
//Hooked so we can get rid of any references to information collected via the ScriptStringAnalyse hook function
typedef HRESULT(WINAPI *ScriptStringFree_funcType)(SCRIPT_STRING_ANALYSIS*);
ScriptStringFree_funcType real_ScriptStringFree=NULL;
HRESULT WINAPI fake_ScriptStringFree(SCRIPT_STRING_ANALYSIS* pssa) {
	//Call the real ScriptStringFree
	HRESULT res=real_ScriptStringFree(pssa);
	//If it worked, and arguments seem sane, we go on.
	//We also need to acquire access to our scriptString analysis map
	if(res==S_OK&&pssa&&allow_ScriptStringAnalyseArgsByAnalysis) {
		EnterCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
		if(!allow_ScriptStringAnalyseArgsByAnalysis) return res;
		//Get rid of unneeded info
		ScriptStringAnalyseArgsByAnalysis.erase(*pssa);
		LeaveCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
	}
	return res; 
}

//ScriptStringOut hook function
//Hooked so we can detect when glyphs previously converted with ScriptStringAnalyse are being outputted.
typedef HRESULT(WINAPI *ScriptStringOut_funcType)(SCRIPT_STRING_ANALYSIS,int,int,UINT,const RECT*,int,int,BOOL);
ScriptStringOut_funcType real_ScriptStringOut=NULL;
HRESULT WINAPI fake_ScriptStringOut(SCRIPT_STRING_ANALYSIS ssa,int iX,int iY,UINT uOptions,const RECT *prc,int iMinSel,int iMaxSel,BOOL fDisabled) {
	//Call the real ScriptStringOut
	HRESULT res=real_ScriptStringOut(ssa,iX,iY,uOptions,prc,iMinSel,iMaxSel,fDisabled);
	//If ScriptStringOut was successful we can go on
	//We also need to acquire access to our Script analysis map
	if(res==S_OK&&allow_ScriptStringAnalyseArgsByAnalysis) {
		EnterCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
		if(!allow_ScriptStringAnalyseArgsByAnalysis) return res;
		//Find out if we know about these glyphs
		ScriptStringAnalyseArgsByAnalysis_t::iterator i=ScriptStringAnalyseArgsByAnalysis.find(ssa);
		if(i!=ScriptStringAnalyseArgsByAnalysis.end()) {
			//Try and get/create a displayModel for this DC, and if we can, then record the origianl text for these glyphs
			displayModel_t* model=acquireDisplayModel(i->second.hdc);
			if(model) {
				BOOL stripHotkeyIndicator=(i->second.dwFlags&SSA_HIDEHOTKEY||i->second.dwFlags&SSA_HOTKEY);
				ExtTextOutHelper(model,i->second.hdc,iX,iY,ScriptString_pSize(i->first),prc,uOptions,GetTextAlign(i->second.hdc),stripHotkeyIndicator,(wchar_t*)(i->second.pString),i->second.cString);
				releaseDisplayModel(model);
			}
		}
		LeaveCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
	}
	return res;
}

//DestroyWindow hook function
//Hooked so that we can get rid of  displayModels for windows that are being destroied.
typedef BOOL(WINAPI *DestroyWindow_funcType)(HWND);
DestroyWindow_funcType real_DestroyWindow=NULL;
BOOL WINAPI fake_DestroyWindow(HWND hwnd) {
	//Call the real DestroyWindow
	BOOL res=real_DestroyWindow(hwnd);
	//If successful, acquire access to the display model maps and remove the displayModel for this window if it exists.
	if(res) {
		EnterCriticalSection(&criticalSection_displayModelMaps);
		if(!allow_displayModelMaps) {
			LeaveCriticalSection(&criticalSection_displayModelMaps);
			return res;
		}
		displayModelsByWindow_t::iterator i=displayModelsByWindow.find(hwnd);
		if(i!=displayModelsByWindow.end()) {
			i->second->Release();
			displayModelsByWindow.erase(i);
		}
		LeaveCriticalSection(&criticalSection_displayModelMaps);
	}
	return res;
}

void gdiHooks_inProcess_initialize() {
	//Initialize critical sections and access variables for various maps
	InitializeCriticalSection(&criticalSection_displayModelMaps);
	allow_displayModelMaps=TRUE;
	InitializeCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
	allow_ScriptStringAnalyseArgsByAnalysis=TRUE;
	if (!apiHook_init()) return; //we can't do anything further
	//Hook needed functions
	hookClass_DrawTextEx<char>::realFunction=(hookClass_DrawTextEx<char>::funcType)apiHook_hookFunction("USER32.dll","DrawTextExA",hookClass_DrawTextEx<char>::fakeFunction);
	hookClass_DrawTextEx<wchar_t>::realFunction=(hookClass_DrawTextEx<wchar_t>::funcType)apiHook_hookFunction("USER32.dll","DrawTextExW",hookClass_DrawTextEx<wchar_t>::fakeFunction);
	//hookClass_TabbedTextOut<char>::realFunction=(hookClass_TabbedTextOut<char>::funcType)apiHook_hookFunction("USER32.dll","TabbedTextOutA",hookClass_TabbedTextOut<char>::fakeFunction);
	//hookClass_TabbedTextOut<wchar_t>::realFunction=(hookClass_TabbedTextOut<wchar_t>::funcType)apiHook_hookFunction("USER32.dll","TabbedTextOutW",hookClass_TabbedTextOut<wchar_t>::fakeFunction);
	hookClass_TextOut<char>::realFunction=(hookClass_TextOut<char>::funcType)apiHook_hookFunction("GDI32.dll","TextOutA",hookClass_TextOut<char>::fakeFunction);
	hookClass_TextOut<wchar_t>::realFunction=(hookClass_TextOut<wchar_t>::funcType)apiHook_hookFunction("GDI32.dll","TextOutW",hookClass_TextOut<wchar_t>::fakeFunction);
	hookClass_ExtTextOut<char>::realFunction=(hookClass_ExtTextOut<char>::funcType)apiHook_hookFunction("GDI32.dll","ExtTextOutA",hookClass_ExtTextOut<char>::fakeFunction);
	hookClass_ExtTextOut<wchar_t>::realFunction=(hookClass_ExtTextOut<wchar_t>::funcType)apiHook_hookFunction("GDI32.dll","ExtTextOutW",hookClass_ExtTextOut<wchar_t>::fakeFunction);
	real_CreateCompatibleDC=(CreateCompatibleDC_funcType)apiHook_hookFunction("GDI32.dll","CreateCompatibleDC",fake_CreateCompatibleDC);
	real_DeleteDC=(DeleteDC_funcType)apiHook_hookFunction("GDI32.dll","DeleteDC",fake_DeleteDC);
	real_BitBlt=(BitBlt_funcType)apiHook_hookFunction("GDI32.dll","BitBlt",fake_BitBlt);
	real_DestroyWindow=(DestroyWindow_funcType)apiHook_hookFunction("USER32.dll","DestroyWindow",fake_DestroyWindow);
	real_ScriptStringAnalyse=(ScriptStringAnalyse_funcType)apiHook_hookFunction("USP10.dll","ScriptStringAnalyse",fake_ScriptStringAnalyse);
	real_ScriptStringFree=(ScriptStringFree_funcType)apiHook_hookFunction("USP10.dll","ScriptStringFree",fake_ScriptStringFree);
	real_ScriptStringOut=(ScriptStringOut_funcType)apiHook_hookFunction("USP10.dll","ScriptStringOut",fake_ScriptStringOut);
}

void gdiHooks_inProcess_terminate() {
	//Acquire access to the maps and clean them up
	EnterCriticalSection(&criticalSection_displayModelMaps);
	allow_displayModelMaps=FALSE;
	displayModelsByWindow_t::iterator i=displayModelsByWindow.begin();
	while(i!=displayModelsByWindow.end()) {
		i->second->Release();
		displayModelsByWindow.erase(i++);
	}  
	displayModelsByDC_t::iterator j=displayModelsByMemoryDC.begin();
	while(j!=displayModelsByMemoryDC.end()) {
		j->second->Release();
		displayModelsByMemoryDC.erase(j++);
	}  
	LeaveCriticalSection(&criticalSection_displayModelMaps);
	EnterCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
	allow_ScriptStringAnalyseArgsByAnalysis=FALSE;
	ScriptStringAnalyseArgsByAnalysis.clear();
	LeaveCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
}
