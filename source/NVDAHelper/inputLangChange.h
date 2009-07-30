//Copyright (c) 2007 Michael Curran <mick@kulgan.net>
//This file is covered by the GNU General Public Licence

#ifndef INPUTLANGCHANGE_H
#define INPUTLANGCHANGE_H

#include <windows.h>
#include <wchar.h>

//Event IDs
#define EVENT_INPUTLANGCHANGE 0x1001

void inputLangChange_inThread_initialize();
void inputLangChange_inThread_terminate();

#endif