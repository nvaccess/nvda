// This is a modified version of the Sonic Library's header,
// which added __declspec(dllimport) to each function
// if SONIC_DLL is defined.
// Used when compiling eSpeak dynamically linked to Sonic.

#ifndef SONIC_H_
#define SONIC_H_

/* Sonic library
   Copyright 2010
   Bill Cox
   This file is part of the Sonic Library.

   This file is licensed under the Apache 2.0 license.
*/

/*
The Sonic Library implements a new algorithm invented by Bill Cox for the
specific purpose of speeding up speech by high factors at high quality.  It
generates smooth speech at speed up factors as high as 6X, possibly more.  It is
also capable of slowing down speech, and generates high quality results
regardless of the speed up or slow down factor.  For speeding up speech by 2X or
more, the following equation is used:

    newSamples = period/(speed - 1.0)
    scale = 1.0/newSamples;

where period is the current pitch period, determined using AMDF or any other
pitch estimator, and speed is the speedup factor.  If the current position in
the input stream is pointed to by "samples", and the current output stream
position is pointed to by "out", then newSamples number of samples can be
generated with:

    out[t] = (samples[t]*(newSamples - t) + samples[t + period]*t)/newSamples;

where t = 0 to newSamples - 1.

For speed factors < 2X, the PICOLA algorithm is used.  The above
algorithm is first used to double the speed of one pitch period.  Then, enough
input is directly copied from the input to the output to achieve the desired
speed up factor, where 1.0 < speed < 2.0.  The amount of data copied is derived:

    speed = (2*period + length)/(period + length)
    speed*length + speed*period = 2*period + length
    length(speed - 1) = 2*period - speed*period
    length = period*(2 - speed)/(speed - 1)

For slowing down speech where 0.5 < speed < 1.0, a pitch period is inserted into
the output twice, and length of input is copied from the input to the output
until the output desired speed is reached.  The length of data copied is:

    length = period*(speed - 0.5)/(1 - speed)

For slow down factors below 0.5, no data is copied, and an algorithm
similar to high speed factors is used.
*/

/* Uncomment this to use sin-wav based overlap add which in theory can improve
   sound quality slightly, at the expense of lots of floating point math. */
/* #define SONIC_USE_SIN */

#ifdef SONIC_DLL
#ifdef SONIC_EXPORT
#define SONIC_API __declspec(dllexport)
#else
#define SONIC_API __declspec(dllimport)
#endif  /* SONIC_EXPORT */
#else
#define SONIC_API
#endif  /* SONIC_DLL */

