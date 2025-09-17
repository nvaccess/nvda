// A part of NonVisual Desktop Access (NVDA)
// This file is covered by the GNU General Public License.
// See the file COPYING for more details.
// Copyright (C) 2025 NV Access Limited, gexgd0419

#ifndef SILENCEDETECT_H
#define SILENCEDETECT_H

#include <windows.h>
#include <mmreg.h>
#include <stdint.h>
#include <type_traits>
#include <limits>

namespace SilenceDetect {

/**
 * Compile-time wave format tag.
 * Supports integer and floating-point formats.
 * `SampleType` should be the smallest numeric type that can hold a sample, for example, 32-bit int for 24-bit format.
 * Signedness of `SampleType` matters. For unsigned types, the zero point is at middle, e.g. 128 for 8-bit unsigned.
 * `bytesPerSample` should be <= `sizeof(SampleType)` for integer formats,
 * and == `sizeof(SampleType)` for floating-point formats.
 * Assumes C++20 standard.
 */
template <typename SampleType, size_t bytesPerSample = sizeof(SampleType)>
struct WaveFormat {
	static_assert(std::is_arithmetic_v<SampleType>, "SampleType should be an integer or floating-point type");
	static_assert(!(std::is_floating_point_v<SampleType> && bytesPerSample != sizeof(SampleType)),
		"When SampleType is a floating-point type, bytesPerSample should be equal to sizeof(SampleType)");
	static_assert(!(std::is_integral_v<SampleType> && !(bytesPerSample <= sizeof(SampleType) && bytesPerSample > 0)),
		"When SampleType is an integer type, bytesPerSample should be less than or equal to sizeof(SampleType) and greater than 0");

	typedef SampleType SampleType;
	static constexpr size_t bytesPerSample = bytesPerSample;

	static constexpr SampleType zeroPoint() {
		// for unsigned types, zero point is at middle
		// for signed types, zero is zero
		if constexpr (std::is_unsigned_v<SampleType>)
			return SampleType(1) << (bytesPerSample * 8 - 1);
		else
			return SampleType();
	}

	static constexpr SampleType (max)() {
		if constexpr (std::is_floating_point_v<SampleType>) {
			// For floating-point samples, maximum value is 1.0
			return SampleType(1);
		} else {
			// Trim the maximum value to `bytesPerSample` bytes
			return (std::numeric_limits<SampleType>::max)() >> ((sizeof(SampleType) - bytesPerSample) * 8);
		}
	}

	static constexpr SampleType (min)() {
		if constexpr (std::is_floating_point_v<SampleType>) {
			// For floating-point samples, minimum value is -1.0
			return SampleType(-1);
		} else {
			// Trim the minimum value to `bytesPerSample` bytes
			return (std::numeric_limits<SampleType>::min)() >> ((sizeof(SampleType) - bytesPerSample) * 8);
		}
	}

	static constexpr SampleType defaultThreshold() {
		// Default threshold: 1 / 2^10 or 0.0009765625
		return (max)() / (1 << 10);
	}

	static constexpr auto toSigned(SampleType smp) {
		if constexpr (std::is_integral_v<SampleType>) {
			// In C++20, signed integer types must use two's complement,
			// so the following conversion is well-defined.
			using SignedType = std::make_signed_t<SampleType>;
			return SignedType(smp - zeroPoint());
		} else {
			return smp;
		}
	}

	static constexpr SampleType fromSigned(SampleType smp) {
		if constexpr (std::is_integral_v<SampleType>) {
			// Signed overflow is undefined behavior,
			// so convert to unsigned first.
			using UnsignedType = std::make_unsigned_t<SampleType>;
			return SampleType(UnsignedType(smp) + zeroPoint());
		} else {
			return smp;
		}
	}

