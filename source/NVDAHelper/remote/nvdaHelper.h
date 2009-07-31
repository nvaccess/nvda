//Copyright (c) 2007 Michael Curran <mick@kulgan.net>
//This file is covered by the GNU General Public Licence

#ifndef NVDAHELPER_H
#define NVDAHELPER_H

#define DLLEXPORT extern "C" __declspec(dllexport)

//Exported functions
DLLEXPORT int nvdaHelper_initialize();
DLLEXPORT int nvdaHelper_terminate();

#endif