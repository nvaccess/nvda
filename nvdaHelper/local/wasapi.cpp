/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2023-2024 NV Access Limited, James Teh.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#include <thread>
#include <vector>
#include <windows.h>
#include <atlbase.h>
#include <atlcomcli.h>
#include <audioclient.h>
#include <audiopolicy.h>
#include <functiondiscoverykeys.h>
#include <Functiondiscoverykeys_devpkey.h>
#include <mmdeviceapi.h>
#include <common/log.h>
#include <random>
#include "silenceDetect.h"

/**
 * Support for audio playback using WASAPI.
 * Most of the core work happens in the WasapiPlayer class. Because Python
 * ctypes can't call C++ classes, NVDA interfaces with this using the wasPlay_*
 * and wasSilence_* functions.
 */

constexpr REFERENCE_TIME REFTIMES_PER_MILLISEC = 10000;
constexpr DWORD BUFFER_MS = 400;
constexpr REFERENCE_TIME BUFFER_SIZE = BUFFER_MS * REFTIMES_PER_MILLISEC;

const CLSID CLSID_MMDeviceEnumerator = __uuidof(MMDeviceEnumerator);
const IID IID_IMMDeviceEnumerator = __uuidof(IMMDeviceEnumerator);
const IID IID_IAudioClient = __uuidof(IAudioClient);
const IID IID_IAudioRenderClient = __uuidof(IAudioRenderClient);
const IID IID_IAudioClock = __uuidof(IAudioClock);
const IID IID_IMMNotificationClient = __uuidof(IMMNotificationClient);
const IID IID_IAudioStreamVolume = __uuidof(IAudioStreamVolume);
const IID IID_IAudioSessionManager2 = __uuidof(IAudioSessionManager2);
const IID IID_IAudioSessionControl2 = __uuidof(IAudioSessionControl2);
const IID IID_IMMEndpoint = __uuidof(IMMEndpoint);

/**
 * C++ RAII class to manage the lifecycle of a standard Windows HANDLE closed
 * with CloseHandle.
 */
class AutoHandle {
	public:
	AutoHandle(): handle(nullptr) {}
	AutoHandle(HANDLE handle): handle(handle) {}

	~AutoHandle() {
		if (handle) {
			CloseHandle(handle);
		}
	}

	AutoHandle& operator=(HANDLE newHandle) {
		if (handle) {
			CloseHandle(handle);
		}
		handle = newHandle;
		return *this;
	}

	operator HANDLE() {
		return handle;
	}

	private:
	HANDLE handle;
};

/**
 * Listens for default device changes and device state changes. These are
 * communicated to WasapiPlayer via the getDefaultDeviceChangeCount and
 * getDeviceStateChangeCount methods.
 */
class NotificationClient: public IMMNotificationClient {
	public:
	ULONG STDMETHODCALLTYPE AddRef() override {
		return InterlockedIncrement(&refCount);
	}

	ULONG STDMETHODCALLTYPE Release() override {
		LONG result = InterlockedDecrement(&refCount);
		if (result == 0) {
			delete this;
		}
		return result;
	}

	STDMETHODIMP QueryInterface(REFIID riid, void** ppvObject) final {
		if (riid == IID_IUnknown || riid == IID_IMMNotificationClient) {
			AddRef();
			*ppvObject = (void*)this;
			return S_OK;
		}
		return E_NOINTERFACE;
	}

	STDMETHODIMP OnDefaultDeviceChanged(EDataFlow flow, ERole     role,
		LPCWSTR   defaultDeviceId
	) final {
		if (flow == eRender && role == eConsole) {
			++defaultDeviceChangeCount;
		}
		return S_OK;
	}

	STDMETHODIMP OnDeviceAdded(LPCWSTR deviceId) final {
		return S_OK;
	}

	STDMETHODIMP OnDeviceRemoved(LPCWSTR deviceId) final {
		return S_OK;
	}

	STDMETHODIMP OnDeviceStateChanged(LPCWSTR deviceId, DWORD   newState) final {
		++deviceStateChangeCount;
		return S_OK;
	}

	STDMETHODIMP OnPropertyValueChanged(LPCWSTR           deviceId,
		const PROPERTYKEY key
	) final {
		return S_OK;
	}

	/**
	 * A counter which increases every time the default device changes. This is
	 * used by WasapiPlayer instances to detect such changes while playing.
	 */
	unsigned int getDefaultDeviceChangeCount() {
		return defaultDeviceChangeCount;
	}

