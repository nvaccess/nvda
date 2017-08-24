/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2006-2010 NVDA contributers.
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

typedef struct {
	std::wstring name;
	IID iid;
	CLSID clsid;
} PSClsidBackup_t;

typedef struct {
	std::wstring dllPath;
	ULONG_PTR classObjectRegistrationCookie;
	std::vector<PSClsidBackup_t> psClsidBackups;
} COMProxyRegistration_t;

COMProxyRegistration_t* registerCOMProxy(wchar_t* dllPath);
bool unregisterCOMProxy(COMProxyRegistration_t* reg);

#endif

