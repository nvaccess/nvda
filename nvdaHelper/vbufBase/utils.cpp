/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2006-2010 NVDA contributers.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#include <cwctype>
#include <string>
#include <map>
#include "utils.h"

using namespace std;

wstring getNameForURL(const wstring &url) {
	if (url.empty())
		// Avoid pointless computation.
		return url;

	wstring::size_type colonPos = url.find(L':');
	if (colonPos != wstring::npos && url.compare(colonPos, 3, L"://") != 0) {
		// This URL specifies a protocol, but it is not a path-based protocol; e.g. it is a javascript: or mailto: URL.
		wstring imgCheck = url.substr(0, 11);
		transform(imgCheck.begin(), imgCheck.end(), imgCheck.begin(), tolower);
		if (imgCheck.compare(0, 11, L"data:image/") == 0)
			return L""; // This URL is not useful.
		// Return the URL as is with the protocol stripped.
		return url.substr(colonPos + 1);
	}

	// The URL either specifies a path-based protocol (e.g. http://)
	// or specifies no protocol, in which case it is assumed to be a path.

	// Find the beginning of the query string.
	wstring::size_type queryStart = url.rfind(L'?');
	// Assume the query string ends at the end of the string.
	wstring::size_type queryLen = wstring::npos;

	// Find the beginning of the target anchor.
	wstring::size_type anchorStart = url.rfind(L'#');
	if (anchorStart != wstring::npos)
		// The query string ends just before the anchor begins.
		queryLen = anchorStart - queryStart - 1;

	wstring::size_type pathStart, pathEnd;
	bool stripExten = true;
	// Find the end of the path.
	if (queryStart != wstring::npos)
		pathEnd = queryStart;
	else if (anchorStart != wstring::npos)
		pathEnd = anchorStart;
	else
		pathEnd = url.length();
	// wstring::npos for pathEnd means no path.
	pathEnd = (pathEnd >= 0) ? (pathEnd - 1) : wstring::npos;

	if (pathEnd != wstring::npos && url[pathEnd] == L'/') {
		// The path ends with a '/', so go back one, as an empty path component is useless.
		pathEnd = (pathEnd >= 0) ? (pathEnd - 1) : wstring::npos;
		// This path component is not a filename, so don't strip the extension.
		stripExten = false;
	}

	if (pathEnd != wstring::npos) {
		// Find the start of this path component.
		pathStart = url.rfind(L'/', pathEnd);
		if (pathStart == wstring::npos) {
			// url is a single path component.
			pathStart = 0;
		} else {
			++pathStart;
			if (stripExten && pathStart == colonPos + 3) {
				// This URL provides a hostname and the hostname is the last path component,
				// so don't strip the extension.
				stripExten = false;
			}
		}

		if (stripExten) {
			// Strip the extension, if any.
			wstring::size_type extenStart = url.rfind(L'.', pathEnd);
			if (extenStart != wstring::npos && extenStart > pathStart)
				pathEnd = extenStart - 1;
		}
	}

	wstring name;
	if (pathEnd != wstring::npos)
		name = url.substr(pathStart, pathEnd - pathStart + 1);
	if (queryStart != wstring::npos)
		name += L' ' + url.substr(queryStart + 1, queryLen);
	if (anchorStart != wstring::npos)
		name += L' ' + url.substr(anchorStart + 1);
	//Finally truncate to 30 chars 
	if(name.length()>30) {
		name=name.substr(0,30)+L'\x2026';
	}
	return name;
}

bool isWhitespace(const wchar_t *str) {
	for (const wchar_t *c = str; *c; ++c) {
		if (!iswspace(*c))
			return false;
	}
	return true;
}

void multiValueAttribsStringToMap(const wstring &attribsString, multiValueAttribsMap &attribsMap) {
	wstring str, key;
	bool inEscape = false;

	for (wstring::const_iterator it = attribsString.begin(); it != attribsString.end(); ++it) {
		if (inEscape) {
			str.push_back(*it);
			inEscape = false;
		} else if (*it == L'\\') {
			inEscape = true;
		} else if (*it == L':') {
			// We're about to move on to the value, so save the key and clear str.
			key = str;
			str.clear();
		} else if (*it == L',' || *it == L';') {
			// We're about to move on to a new attribute or another value for the same attribute.
			// In either case, the current value ends here.
			// Add this key/value pair to the map.
			if (!key.empty()) {
				attribsMap.insert(pair<wstring, wstring>(key, str));
				if (*it == L';') {
					// We're about to move on to a new attribute.
					key.clear();
				}
			}
			str.clear();
		} else {
			str.push_back(*it);
		}
	}
}

bool nodeHasUsefulContent(VBufStorage_fieldNode_t* node) {
	int length = node->getLength();
	if (length == 0)
		return false;
	if (length > 3)
		return true;
	wstring content;
	node->getTextInRange(0, length, content, false);
	for(wstring::iterator i=content.begin();i!=content.end();++i) {
		if(!iswspace(*i)&&!isPrivateCharacter(*i)) {
			return true;
		}
	}
	return false;
}

/*
Used to prevent duplicate content.
*/
bool nodeContentMatchesString(VBufStorage_fieldNode_t* node, const wstring& testStr) {
	const int length = node->getLength();
	if (length != testStr.length()) {
		return false;
	}
	wstring content;
	node->getTextInRange(0, length, content, false);
	return content == testStr;
}
