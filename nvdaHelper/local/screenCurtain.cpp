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
#pragma comment (lib,"Gdiplus.lib")


bool captureScreen() {
	// Bitmap *image;
	// Status s;
	// UINT histSize;
	// UINT* histR = new UINT[300];
	// UINT* histG = new UINT[300];
	// UINT  *histB = new UINT[300];
	// A false negative is better than a false positive,
	// So return false until proven otherwise.
	bool returnValue = false, success;
	// The virtual screen is the bounding rectangle of all of the monitors on the system.
	int screenWidth = GetSystemMetrics(SM_CXVIRTUALSCREEN),
		screenHeight = GetSystemMetrics(SM_CYVIRTUALSCREEN),
		// While the primary monitor's top left corner is at the origin,
		// it is not necessarily at the top left of the virtual screen.
		// Thus, the top left of the virtual screen may be negative.
		screenOriginX = GetSystemMetrics(SM_XVIRTUALSCREEN),
		screenOriginY = GetSystemMetrics(SM_YVIRTUALSCREEN),
		// Screen coordinates are 16-bit integers,
		// and since 2^16 * 2^16 = 2^32,
		// the area of the screen is guaranteed to fit in an int on all supported platforms.
		screenSize = screenWidth * screenHeight,
		bytesWritten;
	DWORD screenshotSize;
	HWND desktopWnd;
	// HBITMAP captureBitmap;
	BITMAP screenshot;
	HGDIOBJ oldObj;
	BITMAPINFOHEADER bmpInfoHeader;
	// LPVOID buff ;

	LOG_INFO(L"Get desktop window");
	desktopWnd = GetDesktopWindow();
	if (desktopWnd == NULL) {
		LOG_ERROR(L"Failed to get handle for desktop window.");
		return false;
	}
	LOG_INFO(L"Get desktop device context.");
	wil::unique_hdc_window desktopDc(GetDC(desktopWnd));
	if (!desktopDc.is_valid()) {
		LOG_ERROR(L"Failed to get device context for desktop.");
		return false;
	}
	LOG_INFO(L"Get compatible DC.");
	wil::unique_hdc captureDc(CreateCompatibleDC(desktopDc.get()));
	if (!captureDc .is_valid()) {
		LOG_ERROR("Failed to create compatible device context.");
		return false;
	}

	LOG_INFO("Getting compatible bitmap.");
	wil::unique_hbitmap captureBitmap(CreateCompatibleBitmap(desktopDc.get(), screenWidth, screenHeight));
	if (captureBitmap == NULL) {
		LOG_ERROR(L"Failed to create compatible bitmap.");
		return false;
	}

	LOG_INFO(L"Setting captureDC to paint to captureBitmap.");
	// Set captureDc to draw to captureBitmap.
	oldObj = SelectObject(captureDc.get(), captureBitmap.get());
	if (oldObj == NULL) {
		LOG_ERROR("Failed to select capture bitmap into capture device context.");
		return false;
	}

	LOG_INFO(L"Bit blitting.");
	// Replace the contents of captureDc with those of desktopDc
	success = BitBlt(
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
	if (!success) {
		LOG_ERROR("Failed to bit blit desktop device context to capture device context. Error #" << GetLastError());
		return false;
	}

	LOG_INFO(L"Getting DDB properties.");
	// Get properties of captureBitmap
	bytesWritten = GetObject(captureBitmap.get(), sizeof(BITMAP), &screenshot);
	if (bytesWritten == 0) {
		LOG_ERROR("Failed to get bitmap metadata.");
		// goto done;
	}

	LOG_INFO(L"Setting DIB props.");
	bmpInfoHeader.biSize = sizeof(BITMAPINFOHEADER);
	bmpInfoHeader.biWidth = screenshot.bmWidth;
	bmpInfoHeader.biHeight = screenshot.bmHeight;
	bmpInfoHeader.biPlanes = 1;  // Can only ever be 1
	bmpInfoHeader.biBitCount = 32;  // High byte unused
	bmpInfoHeader.biCompression = BI_RGB;  // Uncompressed
	bmpInfoHeader.biSizeImage = 0;  // Unneeded as uncompressed
	bmpInfoHeader.biXPelsPerMeter = 0;
	bmpInfoHeader.biYPelsPerMeter = 0;
	bmpInfoHeader.biClrUsed = 0;
	bmpInfoHeader.biClrImportant = 0;  // All colours are needed

	LOG_INFO("Calculating DIB size.");
	screenshotSize = ((screenshot.bmWidth * bmpInfoHeader.biBitCount + 31) / 32) * 4 * screenshot.bmHeight;

	// Convert the device-dependent bitmap to a device-independent bitmap.
	// try {
		LOG_INFO("Allocating size for DIB.");
		auto buff = std::make_shared<char[]>(screenshotSize);
	// } catch (bad_alloc) {
		// LOG_ERROR("Failed to allocate space on heap for device independent bitmap.");
		// return false;
	// }
	LOG_INFO(L"Getting DIB.");
	bytesWritten = GetDIBits(
		// Source device context and device-dependent bitmap
		captureDc.get(), captureBitmap.get(),
		// Range of scan lines to copy
		0, (UINT)screenshot.bmHeight,
		// Destination buffer
		buff.get(),
		// Format of DIB
		(BITMAPINFO*)&bmpInfoHeader, DIB_RGB_COLORS
	);
	if (bytesWritten == 0 || bytesWritten == ERROR_INVALID_PARAMETER) {
		LOG_ERROR(L"Failed to convert device dependent bitmap to device independent bitmap. Return " << bytesWritten);
		return false;
	}

	// Create a GDI+ bitmap from the captured virtual screen, and calculate a histogram of colours.
	LOG_INFO(L"Create GDIPLUS bmp.");
	// Bitmap image((BITMAPINFO*)&bmpInfoHeader, buff.get());
	auto image = make_shared<Bitmap>((BITMAPINFO*)&bmpInfoHeader, buff.get());
	UINT hsize;
	LOG_INFO("Calculate hist size.");
	Status s = image->GetHistogramSize(HistogramFormatARGB, &hsize);

	LOG_INFO("Allocate size for histogram.");
	auto histR = std::make_shared<UINT[]>(hsize);
	auto histG = std::make_shared<UINT[]>(hsize);
	auto histB = std::make_shared<UINT[]>(hsize);

	LOG_INFO(L"Get histogram.");
	image->GetHistogram(HistogramFormatRGB, hsize, histR.get(), histG.get(), histB.get(), NULL);

	// If the entire screen is black, then the only colour in the histogram must be (0, 0, 0).
	// Since the sum of values in each channel must be the number of pixels in the image,
	// if the screen is entirely black,
	// the 0th entry in each of the channels must be the number of pixels in the image.
	LOG_INFO("Work out if is black.");
	returnValue = (histR[0] == screenSize && histG[0] == screenSize && histB[0] == screenSize);

// done:
	LOG_INFO("Clean up.");
	// HeapFree(GetProcessHeap(), NULL, buff);
	// if (desktopWnd != NULL) {
		// if (desktopDc != NULL)
			// ReleaseDC(desktopWnd, desktopDc);
		// CloseHandle(desktopWnd);
	// }
	// if (captureDc != NULL) {

	// }
	// if (captureBitmap != NULL) DeleteObject(captureBitmap.get());

	return returnValue;
}

bool oldCaptureScreen()
{
	// The virtual screen is the bounding rectangle of all of the monitors on the system.
	int screenWidth = GetSystemMetrics(SM_CXVIRTUALSCREEN),
		screenHeight = GetSystemMetrics(SM_CYVIRTUALSCREEN),
		// While the primary monitor's top left corner is at the origin,
		// it is not necessarily at the top left of the virtual screen.
		// Thus, the top left of the virtual screen may be negative.
		screenOriginX = GetSystemMetrics(SM_XVIRTUALSCREEN),
		screenOriginY = GetSystemMetrics(SM_YVIRTUALSCREEN),
		// Screen coordinates are 16-bit integers,
		// and since 2^16 * 2^16 = 2^32,
		// the area of the screen is guaranteed to fit in an int on all supported platforms.
		screenSize = screenWidth * screenHeight;
	LOG_INFO(L"Screen is " << screenWidth << L"x" << screenHeight << " = " << screenSize << "\n");
	HWND desktopWnd = GetDesktopWindow();
	HDC desktopDc = GetDC(desktopWnd),
		captureDc = CreateCompatibleDC(desktopDc);
	HBITMAP captureBitmap = CreateCompatibleBitmap(desktopDc, screenWidth, screenHeight);
	BITMAP screenshot;
	DWORD screenshotSize=0, bytesWritten=0, dibSize=0;
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
		SRCCOPY
	);

	GetObject(captureBitmap, sizeof(BITMAP), &screenshot);
	BITMAPFILEHEADER bmpFileHeader;
	BITMAPINFOHEADER bmpInfoHeader;
	bmpInfoHeader.biSize = sizeof(BITMAPINFOHEADER);
	bmpInfoHeader.biWidth = screenshot.bmWidth;
	bmpInfoHeader.biHeight = screenshot.bmHeight;
	bmpInfoHeader.biPlanes = 1;
	bmpInfoHeader.biBitCount = 32;
	bmpInfoHeader.biCompression = BI_RGB;
	bmpInfoHeader.biSizeImage = 0;
	bmpInfoHeader.biXPelsPerMeter = 0;
	bmpInfoHeader.biYPelsPerMeter = 0;
	bmpInfoHeader.biClrUsed = 0;
	bmpInfoHeader.biClrImportant = 0;

	screenshotSize = ((screenshot.bmWidth * bmpInfoHeader.biBitCount + 31) / 32) * 4 * screenshot.bmHeight;
	dibSize = screenshotSize + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);
	bmpFileHeader.bfOffBits = (DWORD)sizeof(BITMAPFILEHEADER) + (DWORD)sizeof(BITMAPINFOHEADER);
	bmpFileHeader.bfSize = dibSize;
	bmpFileHeader.bfType = 0x4D42;  // BM

	LPVOID buff = HeapAlloc(GetProcessHeap(), HEAP_GENERATE_EXCEPTIONS, screenshotSize);

	GetDIBits(captureDc, captureBitmap, 0, (UINT)screenshot.bmHeight, buff, (BITMAPINFO*)&bmpInfoHeader, DIB_RGB_COLORS);

	IStream *stream = SHCreateMemStream(NULL, dibSize);

	HANDLE hFile = CreateFile(L"screenshot.bmp", GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);

	WriteFile(hFile, (LPSTR)&bmpFileHeader, sizeof(bmpFileHeader), &bytesWritten, NULL);
	stream->Write((LPSTR)&bmpFileHeader, sizeof(bmpFileHeader), &bytesWritten);
	WriteFile(hFile, (LPSTR)&bmpInfoHeader, sizeof(bmpInfoHeader), &bytesWritten, NULL);
	stream->Write((LPSTR)&bmpInfoHeader, sizeof(bmpInfoHeader), &bytesWritten);
	WriteFile(hFile, (LPSTR)buff, screenshotSize, &bytesWritten, NULL);
	stream->Write((LPSTR)buff, screenshotSize, &bytesWritten);

	CloseHandle(hFile);

	Bitmap image((BITMAPINFO*)&bmpInfoHeader, buff);
	UINT hsize;
	Status s = image.GetHistogramSize(HistogramFormatARGB, &hsize);
	UINT* histR = new UINT[hsize];
	UINT* histG = new UINT[hsize];
	UINT* histB = new UINT[hsize];

	image.GetHistogram(HistogramFormatRGB, hsize, histR, histG, histB, NULL);
	bool isBlack;
	isBlack = (histR[0] == screenSize || histG[0] == screenSize || histB[0] == screenSize);

	HeapFree(GetProcessHeap(), NULL, buff);
	ReleaseDC(desktopWnd, desktopDc);
	DeleteDC(captureDc);
	DeleteObject(captureBitmap);
	return isBlack;
}
