//Copyright (c) 2007 Michael Curran <mick@kulgan.net>
//This file is covered by the GNU General Public Licence

#ifndef RPCSRV_H
#define RPCSRV_H

#include <windows.h>

#define DLLEXPORT extern "C" __declspec(dllexport)

DLLEXPORT RPC_STATUS startServer();
DLLEXPORT RPC_STATUS stopServer();
 
#endif
