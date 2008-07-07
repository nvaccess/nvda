//Copyright (c) 2007 Michael Curran <mick@kulgan.net>
//This file is covered by the GNU General Public Licence

#ifndef HOOKMANAGER_H
#define HOOKMANAGER_H

#include <windows.h>
#include <wchar.h>

#define DLLEXPORT __declspec(dllexport)

//Private variables
extern HINSTANCE moduleHandle;
extern BOOL isManagerInitialized;

//Exported functions
DLLEXPORT int initialize();
DLLEXPORT int terminate();

#endif