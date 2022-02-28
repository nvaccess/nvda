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

// Converts a utf8 encoded string into a utf16 encoded wstring
std::wstring stringToWstring(const std::string& from) {
	int wideLen = MultiByteToWideChar(CP_UTF8, 0, from.c_str(), from.length(), nullptr, 0);
	std::wstring wideBuf (wideLen, L'\0');
	MultiByteToWideChar(CP_UTF8, 0, from.c_str(), from.length(), wideBuf.data(), wideLen);
	return wideBuf;
}

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
			auto wideWhat = stringToWstring(e.what());
			messageBlock += L"dumpLog exception: ";
			messageBlock += wideWhat;
			messageBlock += L"\n";
		}
		messageBlock+=L"Dump log end";
		LOG_DEBUG(messageBlock);
	}

	private:
	UiaArray<UiaString> _log;

};
