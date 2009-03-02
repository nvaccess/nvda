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
