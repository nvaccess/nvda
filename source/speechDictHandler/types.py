# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2026 NV Access Limited, Aleksey Sadovoy, Peter Vagner, Aaron Cannon, Leonard de Ruijter, Cyrille Bougot
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Types used for the speech dictionary system."""

from functools import cached_property
import os
import re
from dataclasses import dataclass, field
from typing import Self

from logHandler import log
from NVDAState import shouldWriteToDisk
from utils.displayString import DisplayStringIntEnum, DisplayStringStrEnum


class EntryType(DisplayStringIntEnum):
	"""Types of speech dictionary entries:"""

	ANYWHERE = 0
	"""String can match anywhere"""
	WORD = 2
	"""String must have word boundaries on both sides to match"""
	REGEXP = 1
	"""Regular expression"""

	@cached_property
	def _displayStringLabels(self) -> dict[Self, str]:
		return {
			# Translators: This is a label for an Entry Type radio button in add dictionary entry dialog.
			EntryType.ANYWHERE: _("&Anywhere"),
			# Translators: This is a label for an Entry Type radio button in add dictionary entry dialog.
			EntryType.REGEXP: _("Regular &expression"),
			# Translators: This is a label for an Entry Type radio button in add dictionary entry dialog.
			EntryType.WORD: _("Whole &word"),
		}


class DictionaryType(DisplayStringStrEnum):
	"""Types of speech dictionaries."""

	TEMP = "temp"
	"""Temporary speech dictionary."""
	VOICE = "voice"
	"""Voice specific speech dictionary."""
	DEFAULT = "default"
	"""Default speech dictionary."""
	BUILTIN = "builtin"
	"""Built-in speech dictionary."""

	@cached_property
	def _displayStringLabels(self) -> dict[Self, str]:
		return {
			# Translators: A type of speech dictionary.
			DictionaryType.TEMP: _("Temporary"),
			# Translators: A type of speech dictionary.
			DictionaryType.VOICE: _("Voice specific"),
			# Translators: A type of speech dictionary.
			DictionaryType.DEFAULT: _("Default"),
			# Translators: A type of speech dictionary.
			DictionaryType.BUILTIN: _("Built-in"),
		}


@dataclass
class SpeechDictEntry:
	pattern: str
	"""The pattern to match."""
	replacement: str
	"""The replacement string."""
	comment: str
	"""A comment associated with this entry."""
	caseSensitive: bool = True
	"""Whether the match is case sensitive."""
	type: EntryType = EntryType.ANYWHERE
	"""The type of the entry."""
	compiled: re.Pattern = field(init=False)
	"""The compiled regular expression."""

	def __post_init__(self):
		flags = re.U
		if not self.caseSensitive:
			flags |= re.IGNORECASE
		if self.type == EntryType.REGEXP:
			tempPattern = self.pattern
		elif self.type == EntryType.WORD:
			tempPattern = r"\b" + re.escape(self.pattern) + r"\b"
		else:
			tempPattern = re.escape(self.pattern)
			self.type = EntryType.ANYWHERE  # Ensure sane values.
		self.compiled = re.compile(tempPattern, flags)

	def sub(self, text: str) -> str:
		if self.type == EntryType.REGEXP:
			replacement = self.replacement
		else:
			# Escape the backslashes for non-regexp replacements
			replacement = self.replacement.replace("\\", "\\\\")
		return self.compiled.sub(replacement, text)


class SpeechDict(list):
	fileName: str | None = None

	def __repr__(self) -> str:
		return f"{self.__class__.__name__} ({len(self)} entries, fileName={self.fileName})"

	def load(self, fileName: str) -> None:
		self.fileName = fileName
		comment = ""
		self.clear()
		log.debug("Loading speech dictionary '%s'...", fileName)
		if not os.path.isfile(fileName):
			log.debug("file '%s' not found.", fileName)
			return
		with open(fileName, encoding="utf_8_sig", errors="replace") as file:
			for line in file:
				if line.isspace():
					comment = ""
					continue
				line = line.rstrip("\r\n")
				if line.startswith("#"):
					if comment:
						comment += " "
					comment += line[1:]
				else:
					temp = line.split("\t")
					if len(temp) == 4:
						pattern = temp[0].replace(r"\#", "#")
						replace = temp[1].replace(r"\#", "#")
						try:
							dictionaryEntry = SpeechDictEntry(
								pattern,
								replace,
								comment,
								caseSensitive=bool(int(temp[2])),
								type=int(temp[3]),
							)
							self.append(dictionaryEntry)
						except Exception:
							log.exception('Dictionary ("%s") entry invalid for "%s"', fileName, line)
						comment = ""
					else:
						log.warning("can't parse line '%s'", line)
			log.debug("%d loaded records.", len(self))

	def save(self, fileName: str | None = None):
		if not shouldWriteToDisk():
			log.debugWarning("Not writing dictionary, as shouldWriteToDisk returned False.")
			return
		if not fileName:
			fileName = getattr(self, "fileName", None)
		if not fileName:
			return
		dirName = os.path.dirname(fileName)
		if not os.path.isdir(dirName):
			os.makedirs(dirName)
		with open(fileName, "w", encoding="utf_8_sig", errors="replace") as file:
			for entry in self:
				if entry.comment:
					file.write(f"#{entry.comment}\r\n")
				file.write(
					"{}\t{}\t{}\t{}\r\n".format(
						entry.pattern.replace("#", r"\#"),
						entry.replacement.replace("#", r"\#"),
						int(entry.caseSensitive),
						entry.type,
					),
				)

	def sub(self, text: str) -> str:
		invalidEntries = []
		for index, entry in enumerate(self):
			try:
				text = entry.sub(text)
			except re.error as exc:
				dictName = self.fileName or "temporary dictionary"
				log.error(f'Invalid dictionary entry {index + 1} in {dictName}: "{entry.pattern}", {exc}')
				invalidEntries.append(index)
		for index in reversed(invalidEntries):
			del self[index]
		return text
