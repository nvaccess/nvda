/*
 Copyright (C) 2016-2022 NV Access Limited, Tyler Spivey
 This file may be used under the terms of the GNU General Public License, version 2 or later.
 For more details see: https://www.gnu.org/licenses/gpl-2.0.html

 Windows OneCore voices

 Expected to be used serially (E.G. from python with GIL).
 The token returned from initialize allows error checking on all methods,
 to ensure terminate has not yet been called

 Notes on the approach:
 - Internal function 'speak' is run asynchronously using Windows thread pool.
   Results are passed back to NVDA via a callback, which must still be valid when the results are ready.
   However, terminate will invalidate the callback.
   To protect against this, a locking strategy is used.
   Before the callback is executed a shared_lock is acquired on the mutex, this allows other shared locks
   to be acquired, but prevents unique locks from acquiring the mutex.

 - The lifetime of the winrtSynth instance is managed with a shared_ptr.
   This allows it to be abandoned in terminate, while remaining valid for the duration of 'speak'.
   To debug life-cycle management weak_ptrs are used to observe the reference count.
*/

#pragma once
#define export __declspec(dllexport)

typedef void (*ocSpeech_Callback)(BYTE* data, int length, const wchar_t* markers);

extern "C" {
	export bool __stdcall ocSpeech_supportsProsodyOptions();

	/* Initialize the ocSpeech system. The token returned is used to debug the life cycles of the ocSpeech system.
	* Only one token may be active at a time.
	* @return A token value that should be kept and passed to all ocSpeech functions.
	* Used to verify client and DLL states are aligned.
	*/
	export void* __stdcall ocSpeech_initialize(ocSpeech_Callback fn);

	/* Terminate the ocSpeech system. The given token becomes invalid.
	* Terminate may block while a callback completes.
	* To ensure terminate gets a chance to run, ensure that the callback does not
	* call ocSpeech_speak. Doing so may result in more callbacks before terminate is unblocked.
	* When terminate returns the token should be discarded and the callback will not be called.
	@param token Used to verify dll and client state. Allows detection of synchronization errors.
	*/
	export void __stdcall ocSpeech_terminate(void* token);

	/*
	Send speech text to OneCore, call back to NVDA with synthesized speech.
	@remarks The work is done asynchronously on a background thread.
	@param token Used to verify dll and client state. Allows detection of synchronization errors.
	@param text The text to synthesize.
	*/
	export void __stdcall ocSpeech_speak(void* token, wchar_t* text);

	export BSTR __stdcall ocSpeech_getVoices(void* token);
	export const wchar_t* __stdcall ocSpeech_getCurrentVoiceId(void* token);
	export void __stdcall ocSpeech_setVoice(void* token, int index);
	export const wchar_t* __stdcall ocSpeech_getCurrentVoiceLanguage(void* token);
	export double __stdcall ocSpeech_getPitch(void* token);
	export void __stdcall ocSpeech_setPitch(void* token, double pitch);
	export double __stdcall ocSpeech_getVolume(void* token);
	export void __stdcall ocSpeech_setVolume(void* token, double volume);
	export double __stdcall ocSpeech_getRate(void* token);
	export void __stdcall ocSpeech_setRate(void* token, double rate);
}
