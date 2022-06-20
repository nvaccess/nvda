/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2006-2021 NV Access Limited, Aleksey Sadovoy, Babbage B.V., Matthew Campbell
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#include <vector>
#include <algorithm>
#include <optional>
#include <map>
#include <set>
#include <list>
#include <windows.h>
#include <usp10.h>
#include "nvdaHelperRemote.h"
#include "dllmain.h"
#include "apiHook.h"
#include "displayModel.h"
#include <common/log.h>
#include <remote/nvdaControllerInternal.h>
#include <common/lock.h>
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

map<HWND,int> windowsForTextChangeNotifications;
map<HWND,RECT> textChangeNotifications;
UINT_PTR textChangeNotifyTimerID=0;
DWORD tls_index_textInsertionsCount=TLS_OUT_OF_INDEXES;
DWORD tls_index_curScriptTextOutScriptAnalysis=TLS_OUT_OF_INDEXES;

class TextInsertionTracker {
	private:
	INT_PTR _initialRefCount;
	bool _wasFirst;
	public:
	TextInsertionTracker(): _initialRefCount(0), _wasFirst(false)  {
		_initialRefCount=(INT_PTR)TlsGetValue(tls_index_textInsertionsCount);
		if(_initialRefCount==0) {
			_initialRefCount=1;
			TlsSetValue(tls_index_textInsertionsCount,(LPVOID)_initialRefCount);
			_wasFirst=true;
		} else {
			_wasFirst=false;
		}
	}
	~TextInsertionTracker() {
		if(_wasFirst) TlsSetValue(tls_index_textInsertionsCount,(LPVOID)0);
	}
	static void reportTextInsertion() {
		INT_PTR newRefCount=(INT_PTR)TlsGetValue(tls_index_textInsertionsCount);
		if(newRefCount>0) TlsSetValue(tls_index_textInsertionsCount,(LPVOID)(newRefCount+1));
	}
	bool hasTrackedTextInsertion() {
		INT_PTR newRefCount=(INT_PTR)TlsGetValue(tls_index_textInsertionsCount);
		return newRefCount>_initialRefCount;
	}
};

void CALLBACK textChangeNotifyTimerProc(HWND hwnd, UINT msg, UINT_PTR timerID, DWORD time) {
	map<HWND,RECT> tempMap;
	textChangeNotifications.swap(tempMap);
	for(map<HWND,RECT>::iterator i=tempMap.begin();i!=tempMap.end();++i) {
		nvdaControllerInternal_displayModelTextChangeNotify(HandleToUlong(i->first),i->second.left,i->second.top,i->second.right,i->second.bottom);
	}
}

void queueTextChangeNotify(HWND hwnd, RECT& rc) {
	//If this window is not supposed to fire text change notifications then do nothing.
	map<HWND,int>::iterator i=windowsForTextChangeNotifications.find(hwnd);
	if(i==windowsForTextChangeNotifications.end()||i->second<1) return;
	map<HWND,RECT>::iterator n=textChangeNotifications.find(hwnd);
	if(n==textChangeNotifications.end()) {
		// There isn't a notification yet for this window.
		textChangeNotifications.insert(make_pair(hwnd,rc));
	} else {
		// There is already a notification for this window,
		// so expand its rectangle to encompass this new rectangle.
		n->second.left=min(n->second.left,rc.left);
		n->second.top=min(n->second.top,rc.top);
		n->second.right=max(n->second.right,rc.right);
		n->second.bottom=max(n->second.bottom,rc.bottom);
	}
}

displayModelsMap_t<HDC> displayModelsByMemoryDC;
displayModelsMap_t<HWND> displayModelsByWindow;

/**
 * Fetches and or creates a new displayModel for the window of the given device context.
 * If this function returns a displayModel, you must call release on it when you no longer need it. 
 * @param hdc a handle of the device context who's window the displayModel is for.
 * @param noCreate If true a display model will not be created if it does not exist. 
 * @return a pointer to the  new/existing displayModel, NULL if gdiHooks is not initialized or has been terminated. 
 */
inline displayModel_t* acquireDisplayModel(HDC hdc, BOOL noCreate=FALSE) {
	//If we are allowed, acquire use of the displayModel maps
	displayModel_t* model=NULL;
	//If the DC has a window, then either get an existing displayModel using the window, or create a new one and store it by its window.
	//If  the DC does not have a window, try and get the displayModel from our existing Memory DC displayModels. 
	HWND hwnd=WindowFromDC(hdc);
	LOG_DEBUG(L"window from DC is "<<hwnd);
	if(hwnd) {
		displayModelsByWindow.acquire();
		displayModelsMap_t<HWND>::iterator i=displayModelsByWindow.find(hwnd);
		if(i!=displayModelsByWindow.end()) {
			model=i->second;
		} else if(!noCreate) {
			model=new displayModel_t(hwnd);
			displayModelsByWindow.insert(make_pair(hwnd,model));
		}
		if(model) model->acquire();
		displayModelsByWindow.release();
	} else {
		displayModelsByMemoryDC.acquire();
		displayModelsMap_t<HDC>::iterator i=displayModelsByMemoryDC.find(hdc);
		if(i!=displayModelsByMemoryDC.end()) {
			model=i->second;
		}
		if(model) model->acquire();
		displayModelsByMemoryDC.release();
	}
	return model;
}

/**
 * converts given points from dc coordinates to screen coordinates. 
 * @param hdc a handle to a device context
 * @param points a pointer to the points you wish to convert.
 * @param count the number of points you want to convert.
 */
void dcPointsToScreenPoints(HDC hdc, POINT* points, int count,bool relative) {
	//Convert to logical points to device points 
	//Includes origins and scaling for window and viewport, and also world transformation 
	LPtoDP(hdc,points,count);
	if(relative) {
		//Do what we did with the points, but with 0,0, and then subtract that from all points
		POINT origPoint={0,0};
		LPtoDP(hdc,&origPoint,1);
		for(int i=0;i<count;++i) {
			points[i].x-=origPoint.x;
			points[i].y-=origPoint.y;
		}
	} else { //absolute
		//LptoDp does not take the final DC origin in to account, so plus that to all points here to make them completely screen absolute
		POINT dcOrgPoint;
		GetDCOrgEx(hdc,&dcOrgPoint);
		for(int i=0;i<count;++i) {
			points[i].x+=dcOrgPoint.x;
			points[i].y+=dcOrgPoint.y;
		}
	}
}

//see SynPdf at http://synopse.info
//Converts word array to little endian.
void swapBuffer(WORD* array, int length) {
	for(int i=0; i<length; i++) array[i]=SWAPWORD(array[i]);
}

//Retrieves table data from font selected in DC using GetFontData [SynPdf]
std::vector<BYTE> getTTFData(HDC hdc, char* tableName) {
	DWORD len=GetFontData(hdc,*((LPDWORD)tableName),0,NULL,0);
	if(len==GDI_ERROR) {
		LOG_DEBUG("getTTFData for table "<<tableName<<" result GDI_ERROR");
        return std::vector<BYTE>();
	}
	std::vector<BYTE> resVec(len, BYTE(0));
	PBYTE res = resVec.data();
	if(GetFontData(hdc,*((LPDWORD)tableName),0,res,len)==GDI_ERROR) {
		//Probably could not happen
		LOG_DEBUG("getTTFData for table "<<tableName<<", dataSize="<<len<<" result GDI_ERROR");
		return std::vector<BYTE>();
	}
	LOG_DEBUG("getTTFData for table "<<tableName<<", dataSize="<<len);
	swapBuffer((WORD*)res,len>>1);
	return resVec;
}

