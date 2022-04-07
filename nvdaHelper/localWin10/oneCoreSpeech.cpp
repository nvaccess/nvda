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

std::recursive_mutex InstanceManager::_pendingDeletionInstanceMutex;
std::vector<OcSpeech*> InstanceManager::_terminatedInstances;
std::unique_ptr<OcSpeech> InstanceManager::_aliveInstance;
std::unique_ptr<OcSpeech> InstanceManager::_pendingDeletionInstance;
std::condition_variable_any InstanceManager::_instanceReadyForDeletion;
std::atomic_int SpeakCallbackCounter::_speechThreads = 0;

void SpeakCallbackCounter::increasePendingCount() {
	++_speechThreads;
}

bool SpeakCallbackCounter::areCallbacksPending() {
	return _speechThreads != 0;
}

void SpeakCallbackCounter::decreasePendingCount() {
	--_speechThreads;
	InstanceManager::deleteInstanceIfReady();
}

void InstanceManager::deleteInstanceIfReady() {
	std::lock_guard g(_pendingDeletionInstanceMutex);
	if (_pendingDeletionInstance && !SpeakCallbackCounter::areCallbacksPending()) {
		_pendingDeletionInstance.reset();
		_instanceReadyForDeletion.notify_all();
	}
}

void InstanceManager::waitForAnyPendingDeletion() {
	std::unique_lock lock(_pendingDeletionInstanceMutex);
	// Wait for a signal for speech to finish
	_instanceReadyForDeletion.wait(lock, []{return !_pendingDeletionInstance;});
}

OcSpeech* InstanceManager::getAliveInstance(OcSpeech* token) {
	_assertInstanceAlive(token);
	return _aliveInstance.get();
}

void InstanceManager::_assertInstanceAlive(OcSpeech* token) {
	std::lock_guard g(_pendingDeletionInstanceMutex);
	if (_aliveInstance.get() != token) {
		LOG_ERROR("Supplied OneCore token is not alive");
	}
	if (_pendingDeletionInstance.get() == token) {
		LOG_ERROR("Supplied OneCore token is being terminated");
	}
	for (auto p: _terminatedInstances) {
		if (p == token) {
			LOG_ERROR("Supplied OneCore token has terminated");
		}
	}
}

OcSpeech* InstanceManager::initializeNewInstance() {
	if (_aliveInstance) {
		throw runtime_error(
			"OneCore token still alive."
			"Terminate token before calling initialize"
		);
	}
	waitForAnyPendingDeletion();
	_aliveInstance = std::make_unique<OcSpeech>();
	// Remove instances from terminated instances if we get the same pointer again
	_terminatedInstances.erase(
		std::remove(
			_terminatedInstances.begin(),
			_terminatedInstances.end(),
			_aliveInstance.get()
		),
		_terminatedInstances.end()
	);
	return _aliveInstance.get();
}

