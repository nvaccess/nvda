/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2006-2019 NV Access Limited, Babbage B.V.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#ifndef NVDAHELPER_REMOTE_GDIUTILS_H
#define NVDAHELPER_REMOTE_GDIUTILS_H

#include <windows.h>

/**
 * converts given points from dc coordinates to screen coordinates. 
 * @param hdc a handle to a device context
 * @param points a pointer to the points you wish to convert.
 * @param count the number of points you want to convert.
 */
void logicalPointsToScreenPoints(HDC hdc, POINT* points, int count,bool relative);

/**
 * converts given points from absolute screen coordinates to dc coordinates. 
 * @param hdc a handle to a device context
 * @param points a pointer to the points you wish to convert.
 * @param count the number of points you want to convert.
 */
void screenPointsToLogicalPoints(HDC hdc, POINT* points, int count);

#endif
