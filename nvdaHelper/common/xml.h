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

inline bool isValidXMLNameChar(const wchar_t c) {
	// A conservative subset of the XML NameChar production: expat as shipped with
	// Python enforces the stricter XML 1.0 fourth edition name rules, so anything
	// broader risks emitting names it rejects. All attribute names NVDA consumes
	// are ASCII, so nothing meaningful is lost by replacing the rest.
	return (c >= L'a' && c <= L'z')
		|| (c >= L'A' && c <= L'Z')
		|| (c >= L'0' && c <= L'9')
		|| c == L'-' || c == L'.' || c == L':' || c == L'_';
}

inline std::wstring sanitizeXMLAttribName(std::wstring attribName) {
	// #6249, #7173: Attribute names sourced from browsers can contain characters
	// which aren't valid in XML names; e.g. spaces from localised Chrome action names
	// or quotes from malformed HTML such as aria-label"foo".
	// Replace them so the generated XML stays well-formed.
	std::replace_if(
		attribName.begin(), attribName.end(),
		[](wchar_t c) { return !isValidXMLNameChar(c); },
		L'_'
	);
	// XML names must not be empty or start with a digit, hyphen or period
	// (NameStartChar is stricter than NameChar).
	if (attribName.empty() || !(
		(attribName[0] >= L'a' && attribName[0] <= L'z')
		|| (attribName[0] >= L'A' && attribName[0] <= L'Z')
		|| attribName[0] == L'_' || attribName[0] == L':'
	)) {
		attribName.insert(0, 1, L'_');
	}
	return attribName;
}

#endif
