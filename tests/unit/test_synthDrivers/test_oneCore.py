# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""OneCore queue recovery without a synth DLL or audio device."""

import ctypes
import struct
import unittest
from unittest import mock

from synthDrivers import oneCore


class TestInitialAudioOpenRecovery(unittest.TestCase):
	def setUp(self):
		# Use the real class and methods, without initializing Windows speech.
		self.driver = oneCore.SynthDriver.__new__(oneCore.SynthDriver)
		self.driver._earlyExitCB = False
		self.driver._player = None
		self.driver._queuedSpeech = []
		self.driver._wasCancelled = False
		self.driver._isProcessing = False
		self.driver._consecutiveSpeechFailures = 0
		self.driver._ocSpeechToken = 1
		self.driver._dll = mock.Mock()
		self._patch(oneCore.SynthDriver, "supportsProsodyOptions", False)
		self._patch(oneCore, "isDebugForSynthDriver", lambda: False)
		self.log = self._patch(oneCore, "log", mock.Mock())
		self.index = self._patch(oneCore.synthIndexReached, "notify", mock.Mock())
		self.done = self._patch(oneCore.synthDoneSpeaking, "notify", mock.Mock())
		self.fallback = self._patch(oneCore.queueHandler, "queueFunction", mock.Mock())
		# Existing synth tests also mock WavePlayer to avoid WASAPI device access.
		self.player = mock.Mock()
		self.player.samplesPerSec = 24000
		self.player.feed.side_effect = self._feed
		self.wavePlayer = self._patch(oneCore.nvwave, "WavePlayer", mock.Mock(return_value=self.player))
		pcm = b"\0" * 16
		fmt = struct.pack("<HHIIHHH", 1, 1, 24000, 48000, 2, 16, 0)
		wav = (
			b"RIFF"
			+ struct.pack("<I", 4 + 8 + len(fmt) + 8 + len(pcm))
			+ b"WAVEfmt "
			+ struct.pack("<I", len(fmt))
			+ fmt
			+ b"data"
			+ struct.pack("<I", len(pcm))
			+ pcm
		)
		self.assertEqual(oneCore.WAVE_HEADER_LENGTH, len(wav) - len(pcm))
		self.buffer = ctypes.create_string_buffer(wav)
		self.size = len(wav)

	def _patch(self, target, name, value):
		patcher = mock.patch.object(target, name, value)
		patcher.start()
		self.addCleanup(patcher.stop)
		return value

	def _feed(self, data, size, onDone=None):
		# Complete only callbacks actually submitted by the genuine driver.
		if onDone is not None:
			onDone()

	def _callback(self, index):
		self.driver._callback(ctypes.addressof(self.buffer), self.size, f"{index}:0")

	def test_initialOpenFailureAllowsNewRequestAfterCancelAndDeviceRecovery(self):
		self.wavePlayer.side_effect = OSError(1168, "audio endpoint unavailable")
		self.driver._queueSpeech("first")
		self._callback(10)
		self.assertFalse(self.driver._isProcessing)
		self.assertIsNone(self.driver._player)
		self.index.assert_not_called()
		self.done.assert_not_called()
		self.log.exception.assert_called_once_with("Error initializing OneCore audio playback")
		self.driver.cancel()
		self.wavePlayer.side_effect = None
		self.driver._queueSpeech("new request")
		self.assertEqual(
			[mock.call(1, "first"), mock.call(1, "new request")],
			self.driver._dll.ocSpeech_speak.call_args_list,
		)
		self._callback(20)
		self.index.assert_called_once_with(synth=self.driver, index=20)
		self.done.assert_called_once_with(synth=self.driver)
		self.assertFalse(self.driver._isProcessing)
		self.assertEqual(0, self.driver._consecutiveSpeechFailures)

	def test_healthyQueuedRequestsStillComplete(self):
		self.driver._queueSpeech("first")
		self.driver._queueSpeech("second")
		self.driver._dll.ocSpeech_speak.assert_called_once_with(1, "first")
		self._callback(10)
		self.assertTrue(self.driver._isProcessing)
		self.done.assert_not_called()
		self.assertEqual(2, self.driver._dll.ocSpeech_speak.call_count)
		self._callback(20)
		self.assertEqual(
			[mock.call(synth=self.driver, index=10), mock.call(synth=self.driver, index=20)],
			self.index.call_args_list,
		)
		self.done.assert_called_once_with(synth=self.driver)
		self.assertFalse(self.driver._isProcessing)
		self.assertEqual(0, self.driver._consecutiveSpeechFailures)

	def test_repeatedOpenFailuresDoNotSwitchSynth(self):
		# An unavailable audio device is not a synthesizer failure; another synth could not play either.
		self.wavePlayer.side_effect = OSError(1168, "audio endpoint unavailable")
		for attempt in range(self.driver.MAX_CONSECUTIVE_SPEECH_FAILURES + 1):
			self.driver._queueSpeech(f"request {attempt}")
			self._callback(10 + attempt)
			self.assertFalse(self.driver._isProcessing)
		self.fallback.assert_not_called()
		self.index.assert_not_called()
		self.done.assert_not_called()
