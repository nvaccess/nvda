// WinEventLogger.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include "pch.h"
#include <iostream>
#include <string>
#include <iostream>
#include <ostream>
#include <future>
#include <thread>
#include <chrono>

#include <eventHandlerDll.h>
#include <Windows.h>

HWND doCreateWindow();
void blocking_messagePump();

std::atomic<bool> g_keepPrinting = true;
std::atomic<bool> g_glitch = false;
void printFromBuffer();


void onNewEvent() {
	// Callback from event handler
}

struct EventData;
void onDestroyedEvent(EventData*) {
	// Callback from event handler
}

int main() {
	std::cout << "Starting\n";
	RegisterAndPump_Async( onNewEvent, onDestroyedEvent );
	auto printThread = std::thread(printFromBuffer);
	doCreateWindow();
	blocking_messagePump();
	g_keepPrinting = false; // stops the print thread.
	RegisterAndPump_Join(); 
	printThread.join();
	exit(0);
}

void printFromBuffer() {
	while (g_keepPrinting) {
		std::cout << "-- flush --" << '\n';
		FlushEvents();
		if (g_glitch.exchange(false)) {
			auto numEvents = GetEventCount();
			std::cout << "Glitch Event: ";
			PrintEvent(numEvents+1);
		}
		else {
			auto numEvents = GetEventCount();
			for (auto i = 0u; i < numEvents; ++i) {
				PrintEvent(i);
			}
		}

		using namespace std::chrono_literals;
		std::this_thread::sleep_for(100ms); // mimic cadence of updates from NVDA
	}
}

LRESULT CALLBACK WndProc(HWND hwnd, UINT message, WPARAM wparam, LPARAM lparam) {
	switch (message) {
	case WM_CHAR:
		if (wparam == VK_ESCAPE) {
			DestroyWindow(hwnd);
		}
		if (wparam == 'g') {
			g_glitch = true;
		}
		break;
	case WM_DESTROY:
		DestroyWindow(hwnd);
		PostQuitMessage(0);
		break;
	}
	return DefWindowProc(hwnd, message, wparam, lparam);
}

HWND doCreateWindow() {
	WNDCLASS windowClass = { 0 };
	windowClass.hbrBackground = static_cast<HBRUSH>(GetStockObject(WHITE_BRUSH));
	windowClass.hCursor = LoadCursor(nullptr, IDC_ARROW);
	windowClass.hInstance = nullptr;
	windowClass.lpfnWndProc = WndProc;
	windowClass.lpszClassName = L"Window in Console"; //needs to be the same name when creating the window as well
	windowClass.style = CS_HREDRAW | CS_VREDRAW;
	//also register the class
	if (!RegisterClass(&windowClass)) {
		std::cout << "Could not register class\n";
		exit(-1);
	}

	HWND windowHandle = CreateWindow(
		L"Window in Console", // lpClassName
		nullptr, // lpWindowName
		WS_OVERLAPPEDWINDOW, // dwStyle
		// coordinate of window start point
		0, // x
		0, // y
		// window size
		500, // width
		100, // height
		nullptr, // hWndParent
		nullptr, // hMenu
		nullptr, // hInstance
		nullptr // lpParam
	);
	ShowWindow(windowHandle, SW_RESTORE);
	return windowHandle;
}

void blocking_messagePump() {
	// Keep this app running until we're told to stop
	MSG msg;
	while (0 < GetMessage(&msg, NULL, NULL, NULL)
		) {
		TranslateMessage(&msg);
		DispatchMessage(&msg);
	}
}