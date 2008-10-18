/**
 * tests/test_printExampleBackendXML/test_printExampleBackendXML.cpp
 * Part of the NV  Virtual Buffer Library
 * This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
 * This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
 * http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
 */

#include <iostream>
#include <fstream>
#include <string>
#include <base/base.h>

std::wstring correctXMLString=L"<control controlIdentifier_docHandle=\"1\" controlIdentifier_ID=\"1\" role=\"document\"><control controlIdentifier_docHandle=\"1\" controlIdentifier_ID=\"2\" level=\"1\" role=\"heading\"><text>Test for Virtual Buffer Library</text></control><control controlIdentifier_docHandle=\"1\" controlIdentifier_ID=\"3\" role=\"paragraph\"><text>This content has been rendered by the Test backend. For a much better example of how the Virtual buffer library can be used, please visit the </text><control controlIdentifier_docHandle=\"1\" controlIdentifier_ID=\"4\" role=\"link\" value=\"http://www.nvda-project.org/\"><text>NVDA website</text></control><text>where you can find the NVDA screen reader.</text></control><control controlIdentifier_docHandle=\"1\" controlIdentifier_ID=\"5\" role=\"paragraph\"><text>Copyright (c)2008 NV Access</text></control></control>";

#define testBackendPath "VBufBackend_example.dll"

int main(int argc, char* argv[]) {
	#ifdef DEBUG
	std::wofstream *debugFile=new std::wofstream("debug.log");
	debug_start(debugFile);
	#endif
	VBufContainer_t* buffer=new VBufContainer_t(1,1,testBackendPath);
	std::wstring s;
	buffer->lock.acquire();
	buffer->getTextInRange(0,buffer->getTextLength(),s,true);
	buffer->lock.release();
	delete buffer;
	if(s!=correctXMLString) {
		std::wcerr<<L"Bad XML: "<<s<<std::endl;
		exit(1);
	}
	#ifdef DEBUG
	debug_end();
	delete debugFile;
#endif
	return 0;
}