	/**
	 * A counter which increases every time a device state changes. This is
	 * used by WasapiPlayer instances to detect such changes while playing.
	 */
	unsigned int getDeviceStateChangeCount() {
		return deviceStateChangeCount;
	}

	private:
	LONG refCount = 0;
	unsigned int defaultDeviceChangeCount = 0;
	unsigned int deviceStateChangeCount = 0;
};

CComPtr<NotificationClient> notificationClient;

/**
 * Play a stream of audio using WASAPI.
 */
class WasapiPlayer {
	public:
	using ChunkCompletedCallback = void(*)(WasapiPlayer* player,
		unsigned int id);

	/**
	 * Constructor.
	 * Specify an empty (not null) endpointId to use the default device.
	 */
	WasapiPlayer(wchar_t* endpointId, WAVEFORMATEX format,
		ChunkCompletedCallback callback);

	/**
	 * Open the audio device.
	 * If force is true, the device will be reopened even if it is already open.
	 */
	HRESULT open(bool force=false);

	/**
	 * Feed a chunk of audio.
	 * If not null, id will be set to a number used to identify the audio
	 * associated with this call. The callback will be called with this number when
	 * this audio finishes playing.
	 */
	HRESULT feed(unsigned char* data, unsigned int size, unsigned int* id);

	HRESULT stop();
	HRESULT sync();
	HRESULT idle();
	HRESULT pause();
	HRESULT resume();
	HRESULT setChannelVolume(unsigned int channel, float level);

	void startTrimmingLeadingSilence(bool start);

	private:
	void maybeFireCallback();

	// Reset our state due to being stopped. This runs on the feeder thread
	// rather than on the thread which called stop() because writing to a vector
	// isn't thread safe. We also reset the stream here because this can't be done
	// in stop() if the feeder thread is currently writing to the buffer.
	void completeStop();

	// Convert frames into ms.
	UINT64 framesToMs(UINT32 frames) {
		return frames * 1000 / format.nSamplesPerSec;
	}

	// Get the current playback position in ms.
	UINT64 getPlayPos();

	// Wait until we need to wake up next. This includes needing to fire a
	// callback.
	void waitUntilNeeded(UINT64 maxWait=INFINITE);

	HRESULT getPreferredDevice(CComPtr<IMMDevice>& preferredDevice);
	bool didPreferredDeviceBecomeAvailable();

	HRESULT disableCommunicationDucking(IMMDevice* device);

	enum class PlayState {
		stopped,
		playing,
		stopping,
	};

	CComPtr<IAudioClient> client;
	CComPtr<IAudioRenderClient> render;
	CComPtr<IAudioClock> clock;
	// The maximum number of frames that will fit in the buffer.
	UINT32 bufferFrames;
	std::wstring endpointId;
	WAVEFORMATEX format;
	ChunkCompletedCallback callback;
	PlayState playState = PlayState::stopped;
	// Maps feed ids to the end of their audio in ms since the start of the
	// stream. This is used to call the callback.
	std::vector<std::pair<unsigned int, UINT64>> feedEnds;
	UINT64 clockFreq;
	// The total number of frames buffered so far.
	UINT32 sentFrames = 0;
	unsigned int nextFeedId = 0;
	AutoHandle wakeEvent;
	unsigned int defaultDeviceChangeCount;
	unsigned int deviceStateChangeCount;
	bool isUsingPreferredDevice = false;
	bool isTrimmingLeadingSilence = false;
};

WasapiPlayer::WasapiPlayer(wchar_t* endpointId, WAVEFORMATEX format,
	ChunkCompletedCallback callback)
: endpointId(endpointId), format(format), callback(callback) {
	wakeEvent = CreateEvent(nullptr, false, false, nullptr);
}

