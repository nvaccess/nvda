#ifndef NVDAHELPER_XML_H
#define NVDAHELPER_XML_H

#include <string>

inline void appendCharToXML(const wchar_t c, std::wstring& xml) {
	switch(c) {
		case L'"':
		xml+=L"&quot;";
		break;
		case L'<':
		xml+=L"&lt;";
		break;
		case L'>':
		xml+=L"&gt;";
		break;
		case L'&':
		xml+=L"&amp;";
		break;
		default:
		if (c == 0x9 || c == 0xA || c == 0xD
			|| (c >= 0x20 && c <= 0xD7FF) || (c >= 0xE000 && c <= 0xFFFD)
		) {
			// Valid XML character.
			xml+=c;
		} else {
			// Invalid XML character.
			xml += 0xfffd; // Unicode replacement character
		}
	}
}

#endif
