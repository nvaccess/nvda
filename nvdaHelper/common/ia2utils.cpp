/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2007-2017 NV Access Limited, Mozilla Corporation
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

using namespace std;

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
}

IAccessibleHyperlinkPtr HyperlinkGetter::next() {
	return this->get(this->index++);
}

HtHyperlinkGetter::HtHyperlinkGetter(IAccessibleHypertextPtr hypertext)
	: hypertext(hypertext)
{
}

IAccessibleHyperlinkPtr HtHyperlinkGetter::get(const unsigned long index) {
	IAccessibleHyperlinkPtr link;
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

Ht2HyperlinkGetter::Ht2HyperlinkGetter(IAccessibleHypertext2Ptr hypertext)
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

IAccessibleHyperlinkPtr Ht2HyperlinkGetter::get(const unsigned long index) {
	this->maybeFetch();
	if ((long)index >= this->count) {
		return nullptr;
	}
	// Ensure we don't AddRef this pointer.
	return IAccessibleHyperlinkPtr(this->rawLinks[index], false);
}

Ht2HyperlinkGetter::~Ht2HyperlinkGetter() {
	if (this->rawLinks) {
		CoTaskMemFree(this->rawLinks);
	}
}

// We use a unique_ptr so we can have a polymorphic, optional return.
unique_ptr<HyperlinkGetter> makeHyperlinkGetter(IAccessible2* acc) {
	// Try IAccessibleHypertext2 first.
	IAccessibleHypertext2Ptr ht2 = acc;
	if (ht2) {
		return make_unique<Ht2HyperlinkGetter>(move(ht2));
	}
	// Fall back to IAccessibleHypertext.
	IAccessibleHypertextPtr ht = acc;
	if (ht) {
		return make_unique<HtHyperlinkGetter>(move(ht));
	}
	// Neither interface is supported.
	return nullptr;
}
