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

#include <map>
#include <windows.h>
#include <wchar.h>
#include <msctf.h>
#include <common/log.h>
#include <common/lock.h>
#include "nvdaHelperRemote.h"
#include <remote/nvdaControllerInternal.h>
#include "typedCharacter.h"
#include "ime.h"
#include "tsf.h"
#include "inputLangChange.h"

using namespace std;

CLSID curTSFClsID={0, 0, 0, {0, 0, 0, 0, 0, 0, 0, 0}};


bool fetchRangeExtent(ITfRange* pRange, long* start, ULONG* length) {
	HRESULT res=S_OK;
	if(!pRange) return false;
	ITfRangeACP* pRangeACP=NULL;
	res=pRange->QueryInterface(IID_ITfRangeACP,(void**)&pRangeACP);
	if(res!=S_OK||!pRangeACP) return false;
	res=pRangeACP->GetExtent(start,(long*)length);
	pRangeACP->Release();
	return true?(res==S_OK):false;
}

class TsfSink;
typedef map<DWORD,TsfSink*> sinkMap_t;

static DWORD gTsfIndex = TLS_OUT_OF_INDEXES;
static sinkMap_t gTsfSinks;
static LockableObject gTsfSinksLock;
static PVOID gLastCompStr = NULL;

class TsfSink : public ITfThreadMgrEventSink, public ITfTextEditSink, public ITfUIElementSink, public ITfInputProcessorProfileActivationSink {
public:
	TsfSink();
	~TsfSink();

	// Initializes object after creation
	bool Initialize();

	// Cleans up object before destruction
	void CleanUp();

	// IUnknown methods
	STDMETHODIMP QueryInterface(REFIID, LPVOID*);
	STDMETHODIMP_(ULONG) AddRef();
	STDMETHODIMP_(ULONG) Release();

	// ITfThreadMgrEventSink methods
	STDMETHODIMP OnInitDocumentMgr(ITfDocumentMgr*);
	STDMETHODIMP OnUninitDocumentMgr(ITfDocumentMgr*);
	STDMETHODIMP OnSetFocus(ITfDocumentMgr*, ITfDocumentMgr*);
	STDMETHODIMP OnPushContext(ITfContext*);
	STDMETHODIMP OnPopContext(ITfContext*);

	// ITfTextEditSink methods
	STDMETHODIMP OnEndEdit(ITfContext*, TfEditCookie, ITfEditRecord*);

	// ITfInputProcessorProfileActivationSink methods
	STDMETHODIMP OnActivated(DWORD dwProfileType, LANGID langId, REFCLSID rclsid, REFGUID catId, REFGUID guidProfile, HKL hkl, DWORD dwFlags);

	// ITfUIElementSink methods
	STDMETHODIMP BeginUIElement(DWORD, BOOL*);
	STDMETHODIMP UpdateUIElement(DWORD);
	STDMETHODIMP EndUIElement(DWORD);

	//Is TSF actually being used for this thread?
	bool hasActiveProfile;

private:
	LONG          mRefCount;
	ITfThreadMgr* mpThreadMgr;
	ITfSource*    mpTextEditSrc;
	ITfUIElementMgr* mpUIElementMgr;
	DWORD         mThreadMgrCookie;
	DWORD         mLangProfCookie;
	DWORD         mTextEditCookie;
	DWORD         mUIElementCookie;
	DWORD curReadingInformationUIElementId;
	bool inComposition;

	void UpdateTextEditSink(ITfDocumentMgr* docMgr);
	void RemoveTextEditSink();
	WCHAR* HandleCompositionView(ITfContext* pCtx, TfEditCookie cookie);
	WCHAR* HandleEditRecord(TfEditCookie cookie, ITfEditRecord* pEditRec);
	IEnumITfCompositionView* GetCompViewEnum(ITfContext* pCtx);
	ITfRange* CombineCompRange(ITfContext* pCtx, TfEditCookie cookie);
};

typedef HRESULT (WINAPI* TF_GetThreadMgr_t)(ITfThreadMgr**);
typedef HRESULT (WINAPI* TF_CreateThreadMgr_t)(ITfThreadMgr**);

