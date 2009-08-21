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
	for (unsigned sampleNum=0; sampleNum<totalSamples; ++sampleNum) {
		const short sample=min(max(sin((sampleNum%sampleRate)*PITWO*(hz/sampleRate))*2,-1),1)*amplitude;
		const short leftSample=sample*(left/100.0);
		const short rightSample=sample*(right/100.0);
		buf[sampleNum*2]=leftSample;
		buf[sampleNum*2+1]=rightSample;
	}
	return totalSamples*4;
}