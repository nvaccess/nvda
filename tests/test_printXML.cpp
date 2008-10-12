/**
 * tests/test_printXML.cpp
 * Part of the NV  Virtual Buffer Library
 * This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
 * This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
 * http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
 */

#include <iostream>
#include <fstream>
#include <string>
#include "debug.h"
#include "container.h"

#ifdef DEBUG
#define testBackendPath L"lib_debug/VBufBackend_test.dll"
#else
#define testBackendPath L"lib/VBufBackend_test.dll"
#endif

int main(int argc, char* argv[]) {
	#ifdef DEBUG
	std::wofstream *debugFile=new std::wofstream("debug.log");
	debug_start(debugFile);
	#endif
	VBufContainer_t* buffer=new VBufContainer_t(1,1,testBackendPath);
	std::wstring s;
	buffer->storageBuffer->lock.acquire();
	buffer->storageBuffer->getTextInRange(0,buffer->storageBuffer->getTextLength(),s,false);
	buffer->storageBuffer->lock.release();
	std::wcout<<s<<std::endl;
	delete buffer;
	#ifdef DEBUG
	//debug_end();
	//delete debugFile;
#endif
	return 0;
}
