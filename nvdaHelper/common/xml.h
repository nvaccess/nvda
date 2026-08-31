#ifndef NVDAHELPER_XML_H
#define NVDAHELPER_XML_H

#include <string>
#include <sstream>
#include <algorithm>

inline void appendCharToXML(const wchar_t c, std::wstring& xml, bool isAttribute=false) {
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
			if (isAttribute)
				xml += 0xfffd; // Unicode replacement character
			else {
				std::wostringstream s;
				s<<L"<unich value=\""<<((unsigned short)c)<<L"\" />";
				xml += s.str();
			}
		}
	}
}

inline bool isValidXMLNameStartChar(const wchar_t c) {
	return (c >= L'a' && c <= L'z')
		|| (c >= L'A' && c <= L'Z')
		|| c == L':' || c == L'_';
}

inline bool isValidXMLNameChar(const wchar_t c) {
	return isValidXMLNameStartChar(c)
		|| (c >= L'0' && c <= L'9')
		|| c == L'-' || c == L'.';
}

inline bool isValidXMLAttribName(const std::wstring& attribName) {
	// Use a conservative subset of XML names accepted by the expat parser NVDA uses.
	// All attribute names NVDA consumes are ASCII.
	if (attribName.empty() || !isValidXMLNameStartChar(attribName.front())) {
		return false;
	}
	return std::all_of(
		attribName.cbegin() + 1,
		attribName.cend(),
		isValidXMLNameChar
	);
}

#endif
