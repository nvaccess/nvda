//Copyright (c) 2007 Michael Curran <mick@kulgan.net>
//This file is covered by the GNU General Public Licence

#ifndef IA2SUPPORT_H
#define IA2SUPPORT_H

#include <windows.h>
#include <wchar.h>

//Private variables
extern BOOL isIA2Initialized;

//Private functions
void IA2Support_initialize();
void installIA2Support();

#endif