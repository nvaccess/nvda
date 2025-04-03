#define GDIPVER 0x110
#include <shlwapi.h>
#include <windows.h>
#include <common/log.h>
#include <objidl.h>
#include <gdiplus.h>
#include <memory>
#include <functional>
#include <wil/resource.h>
using namespace Gdiplus;
using namespace std;
#pragma comment(lib, "Gdiplus.lib")

bool captureScreen() {
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
	bool bStatus ;
	Gdiplus::Status sStatus;

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
		SRCCOPY);
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
	diScreenshotHeader.biPlanes = 1;			  // Can only ever be 1
	diScreenshotHeader.biBitCount = 32;		  // High byte unused
	diScreenshotHeader.biCompression = BI_RGB; // Uncompressed
	diScreenshotHeader.biSizeImage = 0;		  // Unneeded as uncompressed
	diScreenshotHeader.biXPelsPerMeter = 0;
	diScreenshotHeader.biYPelsPerMeter = 0;
	diScreenshotHeader.biClrUsed = 0;
	diScreenshotHeader.biClrImportant = 0; // All colours are needed

	// Calculate the size (in bytes) of the DIB.
	diScreenshotSize = ((ddScreenshot.bmWidth * diScreenshotHeader.biBitCount + 31) / 32) * 4 * ddScreenshot.bmHeight;

	try {
		// Convert the device-dependent bitmap to a device-independent bitmap.
		auto diScreenshotBits = std::make_shared<char[]>(diScreenshotSize);
		bytesWritten = GetDIBits(
			// Source device context and device-dependent bitmap
			captureDc.get(), captureBitmap.get(),
			// Range of scan lines to copy
			0, (UINT)ddScreenshot.bmHeight,
			// Destination buffer
			diScreenshotBits.get(),
			// Format of DIB
			(BITMAPINFO *)&diScreenshotHeader, DIB_RGB_COLORS);
		if (bytesWritten == 0 || bytesWritten == ERROR_INVALID_PARAMETER) {
			LOG_ERROR(L"Failed to convert device dependent bitmap to device independent bitmap. Got " << bytesWritten << L".");
			return false;
		}

		// Create a GDI+ bitmap from the captured virtual screen, and calculate a histogram of colours.
		auto diScreenshot = make_shared<Bitmap>((BITMAPINFO *)&diScreenshotHeader, diScreenshotBits.get());
		sStatus = diScreenshot->GetHistogramSize(HistogramFormatARGB, &histogramSize);
		if (sStatus != Gdiplus::Ok) {
			LOG_ERROR(L"Failed to calculate histogram size. Error #" << sStatus << L".");
			return false;
		}
		// Allocate size for the histogram.
		auto histR = std::make_shared<UINT[]>(histogramSize);
		auto histG = std::make_shared<UINT[]>(histogramSize);
		auto histB = std::make_shared<UINT[]>(histogramSize);

		diScreenshot->GetHistogram(HistogramFormatRGB, histogramSize, histR.get(), histG.get(), histB.get(), NULL);

		// If the entire screen is black, then the only colour in the histogram must be (0, 0, 0).
		// Since the sum of values in each channel must be the number of pixels in the image,
		// if the screen is entirely black,
		// the 0th entry in each of the channels must be the number of pixels in the image.
		LOG_INFO("Work out if is black.");
		return histR[0] == screenArea && histG[0] == screenArea && histB[0] == screenArea;
	}
	catch (bad_alloc)
	{
		LOG_ERROR("Failed to allocate space on heap for requisite buffers.");
		return false;
	}
}
/*
bool oldCaptureScreen()
{
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
		screenArea = screenWidth * screenHeight;
	LOG_INFO(L"Screen is " << screenWidth << L"x" << screenHeight << " = " << screenArea << "\n");
	HWND desktopWnd = GetDesktopWindow();
	HDC desktopDc = GetDC(desktopWnd),
		captureDc = CreateCompatibleDC(desktopDc);
	HBITMAP captureBitmap = CreateCompatibleBitmap(desktopDc, screenWidth, screenHeight);
	BITMAP ddScreenshot;
	DWORD screenshotSize = 0, bytesWritten = 0, dibSize = 0;
	SelectObject(captureDc, captureBitmap);

	// Replace the contents of captureDc with those of desktopDc
	BitBlt(
		// Destination device context
		captureDc,
		// Top left of destination
		0, 0,
		// Size of source and destination
		screenWidth, screenHeight,
		// Source device context
		desktopDc,
		// Top left of source
		screenOriginX, screenOriginY,
		// Raster operation to perform.
		// In this case, replace destination with source.
		SRCCOPY);

	GetObject(captureBitmap, sizeof(BITMAP), &ddScreenshot);
	BITMAPFILEHEADER bmpFileHeader;
	BITMAPINFOHEADER bmpInfoHeader;
	bmpInfoHeader.biSize = sizeof(BITMAPINFOHEADER);
	bmpInfoHeader.biWidth = ddScreenshot.bmWidth;
	bmpInfoHeader.biHeight = ddScreenshot.bmHeight;
	bmpInfoHeader.biPlanes = 1;
	bmpInfoHeader.biBitCount = 32;
	bmpInfoHeader.biCompression = BI_RGB;
	bmpInfoHeader.biSizeImage = 0;
	bmpInfoHeader.biXPelsPerMeter = 0;
	bmpInfoHeader.biYPelsPerMeter = 0;
	bmpInfoHeader.biClrUsed = 0;
	bmpInfoHeader.biClrImportant = 0;

	screenshotSize = ((ddScreenshot.bmWidth * bmpInfoHeader.biBitCount + 31) / 32) * 4 * ddScreenshot.bmHeight;
	dibSize = screenshotSize + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);
	bmpFileHeader.bfOffBits = (DWORD)sizeof(BITMAPFILEHEADER) + (DWORD)sizeof(BITMAPINFOHEADER);
	bmpFileHeader.bfSize = dibSize;
	bmpFileHeader.bfType = 0x4D42; // BM

	LPVOID buff = HeapAlloc(GetProcessHeap(), HEAP_GENERATE_EXCEPTIONS, screenshotSize);

	GetDIBits(captureDc, captureBitmap, 0, (UINT)ddScreenshot.bmHeight, buff, (BITMAPINFO *)&bmpInfoHeader, DIB_RGB_COLORS);

	IStream *stream = SHCreateMemStream(NULL, dibSize);

	HANDLE hFile = CreateFile(L"ddScreenshot.bmp", GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);

	WriteFile(hFile, (LPSTR)&bmpFileHeader, sizeof(bmpFileHeader), &bytesWritten, NULL);
	stream->Write((LPSTR)&bmpFileHeader, sizeof(bmpFileHeader), &bytesWritten);
	WriteFile(hFile, (LPSTR)&bmpInfoHeader, sizeof(bmpInfoHeader), &bytesWritten, NULL);
	stream->Write((LPSTR)&bmpInfoHeader, sizeof(bmpInfoHeader), &bytesWritten);
	WriteFile(hFile, (LPSTR)buff, screenshotSize, &bytesWritten, NULL);
	stream->Write((LPSTR)buff, screenshotSize, &bytesWritten);

	CloseHandle(hFile);

	Bitmap image((BITMAPINFO *)&bmpInfoHeader, buff);
	UINT histogramSize;
	Status sStatus = image.GetHistogramSize(HistogramFormatARGB, &histogramSize);
	UINT *histR = new UINT[histogramSize];
	UINT *histG = new UINT[histogramSize];
	UINT *histB = new UINT[histogramSize];

	image.GetHistogram(HistogramFormatRGB, histogramSize, histR, histG, histB, NULL);
	bool isBlack;
	isBlack = (histR[0] == screenArea || histG[0] == screenArea || histB[0] == screenArea);

	HeapFree(GetProcessHeap(), NULL, buff);
	ReleaseDC(desktopWnd, desktopDc);
	DeleteDC(captureDc);
	DeleteObject(captureBitmap);
	return isBlack;
}
*/