//This class contains glyphIndex to wchar_t mapping. See [cmap], subheading "Format 4: Segment mapping to delta values"
class GlyphTranslator {
	private:
	unsigned volatile long _refCount;
	map<int,wchar_t> _glyphs;

	public:

	long incRef() {
		return InterlockedIncrement(&_refCount);
	}

	long decRef() {
		long refCount=InterlockedDecrement(&_refCount);
		if(refCount==0) {
			delete this;
		}
		nhAssert(refCount>=0);
		return refCount;
	}

	GlyphTranslator(HDC hdc) : _glyphs(), _refCount(0) {
		incRef();
		LOG_DEBUG("Creating instance at "<<this);

		std::vector<BYTE> pVec = getTTFData(hdc, "cmap");
		if(pVec.empty()){
			return;
		}
		PBYTE p = pVec.data();
		DWORD cmapLen = static_cast<DWORD>(pVec.size()); // size could be bigger than a DWORD
		CmapHeader* header=(CmapHeader*)p;
		EncodingRecord* encodings=(EncodingRecord*)(p+sizeof(CmapHeader));
		DWORD off=0;
		LOG_DEBUG("Number of encodings: "<<header->numTables);
		for(int i=0; i<header->numTables; i++) {
			EncodingRecord e=encodings[i];
			if(e.platformID==3 && e.encodingID==1) {
				off=SWAPLONG(e.offset);
				LOG_DEBUG("Unicode mapping found at offset "<<off);
				break;
			}
		}
		if(off==0 || off>cmapLen) {
			LOG_DEBUG("Offset seems to be out of range ("<<off<<")");
			return;
		}
		CmapFmt4Header* fmt4=(CmapFmt4Header*)(p+off);
		if(fmt4->format!=4) {
			LOG_DEBUG("No format4 table found, found format "<<fmt4->format);
			return;
		}
		LOG_DEBUG("segCountX2: "<<fmt4->segCountX2<<", format: "<<fmt4->format<<", length: "<<fmt4->length);
		WORD segCount=fmt4->segCountX2>>1;
		PBYTE tmpP=p;
		p+=(off+sizeof(CmapFmt4Header));
		WORD* endCode=(WORD*)p;
		WORD* startCode=endCode+segCount+1; //+1 for reservedPad
		SHORT* idDelta=(SHORT*)startCode+segCount;
		WORD* idRangeOffset=(WORD*)idDelta+segCount;
		WORD* glyphIndexArray=idRangeOffset+segCount;
		p=tmpP;
		LOG_DEBUG("Mapping glyphs...");
		for(int i=0; i<segCount; i++) {
			SHORT delta=idDelta[i];
			WORD offset=idRangeOffset[i];
			for(int code=startCode[i]; code<=endCode[i]; code++) {
				WORD glyphIndex;
				if(offset!=0) {
					glyphIndex=*(offset/2+(code-startCode[i])+&idRangeOffset[i]);
					if(glyphIndex!=0) glyphIndex+=delta;
				}
				else glyphIndex=code+delta;
				_glyphs.insert(make_pair(glyphIndex,(wchar_t)code));
				LOG_DEBUG("Mapped "<<glyphIndex<<" to "<<(wchar_t)code);
			}
		}
		LOG_DEBUG(_glyphs.size()<<" glyphs were mapped");
	}

	~GlyphTranslator() {
		LOG_DEBUG("Deleting instance at "<<this);
	}

	bool hasMapping() { return !_glyphs.empty(); }

	bool translateGlyphs(const wchar_t* lpString, int cbCount, wstring& newString) {
		if(!hasMapping()) return false;
		newString.assign(cbCount, '\0');
		wchar_t* newStr = newString.data();
		for(int i=0; i<cbCount; i++) {
			map<int,wchar_t>::iterator wchr=_glyphs.find((int)lpString[i]);
			if(wchr==_glyphs.end()) newStr[i]=' ';
			else newStr[i]=wchr->second;
		}
		LOG_DEBUG("Translated glyphs: " << newString);
		return true;
	}
};

class GlyphTranslatorCache : protected LockableObject {
	private:

	map<int,GlyphTranslator*> _glyphTranslatorsByFontChecksum;

	public:

	GlyphTranslatorCache() : _glyphTranslatorsByFontChecksum(), LockableObject() {}

	GlyphTranslator* fetchGlyphTranslator(HDC hdc) {
		std::vector<BYTE> fhVec = getTTFData(hdc, "head");
		if (fhVec.empty()) {
			return nullptr;
		}
		FontHeader* fh = reinterpret_cast<FontHeader*>(fhVec.data());
		GlyphTranslator* gt=NULL;
		acquire();
		map<int,GlyphTranslator*>::iterator i=_glyphTranslatorsByFontChecksum.find(fh->checksumAdjustment);
		if(i!=_glyphTranslatorsByFontChecksum.end()) {
			gt=i->second;
		} else {
			gt=new GlyphTranslator(hdc);
			_glyphTranslatorsByFontChecksum.insert(make_pair(fh->checksumAdjustment,gt));
		}
		if(gt) gt->incRef();
		release();
		return gt;
	}

	void cleanup() {
		acquire();
		map<int,GlyphTranslator*>::iterator i=_glyphTranslatorsByFontChecksum.begin();
		while(i!=_glyphTranslatorsByFontChecksum.end()) {
			i->second->decRef();
			_glyphTranslatorsByFontChecksum.erase(i++);
		}    
		release();
	}
};

GlyphTranslatorCache glyphTranslatorCache;

std::pair<std::vector<POINT>, SIZE> calcCharExtentsVecFromLpdx(
	const int cbCount, const int* lpdx, const TEXTMETRIC& tm,
	const UINT& fuOptions,
	const HDC& hdc
) {
	const bool containsXandY = fuOptions & ETO_PDY; // does lpdx contain x and y or just x.
	auto ret = std::make_pair(std::vector<POINT>(cbCount), SIZE());
	auto& [characterExtentsVec, resultTextSize] = ret;

	long acX = 0;
	long acY = tm.tmHeight;
	for (int i = 0; i < cbCount; ++i) {
		const int lpdx_xIndex = containsXandY ? (i * 2) : i;
		acX += lpdx[lpdx_xIndex];
		characterExtentsVec[i].x = acX;
	}
	resultTextSize.cx = acX;
	resultTextSize.cy = acY;
	return ret;
}

std::pair<std::vector<POINT>, SIZE> calcCharExtentsVec(
	const int cbCount, const TEXTMETRIC& tm, const bool fromGlyphs,
	const HDC& hdc, const wchar_t* lpString, std::wstring& newText
) {
	const long height = tm.tmHeight;
	auto ret = std::make_pair(std::vector<POINT>(cbCount), SIZE());
	auto& [characterExtentsVec, resultTextSize] = ret;

	std::vector<int>characterExtentsXVec(cbCount);
	int* characterExtentsX = characterExtentsXVec.data();
	
	if(fromGlyphs) {
		LPWORD lpwszString = reinterpret_cast<LPWORD>(const_cast<wchar_t*>(lpString));
		GetTextExtentExPointI(
			hdc, lpwszString, cbCount, 0, nullptr,
			characterExtentsX, &resultTextSize
		);
	} else {
		GetTextExtentExPoint(
			hdc, newText.data(), cbCount, 0, nullptr,
			characterExtentsX, &resultTextSize
		);
	}
	for (int i = 0; i<cbCount; ++i) {
		characterExtentsVec[i].x = characterExtentsX[i];
		characterExtentsVec[i].y = height;
	}
	return ret;
}

