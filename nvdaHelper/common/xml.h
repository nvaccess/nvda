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

inline std::wstring sanitizeXMLAttribName(std::wstring attribName) {
	// #6249: Attribute names can sometimes contain spaces,
	// but this isn't valid in XML, so filter it out.
	std::replace(attribName.begin(), attribName.end(), L' ', L'_');
	return attribName;
}

#endif
