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

extern std::map<HWND,int> windowsForTextChangeNotifications; 
extern displayModelsMap_t<HWND> displayModelsByWindow;

void gdiHooks_inProcess_initialize();
void gdiHooks_inProcess_terminate();

#endif