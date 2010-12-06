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

#ifndef _VBUF_IA2UTILS_H
#define _VBUF_IA2UTILS_H

#include <string>
#include <map>

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

#endif