#ifdef __cplusplus
extern "C" {
#endif

#ifdef SONIC_INTERNAL
/* The following #define's are used to change the names of the routines defined
 * here so that a new library (i.e. speedy) can reuse these names, and then call
 * the original names.  We do this for two reasons: 1) we don't want to change
 * the original API, and 2) we want to add a shim, using the original names and
 * still call these routines.
 *
 * Original users of this API and the libsonic library need to do nothing.  The
 * original behavior remains.
 *
 * A new user that add some additional functionality above this library (a shim)
 * should #define SONIC_INTERNAL before including this file, undefine all these
 * symbols and call the sonicIntXXX functions directly.
 */
#define sonicCreateStream sonicIntCreateStream
#define sonicDestroyStream sonicIntDestroyStream
#define sonicWriteFloatToStream sonicIntWriteFloatToStream
#define sonicWriteShortToStream sonicIntWriteShortToStream
#define sonicWriteUnsignedCharToStream sonicIntWriteUnsignedCharToStream
#define sonicReadFloatFromStream sonicIntReadFloatFromStream
#define sonicReadShortFromStream sonicIntReadShortFromStream
#define sonicReadUnsignedCharFromStream sonicIntReadUnsignedCharFromStream
#define sonicFlushStream sonicIntFlushStream
#define sonicSamplesAvailable sonicIntSamplesAvailable
#define sonicGetSpeed sonicIntGetSpeed
#define sonicSetSpeed sonicIntSetSpeed
#define sonicGetPitch sonicIntGetPitch
#define sonicSetPitch sonicIntSetPitch
#define sonicGetRate sonicIntGetRate
#define sonicSetRate sonicIntSetRate
#define sonicGetVolume sonicIntGetVolume
#define sonicSetVolume sonicIntSetVolume
#define sonicGetQuality sonicIntGetQuality
#define sonicSetQuality sonicIntSetQuality
#define sonicGetSampleRate sonicIntGetSampleRate
#define sonicSetSampleRate sonicIntSetSampleRate
#define sonicGetNumChannels sonicIntGetNumChannels
#define sonicGetUserData sonicIntGetUserData
#define sonicSetUserData sonicIntSetUserData
#define sonicSetNumChannels sonicIntSetNumChannels
#define sonicChangeFloatSpeed sonicIntChangeFloatSpeed
#define sonicChangeShortSpeed sonicIntChangeShortSpeed
#define sonicEnableNonlinearSpeedup sonicIntEnableNonlinearSpeedup
#define sonicSetDurationFeedbackStrength sonicIntSetDurationFeedbackStrength
#define sonicComputeSpectrogram sonicIntComputeSpectrogram
#define sonicGetSpectrogram sonicIntGetSpectrogram

#endif /* SONIC_INTERNAL */

/* This specifies the range of voice pitches we try to match.
   Note that if we go lower than 65, we could overflow in findPitchInRange */
#ifndef SONIC_MIN_PITCH
#define SONIC_MIN_PITCH 65
#endif  /* SONIC_MIN_PITCH */
#ifndef SONIC_MAX_PITCH
#define SONIC_MAX_PITCH 400
#endif  /* SONIC_MAX_PITCH */

/* These are used to down-sample some inputs to improve speed */
#define SONIC_AMDF_FREQ 4000

struct sonicStreamStruct;
typedef struct sonicStreamStruct* sonicStream;

/* For all of the following functions, numChannels is multiplied by numSamples
   to determine the actual number of values read or returned. */

/* Create a sonic stream.  Return NULL only if we are out of memory and cannot
  allocate the stream. Set numChannels to 1 for mono, and 2 for stereo. */
SONIC_API sonicStream sonicCreateStream(int sampleRate, int numChannels);
/* Destroy the sonic stream. */
SONIC_API void sonicDestroyStream(sonicStream stream);
/* Attach user data to the stream. */
SONIC_API void sonicSetUserData(sonicStream stream, void *userData);
/* Retrieve user data attached to the stream. */
SONIC_API void *sonicGetUserData(sonicStream stream);
/* Use this to write floating point data to be speed up or down into the stream.
   Values must be between -1 and 1.  Return 0 if memory realloc failed,
   otherwise 1 */
SONIC_API int sonicWriteFloatToStream(sonicStream stream, const float* samples, int numSamples);
/* Use this to write 16-bit data to be speed up or down into the stream.
   Return 0 if memory realloc failed, otherwise 1 */
SONIC_API int sonicWriteShortToStream(sonicStream stream, const short* samples, int numSamples);
/* Use this to write 8-bit unsigned data to be speed up or down into the stream.
   Return 0 if memory realloc failed, otherwise 1 */
SONIC_API int sonicWriteUnsignedCharToStream(sonicStream stream, const unsigned char* samples,
                                   int numSamples);
/* Use this to read floating point data out of the stream.  Sometimes no data
   will be available, and zero is returned, which is not an error condition. */
SONIC_API int sonicReadFloatFromStream(sonicStream stream, float* samples,
                             int maxSamples);
/* Use this to read 16-bit data out of the stream.  Sometimes no data will
   be available, and zero is returned, which is not an error condition. */
SONIC_API int sonicReadShortFromStream(sonicStream stream, short* samples,
                             int maxSamples);
/* Use this to read 8-bit unsigned data out of the stream.  Sometimes no data
   will be available, and zero is returned, which is not an error condition. */
SONIC_API int sonicReadUnsignedCharFromStream(sonicStream stream, unsigned char* samples,
                                    int maxSamples);
/* Force the sonic stream to generate output using whatever data it currently
   has.  No extra delay will be added to the output, but flushing in the middle
   of words could introduce distortion. */
SONIC_API int sonicFlushStream(sonicStream stream);
/* Return the number of samples in the output buffer */
SONIC_API int sonicSamplesAvailable(sonicStream stream);
/* Get the speed of the stream. */
SONIC_API float sonicGetSpeed(sonicStream stream);
/* Set the speed of the stream. */
SONIC_API void sonicSetSpeed(sonicStream stream, float speed);
/* Get the pitch of the stream. */
SONIC_API float sonicGetPitch(sonicStream stream);
/* Set the pitch of the stream. */
SONIC_API void sonicSetPitch(sonicStream stream, float pitch);
/* Get the rate of the stream. */
SONIC_API float sonicGetRate(sonicStream stream);
/* Set the rate of the stream. */
SONIC_API void sonicSetRate(sonicStream stream, float rate);
/* Get the scaling factor of the stream. */
SONIC_API float sonicGetVolume(sonicStream stream);
/* Set the scaling factor of the stream. */
SONIC_API void sonicSetVolume(sonicStream stream, float volume);
/* Chord pitch is DEPRECATED.  AFAIK, it was never used by anyone.  These
   functions still exist to avoid breaking existing code. */
/* Get the chord pitch setting. */
SONIC_API int sonicGetChordPitch(sonicStream stream);
/* Set chord pitch mode on or off.  Default is off.  See the documentation
   page for a description of this feature. */
SONIC_API void sonicSetChordPitch(sonicStream stream, int useChordPitch);
/* Get the quality setting. */
SONIC_API int sonicGetQuality(sonicStream stream);
/* Set the "quality".  Default 0 is virtually as good as 1, but very much
 * faster. */
SONIC_API void sonicSetQuality(sonicStream stream, int quality);
/* Get the sample rate of the stream. */
SONIC_API int sonicGetSampleRate(sonicStream stream);
/* Set the sample rate of the stream.  This will drop any samples that have not
 * been read. */
SONIC_API void sonicSetSampleRate(sonicStream stream, int sampleRate);
/* Get the number of channels. */
SONIC_API int sonicGetNumChannels(sonicStream stream);
/* Set the number of channels.  This will drop any samples that have not been
 * read. */
SONIC_API void sonicSetNumChannels(sonicStream stream, int numChannels);
/* This is a non-stream oriented interface to just change the speed of a sound
   sample.  It works in-place on the sample array, so there must be at least
   speed*numSamples available space in the array. Returns the new number of
   samples. */
SONIC_API int sonicChangeFloatSpeed(float* samples, int numSamples, float speed,
                          float pitch, float rate, float volume,
                          int useChordPitch, int sampleRate, int numChannels);
/* This is a non-stream oriented interface to just change the speed of a sound
   sample.  It works in-place on the sample array, so there must be at least
   speed*numSamples available space in the array. Returns the new number of
   samples. */
SONIC_API int sonicChangeShortSpeed(short* samples, int numSamples, float speed,
                          float pitch, float rate, float volume,
                          int useChordPitch, int sampleRate, int numChannels);

#ifdef SONIC_SPECTROGRAM
/*
This code generates high quality spectrograms from sound samples, using
Time-Aliased-FFTs as described at:

    https://github.com/waywardgeek/spectrogram

Basically, two adjacent pitch periods are overlap-added to create a sound
sample that accurately represents the speech sound at that moment in time.
This set of samples is converted to a spetral line using an FFT, and the result
is saved as a single spectral line at that moment in time.  The resulting
spectral lines vary in resolution (it is equal to the number of samples in the
pitch period), and the spacing of spectral lines also varies (proportional to
the numver of samples in the pitch period).

To generate a bitmap, linear interpolation is used to render the grayscale
value at any particular point in time and frequency.
*/

#define SONIC_MAX_SPECTRUM_FREQ 5000

struct sonicSpectrogramStruct;
struct sonicBitmapStruct;
typedef struct sonicSpectrogramStruct* sonicSpectrogram;
typedef struct sonicBitmapStruct* sonicBitmap;

/* sonicBitmap objects represent spectrograms as grayscale bitmaps where each
   pixel is from 0 (black) to 255 (white).  Bitmaps are rows*cols in size.
   Rows are indexed top to bottom and columns are indexed left to right */
struct sonicBitmapStruct {
  unsigned char* data;
  int numRows;
  int numCols;
};

typedef struct sonicBitmapStruct* sonicBitmap;

/* Enable coomputation of a spectrogram on the fly. */
SONIC_API void sonicComputeSpectrogram(sonicStream stream);

/* Get the spectrogram. */
SONIC_API sonicSpectrogram sonicGetSpectrogram(sonicStream stream);

/* Create an empty spectrogram. Called automatically if sonicComputeSpectrogram
   has been called. */
SONIC_API sonicSpectrogram sonicCreateSpectrogram(int sampleRate);

/* Destroy the spectrotram.  This is called automatically when calling
   sonicDestroyStream. */
SONIC_API void sonicDestroySpectrogram(sonicSpectrogram spectrogram);

/* Convert the spectrogram to a bitmap. Caller must destroy bitmap when done. */
SONIC_API sonicBitmap sonicConvertSpectrogramToBitmap(sonicSpectrogram spectrogram,
                                            int numRows, int numCols);

/* Destroy a bitmap returned by sonicConvertSpectrogramToBitmap. */
SONIC_API void sonicDestroyBitmap(sonicBitmap bitmap);

SONIC_API int sonicWritePGM(sonicBitmap bitmap, char* fileName);

/* Add two pitch periods worth of samples to the spectrogram.  There must be
   2*period samples.  Time should advance one pitch period for each call to
   this function. */
SONIC_API void sonicAddPitchPeriodToSpectrogram(sonicSpectrogram spectrogram,
                                      short* samples, int numSamples,
                                      int numChannels);
#endif  /* SONIC_SPECTROGRAM */

#ifdef __cplusplus
}
#endif

#endif  /* SONIC_H_ */