	static constexpr SampleType signExtend(SampleType smp) {
		if constexpr (std::is_unsigned_v<SampleType> || bytesPerSample == sizeof(SampleType)) {
			return smp;
		} else {
			constexpr auto shift = (sizeof(SampleType) - bytesPerSample) * 8;
			// Convert to unsigned first to prevent left-shifting negative numbers
			using UnsignedType = std::make_unsigned_t<SampleType>;
			return SampleType(UnsignedType(smp) << shift) >> shift;
		}
	}
};

inline WORD getFormatTag(const WAVEFORMATEX* wfx) {
	if (wfx->wFormatTag == WAVE_FORMAT_EXTENSIBLE) {
		auto wfext = reinterpret_cast<const WAVEFORMATEXTENSIBLE*>(wfx);
		if (IS_VALID_WAVEFORMATEX_GUID(&wfext->SubFormat))
			return EXTRACT_WAVEFORMATEX_ID(&wfext->SubFormat);
	}
	return wfx->wFormatTag;
}

/**
 * Return the leading silence wave data length, in bytes.
 * Assumes the wave data to be of one channel (mono).
 * Uses a `WaveFormat` type (`Fmt`) to determine the wave format.
 */
template <class Fmt>
size_t getLeadingSilenceSizeMono(
	const unsigned char* waveData,
	size_t size,
	typename Fmt::SampleType threshold
) {
	using SampleType = Fmt::SampleType;
	constexpr size_t bytesPerSample = Fmt::bytesPerSample;

	if (size < bytesPerSample)
		return 0;

	constexpr SampleType zeroPoint = Fmt::zeroPoint();
	const SampleType minValue = zeroPoint - threshold, maxValue = zeroPoint + threshold;

	// Check each sample
	SampleType smp = SampleType();
	const unsigned char* const pEnd = waveData + (size - (size % bytesPerSample));
	for (const unsigned char* p = waveData; p < pEnd; p += bytesPerSample) {
		memcpy(&smp, p, bytesPerSample);
		smp = Fmt::signExtend(smp);
		// this sample is out of range, so the previous sample is the final sample of leading silence.
		if (smp < minValue || smp > maxValue)
			return p - waveData;
	}

	// The whole data block is silence
	return size;
}

/**
 * Invoke a functor with an argument of a WaveFormat type that corresponds to the specified WAVEFORMATEX.
 * Return false if the WAVEFORMATEX is unknown.
 */
template <class Func>
bool callByWaveFormat(const WAVEFORMATEX* wfx, Func&& func) {
	switch (getFormatTag(wfx)) {
	case WAVE_FORMAT_PCM:
		switch (wfx->wBitsPerSample) {
		case 8:  // 8-bits are unsigned, others are signed
			func(WaveFormat<uint8_t>());
			break;
		case 16:
			func(WaveFormat<int16_t>());
			break;
		case 24:
			func(WaveFormat<int32_t, 3>());
			break;
		case 32:
			func(WaveFormat<int32_t>());
			break;
		default:
			return false;
		}
		break;
	case WAVE_FORMAT_IEEE_FLOAT:
		switch (wfx->wBitsPerSample) {
		case 32:
			func(WaveFormat<float>());
			break;
		case 64:
			func(WaveFormat<double>());
			break;
		default:
			return false;
		}
		break;
	default:
		return false;
	}
	return true;
}

/**
 * Return the leading silence wave data length, in bytes.
 * Uses a `WAVEFORMATEX` to determine the wave format.
 */
inline size_t getLeadingSilenceSize(
	const WAVEFORMATEX* wfx,
	const unsigned char* waveData,
	size_t size
) {
	size_t len;
	if (!callByWaveFormat(wfx, [=, &len](auto fmtTag) {
			using Fmt = decltype(fmtTag);
			len = getLeadingSilenceSizeMono<Fmt>(
				waveData, size, Fmt::defaultThreshold());
		}))
		return 0;

	return len - len % wfx->nBlockAlign;  // round down to block (channel) boundaries
}

}  // namespace SilenceDetect

#endif  // SILENCEDETECT_H
