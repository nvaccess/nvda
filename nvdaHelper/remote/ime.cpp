/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2010-2012 World Light Information Limited and Hong Kong Blind Union.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#include <windows.h>
#include <wchar.h>
#include "nvdaHelperRemote.h"
#include <remote/nvdaControllerInternal.h>
#include "typedCharacter.h"
#include "tsf.h"
#include <common/log.h>
#include "ime.h"

#define GETLANG()		LOWORD(g_hklCurrent)
#define GETPRIMLANG()	((WORD)PRIMARYLANGID(GETLANG()))
#define GETSUBLANG()	SUBLANGID(GETLANG())

#define LANG_CHS MAKELANGID(LANG_CHINESE, SUBLANG_CHINESE_SIMPLIFIED)
#define LANG_CHT MAKELANGID(LANG_CHINESE, SUBLANG_CHINESE_TRADITIONAL)

#define MAKEIMEVERSION(major,minor) ( (DWORD)( ( (BYTE)( major ) << 24 ) | ( (BYTE)( minor ) << 16 ) ) )
#define IMEID_VER(dwId)		( ( dwId ) & 0xffff0000 )
#define IMEID_LANG(dwId)	( ( dwId ) & 0x0000ffff )

#define _CHT_HKL_DAYI				( (HKL)(ULONG_PTR)0xE0060404 )	// DaYi
#define _CHT_HKL_NEW_PHONETIC		( (HKL)(ULONG_PTR)0xE0080404 )	// New Phonetic
#define _CHT_HKL_NEW_CHANG_JIE		( (HKL)(ULONG_PTR)0xE0090404 )	// New Chang Jie
#define _CHT_HKL_NEW_QUICK			( (HKL)(ULONG_PTR)0xE00A0404 )	// New Quick
#define _CHT_HKL_HK_CANTONESE		( (HKL)(ULONG_PTR)0xE00B0404 )	// Hong Kong Cantonese
#define _CHT_IMEFILENAME	"TINTLGNT.IME"	// New Phonetic
#define _CHT_IMEFILENAME2	"CINTLGNT.IME"	// New Chang Jie
#define _CHT_IMEFILENAME3	"MSTCIPHA.IME"	// Phonetic 5.1
#define IMEID_CHT_VER42 ( LANG_CHT | MAKEIMEVERSION( 4, 2 ) )	// New(Phonetic/ChanJie)IME98  : 4.2.x.x // Win98
#define IMEID_CHT_VER43 ( LANG_CHT | MAKEIMEVERSION( 4, 3 ) )	// New(Phonetic/ChanJie)IME98a : 4.3.x.x // Win2k
#define IMEID_CHT_VER44 ( LANG_CHT | MAKEIMEVERSION( 4, 4 ) )	// New ChanJie IME98b          : 4.4.x.x // WinXP
#define IMEID_CHT_VER50 ( LANG_CHT | MAKEIMEVERSION( 5, 0 ) )	// New(Phonetic/ChanJie)IME5.0 : 5.0.x.x // WinME
#define IMEID_CHT_VER51 ( LANG_CHT | MAKEIMEVERSION( 5, 1 ) )	// New(Phonetic/ChanJie)IME5.1 : 5.1.x.x // IME2002(w/OfficeXP)
#define IMEID_CHT_VER52 ( LANG_CHT | MAKEIMEVERSION( 5, 2 ) )	// New(Phonetic/ChanJie)IME5.2 : 5.2.x.x // IME2002a(w/WinXP)
#define IMEID_CHT_VER60 ( LANG_CHT | MAKEIMEVERSION( 6, 0 ) )	// New(Phonetic/ChanJie)IME6.0 : 6.0.x.x // New IME 6.0(web download)
#define IMEID_CHT_VER_VISTA ( LANG_CHT | MAKEIMEVERSION( 7, 0 ) )	// All TSF TIP under Cicero UI-less mode: a hack to make GetImeId() return non-zero value

#define _CHS_HKL		( (HKL)(ULONG_PTR)0xE00E0804 )	// MSPY
#define _CHS_IMEFILENAME	"PINTLGNT.IME"	// MSPY1.5/2/3
#define _CHS_IMEFILENAME2	"MSSCIPYA.IME"	// MSPY3 for OfficeXP
#define IMEID_CHS_VER41	( LANG_CHS | MAKEIMEVERSION( 4, 1 ) )	// MSPY1.5	// SCIME97 or MSPY1.5 (w/Win98, Office97)
#define IMEID_CHS_VER42	( LANG_CHS | MAKEIMEVERSION( 4, 2 ) )	// MSPY2	// Win2k/WinME
#define IMEID_CHS_VER53	( LANG_CHS | MAKEIMEVERSION( 5, 3 ) )	// MSPY3	// WinXP

