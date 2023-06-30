/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2023 James Teh.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#include <vector>
#include <windows.h>
#include <atlcomcli.h>
#include <audioclient.h>
#include <audiopolicy.h>
#include <functiondiscoverykeys.h>
#include <Functiondiscoverykeys_devpkey.h>
#include <mmdeviceapi.h>
#include <common/log.h>

/**
 * Support for audio playback using WASAPI.
 * Most of the core work happens in the WasapiPlayer class. Because Python
 * ctypes can't call C++ classes, NVDA interfaces with this using the wasPlay_*
 * functions.
 */

constexpr REFERENCE_TIME REFTIMES_PER_MILLISEC = 10000;
constexpr REFERENCE_TIME BUFFER_SIZE = 400 * REFTIMES_PER_MILLISEC;

const CLSID CLSID_MMDeviceEnumerator = __uuidof(MMDeviceEnumerator);
const IID IID_IMMDeviceEnumerator = __uuidof(IMMDeviceEnumerator);
const IID IID_IAudioClient = __uuidof(IAudioClient);
const IID IID_IAudioRenderClient = __uuidof(IAudioRenderClient);
const IID IID_IAudioClock = __uuidof(IAudioClock);
const IID IID_IMMNotificationClient = __uuidof(IMMNotificationClient);
const IID IID_IAudioStreamVolume = __uuidof(IAudioStreamVolume);

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
 * Listens for default device changes. These are communicated to WasapiPlayer
 * via the getDefaultDeviceChangeCount method.
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

	private:
	LONG refCount = 0;
	unsigned int defaultDeviceChangeCount = 0;
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
	 * Specify an empty (not null) deviceId to use the default device.
	 */
	WasapiPlayer(wchar_t* deviceId, WAVEFORMATEX format,
		ChunkCompletedCallback callback);

	/**
	 * Open the audio device.
	 * If force is true, the device will be reopened even if it is already open.
	 */
	HRESULT open(bool force=false);

	HRESULT close();

	/**
	 * Feed a chunk of audio.
	 * If not null, id will be set to a number used to identify the audio
	 * associated with this call. The callback will be called with this number when
	 * this audio finishes playing.
	 */
	HRESULT feed(unsigned char* data, unsigned int size, unsigned int* id);

	HRESULT stop();
	HRESULT sync();
	HRESULT pause();
	HRESULT resume();
	HRESULT setChannelVolume(unsigned int channel, float level);

	private:
	void maybeFireCallback();

	// Reset our state due to being stopped. This runs on the feeder thread
	// rather than on the thread which called stop() because writing to a vector
	// isn't thread safe.
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
	std::wstring deviceId;
	WAVEFORMATEX format;
	ChunkCompletedCallback callback;
	PlayState playState = PlayState::stopped;
	// Maps feed ids to the end of their audio in ms since the start of the
	// stream. This is used to call the callback.
	std::vector<std::pair<unsigned int, UINT64>> feedEnds;
	UINT64 clockFreq;
	// The duration of audio sent (buffered) so far in ms.
	UINT64 sentMs = 0;
	unsigned int nextFeedId = 0;
	AutoHandle wakeEvent;
	unsigned int defaultDeviceChangeCount;
};

WasapiPlayer::WasapiPlayer(wchar_t* deviceId, WAVEFORMATEX format,
	ChunkCompletedCallback callback)
: deviceId(deviceId), format(format), callback(callback) {
	wakeEvent = CreateEvent(nullptr, false, false, nullptr);
}

