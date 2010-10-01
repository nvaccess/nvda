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

#define _USE_MATH_DEFINES
#include <cmath>
#include "beeps.h"
using namespace std;

const float PITWO=M_PI*2;
const unsigned sampleRate=44100;
const int amplitude=14000;

unsigned generateBeep(short* buf, const float hz, const unsigned length, const unsigned char left, const unsigned char right) {
	const unsigned samplesPerCycle=(sampleRate/hz);
	unsigned totalSamples=(length/1000.0)/(1.0/sampleRate);
	totalSamples+=(samplesPerCycle-(totalSamples%samplesPerCycle));
	if (!buf) { //just return buffer length
		return totalSamples*4;
	}
	const float sinFreq=PITWO/samplesPerCycle;
	for (unsigned sampleNum=0; sampleNum<totalSamples; ++sampleNum) {
		const short sample=min(max(sin((sampleNum%sampleRate)*sinFreq)*2,-1),1)*amplitude;
		const short leftSample=sample*(left/100.0);
		const short rightSample=sample*(right/100.0);
		buf[sampleNum*2]=leftSample;
		buf[sampleNum*2+1]=rightSample;
	}
	return totalSamples*4;
}