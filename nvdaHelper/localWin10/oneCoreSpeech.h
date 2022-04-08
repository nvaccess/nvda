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

typedef void (*ocSpeech_Callback)(BYTE* data, int length, const wchar_t* markers);

class SpeakThreadGuard {
private:
	static std::atomic_int _speechThreads;
public:
	SpeakThreadGuard();
	~SpeakThreadGuard();
	static bool areCallbacksPending();
};

class OcSpeech {
private:
	winrt::Windows::Media::SpeechSynthesis::SpeechSynthesizer synth{ nullptr };
	ocSpeech_Callback callback;
public:
	OcSpeech();
	winrt::fire_and_forget speak(winrt::hstring text);
	void setCallback(ocSpeech_Callback fn);
	std::wstring getVoices();
	winrt::hstring getCurrentVoiceId();
	void setVoice(int index);
	winrt::hstring getCurrentVoiceLanguage();
	double getPitch();
	void setPitch(double pitch);
	double getVolume();
	void setVolume(double volume);
	double getRate();
	void setRate(double rate);
	void performCallback(
		BYTE* data,
		int length,
		const wchar_t* markers
	);
};

enum InstanceState {notInitialized, active, terminated};

class InstanceManager {
private:
	static std::recursive_mutex _instanceStateMutex;
	static std::vector<OcSpeech*> _terminatedInstances;
	static std::unique_ptr<OcSpeech> _instance;
	static std::atomic<InstanceState> _instanceState;
	static std::condition_variable_any _readyForInitialization;
	static void _assertInstanceActive(OcSpeech* token);
public:
	static void waitUntilReadyForInitialization();
	static OcSpeech* initializeNewInstance();
	static void terminateInstance(OcSpeech* token);
	static void deleteInstanceIfTerminatedAndReady();
	static OcSpeech* getActiveInstance(OcSpeech* token);
};

static void protectedCallback(
	OcSpeech* token,
	BYTE* data,
	int length,
	const wchar_t* markers
);

extern "C" {
	export bool __stdcall ocSpeech_supportsProsodyOptions();
	export OcSpeech* __stdcall ocSpeech_initialize();
	export void __stdcall ocSpeech_terminate(OcSpeech* token);
	export void __stdcall ocSpeech_setCallback(OcSpeech* token, ocSpeech_Callback fn);
	export void __stdcall ocSpeech_speak(OcSpeech* token, wchar_t* text);
	export BSTR __stdcall ocSpeech_getVoices(OcSpeech* token);
	export const wchar_t* __stdcall ocSpeech_getCurrentVoiceId(OcSpeech* token);
	export void __stdcall ocSpeech_setVoice(OcSpeech* token, int index);
	export const wchar_t* __stdcall ocSpeech_getCurrentVoiceLanguage(OcSpeech* token);
	export double __stdcall ocSpeech_getPitch(OcSpeech* token);
	export void __stdcall ocSpeech_setPitch(OcSpeech* token, double pitch);
	export double __stdcall ocSpeech_getVolume(OcSpeech* token);
	export void __stdcall ocSpeech_setVolume(OcSpeech* token, double volume);
	export double __stdcall ocSpeech_getRate(OcSpeech* token);
	export void __stdcall ocSpeech_setRate(OcSpeech* token, double rate);
}
