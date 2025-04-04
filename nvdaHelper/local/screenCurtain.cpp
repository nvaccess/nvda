/**
 * A part of NonVisual Desktop Access (NVDA)
 * This file is covered by the GNU General Public License.
 * See the file COPYING for more details.
 * Copyright (C) 2025 NV Access Limited
 *
 * Utilities for Screen Curtain.
 *
 * Must be linked with Gdi32.lib and Gdiplus.lib.
*/
#define GDIPVER 0x110   // GDIPlus 1.1, required for histograms.
#include <windows.h>
#include <common/log.h>
#include <gdiplus.h>
#include <memory>
#include <wil/resource.h>
#include <string>

using namespace Gdiplus;
using namespace std;

/**
 * @brief Captures the entire virtual screen and determines if the screen is entirely black.
 *
 * This function captures the contents of the virtual screen, which is the bounding rectangle
 * of all monitors on the system. It creates a device-independent bitmap (DIB) from the captured
 * screen and calculates a histogram of colors to determine if the screen is entirely black.
 *
 * @return true if the screen is entirely black, false otherwise or if an error occurs.
 *
 * @details
 * - The function retrieves the dimensions and origin of the virtual screen using `GetSystemMetrics`.
 * - It creates a compatible device context and bitmap for capturing the screen.
 * - The screen contents are copied into the compatible device context using `BitBlt`.
 * - The captured bitmap is converted into a device-independent bitmap (DIB) using `GetDIBits`.
 * - A GDI+ bitmap is created from the DIB, and a histogram of colors is calculated.
 * - The function checks if the histogram indicates that the entire screen is black by verifying
 *   that the only color present is black (0, 0, 0) and that the count of black pixels matches
 *   the total screen area.
 *
 * @note
 * - The function uses the GDI+ library for bitmap manipulation and histogram calculation.
 * - Error handling is implemented to log and handle failures at various stages.
 * - Per <https://learn.microsoft.com/en-us/windows/win32/gdi/the-virtual-screen>,
 *   We assume that the screen coordinates and dimensions fit within 16-bit integers.
 */