// Definition from Win98DDK version of IMM.H
typedef struct tagINPUTCONTEXT2 {
    HWND            hWnd;                           
    BOOL            fOpen;                          
    POINT           ptStatusWndPos;                 
    POINT           ptSoftKbdPos;                   
    DWORD           fdwConversion;                  
    DWORD           fdwSentence;                    
    union {                                           
        LOGFONTA    A;                              
        LOGFONTW    W;                              
    } lfFont;                                           
    COMPOSITIONFORM cfCompForm;                     
    CANDIDATEFORM   cfCandForm[4];                  
    HIMCC           hCompStr;                       
    HIMCC           hCandInfo;                      
    HIMCC           hGuideLine;                     
    HIMCC           hPrivate;                       
    DWORD           dwNumMsgBuf;                    
    HIMCC           hMsgBuf;                        
    DWORD           fdwInit;                        
    DWORD           dwReserve[3];                   
} INPUTCONTEXT2, *PINPUTCONTEXT2, NEAR *NPINPUTCONTEXT2, FAR *LPINPUTCONTEXT2;  

HWND curIMEWindow=NULL;
static HWND candidateIMEWindow=0;
static BOOL lastOpenStatus=true;
static HMODULE gImm32Module = NULL;
static DWORD lastConversionModeFlags=0;

UINT wm_candidateChange=0;
UINT wm_handleIMEConversionModeUpdate=0;

static LPINPUTCONTEXT2 (WINAPI* immLockIMC)(HIMC) = NULL;
static BOOL (WINAPI* immUnlockIMC)(HIMC) = NULL;
static LPVOID (WINAPI* immLockIMCC)(HIMCC) = NULL;
static BOOL (WINAPI* immUnlockIMCC)(HIMCC) = NULL;


DWORD getIMEVersion(HKL kbd_layout, wchar_t* filename) {
	DWORD version=0;
	switch ((DWORD_PTR)kbd_layout) {
		case _CHT_HKL_NEW_PHONETIC:
		case _CHT_HKL_NEW_CHANG_JIE:
		case _CHT_HKL_NEW_QUICK:
		case _CHT_HKL_HK_CANTONESE:
		case _CHS_HKL:
			break;
		default:
			// Do not know how to extract version number
			return 0;
	}
	DWORD buf_size = GetFileVersionInfoSizeW(
		filename,
		nullptr  // lpdwHandle
	);
	if (!buf_size)  return 0;
	void* buf = malloc(buf_size);
	if (!buf) {
		return 0;
	}
	const auto gotFileVerInfo = GetFileVersionInfoW(
		filename,
		0,  // dwHandle
		buf_size,
		buf
	);
	if (gotFileVerInfo) {
		void* data = NULL;
		UINT  data_len;
		if (VerQueryValueW(buf, L"\\", &data, &data_len)) {
			VS_FIXEDFILEINFO FAR* info = (VS_FIXEDFILEINFO FAR*)data;
			version = (info->dwFileVersionMS & 0x00ff0000) << 8
					| (info->dwFileVersionMS & 0x000000ff) << 16
					| HandleToUlong(kbd_layout) & 0xffff;
		}
	}
	free(buf);
	return version;
}

bool getTIPFilename(REFCLSID clsid, WCHAR* filename, DWORD len) {
	// Format registry path for CLSID
	WCHAR reg_path[100]{};
	_snwprintf(reg_path, ARRAYSIZE(reg_path),
		L"CLSID\\{%08X-%04X-%04X-%02X%02X-%02X%02X%02X%02X%02X%02X}\\InProcServer32",
		clsid.Data1, clsid.Data2, clsid.Data3,
		clsid.Data4[0], clsid.Data4[1], clsid.Data4[2], clsid.Data4[3],
		clsid.Data4[4], clsid.Data4[5], clsid.Data4[6], clsid.Data4[7]);
	HKEY reg_key = NULL;
	// ensure null terminated for the case where the formatted string is longer than the reg_path buffer
	// see _snwprintf docs
	reg_path[99] = '\0';
	RegOpenKeyW(HKEY_CLASSES_ROOT, reg_path, &reg_key);
	if (!reg_key)  return false;
	DWORD type = REG_NONE;
	DWORD l = 0;
	bool  result = false;
	if ((ERROR_SUCCESS == RegQueryValueExW(reg_key, 0, 0, &type, 0, &l)) &&
			(type == REG_SZ) && (l > 0) && (len >= l)) {
		if (ERROR_SUCCESS ==
				RegQueryValueExW(reg_key, 0, 0, 0, (LPBYTE)filename, &len)) {
			filename[len] = '\0';
			result = true;
		}
	}
	RegCloseKey(reg_key);
	return result;
}

