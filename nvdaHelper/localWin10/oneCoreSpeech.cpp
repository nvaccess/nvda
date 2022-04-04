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
#include <winrt/Windows.Media.SpeechSynthesis.h>
#include <winrt/Windows.Storage.Streams.h>
#include <winrt/Windows.Foundation.h>
#include <winrt/Windows.Foundation.Collections.h>
#include <winrt/Windows.Foundation.Metadata.h>
#include <common/log.h>
#include "oneCoreSpeech.h"
#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <atomic>
#include <thread>
#include <mutex>
#include <condition_variable>

using namespace std;
using namespace winrt;
using namespace winrt::Windows::Media::SpeechSynthesis;
using namespace winrt::Windows::Storage::Streams;
using namespace winrt::Windows::Media;
using namespace winrt::Windows::Foundation::Collections;
using winrt::Windows::Foundation::Metadata::ApiInformation;

std::vector<OcSpeech *> _terminatedInstances;

SpeechCounter::SpeechCounter() : speechThreads{0} {}

void SpeechCounter::reset() {
	std::lock_guard g(speechThreadsMutex_);
	speechThreads = 0;
	cond_var_.notify_all();
}

void SpeechCounter::markSpeechStarted() {
	std::lock_guard g1(preventSpeechMutex_);
	std::lock_guard g2(speechThreadsMutex_);
	speechThreads++;
}

void SpeechCounter::markCallbackFinished() {
	std::lock_guard g(speechThreadsMutex_);
	speechThreads--;
	if (speechThreads == 0) {
		cond_var_.notify_all();
	}
}

bool SpeechCounter::hasSpeechFinished() {
	return speechThreads == 0;
}

void SpeechCounter::waitUntilSpeechFinished() {
	std::unique_lock lock(speechThreadsMutex_);
	// Wait for a signal for speech to finish
	cond_var_.wait(lock, [this]{return this->hasSpeechFinished();});
}

void _assertOcSpeechInstanceAlive(OcSpeech* instance) {
	for (auto p: _terminatedInstances) {
		if (p == instance) {
			LOG_ERROR("Supplied OneCore instance has terminated");
		}
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
	auto instance = new OcSpeech;
	_terminatedInstances.erase(
		std::remove(
			_terminatedInstances.begin(),
			_terminatedInstances.end(),
			instance
		),
		_terminatedInstances.end()
	);
	return instance;
}

void __stdcall ocSpeech_terminate(OcSpeech* instance) {
	_assertOcSpeechInstanceAlive(instance);
	std::lock_guard g(instance->_speechCounter.preventSpeechMutex_);
	instance->_speechCounter.waitUntilSpeechFinished();
	_terminatedInstances.emplace_back(instance);
	delete instance;
}


void __stdcall ocSpeech_setCallback(OcSpeech* instance, ocSpeech_Callback fn) {
	_assertOcSpeechInstanceAlive(instance);
	instance->setCallback(fn);
}

void OcSpeech::setCallback(ocSpeech_Callback fn) {
	callback = fn;
}

void _protectedCallback(
	OcSpeech* instance,
	BYTE* data,
	int length,
	const wchar_t* markers
) {
	_assertOcSpeechInstanceAlive(instance);
	instance->performCallback(data, length, markers);
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
		_speechCounter.markSpeechStarted();

		wstring markersStr;
		SpeechSynthesisStream speechStream{ nullptr };
		try {
			speechStream = co_await synth.SynthesizeSsmlToStreamAsync(text);
		} catch (hresult_error const& e) {
			LOG_ERROR(L"Error " << e.code() << L": " << e.message().c_str());
			_protectedCallback(this, nullptr, 0, nullptr);
			_speechCounter.markCallbackFinished();
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
			_protectedCallback(this, bytes, buffer.Length(), markersStr.c_str());
		} catch (hresult_error const& e) {
			LOG_ERROR(L"Error " << e.code() << L": " << e.message().c_str());
			_protectedCallback(this, nullptr, 0, nullptr);
		}
	} catch (...) {
		LOG_ERROR(L"Unexpected error in OcSpeech::speak");
	}
	_speechCounter.markCallbackFinished();
}

void __stdcall ocSpeech_speak(OcSpeech* instance, wchar_t* text) {
	_assertOcSpeechInstanceAlive(instance);
	instance->speak(text);
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
BSTR __stdcall ocSpeech_getVoices(OcSpeech* instance) {
	_assertOcSpeechInstanceAlive(instance);
	return SysAllocString(instance->getVoices().c_str());
}

hstring OcSpeech::getCurrentVoiceId() {
	return synth.Voice().Id();
}

const wchar_t* __stdcall ocSpeech_getCurrentVoiceId(OcSpeech* instance) {
	_assertOcSpeechInstanceAlive(instance);
	return instance->getCurrentVoiceId().c_str();
}

void OcSpeech::setVoice(int index) {
	synth.Voice(synth.AllVoices().GetAt(index));
}

void __stdcall ocSpeech_setVoice(OcSpeech* instance, int index) {
	_assertOcSpeechInstanceAlive(instance);
	instance->setVoice(index);
}

hstring OcSpeech::getCurrentVoiceLanguage() {
	return synth.Voice().Language();
}

const wchar_t* __stdcall ocSpeech_getCurrentVoiceLanguage(OcSpeech* instance) {
	_assertOcSpeechInstanceAlive(instance);
	return instance->getCurrentVoiceLanguage().c_str();
}

double OcSpeech::getPitch() {
	return synth.Options().AudioPitch();
}

double __stdcall ocSpeech_getPitch(OcSpeech* instance) {
	_assertOcSpeechInstanceAlive(instance);
	return instance->getPitch();
}

void OcSpeech::setPitch(double pitch) {
	synth.Options().AudioPitch(pitch);
}

void __stdcall ocSpeech_setPitch(OcSpeech* instance, double pitch) {
	_assertOcSpeechInstanceAlive(instance);
	instance->setPitch(pitch);
}

double OcSpeech::getVolume() {
	return synth.Options().AudioVolume();
}

double __stdcall ocSpeech_getVolume(OcSpeech* instance) {
	_assertOcSpeechInstanceAlive(instance);
	return instance->getVolume();
}

void OcSpeech::setVolume(double volume) {
	synth.Options().AudioVolume(volume);
}

void __stdcall ocSpeech_setVolume(OcSpeech* instance, double volume) {
	_assertOcSpeechInstanceAlive(instance);
	instance->setVolume(volume);
}

double OcSpeech::getRate() {
	return synth.Options().SpeakingRate();
}

double __stdcall ocSpeech_getRate(OcSpeech* instance) {
	_assertOcSpeechInstanceAlive(instance);
	return instance->getRate();
}

void OcSpeech::setRate(double rate) {
	synth.Options().SpeakingRate(rate);
}

void __stdcall ocSpeech_setRate(OcSpeech* instance, double rate) {
	_assertOcSpeechInstanceAlive(instance);
	instance->setRate(rate);
}
