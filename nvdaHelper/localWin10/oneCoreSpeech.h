/*
Header for C dll bridge to Windows OneCore voices.
This file is a part of the NVDA project.
URL: http://www.nvaccess.org/
Copyright 2016-2022 Tyler Spivey, NV Access Limited.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#pragma once
#define export __declspec(dllexport)

using ocSpeech_CallbackT = void(BYTE* data, int length, const wchar_t* markers);
typedef void (*ocSpeech_Callback)(BYTE* data, int length, const wchar_t* markers);

extern "C" {
	export bool __stdcall ocSpeech_supportsProsodyOptions();
	export void* __stdcall ocSpeech_initialize(ocSpeech_Callback fn);
	export void __stdcall ocSpeech_terminate(void* token);
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
