#define GDIPVER 0x110
#include <shlwapi.h>
#include <windows.h>
#include <common/log.h>
#include <objidl.h>
// #include<gdiplusheaders.h>
#include <gdiplus.h>
// #include <gdiplustypes.h>
// #include <gdiplus.h>
using namespace Gdiplus;
#pragma comment (lib,"Gdiplus.lib")

bool captureScreen()
{
	int screenWidth = GetSystemMetrics(SM_CXSCREEN),
		screenHeight = GetSystemMetrics(SM_CYSCREEN);
	HWND desktopWnd = GetDesktopWindow();
	HDC desktopDc = GetDC(desktopWnd),
		captureDc = CreateCompatibleDC(desktopDc);
	HBITMAP captureBitmap = CreateCompatibleBitmap(desktopDc, screenWidth, screenHeight);
	BITMAP screenshot;
	DWORD screenshotSize=0, bytesWritten=0, dibSize=0;
	SelectObject(captureDc, captureBitmap);
	bool isBlack = true;

	BitBlt(captureDc, 0, 0, screenWidth, screenHeight, desktopDc, 0, 0, SRCCOPY);

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
	UINT* ch0 = new UINT[hsize];
	UINT* ch1 = new UINT[hsize];
	UINT* ch2 = new UINT[hsize];

	image.GetHistogram(HistogramFormatRGB, hsize, ch0, ch1, ch2, NULL);

// Print the histogram values for the three channels: red, green, blue.
for(UINT j = 1; j < hsize; ++j)
{
// check all channels' values
}



	HeapFree(GetProcessHeap(), NULL, buff);
	ReleaseDC(desktopWnd, desktopDc);
	DeleteDC(captureDc);
	DeleteObject(captureBitmap);
	return isBlack;
}
