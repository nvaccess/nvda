#ifndef BEEPS_H_INCLUDED
#define BEEPS_H_INCLUDED

#include "nvdaHelperLocal.h"

DLLEXPORT unsigned generateBeep(short* buf, const float hz, const unsigned length, const unsigned char left=50, const unsigned char right = 50);

#endif