ITfThreadMgr*
create_thread_manager() {
	ITfThreadMgr* mgr = NULL;
	HMODULE dll = LoadLibraryA("msctf.dll");
	if (!dll)  return NULL;
	TF_GetThreadMgr_t get_func =
		(TF_GetThreadMgr_t)GetProcAddress(dll, "TF_GetThreadMgr");
	if (get_func)  get_func(&mgr);
	/*
	if (!mgr) {
		TF_CreateThreadMgr_t create_func =
			(TF_CreateThreadMgr_t)GetProcAddress(dll, "TF_CreateThreadMgr");
		if (create_func)  create_func(&mgr);
	}
	*/
	FreeLibrary(dll);
	return mgr;
}

typedef HRESULT (WINAPI* TF_CreateInputProcessorProfiles_t)(ITfInputProcessorProfiles**);

ITfInputProcessorProfiles*
create_input_processor_profiles() {
	ITfInputProcessorProfiles* profiles = NULL;
	HMODULE dll = LoadLibraryA("msctf.dll");
	if (!dll)  return NULL;
	TF_CreateInputProcessorProfiles_t func =
		(TF_CreateInputProcessorProfiles_t)GetProcAddress(dll, "TF_CreateInputProcessorProfiles");
	if (func)  func(&profiles);
	FreeLibrary(dll);
	return profiles;
}

TsfSink::TsfSink() {
	mRefCount        = 1;
	mpThreadMgr      = NULL;
	mpTextEditSrc    = NULL;
	mpUIElementMgr=NULL;
	mThreadMgrCookie = TF_INVALID_COOKIE;
	mLangProfCookie  = TF_INVALID_COOKIE;
	mTextEditCookie  = TF_INVALID_COOKIE;
	mUIElementCookie = TF_INVALID_COOKIE;
	curReadingInformationUIElementId=-1;
	inComposition=false;
	int lastCompositionStartOffset=0;
	hasActiveProfile=false;
}

TsfSink::~TsfSink() {
}

bool TsfSink::Initialize() {
	mpThreadMgr = create_thread_manager();
	if(!mpThreadMgr) return false;
	HRESULT hr = S_OK;
	ITfSource* src = NULL;
	if (hr == S_OK) {
		hr = mpThreadMgr->QueryInterface(IID_ITfSource, (void**)&src);
	}
	if (src) {
		if (hr == S_OK) {
			hr = src->AdviseSink(IID_ITfThreadMgrEventSink,
				(ITfThreadMgrEventSink*)this, &mThreadMgrCookie);
		}
		if (hr == S_OK) {
			hr = src->AdviseSink(IID_ITfInputProcessorProfileActivationSink,(ITfInputProcessorProfileActivationSink*)this, &mLangProfCookie);
		}
		if (hr == S_OK) {
			hr = mpThreadMgr->QueryInterface(IID_ITfUIElementMgr,(void**)&mpUIElementMgr);
		}
		if (hr == S_OK) {
			hr = src->AdviseSink(IID_ITfUIElementSink,(ITfUIElementSink*)this, &mUIElementCookie);
		}
		src->Release();
		src = NULL;
	}
	ITfDocumentMgr* doc_mgr = NULL;
	mpThreadMgr->GetFocus(&doc_mgr);
	if (doc_mgr) {
		UpdateTextEditSink(doc_mgr);
		doc_mgr->Release();
	}
	//Check to see if there is an active TSF language profile and set hasActiveProfile accordingly.
	ITfInputProcessorProfiles* profiles = create_input_processor_profiles();
	if(profiles) {
		LANGID  lang = 0;
		profiles->GetCurrentLanguage(&lang);
		if(lang) {
			IEnumTfLanguageProfiles* pEnumTfLanguageProfiles=NULL;
			profiles->EnumLanguageProfiles(lang,&pEnumTfLanguageProfiles);
			if(pEnumTfLanguageProfiles) {
				TF_LANGUAGEPROFILE profile;
				ULONG fetched=0;
				while(pEnumTfLanguageProfiles->Next(1,&profile,&fetched)==S_OK&&fetched==1) {
					if(profile.fActive&&IsEqualCLSID(profile.catid,GUID_TFCAT_TIP_KEYBOARD)) {
						hasActiveProfile=true;
						break;
					}
				}
				pEnumTfLanguageProfiles->Release();
			}
		}
		profiles->Release();
	}
	return true;
}