/**
 * Given a displayModel, this function clears a rectangle, and inserts a chunk, for the given text,
 * using the given offsets and rectangle etc.
 * This function is used by many of the hook functions.
 * @param model a pointer to a displayModel
 * @param hdc a handle to the device context that was used to write the text originally.
 * @param[in] x the x coordinate (in device units) where the text should start from
	(depending on textAlign flags, this could be the left, center, or right of the text).
 * @param[in] y the y coordinate (in device units) where the text should start from
	(depending on textAlign flags, this could be the top, or bottom of the text).
 * @param[in] lprc a pointer to the rectangle that should be cleared.
	If lprc is NULL, or ETO_OPAQUE is not in fuOptions, then only the rectangle
	bounding the text will be cleared.
 * @param[in] fuOptions flags accepted by GDI32's ExtTextOut.
 * @param[in] textAlign possible flags returned by GDI32's GetTextAlign.
 * @param[in] lpString the string of unicode text you wish to record.
 * @param[in] codePage not used in the unicode version
 * @param[in] lpdx an optional array of x (or x and y paires if ETO_PDY is set) that describes
	where the next character starts relative to the origin of the current character.
 * @param[in] cbCount the length of the string in characters.
 * @param[out] resultTextSize An optional pointer to a SIZE structure that should be filled
	with the size of the text.
 * @param[in] direction >0 for left to right, <0 for right to left, 0 for neutral or unknown.
	Text must still be passed in in visual order.
  */
void ExtTextOutHelper(
	displayModel_t* model, HDC hdc, int x, int y, const RECT* lprc,
	UINT fuOptions,UINT textAlign, BOOL stripHotkeyIndicator,
	const wchar_t* lpString, const int codePage, const int* lpdx,
	int cbCount, LPSIZE resultTextSize, int direction
) {
	const bool isOpaqueRequested = fuOptions & ETO_OPAQUE; // The current background color should be used to fill the rectangle.
	RECT clearRect={0,0,0,0};
	//If a rectangle was provided, convert it to screen coordinates
	if(lprc) {
		clearRect=*lprc;
		dcPointsToScreenPoints(hdc,(LPPOINT)&clearRect,2,false);
		//Also if opaquing is requested, clear this rectangle in the given display model
		if (isOpaqueRequested) {
			model->clearRectangle(clearRect);
		}
	}
	//If there is no string given, then we don't need to go further
	if(!lpString||cbCount<=0) return;
	wstring newText=L"";
	bool fromGlyphs=false;
	if(fuOptions&ETO_GLYPH_INDEX) {
		GlyphTranslator* gt=glyphTranslatorCache.fetchGlyphTranslator(hdc);
		if(gt) {
			fromGlyphs=gt->translateGlyphs(lpString,cbCount,newText);
			gt->decRef();
		}
		if(!fromGlyphs) return;
	}
	SIZE _textSize;
	if(!resultTextSize) resultTextSize=&_textSize;
	if(resultTextSize) {
		resultTextSize->cx=0;
		resultTextSize->cy=0;
	}
	if(!fromGlyphs) newText=wstring(lpString,cbCount);
	//Windows reports reading direction wrong for a run containing numbers within RTL runs.
	//Therefore for this case let NVDA decide the direction
	if(direction==-1) {
		for(int i=0;i<cbCount;++i) {
			wchar_t c=newText[i];
			if((c>=L'0'&&c<=L'9')||(c>=L'\x0660'&&c<=L'\x0669')) {
				direction=-2;
				break;
			}
		}
	}
	//Search for and remove the first & symbol if we have been requested to stip hotkey indicator.
	if(stripHotkeyIndicator) {
		size_t pos=newText.find(L'&');
		if(pos!=wstring::npos) {
			newText.erase(pos,1);
			cbCount--;
		}
	}

	//Fetch the text metrics for this font
	TEXTMETRIC tm;
	GetTextMetrics(hdc,&tm);

	//Calculate character extents array
	auto[characterExtentsVec, textSize] = lpdx ?
		calcCharExtentsVecFromLpdx(cbCount, lpdx, tm, fuOptions, hdc)
		:
		calcCharExtentsVec(cbCount, tm, fromGlyphs, hdc, lpString, newText);
	POINT* characterExtents = characterExtentsVec.data();
	*resultTextSize = textSize; // resultTextSize is an out-param and must be calculated before early exit.
	
	
	//Convert the character extents from logical to physical points, but keep them relative
	dcPointsToScreenPoints(hdc,characterExtents,cbCount,true);

	// Are we writing a transparent background?
	std::optional<bool> cached_transparentBackground;
	// Prevent multiple calculations
	auto isBackgroundTransparent = [&hdc, &cached_transparentBackground, isOpaqueRequested]() -> bool {
		if (!cached_transparentBackground.has_value()) {
			cached_transparentBackground = (!isOpaqueRequested) && GetBkMode(hdc) == TRANSPARENT;
		}
		return cached_transparentBackground.value();
	};
	
	if(tm.tmCharSet != SYMBOL_CHARSET && isBackgroundTransparent()) {
		//Find out if the text we're writing is just whitespace
		BOOL whitespace=TRUE;
		for(wstring::iterator i=newText.begin();i!=newText.end()&&(whitespace=iswspace(*i));++i);
		if(whitespace) {
			return;
		}
	}
	int textLeft=x;
	int textTop=y;
	//X and Y are not always the left and top of the text.
	//So correct them by taking textAlignment in to account
	UINT hTextAlign=textAlign&(TA_LEFT|TA_RIGHT|TA_CENTER);
	if(hTextAlign==TA_CENTER) {
		LOG_DEBUG(L"TA_CENTER set");
		textLeft-=(resultTextSize->cx/2);
	} else if(hTextAlign==TA_RIGHT) {
		LOG_DEBUG(L"TA_RIGHT set");
		textLeft-=resultTextSize->cx;
	}
	UINT vTextAlign=textAlign&(TA_TOP|TA_BOTTOM|TA_BASELINE);
	if(vTextAlign==TA_BOTTOM) {
		LOG_DEBUG(L"TA_BOTTOM set");
		textTop-=resultTextSize->cy;
	} else if(vTextAlign==TA_BASELINE) {
		LOG_DEBUG(L"TA_BASELINE set");
		textTop-=tm.tmAscent;
	}
	LOG_DEBUG(L"using offset of "<<textLeft<<L","<<textTop);
	RECT textRect={textLeft,textTop,textLeft+resultTextSize->cx,textTop+resultTextSize->cy};
	//We must store chunks using device coordinates, not logical coordinates, as its possible for the DC's viewport to move or resize.
	//For example, in Windows 7, menu items are always drawn at the same DC coordinates, but the DC is moved downward each time.
	POINT baselinePoint={textRect.left,textRect.top+tm.tmAscent};
	dcPointsToScreenPoints(hdc,&baselinePoint,1,false);
	dcPointsToScreenPoints(hdc,(LPPOINT)&textRect,2,false);
	//Calculate the real physical baselineFromTop
	//Clear a space for the text in the model, though take clipping in to account
	RECT tempRect;
	if(lprc&&(fuOptions&ETO_CLIPPED)&&IntersectRect(&tempRect,&textRect,&clearRect)) {
		model->clearRectangle(tempRect,TRUE);
	} else {
		model->clearRectangle(textRect,TRUE);
	}
	//Make sure this is text, and that its not using the symbol charset (e.g. the tick for a checkbox)
	//Before recording the text.
	if(cbCount>0&&tm.tmCharSet!=SYMBOL_CHARSET) {
		LOGFONT logFont;
		HGDIOBJ fontObj = GetCurrentObject(hdc, OBJ_FONT);
		GetObject(fontObj, sizeof(LOGFONT), &logFont);
		
		int fontSize = 0;
		if (logFont.lfHeight != 0) {
			const auto pixelsPerInchY = GetDeviceCaps(hdc, LOGPIXELSY);
			fontSize = (abs(logFont.lfHeight) * 72) / pixelsPerInchY;
		};
		displayModelFormatInfo_t formatInfo = {
			// lfFaceName will be NULL terminated
			// https://docs.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-logfonta
			std::wstring(logFont.lfFaceName), // fontName.
			fontSize, // fontSize
			bool(logFont.lfWeight >= 700), // bold
			bool(logFont.lfItalic), // italic
			bool(logFont.lfUnderline), // underline,
			displayModelFormatColor_t(GetTextColor(hdc)), // color
			displayModelFormatColor_t(GetBkColor(hdc), isBackgroundTransparent()) // backgroundColor
		};
		
		model->insertChunk(textRect,baselinePoint.y,newText,characterExtents,formatInfo,direction,(fuOptions&ETO_CLIPPED)?&clearRect:NULL);
		TextInsertionTracker::reportTextInsertion();
		HWND hwnd=WindowFromDC(hdc);
		if(hwnd) queueTextChangeNotify(hwnd,textRect);
	}
}