HRESULT WasapiPlayer::open(bool force) {
	if (client && !force) {
		// Device already open and we're not forcing reopen.
		return S_OK;
	}
	defaultDeviceChangeCount = notificationClient->getDefaultDeviceChangeCount();
	CComPtr<IMMDeviceEnumerator> enumerator;
	HRESULT hr = enumerator.CoCreateInstance(CLSID_MMDeviceEnumerator);
	if (FAILED(hr)) {
		return hr;
	}
	CComPtr<IMMDevice> device;
	if (deviceId.empty()) {
		hr = enumerator->GetDefaultAudioEndpoint(eRender, eConsole, &device);
	} else {
		hr = enumerator->GetDevice(deviceId.c_str(), &device);
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
	return S_OK;
}

HRESULT WasapiPlayer::close() {
	client = nullptr;
	render = nullptr;
	clock = nullptr;
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
		HRESULT hr = open(true);
		if (FAILED(hr)) {
			return false;
		}
		// Call any pending callbacks. Otherwise, they'll never get called.
		for (auto& [itemId, itemEnd]: feedEnds) {
			callback(this, itemId);
		}
		feedEnds.clear();
		// This is the start of a new stream as far as WASAPI is concerned.
		sentMs = 0;
		return true;
	};

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
			if (deviceId.empty() && defaultDeviceChangeCount !=
					notificationClient->getDefaultDeviceChangeCount()) {
				// The default device changed.
				if (!reopenUsingNewDev()) {
					return false;
				}
			}
			hr = client->GetCurrentPadding(&paddingFrames);
			if (hr == AUDCLNT_E_DEVICE_INVALIDATED) {
				// If we're using a specific device, it's just been invalidated. Fall back
				// to the default device.
				deviceId.clear();
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
		const UINT32 sendFrames = std::min(remainingFrames,
			bufferFrames - paddingFrames);
		const UINT32 sendBytes = sendFrames * format.nBlockAlign;
		BYTE* buffer;
		hr = render->GetBuffer(sendFrames, &buffer);
		if (FAILED(hr)) {
			return hr;
		}
		memcpy(buffer, data, sendBytes);
		hr = render->ReleaseBuffer(sendFrames, 0);
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
		data += sendBytes;
		size -= sendBytes;
		remainingFrames -= sendFrames;
		sentMs += framesToMs(sendFrames);
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
		feedEnds.push_back({*id, sentMs});
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
		return 0;
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

HRESULT WasapiPlayer::stop() {
	playState = PlayState::stopping;
	HRESULT hr = client->Stop();
	if (FAILED(hr)) {
		return hr;
	}
	hr = client->Reset();
	if (FAILED(hr)) {
		return hr;
	}
	// If there is a feed/sync call waiting, wake it up so it can immediately
	// return to the caller.
	SetEvent(wakeEvent);
	return S_OK;
}

void WasapiPlayer::completeStop() {
	nextFeedId = 0;
	sentMs = 0;
	feedEnds.clear();
	playState = PlayState::stopped;
}

HRESULT WasapiPlayer::sync() {
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
		deviceId.clear();
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

/*
 * NVDA calls the functions below. Most of these just wrap calls to
 * WasapiPlayer, with the exception of wasPlay_startup and wasPlay_getDevices.
 */

WasapiPlayer* wasPlay_create(wchar_t* deviceId, WAVEFORMATEX format,
	WasapiPlayer::ChunkCompletedCallback callback
) {
	return new WasapiPlayer(deviceId, format, callback);
}

void wasPlay_destroy(WasapiPlayer* player) {
	delete player;
}

HRESULT wasPlay_open(WasapiPlayer* player) {
	return player->open();
}

HRESULT wasPlay_close(WasapiPlayer* player) {
	return player->close();
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

/**
 * Get playback device ids and friendly names.
 * devicesStr will be set to a BSTR of device ids and names separated by null
 * characters; e.g. "id1\0name1\0id2\0name2\0"
 */
HRESULT wasPlay_getDevices(BSTR* devicesStr) {
	CComPtr<IMMDeviceEnumerator> enumerator;
	HRESULT hr = enumerator.CoCreateInstance(CLSID_MMDeviceEnumerator);
	if (FAILED(hr)) {
		return hr;
	}
	CComPtr<IMMDeviceCollection> devices;
	hr = enumerator->EnumAudioEndpoints(eRender, DEVICE_STATE_ACTIVE, &devices);
	if (FAILED(hr)) {
		return hr;
	}
	UINT count = 0;
	devices->GetCount(&count);
	std::wostringstream s;
	for (UINT d = 0; d < count; ++d) {
		CComPtr<IMMDevice> device;
		hr = devices->Item(d, &device);
		if (FAILED(hr)) {
			return hr;
		}
		wchar_t* id;
		hr = device->GetId(&id);
		if (FAILED(hr)) {
			return hr;
		}
		s << id << L'\0';
		CoTaskMemFree(id);
		CComPtr<IPropertyStore> props;
		hr = device->OpenPropertyStore(STGM_READ, &props);
		if (FAILED(hr)) {
			return hr;
		}
		PROPVARIANT val;
		hr = props->GetValue(PKEY_Device_FriendlyName, &val);
		if (FAILED(hr)) {
			return hr;
		}
		s << val.pwszVal << L'\0';
		PropVariantClear(&val);
	}
	*devicesStr = SysAllocStringLen(s.str().c_str(), (UINT)s.tellp());
	return S_OK;
}