typedef UINT (WINAPI* GetReadingString_funcType)(HIMC, UINT, LPWSTR, PINT, BOOL*, PUINT);

void handleOpenStatus(HWND hwnd) {
	//Only reported for japanese
	if((HandleToUlong(GetKeyboardLayout(0))&0xff)!=0x11) return;
	/* Obtain IME context */
	HIMC imc = ImmGetContext(hwnd);
	if (!imc)  return;
	BOOL opened=ImmGetOpenStatus(imc);
	if(opened!=lastOpenStatus) {
		nvdaControllerInternal_IMEOpenStatusUpdate(opened);
		lastOpenStatus=opened;
	}
	ImmReleaseContext(hwnd, imc);
}

void handleReadingStringUpdate(HWND hwnd) {
	/* Obtain IME context */
	HIMC imc = ImmGetContext(hwnd);
	if (!imc)  return;
	wchar_t* read_str=NULL;
	HKL kbd_layout = GetKeyboardLayout(0);
	WCHAR filename[MAX_PATH + 1];
	DWORD version=0;
	HMODULE IMEFile=NULL;
	GetReadingString_funcType GetReadingString=NULL;
	if (isTSFThread(true)) {
		// Look up filename of active TIP
		if(getTIPFilename(curTSFClsID, filename, MAX_PATH)) {
			IMEFile=LoadLibrary(filename);
			if(IMEFile) {
				GetReadingString=(GetReadingString_funcType)GetProcAddress(IMEFile, "GetReadingString");
			}
		}
	}
	else if(ImmGetIMEFileNameW(kbd_layout, filename, MAX_PATH)>0) {
		IMEFile=LoadLibrary(filename);
		if(IMEFile) {
			GetReadingString=(GetReadingString_funcType)GetProcAddress(IMEFile, "GetReadingString");
		}
		if(!GetReadingString) {
			version=getIMEVersion(kbd_layout,filename);
		}
	}
	if(GetReadingString) {
		// Use GetReadingString() API if available
		UINT   len = 0;
		INT    err = 0;
		BOOL vert = FALSE;
		UINT max_len = 0;
		len = GetReadingString(imc, 0, NULL, &err, &vert, &max_len);
		if (len) {
			read_str = (WCHAR*)malloc(sizeof(WCHAR) * (len + 1));
			if (!read_str) {
				return;
			}
			read_str[len] = '\0';
			GetReadingString(imc, len, read_str, &err, &vert, &max_len);
		}
	} else if(version) {
		// Read private data in IMCC
		UINT   len = 0;
		INT    err = 0;
		LPINPUTCONTEXT2 ctx = immLockIMC(imc);
		LPBYTE          priv = (LPBYTE)immLockIMCC(ctx->hPrivate);
		LPBYTE          p = 0;
		LPBYTE          str = NULL;
		switch (version) {
			case IMEID_CHT_VER42:
			case IMEID_CHT_VER43:
			case IMEID_CHT_VER44:
				p = *(LPBYTE*)(priv + 24);
				if (!p) break;
				len = *(DWORD*)(p + 7*4 + 32*4);  //m_dwInputReadStrLen
				err = *(DWORD*)(p + 8*4 + 32*4);  //m_dwErrorReadStrStart
				str =          (p + 56);
				break;

			case IMEID_CHT_VER51:  // 5.1.x.x // IME2002(w/OfficeXP)
			case IMEID_CHT_VER52:  // 5.2.x.x // (w/whistler)
			case IMEID_CHS_VER53:  // 5.3.x.x // SCIME2k or MSPY3 (w/OfficeXP and Whistler)
				p = *(LPBYTE*)(priv + 4);  // PCKeyCtrlManager
				if (!p) break;
				p = *(LPBYTE*)((LPBYTE)p + 1*4 + 5*4);  // = PCReading = &STypingInfo
				if (!p) break;
				len = *(DWORD*)(p + 1*4 + (16*2+2*4) + 5*4 + 16*2);        //m_dwDisplayStringLength;
				err = *(DWORD*)(p + 1*4 + (16*2+2*4) + 5*4 + 16*2 + 1*4);  //m_dwDisplayErrorStart;
				str =          (p + 1*4 + (16*2+2*4) + 5*4);
				break;

			case IMEID_CHS_VER42:  // 4.2.x.x // SCIME98 or MSPY2 (w/Office2k, Win2k, WinME, etc)
				p = *(LPBYTE*)(priv + 1*4 + 1*4 + 6*4);  // = PCReading = &STypintInfo
				if (!p) break;
				len = *(DWORD*)(p + 1*4 + (16*2+2*4) + 5*4 + 16*2);        //m_dwDisplayStringLength;
				err = *(DWORD*)(p + 1*4 + (16*2+2*4) + 5*4 + 16*2 + 1*4);  //m_dwDisplayErrorStart;
				str =          (p + 1*4 + (16*2+2*4) + 5*4);               //m_tszDisplayString
				break;
		}
		read_str = (WCHAR*)malloc(sizeof(WCHAR) * (len + 1));
		if (!read_str) {
			return;
		}
		read_str[len] = '\0';
		memcpy(read_str, str, sizeof(WCHAR) * len);
		immUnlockIMCC(ctx->hPrivate);
		immUnlockIMC(imc);
	}
	if(IMEFile) FreeLibrary(IMEFile);
	ImmReleaseContext(hwnd, imc);
	if(read_str) {
		long len=(long)wcslen(read_str);
		if(len>1||(len==1&&read_str[0]!=L'\x3000')) {
			long cursorPos=(long)wcslen(read_str);
			nvdaControllerInternal_inputCompositionUpdate(read_str,cursorPos,cursorPos,1);
		}
		free(read_str);
	}
}

