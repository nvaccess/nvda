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

//Copyright (c) 2007 Michael Curran <mick@kulgan.net>
//This file is covered by the GNU General Public Licence

#ifndef IA2SUPPORT_H
#define IA2SUPPORT_H

#include <map>
#include "COMProxyRegistration.h"

struct IA2InstallData {
	COMProxyRegistration_t* IA2ProxyRegistration;
	COMProxyRegistration_t* ISimpleDOMProxyRegistration;
	HANDLE uiThreadHandle;
	HANDLE uiThreadUninstalledEvent;
};

bool installIA2Support();
bool uninstallIA2Support();

//Private functions

std::pair<std::map<DWORD, IA2InstallData>::iterator, bool> installIA2SupportForThread(DWORD threadID);
bool uninstallIA2SupportForThread(DWORD threadID);
void IA2Support_inProcess_initialize();
void IA2Support_inProcess_terminate();

#endif
