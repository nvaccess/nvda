/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright (C) 2017 NV Access Limited.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#ifndef NVDAHELPER_COMPROXYREGISTRATION
#define NVDAHELPER_COMPROXYREGISTRATION

#include <string>
#include <locale>
#include <codecvt>
#include <vector>
#define WIN32_LEAN_AND_MEAN 
#include <windows.h>
#include <objbase.h>

// Tracks information about a COM interface registered in-process
typedef struct {
	// The name of the interface (for debugging)
	std::wstring name;
	// The unique identifier of the interface 
	IID iid;
	// The CLSID of the original class object that handled creating / proxying of this interface.
	// Used when unregistering, so we can put things back the way they were
	CLSID clsid;
} PSClsidBackup_t;

// Represents the registration of a COM proxy dll and its interfaces.
// this can be used for later unregistration of the COM proxy dll
typedef struct {
	// The path to the dll (for debugging)
	std::wstring dllPath;
	// The cookie returned by CoRegisterClassObject, for later unregistration via CoRevokeClassObject
	ULONG_PTR classObjectRegistrationCookie;
	// Information for all the interfaces registered for this proxy dll via CoRegisterPSClsid
	std::vector<PSClsidBackup_t> psClsidBackups;
} COMProxyRegistration_t;

/* Registers a COM proxy dll and all its interfaces for this process so that they can be marshalled to/from other processes
	@param dllPath the relative path to the proxy dll (relative from this dll)
	@return registration data which can be later passed to UnregisterCOMProxy.
	*/
COMProxyRegistration_t* registerCOMProxy(wchar_t* dllPath);

/* Unregisters a COM proxy dll originally registered with registerCOMProxy
	@param reg the registration data returned by registerCOMProxy.
	@return true if successful, false otherwise
	*/
bool unregisterCOMProxy(COMProxyRegistration_t* reg);

#endif

