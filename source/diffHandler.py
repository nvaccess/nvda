# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020-2025 NV Access Limited, Bill Dengler
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import config
import fast_diff_match_patch
from abc import abstractmethod
from baseObject import AutoPropertyObject
from difflib import ndiff
from logHandler import log
from textInfos import TextInfo, UNIT_LINE
from typing import List


class DiffAlgo(AutoPropertyObject):
	@abstractmethod
	def diff(self, newText: str, oldText: str) -> List[str]:
		raise NotImplementedError

	@abstractmethod
	def _getText(self, ti: TextInfo) -> str:
		raise NotImplementedError


class DiffMatchPatch(DiffAlgo):
	"""
	A character-based diffing approach, using the Google Diff Match
	Patch library.
	"""

	_GOOD_LINE_ENDINGS = ("\n", "\r")

	def _getText(self, ti: TextInfo) -> str:
		return ti.text

	def diff(self, newText: str, oldText: str) -> List[str]:
		try:
			outLines: List[str] = []
			for op, text in fast_diff_match_patch.diff(oldText, newText, counts_only=False):
				if op != "+":
					continue
				# Ensure a trailing newline so .splitlines() keeps the final fragment
				if not text.endswith(self._GOOD_LINE_ENDINGS):
					text += "\n"
				for line in text.splitlines():
					if line and not line.isspace():
						outLines.append(line)
			return outLines
		except Exception:
			log.exception("Exception in DMP, falling back to difflib")
			return _difflib.diff(newText, oldText)


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
