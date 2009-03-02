/**
 * base/utils.h
 * Part of the NV  Virtual Buffer Library
 * This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
 * This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
 * http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
 */

#ifndef _VBUF_UTILS_H
#define _VBUF_UTILS_H

#include <string>
#include <wchar.h>
#include <map>
#include <base/libEntry.h>

/**
 * Obtain a user friendly name for a URL if possible.
 * This is done as follows:
 * For a URL which is not path-based (e.g. javascript), return the URL with the protocol (the portion before the colon) stripped.
 * For a path-based URL (e.g. http) or a URL with no protocol (which is assumed to be a path), modify the URL as follows:
 *  * Start with the last path component which is not empty.
 *  * If this is not the hostname and there is no trailing slash, which means we're probably dealing with a filename, strip the extension; i.e. everything after the last "." character.
 *  * Append the query string and the anchor target, if any, with the "#" and "?" characters replaced with spaces.
 * @param url: The URL.
 * @return: The user friendly name for the URL.
 */
std::wstring getNameForURL(const std::wstring &url);

/**
 * Determine whether a string of text is whitespace.
 * @param str: The string in question.
 * @precondition: @c str is not @c NULL.
 * @return: @c true if @c str is whitespace, @c false otherwise.
 */
bool isWhitespace(const wchar_t *str);

typedef std::multimap<std::wstring, std::wstring> multiValueAttribsMap;

/**
 * Convert a multi-value attributes string to a multimap of attribute keys and values.
 * A multi-value attributes string is of the form "name:value;name:value1,value2;...;"
 * Colons, commas and semi-colons must be escaped with a backslash character.
 * An invalid attributes string does not cause an error, but strange results may be returned.
 * @param attribsString: The attributes string to convert.
 * @param attribsMap: The multiValueAttribsMap into which the attributes should be placed, with keys and values as strings.
 */
void multiValueAttribsStringToMap(const std::wstring &attribsString, multiValueAttribsMap &attribsMap);

#endif
