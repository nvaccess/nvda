/*
Header for utilities for use in nvdaHelperLocalWin10 modules.
This file is a part of the NVDA project.
URL: http://www.nvaccess.org/
Copyright 2017 Tyler Spivey, NV Access Limited.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#include <robuffer.h>

byte* getBytes(Windows::Storage::Streams::IBuffer^ buffer);
