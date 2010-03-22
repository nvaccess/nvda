#define _USE_MATH_DEFINES
#include <cmath>
#include "beeps.h"
using namespace std;

#define SAMPLERATE 4100
#define AMPLITUDE 14000

const DOUBLE PITWO=M_PI*2;

unsigned int generateBeep(short* buf, const float hz, const unsigned int length, const unsigned char left, const unsigned char right) {
	const unsigned int samplesPerCycle=(unsigned int)(SAMPLERATE/hz);
	unsigned int totalSamples=(unsigned int)((length/1000.0)/(1.0/SAMPLERATE));
	totalSamples+=(samplesPerCycle-(totalSamples%samplesPerCycle));
	if (!buf) { //just return buffer length
		return totalSamples*4;
	}
	const DOUBLE sinFreq=PITWO/samplesPerCycle;
	for (unsigned sampleNum=0; sampleNum<totalSamples; ++sampleNum) {
		const short sample=(short)min(max(sin((sampleNum%SAMPLERATE)*sinFreq)*2,-1),1)*AMPLITUDE;
		const short leftSample=(short)(sample*(left/100.0));
		const short rightSample=(short)(sample*(right/100.0));
		buf[sampleNum*2]=leftSample;
		buf[sampleNum*2+1]=rightSample;
	}
	return totalSamples*4;
}