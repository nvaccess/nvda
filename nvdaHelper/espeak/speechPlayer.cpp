#include "speak_lib.h"
#include "speech.h"
#include "klatt.h"
#include "phoneme.h"
#include "synthesize.h"
#include "voice.h"
#include <speechPlayer/src/speechPlayer.h>

extern WGEN_DATA wdata;
extern voice_t *wvoice;
extern unsigned char *out_ptr;
extern unsigned char *out_end;

speechPlayer_handle_t speechPlayerHandle=NULL;
#define minFadeLength 110

int mixWaveFile(int maxNumSamples, sample* sampleBuf) {
	int i=0;
	for(;wdata.mix_wavefile_ix<wdata.n_mix_wavefile;++wdata.mix_wavefile_ix) {
		if(i>=maxNumSamples) break;
		int val;
		if(wdata.mix_wave_scale==0) {
			val=wdata.mix_wavefile[wdata.mix_wavefile_ix];
			++(wdata.mix_wavefile_ix);
			signed char c=wdata.mix_wavefile[wdata.mix_wavefile_ix];
			val+=(c*256);
		} else {
			val=(signed char)wdata.mix_wavefile[wdata.mix_wavefile_ix]*wdata.mix_wave_scale;
		}
		val*=(wdata.amplitude_v/1024.0);
		val=(val*wdata.mix_wave_amp)/40;
		sampleBuf[i].value+=val;
		++i;
	}
	return i;
}

bool isKlattFrameFollowing() {
	for(int i=(wcmdq_head+1)%N_WCMDQ;i!=wcmdq_tail;i=(i+1)%N_WCMDQ) {
		int cmd=wcmdq[i][0];
		if(cmd==WCMD_PAUSE||cmd==WCMD_WAVE) {
			break;
		}
		if(cmd==WCMD_KLATT) {
			return true;
		}
	}
	return false;
}

void fillSpeechPlayerFrame(frame_t * eFrame, speechPlayer_frame_t* spFrame) {
	spFrame->voicePitch=(wdata.pitch)/4096;
	spFrame->voiceAmplitude=1;
	spFrame->cf1=(eFrame->ffreq[1]*wvoice->freq[1]/256.0)+wvoice->freqadd[1];
	spFrame->cf2=(eFrame->ffreq[2]*wvoice->freq[2]/256.0)+wvoice->freqadd[2];
	spFrame->cf3=(eFrame->ffreq[3]*wvoice->freq[3]/256.0)+wvoice->freqadd[3];
	spFrame->cf4=(eFrame->ffreq[4]*wvoice->freq[4]/256.0)+wvoice->freqadd[4];
	spFrame->cf5=(eFrame->ffreq[5]*wvoice->freq[5]/256.0)+wvoice->freqadd[5];
	spFrame->cf6=(eFrame->ffreq[6]*wvoice->freq[6]/256.0)+wvoice->freqadd[6];
	spFrame->cfNP=280;
	spFrame->cfN0=eFrame->klattp[KLATT_FNZ]*2;
	if(spFrame->cfN0==0) {
		spFrame->cfN0=spFrame->cfNP;
		spFrame->caNP=0;
	} else {
		spFrame->cfN0=450;
		spFrame->cfNP=216;
		spFrame->caNP=1;
	}
	spFrame->cb1=eFrame->bw[1]*2*(wvoice->width[1]/256.0);
	spFrame->cb2=eFrame->bw[2]*2*(wvoice->width[2]/256.0);
	spFrame->cb3=eFrame->bw[3]*2*(wvoice->width[3]/256.0);
	spFrame->cb4=eFrame->bw[4]*2*(wvoice->width[4]/256.0);
	spFrame->cb5=1000;
	spFrame->cb6=1000;
	spFrame->cbNP=100;
	spFrame->cbN0=100;
	spFrame->preFormantGain=3*(wdata.amplitude/100.0);
	spFrame->endVoicePitch=spFrame->voicePitch;
}

void KlattInit() {
	speechPlayerHandle=speechPlayer_initialize(22050);
}

void KlattReset(int control) {
	speechPlayer_terminate(speechPlayerHandle);
	speechPlayerHandle=speechPlayer_initialize(22050);
	//speechPlayer_queueFrame(speechPlayerHandle,NULL,minFadeLength,1,-1,true);
	//pendingFrameLength=0;
}

int Wavegen_Klatt2(int length, int modulation, int resume, frame_t *fr1, frame_t *fr2){
	if(!resume) {
		speechPlayer_frame_t spFrame1={0};
		fillSpeechPlayerFrame(fr1,&spFrame1);
		speechPlayer_frame_t spFrame2={0};
		fillSpeechPlayerFrame(fr2,&spFrame2);
		wdata.pitch_ix+=(wdata.pitch_inc*(length/STEPSIZE));
		wdata.pitch=((wdata.pitch_env[min(wdata.pitch_ix>>8,127)]*wdata.pitch_range)>>8)+wdata.pitch_base;
		spFrame2.endVoicePitch=wdata.pitch/4096;
		int mainLength=length;
		speechPlayer_queueFrame(speechPlayerHandle,&spFrame1,minFadeLength,minFadeLength,-1,false);
		mainLength-=minFadeLength;
		bool fadeOut=!isKlattFrameFollowing();
		if(fadeOut) {
			mainLength-=fadeOut;
		}
		mainLength=max(mainLength,1);
		speechPlayer_queueFrame(speechPlayerHandle,&spFrame2,mainLength,mainLength,-1,false);
		if(fadeOut) {
			speechPlayer_queueFrame(speechPlayerHandle,NULL,minFadeLength*1.5,minFadeLength,-1,false);
		}
	}
	int maxLength=(out_end-out_ptr)/sizeof(sample);
	int outLength=speechPlayer_synthesize(speechPlayerHandle,maxLength,(sample*)out_ptr);
	int waveOutLength=mixWaveFile(outLength,(sample*)out_ptr);
	out_ptr=out_ptr+(sizeof(sample)*outLength);
	if(out_ptr>=out_end) return 1;
	return 0;
}