void TsfSink::CleanUp() {
	RemoveTextEditSink();
	if (mpThreadMgr) {
		ITfSource* src = NULL;
		mpThreadMgr->QueryInterface(IID_ITfSource, (void**)&src);
		if (src)
		{
			if (mUIElementCookie != TF_INVALID_COOKIE) {
				src->UnadviseSink(mUIElementCookie);
				mUIElementCookie = TF_INVALID_COOKIE;
			}
			if (mThreadMgrCookie != TF_INVALID_COOKIE) {
				src->UnadviseSink(mThreadMgrCookie);
			}
			if (mLangProfCookie != TF_INVALID_COOKIE) {
				src->UnadviseSink(mLangProfCookie);
			}
			src->Release();
		}
		if(mpUIElementMgr) {
			mpUIElementMgr->Release();
			mpUIElementMgr=NULL;
		}
		mThreadMgrCookie = TF_INVALID_COOKIE;
		mLangProfCookie  = TF_INVALID_COOKIE;
		mpThreadMgr->Release();
		mpThreadMgr = NULL;
	}
	CoUninitialize();
}

void TsfSink::UpdateTextEditSink(ITfDocumentMgr* docMgr) {
	RemoveTextEditSink();
	if (!docMgr)  return;
	ITfContext* ctx = NULL;
	HRESULT hr = docMgr->GetBase(&ctx);
	if (hr == S_OK) {
		hr = ctx->QueryInterface(IID_ITfSource, (void**)&mpTextEditSrc);
		ctx->Release();
	}
	if (hr == S_OK) {
		hr = mpTextEditSrc->AdviseSink(IID_ITfTextEditSink,
			(ITfTextEditSink*)this, &mTextEditCookie);
	}
	if (hr != S_OK) {
		RemoveTextEditSink();
		return;
	}
}

void TsfSink::RemoveTextEditSink() {
	if (mTextEditCookie != TF_INVALID_COOKIE) {
		mpTextEditSrc->UnadviseSink(mTextEditCookie);
		mTextEditCookie = TF_INVALID_COOKIE;
	}
	if (mpTextEditSrc) {
		mpTextEditSrc->Release();
		mpTextEditSrc = NULL;
	}
}

STDMETHODIMP TsfSink::QueryInterface(REFIID riid, LPVOID* ppvObj) {
	if (!ppvObj)  return E_INVALIDARG;
	if (IsEqualIID(riid, IID_IUnknown) ||
			IsEqualIID(riid, IID_ITfThreadMgrEventSink)) {
		*ppvObj = (ITfThreadMgrEventSink*)this;
	} else if (IsEqualIID(riid, IID_ITfInputProcessorProfileActivationSink)) {
		*ppvObj = (ITfInputProcessorProfileActivationSink*)this;
	} else if (IsEqualIID(riid, IID_ITfTextEditSink)) {
		*ppvObj = (ITfTextEditSink*)this;
	} else if (IsEqualIID(riid, IID_ITfUIElementSink)) {
		*ppvObj = (ITfUIElementSink*)this;
	} else {
		*ppvObj = NULL;
		return E_NOINTERFACE;
	}
	AddRef();
	return S_OK;
}

STDMETHODIMP_(ULONG) TsfSink::AddRef() {
	return ++mRefCount;
}

STDMETHODIMP_(ULONG) TsfSink::Release() {
	LONG count = --mRefCount;
	if (count == 0)  delete this;
	return count;
}

STDMETHODIMP TsfSink::OnInitDocumentMgr(ITfDocumentMgr* pDIM) {
	return S_OK;
}

STDMETHODIMP TsfSink::OnUninitDocumentMgr(ITfDocumentMgr* pDIM) {
	return S_OK;
}

STDMETHODIMP TsfSink::OnSetFocus(
		ITfDocumentMgr* pDIM, ITfDocumentMgr* pPrevDIM) {
	UpdateTextEditSink(pDIM);
	return S_OK;
}

STDMETHODIMP TsfSink::OnPushContext(ITfContext* pCtx) {
	return S_OK;
}

STDMETHODIMP TsfSink::OnPopContext(ITfContext* pCtx) {
	return S_OK;
}

