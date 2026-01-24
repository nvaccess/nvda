# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2026 NV Access Limited, Aleksey Sadovoy, Peter Vagner, Aaron Cannon, Leonard de Ruijter, Cyrille Bougot
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Types used for the speech dictionary system."""

import fnmatch
import os
import re
from dataclasses import dataclass, field
from functools import cached_property
from typing import Self

from logHandler import log
from NVDAState import shouldWriteToDisk
from utils.displayString import DisplayStringIntEnum, DisplayStringStrEnum


class EntryType(DisplayStringIntEnum):
	"""Types of speech dictionary entries:"""

	ANYWHERE = 0
	"""String can match anywhere"""
	REGEXP = 1
	"""Regular expression"""
	WORD = 2
	"""String must have word boundaries on both sides to match"""
	PART_OF_WORD = 3
	"""String must be preseeded or followed by an alphanumeric character to match."""
	START_OF_WORD = 4
	"""String must have a word boundary at the start and an alphanumeric character at the end."""
	END_OF_WORD = 5
	"""String must have an alphanumeric character at the start and a word boundary at the end."""
	UNIX = 6
	"""Unix shell-style wildcards."""

	@cached_property
	def _displayStringLabels(self) -> dict[Self, str]:
		return {
			# Translators: This is a label for an Entry Type radio button in add dictionary entry dialog.
			EntryType.ANYWHERE: _("&Anywhere"),
			# Translators: This is a label for an Entry Type radio button in add dictionary entry dialog.
			EntryType.REGEXP: _("Regular &expression"),
			# Translators: This is a label for an Entry Type radio button in add dictionary entry dialog.
			EntryType.WORD: _("Whole &word"),
			# Translators: This is a label for an Entry Type radio button in add dictionary entry dialog.
			EntryType.PART_OF_WORD: _("&Part of word"),
			# Translators: This is a label for an Entry Type radio button in add dictionary entry dialog.
			EntryType.START_OF_WORD: _("&Start of word"),
			# Translators: This is a label for an Entry Type radio button in add dictionary entry dialog.
			EntryType.END_OF_WORD: _("E&nd of word"),
			# Translators: This is a label for an Entry Type radio button in add dictionary entry dialog.
			EntryType.UNIX: _("&Unix shell-style wildcards"),
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
		match self.type:
			case EntryType.REGEXP:
				tempPattern = self.pattern
			case EntryType.WORD:
				tempPattern = rf"\b{re.escape(self.pattern)}\b"
			case EntryType.PART_OF_WORD:
				escaped = re.escape(self.pattern)
				tempPattern = rf"(?<=\w){escaped}|{escaped}(?=\w)"
			case EntryType.START_OF_WORD:
				tempPattern = rf"\b{re.escape(self.pattern)}(?=\w)"
			case EntryType.END_OF_WORD:
				tempPattern = rf"(?<=\w){re.escape(self.pattern)}\b"
			case EntryType.UNIX:
				tempPattern = fnmatch.translate(self.pattern)
			case _:
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


class SpeechDict(list[SpeechDictEntry]):
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
								type=EntryType(int(temp[3])),
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
				pattern = entry.pattern.replace("#", r"\#")
				replacement = entry.replacement.replace("#", r"\#")
				file.write(f"{pattern}\t{replacement}\t{entry.caseSensitive:d}\t{entry.type:d}\r\n")

	def sub(self, text: str) -> str:
		invalidEntries = []
		for index, entry in enumerate(self):
			try:
				text = entry.sub(text)
			except re.error:
				dictName = self.fileName or DictionaryType.TEMP.value
				log.exception("Invalid dictionary entry %d in %r: %r", index + 1, dictName, entry.pattern)
				invalidEntries.append(index)
		for index in reversed(invalidEntries):
			del self[index]
		return text