/**
 * an overload of ExtTextOutHelper to work with ansi strings.
 * @param lpString the string of ansi text you wish to record.
 * @param codePage the code page used for the string which will be converted to unicode
  */
void ExtTextOutHelper(displayModel_t* model, HDC hdc, int x, int y, const RECT* lprc,UINT fuOptions,UINT textAlign, BOOL stripHotkeyIndicator, const char* lpString, const int codePage, const int* lpdx, int cbCount, LPSIZE resultTextSize, int direction) {
	int newCount=0;
	wchar_t* pNewString = nullptr;
	std::wstring newString;
	if(lpString&&cbCount) {
		newCount=MultiByteToWideChar(codePage,0,lpString,cbCount,NULL,0);
		if(newCount>0) {
			newString.assign(newCount + 1, '\0');
			pNewString = newString.data();
			MultiByteToWideChar(codePage, 0, lpString, cbCount, pNewString, newCount);
		}
	}
	ExtTextOutHelper(
					model,
					hdc,
					x,
					y,
					lprc,
					fuOptions,
					textAlign,
					stripHotkeyIndicator,
					pNewString,
					codePage,
					lpdx,
					newCount,
					resultTextSize,
					direction
	);
}

//TextOut hook class template
//Handles char or wchar_t
template<typename charType> class hookClass_TextOut {
	public:
	typedef int(WINAPI *funcType)(HDC,int,int, const charType*,int);
	static funcType realFunction;
	static int  WINAPI fakeFunction(HDC hdc, int x, int y, const charType* lpString, int cbCount);
};

template<typename charType> typename hookClass_TextOut<charType>::funcType hookClass_TextOut<charType>::realFunction=NULL;

template<typename charType> int  WINAPI hookClass_TextOut<charType>::fakeFunction(HDC hdc, int x, int y, const charType* lpString, int cbCount) {
	UINT textAlign=GetTextAlign(hdc);
	POINT pos={x,y};
	if(textAlign&TA_UPDATECP) GetCurrentPositionEx(hdc,&pos);
	//Call the real function
	BOOL res;
	{
		TextInsertionTracker tracker; 
		res=realFunction(hdc,x,y,lpString,cbCount);
		if(tracker.hasTrackedTextInsertion()) return res;
	}
	//If the real function did not work, or the arguments are not sane, then stop here
	if(res==0||!lpString||cbCount<=0) return res;
	displayModel_t* model=acquireDisplayModel(hdc);
	//If we can't get a display model then stop here.
	if(!model) return res;
	//Calculate the size of the text
	ExtTextOutHelper(model,hdc,pos.x,pos.y,NULL,0,textAlign,FALSE,lpString,CP_THREAD_ACP,NULL,cbCount,NULL,false);
	model->release();
	return res;
}

//PolyTextOut hook class template

template<typename WA_POLYTEXT> class hookClass_PolyTextOut {
	public:
	typedef BOOL(WINAPI *funcType)(HDC,const WA_POLYTEXT*,int);
	static funcType realFunction;
	static BOOL WINAPI fakeFunction(HDC hdc,const WA_POLYTEXT* pptxt,int cStrings);
};

template<typename WA_POLYTEXT> typename hookClass_PolyTextOut<WA_POLYTEXT>::funcType hookClass_PolyTextOut<WA_POLYTEXT>::realFunction=NULL;

template<typename WA_POLYTEXT> BOOL WINAPI hookClass_PolyTextOut<WA_POLYTEXT>::fakeFunction(HDC hdc,const WA_POLYTEXT* pptxt,int cStrings) {
	//Collect text alignment and possibly current position
	UINT textAlign=GetTextAlign(hdc);
	POINT curPos;
	if(textAlign&TA_UPDATECP) {
		GetCurrentPositionEx(hdc,&curPos);
	}
	//Call the real function
	BOOL res;
	{
		TextInsertionTracker tracker;
		res=realFunction(hdc,pptxt,cStrings);
		if(tracker.hasTrackedTextInsertion()) return res;
	}
	//If the draw did not work, or there are no strings, then  stop here
	if(res==0||cStrings==0||!pptxt) return res;
	//Get or create a display model for this DC. If we can't get one then stop here
	displayModel_t* model=acquireDisplayModel(hdc);
	if(!model) return res;
	SIZE curTextSize;
	//For each of the strings, record the text
	for(int i=0;i<cStrings;++i) {
		const WA_POLYTEXT* curPptxt=&pptxt[i];
		RECT curClearRect={curPptxt->rcl.left,curPptxt->rcl.top,curPptxt->rcl.right,curPptxt->rcl.bottom};
		//Only use the given x and y if DC's current position should not be used
		if(!(textAlign&TA_UPDATECP)) {
			curPos.x=curPptxt->x;
			curPos.y=curPptxt->y;
		}
		//record the text
		ExtTextOutHelper(model,hdc,curPos.x,curPos.y,&curClearRect,curPptxt->uiFlags,textAlign,FALSE,curPptxt->lpstr,CP_THREAD_ACP,curPptxt->pdx,curPptxt->n,&curTextSize,false);
		//If the DC's current position should be used,  move our idea of it by the size of the text just recorded
		if(textAlign&TA_UPDATECP) {
			curPos.x+=curTextSize.cx;
			curPos.y+=curTextSize.cy;
		} 
	}
	//Release model and return
	model->release();
	return res;
}

//FillRect hook function
typedef int(WINAPI *FillRect_funcType)(HDC,const RECT*,HBRUSH);
FillRect_funcType real_FillRect=NULL;
int WINAPI fake_FillRect(HDC hdc, const RECT* lprc, HBRUSH hBrush) {
	//Call the real FillRectangle
	int res=real_FillRect(hdc,lprc,hBrush);
	//IfThe fill was successull we can go on.
	if(res==0||lprc==NULL) return res;
	//Try and get a displayModel for this DC, and if we can, then record the original text for these glyphs
	displayModel_t* model=acquireDisplayModel(hdc,TRUE);
	if(!model) return res;
	RECT rect=*lprc;
	dcPointsToScreenPoints(hdc,(LPPOINT)&rect,2,false);
	model->clearRectangle(rect);
	model->release();
	return res;
}

