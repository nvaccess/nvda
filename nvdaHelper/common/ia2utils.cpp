/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2007-2021 NV Access Limited, Mozilla Corporation
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#include <string>
#include <map>
#include "ia2utils.h"
#include <ia2.h>

using namespace std;

bool fetchIA2Attributes(IAccessible2* pacc2, map<wstring, wstring>& attribsMap) {
	BSTR attribs = NULL;
	pacc2->get_attributes(&attribs);
	if (!attribs) {
		return false;
	}
	IA2AttribsToMap(attribs, attribsMap);
	SysFreeString(attribs);
	return true;
}

void IA2AttribsToMap(const wstring &attribsString, map<wstring, wstring> &attribsMap) {
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
		} else if (*it == L';') {
			// We're about to move on to a new attribute.
			// Add this key/value pair to the map.
			if (!key.empty())
				attribsMap[key] = str;
				key.clear();
			str.clear();
		} else {
			str.push_back(*it);
		}
	}
	// If there was no trailing semi-colon, we need to handle the last attribute.
	if (!key.empty())
		attribsMap[key] = str;
	// Truncate the value of "src" if it contains base64 data
	map<wstring,wstring>::const_iterator attribsMapIt;
	if ((attribsMapIt = attribsMap.find(L"src")) != attribsMap.end()) {
		str = attribsMapIt->second;
		const wstring prefix = L"data:";
		if (str.substr(0, prefix.length()) == prefix) {
			const wstring needle = L"base64,";
			wstring::size_type pos = str.find(needle);
			if (pos != wstring::npos) {
				str.replace(pos + needle.length(), wstring::npos, L"<truncated>");
				attribsMap[L"src"] = str;
			}
		}
	}
}

std::pair<std::vector<CComVariant>, HRESULT>
getAccessibleChildren(IAccessible* pacc, long indexOfFirstChild, long maxChildCount) {
	try {
		std::vector<CComVariant> varChildren(maxChildCount);
		const auto res = AccessibleChildren(
			pacc,
			indexOfFirstChild,
			maxChildCount,
			varChildren.data(),
			&maxChildCount
		);
		if (res != S_OK) {
			return std::make_pair(
				std::vector<CComVariant>(0),
				res
			);
		}
		// shrink the vector in case less children were returned.
		// so that varChildren.size() will equal actual filled size
		varChildren.resize(maxChildCount);
		// no need to shrink to fit, make_pair will copy the vector, using only the first varChildren.size() elements.
		return std::make_pair(varChildren, S_OK);
	}
	catch (std::bad_array_new_length&) {
		return std::make_pair(
			std::vector<CComVariant>(0),
			S_FALSE
		);
	}
}

CComPtr<IAccessibleHyperlink> HyperlinkGetter::next() {
	return this->get(this->index++);
}

HtHyperlinkGetter::HtHyperlinkGetter(CComPtr<IAccessibleHypertext> hypertext)
	: hypertext(hypertext)
{
}

CComPtr<IAccessibleHyperlink> HtHyperlinkGetter::get(const unsigned long index) {
	CComPtr<IAccessibleHyperlink> link;
	// hyperlink will fail or return null if the index is too big. The caller
	// is probably only calling us when it encounters an embedded object
	// character anyway.
	// Thus, we don't need to call nHyperlinks.
	HRESULT res = this->hypertext->get_hyperlink(index, &link);
	if (FAILED(res) || !link) {
		return nullptr;
	}
	return link;
}

Ht2HyperlinkGetter::Ht2HyperlinkGetter(CComPtr<IAccessibleHypertext2> hypertext)
	: hypertext(hypertext), count(-1)
{
	// count -1 means hyperlinks haven't been fetched yet.
	// See maybeFetch().
}

void Ht2HyperlinkGetter::maybeFetch() {
	// We lazily fetch hyperlinks the first time get() is called.
	// This avoids a pointless COM call in the case where there are no hyperlinks,
	// since the caller probably only calls when it encounters an
	// embedded object character.
	if (this->count >= 0) {
		// Already fetched.
		return;
	}
	if (FAILED(hypertext->get_hyperlinks(&this->rawLinks, &this->count))) {
		this->count = 0;
	}
}

CComPtr<IAccessibleHyperlink> Ht2HyperlinkGetter::get(const unsigned long index) {
	this->maybeFetch();
	if ((long)index >= this->count) {
		return nullptr;
	}
	// Ensure we don't AddRef this pointer.
	CComPtr<IAccessibleHyperlink> link;
	link.Attach(this->rawLinks[index]);
	return link;
}

Ht2HyperlinkGetter::~Ht2HyperlinkGetter() {
	if (this->rawLinks) {
		CoTaskMemFree(this->rawLinks);
	}
}

// We use a unique_ptr so we can have a polymorphic, optional return.
unique_ptr<HyperlinkGetter> makeHyperlinkGetter(IAccessible2* acc) {
	// Try IAccessibleHypertext2 first.
	CComQIPtr<IAccessibleHypertext2> ht2 = acc;
	if (ht2) {
		return make_unique<Ht2HyperlinkGetter>(ht2);
	}
	// Fall back to IAccessibleHypertext.
	CComQIPtr<IAccessibleHypertext> ht = acc;
	if (ht) {
		return make_unique<HtHyperlinkGetter>(ht);
	}
	// Neither interface is supported.
	return nullptr;
}
