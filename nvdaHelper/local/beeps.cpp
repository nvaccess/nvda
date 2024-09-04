/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2006-2015 NVDA contributers.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/
#define _USE_MATH_DEFINES
#include <cmath>
#include <algorithm>
#include "beeps.h"


using std::min;
using std::max;

const int sampleRate=44100;
const int amplitude=14000;

int generateBeep(short* buf, const float hz, const int length, const int left, const int right) {
	const int samplesPerCycle=static_cast<int>(sampleRate/hz);
	int totalSamples=static_cast<int>((length/1000.0)/(1.0/sampleRate));
	totalSamples+=samplesPerCycle-(totalSamples%samplesPerCycle);
	if (!buf) { //just return buffer length
		return totalSamples*4;
	}
	const double lpan=(left/100.0)*amplitude, rpan=(right/100.0)*amplitude;
	const double sinFreq=(2.0*M_PI)/(sampleRate/hz); //DON'T use samplesPerCycle here
	for (int sampleNum=0; sampleNum<totalSamples; ++sampleNum) {
		const double sample=min(max(sin((sampleNum%sampleRate)*sinFreq)*2.0,-1.0),1.0);
		buf[sampleNum*2]=static_cast<short>(sample*lpan);
		buf[sampleNum*2+1]=static_cast<short>(sample*rpan);
	}
	return totalSamples*4;
}