//DrawFocusRect hook function
typedef BOOL(WINAPI *DrawFocusRect_funcType)(HDC,const RECT*);
DrawFocusRect_funcType real_DrawFocusRect=NULL;
BOOL WINAPI fake_DrawFocusRect(HDC hdc, const RECT* lprc) {
	//Call the real DrawFocusRect
	BOOL res=real_DrawFocusRect(hdc,lprc);
	//If the draw was successfull we can go on.
	if(!res||!lprc) return res;
	displayModel_t* model=acquireDisplayModel(hdc,TRUE);
	if(!model) return res;
	RECT oldFocusRect;
	bool hadFocusRect=model->getFocusRect(&oldFocusRect);
	RECT focusRect=*lprc;
	dcPointsToScreenPoints(hdc,(LPPOINT)&focusRect,2,false);
	POINT pt={(focusRect.left+focusRect.right)/2,(focusRect.top+focusRect.bottom)/2};
	/*
	if(!hwnd) {
		// Not drawing directly to a window, so try and guess it by the coordinates
		hwnd=WindowFromPoint(pt);
		DWORD windowProcessID=0;
		DWORD curProcessID=GetCurrentProcessId();
		RECT windowRect;
		while(hwnd) {
			GetWindowRect(hwnd,&windowRect);
			GetWindowThreadProcessId(hwnd,&windowProcessID);
			if(windowProcessID==curProcessID&&windowRect.left<=focusRect.left&&windowRect.top<=focusRect.top&&windowRect.right>=focusRect.right&&windowRect.bottom>=focusRect.bottom) {
				break;
			}
			hwnd=GetAncestor(hwnd,GA_PARENT);
		}
	}
	*/
	if(hadFocusRect&&EqualRect(&oldFocusRect,&focusRect)) {
		model->setFocusRect(NULL);
	} else {
		model->setFocusRect(&focusRect);
		if(model->hwnd) nvdaControllerInternal_drawFocusRectNotify(HandleToUlong(model->hwnd),focusRect.left,focusRect.top,focusRect.right,focusRect.bottom);
	}
	model->release();
	return res;
}

//PatBlt hook function
typedef BOOL(WINAPI *PatBlt_funcType)(HDC,int,int,int,int,DWORD);
PatBlt_funcType real_PatBlt=NULL;
BOOL WINAPI fake_PatBlt(HDC hdc, int nxLeft, int nxTop, int nWidth, int nHeight, DWORD dwRop) {
	//Call the real PatBlt
	BOOL res=real_PatBlt(hdc,nxLeft,nxTop,nWidth,nHeight,dwRop);
	//IfPatBlt was successfull we can go on
	if(res==0) return res;
	//Try and get a displayModel for this DC, and if we can, then record the original text for these glyphs
	displayModel_t* model=acquireDisplayModel(hdc,TRUE);
	if(!model) return res;
	RECT rect={nxLeft,nxTop,nxLeft+nWidth,nxTop+nHeight};
	dcPointsToScreenPoints(hdc,(LPPOINT)&rect,2,false);
	model->clearRectangle(rect);
	model->release();
	return res;
}

//BeginPaint hook function
typedef HDC(WINAPI *BeginPaint_funcType)(HWND,LPPAINTSTRUCT);
BeginPaint_funcType real_BeginPaint=NULL;
HDC WINAPI fake_BeginPaint(HWND hwnd, LPPAINTSTRUCT lpPaint) {
	//Call the real BeginPaint
	HDC res=real_BeginPaint(hwnd,lpPaint);
	//If beginPaint was successfull we can go on
	if(res==0||!hwnd) return res;
	//Try and get a displayModel for this DC, and if we can, then record the original text for these glyphs
	displayModel_t* model=acquireDisplayModel(lpPaint->hdc,TRUE);
	if(!model) return res;
	RECT rect=lpPaint->rcPaint;
	ClientToScreen(hwnd,(LPPOINT)&rect);
	ClientToScreen(hwnd,((LPPOINT)&rect)+1);
	model->clearRectangle(rect);
	model->release();
	return res;
}

//ExtTextOut hook class template
//Handles char or wchar_t
template<typename charType> class hookClass_ExtTextOut {
	public:
	typedef BOOL(__stdcall *funcType)(HDC,int,int,UINT,const RECT*,const charType*,UINT,const INT*);
	static funcType realFunction;
	static BOOL __stdcall fakeFunction(HDC hdc, int x, int y, UINT fuOptions, const RECT* lprc, const charType* lpString, UINT cbCount, const INT* lpDx);
};

template<typename charType> typename hookClass_ExtTextOut<charType>::funcType hookClass_ExtTextOut<charType>::realFunction=NULL;

template<typename charType> BOOL __stdcall hookClass_ExtTextOut<charType>::fakeFunction(HDC hdc, int x, int y, UINT fuOptions, const RECT* lprc, const charType* lpString, UINT cbCount, const INT* lpDx) {
	UINT textAlign=GetTextAlign(hdc);
	POINT pos={x,y};
	if(textAlign&TA_UPDATECP) GetCurrentPositionEx(hdc,&pos);
	//Call the real function
	BOOL res;
	{
		TextInsertionTracker tracker;
		res=realFunction(hdc,x,y,fuOptions,lprc,lpString,cbCount,lpDx);
		if(tracker.hasTrackedTextInsertion()) return res;
	}
	//If the real function did not work, or the arguments are not sane, or only glyphs were provided, then stop here. 
	if(res==0) return res;
	//try to get or create a displayModel for this device context
	displayModel_t* model=acquireDisplayModel(hdc);
	//If we can't get a display model then stop here
	if(!model) return res;
	//Find out if this is rtl
	SCRIPT_ANALYSIS* psa=(SCRIPT_ANALYSIS*)TlsGetValue(tls_index_curScriptTextOutScriptAnalysis);
	//Record the text in the displayModel
	int direction=0;
	if(psa) {
		direction=(psa->fRTL)?-1:1;
	}
	ExtTextOutHelper(model,hdc,pos.x,pos.y,lprc,fuOptions,textAlign,FALSE,lpString,CP_THREAD_ACP,lpDx,cbCount,NULL,direction);
	//Release the displayModel and return
	model->release();
	return res;
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
	if(!newHdc) return NULL;
	displayModel_t* model=new displayModel_t();
	displayModelsByMemoryDC.acquire();
	displayModelsByMemoryDC.insert(make_pair(newHdc,model));
	displayModelsByMemoryDC.release();
	return newHdc;
}

//SelectObject hook function
//If a bitmap is being selected, then  we fully clear the display model for this DC if it exists.
typedef HGDIOBJ(WINAPI *SelectObject_funcType)(HDC,HGDIOBJ);
SelectObject_funcType real_SelectObject=NULL;
HGDIOBJ WINAPI fake_SelectObject(HDC hdc, HGDIOBJ hGdiObj) {
	//Call the real SelectObject
	HGDIOBJ res=real_SelectObject(hdc,hGdiObj);
	//If The select was successfull, and the object is a bitmap,  we can go on.
	if(res==0||hGdiObj==NULL||GetObjectType(hGdiObj)!=OBJ_BITMAP) return res;
	//Try and get a displayModel for this DC
	displayModel_t* model=acquireDisplayModel(hdc,TRUE);
	if(!model) return res;
	model->clearAll();
	model->release();
	return res;
}

//DeleteDC hook function
//Hooked so we can get rid of any memory DC no longer needed by the application.
typedef BOOL(WINAPI *DeleteDC_funcType)(HDC);
DeleteDC_funcType real_DeleteDC=NULL;
BOOL WINAPI fake_DeleteDC(HDC hdc) {
	//Call the real DeleteDC
	BOOL res=real_DeleteDC(hdc);
	if(res==0) return res;
	//If the DC was successfully deleted, we should remove  the displayModel we have for it, if it exists.
	displayModelsByMemoryDC.acquire();
	displayModelsMap_t<HDC>::iterator i=displayModelsByMemoryDC.find(hdc);
	if(i!=displayModelsByMemoryDC.end()) {
		i->second->requestDelete();
		displayModelsByMemoryDC.erase(i);
	}
	displayModelsByMemoryDC.release();
	return res;
}

