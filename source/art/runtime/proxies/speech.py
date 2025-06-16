# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU Lesser General Public License.
# See the file COPYING for more details.


from typing import Optional, Any, List
from dataclasses import dataclass


# Speech command classes that synths use
@dataclass
class IndexCommand:
	index: int
	
	def __repr__(self):
		return f"IndexCommand({self.index})"


@dataclass
class CharacterModeCommand:
	state: bool
	
	def __repr__(self):
		return f"CharacterModeCommand({self.state})"


@dataclass
class BreakCommand:
	time: Optional[int] = None
	
	def __repr__(self):
		return f"BreakCommand({self.time})"


@dataclass
class LangChangeCommand:
	lang: Optional[str]
	
	def __repr__(self):
		return f"LangChangeCommand({self.lang!r})"


@dataclass
class PitchCommand:
	offset: int = 0
	
	def __repr__(self):
		return f"PitchCommand({self.offset})"


@dataclass
class RateCommand:
	offset: int = 0
	
	def __repr__(self):
		return f"RateCommand({self.offset})"


@dataclass
class VolumeCommand:
	offset: int = 0
	
	def __repr__(self):
		return f"VolumeCommand({self.offset})"


@dataclass
class PhonemeCommand:
	phoneme: str
	
	def __repr__(self):
		return f"PhonemeCommand({self.phoneme!r})"


class SpeechPriority:
	FIRST = -2
	BEFORE = -1
	NORMAL = 0
	NEXT = 1
	NOW = 2
	NOW_BEEP = 3


# For backwards compatibility
Spri = SpeechPriority


SpeechSequence = List[Any]


class commands:
	IndexCommand = IndexCommand
	CharacterModeCommand = CharacterModeCommand
	BreakCommand = BreakCommand
	LangChangeCommand = LangChangeCommand
	PitchCommand = PitchCommand
	RateCommand = RateCommand
	VolumeCommand = VolumeCommand
	PhonemeCommand = PhonemeCommand


class types:
	SpeechSequence = SpeechSequence


synthIndexReached = "synthIndexReached"
synthDoneSpeaking = "synthDoneSpeaking"
