# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2025 NV Access Limited, Christopher Toth, Tyler Spivey, Babbage B.V., David Sexton and others.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Local machine interface for NVDA Remote.

This module provides functionality for controlling the local NVDA instance
in response to commands received from remote connections.

The main class :class:`LocalMachine` implements all local control operations
that can be triggered by remote NVDA instances. It includes safety features like
muting and uses wxPython's CallAfter for thread synchronization.

.. note::

	This module is part of the NVDA Remote protocol implementation and should
	not be used directly outside of the remote connection infrastructure.
"""

from enum import IntEnum, nonmember
import os
from typing import Any, Dict, List, Optional
import winreg

import winBindings.sas
import api
import braille
from config.registry import RegistryKey
import inputCore
import nvwave
import speech
import tones
import wx
from speech.priorities import Spri
from speech.types import SpeechSequence
from systemUtils import hasUiAccess
import ui
from logHandler import log
from utils.security import isRunningOnSecureDesktop

from . import cues, input


class SoftwareSASGeneration(IntEnum):
	"""
	Possible values for the Windows Components | Windows Logon Options | Disable or enable software Secure Attention Sequence group policy.

	Values extracted from WinLogon.admx.
	<https://www.microsoft.com/en-us/download/details.aspx?id=106254>
	"""

	NONE = 0
	"""User mode software cannot simulate the SAS."""

	SYSTEM = 1
	"""Services can simulate the SAS."""

	UIACCESS = 2
	"""Ease of Access applications can simulate the SAS"""

	BOTH = 3
	"""both services and Ease of Access applications can simulate the SAS."""

	KEY: int = nonmember(winreg.HKEY_LOCAL_MACHINE)
	SUBKEY: str = nonmember(RegistryKey.SYSTEM_POLICIES.value)
	VALUE_NAME: str = nonmember("SoftwareSASGeneration")
	DISPLAY_PATH: str = nonmember(
		rf"HKLM\{RegistryKey.SYSTEM_POLICIES.value}!SoftwareSASGeneration",
	)


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

	:note: This class is instantiated by the remote session manager and should not
	    be created directly. All methods are called in response to remote messages.

	:seealso:
	    - :class:`session.FollowerSession` - Manages remote connections
	    - :mod:`transport` - Network transport layer
	"""

	def __init__(self) -> None:
		"""Initialize the local machine controller.

		:note: The local machine starts unmuted with local braille enabled.
		"""
		self.isMuted: bool = False
		"""When True, most remote commands will be ignored"""

		self.receivingBraille: bool = False
		"""When True, braille output comes from remote"""

		self._cachedSizes: Optional[List[int]] = None
		"""Cached braille display sizes from remote machines"""

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

	def setBrailleDisplaySize(self, sizes: List[int]) -> None:
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
		"""Simulate a secure attention sequence (i.e. control+alt+delete).

		:note: SendSAS requires UI Access. If this fails, a warning is displayed.
		"""
		if self._canSendSAS():
			winBindings.sas.SendSAS(not isRunningOnSecureDesktop())
		else:
			# Translators: Message displayed when a remote computer tries to send control+alt+delete but UI Access is disabled.
			ui.message(pgettext("remote", "Unable to trigger control+alt+delete"))

	@staticmethod
	def _canSendSAS() -> bool:
		"""Determine if we have sufficient permissions to send a secure attention sequence.

		If we can't, a more specific reason is logged.

		:return: True if simulating an SAS should succeed, false otherwise.
		"""
		if not hasUiAccess():
			log.debug("Unable to simulate the SAS as NVDA does not have UI Access.")
			return False
		# If we have UI Access, whether we can simulate the SAS depends on the Software SAS Generation group policy.
		try:
			with winreg.OpenKeyEx(SoftwareSASGeneration.KEY, SoftwareSASGeneration.SUBKEY) as regkey:
				valueData, valueType = winreg.QueryValueEx(regkey, SoftwareSASGeneration.VALUE_NAME)
				if valueType != winreg.REG_DWORD:
					# SoftwareSASGeneration should be a REG_DWORD, but it isn't.
					# Return False to avoid a false positive.
					log.debug(
						f"{SoftwareSASGeneration.DISPLAY_PATH} is not a REG_DWORD. Got {valueType=}, {valueData=}",
					)
					return False
				if valueData not in (SoftwareSASGeneration.UIACCESS, SoftwareSASGeneration.BOTH):
					# UIAccess means ease of access applications can simulate the SAS,
					# and both means services and ease of access applications can simulate the SAS.
					# Since it's neither of these values, we can't simulate an SAS.
					log.debug(
						f"The setting of {SoftwareSASGeneration.DISPLAY_PATH} does not allow NVDA to simulate the SAS. Got {valueData=}",
					)
					return False
		except FileNotFoundError:
			# The group policy is either disabled or not set,
			# which means that ATs can only simulate the SAS on secure desktops.
			if not isRunningOnSecureDesktop():
				log.debug(
					f"Unable to simulate the SAS as {SoftwareSASGeneration.DISPLAY_PATH} is not set and NVDA is not running on the secure desktop.",
				)
				return False
		except OSError:
			# Something went wrong trying to read the registry.
			# Return False to avoid a false positive.
			log.error(f"Error reading {SoftwareSASGeneration.DISPLAY_PATH}.", exc_info=True)
			return False
		# None of the known impediments to simulating the SAS seem to hold,
		# so it should be safe to do so.
		return True