HRESULT WasapiPlayer::open(bool force) {
	if (client && !force) {
		// Device already open and we're not forcing reopen.
		return S_OK;
	}
	defaultDeviceChangeCount = notificationClient->getDefaultDeviceChangeCount();
	deviceStateChangeCount = notificationClient->getDeviceStateChangeCount();
	CComPtr<IMMDeviceEnumerator> enumerator;
	HRESULT hr = enumerator.CoCreateInstance(CLSID_MMDeviceEnumerator);
	if (FAILED(hr)) {
		return hr;
	}
	CComPtr<IMMDevice> device;
	isUsingPreferredDevice = false;
	if (endpointId.empty()) {
		hr = enumerator->GetDefaultAudioEndpoint(eRender, eConsole, &device);
	} else {
		hr = getPreferredDevice(device);
		if (SUCCEEDED(hr)) {
			isUsingPreferredDevice = true;
		} else {
			// The preferred device wasn't found. Fall back to the default device.
			hr = enumerator->GetDefaultAudioEndpoint(eRender, eConsole, &device);
		}
	}
	if (FAILED(hr)) {
		return hr;
	}
	hr = device->Activate(IID_IAudioClient, CLSCTX_ALL, nullptr, (void**)&client);
	if (FAILED(hr)) {
		return hr;
	}
	hr = client->Initialize(AUDCLNT_SHAREMODE_SHARED,
		AUDCLNT_STREAMFLAGS_AUTOCONVERTPCM | AUDCLNT_STREAMFLAGS_SRC_DEFAULT_QUALITY,
		BUFFER_SIZE, 0, &format, nullptr);
	if (FAILED(hr)) {
		return hr;
	}
	hr = client->GetBufferSize(&bufferFrames);
	if (FAILED(hr)) {
		return hr;
	}
	hr = client->GetService(IID_IAudioRenderClient, (void**)&render);
	if (FAILED(hr)) {
		return hr;
	}
	hr = client->GetService(IID_IAudioClock, (void**)&clock);
	if (FAILED(hr)) {
		return hr;
	}
	hr = clock->GetFrequency(&clockFreq);
	if (FAILED(hr)) {
		return hr;
	}
	playState = PlayState::stopped;
	hr = disableCommunicationDucking(device);
	if (FAILED(hr)) {
		// Gracefully ignore failure, as disabling ducking isn't critical.
		LOG_DEBUGWARNING(L"Couldn't disable communication ducking: " << hr);
	}
	return S_OK;
}

