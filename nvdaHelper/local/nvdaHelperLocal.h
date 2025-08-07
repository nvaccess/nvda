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

#ifndef NVDAHELPERLOCAL_H
#define NVDAHELPERLOCAL_H
#include <rpc.h>

handle_t createRemoteBindingHandle(wchar_t* uuidString);
LRESULT cancellableSendMessageTimeout(HWND hwnd, UINT Msg, WPARAM wParam, LPARAM lParam, UINT fuFlags, UINT uTimeout, PDWORD_PTR lpdwResult);
/*
 * Initializes the NVDAHelper local library
 * @param secureMode true specifies that the NVDA process initializing NVDAHelper is in secure mode
 */
void nvdaHelperLocal_initialize(bool secureMode);
void nvdaHelperLocal_terminate();
/*
 * Calculate the start offsets for characters in a string.
 * @param text: The text to calculate offsets for.
 * @param textLength: The length of the provided text, encluding a terminating NULL character.
 * @param offsets: An array of size textLength allocated by the caller to fill with offsets.
 * @param offsetsCount: The number of offsets in the array after calculation.
 */
bool calculateCharacterBoundaries(const wchar_t* text, int textLength, int* offsets, int* offsetsCount);

#endif
