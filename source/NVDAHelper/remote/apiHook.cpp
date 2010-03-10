#include <set>
#include <windows.h>
#include <MinHook.h>
#include "apiHook.h"

using namespace std;

typedef multiset<HMODULE> moduleSet_t;
typedef set<void*> funcSet_t;

moduleSet_t g_hookedModules;
funcSet_t g_hookedFunctions;

void* apiHook_hookFunction(const char* moduleName, const char* functionName, void* newHookProc) {
	HMODULE moduleHandle=LoadLibraryA(moduleName);
	if(!moduleHandle) {
		fprintf(stderr,"apiHook_hookFunction: module %s not loaded\n");
		return NULL;
	}
	void* realFunc=GetProcAddress(moduleHandle,functionName);
	if(!realFunc) {
		fprintf(stderr,"apiHook_hookFunction: function %s does not exist in module %s\n",functionName,moduleName);
		FreeLibrary(moduleHandle);
		return NULL;
	}
	if(g_hookedFunctions.empty()) {
		printf("apiHook_hookFunction: calling MH_Initialize\n");
		MH_Initialize();
	} else if(g_hookedFunctions.count(realFunc)>0) {
		fprintf(stderr,"apiHook_hookFunction: function %s in module %s is already hooked, returnning false\n",functionName,moduleName);
		FreeLibrary(moduleHandle);
		return FALSE;
	}
	printf("apiHook_hookFunction: requesting to hook function %s at address 0X%X in module %s at address 0X%X with  new function at address 0X%X\n",functionName,realFunc,moduleName,moduleHandle,newHookProc);
	void* origFunc;
	int res;
	if((res=MH_CreateHook(realFunc,newHookProc,&origFunc))!=MH_OK) {
		fprintf(stderr,"apiHook_hookFunction: MH_CreateHook failed with %d\n", res);
		return NULL;
	}
	if((res=MH_EnableHook(realFunc))!=MH_OK) {
		fprintf(stderr,"apiHook_hookFunction: MH_EnableHook failed with %d\n", res);
		return NULL;
	}
	g_hookedModules.insert(moduleHandle);
	g_hookedFunctions.insert(realFunc);
	printf("apiHook_hookFunction: successfully hooked function %s in module %s with hook procedure at address 0X%X, returning true\n",functionName,moduleName,newHookProc);
	return origFunc;
}

BOOL apiHook_unhookFunctions() {
	for(funcSet_t::iterator i=g_hookedFunctions.begin();i!=g_hookedFunctions.end();i++) {
		MH_DisableHook(*i);
	}
	MH_Uninitialize();
	g_hookedFunctions.clear();
	for(moduleSet_t::iterator i=g_hookedModules.begin();i!=g_hookedModules.end();i++) {
		FreeLibrary(*i);
	}
	g_hookedModules.clear();
	return TRUE;
}
