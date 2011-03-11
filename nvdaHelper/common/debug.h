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

#ifndef DEBUG_H
#define DEBUG_H

#include <iostream>

extern std::wostream* _debugFile;

//initialization and termination functions
void debug_start(std::wostream* s);
void debug_end();

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
