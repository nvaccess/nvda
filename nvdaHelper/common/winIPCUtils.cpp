/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2006-2010 NVDA contributers.
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License version 2.1, as published by
the Free Software Foundation.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
*/

#include <cwchar>
#include <string>
#include <sstream>
#define WIN32_LEAN_AND_MEAN 
#include <windows.h>
#include "winIPCUtils.h"

using namespace std;

size_t generateDesktopSpecificNamespace(wchar_t* buf, size_t cch) {
	DWORD sessionId=0;
	ProcessIdToSessionId(GetCurrentProcessId(),&sessionId);
	HANDLE hDesk=GetThreadDesktop(GetCurrentThreadId());
	wchar_t deskName[32];
	GetUserObjectInformation(hDesk,UOI_NAME,deskName,sizeof(deskName),NULL);
	wostringstream s;
	s<<sessionId<<"."<<deskName;
	size_t len=s.str().length();
	if(!buf||(cch==0)) return len;
	wcsncpy(buf,s.str().c_str(),cch);
	return min(len,cch);
}
