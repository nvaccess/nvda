/*
Code for utilities for use in nvdaHelperLocalWin10 modules.
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

#include <collection.h>
#include <wrl.h>
#include <robuffer.h>
#include <common/log.h>

using namespace Windows::Storage::Streams;
using namespace Microsoft::WRL;

byte* getBytes(IBuffer^ buffer) {
	// We want direct access to the buffer rather than copying it.
	// To do this, we need to get to the IBufferByteAccess interface.
	// See http://cm-bloggers.blogspot.com/2012/09/accessing-image-pixel-data-in-ccx.html
	ComPtr<IInspectable> insp = reinterpret_cast<IInspectable*>(buffer);
	ComPtr<IBufferByteAccess> bufferByteAccess;
	if (FAILED(insp.As(&bufferByteAccess))) {
		LOG_ERROR(L"Couldn't get IBufferByteAccess from IBuffer");
		return nullptr;
	}
	byte* bytes = nullptr;
	bufferByteAccess->Buffer(&bytes);
	return bytes;
}