void handleIMEConversionModeUpdate(HWND hwnd, bool report) {
	if(!ImmGetProperty(GetKeyboardLayout(0),IGP_CONVERSION)) return;
	/* Obtain IME context */
	HIMC imc = ImmGetContext(hwnd);
	if (!imc)  return;
	DWORD flags=0;
	ImmGetConversionStatus(imc,&flags,NULL);
	ImmReleaseContext(hwnd, imc);
	if(report&&flags!=lastConversionModeFlags) {
		nvdaControllerInternal_inputConversionModeUpdate(lastConversionModeFlags,flags,HandleToUlong(GetKeyboardLayout(0))&0xffff);
	}
	lastConversionModeFlags=flags;
}

inline void handleCandidatesClosed(HWND hwnd) {
	if(!hwnd||hwnd!=candidateIMEWindow) return;
	/* Obtain IME context */
	HIMC imc = ImmGetContext(hwnd);
	if (!imc) {
		candidateIMEWindow=0;
		nvdaControllerInternal_inputCandidateListUpdate(L"",-1,L"");
		return;
	}
	DWORD count = 0;
	DWORD len = ImmGetCandidateListCountW(imc, &count);
	ImmReleaseContext(hwnd, imc);
	if (!count) {
		candidateIMEWindow=0;
		nvdaControllerInternal_inputCandidateListUpdate(L"",-1,L"");
	}
}