void StretchBlt_helper(HDC hdcDest, int nXDest, int nYDest, int nWidthDest, int nHeightDest, HDC hdcSrc, int nXSrc, int nYSrc, int nWidthSrc, int nHeightSrc, DWORD dwRop) {
	dwRop=dwRop&0x00ffffff;
	bool useSource=(dwRop==MERGECOPY||dwRop==MERGEPAINT||dwRop==NOTSRCCOPY||dwRop==NOTSRCERASE||dwRop==PATPAINT||dwRop==SRCAND||dwRop==SRCCOPY||dwRop==SRCERASE||dwRop==SRCINVERT||dwRop==SRCPAINT);
	bool destInvertBefore=dwRop==SRCERASE;
	bool destInvertAfter=(dwRop==DSTINVERT||dwRop==NOTSRCERASE);
	bool sourceInvert=(dwRop==MERGEPAINT||dwRop==NOTSRCCOPY||dwRop==PATPAINT);
	bool opaqueSource=(dwRop==MERGECOPY||dwRop==NOTSRCCOPY||dwRop==SRCCOPY);
	bool clearDest=(dwRop==BLACKNESS||dwRop==WHITENESS||dwRop==PATCOPY);
	//If there is no source dc given, the destination dc should be used as the source
	if(hdcSrc==NULL) hdcSrc=hdcDest;
	//Try getting a display model for the source DC if one is needed.
	displayModel_t* srcModel=NULL;
	if(useSource) {
		srcModel=acquireDisplayModel(hdcSrc,TRUE);
	}
	//Get or create a display model from the destination DC
	//Don't create one if there is no source model (i.e. dest model will be used as source model)
	displayModel_t* destModel=acquireDisplayModel(hdcDest,srcModel==NULL);
	if(!destModel) {
		if(srcModel) srcModel->release();
		return;
	}
	RECT srcRect={nXSrc,nYSrc,nXSrc+nWidthSrc,nYSrc+nHeightSrc};
	//we record chunks using device coordinates -- DCs can move/resize
	dcPointsToScreenPoints(hdcSrc,(LPPOINT)&srcRect,2,false);
	RECT destRect={nXDest,nYDest,nXDest+nWidthDest,nYDest+nHeightDest};
	//we record chunks using device coordinates -- DCs can move/resize
	dcPointsToScreenPoints(hdcDest,(LPPOINT)&destRect,2,false);
	if(destInvertBefore) {
		destModel->copyRectangle(destRect,TRUE,TRUE,TRUE,destRect,NULL,NULL);
	}
	if(srcModel) {
		//Copy the requested rectangle from the source model in to the destination model, at the given coordinates.
		srcModel->copyRectangle(srcRect,FALSE,opaqueSource,sourceInvert,destRect,NULL,destModel);
		HWND hwnd=WindowFromDC(hdcDest);
		if(hwnd) queueTextChangeNotify(hwnd,destRect);
	}
	if(destInvertAfter) {
		destModel->copyRectangle(destRect,TRUE,TRUE,TRUE,destRect,NULL,NULL);
	}
	if(clearDest) {
		destModel->clearRectangle(destRect);
	}
	//release models and return
	if(srcModel) srcModel->release();
	destModel->release();
	return;
}

//BitBlt hook function
//Hooked so we can tell when content from one DC is being copied (bit blitted) to another (most likely from a memory DC to a window DC). 
typedef BOOL(WINAPI *BitBlt_funcType)(HDC,int,int,int,int,HDC,int,int,DWORD);
BitBlt_funcType real_BitBlt=NULL;
BOOL WINAPI fake_BitBlt(HDC hdcDest, int nXDest, int nYDest, int nWidth, int nHeight, HDC hdcSrc, int nXSrc, int nYSrc, DWORD dwRop) {
	//Call the real BitBlt
	BOOL res=real_BitBlt(hdcDest,nXDest,nYDest,nWidth,nHeight,hdcSrc,nXSrc,nYSrc,dwRop);
	//If bit blit didn't work, or its not a simple copy, we don't want to know about it
	if(!res) return res;
	StretchBlt_helper(hdcDest, nXDest, nYDest, nWidth, nHeight, hdcSrc, nXSrc, nYSrc, nWidth, nHeight, dwRop);
	return res;
}

//StretchBlt hook function
typedef BOOL(WINAPI *StretchBlt_funcType)(HDC,int,int,int,int,HDC,int,int,int,int,DWORD);
StretchBlt_funcType real_StretchBlt=NULL;
BOOL WINAPI fake_StretchBlt(HDC hdcDest, int nXDest, int nYDest, int nWidthDest, int nHeightDest, HDC hdcSrc, int nXSrc, int nYSrc, int nWidthSrc, int nHeightSrc, DWORD dwRop) {
	//Call the real StretchBlt
	BOOL res=real_StretchBlt(hdcDest,nXDest,nYDest,nWidthDest,nHeightDest,hdcSrc,nXSrc,nYSrc,nWidthSrc,nHeightSrc,dwRop);
	if(!res) return res;
	//#2989: KMPlayer uses stretchBlt with SRCCOPY  to place a graphic over the top of its menu items replacing the real text.
	//Therefore at the moment don't allow stretchBlt SRCCOPY to clear previous text -- change it to SRCAND if blitting directly to a menu window
	HWND hwnd=NULL;
	wchar_t className[7]; 
	if(hdcDest&&dwRop==SRCCOPY&&(hwnd=WindowFromDC(hdcDest))&&GetClassName(hwnd,className,ARRAYSIZE(className))>0&&wcscmp(className,L"#32768")==0) {
		dwRop=SRCAND;
	}
	StretchBlt_helper(hdcDest, nXDest, nYDest, nWidthDest, nHeightDest, hdcSrc, nXSrc, nYSrc, nWidthSrc, nHeightSrc, dwRop);
	return res;
}

//GdiTransparentBlt hook function
typedef BOOL(WINAPI *GdiTransparentBlt_funcType)(HDC,int,int,int,int,HDC,int,int,int,int,UINT);
GdiTransparentBlt_funcType real_GdiTransparentBlt=NULL;
BOOL WINAPI fake_GdiTransparentBlt(HDC hdcDest, int nXDest, int nYDest, int nWidthDest, int nHeightDest, HDC hdcSrc, int nXSrc, int nYSrc, int nWidthSrc, int nHeightSrc, UINT crTransparent) {
	//Call the real StretchBlt
	BOOL res=real_GdiTransparentBlt(hdcDest,nXDest,nYDest,nWidthDest,nHeightDest,hdcSrc,nXSrc,nYSrc,nWidthSrc,nHeightSrc,crTransparent);
	if(!res) return res;
	StretchBlt_helper(hdcDest, nXDest, nYDest, nWidthDest, nHeightDest, hdcSrc, nXSrc, nYSrc, nWidthSrc, nHeightSrc, SRCPAINT);
	return res;
}