void InstanceManager::terminateInstance(OcSpeech* token) {
	_assertInstanceAlive(token);
	std::lock_guard g(_pendingDeletionInstanceMutex);
	if (_pendingDeletionInstance != nullptr) {
		throw runtime_error(
			"OneCore token is already pending termination."
			"Initialize a new token before terminating."
		);
	}
	_pendingDeletionInstance.swap(_aliveInstance);
	_terminatedInstances.emplace_back(_pendingDeletionInstance.get());
	if (!SpeakCallbackCounter::areCallbacksPending()){
		_pendingDeletionInstance.reset();
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
	InstanceManager::getAliveInstance(token)->setCallback(fn);
}

void OcSpeech::setCallback(ocSpeech_Callback fn) {
	callback = fn;
}

void InstanceManager::protectedCallback(
	OcSpeech* token,
	BYTE* data,
	int length,
	const wchar_t* markers
) {
	std::lock_guard g(_pendingDeletionInstanceMutex);
	if (token == _pendingDeletionInstance.get()) {
		LOG_DEBUGWARNING("OneCore token is pending deletion");
		return;
	}
	InstanceManager::getAliveInstance(token)->performCallback(data, length, markers);
}

void OcSpeech::performCallback(
	BYTE* data,
	int length,
	const wchar_t* markers
) {
	callback(data, length, markers);
}

fire_and_forget OcSpeech::speak(hstring text) {
	// Ensure we catch all exceptions in this method,

	// as an unhandled exception causes std::terminate to get called, resulting in a crash.
	// See https://devblogs.microsoft.com/oldnewthing/20190320-00/?p=102345
	try {
		// Ensure that work is performed on a background thread.
		co_await resume_background();
		SpeakCallbackCounter::increasePendingCount();

		wstring markersStr;
		SpeechSynthesisStream speechStream{ nullptr };
		try {
			speechStream = co_await synth.SynthesizeSsmlToStreamAsync(text);
		} catch (hresult_error const& e) {
			LOG_ERROR(L"Error " << e.code() << L": " << e.message().c_str());
			InstanceManager::protectedCallback(this, nullptr, 0, nullptr);
			SpeakCallbackCounter::decreasePendingCount();
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
			InstanceManager::protectedCallback(this, bytes, buffer.Length(), markersStr.c_str());
		} catch (hresult_error const& e) {
			LOG_ERROR(L"Error " << e.code() << L": " << e.message().c_str());
			InstanceManager::protectedCallback(this, nullptr, 0, nullptr);
		}
	} catch (...) {
		LOG_ERROR(L"Unexpected error in OcSpeech::speak");
	}
	SpeakCallbackCounter::decreasePendingCount();
}

void __stdcall ocSpeech_speak(OcSpeech* token, wchar_t* text) {
	InstanceManager::getAliveInstance(token)->speak(text);
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
		InstanceManager::getAliveInstance(token)->getVoices().c_str()
	);
}

hstring OcSpeech::getCurrentVoiceId() {
	return synth.Voice().Id();
}

const wchar_t* __stdcall ocSpeech_getCurrentVoiceId(OcSpeech* token) {
	return InstanceManager::getAliveInstance(token)->getCurrentVoiceId().c_str();
}

void OcSpeech::setVoice(int index) {
	synth.Voice(synth.AllVoices().GetAt(index));
}

void __stdcall ocSpeech_setVoice(OcSpeech* token, int index) {
	InstanceManager::getAliveInstance(token)->setVoice(index);
}

hstring OcSpeech::getCurrentVoiceLanguage() {
	return synth.Voice().Language();
}

const wchar_t* __stdcall ocSpeech_getCurrentVoiceLanguage(OcSpeech* token) {
	return InstanceManager::getAliveInstance(token)->getCurrentVoiceLanguage().c_str();
}

double OcSpeech::getPitch() {
	return synth.Options().AudioPitch();
}

double __stdcall ocSpeech_getPitch(OcSpeech* token) {
	return InstanceManager::getAliveInstance(token)->getPitch();
}

void OcSpeech::setPitch(double pitch) {
	synth.Options().AudioPitch(pitch);
}

void __stdcall ocSpeech_setPitch(OcSpeech* token, double pitch) {
	InstanceManager::getAliveInstance(token)->setPitch(pitch);
}

double OcSpeech::getVolume() {
	return synth.Options().AudioVolume();
}

double __stdcall ocSpeech_getVolume(OcSpeech* token) {
	return InstanceManager::getAliveInstance(token)->getVolume();
}

void OcSpeech::setVolume(double volume) {
	synth.Options().AudioVolume(volume);
}

void __stdcall ocSpeech_setVolume(OcSpeech* token, double volume) {
	InstanceManager::getAliveInstance(token)->setVolume(volume);
}

double OcSpeech::getRate() {
	return synth.Options().SpeakingRate();
}

double __stdcall ocSpeech_getRate(OcSpeech* token) {
	return InstanceManager::getAliveInstance(token)->getRate();
}

void OcSpeech::setRate(double rate) {
	synth.Options().SpeakingRate(rate);
}

void __stdcall ocSpeech_setRate(OcSpeech* token, double rate) {
	InstanceManager::getAliveInstance(token)->setRate(rate);
}