static bool handleCandidates(HWND hwnd) {
	/* Obtain IME context */
	HIMC imc = ImmGetContext(hwnd);
	if (!imc)  return false;

	/* Make sure there is at least one candidate list */
	DWORD count = 0;
	ImmGetCandidateListCountW(imc, &count);
	if (!count) {
		ImmReleaseContext(hwnd, imc);
		return false;
	}
	candidateIMEWindow=hwnd;
	/* Read first candidate list */
	DWORD len = ImmGetCandidateList(imc, 0, NULL, 0);
	if(!len) {
		ImmReleaseContext(hwnd, imc);
		return false;
	}
	CANDIDATELIST* list = (CANDIDATELIST*)malloc(len);
	if (!list) {
		return false;
	}
	ImmGetCandidateList(imc, 0, list, len);
	ImmReleaseContext(hwnd, imc);

	/* Determine candidates currently being shown */
	DWORD pageEnd = list->dwPageStart + list->dwPageSize;
	DWORD selection=list->dwSelection-list->dwPageStart;
	if (list->dwPageSize == 0) {
		pageEnd = list->dwCount;
	} else if (pageEnd > list->dwCount) {
		pageEnd = list->dwCount;
	}
	/* Concatenate currently shown candidates into a string */
	size_t buflen = 0;
	for (DWORD n = list->dwPageStart;  n < pageEnd; ++n) {
		DWORD offset = list->dwOffset[n];
		WCHAR* cand = (WCHAR*)(((char*)list) + offset);
		size_t clen = wcslen(cand);
		if(clen>0) {
			buflen += ((clen + 1) * sizeof(WCHAR));
		}
	}
	WCHAR* cand_str = NULL;
	bool cand_updated = false;
	if(buflen>0) {
		cand_str=(WCHAR*)malloc(buflen);
		if (!cand_str) {
			return false;
		}
		WCHAR* ptr = cand_str;
		for (DWORD n = list->dwPageStart; n < pageEnd;  ++n) {
			DWORD offset = list->dwOffset[n];
			WCHAR* cand = (WCHAR*)(((char*)list) + offset);
			size_t clen = wcslen(cand);
			if (!clen)  continue;
			CopyMemory(ptr, cand, (clen + 1) * sizeof(WCHAR));
			if ((n + 1) < pageEnd)  ptr[clen] = '\n';
			ptr += (clen + 1);
		}
		HKL kbd_layout = GetKeyboardLayout(0);
		WCHAR filename[MAX_PATH + 1]={0};
		ImmGetIMEFileNameW(kbd_layout, filename, MAX_PATH);
		nvdaControllerInternal_inputCandidateListUpdate(cand_str,selection,filename);
		cand_updated = true;
		free(cand_str);
	}
	/* Clean up */
	free(list);
	return cand_updated;
}

static WCHAR* getCompositionString(HIMC imc, DWORD index) {
	int len = ImmGetCompositionStringW(imc, index, 0, 0);
	if (len < sizeof(WCHAR))  return NULL;
	WCHAR* wstr = (WCHAR*)malloc(len + sizeof(WCHAR));
	if (!wstr) {
		return nullptr;
	}
	len = ImmGetCompositionStringW(imc, index, wstr, len) / sizeof(WCHAR);
	wstr[len] = L'\0';
	 return wstr;
}

static bool handleComposition(HWND hwnd, WPARAM wParam, LPARAM lParam) {
	/* Obtain IME context */
	HIMC imc = ImmGetContext(hwnd);
	if (!imc)  return false;

	wchar_t* comp_str = getCompositionString(imc, GCS_COMPSTR);
	long selectionStart=ImmGetCompositionString(imc,GCS_CURSORPOS,NULL,0)&0xffff;
	ImmReleaseContext(hwnd, imc);
	if(!comp_str) return false;

	/* Generate notification */
	long len=(long)wcslen(comp_str);
	if(len>1||(len==1&&comp_str[0]!=L'\x3000')) {
		nvdaControllerInternal_inputCompositionUpdate(comp_str,selectionStart,selectionStart,0);
	}
	free(comp_str);
	return true;
}

static bool handleEndComposition(HWND hwnd, WPARAM wParam, LPARAM lParam) {
	/* Obtain IME context */
	HIMC imc = ImmGetContext(hwnd);
	if (!imc)  return false;

	wchar_t* comp_str = getCompositionString(imc, GCS_RESULTSTR);
	ImmReleaseContext(hwnd, imc);
	/* Generate notification */
	nvdaControllerInternal_inputCompositionUpdate((comp_str?comp_str:L""),-1,-1,0);
	if(comp_str) {
		free(comp_str);
		return true;
	}
	return false;
}

bool hasValidIMEContext(HWND hwnd) {
	if(!hwnd) return false;
	bool valid_imc = false;
	HIMC imc = ImmGetContext(hwnd);
	if (imc) {
		LPINPUTCONTEXT2 ctx = immLockIMC(imc);
		if (ctx) {
			if (ctx->hWnd)  valid_imc = true;
			immUnlockIMC(imc);
		}
		ImmReleaseContext(hwnd, imc);
	}
	return valid_imc;
}

