# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""NVWave service for ART - provides wave playback functionality to add-ons."""

import Pyro5.api
import nvwave
from logHandler import log
from .base import BaseService


@Pyro5.api.expose
class NVWaveService(BaseService):
	"""Provides wave playback functionality for add-ons running in ART."""

	def __init__(self):
		super().__init__("NVWaveService")

	def playWaveFile(self, fileName: str, asynchronous: bool = True, isSpeechWaveFileCommand: bool = False) -> bool:
		"""Play a wave file.

		@param fileName: Path to the wave file to play
		@param asynchronous: Whether to play asynchronously
		@param isSpeechWaveFileCommand: Whether this is part of a speech sequence
		@return: True if playback was initiated successfully
		"""
		try:
			# Validate the file path to ensure it's safe
			if not fileName:
				log.warning("Empty filename provided to playWaveFile")
				return False

			# Call the actual nvwave function
			nvwave.playWaveFile(
				fileName=fileName,
				asynchronous=asynchronous,
				isSpeechWaveFileCommand=isSpeechWaveFileCommand
			)

			log.debug(f"Playing wave file: {fileName}")
			return True

		except Exception:
			self._log_error("playWaveFile", fileName)
			return False

	def isInError(self) -> bool:
		"""Check if the audio device is in an error state.

		@return: True if there's an audio device error
		"""
		try:
			return nvwave.isInError()
		except Exception:
			self._log_error("isInError")
			return True
