/**
 * base/debug.cpp
 * Part of the NV  Virtual Buffer Library
 * This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
 * This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
 * http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
 */

#include <fstream>
#include "debug.h"

using namespace std;

wostream* _debugFile=NULL;

void debug_start(wostream* s) {
	if(!_debugFile) {
		_debugFile=s;
		(*_debugFile)<<L"Debugging started"<<endl;
	}
}

void debug_end() {
	if(_debugFile) {
		(*_debugFile)<<L"Debugging ended"<<endl;
		_debugFile=NULL;
	}
}
