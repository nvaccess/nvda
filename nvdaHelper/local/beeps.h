/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2006-2015 NVDA contributers.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#ifndef BEEPS_H_INCLUDED
#define BEEPS_H_INCLUDED

#include "nvdaHelperLocal.h"

int generateBeep(short* buf, const float hz, const int length, const int left=50, const int right=50);

#endif
