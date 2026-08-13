/*
A part of NonVisual Desktop Access (NVDA)
Copyright (C) 2026 NV Access Limited, Cary-rowen
This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
*/

#pragma once

#include <windows.h>

#define export __declspec(dllexport)

extern "C" {

/** Return whether the required WGC monitor-capture APIs are available. */
export bool __stdcall wgcCapture_isSupported();

/**
 * Capture a virtual-screen region using Windows Graphics Capture.
 *
 * The source and destination dimensions must be non-zero, and the region must
 * intersect at least one monitor. Each intersecting monitor is captured and
 * composited, and remaining pixels outside all monitors are black. The captured
 * region is scaled to destinationWidth by destinationHeight and written as
 * top-down RGBQUAD pixels with rgbReserved set to 0. image must point to a
 * buffer containing at least destinationWidth * destinationHeight RGBQUAD elements.
 */
export bool __stdcall wgcCapture_captureScreenRegion(
	int screenX,
	int screenY,
	unsigned int width,
	unsigned int height,
	RGBQUAD* image,
	unsigned int destinationWidth,
	unsigned int destinationHeight
);

}