HRESULT WasapiPlayer::feed(unsigned char* data, unsigned int size,
	unsigned int* id
) {
	if (playState == PlayState::stopping) {
		// stop() was called after feed() returned.
		completeStop();
	}
	UINT32 remainingFrames = size / format.nBlockAlign;
	HRESULT hr;

	// Returns false if we should abort, in which case we should return hr.
	auto reopenUsingNewDev = [&] {
		hr = open(true);
		if (FAILED(hr)) {
			return false;
		}
		// Call any pending callbacks. Otherwise, they'll never get called.
		for (auto& [itemId, itemEnd]: feedEnds) {
			callback(this, itemId);
		}
		feedEnds.clear();
		// This is the start of a new stream as far as WASAPI is concerned.
		sentFrames = 0;
		return true;
	};

	bool shouldInsertSilentFrame = false;
	if (isTrimmingLeadingSilence && data && size > 0) {
		size_t silenceSize = SilenceDetect::getLeadingSilenceSize(&format, data, size);
		if (silenceSize >= size) {
			// The whole chunk is silence. Continue checking for silence in the next chunk.
			// We cannot just skip the whole chunk, however,
			// because then the rest of this function will not perform some tasks,
			// such as opening the device or checking for callbacks.
			// Add one silent frame to be played, so those things work as usual.
			shouldInsertSilentFrame = true;
			remainingFrames = 1;
		} else {
			// Silence ends in this chunk. Skip the silence and continue.
			data += silenceSize;
			size -= silenceSize;
			remainingFrames = size / format.nBlockAlign;
			isTrimmingLeadingSilence = false;  // Stop checking for silence

			// Insert one silent frame before the trimmed audio in this chunk.
			// Not doing so may cause the beginning of the audio to be chopped off.
			// See: https://github.com/nvaccess/nvda/discussions/17697
			shouldInsertSilentFrame = true;
			remainingFrames++;
		}
	}

	while (remainingFrames > 0) {
		UINT32 paddingFrames;

		// Returns false if we should abort, in which case we should return hr.
		auto getPaddingHandlingStopOrDevChange = [&] {
			if (playState == PlayState::stopping) {
				// stop() was called in another thread. Don't send any more.
				completeStop();
				hr = S_OK;
				return false;
			}
			if (
				didPreferredDeviceBecomeAvailable() ||
				// We're using the default device and the default device changed.
				(!isUsingPreferredDevice && defaultDeviceChangeCount !=
					notificationClient->getDefaultDeviceChangeCount())
			) {
				if (!reopenUsingNewDev()) {
					return false;
				}
			}
			hr = client->GetCurrentPadding(&paddingFrames);
			if (
				hr == AUDCLNT_E_DEVICE_INVALIDATED
				|| hr == AUDCLNT_E_NOT_INITIALIZED
			) {
				// Either the device we're using has just been invalidated, or it was
				// invalidated previously and we failed to reopen. Try reopening, which
				// might fall back to the default device if appropriate.
				if (!reopenUsingNewDev()) {
					return false;
				}
				hr = client->GetCurrentPadding(&paddingFrames);
			}
			return SUCCEEDED(hr);
		};

		if (!getPaddingHandlingStopOrDevChange()) {
			return hr;
		}
		if (paddingFrames > bufferFrames / 2) {
			// Wait until the buffer is less than half full.
			waitUntilNeeded(framesToMs(paddingFrames - bufferFrames / 2));
			if (!getPaddingHandlingStopOrDevChange()) {
				return hr;
			}
		}
		// We might have more frames than will fit in the buffer. Send what we can.
		// If we need to insert a silent frame, the frame counts towards the total frame count,
		// but does not count towards the total byte count, as it's not in the provided data buffer.
		const UINT32 sendFrames = std::min(remainingFrames,
			bufferFrames - paddingFrames);
		const UINT32 sendBytes = (sendFrames - (shouldInsertSilentFrame ? 1 : 0))
			* format.nBlockAlign;
		BYTE* buffer;
		hr = render->GetBuffer(sendFrames, &buffer);
		if (FAILED(hr)) {
			return hr;
		}
		if (shouldInsertSilentFrame) {
			// If needed, insert one frame of silence at the beginning
			if (format.wFormatTag == WAVE_FORMAT_PCM && format.wBitsPerSample == 8) {
				memset(buffer, 0x80, format.nBlockAlign);
			} else {
				memset(buffer, 0, format.nBlockAlign);
			}
			buffer += format.nBlockAlign;
			shouldInsertSilentFrame = false;
		}
		if (data) {
			memcpy(buffer, data, sendBytes);
			hr = render->ReleaseBuffer(sendFrames, 0);
		} else {
			// Null data means play silence.
			hr = render->ReleaseBuffer(sendFrames, AUDCLNT_BUFFERFLAGS_SILENT);
		}
		if (FAILED(hr)) {
			return hr;
		}
		if (playState == PlayState::stopped) {
			hr = client->Start();
			if (FAILED(hr)) {
				return hr;
			}
			if (playState == PlayState::stopping) {
				// stop() was called while we were calling client->Start().
				completeStop();
				return S_OK;
			}
			playState = PlayState::playing;
		}
		maybeFireCallback();
		if (data) {
			data += sendBytes;
		}
		size -= sendBytes;
		remainingFrames -= sendFrames;
		sentFrames += sendFrames;
	}

	if (playState == PlayState::playing) {
		maybeFireCallback();
	}
	if (id) {
		*id = nextFeedId++;
		// Track that we want to call the callback with this id when playback
		// reaches the end of the audio provided to this call.
		// It is important that we add a new callback after we fire existing
		// callbacks. Otherwise, we might fire a newly added callback before its
		// feed() call returns, which will fail because the caller doesn't know about
		// this new id yet.
		feedEnds.push_back({*id, framesToMs(sentFrames)});
	}
	return S_OK;
}

void WasapiPlayer::maybeFireCallback() {
	const UINT64 playPos = getPlayPos();
	std::erase_if(feedEnds, [&](auto& val) {
		auto [id, end] = val;
		if (playPos >= end) {
			callback(this, id);
			return true;
		}
		return false;
	});
}

UINT64 WasapiPlayer::getPlayPos() {
	// Apparently IAudioClock::GetPosition can be expensive. If we hit performance
	// problems here, consider using the performance counter it returns for
	// subsequent calls.
	UINT64 pos;
	HRESULT hr = clock->GetPosition(&pos, nullptr);
	if (FAILED(hr)) {
		// If we get an error, playback has probably been interrupted; e.g. because
		// the device disconnected. Treat this as if playback has finished so we
		// don't wait forever and so that we fire any pending callbacks.
		return framesToMs(sentFrames);
	}
	return pos * 1000 / clockFreq;
}

