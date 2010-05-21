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
#include <windows.h>
#include "winIPCUtils.h"

using namespace std;

#define nvdaControllerNcalrpcPortBase L"NvdaCtlr"

int getNVDAControllerNcalrpcEndpointString(wchar_t* buf, int cch, BOOL fullAddress) {
	DWORD sessionId=0;
	ProcessIdToSessionId(GetCurrentProcessId(),&sessionId);
	HANDLE hDesk=GetThreadDesktop(GetCurrentThreadId());
	wchar_t deskName[32];
	GetUserObjectInformation(hDesk,UOI_NAME,deskName,sizeof(deskName),NULL);
	wostringstream s;
	if(fullAddress) 		s<<L"ncalrpc:[";
	s<<nvdaControllerNcalrpcPortBase<<"."<<sessionId<<"."<<deskName;
	if(fullAddress) s<<L"]";
	int len=s.str().length();
	if(!buf||(cch<=0)) return len;
	wcscpy_s(buf,cch,s.str().c_str());
	return min(len,cch);
}
