/*
Code for C dll bridge to Windows OneCore voices.
This file is a part of the NVDA project.
URL: http://www.nvaccess.org/
Copyright 2016-2022 Tyler Spivey, NV Access Limited, Leonard de Ruijter.
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License version 2.0, as published by
	the Free Software Foundation.
	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#include <string>
#include <iostream>
#include <vector>
#include <algorithm>
#include <atomic>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <winrt/Windows.Media.SpeechSynthesis.h>
#include <winrt/Windows.Storage.Streams.h>
#include <winrt/Windows.Foundation.h>
#include <winrt/Windows.Foundation.Collections.h>
#include <winrt/Windows.Foundation.Metadata.h>
#include <common/log.h>
#include "oneCoreSpeech.h"

using namespace std;
using namespace winrt;
using namespace winrt::Windows::Media::SpeechSynthesis;
using namespace winrt::Windows::Storage::Streams;
using namespace winrt::Windows::Media;
using namespace winrt::Windows::Foundation::Collections;
using winrt::Windows::Foundation::Metadata::ApiInformation;

std::recursive_mutex InstanceManager::_instanceStateMutex;
std::vector<OcSpeech*> InstanceManager::_terminatedInstances;
std::unique_ptr<OcSpeech> InstanceManager::_instance;
std::atomic<InstanceState> InstanceManager::_instanceState = InstanceState::notInitialized;
std::condition_variable_any InstanceManager::_readyForInitialization;
std::atomic_int SpeakThreadGuard::_speechThreads = 0;

SpeakThreadGuard::SpeakThreadGuard() {
	/*
	When initialized, increases the count of active speech threads
	waiting on a callback.
	When exiting the scope of initialization, decreases the count
	of active speech threads and deletes the OneCore instance if it has
	been terminated.
	*/
	++_speechThreads;
}

bool SpeakThreadGuard::areCallbacksPending() {
	/*
	Checks if any speak threads are active, with callbacks pending.
	*/
	return _speechThreads != 0;
}

SpeakThreadGuard::~SpeakThreadGuard() {
	/* 
	When exiting the scope of initialization, decreases the count
	of active speech threads and deletes the OneCore instance if it has
	been terminated.
	*/
	--_speechThreads;
	if (_speechThreads < 0) {
		throw runtime_error(
			"Negative callback count."
			"decreasePendingCount has been called too many times."
		);
	}
	InstanceManager::deleteInstanceIfTerminatedAndReady();
}

void InstanceManager::deleteInstanceIfTerminatedAndReady() {
	/*
	If the instance is terminated and no speak callbacks are pending,
	delete the instance and notify any waiting threads,
	such as the instance initializer.
	*/
	std::lock_guard g(_instanceStateMutex);
	if (
		_instanceState == InstanceState::terminated
		&& !SpeakThreadGuard::areCallbacksPending()
	) {
		_instance.reset();
		_instanceState = InstanceState::notInitialized;
		_readyForInitialization.notify_all();
	}
}

void InstanceManager::waitUntilReadyForInitialization() {
	/* Wait for a signal that there is no active or terminated instance. */
	std::unique_lock lock(_instanceStateMutex);
	_readyForInitialization.wait(lock, []{
		return !_instance && _instanceState == InstanceState::notInitialized;
	});
}

OcSpeech* InstanceManager::getActiveInstance(OcSpeech* token) {
	/* Throw a runtime error if no instance is active */
	_assertInstanceActive(token);
	return _instance.get();
}

void InstanceManager::_assertInstanceActive(OcSpeech* token) {
	if (_instanceState != InstanceState::active) {
		throw runtime_error("Supplied OneCore token is not active");
	}
	if (_instance.get() != token) {
		throw runtime_error("Supplied OneCore instance token does not match initialized instance");
	}
}