void WasapiPlayer::waitUntilNeeded(UINT64 maxWait) {
	if (!feedEnds.empty()) {
		// There's at least one pending callback.
		UINT64 feedEnd = feedEnds[0].second;
		const UINT64 nextCallbackTime = feedEnd - getPlayPos();
		if (nextCallbackTime < maxWait) {
			// The callback needs to happen before maxWait supplied by the caller.
			// Lower maxWait accordingly.
			maxWait = nextCallbackTime;
		}
	}
	WaitForSingleObject(wakeEvent, (DWORD)maxWait);
}

HRESULT WasapiPlayer::getPreferredDevice(CComPtr<IMMDevice>& preferredDevice) {
	CComPtr<IMMDeviceEnumerator> enumerator;
	HRESULT hr = enumerator.CoCreateInstance(CLSID_MMDeviceEnumerator);
	if (FAILED(hr)) {
		return hr;
	}
	CComPtr<IMMDevice> device;
	hr = enumerator->GetDevice(endpointId.c_str(), &device);
	if (FAILED(hr)) {
		return hr;
	}

	// We only want to use the device if it is plugged in and enabled.
	DWORD state;
	hr = device->GetState(&state);
	if (FAILED(hr)) {
		return hr;
	} else if (state != DEVICE_STATE_ACTIVE) {
		return E_NOTFOUND;
	}

	// We only want to use the device if it is an output device.
	IMMEndpoint* endpoint;
	hr = device->QueryInterface(IID_IMMEndpoint, (void**)&endpoint);
	if (FAILED(hr)) {
		return hr;
	}
	EDataFlow dataFlow;
	hr = endpoint->GetDataFlow(&dataFlow);
	if (FAILED(hr)) {
		return hr;
	} else if (dataFlow != eRender) {
		return E_NOTFOUND;
	}
	preferredDevice = std::move(device);
	endpoint->Release();
	device.Release();
	enumerator.Release();
	return S_OK;
}

bool WasapiPlayer::didPreferredDeviceBecomeAvailable() {
	if (
		// We're already using the preferred device.
		isUsingPreferredDevice ||
		// A preferred device was not specified.
		endpointId.empty() ||
		// A device hasn't recently changed state.
		deviceStateChangeCount == notificationClient->getDeviceStateChangeCount()
	) {
		return false;
	}
	CComPtr<IMMDevice> device;
	return SUCCEEDED(getPreferredDevice(device));
}

HRESULT WasapiPlayer::stop() {
	HRESULT hr = client->Stop();
	// It's important that we set playState *after*
	// calling client->Stop() because otherwise, the feeder thread might see the
	// playState change and call client->Reset() before client->Stop() runs,
	// causing AUDCLNT_E_NOT_STOPPED.
	playState = PlayState::stopping;
	// If the device has been invalidated, it has already stopped. Just ignore
	// this and behave as if we were successful to avoid a cascade of breakage.
	// feed() will attempt to reopen the device next time it is called.
	if (
		hr != AUDCLNT_E_DEVICE_INVALIDATED
		&& hr != AUDCLNT_E_NOT_INITIALIZED
		&& FAILED(hr)
	) {
		return hr;
	}
	// If there is a feed/sync call waiting, wake it up so it can immediately
	// return to the caller.
	SetEvent(wakeEvent);
	return S_OK;
}

void WasapiPlayer::completeStop() {
	HRESULT hr = client->Reset();
	if (FAILED(hr)) {
		// We must not use LOG_ERROR here because that plays a sound and we might be
		// in the middle of stopping our sound player.
		LOG_DEBUGWARNING(L"Couldn't reset stream: " << hr);
		// We deliberately continue here. If Reset failed, the stream is probably
		// already cleared or unusable anyway. We should always reset our state.
	}
	nextFeedId = 0;
	sentFrames = 0;
	feedEnds.clear();
	playState = PlayState::stopped;
}

HRESULT WasapiPlayer::sync() {
	UINT64 sentMs = framesToMs(sentFrames);
	for (UINT64 playPos = getPlayPos(); playPos < sentMs;
			playPos = getPlayPos()) {
		if (playState != PlayState::playing) {
			return S_OK;
		}
		maybeFireCallback();
		waitUntilNeeded(sentMs - playPos);
	}
	// If there's a callback right at the end of the stream (sentMs), fire it.
	if (playState == PlayState::playing) {
		maybeFireCallback();
	}
	return S_OK;
}

HRESULT WasapiPlayer::idle() {
	HRESULT hr = sync();
	if (FAILED(hr)) {
		return hr;
	}
	hr = stop();
	if (FAILED(hr)) {
		return hr;
	}
	completeStop();
	return S_OK;
}

