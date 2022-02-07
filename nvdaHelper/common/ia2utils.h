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

#ifndef _VBUF_IA2UTILS_H
#define _VBUF_IA2UTILS_H

#include <atlcomcli.h>
#include <string>
#include <map>
#include <vector>
#include <utility>
#include <memory>
#include <ia2.h>

bool fetchIA2Attributes(IAccessible2* pacc2, std::map<std::wstring, std::wstring>& attribsMap);

/**
 * Convert an IAccessible2 attributes string to a map of attribute keys and values.
 * An IAccessible2 attributes string is of the form "name:value;name:value;...;"
 * Colons and semi-colons must be escaped with a backslash character.
 * An invalid attributes string does not cause an error, but strange results may be returned.
 * @note: Sub-attributes are currently not handled in any special way.
 * @param attribsString: The IAccessible2 attributes string to convert.
 * @param attribsMap: The map into which the attributes should be placed, with keys and values as strings.
 */
void IA2AttribsToMap(const std::wstring &attribsString, std::map<std::wstring, std::wstring> &attribsMap);

/**
* Helper to collect the children for an IAccessible, uses memory managed types that will clear / delete automatically.
*/
std::pair<std::vector<CComVariant>, HRESULT>
getAccessibleChildren(IAccessible* pacc, long indexOfFirstChild, long maxChildCount);

/**
 * Base class to support retrieving hyperlinks (embedded objects) from
 * IAccessibleHypertext or IAccessibleHypertext2.
 * Callers should use the makeHyperlinkGetter factory function,
 * rather than instantiating subclasses directly.
 */
class HyperlinkGetter {
	public:
	virtual ~HyperlinkGetter() {}

	/** Get the next hyperlink.
	 */
	virtual CComPtr<IAccessibleHyperlink> next();

	protected:
	long index = 0;
	virtual CComPtr<IAccessibleHyperlink> get(const unsigned long index) = 0;
};

/** Supports retrieval of hyperlinks from IAccessibleHypertext.
 */
class HtHyperlinkGetter: public HyperlinkGetter {
	public:
	HtHyperlinkGetter(CComPtr<IAccessibleHypertext> hypertext);

	protected:
	virtual CComPtr<IAccessibleHyperlink> get(const unsigned long index) override;

	private:
	CComPtr<IAccessibleHypertext> hypertext;
};

/** Supports retrieval of hyperlinks from IAccessibleHypertext2.
 */
class Ht2HyperlinkGetter: public HyperlinkGetter {
	public:
	Ht2HyperlinkGetter(CComPtr<IAccessibleHypertext2> hypertext);
	virtual ~Ht2HyperlinkGetter();

	protected:
	virtual CComPtr<IAccessibleHyperlink> get(const unsigned long index) override;

	private:
	CComPtr<IAccessibleHypertext2> hypertext;
	IAccessibleHyperlink** rawLinks = nullptr;
	long count;
	void maybeFetch();
};

/**
 * Create an appropriate HyperlinkGetter to retrieve hyperlinks
 * (embedded objects) if they are supported.
 * IAccessibleHypertext2 will be used in preference to IAccessibleHypertext.
 * @param acc The accessible to use.
 * @return A pointer to the HyperlinkGetter
 *  or a null pointer if hyperlinks aren't supported.
 */
std::unique_ptr<HyperlinkGetter> makeHyperlinkGetter(IAccessible2* acc);

#endif
