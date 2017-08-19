/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2008-2017 NV Access Limited, Derek Riemer.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/
// This file can only compile for Vista and above
// NVDA will not call this function on lower operating Systems
#undef _WIN32_WINNT
#define _WIN32_WINNT 0x0600  

#include <comdef.h>
#include <comip.h>
#include <windows.h>
#include <mmdeviceapi.h>
#include <endpointvolume.h>
#include <common/log.h>

_COM_SMARTPTR_TYPEDEF(IMMDeviceEnumerator, __uuidof(IMMDeviceEnumerator));
_COM_SMARTPTR_TYPEDEF(IMMDeviceCollection, __uuidof(IMMDeviceCollection));
_COM_SMARTPTR_TYPEDEF(IMMDevice, __uuidof(IMMDevice));
_COM_SMARTPTR_TYPEDEF(IAudioMeterInformation, __uuidof(IAudioMeterInformation));
_COM_SMARTPTR_TYPEDEF(IAudioEndpointVolume, __uuidof(IAudioEndpointVolume));

/*
	* Should NVDA delay speech slightly when beginning to duck other audio?
	* @return true if other audio is playing or there is an error for any device. Or in other words, false only if all devices can be checked, and they  all have a peak of 0. 
	*/
bool audioDucking_shouldDelay() {
	HRESULT res;
	IMMDeviceEnumeratorPtr pMMDeviceEnumerator=NULL;
	res=pMMDeviceEnumerator.CreateInstance(__uuidof(MMDeviceEnumerator),NULL,CLSCTX_INPROC_SERVER);
	if(res!=S_OK||!pMMDeviceEnumerator) {
		LOG_ERROR(L"Cannot create MMDeviceEnumerator: "<<res);
		return true;
	}
	IMMDeviceCollectionPtr pMMDeviceCollection=NULL;
	res=pMMDeviceEnumerator->EnumAudioEndpoints(eRender,DEVICE_STATE_ACTIVE,&pMMDeviceCollection);
	if(res!=S_OK||!pMMDeviceCollection) {
		LOG_ERROR(L"Cannot enumerate audio endpoints");
		return true;
	}
	UINT count=0;
	pMMDeviceCollection->GetCount(&count);
	bool foundAudio=false;
	for(UINT i=0;i<count;++i) {
		IMMDevicePtr pMMDevice=NULL;
		res=pMMDeviceCollection->Item(i,&pMMDevice);
		if(res!=S_OK||!pMMDevice) {
			LOG_WARNING(L"Cannot fetch device "<<i<<L" from MMDeviceCollection: "<<res);
			continue;
		}
		IAudioMeterInformationPtr pAudioMeterInformation=NULL;
		res=pMMDevice->Activate(__uuidof(IAudioMeterInformation),CLSCTX_ALL,NULL,(void**)&pAudioMeterInformation);
		if(res!=S_OK||!pAudioMeterInformation) {
			LOG_WARNING(L"Cannot fetch audio meter information from device "<<i<<L": "<<res);
			continue;
		}
		float volume=0;
		res=pAudioMeterInformation->GetPeakValue(&volume);
		if(res!=S_OK) {
			LOG_WARNING(L"Cannot fetch peak value from audio meter information for device "<<i<<L": "<<res);
			continue;
		}
		if(volume>0) return true;
		foundAudio=true;
	}
	if(!foundAudio) {
		LOG_ERROR(L"Could not get peak meter value from any audio device");
		return true;
	}
	return false;
}

/*
	* Tell NVDA to unmute the system.
	* @return true if NVDA was successfully able to unmute the system, or if no change was necessary or   false if there was an error checking mute status, or setting the new mute status.
	*/
bool unmuteActiveDevice() {
	HRESULT res;
	IMMDeviceEnumeratorPtr pMMDeviceEnumerator=NULL;
	res=pMMDeviceEnumerator.CreateInstance(__uuidof(MMDeviceEnumerator),NULL,CLSCTX_INPROC_SERVER);
	if(res!=S_OK||!pMMDeviceEnumerator) {
		LOG_ERROR(L"Cannot create MMDeviceEnumerator: "<<res);
		return false;
	}
	IMMDevicePtr pMMDevice=NULL;
	res = pMMDeviceEnumerator->GetDefaultAudioEndpoint(eRender, eConsole, &pMMDevice);
	if(res!=S_OK||!pMMDevice) {
		LOG_WARNING(L"Cannot fetch default device"<<res);
		return false;
	}
	IAudioEndpointVolumePtr pAudioEndpointVolume=NULL;
	res = pMMDevice->Activate(__uuidof(IAudioEndpointVolume),CLSCTX_ALL, NULL, (void**)&pAudioEndpointVolume);
	if(res!=S_OK||!pAudioEndpointVolume) {
		LOG_WARNING(L"Cannot Activate Endpoint volume" << res);
		return false;
	}
	//Force the mute state to false, reguardless.
	res = pAudioEndpointVolume->SetMute(false, NULL);
	//If we changed it, we get S_OK if not, but success, we get S_FALSE.
	if(res == S_OK || res == S_FALSE)
		return true;
	else
		return false;
}