# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2025 NV Access Limited, Christopher Toth, Tyler Spivey, Babbage B.V., David Sexton and others.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Local machine interface for NVDA Remote.

This module provides functionality for controlling the local NVDA instance
in response to commands received from remote connections.

:param speech: Controls speech output and cancellation
:param braille: Handles braille display sharing and input routing
:param audio: Provides feedback through wave files and tones
:param input: Simulates keyboard and system input
:param clipboard: Enables one-way text transfer from remote
:param system: Provides functions like Secure Attention Sequence (SAS)

The main class :class:`LocalMachine` implements all local control operations
that can be triggered by remote NVDA instances. It includes safety features like
muting and uses wxPython's CallAfter for thread synchronization.

:note: This module is part of the NVDA Remote protocol implementation and should
    not be used directly outside of the remote connection infrastructure.
"""

import ctypes
import logging
import os
from typing import Any, Dict, List, Optional

import api
import braille
import inputCore
import nvwave
import speech
import tones
import wx
from speech.priorities import Spri
from speech.types import SpeechSequence

from . import cues, input

try:
	from systemUtils import hasUiAccess
except ModuleNotFoundError:
	from config import hasUiAccess

import ui

logger = logging.getLogger("local_machine")


def setSpeechCancelledToFalse() -> None:
	"""Reset the speech cancellation flag to allow new speech.

	:note: Updates NVDA's internal speech state to ensure future speech will not be cancelled.
	    Required when receiving remote speech commands.
	:warning: This is a temporary workaround that modifies internal NVDA state.
	    May break in future NVDA versions if the speech subsystem changes.
	:seealso: :meth:`LocalMachine.speak`
	"""
	# workaround as beenCanceled is readonly as of NVDA#12395
	speech.speech._speechState.beenCanceled = False


class LocalMachine:
	"""Controls the local NVDA instance based on remote commands.

	This class implements the local side of remote control functionality,
	serving as the bridge between network commands and local NVDA operations.
	It ensures thread-safe execution and proper state management.

	:ivar isMuted: When True, most remote commands will be ignored
	:type isMuted: bool
	:ivar receivingBraille: When True, braille output comes from remote
	:type receivingBraille: bool
	:ivar _cachedSizes: Cached braille display sizes from remote machines
	:type _cachedSizes: Optional[List[int]]

	:note: This class is instantiated by the remote session manager and should not
	    be created directly. All methods are called in response to remote messages.

	:seealso:
	    - :class:`session.SlaveSession` - Manages remote connections
	    - :mod:`transport` - Network transport layer
	"""

	def __init__(self) -> None:
		"""Initialize the local machine controller.

		:note: The local machine starts unmuted with local braille enabled.
		"""
		self.isMuted: bool = False
		self.receivingBraille: bool = False
		self._cachedSizes: Optional[List[int]] = None
		braille.decide_enabled.register(self.handleDecideEnabled)

	def terminate(self) -> None:
		"""Clean up resources when the local machine controller is terminated.

		:note: Unregisters the braille display handler to prevent memory leaks and
		    ensure proper cleanup when the remote connection ends.
		"""
		braille.decide_enabled.unregister(self.handleDecideEnabled)

	def playWave(self, fileName: str) -> None:
		"""Play a wave file on the local machine.

		:param fileName: Path to the wave file to play
		:note: Sound playback is ignored if the local machine is muted.
		       The file must exist on the local system.
		"""
		if self.isMuted:
			return
		if os.path.exists(fileName):
			nvwave.playWaveFile(fileName=fileName, asynchronous=True)

	def beep(self, hz: float, length: int, left: int = 50, right: int = 50) -> None:
		"""Play a beep sound on the local machine.

		:param hz: Frequency of the beep in Hertz
		:param length: Duration of the beep in milliseconds
		:param left: Left channel volume (0-100)
		:param right: Right channel volume (0-100)
		:note: Beeps are ignored if the local machine is muted.
		"""
		if self.isMuted:
			return
		tones.beep(hz, length, left, right)

	def cancelSpeech(self) -> None:
		"""Cancel any ongoing speech on the local machine.

		:note: Speech cancellation is ignored if the local machine is muted.
		    Uses wx.CallAfter to ensure thread-safe execution.
		"""
		if self.isMuted:
			return
		wx.CallAfter(speech._manager.cancel)

	def pauseSpeech(self, switch: bool) -> None:
		"""Pause or resume speech on the local machine.

		:param switch: True to pause speech, False to resume
		:note: Speech control is ignored if the local machine is muted.
		       Uses wx.CallAfter to ensure thread-safe execution.
		"""
		if self.isMuted:
			return
		wx.CallAfter(speech.pauseSpeech, switch)

	def speak(
		self,
		sequence: SpeechSequence,
		priority: Spri = Spri.NORMAL,
	) -> None:
		"""Process a speech sequence from a remote machine.

		Safely queues speech from remote NVDA instances into the local speech
		subsystem, handling priority and ensuring proper cancellation state.

		:param sequence: List of speech sequences (text and commands) to speak
		:param priority: Speech priority level
		:note: Speech is always queued asynchronously via wx.CallAfter to ensure
		       thread safety, as this may be called from network threads.
		"""
		if self.isMuted:
			return
		setSpeechCancelledToFalse()
		wx.CallAfter(speech._manager.speak, sequence, priority)

	def display(self, cells: List[int]) -> None:
		"""Update the local braille display with cells from remote.

		Safely writes braille cells from a remote machine to the local braille
		display, handling display size differences and padding.

		:param cells: List of braille cells as integers (0-255)
		:note: Only processes cells when:
		       - receivingBraille is True (display sharing is enabled)
		       - Local display is connected (displaySize > 0)
		       - Remote cells fit on local display

		       Cells are padded with zeros if remote data is shorter than local display.
		       Uses thread-safe _writeCells method for compatibility with all displays.
		"""
		if (
			self.receivingBraille
			and braille.handler.displaySize > 0
			and len(cells) <= braille.handler.displaySize
		):
			cells = cells + [0] * (braille.handler.displaySize - len(cells))
			wx.CallAfter(braille.handler._writeCells, cells)

	def brailleInput(self, **kwargs: Dict[str, Any]) -> None:
		"""Process braille input gestures from a remote machine.

		Executes braille input commands locally using NVDA's input gesture system.
		Handles both display routing and braille keyboard input.

		:param kwargs: Gesture parameters passed to BrailleInputGesture
		:note: Silently ignores gestures that have no associated action.
		"""
		try:
			inputCore.manager.executeGesture(input.BrailleInputGesture(**kwargs))
		except inputCore.NoInputGestureAction:
			pass

	def setBrailleDisplay_size(self, sizes: List[int]) -> None:
		"""Cache remote braille display sizes for size negotiation.

		:param sizes: List of display sizes (cells) from remote machines
		"""
		self._cachedSizes = sizes

	def handleFilterDisplaySize(self, value: int) -> int:
		"""Filter the local display size based on remote display sizes.

		Determines the optimal display size when sharing braille output by
		finding the smallest positive size among local and remote displays.

		:param value: Local display size in cells
		:return: The negotiated display size to use
		"""
		if not self._cachedSizes:
			return value
		sizes = self._cachedSizes + [value]
		try:
			return min(i for i in sizes if i > 0)
		except ValueError:
			return value

	def handleDecideEnabled(self) -> bool:
		"""Determine if the local braille display should be enabled.

		:return: False if receiving remote braille, True otherwise
		"""
		return not self.receivingBraille

	def sendKey(
		self,
		vk_code: Optional[int] = None,
		extended: Optional[bool] = None,
		pressed: Optional[bool] = None,
	) -> None:
		"""Simulate a keyboard event on the local machine.

		:param vk_code: Virtual key code to simulate
		:param extended: Whether this is an extended key
		:param pressed: True for key press, False for key release
		"""
		wx.CallAfter(input.sendKey, vk_code, None, extended, pressed)

	def setClipboardText(self, text: str) -> None:
		"""Set the local clipboard text from a remote machine.

		:param text: Text to copy to the clipboard
		"""
		cues.clipboardReceived()
		api.copyToClip(text=text)

	def sendSAS(self) -> None:
		"""Simulate a secure attention sequence (e.g. CTRL+ALT+DEL).

		:note: SendSAS requires UI Access. If this fails, a warning is displayed.
		"""
		if hasUiAccess():
			ctypes.windll.sas.SendSAS(0)
		else:
			# Translators: Message displayed when a remote machine tries to send a SAS but UI Access is disabled.
			ui.message(_("No permission on device to trigger CTRL+ALT+DEL from remote"))
			logger.warning("UI Access is disabled on this machine so cannot trigger CTRL+ALT+DEL")
