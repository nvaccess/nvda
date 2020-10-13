# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2020 Bill Dengler

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
		"Start the nvda_dmp process if it is not already running."
		if not DiffMatchPatch._proc:
			log.debug("Starting diff-match-patch proxy")
			if hasattr(sys, "frozen"):
				dmp_path = (os.path.join(globalVars.appDir, "nvda_dmp.exe"),)
			else:
				dmp_path = (sys.executable, os.path.join(
					globalVars.appDir, "..", "include", "nvda_dmp", "nvda_dmp.py"
				))
			DiffMatchPatch._proc = subprocess.Popen(
				dmp_path,
				creationflags=subprocess.CREATE_NO_WINDOW,
				bufsize=0,
				stdin=subprocess.PIPE,
				stdout=subprocess.PIPE
			)

	def _getText(self, ti: TextInfo) -> str:
		return ti.text

	def diff(self, newText: str, oldText: str) -> List[str]:
		with DiffMatchPatch._lock:
			try:
				self._initialize()
				if not newText and not oldText:
					# Return an empty list here to avoid exiting
					# nvda_dmp uses two zero-length texts as a sentinal value
					return []
				old = oldText.encode("utf-8")
				new = newText.encode("utf-8")
				# Sizes are packed as 32-bit ints in native byte order.
				# Since nvda and nvda_dmp are running on the same Python
				# platform/version, this is okay.
				tl = struct.pack("=II", len(old), len(new))
				DiffMatchPatch._proc.stdin.write(tl)
				DiffMatchPatch._proc.stdin.write(old)
				DiffMatchPatch._proc.stdin.write(new)
				buf = b""
				sizeb = b""
				SIZELEN = 4
				while len(sizeb) < SIZELEN:
					try:
						sizeb += DiffMatchPatch._proc.stdout.read(SIZELEN - len(sizeb))
					except TypeError:
						pass
				(size,) = struct.unpack("=I", sizeb)
				while len(buf) < size:
					buf += DiffMatchPatch._proc.stdout.read(size - len(buf))
				return [
					line
					for line in buf.decode("utf-8").splitlines()
					if line and not line.isspace()
				]
			except Exception:
				log.exception("Exception in DMP, falling back to difflib")
				return Difflib().diff(newText, oldText)

	def _terminate(self):
		if DiffMatchPatch._proc:
			log.debug("Terminating diff-match-patch proxy")
			# nvda_dmp exits when it receives two zero-length texts.
			DiffMatchPatch._proc.stdin.write(struct.pack("=II", 0, 0))


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


def get_dmp_algo():
	"""
		This property controls which diff algorithm is used. The default
		implementation returns either diffHandler.dmp or diffHandler.difflib
		based on user preference. Subclasses can override this property to
		choose a diffAlgo object (overriding user preference)
		if one is incompatible with a particular application.
		As of NVDA 2020.4, diffHandler.dmp is experimental. Therefore,
		subclasses should either use the base implementation to check the
		user config, or return diffHandler.difflib
		to forcibly use Difflib.
	"""
	return (
		dmp
		if config.conf["terminals"]["diffAlgo"] == "dmp"
		else difflib
	)


difflib = Difflib()
dmp = DiffMatchPatch()
