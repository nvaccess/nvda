/*
This file is a part of the NVDA project.
Copyright 2018 NV Access Limited.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#pragma once

#include <windows.h>

// A Smart Library handle.
// Construct it with a handle returned by LoadLibrary or similar.
// Once the object goes out of scope, FreeLibrary will automatically be called on the handle. 
class CLoadedLibrary {
	private:
	HMODULE _hModule {nullptr};
	CLoadedLibrary(const CLoadedLibrary&)=delete;
	const CLoadedLibrary& operator=(const CLoadedLibrary&)=delete;

	public:

	CLoadedLibrary(HMODULE h): _hModule(h) {};

	void free() {
		if(_hModule) {
			FreeLibrary(_hModule);
			_hModule=nullptr;
		}
	}

	CLoadedLibrary& operator=(HMODULE h) {
		free();
		_hModule=h;
		return *this;
	}

	operator HMODULE() {
		return _hModule;
	}

	operator bool() {
		return static_cast<bool>(_hModule);
	}

	~CLoadedLibrary() {
		free();
	}

};

