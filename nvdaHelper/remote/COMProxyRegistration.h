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

// Represents the registration of a COM proxy dll and its interfaces.
// this can be used for later unregistration of the COM proxy dll
typedef struct {
	// The path to the dll (for debugging)
	std::wstring dllPath;
	// The cookie returned by CoRegisterClassObject, for later unregistration via CoRevokeClassObject
	ULONG_PTR classObjectRegistrationCookie;
	std::map<std::wstring, IID> registeredInterfaces;
} COMProxyRegistration_t;

/* Registers a COM proxy dll and all its interfaces for this process so that they can be marshalled to/from other processes
	@param dllPath the relative path to the proxy dll (relative from this dll)
	@return registration data which can be later passed to UnregisterCOMProxy.
	*/
COMProxyRegistration_t* registerCOMProxy(const wchar_t* dllPath);

/* Unregisters a COM proxy dll originally registered with registerCOMProxy
	@param reg the registration data returned by registerCOMProxy.
	@return true if successful, false otherwise
	*/
bool unregisterCOMProxy(COMProxyRegistration_t* reg);

/* Registers a proxy for the specified interface, and backs up the original proxy CLSID for later restoration.
	@param interfaceName the name of the interface (for debugging)
	@param dllPath the relative path to the proxy dll (relative from this dll)
	@param iid the IID of the interface to register the proxy for
	@param clsid the CLSID of the proxy to register for this interface
	@return true if successful, false otherwise
	*/
bool registerInterfaceProxy(std::wstring interfaceName, std::wstring dllPath, IID iid, CLSID clsid);

/* Unregisters the proxy for the specified interface, restoring the original proxy CLSID if it was changed when registering the proxy.
	@param iid the IID of the interface to unregister the proxy for
	@return void
	*/
bool unregisterInterfaceProxy(IID iid);

/* Clears the cache used for storing generated proxy CLSIDs for dlls. Should be called when NVDA unloads from this process to free cached CLSIDs.
	@return void
	*/
void clearCOMProxyRegistrationCache();

/* Clears the cache used for storing original proxy CLSIDs for interfaces. Should be called when NVDA unloads from this process to free cached CLSIDs.
	@return void
	*/
void clearInterfaceProxyBackups();

#endif