HRESULT WasapiPlayer::pause() {
	if (playState != PlayState::playing) {
		return S_OK;
	}
	HRESULT hr = client->Stop();
	if (FAILED(hr)) {
		return hr;
	}
	return S_OK;
}

HRESULT WasapiPlayer::resume() {
	if (playState != PlayState::playing) {
		return S_OK;
	}
	HRESULT hr = client->Start();
	if (FAILED(hr)) {
		return hr;
	}
	return S_OK;
}

HRESULT WasapiPlayer::setChannelVolume(unsigned int channel, float level) {
	CComPtr<IAudioStreamVolume> volume;
	HRESULT hr = client->GetService(IID_IAudioStreamVolume, (void**)&volume);
	if (hr == AUDCLNT_E_DEVICE_INVALIDATED) {
		// If we're using a specific device, it's just been invalidated. Fall back
		// to the default device.
		hr = open(true);
		if (FAILED(hr)) {
			return hr;
		}
		hr = client->GetService(IID_IAudioStreamVolume, (void**)&volume);
	}
	if (FAILED(hr)) {
		return hr;
	}
	return volume->SetChannelVolume(channel, level);
}

void WasapiPlayer::startTrimmingLeadingSilence(bool start) {
	isTrimmingLeadingSilence = start;
}

HRESULT WasapiPlayer::disableCommunicationDucking(IMMDevice* device) {
	// Disable the default ducking experience used when a communication audio
	// session is active, as we never want NVDA's audio to be ducked.
	// https://learn.microsoft.com/en-us/windows/win32/coreaudio/stream-attenuation
	// https://learn.microsoft.com/en-us/windows/win32/coreaudio/disabling-the-ducking-experience
	CComPtr<IAudioSessionManager2> manager;
	HRESULT hr = device->Activate(IID_IAudioSessionManager2, CLSCTX_ALL, nullptr,
		(void**)&manager);
	if (FAILED(hr)) {
		return hr;
	}
	CComPtr<IAudioSessionControl> control;
	hr = manager->GetAudioSessionControl(nullptr, 0, &control);
	if (FAILED(hr)) {
		return hr;
	}
	CComQIPtr<IAudioSessionControl2, &IID_IAudioSessionControl2> control2(control);
	if (!control2) {
		return E_NOINTERFACE;
	}
	return control2->SetDuckingPreference(TRUE);
}

/**
 * Asynchronously play silence for requested durations.
 * Silence is played in a background thread. The duration can be adjusted from
 * any thread.
 */
class SilencePlayer {
	public:
	SilencePlayer(wchar_t* endpointId);
	HRESULT init();
	// Play silence for the specified duration.
	void playFor(DWORD ms, float volume);
	void terminate();

	private:
	static WAVEFORMATEX getFormat();
	void generateWhiteNoise(float volume);
	// The code which is run in the silence thread.
	void run();

	static constexpr DWORD SAMPLES_PER_SEC = 48000;
	// How many bytes of silence in each buffer.
	static constexpr unsigned int SILENCE_BYTES = SAMPLES_PER_SEC * 2 * BUFFER_MS
		/ 1000;
	WasapiPlayer player;
	AutoHandle wakeEvent;
	// The time (not duration) at which silence should end.
	ULONGLONG endTime = 0;
	std::thread silenceThread;
	float volume;
	std::vector<INT16> whiteNoiseData;
};

SilencePlayer::SilencePlayer(wchar_t* endpointId):
player(endpointId, getFormat(), nullptr),
whiteNoiseData(
	SILENCE_BYTES  / (
		sizeof(INT16) / sizeof(unsigned char)
	)
),
volume(-1) {
	wakeEvent = CreateEvent(nullptr, false, false, nullptr);
}

WAVEFORMATEX SilencePlayer::getFormat() {
	WAVEFORMATEX format;
	format.wFormatTag = WAVE_FORMAT_PCM;
	format.nChannels = 1;
	format.nSamplesPerSec = SAMPLES_PER_SEC;
	format.wBitsPerSample = 16;
	format.nBlockAlign = 2;
	format.nAvgBytesPerSec = SAMPLES_PER_SEC * 2;
	format.cbSize = 0;
	return format;
}