//Converts a GDI font charset identifier to a Windows codePage identifier
inline int charSetToCodePage(int charset) {
	//Mappings from http://support.microsoft.com/kb/165478
	switch(charset) {
		case DEFAULT_CHARSET:
		return CP_ACP;
		case SYMBOL_CHARSET:
		return CP_SYMBOL;
		case MAC_CHARSET:
		return CP_MACCP;
		case OEM_CHARSET:
		return CP_OEMCP;
		case ANSI_CHARSET:
		return 1252;
		case RUSSIAN_CHARSET:
		return 1251;
		case EASTEUROPE_CHARSET:
		return 1250;
	case GREEK_CHARSET:
		return 1253;
		case TURKISH_CHARSET:
		return 1254;
		case BALTIC_CHARSET:
		return 1257;
		case HEBREW_CHARSET:
		return 1255;
		case ARABIC_CHARSET:
		return 1256;
		case SHIFTJIS_CHARSET:
		return 932;
		case HANGEUL_CHARSET:
		return 949;
		case CHINESEBIG5_CHARSET:
		return 950;
		default:
		LOG_ERROR(L"Unknown charset "<<charset);
	}
	return -1;
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
	if(res!=S_OK||!pString||cString<=0||!pssa||!allow_ScriptStringAnalyseArgsByAnalysis) return res;
	EnterCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
	if(!allow_ScriptStringAnalyseArgsByAnalysis) {
		LeaveCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
		return res;
	}
	//Record information such as the origianl string and a way we can identify it later.
	ScriptStringAnalyseArgs_t args={hdc,pString,cString,iCharset,dwFlags};
	ScriptStringAnalyseArgsByAnalysis[*pssa]=args;
	LeaveCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
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
	if(res!=S_OK||!pssa||!allow_ScriptStringAnalyseArgsByAnalysis) return res;
	EnterCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
	if(!allow_ScriptStringAnalyseArgsByAnalysis) {
		LeaveCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
		return res;
	}
	//Get rid of unneeded info
	ScriptStringAnalyseArgsByAnalysis.erase(*pssa);
	LeaveCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
	return res; 
}

//ScriptStringOut hook function
//Hooked so we can detect when glyphs previously converted with ScriptStringAnalyse are being outputted.
typedef HRESULT(WINAPI *ScriptStringOut_funcType)(SCRIPT_STRING_ANALYSIS,int,int,UINT,const RECT*,int,int,BOOL);
ScriptStringOut_funcType real_ScriptStringOut=NULL;
HRESULT WINAPI fake_ScriptStringOut(SCRIPT_STRING_ANALYSIS ssa,int iX,int iY,UINT uOptions,const RECT *prc,int iMinSel,int iMaxSel,BOOL fDisabled) {
	//Call the real ScriptStringOut
	HRESULT res;
	{
		TextInsertionTracker tracker;
		res=real_ScriptStringOut(ssa,iX,iY,uOptions,prc,iMinSel,iMaxSel,fDisabled);
		if(tracker.hasTrackedTextInsertion()) return res;
	}
	//If ScriptStringOut was successful we can go on
	//We also need to acquire access to our Script analysis map
	if(res!=S_OK||!ssa||!allow_ScriptStringAnalyseArgsByAnalysis) return res;
	EnterCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
	if(!allow_ScriptStringAnalyseArgsByAnalysis) {
		LeaveCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
		return res;
	}
	//Find out if we know about these glyphs
	ScriptStringAnalyseArgsByAnalysis_t::iterator i=ScriptStringAnalyseArgsByAnalysis.find(ssa);
	if(i==ScriptStringAnalyseArgsByAnalysis.end()) {
		LeaveCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
		return res;
	} 
	//Try and get/create a displayModel for this DC, and if we can, then record the origianl text for these glyphs
		displayModel_t* model=acquireDisplayModel(i->second.hdc);
	if(!model) {
		LeaveCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
		return res;
	}
	BOOL stripHotkeyIndicator=(i->second.dwFlags&SSA_HIDEHOTKEY||i->second.dwFlags&SSA_HOTKEY);
	//The next two extTextOutHelper calls must keep their direction argument as 1. 
	//This is because ScriptStringAnalyze gave us a string in logical order and therefore we need to make sure that NVDA does not try to detect and possibly reverse.
	if(i->second.iCharset==-1) { //Unicode
		ExtTextOutHelper(model,i->second.hdc,iX,iY,prc,uOptions,GetTextAlign(i->second.hdc),stripHotkeyIndicator,(wchar_t*)(i->second.pString),CP_THREAD_ACP,NULL,i->second.cString,NULL,1);
	} else { // character set
		int codePage=charSetToCodePage(i->second.iCharset);
		ExtTextOutHelper(model,i->second.hdc,iX,iY,prc,uOptions,GetTextAlign(i->second.hdc),stripHotkeyIndicator,(char*)(i->second.pString),codePage,NULL,i->second.cString,NULL,1);
	}
	model->release();
	LeaveCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
	return res;
}

//ScriptTextOut
//Hooked so we can look at the current SCRIPT_ANALYSIS structure being used within an inner call to ExtTextOut
typedef HRESULT(WINAPI *ScriptTextOut_funcType)(const HDC,SCRIPT_CACHE*,int,int,UINT,const RECT*,const SCRIPT_ANALYSIS*,const WCHAR*,int,const WORD*,int,const int*,const int*,const GOFFSET*);
ScriptTextOut_funcType real_ScriptTextOut=NULL;
HRESULT WINAPI fake_ScriptTextOut(const HDC hdc, SCRIPT_CACHE* psc, int x, int y, UINT fuOptions, const RECT* lprc, const SCRIPT_ANALYSIS* psa, const WCHAR* pwcReserved, int iReserved, const WORD* pwGlyphs, int cGlyphs, const int* piAdvanced, const int* piJustify, const GOFFSET* pGoffset) {
	TlsSetValue(tls_index_curScriptTextOutScriptAnalysis,(LPVOID)psa);
	HRESULT res=real_ScriptTextOut(hdc, psc, x, y, fuOptions, lprc, psa, pwcReserved, iReserved, pwGlyphs, cGlyphs, piAdvanced, piJustify, pGoffset);
	TlsSetValue(tls_index_curScriptTextOutScriptAnalysis,NULL);
	return res;
}

//ScrollWindow hook function
typedef BOOL(WINAPI *ScrollWindow_funcType)(HWND,int,int,const RECT*, const RECT*);
ScrollWindow_funcType real_ScrollWindow=NULL;
BOOL WINAPI fake_ScrollWindow(HWND hwnd, int XAmount, int YAmount, const RECT* lpRect, const RECT* lpClipRect) {
	BOOL res=real_ScrollWindow(hwnd,XAmount,YAmount,lpRect,lpClipRect);
	if(!res) return res;
	displayModel_t* model=NULL;
	displayModelsByWindow.acquire();
	displayModelsMap_t<HWND>::iterator i=displayModelsByWindow.find(hwnd);
	if(i!=displayModelsByWindow.end()) {
		model=i->second;
		model->acquire();
	}
	displayModelsByWindow.release();
	if(!model) return res;
	RECT clientRect;
	GetClientRect(hwnd,&clientRect);
	RECT realScrollRect=lpRect?*lpRect:clientRect;
	ClientToScreen(hwnd,(LPPOINT)&realScrollRect);
	ClientToScreen(hwnd,((LPPOINT)&realScrollRect)+1);
	RECT realClipRect=lpClipRect?*lpClipRect:clientRect;
	ClientToScreen(hwnd,(LPPOINT)&realClipRect);
	ClientToScreen(hwnd,((LPPOINT)&realClipRect)+1);
	RECT destRect={realScrollRect.left+XAmount,realScrollRect.top+YAmount,realScrollRect.right+XAmount,realScrollRect.bottom+YAmount};
	model->copyRectangle(realScrollRect,TRUE,TRUE,false,destRect,&realClipRect,NULL);
	model->release();
	return res;
}
 
