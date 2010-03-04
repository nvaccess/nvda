#ifndef NVDAHELPER_REMOTE_GDIHOOKS_H
#define NVDAHELPER_REMOTE_GDIHOOKS_H

#include <map>
#include <windows.h>
#include "displayModel.h"

typedef std::map<HWND,displayModel_t*> displayModelsByWindow_t;
extern displayModelsByWindow_t displayModelsByWindow;

void gdiHooks_inProcess_initialize();
void gdiHooks_inProcess_terminate();

#endif