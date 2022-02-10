/*
This file is a part of the NVDA project.
URL: http://www.nvaccess.org/
Copyright 2021-2022 NV Access Limited
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

const std::wstring endl{L"\n"};

class RemoteableLogger;

// A class for logging messages from within a remote ops call.
// Push messages to the object with << just like an ostream.
// Currently standard strings, UiaStrings, and UiaInt instances are supported.
// After remote execution is complete, call dumpLog to write the content to our standard logging framework. 
class RemoteableLogger {
	public:

	RemoteableLogger(UiaOperationScope& scope): _log{} {
		scope.BindResult(_log);
	}

	RemoteableLogger& operator <<(UiaInt& message) {
		_log.Append(message.Stringify());
		return *this;
	}

	RemoteableLogger& operator <<(UiaString& message) {
		_log.Append(message);
		return *this;
	}

	RemoteableLogger& operator <<(const std::wstring message) {
		_log.Append(message);
		return *this;
	}

	void dumpLog() {
		assert(!UiaOperationAbstraction::ShouldUseRemoteApi());
		std::wstring messageBlock{L"Dump log start:\n"};
		try {
			// locally, a UiaArray is a shared_ptr to a vector of will_shared_bstr 
			const std::vector<wil::shared_bstr>& v = *_log;
			for(const auto& message: v) {
				messageBlock+=message.get();
			}
		} catch (std::exception& e) {
			const std::string what{e.what()};
			// convert exception message to unicode
			int wideLen = MultiByteToWideChar(CP_UTF8, 0, what.c_str(), what.length(), nullptr, 0);
			auto wideBuf = std::make_unique<wchar_t[]>(wideLen);
			MultiByteToWideChar(CP_UTF8, 0, what.c_str(), what.length(), wideBuf.get(), wideLen);
			messageBlock += L"dumpLog exception: ";
			messageBlock += wideBuf.get();
			messageBlock += L"\n";
		}
		messageBlock+=L"Dump log end";
		LOG_DEBUG(messageBlock);
	}

	private:
	UiaArray<UiaString> _log;

};