//ScrollWindowEx hook function
typedef BOOL(WINAPI *ScrollWindowEx_funcType)(HWND,int,int,const RECT*, const RECT*, HRGN, LPRECT,UINT);
ScrollWindowEx_funcType real_ScrollWindowEx=NULL;
BOOL WINAPI fake_ScrollWindowEx(HWND hwnd, int dx, int dy, const RECT* prcScroll, const RECT* prcClip, HRGN hrgnUpdate, LPRECT prcUpdate, UINT flags) {
	BOOL res=real_ScrollWindowEx(hwnd,dx,dy,prcScroll,prcClip,hrgnUpdate,prcUpdate,flags);
	if(!res) return res;
	displayModel_t* model=NULL;
	displayModelsByWindow.acquire();
	displayModelsMap_t<HWND>::iterator i=displayModelsByWindow.find(hwnd);
	if(i!=displayModelsByWindow.end()) {
		model=i->second;
		model->acquire();
	}
	displayModelsByWindow.release();
	if(!model) return res;
	RECT clientRect;
	GetClientRect(hwnd,&clientRect);
	RECT realScrollRect=prcScroll?*prcScroll:clientRect;
	ClientToScreen(hwnd,(LPPOINT)&realScrollRect);
	ClientToScreen(hwnd,((LPPOINT)&realScrollRect)+1);
	RECT realClipRect=prcClip?*prcClip:clientRect;
	ClientToScreen(hwnd,(LPPOINT)&realClipRect);
	ClientToScreen(hwnd,((LPPOINT)&realClipRect)+1);
	RECT destRect={realScrollRect.left+dx,realScrollRect.top+dy,realScrollRect.right+dx,realScrollRect.bottom+dy};
	model->copyRectangle(realScrollRect,TRUE,TRUE,false,destRect,&realClipRect,NULL);
	model->release();
	return res;
}

//DestroyWindow hook function
//Hooked so that we can get rid of  displayModels for windows that are being destroied.
typedef BOOL(WINAPI *DestroyWindow_funcType)(HWND);
DestroyWindow_funcType real_DestroyWindow=NULL;
BOOL WINAPI fake_DestroyWindow(HWND hwnd) {
	//Call the real DestroyWindow
	BOOL res=real_DestroyWindow(hwnd);
	if(res==0) return res;
	//If successful, acquire access to the display model maps and remove the displayModel for this window if it exists.
	displayModelsByWindow.acquire();
	displayModelsMap_t<HWND>::iterator i=displayModelsByWindow.find(hwnd);
	if(i!=displayModelsByWindow.end()) {
		i->second->requestDelete();
		displayModelsByWindow.erase(i);
	}
	displayModelsByWindow.release();
	return res;
}

void gdiHooks_inProcess_initialize() {
	tls_index_textInsertionsCount=TlsAlloc();
	tls_index_curScriptTextOutScriptAnalysis=TlsAlloc();
	//Initialize the timer for text change notifications
	textChangeNotifyTimerID=SetTimer(NULL,NULL,50,textChangeNotifyTimerProc);
	nhAssert(textChangeNotifyTimerID);
	//Initialize critical sections and access variables for various maps
	InitializeCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
	allow_ScriptStringAnalyseArgsByAnalysis=TRUE;
	// Hook needed functions
	apiHook_hookFunction_safe(TextOutA, hookClass_TextOut<char>::fakeFunction, &hookClass_TextOut<char>::realFunction);
	apiHook_hookFunction_safe(TextOutW, hookClass_TextOut<wchar_t>::fakeFunction, &hookClass_TextOut<wchar_t>::realFunction);
	apiHook_hookFunction_safe(PolyTextOutA, hookClass_PolyTextOut<POLYTEXTA>::fakeFunction, &hookClass_PolyTextOut<POLYTEXTA>::realFunction);
	apiHook_hookFunction_safe(PolyTextOutW, hookClass_PolyTextOut<POLYTEXTW>::fakeFunction, &hookClass_PolyTextOut<POLYTEXTW>::realFunction);
	apiHook_hookFunction_safe(ExtTextOutA, hookClass_ExtTextOut<char>::fakeFunction, &hookClass_ExtTextOut<char>::realFunction);
	apiHook_hookFunction_safe(ExtTextOutW, hookClass_ExtTextOut<wchar_t>::fakeFunction, &hookClass_ExtTextOut<wchar_t>::realFunction);
	apiHook_hookFunction_safe(CreateCompatibleDC, fake_CreateCompatibleDC, &real_CreateCompatibleDC);
	apiHook_hookFunction_safe(SelectObject, fake_SelectObject, &real_SelectObject);
	apiHook_hookFunction_safe(DeleteDC, fake_DeleteDC, &real_DeleteDC);
	apiHook_hookFunction_safe(FillRect, fake_FillRect, &real_FillRect);
	apiHook_hookFunction_safe(DrawFocusRect, fake_DrawFocusRect, &real_DrawFocusRect);
	apiHook_hookFunction_safe(BeginPaint, fake_BeginPaint, &real_BeginPaint);
	apiHook_hookFunction_safe(BitBlt, fake_BitBlt, &real_BitBlt);
	apiHook_hookFunction_safe(StretchBlt, fake_StretchBlt, &real_StretchBlt);
	apiHook_hookFunction_safe(GdiTransparentBlt, fake_GdiTransparentBlt, &real_GdiTransparentBlt);
	apiHook_hookFunction_safe(PatBlt, fake_PatBlt, &real_PatBlt);
	apiHook_hookFunction_safe(ScrollWindow, fake_ScrollWindow, &real_ScrollWindow);
	apiHook_hookFunction_safe(ScrollWindowEx, fake_ScrollWindowEx, &real_ScrollWindowEx);
	apiHook_hookFunction_safe(DestroyWindow, fake_DestroyWindow, &real_DestroyWindow);
	apiHook_hookFunction_safe(ScriptStringAnalyse, fake_ScriptStringAnalyse, &real_ScriptStringAnalyse);
	apiHook_hookFunction_safe(ScriptStringFree, fake_ScriptStringFree, &real_ScriptStringFree);
	apiHook_hookFunction_safe(ScriptStringOut, fake_ScriptStringOut, &real_ScriptStringOut);
	apiHook_hookFunction_safe(ScriptTextOut, fake_ScriptTextOut, &real_ScriptTextOut);
}

void gdiHooks_inProcess_terminate() {
	//Kill the text change notification timer
	KillTimer(0,textChangeNotifyTimerID);
	//Cleanup glyph mapping.
	glyphTranslatorCache.cleanup();
	//Acquire access to the maps and clean them up
	displayModelsByWindow.acquire();
	displayModelsMap_t<HWND>::iterator i=displayModelsByWindow.begin();
	while(i!=displayModelsByWindow.end()) {
		i->second->requestDelete();
		displayModelsByWindow.erase(i++);
	}  
	displayModelsByWindow.release();
	displayModelsByMemoryDC.acquire();
	displayModelsMap_t<HDC>::iterator j=displayModelsByMemoryDC.begin();
	while(j!=displayModelsByMemoryDC.end()) {
		j->second->requestDelete();
		displayModelsByMemoryDC.erase(j++);
	}  
	displayModelsByMemoryDC.release();
	EnterCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
	allow_ScriptStringAnalyseArgsByAnalysis=FALSE;
	ScriptStringAnalyseArgsByAnalysis.clear();
	LeaveCriticalSection(&criticalSection_ScriptStringAnalyseArgsByAnalysis);
	TlsFree(tls_index_textInsertionsCount);
	TlsFree(tls_index_curScriptTextOutScriptAnalysis);
}
