# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2026 NV Access Limited, Aleksey Sadovoy, Peter Vagner, Aaron Cannon, Leonard de Ruijter, Cyrille Bougot
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Types used for the speech dictionary system."""

import fnmatch
import os
import re
import typing
from dataclasses import dataclass, field
from functools import cached_property

import config
from logHandler import log
from NVDAState import WritePaths, shouldWriteToDisk
from utils.displayString import DisplayStringIntEnum, DisplayStringStrEnum

from . import dictFormatUpgrade

if typing.TYPE_CHECKING:
	import synthDriverHandler


class EntryType(DisplayStringIntEnum):
	"""Types of speech dictionary entries:"""

	ANYWHERE = 0
	"""String can match anywhere"""
	REGEXP = 1
	"""Regular expression"""
	WORD = 2
	"""String must have word boundaries on both sides to match"""
	PART_OF_WORD = 3
	"""String must be preceded or followed by a word character (letter, digit, or underscore) to match."""
	START_OF_WORD = 4
	"""String must have a word boundary at the start and a word character (letter, digit, or underscore) at the end."""
	END_OF_WORD = 5
	"""String must have a word character (letter, digit, or underscore) at the start and a word boundary at the end."""
	UNIX = 6
	"""Unix shell-style wildcards."""

	@cached_property
	def _displayStringLabels(self) -> dict[typing.Self, str]:
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
	def _displayStringLabels(self) -> dict[typing.Self, str]:
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
	comment: str = ""
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
				# fnmatch.translate appends \Z to the end of the pattern; discard that anchor.
				translated = fnmatch.translate(self.pattern)
				suffix = r"\Z"
				if translated.endswith(suffix):
					tempPattern = translated.removesuffix(suffix)
				else:
					tempPattern = translated
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

	def load(self, fileName: str, raiseOnError: bool = False) -> None:
		self.fileName = fileName
		comment = ""
		self.clear()
		log.debug("Loading speech dictionary %r...", fileName)
		if not os.path.isfile(fileName):
			msg = f"file {fileName!r} not found."
			if raiseOnError:
				raise FileNotFoundError(msg)
			log.debug(msg)
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
						except Exception as e:
							msg = f"Dictionary {fileName!r} entry invalid for {line!r}"
							if raiseOnError:
								raise ValueError(msg) from e
							log.exception(msg)
						comment = ""
					else:
						msg = f"can't parse line {line!r}"
						if raiseOnError:
							raise ValueError(msg)
						log.warning(msg)
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


@dataclass(frozen=True, kw_only=True)
class SpeechDictDefinition:
	"""An abstract class for a speech dictionary definition."""

	name: str
	"""The name of the dictionary."""

	path: str | None = None
	"""The path to the dictionary."""

	source: DictionaryType | str
	"""The source of the dictionary."""

	displayName: str | None = None
	"""The translatable name of the dictionary.
	When not provided, the dictionary can not be visible to the end user.
	"""

	mandatory: bool = False
	"""Whether this dictionary is mandatory.
	Mandatory dictionaries are always enabled."""

	_dictionary: SpeechDict = field(init=False, repr=False, compare=False, default_factory=SpeechDict)

	def __post_init__(self):
		if not self.displayName and not self.mandatory:
			raise ValueError("A non-mandatory dictionary without a display name is unsupported")
		if self.path:
			self._dictionary.load(self.path, raiseOnError=self.source not in DictionaryType)

	@property
	def readOnly(self) -> bool:
		"""Whether this dictionary is read-only."""
		return self.source not in DictionaryType

	@property
	def userVisible(self) -> bool:
		"""Whether this dictionary is visible to end users (i.e. in the GUI).
		Mandatory dictionaries are hidden.
		"""
		return not self.mandatory and bool(self.displayName)

	@property
	def enabled(self) -> bool:
		return self.mandatory or self.name in config.conf["speech"]["speechDictionaries"]

	def sub(self, text: str) -> str:
		"""Applies the dictionary to the given text.
		:param text: The text to apply the dictionary to.
		:return: The text after applying the dictionary.
		"""
		return self._dictionary.sub(text)


@dataclass(frozen=True, kw_only=True)
class VoiceSpeechDictDefinition(SpeechDictDefinition):
	source: DictionaryType = field(init=False, default=DictionaryType.VOICE)
	name: str = field(init=False, default=DictionaryType.VOICE.value)
	displayName: str = field(
		init=False,
		# Translators: Name of the voice-specific speech dictionary.
		default=_("Voice Dictionary"),
	)

	def load(self, synth: "synthDriverHandler.SynthDriver"):
		"""Loads appropriate dictionary for the given synthesizer.
		It handles the case when the synthesizer doesn't support the voice setting.
		"""
		try:
			dictFormatUpgrade.doAnyUpgrades(synth)
		except Exception:
			log.exception("error trying to upgrade dictionaries")
		if synth.isSupported("voice"):
			voice = synth.availableVoices[synth.voice].displayName
			baseName = dictFormatUpgrade.createVoiceDictFileName(synth.name, voice)
		else:
			baseName = f"{synth.name}.dic"
		object.__setattr__(self, "path", os.path.join(WritePaths.voiceDictsDir, synth.name, baseName))
		self.__post_init__()