IEnumITfCompositionView* TsfSink::GetCompViewEnum(ITfContext* pCtx) {
	// Make sure there is a composition context
	ITfContextComposition* ctx_comp = NULL;
	pCtx->QueryInterface(IID_ITfContextComposition, (void**)&ctx_comp);
	if (!ctx_comp)  return NULL;

	// Obtain composition view enumerator
	IEnumITfCompositionView* enum_view = NULL;
	ctx_comp->EnumCompositions(&enum_view);
	ctx_comp->Release();
	return enum_view;
}

ITfRange* TsfSink::CombineCompRange(ITfContext* pCtx, TfEditCookie cookie) {
	// Make sure there is a composition view enumerator
	IEnumITfCompositionView* enum_view = GetCompViewEnum(pCtx);
	if (!enum_view)  return NULL;

	// Combine composition ranges from all views
	ITfRange*           range = NULL;
	ITfCompositionView* view = NULL;
	while (enum_view->Next(1, &view, NULL) == S_OK) {
		ITfRange *view_range = NULL;
		if (view->GetRange(&view_range) == S_OK) {
			if (!range) {
				view_range->Clone(&range);
			} else {
				range->ShiftEndToRange(cookie, view_range, TF_ANCHOR_END);
			}
			view_range->Release();
		}
		view->Release();
	}
	enum_view->Release();
	return range;
}

WCHAR* TsfSink::HandleCompositionView(ITfContext* pCtx, TfEditCookie cookie) {
	// Make sure there is a composition view enumerator
	IEnumITfCompositionView* enum_view = GetCompViewEnum(pCtx);
	if (!enum_view)  return NULL;

	// Concatenate text in all composition views into composition string
	WCHAR* comp_str = (WCHAR*)malloc(sizeof(WCHAR));
	int    comp_len = 0;
	ITfCompositionView* view = NULL;
	while (enum_view->Next(1, &view, NULL) == S_OK) {
		ITfRange *range;
		if (view->GetRange(&range) == S_OK) {
			BOOL empty;
			while ((range->IsEmpty(cookie, &empty) == S_OK) && !empty) {
				wchar_t buf[256];
				ULONG len = ARRAYSIZE(buf) - 1;
				range->GetText(cookie, TF_TF_MOVESTART, buf, len, &len);
				comp_str = (WCHAR*)realloc(comp_str,
						(comp_len + len + 1) * sizeof(WCHAR));
				CopyMemory(comp_str + comp_len, buf, len * sizeof(WCHAR));
				comp_len += len;
			}
			range->Release();
		}
		view->Release();
	}
	enum_view->Release();

	// Generate notification
	comp_str[comp_len] = '\0';
	if (comp_len > 0)  return comp_str;
	free(comp_str);
	return NULL;
}

WCHAR* TsfSink::HandleEditRecord(TfEditCookie cookie, ITfEditRecord* pEditRec) {
	// Make sure that are is a valid range enumerator
	IEnumTfRanges* enum_range = NULL;
	HRESULT hr = pEditRec->GetTextAndPropertyUpdates(
		TF_GTP_INCL_TEXT, NULL, 0, &enum_range);
	if (!enum_range)  return NULL;

	// Concatenate the text from all ranges
	WCHAR*    edit_str = (WCHAR*)malloc(sizeof(WCHAR));
	int       edit_len = 0;
	ITfRange* range = NULL;
	ULONG     count = 0;
	while ((enum_range->Next(1, &range, &count) == S_OK) && count) {
		BOOL empty;
		while ((range->IsEmpty(cookie, &empty) == S_OK) && !empty) {
			wchar_t buf[256];
			ULONG len = ARRAYSIZE(buf) - 1;
			range->GetText(cookie, TF_TF_MOVESTART, buf, len, &len);
			edit_str = (WCHAR*)realloc(edit_str,
					(edit_len + len + 1) * sizeof(WCHAR));
			CopyMemory(edit_str + edit_len, buf, len * sizeof(WCHAR));
			edit_len += len;
		}
		range->Release();
	}
	enum_range->Release();

	// Generate notification
	edit_str[edit_len] = '\0';
	if (edit_len > 0)  return edit_str;
	free(edit_str);
	return NULL;
}