static LRESULT handleIMEWindowMessage(HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam) {
	switch (message) {
		case WM_IME_NOTIFY:
			if(!hasValidIMEContext(hwnd)) return 0;
			switch (wParam) {
				case IMN_SETOPENSTATUS:
					handleOpenStatus(hwnd);
					break;
				case IMN_OPENCANDIDATE:
				case IMN_CHANGECANDIDATE:
					PostMessage(hwnd,wm_candidateChange,0,0);
					break;

				case IMN_CLOSECANDIDATE:
					nvdaControllerInternal_inputCandidateListUpdate(L"",-1,L"");
					break;

				case IMN_SETCONVERSIONMODE:
					PostMessage(hwnd,wm_handleIMEConversionModeUpdate,0,0);
					break;

				case IMN_PRIVATE:
					// Needed to support EasyDots IME when TSF is not available
					if (!isTSFThread(true))
						handleReadingStringUpdate(hwnd);
					break;
			}
			break;

		case WM_IME_COMPOSITION:
			if(!hasValidIMEContext(hwnd)) return 0;
			curIMEWindow=hwnd;
			if(!isTSFThread(true)) {\
				if(lParam&GCS_COMPSTR||lParam&GCS_CURSORPOS) {
					handleComposition(hwnd, wParam, lParam);
				}
			}
			break;

		case WM_IME_ENDCOMPOSITION:
			if(!hasValidIMEContext(hwnd)) return 0;
			if(curIMEWindow==hwnd) {
				if(handleEndComposition(hwnd, wParam, lParam)) {
					//Disable further typed character notifications produced by TSF
					typedCharacter_window=NULL;
				}
				curIMEWindow=NULL;
			}
			break;

		case WM_ACTIVATE:
		case WM_SETFOCUS:
			if(!hasValidIMEContext(hwnd)) return 0;
			handleIMEConversionModeUpdate(hwnd,false);
			if(!isTSFThread(true)) {
				if (hwnd != GetFocus())  break;
				handleComposition(hwnd, wParam, lParam);
				handleCandidates(hwnd);
			}
			break;
		default:
			break;
	}
	return 0;
}

static LRESULT CALLBACK IME_callWndProcHook(int code, WPARAM wParam, LPARAM lParam) {
	CWPSTRUCT* pcwp=(CWPSTRUCT*)lParam;
	handleIMEWindowMessage(pcwp->hwnd,pcwp->message,pcwp->wParam,pcwp->lParam);
	return 0;
}

WCHAR* IME_getCompositionString() {
	HWND hwnd = GetFocus();
	if (!hwnd)  return NULL;
	HIMC imc = ImmGetContext(hwnd);
	if (!imc)  return NULL;
	WCHAR* comp_str = getCompositionString(imc, GCS_COMPSTR);
	ImmReleaseContext(hwnd, imc);
	return comp_str;
}

LRESULT CALLBACK IME_getMessageHook(int code, WPARAM wParam, LPARAM lParam) {
	MSG* pmsg=(MSG*)lParam;
	if(pmsg->message==wm_handleIMEConversionModeUpdate) {
		handleIMEConversionModeUpdate(pmsg->hwnd,true);
	} else if(pmsg->message==wm_candidateChange) {
		handleCandidates(pmsg->hwnd);
	} else {
		handleCandidatesClosed(pmsg->hwnd);
	}
	handleIMEWindowMessage(pmsg->hwnd,pmsg->message,pmsg->wParam,pmsg->lParam);
	return 0;
}

void IME_inProcess_initialize() {
	wm_candidateChange=RegisterWindowMessage(L"nvda_wm_candidateChange");
	wm_handleIMEConversionModeUpdate=RegisterWindowMessage(L"nvda_wm_handleIMEConversionModeUpdate");
	gImm32Module = LoadLibraryA("imm32.dll");
	if (gImm32Module) {
		immLockIMC    = (LPINPUTCONTEXT2 (WINAPI*)(HIMC))
			GetProcAddress(gImm32Module, "ImmLockIMC");
		immUnlockIMC  = (BOOL (WINAPI*)(HIMC))
			GetProcAddress(gImm32Module, "ImmUnlockIMC");
		immLockIMCC   = (LPVOID (WINAPI*)(HIMCC))
			GetProcAddress(gImm32Module, "ImmLockIMCC");
		immUnlockIMCC = (BOOL (WINAPI*)(HIMCC))
			GetProcAddress(gImm32Module, "ImmUnlockIMCC");
	}
	registerWindowsHook(WH_CALLWNDPROC, IME_callWndProcHook);
	registerWindowsHook(WH_GETMESSAGE, IME_getMessageHook);
}

void IME_inProcess_terminate() {
	unregisterWindowsHook(WH_CALLWNDPROC, IME_callWndProcHook);
	unregisterWindowsHook(WH_GETMESSAGE, IME_getMessageHook);
	if (gImm32Module)  FreeLibrary(gImm32Module);
}
