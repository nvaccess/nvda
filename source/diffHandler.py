# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020-2022 NV Access Limited, Bill Dengler
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import config
import globalVars
import os
import struct
import subprocess
import sys
from abc import abstractmethod
from baseObject import AutoPropertyObject
from difflib import ndiff
from logHandler import log
from textInfos import TextInfo, UNIT_LINE
from threading import Lock
from typing import List
import NVDAState


class DiffAlgo(AutoPropertyObject):
	@abstractmethod
	def diff(self, newText: str, oldText: str) -> List[str]:
		raise NotImplementedError

	@abstractmethod
	def _getText(self, ti: TextInfo) -> str:
		raise NotImplementedError


class DiffMatchPatch(DiffAlgo):
	"""A character-based diffing approach, using the Google Diff Match Patch
	library in a proxy process (to work around a licence conflict).
	"""

	#: A subprocess.Popen object for the nvda_dmp process.
	_proc = None
	#: A lock to control access to the nvda_dmp process.
	#: Control access to avoid synchronization problems if multiple threads
	#: attempt to use nvda_dmp at the same time.
	_lock = Lock()

	def _initialize(self):
		"""Start the nvda_dmp process if it is not already running.
		@note: This should be run from within the context of an acquired lock."""
		if not DiffMatchPatch._proc:
			log.debug("Starting diff-match-patch proxy")
			if NVDAState.isRunningAsSource():
				dmp_path = (
					sys.executable,
					os.path.join(
						globalVars.appDir,
						"..",
						"include",
						"nvda_dmp",
						"nvda_dmp.py",
					),
				)
			else:
				dmp_path = (os.path.join(globalVars.appDir, "nvda_dmp.exe"),)
			DiffMatchPatch._proc = subprocess.Popen(
				dmp_path,
				creationflags=subprocess.CREATE_NO_WINDOW,
				bufsize=0,
				stdin=subprocess.PIPE,
				stdout=subprocess.PIPE,
			)

	def _getText(self, ti: TextInfo) -> str:
		return ti.text

	@classmethod
	def _readData(cls, size: int) -> bytes:
		"""Reads from stdout, raises exception on EOF."""
		buffer = b""
		while (remainingLength := size - len(buffer)) > 0:
			chunk = cls._proc.stdout.read(remainingLength)
			if chunk:
				buffer += chunk
				continue
			return_code = cls._proc.poll()
			if return_code is None:
				continue
			raise RuntimeError(f"Diff-match-patch proxy process died! Return code {return_code}")
		return buffer

	def diff(self, newText: str, oldText: str) -> List[str]:
		try:
			if not newText and not oldText:
				# Return an empty list here to avoid exiting
				# nvda_dmp uses two zero-length texts as a sentinal value
				return []
			with DiffMatchPatch._lock:
				self._initialize()
				oldEncodedText = oldText.encode()
				newEncodedText = newText.encode()
				# Sizes are packed as 32-bit ints in native byte order.
				# Since nvda and nvda_dmp are running on the same Python
				# platform/version, this is okay.
				packedTextLength = struct.pack("=II", len(oldEncodedText), len(newEncodedText))
				DiffMatchPatch._proc.stdin.write(packedTextLength)
				DiffMatchPatch._proc.stdin.write(oldEncodedText)
				DiffMatchPatch._proc.stdin.write(newEncodedText)
				DiffMatchPatch._proc.stdin.flush()
				DIFF_LENGTH_BUFFER_SIZE = 4
				diffLengthBuffer = DiffMatchPatch._readData(DIFF_LENGTH_BUFFER_SIZE)
				(diff_length,) = struct.unpack("=I", diffLengthBuffer)
				diffBuffer = DiffMatchPatch._readData(diff_length)
				return [
					line for line in diffBuffer.decode("utf-8").splitlines() if line and not line.isspace()
				]
		except Exception:
			log.exception("Exception in DMP, falling back to difflib")
			self._terminate()
			return Difflib().diff(newText, oldText)

	def _terminate(self):
		with DiffMatchPatch._lock:
			if DiffMatchPatch._proc:
				log.debug("Terminating diff-match-patch proxy")
				# nvda_dmp exits when it receives two zero-length texts.
				returnCode = DiffMatchPatch._proc.poll()
				if returnCode is None:
					try:
						DiffMatchPatch._proc.stdin.write(struct.pack("=II", 0, 0))
						DiffMatchPatch._proc.wait(timeout=5)
					except Exception:
						log.exception("Exception during DMP termination")
				else:
					log.debug(f"Diff-match-patch proxy already terminated, return code is {returnCode}")
				DiffMatchPatch._proc = None


class Difflib(DiffAlgo):
	"A line-based diffing approach in pure Python, using the Python standard library."

	def diff(self, newText: str, oldText: str) -> List[str]:
		newLines = newText.splitlines()
		oldLines = oldText.splitlines()
		outLines = []

		prevLine = None

		for line in ndiff(oldLines, newLines):
			if line[0] == "?":
				# We're never interested in these.
				continue
			if line[0] != "+":
				# We're only interested in new lines.
				prevLine = line
				continue
			text = line[2:]
			if not text or text.isspace():
				prevLine = line
				continue

			if prevLine and prevLine[0] == "-" and len(prevLine) > 2:
				# It's possible that only a few characters have changed in this line.
				# If so, we want to speak just the changed section, rather than the entire line.
				prevText = prevLine[2:]
				textLen = len(text)
				prevTextLen = len(prevText)
				# Find the first character that differs between the two lines.
				for pos in range(min(textLen, prevTextLen)):
					if text[pos] != prevText[pos]:
						start = pos
						break
				else:
					# We haven't found a differing character so far and we've hit the end of one of the lines.
					# This means that the differing text starts here.
					start = pos + 1
				# Find the end of the differing text.
				if textLen != prevTextLen:
					# The lines are different lengths, so assume the rest of the line changed.
					end = textLen
				else:
					for pos in range(textLen - 1, start - 1, -1):
						if text[pos] != prevText[pos]:
							end = pos + 1
							break

				if end - start < 15:
					# Less than 15 characters have changed, so only speak the changed chunk.
					text = text[start:end]

			if text and not text.isspace():
				outLines.append(text)
			prevLine = line

		return outLines

	def _getText(self, ti: TextInfo) -> str:
		return "\n".join(ti.getTextInChunks(UNIT_LINE))


def prefer_dmp():
	"""
	This function returns a Diff Match Patch object if allowed by the user.
	DMP is new and can be explicitly disabled by a user setting. If config
	does not allow DMP, this function returns a Difflib instance instead.
	"""
	return _difflib if config.conf["terminals"]["diffAlgo"] == "difflib" else _dmp


def prefer_difflib():
	"""
	This function returns a Difflib object if allowed by the user.
	Difflib can be explicitly disabled by a user setting. If config
	does not allow Difflib, this function returns a DMP instance instead.
	"""
	return _dmp if config.conf["terminals"]["diffAlgo"] == "dmp" else _difflib


_difflib = Difflib()
_dmp = DiffMatchPatch()