STDMETHODIMP TsfSink::BeginUIElement(DWORD elementId, BOOL* pShow) {
	if(mpUIElementMgr) {
		ITfUIElement* pUIElement=NULL;
		mpUIElementMgr->GetUIElement(elementId,&pUIElement);
		if(pUIElement) {
			ITfReadingInformationUIElement* pReadingInformationUIElement=NULL;
			pUIElement->QueryInterface(IID_ITfReadingInformationUIElement,(void**)&pReadingInformationUIElement);
			pUIElement->Release();
			if(pReadingInformationUIElement) {
				curReadingInformationUIElementId=elementId;
				pReadingInformationUIElement->Release();
			}
		}
	}
	*pShow=(curReadingInformationUIElementId!=-1)?false:true;
	return S_OK;
}

STDMETHODIMP TsfSink::UpdateUIElement(DWORD elementId) {
	if(elementId==curReadingInformationUIElementId&&mpUIElementMgr) {
		ITfUIElement* pUIElement=NULL;
		mpUIElementMgr->GetUIElement(elementId,&pUIElement);
		if(pUIElement) {
			ITfReadingInformationUIElement* pReadingInformationUIElement=NULL;
			pUIElement->QueryInterface(IID_ITfReadingInformationUIElement,(void**)&pReadingInformationUIElement);
			pUIElement->Release();
			if(pReadingInformationUIElement) {
				BSTR read_str=NULL;
				pReadingInformationUIElement->GetString(&read_str);
				if(read_str) {
					long len=SysStringLen(read_str);
					if(len>0) {
						nvdaControllerInternal_inputCompositionUpdate(read_str,len,len,1);
					}
					SysFreeString(read_str);
				}
				pReadingInformationUIElement->Release();
			}
		}
	}
	return S_OK;
}

STDMETHODIMP TsfSink::EndUIElement(DWORD elementId) {
	if(elementId==curReadingInformationUIElementId) curReadingInformationUIElementId=-1;
	return S_OK;
}

STDMETHODIMP TsfSink::OnEndEdit(
		ITfContext* pCtx, TfEditCookie cookie, ITfEditRecord* pEditRec) {
	// TSF input processor performing composition
	ITfRange* pRange=CombineCompRange(pCtx,cookie);
	if(!pRange) {
		if(inComposition) {
			inComposition=false;
			if(!curIMEWindow) {
				wchar_t* edit_str=HandleEditRecord(cookie, pEditRec);
				nvdaControllerInternal_inputCompositionUpdate((edit_str?edit_str:L""),-1,-1,0);
				if(edit_str) free(edit_str);
				//Disable further typed character notifications produced by TSF
				typedCharacter_window=NULL;
			}
		}
		return S_OK;
	}
	inComposition=true;
	wchar_t buf[256];
	ULONG len = ARRAYSIZE(buf) - 1;
	pRange->GetText(cookie, 0, buf, len, &len);
	buf[min(len,255)]=L'\0';
	long compStart=0;
	fetchRangeExtent(pRange,&compStart,&len);
	long selStart=compStart;
	long selEnd=compStart;
	TF_SELECTION tfSelection={0};
	if(pCtx->GetSelection(cookie,TF_DEFAULT_SELECTION,1,&tfSelection,&len)==S_OK&&tfSelection.range) {
		if(fetchRangeExtent(tfSelection.range,&selStart,&len)) {
			selEnd=selStart+len;
		}
		tfSelection.range->Release();
	}
	selStart=max(0,selStart-compStart);
	selEnd=max(0,selEnd-compStart);
	nvdaControllerInternal_inputCompositionUpdate(buf,selStart,selEnd,0);
	return S_OK;
}

