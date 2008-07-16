//Copyright (c) 2007 Michael Curran <mick@kulgan.net>
//This file is covered by the GNU General Public Licence

#ifndef IA2SUPPORT_H
#define IA2SUPPORT_H

#include <windows.h>
#include <wchar.h>

//Private variables
extern BOOL isIA2Initialized;

//Private functions
BOOL IA2Support_initialize();
BOOL installIA2Support();
BOOL uninstallIA2Support();
BOOL IA2Support_terminate();

#endif