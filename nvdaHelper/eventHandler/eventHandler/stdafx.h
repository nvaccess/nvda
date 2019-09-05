// stdafx.h : include file for standard system include files,
// or project specific include files that are used frequently, but
// are changed infrequently
//

#pragma once

#define WIN32_LEAN_AND_MEAN             // Exclude rarely-used stuff from Windows headers



// reference additional headers your program requires here
#define NOMINMAX  // Use std::min / std::max
#include <windows.h>
#undef NOMINMAX

#include <oleacc.h>
#include <objbase.h>