void SilencePlayer::generateWhiteNoise(float volume) {
	if (volume == 0) {
		return;
	}
	UINT32 n = whiteNoiseData.size();
	const double mean = 0.0;
	const double stddev = volume * 256;
	std::default_random_engine generator;
	std::normal_distribution<double> dist(mean, stddev);
	for (UINT32 i = 0; i < n; i++) {
		whiteNoiseData[i] = (INT16)dist(generator);
	}
}

HRESULT SilencePlayer::init() {
	HRESULT hr = player.open();
	if (FAILED(hr)) {
		return hr;
	}
	silenceThread = std::thread(&SilencePlayer::run, this);
	return S_OK;
}

void SilencePlayer::run() {
	for (;;) {
		// Wait for silence or termination to be requested.
		WaitForSingleObject(wakeEvent, INFINITE);
		if (endTime == 0) {
			// We have been asked to terminate.
			// std::thread cannot be destroyed while it is attached, so detach it first.
			silenceThread.detach();
			delete this;
			return;
		}
		// Play silence until the desired time. This time might increase or decrease
		// as we're looping. This is fine because we're only pushing BUFFER_MS each
		// iteration.
		while (GetTickCount64() < endTime) {
			unsigned char* whiteNoisePtr = volume > 0
				? reinterpret_cast<unsigned char*>(&whiteNoiseData[0])
				: nullptr;
			player.feed(whiteNoisePtr, SILENCE_BYTES, nullptr);
		}
		player.idle();
	}
}

void SilencePlayer::playFor(DWORD ms, float volume) {
	if (volume != this->volume) {
		generateWhiteNoise(volume);
		this->volume = volume;
	}
	endTime = ms == INFINITE ? ULLONG_MAX : GetTickCount64() + ms;
	SetEvent(wakeEvent);
}

void SilencePlayer::terminate() {
	// 0 signals silenceThread to exit.
	endTime = 0;
	// If silenceThread is feeding, this will make feed return early.
	player.stop();
	// If silenceThread is waiting, this will wake it up.
	SetEvent(wakeEvent);
}

/*
 * NVDA calls the functions below. Most of these just wrap calls to
 * WasapiPlayer or SilencePlayer, with the exception of wasPlay_startup.
 */

WasapiPlayer* wasPlay_create(wchar_t* endpointId, WAVEFORMATEX format,
	WasapiPlayer::ChunkCompletedCallback callback
) {
	return new WasapiPlayer(endpointId, format, callback);
}

void wasPlay_destroy(WasapiPlayer* player) {
	delete player;
}

HRESULT wasPlay_open(WasapiPlayer* player) {
	return player->open();
}

HRESULT wasPlay_feed(WasapiPlayer* player, unsigned char* data,
	unsigned int size, unsigned int* id
) {
	return player->feed(data, size, id);
}

HRESULT wasPlay_stop(WasapiPlayer* player) {
	return player->stop();
}

HRESULT wasPlay_sync(WasapiPlayer* player) {
	return player->sync();
}

HRESULT wasPlay_idle(WasapiPlayer* player) {
	return player->idle();
}

HRESULT wasPlay_pause(WasapiPlayer* player) {
	return player->pause();
}

HRESULT wasPlay_resume(WasapiPlayer* player) {
	return player->resume();
}

HRESULT wasPlay_setChannelVolume(
	WasapiPlayer* player,
	unsigned int channel,
	float level
) {
	return player->setChannelVolume(channel, level);
}

void wasPlay_startTrimmingLeadingSilence(WasapiPlayer* player, bool start) {
	player->startTrimmingLeadingSilence(start);
}

/**
 * This must be called once per session at startup before wasPlay_create is
 * called.
 */
HRESULT wasPlay_startup() {
	CComPtr<IMMDeviceEnumerator> enumerator;
	HRESULT hr = enumerator.CoCreateInstance(CLSID_MMDeviceEnumerator);
	if (FAILED(hr)) {
		return hr;
	}
	notificationClient = new NotificationClient();
	return enumerator->RegisterEndpointNotificationCallback(notificationClient);
}

SilencePlayer* silence = nullptr;

HRESULT wasSilence_init(wchar_t* endpointId) {
	assert(!silence);
	silence = new SilencePlayer(endpointId);
	return silence->init();
}

void wasSilence_playFor(DWORD ms, float volume) {
	assert(silence);
	silence->playFor(ms, volume);
}

void wasSilence_terminate() {
	assert(silence);
	silence->terminate();
	// silence will delete itself once the thread terminates.
	silence = nullptr;
}
