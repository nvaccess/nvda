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

#include "hook.cpp"

using namespace MinHook;

//Based on MH_EnableHook from minHook
MH_STATUS _doAllHooks(bool enable) {
	CriticalSection::ScopedLock lock(gCS);
	if (!gIsInitialized) {
		return MH_ERROR_NOT_INITIALIZED;
	}
	std::vector<uintptr_t> oldIPs;
	std::vector<uintptr_t> newIPs;
	for(std::vector<HOOK_ENTRY>::iterator hooksIter=gHooks.begin();hooksIter!=gHooks.end();++hooksIter) {
		oldIPs.insert(oldIPs.end(),hooksIter->oldIPs.begin(),hooksIter->oldIPs.end());
		newIPs.insert(newIPs.end(),hooksIter->newIPs.begin(),hooksIter->newIPs.end());
	}
	{
		ScopedThreadExclusive tex(oldIPs, newIPs);
		for(std::vector<HOOK_ENTRY>::iterator hooksIter=gHooks.begin();hooksIter!=gHooks.end();++hooksIter) {
			HOOK_ENTRY*pHook=&(*hooksIter);
			if (pHook->isEnabled==enable) continue;
			DWORD oldProtect;
			if (!VirtualProtect(pHook->pTarget, sizeof(JMP_REL), PAGE_EXECUTE_READWRITE, &oldProtect)) {
				return MH_ERROR_MEMORY_PROTECT;
			}
			if(enable) {
#if defined _M_X64
				WriteRelativeJump(pHook->pTarget, pHook->pRelay);
#elif defined _M_IX86
				WriteRelativeJump(pHook->pTarget, pHook->pDetour);
#endif
			} else {
				memcpy(pHook->pTarget, pHook->pBackup, sizeof(JMP_REL));
			}
			VirtualProtect(pHook->pTarget, sizeof(JMP_REL), oldProtect, &oldProtect);
				pHook->isEnabled = enable;
		}
	}
	return MH_OK;
}

MH_STATUS MH_EnableAllHooks() {
	return _doAllHooks(true);
}

MH_STATUS MH_DisableAllHooks() {
	return _doAllHooks(false);
}

