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
#include "nvdaControllerInternal.h"
#include "typedCharacter.h"
#include "tsf.h"
#include "ime.h"

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

static HMODULE gImm32Module = NULL;
static DWORD lastConversionModeFlags=0;
bool disableIMEConversionModeUpdateReporting=false;

static LPINPUTCONTEXT2 (WINAPI* immLockIMC)(HIMC) = NULL;
static BOOL (WINAPI* immUnlockIMC)(HIMC) = NULL;
static LPVOID (WINAPI* immLockIMCC)(HIMCC) = NULL;
static BOOL (WINAPI* immUnlockIMCC)(HIMCC) = NULL;

void handleIMEConversionModeUpdate(HWND hwnd, bool report) {
	/* Obtain IME context */
	HIMC imc = ImmGetContext(hwnd);
	if (!imc)  return;
	DWORD flags=0;
	ImmGetConversionStatus(imc,&flags,NULL);
	ImmReleaseContext(hwnd, imc);
	if(report&&flags!=lastConversionModeFlags) {
		nvdaControllerInternal_inputConversionModeUpdate(lastConversionModeFlags,flags);
	}
	lastConversionModeFlags=flags;
}

static bool handleCandidates(HWND hwnd) {
	/* Obtain IME context */
	HIMC imc = ImmGetContext(hwnd);
	if (!imc)  return false;

	/* Make sure there is at least one candidate list */
	DWORD count = 0;
	DWORD len = ImmGetCandidateListCountW(imc, &count);
	if (!count) {
		ImmReleaseContext(hwnd, imc);
		return false;
	}

	/* Read first candidate list */
	CANDIDATELIST* list = (CANDIDATELIST*)malloc(len);
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
	WCHAR* cand_str = (WCHAR*)malloc(len);
	WCHAR* ptr = cand_str;
	for (DWORD n = list->dwPageStart, count = 0;  n < pageEnd;  ++n) {
		DWORD offset = list->dwOffset[n];
		WCHAR* cand = (WCHAR*)(((char*)list) + offset);
		size_t clen = wcslen(cand);
		if (!clen)  continue;
		CopyMemory(ptr, cand, (clen + 1) * sizeof(WCHAR));
		if ((n + 1) < pageEnd)  ptr[clen] = '\n';
		ptr += (clen + 1);
		++count;
	}
	if(cand_str&&wcslen(cand_str)>0) {
		nvdaControllerInternal_inputCandidateListUpdate(cand_str,selection);
	}
	/* Clean up */
	free(cand_str);
	free(list);
	return (count > 0);
}

static WCHAR* getCompositionString(HIMC imc, DWORD index) {
	int len = ImmGetCompositionStringW(imc, index, 0, 0);
	if (len < sizeof(WCHAR))  return NULL;
	WCHAR* wstr = (WCHAR*)malloc(len + sizeof(WCHAR));
	len = ImmGetCompositionStringW(imc, index, wstr, len) / sizeof(WCHAR);
	wstr[len] = '\0';
	 return wstr;
}

static bool handleComposition(HWND hwnd, WPARAM wParam, LPARAM lParam) {
	/* Obtain IME context */
	HIMC imc = ImmGetContext(hwnd);
	if (!imc)  return false;

	wchar_t* comp_str = getCompositionString(imc, GCS_COMPSTR);
	long selectionStart=ImmGetCompositionString(imc,GCS_CURSORPOS,NULL,0)&0xffff;
	ImmReleaseContext(hwnd, imc);

	/* Generate notification */
	if(comp_str) {
		nvdaControllerInternal_inputCompositionUpdate(comp_str,selectionStart,selectionStart,0);
		free(comp_str);
		return true;
	}
	return false;
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

static LRESULT CALLBACK IME_callWndProcHook(int code, WPARAM wParam, LPARAM lParam) {
	CWPSTRUCT* pcwp=(CWPSTRUCT*)lParam;
	// Ignore messages with invalid HIMC
	if(!hasValidIMEContext(pcwp->hwnd)) return 0; 
	switch (pcwp->message) {
		case WM_IME_NOTIFY:
			switch (pcwp->wParam) {
				case IMN_OPENCANDIDATE:
				case IMN_CHANGECANDIDATE:
					if(!isTSFThread(true)) handleCandidates(pcwp->hwnd);
					break;

				case IMN_CLOSECANDIDATE:
					if(!isTSFThread(true)) nvdaControllerInternal_inputCandidateListUpdate(L"",-1);
					break;

				case IMN_SETCONVERSIONMODE:
					if(!disableIMEConversionModeUpdateReporting) handleIMEConversionModeUpdate(pcwp->hwnd,true);
					break;
			}

		case WM_IME_COMPOSITION:
			if(!isTSFThread(true)) handleComposition(pcwp->hwnd, pcwp->wParam, pcwp->lParam);
			break;

		case WM_IME_ENDCOMPOSITION:
			if(!isTSFThread(true)) {
				handleEndComposition(pcwp->hwnd, pcwp->wParam, pcwp->lParam);
				//Disable further typed character notifications produced by TSF
				typedCharacter_window=NULL;
			}
			break;

		case WM_ACTIVATE:
		case WM_SETFOCUS:
			handleIMEConversionModeUpdate(pcwp->hwnd,false);
			if(!isTSFThread(true)) {
				if (pcwp->hwnd != GetFocus())  break;
				handleComposition(pcwp->hwnd, pcwp->wParam, pcwp->lParam);
				handleCandidates(pcwp->hwnd);
			}
			break;
		default:
			break;
	}
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

void IME_inProcess_initialize() {
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
}

void IME_inProcess_terminate() {
	unregisterWindowsHook(WH_CALLWNDPROC, IME_callWndProcHook);
	if (gImm32Module)  FreeLibrary(gImm32Module);
}
