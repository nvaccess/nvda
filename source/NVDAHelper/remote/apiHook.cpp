#include <set>
#include <windows.h>
#include "apiHook.h"

using namespace std;

#pragma pack(push)
#pragma pack(1)
typedef struct {
	byte longJumpCode;
	long longJumpAddress;
	byte shortJumpCode;
	byte shortJumpAddress;
} hotPatchProlog_t; 
#pragma pack(pop)

#define OPCODE_MOVE 0X8B
#define REGISTERCODE_EDI 0XFF
#define OPCODE_JUMP8 0XEB
#define OPCODE_JUMP32 0XE9
 
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
	byte* byteAddr=(byte*)realFunc;
	if(g_hookedFunctions.count(realFunc)>0) {
		fprintf(stderr,"apiHook_hookFunction: function %s in module %s is already hooked, returnning false\n",functionName,moduleName);
		FreeLibrary(moduleHandle);
		return FALSE;
	}
	printf("apiHook_hookFunction: requesting to hook function %s at address 0X%X in module %s at address 0X%X with  new function at address 0X%X\n",functionName,realFunc,moduleName,moduleHandle,newHookProc);
	if(byteAddr[0]!=OPCODE_MOVE||byteAddr[1]!=REGISTERCODE_EDI) {
		fprintf(stderr,"apiHook_hookFunction: unable to patch function at address 0X%X, function not compiled for hot patching. Returnning NULL\n",realFunc);
		FreeLibrary(moduleHandle);
		return NULL;
	}
	hotPatchProlog_t prolog={OPCODE_JUMP32,(byte*)newHookProc-byteAddr,OPCODE_JUMP8,-7};
	byteAddr-=5;
	DWORD oldProtect;
	VirtualProtect(byteAddr,7,PAGE_EXECUTE_READWRITE,&oldProtect);
	memcpy(byteAddr,&prolog,7);
	VirtualProtect(byteAddr,7,oldProtect,&oldProtect);
	g_hookedModules.insert(moduleHandle);
	g_hookedFunctions.insert(realFunc);
	printf("apiHook_hookFunction: successfully hooked function %s in module %s with hook procedure at address 0X%X, returning true\n",functionName,moduleName,newHookProc);
	return byteAddr+7;
}

BOOL apiHook_unhookFunctions() {
	for(funcSet_t::iterator i=g_hookedFunctions.begin();i!=g_hookedFunctions.end();i++) {
		void* realFunc=*i;
		byte* byteAddr=(byte*)realFunc;
		if(byteAddr[0]!=OPCODE_JUMP8||byteAddr[1]!=(byte)-7) {
			continue;
		}
		byte defaultBytes[2]={OPCODE_MOVE,REGISTERCODE_EDI};
		DWORD oldProtect;
		VirtualProtect(realFunc,2,PAGE_EXECUTE_READWRITE,&oldProtect);
		memcpy(realFunc,defaultBytes,2);
		VirtualProtect(realFunc,2,oldProtect,&oldProtect);
	}
	g_hookedFunctions.clear();
	for(moduleSet_t::iterator i=g_hookedModules.begin();i!=g_hookedModules.end();i++) {
		FreeLibrary(*i);
	}
	g_hookedModules.clear();
	return TRUE;
}