bool isScreenFullyBlack() {
	// The virtual screen is the bounding rectangle of all of the monitors on the system.
	int screenWidth = GetSystemMetrics(SM_CXVIRTUALSCREEN),
		screenHeight = GetSystemMetrics(SM_CYVIRTUALSCREEN),
		// While the primary monitor'sStatus top left corner is at the origin,
		// it is not necessarily at the top left of the virtual screen.
		// Thus, the top left of the virtual screen may be negative.
		screenOriginX = GetSystemMetrics(SM_XVIRTUALSCREEN),
		screenOriginY = GetSystemMetrics(SM_YVIRTUALSCREEN),
		// Screen coordinates are 16-bit integers,
		// and since 2^16 * 2^16 = 2^32,
		// the area of the screen is guaranteed to fit in an int on all supported platforms.
		screenArea = screenWidth * screenHeight,
		bytesWritten;
	UINT histogramSize;
	DWORD diScreenshotSize;
	HWND desktopWnd;
	BITMAP ddScreenshot;
	HGDIOBJ oldObj;
	BITMAPINFOHEADER diScreenshotHeader;
	bool bStatus;
	Status sStatus;

	// The desktop window covers the entire virtual screen.
	desktopWnd = GetDesktopWindow();
	if (desktopWnd == NULL) {
		LOG_ERROR(L"Failed to get handle for desktop window.");
		return false;
	}
	wil::unique_hdc_window desktopDc(GetDC(desktopWnd));
	if (!desktopDc.is_valid()) {
		LOG_ERROR(L"Failed to get device context for desktop.");
		return false;
	}
	wil::unique_hdc captureDc(CreateCompatibleDC(desktopDc.get()));
	if (!captureDc.is_valid()) {
		LOG_ERROR("Failed to create compatible device context.");
		return false;
	}
	wil::unique_hbitmap captureBitmap(CreateCompatibleBitmap(desktopDc.get(), screenWidth, screenHeight));
	if (captureBitmap == NULL) {
		LOG_ERROR(L"Failed to create compatible bitmap.");
		return false;
	}

	// Set captureDc to draw to captureBitmap.
	oldObj = SelectObject(captureDc.get(), captureBitmap.get());
	if (oldObj == NULL) {
		LOG_ERROR("Failed to select capture bitmap into capture device context.");
		return false;
	}

	// Replace the contents of captureDc with those of desktopDc
	bStatus = BitBlt(
		// Destination device context
		captureDc.get(),
		// Top left of destination
		0, 0,
		// Size of source and destination
		screenWidth, screenHeight,
		// Source device context
		desktopDc.get(),
		// Top left of source
		screenOriginX, screenOriginY,
		// Raster operation to perform.
		// In this case, replace destination with source.
		SRCCOPY
	);
	// Restore captureDC for safety.
	SelectObject(captureDc.get(), oldObj);
	if (!bStatus) {
		LOG_ERROR("Failed to bit blit desktop device context to capture device context. Error #" << GetLastError());
		return false;
	}

	// Get properties of captureBitmap
	bytesWritten = GetObject(captureBitmap.get(), sizeof(BITMAP), &ddScreenshot);
	if (bytesWritten == 0) {
		LOG_ERROR("Failed to get bitmap metadata.");
		return false;
	}

	// And use them to set the properties of the device independent bitmap.
	diScreenshotHeader.biSize = sizeof(BITMAPINFOHEADER);
	diScreenshotHeader.biWidth = ddScreenshot.bmWidth;
	diScreenshotHeader.biHeight = ddScreenshot.bmHeight;
	diScreenshotHeader.biPlanes = 1;  // Can only ever be 1
	diScreenshotHeader.biBitCount = 32;  // High byte unused
	diScreenshotHeader.biCompression = BI_RGB;  // Uncompressed
	diScreenshotHeader.biSizeImage = 0;  // Unneeded as uncompressed
	diScreenshotHeader.biXPelsPerMeter = 0;
	diScreenshotHeader.biYPelsPerMeter = 0;
	diScreenshotHeader.biClrUsed = 0;
	diScreenshotHeader.biClrImportant = 0; // All colours are needed

	// Calculate the size (in bytes) of the DIB.
	// Each scan line must be a multiple of 32bits long, including padding if necessary.
	// So add 31 to push us to that boundary if padding is needed.
	// If the scan line doesn't need any padding, adding 31 will make no difference,
	// since (32n + 31) / 32 = n R 31.
	diScreenshotSize = ((ddScreenshot.bmWidth * diScreenshotHeader.biBitCount + 31) / 32) * 4 * ddScreenshot.bmHeight;

	try {
		// Convert the device-dependent bitmap to a device-independent bitmap.
		// Initialise each byte to 1 as a canary.
		auto diScreenshotBits = make_shared<char[]>(diScreenshotSize, 1);
		bytesWritten = GetDIBits(
			// Source device context and device-dependent bitmap
			captureDc.get(), captureBitmap.get(),
			// Range of scan lines to copy
			0, (UINT)ddScreenshot.bmHeight,
			// Destination buffer
			diScreenshotBits.get(),
			// Format of DIB
			(BITMAPINFO*)&diScreenshotHeader, DIB_RGB_COLORS
		);
		if (bytesWritten == 0 || bytesWritten == ERROR_INVALID_PARAMETER) {
			LOG_ERROR(L"Failed to convert device dependent bitmap to device independent bitmap. Got " << bytesWritten << L".");
			return false;
		}

		// Create a GDI+ bitmap from the captured virtual screen, and calculate a histogram of colours.
		auto diScreenshot = make_shared<Bitmap>((BITMAPINFO*)&diScreenshotHeader, diScreenshotBits.get());
		sStatus = diScreenshot->GetHistogramSize(HistogramFormatARGB, &histogramSize);
		if (sStatus != Ok) {
			LOG_ERROR(L"Failed to calculate histogram size. Error #" << sStatus << L".");
			return false;
		}
		// Allocate size for the histogram.
		auto histR = make_shared<UINT[]>(histogramSize);
		auto histG = std::make_shared<UINT[]>(histogramSize);
		auto histB = std::make_shared<UINT[]>(histogramSize);

		diScreenshot->GetHistogram(HistogramFormatRGB, histogramSize, histR.get(), histG.get(), histB.get(), NULL);
		auto ssHist = make_unique<wostringstream>();
		*ssHist << L"Histogram of virtual screen:";
		for (UINT i = 0; i < histogramSize; i++) {
			*ssHist << L" (" << histR[i] << L", " << histG[i] << L", " << histB[i] << L")";
		}
		LOG_DEBUG(ssHist->str());

		// If the entire screen is black, then the only colour in the histogram must be (0, 0, 0).
		// Since the sum of values in each channel must be the number of pixels in the image,
		// if the screen is entirely black,
		// the 0th entry in each of the channels must be the number of pixels in the image.
		return histR[0] == screenArea && histG[0] == screenArea && histB[0] == screenArea;
	}
	catch (bad_alloc)
	{
		LOG_ERROR("Failed to allocate space on heap for requisite buffers.");
		return false;
	}
}
