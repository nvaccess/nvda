#ifndef NVDAHELPER_REMOTE_GDIHOOKS_H
#define NVDAHELPER_REMOTE_GDIHOOKS_H

#include <map>
#include <windows.h>
#include "displayModel.h"
#include <common/lock.h>

template <typename t> class displayModelsMap_t: public std::map<t,displayModel_t*>, public LockableObject {
	public:
	displayModelsMap_t(): map<t,displayModel_t*>(), LockableObject() {
	}
};

extern displayModelsMap_t<HWND> displayModelsByWindow;

void gdiHooks_inProcess_initialize();
void gdiHooks_inProcess_terminate();

#endif