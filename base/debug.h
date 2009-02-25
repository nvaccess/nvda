/**
 * base/debug.h
 * Part of the NV  Virtual Buffer Library
 * This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
 * This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
 * http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
 */

#ifndef DEBUG_H
#define DEBUG_H

#include <iostream>
#include "libEntry.h"

extern VBUFLIBENTRY std::wostream* _debugFile;

//initialization and termination functions
VBUFLIBENTRY void debug_start(std::wostream* s);
VBUFLIBENTRY void debug_end();

#ifdef DEBUG

#ifndef __GNUC__
#define __PRETTY_FUNCTION__ __FUNCTION__
#endif

#define __STR2WSTR(x) L##x
#define _STR2WSTR(x) __STR2WSTR(x)

#include <wchar.h>

#define DEBUG_MSG(messageArg) {\
	if(_debugFile!=NULL) {\
		wchar_t* __WFUNCTION__=(wchar_t*)malloc(sizeof(wchar_t)*1024);\
		mbstowcs(__WFUNCTION__,__PRETTY_FUNCTION__,1023);\
		(*_debugFile)<<L"debug "<<__WFUNCTION__<<L", line "<<__LINE__<<L" of file "<<_STR2WSTR(__FILE__)<<L":\n"<<messageArg<<std::endl<<std::flush;\
		free(__WFUNCTION__);\
	}\
}

#else

#define DEBUG_MSG(messageArg)

#endif

#endif