OcSpeech* InstanceManager::initializeNewInstance() {
	/*
	Initializes a new OneCore instance.
	Waits until an instance has been fully terminated,
	and then (once speech callbacks have finished) deleted.
	*/
	std::lock_guard g(_instanceStateMutex);
	if (_instanceState == InstanceState::active) {
		throw runtime_error(
			"OneCore token still active."
			"Terminate token before calling initialize"
		);
	}
	waitUntilReadyForInitialization();
	_instance = std::make_unique<OcSpeech>();
	_instanceState = InstanceState::active;
	// Remove instance from terminated instances if we get the same pointer again
	_terminatedInstances.erase(
		std::remove(
			_terminatedInstances.begin(),
			_terminatedInstances.end(),
			_instance.get()
		),
		_terminatedInstances.end()
	);
	return _instance.get();
}

void InstanceManager::terminateInstance(OcSpeech* token) {
	/*
	Marks an instance as terminated.
	If no callbacks are pending, proceed with deletion of the instance.
	*/
	_assertInstanceActive(token);
	std::lock_guard g(_instanceStateMutex);
	_instanceState = InstanceState::terminated;
	_terminatedInstances.emplace_back(_instance.get());
	if (!SpeakThreadGuard::areCallbacksPending()){
		_instance.reset();
		_instanceState = InstanceState::notInitialized;
	}
}

bool __stdcall ocSpeech_supportsProsodyOptions() {
	return ApiInformation::IsApiContractPresent(hstring{L"Windows.Foundation.UniversalApiContract"}, 5, 0);
}

OcSpeech::OcSpeech() : synth(SpeechSynthesizer{}) {
	// By default, OneCore speech appends a  large annoying chunk of silence at the end of every utterance.
	// Newer versions of OneCore speech allow disabling this feature, so turn it off where possible.
	if (ApiInformation::IsApiContractPresent(hstring{L"Windows.Foundation.UniversalApiContract"}, 6, 0)) {
		synth.Options().AppendedSilence(SpeechAppendedSilence::Min);
	} else {
		LOG_DEBUGWARNING(L"AppendedSilence not supported");
	}
}

OcSpeech* __stdcall ocSpeech_initialize() {
	return InstanceManager::initializeNewInstance();
}

void __stdcall ocSpeech_terminate(OcSpeech* token) {
	InstanceManager::terminateInstance(token);
}

void __stdcall ocSpeech_setCallback(OcSpeech* token, ocSpeech_Callback fn) {
	InstanceManager::getActiveInstance(token)->setCallback(fn);
}

void OcSpeech::setCallback(ocSpeech_Callback fn) {
	callback = fn;
}

void protectedCallback(
	OcSpeech* token,
	BYTE* data,
	int length,
	const wchar_t* markers
) {
	InstanceManager::getActiveInstance(token)->performCallback(data, length, markers);
}

void OcSpeech::performCallback(
	BYTE* data,
	int length,
	const wchar_t* markers
) {
	callback(data, length, markers);
}

fire_and_forget OcSpeech::speak(hstring text) {
	/*
	Send speech to OneCore.
	Will block OneCore from being re-initialized until speech callbacks have completed.
	*/
	SpeakThreadGuard();
	// Ensure we catch all exceptions in this method,

	// as an unhandled exception causes std::terminate to get called, resulting in a crash.
	// See https://devblogs.microsoft.com/oldnewthing/20190320-00/?p=102345
	try {
		// Ensure that work is performed on a background thread.
		co_await resume_background();

		wstring markersStr;
		SpeechSynthesisStream speechStream{ nullptr };
		try {
			speechStream = co_await synth.SynthesizeSsmlToStreamAsync(text);
		} catch (hresult_error const& e) {
			LOG_ERROR(L"Error " << e.code() << L": " << e.message().c_str());
			protectedCallback(this, nullptr, 0, nullptr);
			co_return;
		}
		// speechStream.Size() is 64 bit, but Buffer can only take 32 bit.
		// We shouldn't get values above 32 bit in reality.
		const unsigned int size = static_cast<unsigned int>(speechStream.Size());
		Buffer buffer { size };

		IVectorView<IMediaMarker> markers = speechStream.Markers();
		for (auto const& marker : markers) {
			if (markersStr.length() > 0) {
				markersStr += L"|";
			}
			markersStr += marker.Text();
			markersStr += L":";
			markersStr += to_wstring(marker.Time().count());
		}
		try {
			co_await speechStream.ReadAsync(buffer, size, InputStreamOptions::None);
			// Data has been read from the speech stream.
			// Pass it to the callback.
			BYTE* bytes = buffer.data();
			protectedCallback(this, bytes, buffer.Length(), markersStr.c_str());
		} catch (hresult_error const& e) {
			LOG_ERROR(L"Error " << e.code() << L": " << e.message().c_str());
			protectedCallback(this, nullptr, 0, nullptr);
		}
	} catch (...) {
		LOG_ERROR(L"Unexpected error in OcSpeech::speak");
	}
}

