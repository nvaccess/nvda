#include <string>
#include <map>

using namespace std;

void IA2AttribsToMap(const wstring &attribsString, map<wstring, wstring> &attribsMap) {
	wstring str, key;
	bool inEscape = false;

	for (wstring::const_iterator it = attribsString.begin(); it != attribsString.end(); it++) {
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
