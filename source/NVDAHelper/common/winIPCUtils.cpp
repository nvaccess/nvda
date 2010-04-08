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
