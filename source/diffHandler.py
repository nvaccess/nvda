# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2020 Bill Dengler

import globalVars
import os
import struct
import subprocess
import sys
from difflib import ndiff
from logHandler import log
from typing import List

_dmpProc = None


def _dmp(newText: str, oldText: str) -> List[str]:
	global _dmpProc
	try:
		initialize()
		if not newText and not oldText:
			# Return an empty list here to avoid exiting
			# nvda_dmp uses two zero-length texts as a sentinal value
			return []
		old = oldText.encode("utf-8")
		new = newText.encode("utf-8")
		# Sizes are packed as 32-bit ints in native byte order.
		# Since nvda and nvda_dmp are running under the same interpreter, this is okay.
		tl = struct.pack("=II", len(old), len(new))
		_dmpProc.stdin.write(tl)
		_dmpProc.stdin.write(old)
		_dmpProc.stdin.write(new)
		buf = b""
		sizeb = b""
		SIZELEN = 4
		while len(sizeb) < SIZELEN:
			try:
				sizeb += _dmpProc.stdout.read(SIZELEN - len(sizeb))
			except TypeError:
				pass
		(size,) = struct.unpack("=I", sizeb)
		while len(buf) < size:
			buf += _dmpProc.stdout.read(size - len(buf))
		return [
			line
			for line in buf.decode("utf-8").splitlines()
			if line and not line.isspace()
		]
	except Exception:
		log.exception("Exception in DMP, falling back to difflib")
		return _difflib(newText, oldText)


def _difflib(newText: str, oldText: str) -> List[str]:
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


def _should_use_DMP(supports_dmp: bool = True):
	import config
	return supports_dmp and config.conf["terminals"]["useDMPWhenSupported"]


def initialize():
	global _dmpProc
	if not _dmpProc:
		log.debug("Starting diff-match-patch proxy")
		if hasattr(sys, "frozen"):
			dmp_path = (os.path.join(globalVars.appDir, "nvda_dmp.exe"),)
		else:
			dmp_path = (sys.executable, os.path.join(
				globalVars.appDir, "..", "include", "nvda_dmp", "nvda_dmp.py"
			))
		_dmpProc = subprocess.Popen(
			dmp_path,
			creationflags=subprocess.CREATE_NO_WINDOW,
			bufsize=0,
			stdin=subprocess.PIPE,
			stdout=subprocess.PIPE
		)


def terminate():
	global _dmpProc
	try:
		if _dmpProc:
			log.debug("Terminating diff-match-patch proxy")
			_dmpProc.stdin.write(struct.pack("=II", 0, 0))  # Sentinal value
	except Exception:
		pass


def diff(newText: str, oldText: str, supports_dmp: bool = True):
	return _dmp(newText, oldText) if _should_use_DMP(supports_dmp=supports_dmp) else _difflib(newText, oldText)