STDMETHODIMP TsfSink::OnActivated(DWORD dwProfileType, LANGID langId, REFCLSID rclsid, REFGUID catId, REFGUID guidProfile, HKL hkl, DWORD dwFlags) {
	const CLSID null_clsid = {0, 0, 0, {0, 0, 0, 0, 0, 0, 0, 0}};
	if(dwProfileType==TF_PROFILETYPE_KEYBOARDLAYOUT) {
		//This is a normal keyboard layout, so forget any last active TSF profile
		hasActiveProfile=false;
		curTSFClsID=null_clsid;
		if(dwFlags&TF_IPSINK_FLAG_ACTIVE) {
			//As it is activating, report the layout change to NVDA
			wchar_t buf[KL_NAMELENGTH];
			GetKeyboardLayoutName(buf);
			nvdaControllerInternal_inputLangChangeNotify(GetCurrentThreadId(),HandleToUlong(GetKeyboardLayout(0)), buf);
			handleIMEConversionModeUpdate(GetFocus(),true);
		}
		return S_OK;
	}
	//From here on this is a text service change
	if(!IsEqualCLSID(catId,GUID_TFCAT_TIP_KEYBOARD)) {
		//We don't handle anything other than keyboard text services (no speech etc)
		return S_OK;
	}
	if(!(dwFlags&TF_IPSINK_FLAG_ACTIVE)) {
		//This keyboard text service is deactivating
		curTSFClsID=null_clsid;
		hasActiveProfile=false;
		return S_OK;
	}
	curTSFClsID=rclsid;
	hasActiveProfile = true;
	ITfInputProcessorProfiles* profiles = create_input_processor_profiles();
	if (!profiles)  return S_OK;
	BSTR desc = NULL;
	profiles->GetLanguageProfileDescription(rclsid, langId, guidProfile, &desc);
	if (desc) {
		nvdaControllerInternal_inputLangChangeNotify(GetCurrentThreadId(),HandleToUlong(GetKeyboardLayout(0)), desc);
		SysFreeString(desc);
	}
	profiles->Release();
	handleIMEConversionModeUpdate(GetFocus(),true);
	return S_OK;
}

static void CALLBACK TSF_winEventHook(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time) { 
	switch (eventID)
	{
		case EVENT_SYSTEM_FOREGROUND:
		case EVENT_OBJECT_FOCUS:
			// Create TSF sink when window gains focus
			break;
		default:
			// Ignore all other events
			return;
	}

	// Create TSF sink now
	if (TlsGetValue(gTsfIndex))  return;
	TsfSink* sink = new TsfSink;
	if (!sink)  return;
	if(!sink->Initialize()) {
		sink->Release();
		return;
	}
	gTsfSinksLock.acquire();
	gTsfSinks[GetCurrentThreadId()] = sink;
	gTsfSinksLock.release();
	TlsSetValue(gTsfIndex, sink);
}

TsfSink* fetchCurrentTsfSink() {
	if (gTsfIndex == TLS_OUT_OF_INDEXES)  return NULL;
	return (TsfSink*)TlsGetValue(gTsfIndex);
}

void TSF_inProcess_initialize() {
	// Initialize TLS and use window hook to create TSF sink in each thread
	gTsfIndex = TlsAlloc();
	if (gTsfIndex != TLS_OUT_OF_INDEXES)
		registerWinEventHook(TSF_winEventHook);
}

void TSF_inProcess_terminate() {
	if (gTsfIndex == TLS_OUT_OF_INDEXES)  return;

	// Remove window hook and clean up TLS
	unregisterWinEventHook(TSF_winEventHook);
	TlsFree(gTsfIndex);
	gTsfIndex = TLS_OUT_OF_INDEXES;

	// Destroy all TSF sinks belonging to this process
	gTsfSinksLock.acquire();
	sinkMap_t::const_iterator end = gTsfSinks.end();
	for (sinkMap_t::const_iterator i = gTsfSinks.begin();  i != end;  ++i) {
		TsfSink* sink = i->second;
		sink->CleanUp();
		sink->Release();
	}
	gTsfSinks.clear();
	gTsfSinksLock.release();
}

void TSF_thread_detached() {
	TsfSink* sink=fetchCurrentTsfSink();
	// Remove TSF sink from the list
	gTsfSinksLock.acquire();
	gTsfSinks.erase(GetCurrentThreadId());
	gTsfSinksLock.release();

	// Destroy TSF sink belonging to this thread
	TlsSetValue(gTsfIndex, NULL);
	sink->CleanUp();
	sink->Release();
}

bool isTSFThread(bool checkActiveProfile) {
	TsfSink* tsf=fetchCurrentTsfSink();
	if(!tsf) return false; 
	return checkActiveProfile?tsf->hasActiveProfile:true;
}