void __stdcall ocSpeech_speak(OcSpeech* token, wchar_t* text) {
	/*
	Send speech to OneCore.
	Will block OneCore from being re-initialized until speech callbacks have completed.
	*/
	InstanceManager::getActiveInstance(token)->speak(text);
}

wstring OcSpeech::getVoices() {
	wstring voices;
	auto const& allVoices = synth.AllVoices();
	for (unsigned int i = 0; i < allVoices.Size(); ++i) {
		VoiceInformation const& voiceInfo = allVoices.GetAt(i);
		voices += voiceInfo.Id();
		voices += L":";
		voices += voiceInfo.Language();
		voices += L":";
		voices += voiceInfo.DisplayName();
		if (i != allVoices.Size() - 1) {
			voices += L"|";
		}
	}
	return voices;
}

// We use BSTR because we need the string to stay around until the caller is done with it
// but the caller then needs to free it.
// We can't just use malloc because the caller might be using a different CRT
// and calling malloc and free from different CRTs isn't safe.
BSTR __stdcall ocSpeech_getVoices(OcSpeech* token) {
	return SysAllocString(
		InstanceManager::getActiveInstance(token)->getVoices().c_str()
	);
}

hstring OcSpeech::getCurrentVoiceId() {
	return synth.Voice().Id();
}

const wchar_t* __stdcall ocSpeech_getCurrentVoiceId(OcSpeech* token) {
	return InstanceManager::getActiveInstance(token)->getCurrentVoiceId().c_str();
}

void OcSpeech::setVoice(int index) {
	synth.Voice(synth.AllVoices().GetAt(index));
}

void __stdcall ocSpeech_setVoice(OcSpeech* token, int index) {
	InstanceManager::getActiveInstance(token)->setVoice(index);
}

hstring OcSpeech::getCurrentVoiceLanguage() {
	return synth.Voice().Language();
}

const wchar_t* __stdcall ocSpeech_getCurrentVoiceLanguage(OcSpeech* token) {
	return InstanceManager::getActiveInstance(token)->getCurrentVoiceLanguage().c_str();
}

double OcSpeech::getPitch() {
	return synth.Options().AudioPitch();
}

double __stdcall ocSpeech_getPitch(OcSpeech* token) {
	return InstanceManager::getActiveInstance(token)->getPitch();
}

void OcSpeech::setPitch(double pitch) {
	synth.Options().AudioPitch(pitch);
}

void __stdcall ocSpeech_setPitch(OcSpeech* token, double pitch) {
	InstanceManager::getActiveInstance(token)->setPitch(pitch);
}

double OcSpeech::getVolume() {
	return synth.Options().AudioVolume();
}

double __stdcall ocSpeech_getVolume(OcSpeech* token) {
	return InstanceManager::getActiveInstance(token)->getVolume();
}

void OcSpeech::setVolume(double volume) {
	synth.Options().AudioVolume(volume);
}

void __stdcall ocSpeech_setVolume(OcSpeech* token, double volume) {
	InstanceManager::getActiveInstance(token)->setVolume(volume);
}

double OcSpeech::getRate() {
	return synth.Options().SpeakingRate();
}

double __stdcall ocSpeech_getRate(OcSpeech* token) {
	return InstanceManager::getActiveInstance(token)->getRate();
}

void OcSpeech::setRate(double rate) {
	synth.Options().SpeakingRate(rate);
}

void __stdcall ocSpeech_setRate(OcSpeech* token, double rate) {
	InstanceManager::getActiveInstance(token)->setRate(rate);
}
