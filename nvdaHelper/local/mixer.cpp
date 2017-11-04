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

#include <comdef.h>
#include <comip.h>
#include <windows.h>
#include <mmdeviceapi.h>
#include <endpointvolume.h>
#include <Mmddk.h>
#include <common/log.h>

_COM_SMARTPTR_TYPEDEF(IMMDeviceEnumerator, __uuidof(IMMDeviceEnumerator));
_COM_SMARTPTR_TYPEDEF(IMMDeviceCollection, __uuidof(IMMDeviceCollection));
_COM_SMARTPTR_TYPEDEF(IMMDevice, __uuidof(IMMDevice));
_COM_SMARTPTR_TYPEDEF(IAudioMeterInformation, __uuidof(IAudioMeterInformation));
_COM_SMARTPTR_TYPEDEF(IAudioEndpointVolume, __uuidof(IAudioEndpointVolume));

/*
	* Given an input waveOut id, convert to an EndPoint ID.
*/
WCHAR *waveOutIDToEndpointID(const int waveOutID){
	MMRESULT mmr;
	size_t endpointIDSize;
	//We have to convert to an HWAVEOUT for sending the message.
	//Get the size of the endpoint ID string.
	mmr = waveOutMessage((HWAVEOUT)IntToPtr(waveOutID),
		DRV_QUERYFUNCTIONINSTANCEIDSIZE,
		(DWORD_PTR)&endpointIDSize, NULL);
	if (mmr != MMSYSERR_NOERROR) {
		return nullptr; //Asking the driver for the size of the endpoint id string failed.
	}
	//Need to include room for the null at the end.
	endpointIDSize += 1;
	//WCHAR *endpointID = (WCHAR*)CoTaskMemAlloc(endpointIDSize);
	WCHAR *endpointID = new WCHAR[endpointIDSize];
	if(endpointID == nullptr) //out of memory!
		return nullptr;
	endpointID[endpointIDSize] = '\0';
	mmr = waveOutMessage((HWAVEOUT)IntToPtr(waveOutID),
	DRV_QUERYFUNCTIONINSTANCEID,
	(DWORD_PTR)endpointID,
	endpointIDSize);
	if (mmr != MMSYSERR_NOERROR)
	{
		return nullptr; //Can't get endpoint id from the device.
	}
	return endpointID;
}

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
	* Tell NVDA to apply unmuting and volume gain to systems where the audio is not perceivable. 
	* This only applys fixes to devices which are muted, or at volume 0, definitely not audible.
	* @param: deviceID: The device id (from waveOut) needed to fetch this device. the mapper is also supported.
	* @return true if NVDA was successfully able to unmute the system, or if no change was necessary or   false if there was an error checking mute status, or setting the new mute status.
	*/
bool applyActiveDeviceAudioFixes(const int deviceID) {
	HRESULT res;
	IMMDeviceEnumeratorPtr pMMDeviceEnumerator=NULL;
	res=pMMDeviceEnumerator.CreateInstance(__uuidof(MMDeviceEnumerator),NULL,CLSCTX_INPROC_SERVER);
	if(res!=S_OK||!pMMDeviceEnumerator) {
		LOG_ERROR(L"Cannot create MMDeviceEnumerator: "<<res);
		return false;
	}
	IMMDevicePtr pMMDevice=NULL;
	if(deviceID == -1){
		res = pMMDeviceEnumerator->GetDefaultAudioEndpoint(eRender, eConsole, &pMMDevice);	
	}
	else {
		WCHAR *id = waveOutIDToEndpointID(deviceID);
		if(id == nullptr){
			return false;
		}
		res = pMMDeviceEnumerator->GetDevice((LPCWSTR)id, &pMMDevice);
		delete[] id;
	}
	if(res!=S_OK||!pMMDevice) {
		LOG_WARNING(L"Cannot fetch requested device"<<res);
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
	if(!(res == S_OK || res == S_FALSE))
		return false;
	UINT step=0;
	UINT stepCount=0;
	res = pAudioEndpointVolume->GetVolumeStepInfo(&step, &stepCount);
	if(res != S_OK)
		return false;
	if(step == 0){
		//Move the volume up 5 steps. We could do it by math, but this way, we know it moved exactly 5 steps, no rounding error from us.
		for(UINT i=0;i<5;i++){
			res = pAudioEndpointVolume->VolumeStepUp(NULL);
			if(res != S_OK)
				return false;
		}
	}
	return true;
}
