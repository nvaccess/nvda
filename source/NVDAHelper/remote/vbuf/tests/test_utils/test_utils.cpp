/**
 * tests/test_utils/test_utils.cpp
 * Part of the NV  Virtual Buffer Library
 * This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
 * This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
 * http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
 */

#include <iostream>
#include <base/utils.h>

using namespace std;

int failCount=0;

#define test(expr, msg, input, output) if (!(expr)) { wcerr << L"fail: " << msg << L": " << input << L" -> " << output << endl; failCount++;}
#define testNoIO(expr, msg) if (!(expr)) { wcerr << L"fail: " << msg << endl; failCount++;}

void test_getNameForURL() {
	wstring s, n;
	n = getNameForURL(s);
	test(n.empty(), L"empty", s, n);

	s = L"javascript:foo";
	n = getNameForURL(s);
	test(n == L"foo", L"javascript", s, n);

	s = L"http://www";
	n = getNameForURL(s);
	test(n == L"www", L"hostname only", s, n);

	s = L"http://www.domain.com";
	n = getNameForURL(s);
	test(n == L"www.domain.com", L"domain only", s, n);

	s = L"http://www.domain.com/";
	n = getNameForURL(s);
	test(n == L"www.domain.com", L"domain only with trailing slash", s, n);

	s = L"http://www.domain.com/path/";
	n = getNameForURL(s);
	test(n == L"path", L"path", s, n);

	s = L"http://www.domain.com/path/file";
	n = getNameForURL(s);
	test(n == L"file", L"file", s, n);

	s = L"http://www.domain.com/file.ext";
	n = getNameForURL(s);
	test(n == L"file", L"file with extension", s, n);

	s = L"http://www.domain.com/file.ext#anchor";
	n = getNameForURL(s);
	test(n == L"file anchor", L"anchor", s, n);

	s = L"http://www.domain.com/file.ext#";
	n = getNameForURL(s);
	test(n == L"file ", L"empty anchor", s, n);

	s = L"http://www.domain.com/#";
	n = getNameForURL(s);
	test(n == L"www.domain.com ", L"empty anchor no file", s, n);

	s = L"http://www.domain.com/file.ext?query";
	n = getNameForURL(s);
	test(n == L"file query", L"query string", s, n);

	s = L"http://www.domain.com/file.ext?query#anchor";
	n = getNameForURL(s);
	test(n == L"file query anchor", L"query string and anchor", s, n);

	s = L"file.ext";
	n = getNameForURL(s);
	test(n == L"file", "no proto, file only", s, n);

	s = L"/";
	n = getNameForURL(s);
	test(n == L"", L"no proto, slash only", s, n);

	s = L"/path/file.ext";
	n = getNameForURL(s);
	test(n == L"file", L"no proto, path and file", s, n);

	s = L"file.ext?query";
	n = getNameForURL(s);
	test(n == L"file query", L"no proto, file and query only", s, n);

	s = L"?query";
	n = getNameForURL(s);
	test(n == L" query", L"no proto, query only", s, n);

	s = L"/?query";
	n = getNameForURL(s);
	test(n == L" query", L"no proto, slash and query only", s, n);
}

void test_multiValueAttribsStringToMap() {
	wstring s;
	multiValueAttribsMap  m;
	multiValueAttribsMap::iterator it;

	multiValueAttribsStringToMap(s, m);
	testNoIO(m.size() == 0, L"empty");
	m.clear();

	s = L"a:1;b:2;c:3;";
	multiValueAttribsStringToMap(s, m);
	testNoIO(m.size() == 3 && m.find(L"a")->second == L"1" && m.find(L"b")->second == L"2" && m.find(L"c")->second == L"3", L"normal: " << s);
	m.clear();

	s = L"a\\:b:1;b:2\\;3;c\\;d:4\\:5;";
	multiValueAttribsStringToMap(s, m);
	testNoIO(m.size() == 3 && m.find(L"a:b")->second == L"1" && m.find(L"b")->second == L"2;3" && m.find(L"c;d")->second == L"4:5", L"escaping: " << s);
	m.clear();

	s = L":;";
	multiValueAttribsStringToMap(s, m);
	testNoIO(m.size() == 0, L"empty key: " << s);
	m.clear();

	s = L"a:;";
	multiValueAttribsStringToMap(s, m);
	testNoIO(m.size() == 1 && m.find(L"a")->second == L"", L"empty value: " << s);
	m.clear();

	s = L"a:1,2;";
	multiValueAttribsStringToMap(s, m);
	testNoIO(m.size() == 2 && m.count(L"a") == 2 && (it = m.find(L"a"))->second == L"1" && (++it)->second == L"2", L"single multi value: " << s);
	m.clear();

	s = L"a:a1,a2;b:b1;";
	multiValueAttribsStringToMap(s, m);
	testNoIO(m.size() == 3 && m.count(L"a") == 2 && m.count(L"b") == 1 && (it = m.find(L"a"))->second == L"a1" && (++it)->second == L"a2" && m.find(L"b")->second == L"b1", L"mixed multi and non-multi values: " << s);
	m.clear();

	s = L"a:a1,a2;b:;";
	multiValueAttribsStringToMap(s, m);
	testNoIO(m.size() == 3 && m.count(L"a") == 2 && m.count(L"b") == 1 && m.find(L"a")->second == L"a1" && m.find(L"b")->second == L"", L"mixed empty and multi values: " << s);
	m.clear();
}

int main(int argc, char *argv[]) {
	test_getNameForURL();
	test_multiValueAttribsStringToMap();
	if(failCount>0) {
		wcerr<<L"number of failed tests: "<<failCount<<endl;
	}
	return failCount;
}
