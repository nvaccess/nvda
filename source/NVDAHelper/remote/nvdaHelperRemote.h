//Copyright (c) 2007 Michael Curran <mick@kulgan.net>
//This file is covered by the GNU General Public Licence

#ifndef NVDAHELPERREMOTE_H
#define NVDAHELPERREMOTE_H

#define DLLEXPORT extern "C" __declspec(dllexport)

//Exported functions
DLLEXPORT int nvdaHelper_initialize();
DLLEXPORT int nvdaHelper_terminate();

#endif