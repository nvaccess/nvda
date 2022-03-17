# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2006-2021 NV Access Limited, Peter Vágner, Aleksey Sadovoy, Babbage B.V., Bill Dengler,
# Julien Cochuyt

"""High-level functions to speak information.
""" 

import itertools
import typing
import weakref
import unicodedata
import time
import colors
import api
import controlTypes
from controlTypes import OutputReason, TextPosition
import tones
from synthDriverHandler import getSynth
import re
import textInfos
import speechDictHandler
import characterProcessing
import languageHandler
from . import manager
from .commands import (
	# Commands that are used in this file.
	SpeechCommand,
	PitchCommand,
	LangChangeCommand,
	BeepCommand,
	EndUtteranceCommand,
	CharacterModeCommand,
)

from . import types
from .types import (
	SpeechSequence,
	SequenceItemT,
	logBadSequenceTypes,
	GeneratorWithReturn,
	_flattenNestedSequences
)
from typing import (
	Iterable,
	Optional,
	Dict,
	List,
	Any,
	Generator,
	Union,
	Tuple,
)
from logHandler import log
import config
import aria
from .priorities import Spri
from enum import IntEnum
from dataclasses import dataclass
from copy import copy

if typing.TYPE_CHECKING:
	import NVDAObjects

_speechState: Optional['SpeechState'] = None
_curWordChars: List[str] = []


class SpeechMode(IntEnum):
	off = 0
	beeps = 1
	talk = 2


@dataclass
class SpeechState:
	beenCanceled = True
	isPaused = False
	#: How speech should be handled; one of SpeechMode.off, SpeechMode.beeps or SpeechMode.talk.
	speechMode: SpeechMode = SpeechMode.talk
	# Length of the beep tone when speech mode is beeps
	speechMode_beeps_ms = 15
	#: The number of typed characters for which to suppress speech.
	_suppressSpeakTypedCharactersNumber = 0
	#: The time at which suppressed typed characters were sent.
	_suppressSpeakTypedCharactersTime: Optional[float] = None
	# Property values that are kept from getPropertiesSpeech
	oldTreeLevel = None
	oldTableID = None
	oldRowNumber = None
	oldRowSpan = None
	oldColumnNumber = None
	oldColumnSpan = None


def getState():
	return copy(_speechState)


def setSpeechMode(newMode: SpeechMode):
	_speechState.speechMode = newMode


def initialize():
	global _speechState
	_speechState = SpeechState()


#Set containing locale codes for languages supporting conjunct characters
LANGS_WITH_CONJUNCT_CHARS = {'hi', 'as', 'bn', 'gu', 'kn', 'kok', 'ml', 'mni', 'mr', 'pa', 'te', 'ur', 'ta'}

#: The string used to separate distinct chunks of text when multiple chunks should be spoken without pauses.
# #555: Use two spaces so that numbers from adjacent chunks aren't treated as a single number
# for languages such as French and German which use space as a thousands separator.
CHUNK_SEPARATOR = "  "


#: If a chunk of text contains only these characters, it will be considered blank.
BLANK_CHUNK_CHARS = frozenset((" ", "\n", "\r", "\0", u"\xa0"))
def isBlank(text):
	"""Determine whether text should be reported as blank.
	@param text: The text in question.
	@type text: str
	@return: C{True} if the text is blank, C{False} if not.
	@rtype: bool
	"""
	return not text or set(text) <= BLANK_CHUNK_CHARS

RE_CONVERT_WHITESPACE = re.compile("[\0\r\n]")

def processText(locale,text,symbolLevel):
	text = speechDictHandler.processText(text)
	text = characterProcessing.processSpeechSymbols(locale, text, symbolLevel)
	text = RE_CONVERT_WHITESPACE.sub(u" ", text)
	return text.strip()

def cancelSpeech():
	"""Interupts the synthesizer from currently speaking"""
	# Import only for this function to avoid circular import.
	from .sayAll import SayAllHandler
	SayAllHandler.stop()
	if _speechState.beenCanceled:
		return
	elif _speechState.speechMode == SpeechMode.off:
		return
	elif _speechState.speechMode == SpeechMode.beeps:
		return
	_manager.cancel()
	_speechState.beenCanceled = True
	_speechState.isPaused = False

def pauseSpeech(switch):
	getSynth().pause(switch)
	_speechState.isPaused = switch
	_speechState.beenCanceled = False


def _getSpeakMessageSpeech(
		text: str,
) -> SpeechSequence:
	"""Gets the speech sequence for a given message.
	@param text: the message to speak
	"""
	if text is None:
		return []
	if isBlank(text):
		return [
			# Translators: This is spoken when the line is considered blank.
			_("blank"),
		]
	return [text, ]


def speakMessage(
		text: str,
		priority: Optional[Spri] = None
) -> None:
	"""Speaks a given message.
	@param text: the message to speak
	@param priority: The speech priority.
	"""
	seq = _getSpeakMessageSpeech(text)
	if seq:
		speak(seq, symbolLevel=None, priority=priority)


def getCurrentLanguage() -> str:
	synth = getSynth()
	language=None
	if  synth:
		try:
			language=synth.language if config.conf['speech']['trustVoiceLanguage'] else None
		except NotImplementedError:
			pass
	if language:
		language=languageHandler.normalizeLanguage(language)
	if not language:
		language=languageHandler.getLanguage()
	return language


def spellTextInfo(
		info: textInfos.TextInfo,
		useCharacterDescriptions: bool = False,
		priority: Optional[Spri] = None
) -> None:
	"""Spells the text from the given TextInfo, honouring any LangChangeCommand objects it finds if autoLanguageSwitching is enabled."""
	if not config.conf['speech']['autoLanguageSwitching']:
		speakSpelling(info.text,useCharacterDescriptions=useCharacterDescriptions)
		return
	curLanguage=None
	for field in info.getTextWithFields({}):
		if isinstance(field,str):
			speakSpelling(field,curLanguage,useCharacterDescriptions=useCharacterDescriptions,priority=priority)
		elif isinstance(field,textInfos.FieldCommand) and field.command=="formatChange":
			curLanguage=field.field.get('language')


def speakSpelling(
		text: str,
		locale: Optional[str] = None,
		useCharacterDescriptions: bool = False,
		priority: Optional[Spri] = None
) -> None:
	# This could be a very large list. In future we could convert this into chunks.
	seq = list(getSpellingSpeech(
		text,
		locale=locale,
		useCharacterDescriptions=useCharacterDescriptions
	))
	speak(seq, priority=priority)


def _getSpellingSpeechAddCharMode(
		seq: Generator[SequenceItemT, None, None],
) -> Generator[SequenceItemT, None, None]:
	"""Inserts CharacterMode commands in a speech sequence generator to ensure any single character
	is spelt by the synthesizer.
	@param seq: The speech sequence to be spelt.
	"""
	charMode = False
	for item in seq:
		if isinstance(item, str):
			if len(item) == 1:
				if not charMode:
					yield CharacterModeCommand(True)
					charMode = True
			elif charMode:
				yield CharacterModeCommand(False)
				charMode = False
		yield item


def _getSpellingCharAddCapNotification(
		speakCharAs: str,
		sayCapForCapitals: bool,
		capPitchChange: int,
		beepForCapitals: bool,
) -> Generator[SequenceItemT, None, None]:
	"""This function produces a speech sequence containing a character to be spelt as well as commands
	to indicate that this character is uppercase if applicable.
	@param speakCharAs: The character as it will be spoken by the synthesizer.
	@param sayCapForCapitals: indicates if 'cap' should be reported along with the currently spelt character.
	@param capPitchChange: pitch offset to apply while spelling the currently spelt character.
	@param beepForCapitals: indicates if a cap notification beep should be produced while spelling the currently
	spellt character.
	"""
	if sayCapForCapitals:
		# Translators: cap will be spoken before the given letter when it is capitalized.
		capMsg = _("cap %s")
		(capMsgBefore, capMsgAfter) = capMsg.split('%s')
	else:
		capMsgBefore = ''
		capMsgAfter = ''
	
	if capPitchChange:
		yield PitchCommand(offset=capPitchChange)
	if beepForCapitals:
		yield BeepCommand(2000, 50)
	if capMsgBefore:
		yield capMsgBefore
	yield speakCharAs
	if capMsgAfter:
		yield capMsgAfter
	if capPitchChange:
		yield PitchCommand()


def _getSpellingSpeechWithoutCharMode(
		text: str,
		locale: str,
		useCharacterDescriptions: bool,
		sayCapForCapitals: bool,
		capPitchChange: int,
		beepForCapitals: bool,
) -> Generator[SequenceItemT, None, None]:
	
	defaultLanguage=getCurrentLanguage()
	if not locale or (not config.conf['speech']['autoDialectSwitching'] and locale.split('_')[0]==defaultLanguage.split('_')[0]):
		locale=defaultLanguage

	if not text:
		# Translators: This is spoken when NVDA moves to an empty line.
		yield _("blank")
		return
	if not text.isspace():
		text=text.rstrip()

	textLength=len(text)
	count = 0
	localeHasConjuncts = True if locale.split('_',1)[0] in LANGS_WITH_CONJUNCT_CHARS else False
	charDescList = getCharDescListFromText(text,locale) if localeHasConjuncts else text
	for item in charDescList:
		if localeHasConjuncts:
			# item is a tuple containing character and its description
			speakCharAs = item[0]
			charDesc = item[1]
		else:
			# item is just a character.
			speakCharAs = item
			if useCharacterDescriptions:
				charDesc=characterProcessing.getCharacterDescription(locale,speakCharAs.lower())
		uppercase=speakCharAs.isupper()
		if useCharacterDescriptions and charDesc:
			IDEOGRAPHIC_COMMA = u"\u3001"
			speakCharAs=charDesc[0] if textLength>1 else IDEOGRAPHIC_COMMA.join(charDesc)
		else:
			speakCharAs=characterProcessing.processSpeechSymbol(locale,speakCharAs)
		if config.conf['speech']['autoLanguageSwitching']:
			yield LangChangeCommand(locale)
		yield from _getSpellingCharAddCapNotification(
			speakCharAs,
			uppercase and sayCapForCapitals,
			capPitchChange if uppercase else 0,
			uppercase and beepForCapitals,
		)
		yield EndUtteranceCommand()


def getSpellingSpeech(
		text: str,
		locale: Optional[str] = None,
		useCharacterDescriptions: bool = False
) -> Generator[SequenceItemT, None, None]:
	
	synth = getSynth()
	synthConfig = config.conf["speech"][synth.name]
	
	if synth.isSupported("pitch"):
		capPitchChange = synthConfig["capPitchChange"]
	else:
		capPitchChange = 0
	seq = _getSpellingSpeechWithoutCharMode(
		text,
		locale,
		useCharacterDescriptions,
		sayCapForCapitals=synthConfig["sayCapForCapitals"],
		capPitchChange=capPitchChange,
		beepForCapitals=synthConfig["beepForCapitals"],
	)
	if synthConfig["useSpellingFunctionality"]:
		seq = _getSpellingSpeechAddCharMode(seq)
	yield from seq


def getCharDescListFromText(text,locale):
	"""This method prepares a list, which contains character and its description for all characters the text is made up of, by checking the presence of character descriptions in characterDescriptions.dic of that locale for all possible combination of consecutive characters in the text.
	This is done to take care of conjunct characters present in several languages such as Hindi, Urdu, etc.
	"""
	charDescList = []
	charDesc=None
	i = len(text)
	while i:
		subText = text[:i]
		charDesc = characterProcessing.getCharacterDescription(locale,subText)
		if charDesc or i==1:
			if not charDesc:
				# #5375: We're down to a single character (i == 1) and we don't have a description.
				# Try converting to lower case.
				# This provides for upper case English characters (which only have lower case descriptions).
				charDesc = characterProcessing.getCharacterDescription(locale,subText.lower())
			charDescList.append((subText,charDesc))
			text = text[i:]
			i = len(text)
		else:
			i = i - 1
	return charDescList


def speakObjectProperties(
		obj,
		reason: OutputReason = OutputReason.QUERY,
		_prefixSpeechCommand: Optional[SpeechCommand] = None,
		priority: Optional[Spri] = None,
		**allowedProperties
):
	speechSequence = getObjectPropertiesSpeech(
		obj,
		reason,
		_prefixSpeechCommand,
		**allowedProperties,
	)
	if speechSequence:
		speak(speechSequence, priority=priority)


# C901 'getObjectPropertiesSpeech' is too complex
# Note: when working on getObjectPropertiesSpeech, look for opportunities to simplify
# and move logic out into smaller helper functions.
def getObjectPropertiesSpeech(  # noqa: C901
		obj: "NVDAObjects.NVDAObject",
		reason: OutputReason = OutputReason.QUERY,
		_prefixSpeechCommand: Optional[SpeechCommand] = None,
		**allowedProperties
) -> SpeechSequence:
	#Fetch the values for all wanted properties
	newPropertyValues={}
	positionInfo=None
	for name,value in allowedProperties.items():
		if name=="includeTableCellCoords":
			# This is verbosity info.
			newPropertyValues[name]=value
		elif name.startswith('positionInfo_') and value:
			if positionInfo is None:
				positionInfo=obj.positionInfo
		elif value and name == "current":
			# getPropertiesSpeech names this "current", but the NVDAObject property is
			# named "isCurrent", it's type should always be controltypes.IsCurrent
			newPropertyValues['current'] = obj.isCurrent

		elif value and name == "hasDetails":
			newPropertyValues['hasDetails'] = obj.hasDetails
		elif value and name == "descriptionFrom" and (
			obj.descriptionFrom == controlTypes.DescriptionFrom.ARIA_DESCRIPTION
		):
			newPropertyValues['_description-from'] = obj.descriptionFrom
			newPropertyValues['description'] = obj.description
		elif value:
			# Certain properties such as row and column numbers have presentational versions, which should be used for speech if they are available.
			# Therefore redirect to those values first if they are available, falling back to the normal properties if not.
			names=[name]
			if name=='rowNumber':
				names.insert(0,'presentationalRowNumber')
			elif name=='columnNumber':
				names.insert(0,'presentationalColumnNumber')
			elif name=='rowCount':
				names.insert(0,'presentationalRowCount')
			elif name=='columnCount':
				names.insert(0,'presentationalColumnCount')
			for tryName in names:
				try:
					newPropertyValues[name]=getattr(obj,tryName)
				except NotImplementedError:
					continue
				break

	if (
		newPropertyValues.get("description")  # has a value
		and newPropertyValues.get("name") == newPropertyValues.get("description")  # value is equal to name
		and reason != controlTypes.OutputReason.CHANGE  # if the value has changed, report it.
	):
		del newPropertyValues['description']  # prevent duplicate speech due to description matching name

	if positionInfo:
		if allowedProperties.get('positionInfo_level',False) and 'level' in positionInfo:
			newPropertyValues['positionInfo_level']=positionInfo['level']
		if allowedProperties.get('positionInfo_indexInGroup',False) and 'indexInGroup' in positionInfo:
			newPropertyValues['positionInfo_indexInGroup']=positionInfo['indexInGroup']
		if allowedProperties.get('positionInfo_similarItemsInGroup',False) and 'similarItemsInGroup' in positionInfo:
			newPropertyValues['positionInfo_similarItemsInGroup']=positionInfo['similarItemsInGroup']
	#Fetched the cached properties and update them with the new ones
	oldCachedPropertyValues=getattr(obj,'_speakObjectPropertiesCache',{}).copy()
	cachedPropertyValues=oldCachedPropertyValues.copy()
	cachedPropertyValues.update(newPropertyValues)
	obj._speakObjectPropertiesCache=cachedPropertyValues
	#If we should only cache we can stop here
	if reason == OutputReason.ONLYCACHE:
		return []
	#If only speaking change, then filter out all values that havn't changed
	if reason == OutputReason.CHANGE:
		for name in set(newPropertyValues)&set(oldCachedPropertyValues):
			if newPropertyValues[name]==oldCachedPropertyValues[name]:
				del newPropertyValues[name]
			elif name=="states": #states need specific handling
				oldStates=oldCachedPropertyValues[name]
				newStates=newPropertyValues[name]
				newPropertyValues['states']=newStates-oldStates
				newPropertyValues['negativeStates']=oldStates-newStates

	# properties such as states or value need to know the role to speak properly,
	# give it as a _ name
	newPropertyValues['_role'] = newPropertyValues.get('role', obj.role)

	# The real states are needed also, as the states entry might be filtered.
	newPropertyValues['_states']=obj.states
	if "rowNumber" in newPropertyValues or "columnNumber" in newPropertyValues:
		# We're reporting table cell info, so pass the table ID.
		try:
			newPropertyValues["_tableID"]=obj.tableID
		except NotImplementedError:
			pass
	if allowedProperties.get('placeholder', False):
		newPropertyValues['placeholder']=obj.placeholder
	# When speaking an object due to a focus change, the 'selected' state should not be reported if only one item is selected.
	# This is because that one item will be the focused object, and saying selected is redundant.
	# Rather, 'unselected' will be spoken for an unselected object if 1 or more items are selected. 
	states=newPropertyValues.get('states')
	if states is not None and reason == OutputReason.FOCUS:
		if (
			controlTypes.State.SELECTABLE in states 
			and controlTypes.State.FOCUSABLE in states
			and controlTypes.State.SELECTED in states
			and obj.selectionContainer 
			and obj.selectionContainer.getSelectedItemsCount(2)==1
		):
			# We must copy the states set and  put it back in newPropertyValues otherwise mutating the original states set in-place will wrongly change the cached states.
			# This would then cause 'selected' to be announced as a change when any other state happens to change on this object in future.
			states=states.copy()
			states.discard(controlTypes.State.SELECTED)
			states.discard(controlTypes.State.SELECTABLE)
			newPropertyValues['states']=states
	#Get the speech text for the properties we want to speak, and then speak it
	speechSequence = getPropertiesSpeech(reason=reason, **newPropertyValues)

	if speechSequence:
		if _prefixSpeechCommand is not None:
			speechSequence.insert(0, _prefixSpeechCommand)
		from eventHandler import _getFocusLossCancellableSpeechCommand
		cancelCommand = _getFocusLossCancellableSpeechCommand(obj, reason)
		if cancelCommand is not None:
			speechSequence.append(cancelCommand)
	return speechSequence


def _getPlaceholderSpeechIfTextEmpty(
		obj,
		reason: OutputReason,
) -> Tuple[bool, SpeechSequence]:
	""" Attempt to get speech for placeholder attribute if text for 'obj' is empty. Don't report the placeholder
		value unless the text is empty, because it is confusing to hear the current value (presumably typed by the
		user) *and* the placeholder. The placeholder should "disappear" once the user types a value.
	@return: (True, SpeechSequence) if text for obj was considered empty and we attempted to get speech for the
		placeholder value. (False, []) if text for obj was not considered empty.
	"""
	textEmpty = obj._isTextEmpty
	if textEmpty:
		return True, getObjectPropertiesSpeech(obj, reason=reason, placeholder=True)
	return False, []


def speakObject(
		obj,
		reason: OutputReason = OutputReason.QUERY,
		_prefixSpeechCommand: Optional[SpeechCommand] = None,
		priority: Optional[Spri] = None
):
	sequence = getObjectSpeech(
		obj,
		reason,
		_prefixSpeechCommand,
	)
	if sequence:
		speak(sequence, priority=priority)




# C901 'getObjectSpeech' is too complex
# Note: when working on getObjectSpeech, look for opportunities to simplify
# and move logic out into smaller helper functions.
def getObjectSpeech(  # noqa: C901
		obj,
		reason: OutputReason = OutputReason.QUERY,
		_prefixSpeechCommand: Optional[SpeechCommand] = None,
):
	role=obj.role
	# Choose when we should report the content of this object's textInfo, rather than just the object's value
	import browseMode
	shouldReportTextContent=not (
		# focusEntered should never present text content
		(reason == OutputReason.FOCUSENTERED)
		# The rootNVDAObject of a browseMode document in browse mode (not passThrough)
		# should never present text content
		or (
			isinstance(obj.treeInterceptor, browseMode.BrowseModeDocumentTreeInterceptor)
			and not obj.treeInterceptor.passThrough
			and obj == obj.treeInterceptor.rootNVDAObject
		)
		# objects that do not report as having navigableText should not report their text content either
		or not obj._hasNavigableText
	)

	allowProperties = _objectSpeech_calculateAllowedProps(reason, shouldReportTextContent)

	if reason == OutputReason.FOCUSENTERED:
		# Aside from excluding some properties, focus entered should be spoken like focus.
		reason = OutputReason.FOCUS

	sequence = getObjectPropertiesSpeech(
		obj,
		reason=reason,
		_prefixSpeechCommand=_prefixSpeechCommand,
		**allowProperties
	)
	if reason == OutputReason.ONLYCACHE:
		return sequence
	if shouldReportTextContent:
		try:
			info = obj.makeTextInfo(textInfos.POSITION_SELECTION)
		except (NotImplementedError, RuntimeError):
			info = None
		if info and not info.isCollapsed:
			# if there is selected text, then there is a value and we do not report placeholder
			sequence.extend(getPreselectedTextSpeech(info.text))
		else:
			if not info:
				info = obj.makeTextInfo(textInfos.POSITION_FIRST)
			info.expand(textInfos.UNIT_LINE)
			textEmpty, placeholderSeq = _getPlaceholderSpeechIfTextEmpty(obj, reason)
			sequence.extend(placeholderSeq)
			speechGen = getTextInfoSpeech(
				info,
				unit=textInfos.UNIT_LINE,
				reason=OutputReason.CARET,
			)
			sequence.extend(_flattenNestedSequences(speechGen))
	elif role == controlTypes.Role.MATH:
		import mathPres
		if mathPres.speechProvider:
			try:
				sequence.extend(
					mathPres.speechProvider.getSpeechForMathMl(obj.mathMl)
				)
			except (NotImplementedError, LookupError):
				pass
	return sequence


def _objectSpeech_calculateAllowedProps(reason, shouldReportTextContent):
	allowProperties = {
		'name': True,
		'role': True,
		'roleText': True,
		'states': True,
		'value': True,
		'description': True,
		'hasDetails': config.conf["annotations"]["reportDetails"],
		'descriptionFrom': config.conf["annotations"]["reportAriaDescription"],
		'keyboardShortcut': True,
		'positionInfo_level': True,
		'positionInfo_indexInGroup': True,
		'positionInfo_similarItemsInGroup': True,
		"cellCoordsText": True,
		"rowNumber": True,
		"columnNumber": True,
		"includeTableCellCoords": True,
		"columnCount": True,
		"rowCount": True,
		"rowHeaderText": True,
		"columnHeaderText": True,
		"rowSpan": True,
		"columnSpan": True,
		"current": True
	}
	if reason == OutputReason.FOCUSENTERED:
		allowProperties["value"] = False
		allowProperties["keyboardShortcut"] = False
		allowProperties["positionInfo_level"] = False
	if not config.conf["presentation"]["reportObjectDescriptions"]:
		allowProperties["description"] = False
	if not config.conf["presentation"]["reportKeyboardShortcuts"]:
		allowProperties["keyboardShortcut"] = False
	if not config.conf["presentation"]["reportObjectPositionInformation"]:
		allowProperties["positionInfo_level"] = False
		allowProperties["positionInfo_indexInGroup"] = False
		allowProperties["positionInfo_similarItemsInGroup"] = False
	if reason != OutputReason.QUERY:
		allowProperties["rowCount"] = False
		allowProperties["columnCount"] = False
	formatConf = config.conf["documentFormatting"]
	if not formatConf["reportTableCellCoords"]:
		allowProperties["cellCoordsText"] = False
		# rowNumber and columnNumber might be needed even if we're not reporting coordinates.
		allowProperties["includeTableCellCoords"] = False
	if not formatConf["reportTableHeaders"]:
		allowProperties["rowHeaderText"] = False
		allowProperties["columnHeaderText"] = False
	if (
		not formatConf["reportTables"]
		or (
			not formatConf["reportTableCellCoords"]
			and not formatConf["reportTableHeaders"]
		)
	):
		# We definitely aren't reporting any table info at all.
		allowProperties["rowNumber"] = False
		allowProperties["columnNumber"] = False
		allowProperties["rowSpan"] = False
		allowProperties["columnSpan"] = False
	if shouldReportTextContent:
		allowProperties['value'] = False
	return allowProperties


def speakText(
		text: str,
		reason: OutputReason = OutputReason.MESSAGE,
		symbolLevel: Optional[int] = None,
		priority: Optional[Spri] = None
):
	"""Speaks some text.
	@param text: The text to speak.
	@param reason: Unused
	@param symbolLevel: The symbol verbosity level; C{None} (default) to use the user's configuration.
	@param priority: The speech priority.
	"""
	seq = _getSpeakMessageSpeech(text)
	if seq:
		speak(seq, symbolLevel=symbolLevel, priority=priority)


RE_INDENTATION_SPLIT = re.compile(r"^([^\S\r\n\f\v]*)(.*)$", re.UNICODE | re.DOTALL)


def splitTextIndentation(text):
	"""Splits indentation from the rest of the text.
	@param text: The text to split.
	@type text: str
	@return: Tuple of indentation and content.
	@rtype: (str, str)
	"""
	return RE_INDENTATION_SPLIT.match(text).groups()


RE_INDENTATION_CONVERT = re.compile(r"(?P<char>\s)(?P=char)*", re.UNICODE)
IDT_BASE_FREQUENCY = 220 #One octave below middle A.
IDT_TONE_DURATION = 80 #Milleseconds
IDT_MAX_SPACES = 72


def getIndentationSpeech(indentation: str, formatConfig: Dict[str, bool]) -> SpeechSequence:
	"""Retrieves the indentation speech sequence for a given string of indentation.
	@param indentation: The string of indentation.
	@param formatConfig: The configuration to use.
	"""
	speechIndentConfig = formatConfig["reportLineIndentation"]
	toneIndentConfig = (
		formatConfig["reportLineIndentationWithTones"]
		and _speechState.speechMode == SpeechMode.talk
	)
	indentSequence: SpeechSequence = []
	if not indentation:
		if toneIndentConfig:
			indentSequence.append(BeepCommand(IDT_BASE_FREQUENCY, IDT_TONE_DURATION))
		if speechIndentConfig:
			indentSequence.append(
				# Translators: This is spoken when the given line has no indentation.
				_("no indent")
			)
		return indentSequence

	#The non-breaking space is semantically a space, so we replace it here.
	indentation = indentation.replace(u"\xa0", u" ")
	res = []
	locale=languageHandler.getLanguage()
	quarterTones = 0
	for m in RE_INDENTATION_CONVERT.finditer(indentation):
		raw = m.group()
		symbol = characterProcessing.processSpeechSymbol(locale, raw[0])
		count = len(raw)
		if symbol == raw[0]:
			# There is no replacement for this character, so do nothing.
			res.append(raw)
		elif count == 1:
			res.append(symbol)
		else:
			res.append(u"{count} {symbol}".format(count=count, symbol=symbol))
		quarterTones += (count*4 if raw[0]== "\t" else count)

	speak = speechIndentConfig
	if toneIndentConfig: 
		if quarterTones <= IDT_MAX_SPACES:
			pitch = IDT_BASE_FREQUENCY*2**(quarterTones/24.0) #24 quarter tones per octave.
			indentSequence.append(BeepCommand(pitch, IDT_TONE_DURATION))
		else: 
			#we have more than 72 spaces (18 tabs), and must speak it since we don't want to hurt the users ears.
			speak = True
	if speak:
		indentSequence.extend(res)
	return indentSequence


# C901 'speak' is too complex
# Note: when working on speak, look for opportunities to simplify
# and move logic out into smaller helper functions.
def speak(  # noqa: C901
		speechSequence: SpeechSequence,
		symbolLevel: Optional[int] = None,
		priority: Spri = Spri.NORMAL
):
	"""Speaks a sequence of text and speech commands
	@param speechSequence: the sequence of text and L{SpeechCommand} objects to speak
	@param symbolLevel: The symbol verbosity level; C{None} (default) to use the user's configuration.
	@param priority: The speech priority.
	"""
	logBadSequenceTypes(speechSequence)
	# in case priority was explicitly passed in as None, set to default.
	priority: Spri = Spri.NORMAL if priority is None else priority

	if not speechSequence:  # Pointless - nothing to speak
		return
	import speechViewer
	if speechViewer.isActive:
		speechViewer.appendSpeechSequence(speechSequence)
	if _speechState.speechMode == SpeechMode.off:
		return
	elif _speechState.speechMode == SpeechMode.beeps:
		tones.beep(config.conf["speech"]["beepSpeechModePitch"], _speechState.speechMode_beeps_ms)
		return
	if _speechState.isPaused:
		cancelSpeech()
	_speechState.beenCanceled = False
	#Filter out redundant LangChangeCommand objects 
	#And also fill in default values
	autoLanguageSwitching=config.conf['speech']['autoLanguageSwitching']
	autoDialectSwitching=config.conf['speech']['autoDialectSwitching']
	curLanguage=defaultLanguage=getCurrentLanguage()
	prevLanguage=None
	defaultLanguageRoot=defaultLanguage.split('_')[0]
	oldSpeechSequence=speechSequence
	speechSequence=[]
	for item in oldSpeechSequence:
		if isinstance(item,LangChangeCommand):
			if not autoLanguageSwitching: continue
			curLanguage=item.lang
			if not curLanguage or (not autoDialectSwitching and curLanguage.split('_')[0]==defaultLanguageRoot):
				curLanguage=defaultLanguage
		elif isinstance(item,str):
			if not item: continue
			if autoLanguageSwitching and curLanguage!=prevLanguage:
				speechSequence.append(LangChangeCommand(curLanguage))
				prevLanguage=curLanguage
			speechSequence.append(item)
		else:
			speechSequence.append(item)
	if not speechSequence:
		# After normalisation, the sequence is empty.
		# There's nothing to speak.
		return
	import inputCore
	inputCore.logTimeSinceInput()
	log.io("Speaking %r" % speechSequence)
	if symbolLevel is None:
		symbolLevel=config.conf["speech"]["symbolLevel"]
	curLanguage=defaultLanguage
	inCharacterMode=False
	for index in range(len(speechSequence)):
		item=speechSequence[index]
		if isinstance(item,CharacterModeCommand):
			inCharacterMode=item.state
		if autoLanguageSwitching and isinstance(item,LangChangeCommand):
			curLanguage=item.lang
		if isinstance(item,str):
			speechSequence[index]=processText(curLanguage,item,symbolLevel)
			if not inCharacterMode:
				speechSequence[index]+=CHUNK_SEPARATOR
	_manager.speak(speechSequence, priority)


def speakPreselectedText(
		text: str,
		priority: Optional[Spri] = None
):
	""" Helper method to announce that a newly focused control already has
	text selected. This method is in contrast with L{speakTextSelected}.
	The method will speak the word "selected" with the provided text appended.
	The announcement order is different from L{speakTextSelected} in order to
	inform a user that the newly focused control has content that is selected,
	which they may unintentionally overwrite.

	@remarks: Implemented using L{getPreselectedTextSpeech}
	"""
	seq = getPreselectedTextSpeech(text)
	if seq:
		speak(seq, symbolLevel=None, priority=priority)


def getPreselectedTextSpeech(
		text: str
) -> SpeechSequence:
	""" Helper method to get the speech sequence to announce a newly focused control already has
	text selected.
	This method will speak the word "selected" with the provided text appended.
	The announcement order is different from L{speakTextSelected} in order to
	inform a user that the newly focused control has content that is selected,
	which they may unintentionally overwrite.

	@remarks: Implemented using L{_getSelectionMessageSpeech}, which allows for
		creating a speech sequence with an arbitrary attached message.
	"""
	return _getSelectionMessageSpeech(
		# Translators: This is spoken to indicate that some text is already selected.
		# 'selected' preceding text is intentional.
		# For example 'selected hello world'
		_("selected %s"),
		text
	)


def speakTextSelected(
		text: str,
		priority: Optional[Spri] = None
):
	""" Helper method to announce that the user has caused text to be selected.
	This method is in contrast with L{speakPreselectedText}.
	The method will speak the provided text with the word "selected" appended.

	@remarks: Implemented using L{speakSelectionMessage}, which allows for
		speaking text with an arbitrary attached message.
	"""
	# Translators: This is spoken to indicate what has just been selected.
	# The text preceding 'selected' is intentional.
	# For example 'hello world selected'
	speakSelectionMessage(_("%s selected"), text, priority)


def speakSelectionMessage(
		message: str,
		text: str,
		priority: Optional[Spri] = None
):
	seq = _getSelectionMessageSpeech(message, text)
	if seq:
		speak(seq, symbolLevel=None, priority=priority)


def _getSelectionMessageSpeech(
		message: str,
		text: str,
) -> SpeechSequence:
	if len(text) < 512:
		return _getSpeakMessageSpeech(message % text)
	# Translators: This is spoken when the user has selected a large portion of text.
	# Example output "1000 characters"
	numCharactersText = _("%d characters") % len(text)
	return _getSpeakMessageSpeech(message % numCharactersText)

# C901 'speakSelectionChange' is too complex
# Note: when working on speakSelectionChange, look for opportunities to simplify
# and move logic out into smaller helper functions.
def speakSelectionChange(  # noqa: C901
		oldInfo: textInfos.TextInfo,
		newInfo: textInfos.TextInfo,
		speakSelected: bool = True,
		speakUnselected: bool = True,
		generalize: bool = False,
		priority: Optional[Spri] = None
):
	"""Speaks a change in selection, either selected or unselected text.
	@param oldInfo: a TextInfo instance representing what the selection was before
	@param newInfo: a TextInfo instance representing what the selection is now
	@param generalize: if True, then this function knows that the text may have changed between the creation of the oldInfo and newInfo objects, meaning that changes need to be spoken more generally, rather than speaking the specific text, as the bounds may be all wrong.
	@param priority: The speech priority.
	"""
	selectedTextList=[]
	unselectedTextList=[]
	if newInfo.isCollapsed and oldInfo.isCollapsed:
		return
	startToStart=newInfo.compareEndPoints(oldInfo,"startToStart")
	startToEnd=newInfo.compareEndPoints(oldInfo,"startToEnd")
	endToStart=newInfo.compareEndPoints(oldInfo,"endToStart")
	endToEnd=newInfo.compareEndPoints(oldInfo,"endToEnd")
	if speakSelected and oldInfo.isCollapsed:
		selectedTextList.append(newInfo.text)
	elif speakUnselected and newInfo.isCollapsed:
		unselectedTextList.append(oldInfo.text)
	else:
		if startToEnd>0 or endToStart<0:
			if speakSelected and not newInfo.isCollapsed:
				selectedTextList.append(newInfo.text)
			if speakUnselected and not oldInfo.isCollapsed:
				unselectedTextList.append(oldInfo.text)
		else:
			if speakSelected and startToStart<0 and not newInfo.isCollapsed:
				tempInfo=newInfo.copy()
				tempInfo.setEndPoint(oldInfo,"endToStart")
				selectedTextList.append(tempInfo.text)
			if speakSelected and endToEnd>0 and not newInfo.isCollapsed:
				tempInfo=newInfo.copy()
				tempInfo.setEndPoint(oldInfo,"startToEnd")
				selectedTextList.append(tempInfo.text)
			if startToStart>0 and not oldInfo.isCollapsed:
				tempInfo=oldInfo.copy()
				tempInfo.setEndPoint(newInfo,"endToStart")
				unselectedTextList.append(tempInfo.text)
			if endToEnd<0 and not oldInfo.isCollapsed:
				tempInfo=oldInfo.copy()
				tempInfo.setEndPoint(newInfo,"startToEnd")
				unselectedTextList.append(tempInfo.text)
	locale=getCurrentLanguage()
	if speakSelected:
		if not generalize:
			for text in selectedTextList:
				if  len(text)==1:
					text=characterProcessing.processSpeechSymbol(locale,text)
				speakTextSelected(text, priority=priority)
		elif len(selectedTextList)>0:
			text=newInfo.text
			if len(text)==1:
				text=characterProcessing.processSpeechSymbol(locale,text)
			speakTextSelected(text, priority=priority)
	if speakUnselected:
		if not generalize:
			for text in unselectedTextList:
				if  len(text)==1:
					text=characterProcessing.processSpeechSymbol(locale,text)
				# Translators: This is spoken to indicate what has been unselected. for example 'hello unselected'
				speakSelectionMessage(_("%s unselected"),text,priority=priority)
		elif len(unselectedTextList)>0:
			if not newInfo.isCollapsed:
				text=newInfo.text
				if len(text)==1:
					text=characterProcessing.processSpeechSymbol(locale,text)
				# Translators: This is spoken to indicate when the previous selection was removed and a new selection was made. for example 'hello world selected instead'
				speakSelectionMessage(_("%s selected instead"),text,priority=priority)
			else:
				# Translators: Reported when selection is removed.
				speakMessage(_("selection removed"),priority=priority)


def _suppressSpeakTypedCharacters(number: int):
	"""Suppress speaking of typed characters.
	This should be used when sending a string of characters to the system
	and those characters should not be spoken individually as if the user were typing them.
	@param number: The number of characters to suppress.
	"""
	_speechState._suppressSpeakTypedCharactersNumber += number
	_speechState._suppressSpeakTypedCharactersTime = time.time()


#: The character to use when masking characters in protected fields.
PROTECTED_CHAR = "*"
#: The first character which is not a Unicode control character.
#: This is used to test whether a character should be spoken as a typed character;
#: i.e. it should have a visual or spatial representation.
FIRST_NONCONTROL_CHAR = u" "


def speakTypedCharacters(ch: str):
	typingIsProtected=api.isTypingProtected()
	if typingIsProtected:
		realChar=PROTECTED_CHAR
	else:
		realChar=ch
	if unicodedata.category(ch)[0] in "LMN":
		_curWordChars.append(realChar)
	elif ch=="\b":
		# Backspace, so remove the last character from our buffer.
		del _curWordChars[-1:]
	elif ch==u'\u007f':
		# delete character produced in some apps with control+backspace
		return
	elif len(_curWordChars) > 0:
		typedWord = "".join(_curWordChars)
		clearTypedWordBuffer()
		if log.isEnabledFor(log.IO):
			log.io("typed word: %s"%typedWord)
		if config.conf["keyboard"]["speakTypedWords"] and not typingIsProtected:
			speakText(typedWord)
	if _speechState._suppressSpeakTypedCharactersNumber > 0:
		# We primarily suppress based on character count and still have characters to suppress.
		# However, we time out after a short while just in case.
		suppress = time.time() - _speechState._suppressSpeakTypedCharactersTime <= 0.1
		if suppress:
			_speechState._suppressSpeakTypedCharactersNumber -= 1
		else:
			_speechState._suppressSpeakTypedCharactersNumber = 0
			_speechState._suppressSpeakTypedCharactersTime = None
	else:
		suppress = False
	if not suppress and config.conf["keyboard"]["speakTypedCharacters"] and ch >= FIRST_NONCONTROL_CHAR:
		speakSpelling(realChar)


class SpeakTextInfoState(object):
	"""Caches the state of speakTextInfo such as the current controlField stack, current formatfield and indentation."""

	__slots__=[
		'objRef',
		'controlFieldStackCache',
		'formatFieldAttributesCache',
		'indentationCache',
	]

	def __init__(self,obj):
		if isinstance(obj,SpeakTextInfoState):
			oldState=obj
			self.objRef=oldState.objRef
		else:
			self.objRef=weakref.ref(obj)
			oldState=getattr(obj,'_speakTextInfoState',None)
		self.controlFieldStackCache=list(oldState.controlFieldStackCache) if oldState else []
		self.formatFieldAttributesCache=oldState.formatFieldAttributesCache if oldState else {}
		self.indentationCache=oldState.indentationCache if oldState else ""

	def updateObj(self):
		obj=self.objRef()
		if obj:
			obj._speakTextInfoState=self.copy()

	def copy(self):
		return self.__class__(self)


def _extendSpeechSequence_addMathForTextInfo(
		speechSequence: SpeechSequence, info: textInfos.TextInfo, field: textInfos.Field
) -> None:
	import mathPres
	if not mathPres.speechProvider:
		return
	try:
		speechSequence.extend(mathPres.speechProvider.getSpeechForMathMl(info.getMathMl(field)))
	except (NotImplementedError, LookupError):
		return


def speakTextInfo(
		info: textInfos.TextInfo,
		useCache: Union[bool, SpeakTextInfoState] = True,
		formatConfig: Dict[str, bool] = None,
		unit: Optional[str] = None,
		reason: OutputReason = OutputReason.QUERY,
		_prefixSpeechCommand: Optional[SpeechCommand] = None,
		onlyInitialFields: bool = False,
		suppressBlanks: bool = False,
		priority: Optional[Spri] = None
) -> bool:
	speechGen = getTextInfoSpeech(
		info,
		useCache,
		formatConfig,
		unit,
		reason,
		_prefixSpeechCommand,
		onlyInitialFields,
		suppressBlanks
	)

	speechGen = GeneratorWithReturn(speechGen)
	for seq in speechGen:
		speak(seq, priority=priority)
	return speechGen.returnValue


# C901 'getTextInfoSpeech' is too complex
# Note: when working on getTextInfoSpeech, look for opportunities to simplify
# and move logic out into smaller helper functions.
def getTextInfoSpeech(  # noqa: C901
		info: textInfos.TextInfo,
		useCache: Union[bool, SpeakTextInfoState] = True,
		formatConfig: Dict[str, bool] = None,
		unit: Optional[str] = None,
		reason: OutputReason = OutputReason.QUERY,
		_prefixSpeechCommand: Optional[SpeechCommand] = None,
		onlyInitialFields: bool = False,
		suppressBlanks: bool = False
) -> Generator[SpeechSequence, None, bool]:
	onlyCache = reason == OutputReason.ONLYCACHE
	if isinstance(useCache,SpeakTextInfoState):
		speakTextInfoState=useCache
	elif useCache:
		speakTextInfoState=SpeakTextInfoState(info.obj)
	else:
		speakTextInfoState=None
	autoLanguageSwitching=config.conf['speech']['autoLanguageSwitching']
	extraDetail=unit in (textInfos.UNIT_CHARACTER,textInfos.UNIT_WORD)
	if not formatConfig:
		formatConfig=config.conf["documentFormatting"]
	formatConfig=formatConfig.copy()
	if extraDetail:
		formatConfig['extraDetail']=True
	reportIndentation=unit==textInfos.UNIT_LINE and ( formatConfig["reportLineIndentation"] or formatConfig["reportLineIndentationWithTones"])
	# For performance reasons, when navigating by paragraph or table cell, spelling errors will not be announced.
	if unit in (textInfos.UNIT_PARAGRAPH, textInfos.UNIT_CELL) and reason == OutputReason.CARET:
		formatConfig['reportSpellingErrors']=False

	#Fetch the last controlFieldStack, or make a blank one
	controlFieldStackCache=speakTextInfoState.controlFieldStackCache if speakTextInfoState else []
	formatFieldAttributesCache=speakTextInfoState.formatFieldAttributesCache if speakTextInfoState else {}
	textWithFields=info.getTextWithFields(formatConfig)
	# We don't care about node bounds, especially when comparing fields.
	# Remove them.
	for command in textWithFields:
		if not isinstance(command,textInfos.FieldCommand):
			continue
		field=command.field
		if not field:
			continue
		try:
			del field["_startOfNode"]
		except KeyError:
			pass
		try:
			del field["_endOfNode"]
		except KeyError:
			pass

	#Make a new controlFieldStack and formatField from the textInfo's initialFields
	newControlFieldStack=[]
	newFormatField=textInfos.FormatField()
	initialFields=[]
	for field in textWithFields:
		if isinstance(field,textInfos.FieldCommand) and field.command in ("controlStart","formatChange"):
			initialFields.append(field.field)
		else:
			break
	if len(initialFields)>0:
		del textWithFields[0:len(initialFields)]
	endFieldCount=0
	for field in reversed(textWithFields):
		if isinstance(field,textInfos.FieldCommand) and field.command=="controlEnd":
			endFieldCount+=1
		else:
			break
	if endFieldCount>0:
		del textWithFields[0-endFieldCount:]
	for field in initialFields:
		if isinstance(field,textInfos.ControlField):
			newControlFieldStack.append(field)
		elif isinstance(field,textInfos.FormatField):
			newFormatField.update(field)
		else:
			raise ValueError("unknown field: %s"%field)
	#Calculate how many fields in the old and new controlFieldStacks are the same
	commonFieldCount=0
	for count in range(min(len(newControlFieldStack),len(controlFieldStackCache))):
		# #2199: When comparing controlFields try using uniqueID if it exists before resorting to compairing the entire dictionary
		oldUniqueID=controlFieldStackCache[count].get('uniqueID')
		newUniqueID=newControlFieldStack[count].get('uniqueID')
		if ((oldUniqueID is not None or newUniqueID is not None) and newUniqueID==oldUniqueID) or (newControlFieldStack[count]==controlFieldStackCache[count]):
			commonFieldCount+=1
		else:
			break

	speechSequence: SpeechSequence = []
	# #2591: Only if the reason is not focus, Speak the exit of any controlFields not in the new stack.
	# We don't do this for focus because hearing "out of list", etc. isn't useful when tabbing or using quick navigation and makes navigation less efficient.
	if reason not in [OutputReason.FOCUS, OutputReason.QUICKNAV]:
		endingBlock=False
		for count in reversed(range(commonFieldCount,len(controlFieldStackCache))):
			fieldSequence = info.getControlFieldSpeech(
				controlFieldStackCache[count],
				controlFieldStackCache[0:count],
				"end_removedFromControlFieldStack",
				formatConfig,
				extraDetail,
				reason=reason
			)
			if fieldSequence:
				speechSequence.extend(fieldSequence)
			if not endingBlock and reason == OutputReason.SAYALL:
				endingBlock=bool(int(controlFieldStackCache[count].get('isBlock',0)))
		if endingBlock:
			speechSequence.append(EndUtteranceCommand())
	# The TextInfo should be considered blank if we are only exiting fields (i.e. we aren't
	# entering any new fields and there is no text).
	shouldConsiderTextInfoBlank = True

	if _prefixSpeechCommand is not None:
		assert isinstance(_prefixSpeechCommand, SpeechCommand)
		speechSequence.append(_prefixSpeechCommand)

	#Get speech text for any fields that are in both controlFieldStacks, if extra detail is not requested
	if not extraDetail:
		for count in range(commonFieldCount):
			field=newControlFieldStack[count]
			fieldSequence = info.getControlFieldSpeech(
				field,
				newControlFieldStack[0:count],
				"start_inControlFieldStack",
				formatConfig,
				extraDetail,
				reason=reason
			)
			if fieldSequence:
				speechSequence.extend(fieldSequence)
				shouldConsiderTextInfoBlank = False
			if field.get("role")==controlTypes.Role.MATH:
				shouldConsiderTextInfoBlank = False
				_extendSpeechSequence_addMathForTextInfo(speechSequence, info, field)

	# When true, we are inside a clickable field, and should therefore not announce any more new clickable fields
	inClickable=False
	#Get speech text for any fields in the new controlFieldStack that are not in the old controlFieldStack
	for count in range(commonFieldCount,len(newControlFieldStack)):
		field=newControlFieldStack[count]
		if not inClickable and formatConfig['reportClickable']:
			states=field.get('states')
			if states and controlTypes.State.CLICKABLE in states:
				# We entered the most outer clickable, so announce it, if we won't be announcing anything else interesting for this field
				presCat=field.getPresentationCategory(newControlFieldStack[0:count],formatConfig,reason)
				if not presCat or presCat is field.PRESCAT_LAYOUT:
					speechSequence.append(controlTypes.State.CLICKABLE.displayString)
					shouldConsiderTextInfoBlank = False
				inClickable=True
		fieldSequence = info.getControlFieldSpeech(
			field,
			newControlFieldStack[0:count],
			"start_addedToControlFieldStack",
			formatConfig,
			extraDetail,
			reason=reason
		)
		if fieldSequence:
			speechSequence.extend(fieldSequence)
			shouldConsiderTextInfoBlank = False
		if field.get("role")==controlTypes.Role.MATH:
			shouldConsiderTextInfoBlank = False
			_extendSpeechSequence_addMathForTextInfo(speechSequence, info, field)
		commonFieldCount+=1

	#Fetch the text for format field attributes that have changed between what was previously cached, and this textInfo's initialFormatField.
	fieldSequence = info.getFormatFieldSpeech(
		newFormatField,
		formatFieldAttributesCache,
		formatConfig,
		reason=reason,
		unit=unit,
		extraDetail=extraDetail,
		initialFormat=True
	)
	if fieldSequence:
		speechSequence.extend(fieldSequence)
	language = None
	if autoLanguageSwitching:
		language=newFormatField.get('language')
		speechSequence.append(LangChangeCommand(language))
		lastLanguage=language

	def isControlEndFieldCommand(x):
		return isinstance(x, textInfos.FieldCommand) and x.command == "controlEnd"

	isWordOrCharUnit = unit in (textInfos.UNIT_CHARACTER, textInfos.UNIT_WORD)
	if onlyInitialFields or (
		isWordOrCharUnit
		and len(textWithFields) > 0
		and len(textWithFields[0].strip() if not textWithFields[0].isspace() else textWithFields[0]) == 1
		and all(isControlEndFieldCommand(x) for x in itertools.islice(textWithFields, 1, None))
	):
		if not onlyCache:
			if onlyInitialFields or any(isinstance(x, str) for x in speechSequence):
				yield speechSequence
			if not onlyInitialFields:
				spellingSequence = list(getSpellingSpeech(
					textWithFields[0],
					locale=language
				))
				logBadSequenceTypes(spellingSequence)
				yield spellingSequence
		if useCache:
			speakTextInfoState.controlFieldStackCache=newControlFieldStack
			speakTextInfoState.formatFieldAttributesCache=formatFieldAttributesCache
			if not isinstance(useCache,SpeakTextInfoState):
				speakTextInfoState.updateObj()
		return False

	# Similar to before, but If the most inner clickable is exited, then we allow announcing clickable for the next lot of clickable fields entered.
	inClickable=False
	#Move through the field commands, getting speech text for all controlStarts, controlEnds and formatChange commands
	#But also keep newControlFieldStack up to date as we will need it for the ends
	# Add any text to a separate list, as it must be handled differently.
	#Also make sure that LangChangeCommand objects are added before any controlField or formatField speech
	relativeSpeechSequence=[]
	inTextChunk=False
	allIndentation=""
	indentationDone=False
	for command in textWithFields:
		if isinstance(command,str):
			# Text should break a run of clickables
			inClickable=False
			if reportIndentation and not indentationDone:
				indentation,command=splitTextIndentation(command)
				# Combine all indentation into one string for later processing.
				allIndentation+=indentation
				if command:
					# There was content after the indentation, so there is no more indentation.
					indentationDone=True
			if command:
				if inTextChunk:
					relativeSpeechSequence[-1]+=command
				else:
					relativeSpeechSequence.append(command)
					inTextChunk=True
		elif isinstance(command,textInfos.FieldCommand):
			newLanguage=None
			if  command.command=="controlStart":
				# Control fields always start a new chunk, even if they have no field text.
				inTextChunk=False
				fieldSequence = []
				if not inClickable and formatConfig['reportClickable']:
					states=command.field.get('states')
					if states and controlTypes.State.CLICKABLE in states:
						# We have entered an outer most clickable or entered a new clickable after exiting a previous one 
						# Announce it if there is nothing else interesting about the field, but not if the user turned it off. 
						presCat=command.field.getPresentationCategory(newControlFieldStack[0:],formatConfig,reason)
						if not presCat or presCat is command.field.PRESCAT_LAYOUT:
							fieldSequence.append(controlTypes.State.CLICKABLE.displayString)
						inClickable=True
				fieldSequence.extend(info.getControlFieldSpeech(
					command.field,
					newControlFieldStack,
					"start_relative",
					formatConfig,
					extraDetail,
					reason=reason
				))
				newControlFieldStack.append(command.field)
			elif command.command=="controlEnd":
				# Exiting a controlField should break a run of clickables
				inClickable=False
				# Control fields always start a new chunk, even if they have no field text.
				inTextChunk=False
				fieldSequence = info.getControlFieldSpeech(
					newControlFieldStack[-1],
					newControlFieldStack[0:-1],
					"end_relative",
					formatConfig,
					extraDetail,
					reason=reason
				)
				del newControlFieldStack[-1]
				if commonFieldCount>len(newControlFieldStack):
					commonFieldCount=len(newControlFieldStack)
			elif command.command=="formatChange":
				fieldSequence = info.getFormatFieldSpeech(
					command.field,
					formatFieldAttributesCache,
					formatConfig,
					reason=reason,
					unit=unit,
					extraDetail=extraDetail
				)
				if fieldSequence:
					inTextChunk=False
				if autoLanguageSwitching:
					newLanguage=command.field.get('language')
					if lastLanguage!=newLanguage:
						# The language has changed, so this starts a new text chunk.
						inTextChunk=False
			if not inTextChunk:
				if fieldSequence:
					if autoLanguageSwitching and lastLanguage is not None:
						# Fields must be spoken in the default language.
						relativeSpeechSequence.append(LangChangeCommand(None))
						lastLanguage=None
					relativeSpeechSequence.extend(fieldSequence)
				if command.command=="controlStart" and command.field.get("role")==controlTypes.Role.MATH:
					_extendSpeechSequence_addMathForTextInfo(relativeSpeechSequence, info, command.field)
				if autoLanguageSwitching and newLanguage!=lastLanguage:
					relativeSpeechSequence.append(LangChangeCommand(newLanguage))
					lastLanguage=newLanguage
	if reportIndentation and speakTextInfoState and allIndentation!=speakTextInfoState.indentationCache:
		indentationSpeech=getIndentationSpeech(allIndentation, formatConfig)
		if autoLanguageSwitching and speechSequence[-1].lang is not None:
			# Indentation must be spoken in the default language,
			# but the initial format field specified a different language.
			# Insert the indentation before the LangChangeCommand.
			langChange = speechSequence.pop()
			speechSequence.extend(indentationSpeech)
			speechSequence.append(langChange)
		else:
			speechSequence.extend(indentationSpeech)
		if speakTextInfoState: speakTextInfoState.indentationCache=allIndentation
	# Don't add this text if it is blank.
	relativeBlank=True
	for x in relativeSpeechSequence:
		if isinstance(x,str) and not isBlank(x):
			relativeBlank=False
			break
	if not relativeBlank:
		speechSequence.extend(relativeSpeechSequence)
		shouldConsiderTextInfoBlank = False

	#Finally get speech text for any fields left in new controlFieldStack that are common with the old controlFieldStack (for closing), if extra detail is not requested
	if autoLanguageSwitching and lastLanguage is not None:
		speechSequence.append(
			LangChangeCommand(None)
		)
		lastLanguage=None
	if not extraDetail:
		for count in reversed(range(min(len(newControlFieldStack),commonFieldCount))):
			fieldSequence = info.getControlFieldSpeech(
				newControlFieldStack[count],
				newControlFieldStack[0:count],
				"end_inControlFieldStack",
				formatConfig,
				extraDetail,
				reason=reason
			)
			if fieldSequence:
				speechSequence.extend(fieldSequence)
				shouldConsiderTextInfoBlank = False

	# If there is nothing that should cause the TextInfo to be considered
	# non-blank, blank should be reported, unless we are doing a say all.
	if not suppressBlanks and reason != OutputReason.SAYALL and shouldConsiderTextInfoBlank:
		# Translators: This is spoken when the line is considered blank.
		speechSequence.append(_("blank"))

	#Cache a copy of the new controlFieldStack for future use
	if useCache:
		speakTextInfoState.controlFieldStackCache=list(newControlFieldStack)
		speakTextInfoState.formatFieldAttributesCache=formatFieldAttributesCache
		if not isinstance(useCache,SpeakTextInfoState):
			speakTextInfoState.updateObj()

	if reason == OutputReason.ONLYCACHE or not speechSequence:
		return False

	yield speechSequence
	return True


# C901 'getPropertiesSpeech' is too complex
# Note: when working on getPropertiesSpeech, look for opportunities to simplify
# and move logic out into smaller helper functions.
def getPropertiesSpeech(  # noqa: C901
		reason: OutputReason = OutputReason.QUERY,
		**propertyValues
) -> SpeechSequence:
	textList: List[str] = []
	name: Optional[str] = propertyValues.get('name')
	if name:
		textList.append(name)
	if 'role' in propertyValues:
		role: controlTypes.Role = propertyValues['role']
		speakRole=True
	elif '_role' in propertyValues:
		speakRole=False
		role: controlTypes.Role = propertyValues['_role']
	else:
		speakRole=False
		role=controlTypes.Role.UNKNOWN
	role = controlTypes.Role(role)
	value: Optional[str] = propertyValues.get('value') if role not in controlTypes.silentValuesForRoles else None
	cellCoordsText: Optional[str] = propertyValues.get('cellCoordsText')
	rowNumber = propertyValues.get('rowNumber')
	columnNumber = propertyValues.get('columnNumber')
	includeTableCellCoords = propertyValues.get('includeTableCellCoords', True)

	if role == controlTypes.Role.CHARTELEMENT:
		speakRole = False
	roleText: Optional[str] = propertyValues.get('roleText')
	if (
		speakRole
		and (
			roleText
			or reason not in (
				OutputReason.SAYALL,
				OutputReason.CARET,
				OutputReason.FOCUS,
				OutputReason.QUICKNAV
			)
			or not (
				name
				or value
				or cellCoordsText
				or rowNumber
				or columnNumber
			)
			or role not in controlTypes.silentRolesOnFocus
		)
		and (
			role != controlTypes.Role.MATH
			or reason not in (
				OutputReason.CARET,
				OutputReason.SAYALL
			)
	)):
		textList.append(roleText if roleText else role.displayString)
	if value:
		textList.append(value)
	states = propertyValues.get('states')
	realStates=propertyValues.get('_states',states)
	negativeStates=propertyValues.get('negativeStates',set())
	# If the caller didn't want states, states will be None.
	# However, empty states means the caller still wants states, but the object
	# had no states; e.g. an unchecked check box with no other states.
	if states is not None or negativeStates:
		if states is None:
			# processAndLabelStates won't accept None for states.
			states = set()
		labelStates = controlTypes.processAndLabelStates(role, realStates, reason, states, negativeStates)
		textList.extend(labelStates)
	# sometimes description key is present but value is None
	description: Optional[str] = propertyValues.get('description')
	if description:
		textList.append(description)
	# sometimes keyboardShortcut key is present but value is None
	keyboardShortcut: Optional[str] = propertyValues.get('keyboardShortcut')
	if keyboardShortcut:
		textList.append(keyboardShortcut)
	if includeTableCellCoords and cellCoordsText:
		textList.append(cellCoordsText)
	if cellCoordsText or rowNumber or columnNumber:
		tableID = propertyValues.get("_tableID")
		# Always treat the table as different if there is no tableID.
		sameTable = (tableID and tableID == _speechState.oldTableID)
		# Don't update the oldTableID if no tableID was given.
		if tableID and not sameTable:
			_speechState.oldTableID = tableID
		# When fetching row and column span
		# default the values to 1 to make further checks a lot simpler.
		# After all, a table cell that has no rowspan implemented is assumed to span one row.
		rowSpan = propertyValues.get("rowSpan") or 1
		columnSpan = propertyValues.get("columnSpan") or 1
		if rowNumber and (
			not sameTable
			or rowNumber != _speechState.oldRowNumber
			or rowSpan != _speechState.oldRowSpan
		):
			rowHeaderText: Optional[str] = propertyValues.get("rowHeaderText")
			if rowHeaderText:
				textList.append(rowHeaderText)
			if includeTableCellCoords and not cellCoordsText: 
				# Translators: Speaks current row number (example output: row 3).
				rowNumberTranslation: str = _("row %s") % rowNumber
				textList.append(rowNumberTranslation)
				if rowSpan>1 and columnSpan<=1:
					# Translators: Speaks the row span added to the current row number (example output: through 5).
					rowSpanAddedTranslation: str = _("through %s") % (rowNumber + rowSpan - 1)
					textList.append(rowSpanAddedTranslation)
			_speechState.oldRowNumber = rowNumber
			_speechState.oldRowSpan = rowSpan
		if columnNumber and (
			not sameTable
			or columnNumber != _speechState.oldColumnNumber
			or columnSpan != _speechState.oldColumnSpan
		):
			columnHeaderText: Optional[str] = propertyValues.get("columnHeaderText")
			if columnHeaderText:
				textList.append(columnHeaderText)
			if includeTableCellCoords and not cellCoordsText:
				# Translators: Speaks current column number (example output: column 3).
				colNumberTranslation: str = _("column %s") % columnNumber
				textList.append(colNumberTranslation)
				if columnSpan>1 and rowSpan<=1:
					# Translators: Speaks the column span added to the current column number (example output: through 5).
					colSpanAddedTranslation: str = _("through %s") % (columnNumber + columnSpan - 1)
					textList.append(colSpanAddedTranslation)
			_speechState.oldColumnNumber = columnNumber
			_speechState.oldColumnSpan = columnSpan
		if includeTableCellCoords and not cellCoordsText and rowSpan>1 and columnSpan>1:
			# Translators: Speaks the row and column span added to the current row and column numbers
			#			(example output: through row 5 column 3).
			rowColSpanTranslation: str = _("through row {row} column {column}").format(
				row=rowNumber + rowSpan - 1,
				column=columnNumber + columnSpan - 1
			)
			textList.append(rowColSpanTranslation)
	rowCount=propertyValues.get('rowCount',0)
	columnCount=propertyValues.get('columnCount',0)
	if rowCount and columnCount:
		# Translators: Speaks number of columns and rows in a table (example output: with 3 rows and 2 columns).
		rowAndColCountTranslation: str = _("with {rowCount} rows and {columnCount} columns").format(
			rowCount=rowCount,
			columnCount=columnCount
		)
		textList.append(rowAndColCountTranslation)
	elif columnCount and not rowCount:
		# Translators: Speaks number of columns (example output: with 4 columns).
		columnCountTransation: str = _("with %s columns") % columnCount
		textList.append(columnCountTransation)
	elif rowCount and not columnCount:
		# Translators: Speaks number of rows (example output: with 2 rows).
		rowCountTranslation: str = _("with %s rows") % rowCount
		textList.append(rowCountTranslation)
	if rowCount or columnCount:
		# The caller is entering a table, so ensure that it is treated as a new table, even if the previous table was the same.
		_speechState.oldTableID = None

	# speak isCurrent property EG aria-current
	isCurrent = propertyValues.get('current', controlTypes.IsCurrent.NO)
	if isCurrent != controlTypes.IsCurrent.NO:
		textList.append(isCurrent.displayString)

	# are there further details
	hasDetails = propertyValues.get('hasDetails', False)
	if hasDetails:
		textList.append(
			# Translators: Speaks when there a further details/annotations that can be fetched manually.
			_("has details")
		)

	placeholder: Optional[str] = propertyValues.get('placeholder', None)
	if placeholder:
		textList.append(placeholder)
	indexInGroup=propertyValues.get('positionInfo_indexInGroup',0)
	similarItemsInGroup=propertyValues.get('positionInfo_similarItemsInGroup',0)
	if 0<indexInGroup<=similarItemsInGroup:
		# Translators: Spoken to indicate the position of an item in a group of items (such as a list).
		# {number} is replaced with the number of the item in the group.
		# {total} is replaced with the total number of items in the group.
		itemPosTranslation: str = _("{number} of {total}").format(
			number=indexInGroup,
			total=similarItemsInGroup
		)
		textList.append(itemPosTranslation)
	if 'positionInfo_level' in propertyValues:
		level=propertyValues.get('positionInfo_level',None)
		role=propertyValues.get('role',None)
		if level is not None:
			# Translators: Speaks the item level in treeviews (example output: level 2).
			levelTranslation: str = _('level %s') % level
			if (
				role in (controlTypes.Role.TREEVIEWITEM, controlTypes.Role.LISTITEM)
				and level != _speechState.oldTreeLevel
			):
				textList.insert(0, levelTranslation)
				_speechState.oldTreeLevel = level
			else:
				textList.append(levelTranslation)
	types.logBadSequenceTypes(textList)
	return textList


def _shouldSpeakContentFirst(
		reason: OutputReason,
		role: int,
		presCat: str,
		attrs: textInfos.ControlField,
		tableID: Any,
		states: Iterable[int],
) -> bool:
	"""
	Determines whether or not to speak the content before the controlField information.
	Helper function for getControlFieldSpeech.
	"""
	_neverSpeakContentFirstRoles = (
		controlTypes.Role.EDITABLETEXT,
		controlTypes.Role.COMBOBOX,
		controlTypes.Role.TREEVIEW,
		controlTypes.Role.LIST,
		controlTypes.Role.LANDMARK,
		controlTypes.Role.REGION,
	)
	return (
		reason in [OutputReason.FOCUS, OutputReason.QUICKNAV]
		and (
			# the category is not a container, unless it's an article (#11103)
			presCat != attrs.PRESCAT_CONTAINER
			or role == controlTypes.Role.ARTICLE
		)
		and not (role in _neverSpeakContentFirstRoles)
		and not tableID
		and controlTypes.State.EDITABLE not in states
	)


# C901 'getControlFieldSpeech' is too complex
# Note: when working on getControlFieldSpeech, look for opportunities to simplify
# and move logic out into smaller helper functions.
def getControlFieldSpeech(  # noqa: C901
		attrs: textInfos.ControlField,
		ancestorAttrs: List[textInfos.Field],
		fieldType: str,
		formatConfig: Optional[Dict[str, bool]] = None,
		extraDetail: bool = False,
		reason: Optional[OutputReason] = None
) -> SpeechSequence:
	if attrs.get('isHidden'):
		return []
	if not formatConfig:
		formatConfig=config.conf["documentFormatting"]

	presCat = attrs.getPresentationCategory(
		ancestorAttrs,
		formatConfig,
		reason=reason,
		extraDetail=extraDetail
	)
	childControlCount=int(attrs.get('_childcontrolcount',"0"))
	role = attrs.get('role', controlTypes.Role.UNKNOWN)
	if (
		reason in [OutputReason.FOCUS, OutputReason.QUICKNAV]
		or attrs.get('alwaysReportName', False)
	):
		name = attrs.get('name', "")
	else:
		name = ""
	states=attrs.get('states',set())
	keyboardShortcut=attrs.get('keyboardShortcut', "")
	isCurrent = attrs.get('current', controlTypes.IsCurrent.NO)
	hasDetails = attrs.get('hasDetails', False)
	placeholderValue=attrs.get('placeholder', None)
	value=attrs.get('value',"")

	description: Optional[str] = None
	_descriptionFrom = attrs.get('_description-from', controlTypes.DescriptionFrom.UNKNOWN)
	_descriptionIsContent: bool = attrs.get("descriptionIsContent", False)
	_reportDescriptionAsAnnotation: bool = (
		# Don't report other sources of description like "title" all the time
		# The usages of these is not consistent and often does not seem to have
		# Screen Reader users in mind
		config.conf["annotations"]["reportAriaDescription"]
		and not _descriptionIsContent
		and controlTypes.DescriptionFrom.ARIA_DESCRIPTION == _descriptionFrom
		and reason in (
			OutputReason.FOCUS,
			OutputReason.QUICKNAV,
			OutputReason.CARET,
			OutputReason.SAYALL,
		)
	)
	if (
		(
			config.conf["presentation"]["reportObjectDescriptions"]
			and not _descriptionIsContent
			and reason in [OutputReason.FOCUS, OutputReason.QUICKNAV]
		)
		or (
			# 'alwaysReportDescription' provides symmetry with 'alwaysReportName'.
			# Not used internally, but may be used by addons.
			attrs.get('alwaysReportDescription', False)
		)
		or _reportDescriptionAsAnnotation
	):
		description = attrs.get('description')

	level=attrs.get('level',None)

	if presCat != attrs.PRESCAT_LAYOUT:
		tableID = attrs.get("table-id")
	else:
		tableID = None

	roleText = attrs.get('roleText')
	landmark = attrs.get("landmark")
	if roleText:
		roleTextSequence = [roleText, ]
	elif role == controlTypes.Role.LANDMARK and landmark:
		roleTextSequence = [
			f"{aria.landmarkRoles[landmark]} {controlTypes.Role.LANDMARK.displayString}",
		]
	else:
		roleTextSequence = getPropertiesSpeech(reason=reason, role=role)
	stateTextSequence = getPropertiesSpeech(reason=reason, states=states, _role=role)
	keyboardShortcutSequence = []
	if config.conf["presentation"]["reportKeyboardShortcuts"]:
		keyboardShortcutSequence = getPropertiesSpeech(
			reason=reason, keyboardShortcut=keyboardShortcut
		)
	isCurrentSequence = getPropertiesSpeech(reason=reason, current=isCurrent)
	hasDetailsSequence = getPropertiesSpeech(reason=reason, hasDetails=hasDetails)
	placeholderSequence = getPropertiesSpeech(reason=reason, placeholder=placeholderValue)
	nameSequence = getPropertiesSpeech(reason=reason, name=name)
	valueSequence = getPropertiesSpeech(reason=reason, value=value, _role=role)
	descriptionSequence = []
	if description is not None:
		descriptionSequence = getPropertiesSpeech(
			reason=reason, description=description
		)
	levelSequence = getPropertiesSpeech(reason=reason, positionInfo_level=level)

	# Determine under what circumstances this node should be spoken.
	# speakEntry: Speak when the user enters the control.
	# speakWithinForLine: When moving by line, speak when the user is already within the control.
	# speakExitForLine: When moving by line, speak when the user exits the control.
	# speakExitForOther: When moving by word or character, speak when the user exits the control.
	speakEntry=speakWithinForLine=speakExitForLine=speakExitForOther=False
	if presCat == attrs.PRESCAT_SINGLELINE:
		speakEntry=True
		speakWithinForLine=True
		speakExitForOther=True
	elif presCat in (attrs.PRESCAT_MARKER, attrs.PRESCAT_CELL):
		speakEntry=True
	elif presCat == attrs.PRESCAT_CONTAINER:
		speakEntry=True
		speakExitForLine = bool(
			attrs.get('roleText')
			or role != controlTypes.Role.LANDMARK
		)
		speakExitForOther=True

	# Determine the order of speech.
	# speakContentFirst: Speak the content before the control field info.
	speakContentFirst = _shouldSpeakContentFirst(reason, role, presCat, attrs, tableID, states)
	# speakStatesFirst: Speak the states before the role.
	speakStatesFirst=role==controlTypes.Role.LINK

	containerContainsText="" #: used for item counts for lists

	# Determine what text to speak.
	# Special cases
	if(
		childControlCount
		and fieldType == "start_addedToControlFieldStack"
		and role == controlTypes.Role.LIST
		and controlTypes.State.READONLY in states
	):
		# List.
		# #7652: containerContainsText variable is set here, but the actual generation of all other output is
		# handled further down in the general cases section.
		# This ensures that properties such as name, states and level etc still get reported appropriately.
		# Translators: Number of items in a list (example output: list with 5 items).
		containerContainsText=_("with %s items")%childControlCount
	elif fieldType=="start_addedToControlFieldStack" and role==controlTypes.Role.TABLE and tableID:
		# Table.
		rowCount=(attrs.get("table-rowcount-presentational") or attrs.get("table-rowcount"))
		columnCount=(attrs.get("table-columncount-presentational") or attrs.get("table-columncount"))
		tableSeq = nameSequence[:]
		tableSeq.extend(roleTextSequence)
		tableSeq.extend(stateTextSequence)
		tableSeq.extend(
			getPropertiesSpeech(
				_tableID=tableID, 
				rowCount=rowCount, 
				columnCount=columnCount
		))
		tableSeq.extend(levelSequence)
		types.logBadSequenceTypes(tableSeq)
		return tableSeq
	elif (
		nameSequence
		and reason in [OutputReason.FOCUS, OutputReason.QUICKNAV]
		and fieldType == "start_addedToControlFieldStack"
		and role in (controlTypes.Role.GROUPING, controlTypes.Role.PROPERTYPAGE)
	):
		# #10095, #3321, #709: Report the name and description of groupings (such as fieldsets) and tab pages
		nameAndRole = nameSequence[:]
		nameAndRole.extend(roleTextSequence)
		types.logBadSequenceTypes(nameAndRole)
		return nameAndRole
	elif (
		fieldType in ("start_addedToControlFieldStack", "start_relative")
		and role in (
			controlTypes.Role.TABLECELL,
			controlTypes.Role.TABLECOLUMNHEADER,
			controlTypes.Role.TABLEROWHEADER
		)
		and tableID
	):
		# Table cell.
		reportTableHeaders = formatConfig["reportTableHeaders"]
		reportTableCellCoords = formatConfig["reportTableCellCoords"]
		getProps = {
			'rowNumber': (attrs.get("table-rownumber-presentational") or attrs.get("table-rownumber")),
			'columnNumber': (attrs.get("table-columnnumber-presentational") or attrs.get("table-columnnumber")),
			'rowSpan': attrs.get("table-rowsspanned"),
			'columnSpan': attrs.get("table-columnsspanned"),
			'includeTableCellCoords': reportTableCellCoords
		}
		if reportTableHeaders:
			getProps['rowHeaderText'] = attrs.get("table-rowheadertext")
			getProps['columnHeaderText'] = attrs.get("table-columnheadertext")
		tableCellSequence = getPropertiesSpeech(_tableID=tableID, **getProps)
		tableCellSequence.extend(stateTextSequence)
		tableCellSequence.extend(isCurrentSequence)
		tableCellSequence.extend(hasDetailsSequence)
		types.logBadSequenceTypes(tableCellSequence)
		return tableCellSequence

	content = attrs.get("content")
	# General cases.
	if ((
		speakEntry and ((
			speakContentFirst
			and fieldType in ("end_relative", "end_inControlFieldStack")
		)
		or (
			not speakContentFirst
			and fieldType in ("start_addedToControlFieldStack", "start_relative")
		))
	)
	or (
		speakWithinForLine
		and not speakContentFirst
		and not extraDetail
		and fieldType == "start_inControlFieldStack"
	)):
		out = []
		if content and speakContentFirst:
			out.append(content)
		if placeholderValue:
			if valueSequence:
				log.error(
					f"valueSequence exists when expected none: "
					f"valueSequence: {valueSequence!r} placeholderSequence: {placeholderSequence!r}"
				)
			valueSequence = placeholderSequence

		# Avoid speaking name twice. Which may happen if this controlfield is labelled by
		# one of it's internal fields. We determine this by checking for 'labelledByContent'.
		# An example of this situation is a checkbox element that has aria-labelledby pointing to a child
		# element.
		if (
			# Don't speak name when labelledByContent. It will be spoken by the subsequent controlFields instead.
			attrs.get("IAccessible2::attribute_explicit-name", False)
			and attrs.get("labelledByContent", False)
		):
			log.debug("Skipping name sequence: control field is labelled by content")
		else:
			out.extend(nameSequence)

		out.extend(stateTextSequence if speakStatesFirst else roleTextSequence)
		out.extend(roleTextSequence if speakStatesFirst else stateTextSequence)
		out.append(containerContainsText)
		out.extend(isCurrentSequence)
		out.extend(hasDetailsSequence)
		out.extend(valueSequence)
		out.extend(descriptionSequence)
		out.extend(levelSequence)
		out.extend(keyboardShortcutSequence)
		if content and not speakContentFirst:
			out.append(content)

		types.logBadSequenceTypes(out)
		return out
	elif (
		fieldType in (
			"end_removedFromControlFieldStack",
			"end_relative",
		)
		and roleTextSequence
		and (
			(not extraDetail and speakExitForLine)
			or (extraDetail and speakExitForOther)
	)):
		if all(isinstance(item, str) for item in roleTextSequence):
			joinedRoleText = " ".join(roleTextSequence)
			out = [
				# Translators: Indicates end of something (example output: at the end of a list, speaks out of list).
				_("out of %s") % joinedRoleText,
			]
		else:
			out = roleTextSequence

		types.logBadSequenceTypes(out)
		return out

	# Special cases
	elif not speakEntry and fieldType in ("start_addedToControlFieldStack","start_relative"):
		out = []
		if isCurrent != controlTypes.IsCurrent.NO:
			out.extend(isCurrentSequence)
		if hasDetails:
			out.extend(hasDetailsSequence)
		if descriptionSequence and _reportDescriptionAsAnnotation:
			out.extend(descriptionSequence)
		# Speak expanded / collapsed / level for treeview items (in ARIA treegrids)
		if role == controlTypes.Role.TREEVIEWITEM:
			if controlTypes.State.EXPANDED in states:
				out.extend(
					getPropertiesSpeech(reason=reason, states={controlTypes.State.EXPANDED}, _role=role)
				)
			elif controlTypes.State.COLLAPSED in states:
				out.extend(
					getPropertiesSpeech(reason=reason, states={controlTypes.State.COLLAPSED}, _role=role)
				)
			if levelSequence:
				out.extend(levelSequence)
		if role == controlTypes.Role.GRAPHIC and content:
			out.append(content)
		types.logBadSequenceTypes(out)
		return out
	else:
		return []


# C901 'getFormatFieldSpeech' is too complex
# Note: when working on getFormatFieldSpeech, look for opportunities to simplify
# and move logic out into smaller helper functions.
def getFormatFieldSpeech(  # noqa: C901
		attrs: textInfos.Field,
		attrsCache: Optional[textInfos.Field] = None,
		formatConfig: Optional[Dict[str, bool]] = None,
		reason: Optional[OutputReason] = None,
		unit: Optional[str] = None,
		extraDetail: bool = False,
		initialFormat: bool = False,
) -> SpeechSequence:
	if not formatConfig:
		formatConfig=config.conf["documentFormatting"]
	textList=[]
	if formatConfig["reportTables"]:
		tableInfo=attrs.get("table-info")
		oldTableInfo=attrsCache.get("table-info") if attrsCache is not None else None
		tableSequence = getTableInfoSpeech(
			tableInfo, oldTableInfo, extraDetail=extraDetail
		)
		if tableSequence:
			textList.extend(tableSequence)
	if formatConfig["reportPage"]:
		pageNumber=attrs.get("page-number")
		oldPageNumber=attrsCache.get("page-number") if attrsCache is not None else None
		if pageNumber and pageNumber!=oldPageNumber:
			# Translators: Indicates the page number in a document.
			# %s will be replaced with the page number.
			text=_("page %s")%pageNumber
			textList.append(text)
		sectionNumber=attrs.get("section-number")
		oldSectionNumber=attrsCache.get("section-number") if attrsCache is not None else None
		if sectionNumber and sectionNumber!=oldSectionNumber:
			# Translators: Indicates the section number in a document.
			# %s will be replaced with the section number.
			text=_("section %s")%sectionNumber
			textList.append(text)

		textColumnCount=attrs.get("text-column-count")
		oldTextColumnCount=attrsCache.get("text-column-count") if attrsCache is not None else None
		textColumnNumber=attrs.get("text-column-number")
		oldTextColumnNumber=attrsCache.get("text-column-number") if attrsCache is not None else None

		# Because we do not want to report the number of columns when a document is just opened and there is only 
		# one column. This would be verbose, in the standard case.
		# column number has changed, or the columnCount has changed
		# but not if the columnCount is 1 or less and there is no old columnCount.
		if (((textColumnNumber and textColumnNumber!=oldTextColumnNumber) or
			(textColumnCount and textColumnCount!=oldTextColumnCount)) and not
			(textColumnCount and int(textColumnCount) <=1 and oldTextColumnCount == None)) :
			if textColumnNumber and textColumnCount:
				# Translators: Indicates the text column number in a document.
				# {0} will be replaced with the text column number.
				# {1} will be replaced with the number of text columns.
				text=_("column {0} of {1}").format(textColumnNumber,textColumnCount)
				textList.append(text)
			elif textColumnCount:
				# Translators: Indicates the text column number in a document.
				# %s will be replaced with the number of text columns.
				text=_("%s columns")%(textColumnCount)
				textList.append(text)
			elif textColumnNumber:
				# Translators: Indicates the text column number in a document.
				text = _("column {columnNumber}").format(columnNumber=textColumnNumber)
				textList.append(text)

	sectionBreakType=attrs.get("section-break")
	if sectionBreakType:
		if sectionBreakType == "0" : # Continuous section break.
			text=_("continuous section break")
		elif sectionBreakType == "1" : # New column section break.
			text=_("new column section break")
		elif sectionBreakType == "2" : # New page section break.
			text=_("new page section break")
		elif sectionBreakType == "3" : # Even pages section break.
			text=_("even pages section break")
		elif sectionBreakType == "4" : # Odd pages section break.
			text=_("odd pages section break")
		else:
			text=""
		textList.append(text)
	columnBreakType=attrs.get("column-break")
	if columnBreakType:
		textList.append(_("column break"))
	if  formatConfig["reportHeadings"]:
		headingLevel=attrs.get("heading-level")
		oldHeadingLevel=attrsCache.get("heading-level") if attrsCache is not None else None
		# headings should be spoken not only if they change, but also when beginning to speak lines or paragraphs
		# Ensuring a similar experience to if a heading was a controlField
		if(
			headingLevel
			and (
				initialFormat
				and (
					reason in [OutputReason.FOCUS, OutputReason.QUICKNAV]
					or unit in (textInfos.UNIT_LINE, textInfos.UNIT_PARAGRAPH)
				)
				or headingLevel != oldHeadingLevel
			)
		):
			# Translators: Speaks the heading level (example output: heading level 2).
			text=_("heading level %d")%headingLevel
			textList.append(text)
	if  formatConfig["reportStyle"]:
		style=attrs.get("style")
		oldStyle=attrsCache.get("style") if attrsCache is not None else None
		if style!=oldStyle:
			if style:
				# Translators: Indicates the style of text.
				# A style is a collection of formatting settings and depends on the application.
				# %s will be replaced with the name of the style.
				text=_("style %s")%style
			else:
				# Translators: Indicates that text has reverted to the default style.
				# A style is a collection of formatting settings and depends on the application.
				text=_("default style")
			textList.append(text)
	if  formatConfig["reportBorderStyle"]:
		borderStyle=attrs.get("border-style")
		oldBorderStyle=attrsCache.get("border-style") if attrsCache is not None else None
		if borderStyle!=oldBorderStyle:
			if borderStyle:
				text=borderStyle
			else:
				# Translators: Indicates that cell does not have border lines.
				text=_("no border lines")
			textList.append(text)
	if  formatConfig["reportFontName"]:
		fontFamily=attrs.get("font-family")
		oldFontFamily=attrsCache.get("font-family") if attrsCache is not None else None
		if fontFamily and fontFamily!=oldFontFamily:
			textList.append(fontFamily)
		fontName=attrs.get("font-name")
		oldFontName=attrsCache.get("font-name") if attrsCache is not None else None
		if fontName and fontName!=oldFontName:
			textList.append(fontName)
	if  formatConfig["reportFontSize"]:
		fontSize=attrs.get("font-size")
		oldFontSize=attrsCache.get("font-size") if attrsCache is not None else None
		if fontSize and fontSize!=oldFontSize:
			textList.append(fontSize)
	if  formatConfig["reportColor"]:
		color=attrs.get("color")
		oldColor=attrsCache.get("color") if attrsCache is not None else None
		backgroundColor=attrs.get("background-color")
		oldBackgroundColor=attrsCache.get("background-color") if attrsCache is not None else None
		backgroundColor2=attrs.get("background-color2")
		oldBackgroundColor2=attrsCache.get("background-color2") if attrsCache is not None else None
		bgColorChanged=backgroundColor!=oldBackgroundColor or backgroundColor2!=oldBackgroundColor2
		bgColorText=backgroundColor.name if isinstance(backgroundColor,colors.RGB) else backgroundColor
		if backgroundColor2:
			bg2Name=backgroundColor2.name if isinstance(backgroundColor2,colors.RGB) else backgroundColor2
			# Translators: Reported when there are two background colors.
			# This occurs when, for example, a gradient pattern is applied to a spreadsheet cell.
			# {color1} will be replaced with the first background color.
			# {color2} will be replaced with the second background color.
			bgColorText=_("{color1} to {color2}").format(color1=bgColorText,color2=bg2Name)
		if color and backgroundColor and color!=oldColor and bgColorChanged:
			# Translators: Reported when both the text and background colors change.
			# {color} will be replaced with the text color.
			# {backgroundColor} will be replaced with the background color.
			textList.append(_("{color} on {backgroundColor}").format(
				color=color.name if isinstance(color,colors.RGB) else color,
				backgroundColor=bgColorText))
		elif color and color!=oldColor:
			# Translators: Reported when the text color changes (but not the background color).
			# {color} will be replaced with the text color.
			textList.append(_("{color}").format(color=color.name if isinstance(color,colors.RGB) else color))
		elif backgroundColor and bgColorChanged:
			# Translators: Reported when the background color changes (but not the text color).
			# {backgroundColor} will be replaced with the background color.
			textList.append(_("{backgroundColor} background").format(backgroundColor=bgColorText))
		backgroundPattern=attrs.get("background-pattern")
		oldBackgroundPattern=attrsCache.get("background-pattern") if attrsCache is not None else None
		if backgroundPattern and backgroundPattern!=oldBackgroundPattern:
			textList.append(_("background pattern {pattern}").format(pattern=backgroundPattern))
	if  formatConfig["reportLineNumber"]:
		lineNumber=attrs.get("line-number")
		oldLineNumber=attrsCache.get("line-number") if attrsCache is not None else None
		if lineNumber is not None and lineNumber!=oldLineNumber:
			# Translators: Indicates the line number of the text.
			# %s will be replaced with the line number.
			text=_("line %s")%lineNumber
			textList.append(text)
	if  formatConfig["reportRevisions"]:
		# Insertion
		revision=attrs.get("revision-insertion")
		oldRevision=attrsCache.get("revision-insertion") if attrsCache is not None else None
		if (revision or oldRevision is not None) and revision!=oldRevision:
			# Translators: Reported when text is marked as having been inserted
			text=(_("inserted") if revision
				# Translators: Reported when text is no longer marked as having been inserted.
				else _("not inserted"))
			textList.append(text)
		revision=attrs.get("revision-deletion")
		oldRevision=attrsCache.get("revision-deletion") if attrsCache is not None else None
		if (revision or oldRevision is not None) and revision!=oldRevision:
			# Translators: Reported when text is marked as having been deleted
			text=(_("deleted") if revision
				# Translators: Reported when text is no longer marked as having been  deleted.
				else _("not deleted"))
			textList.append(text)
		revision=attrs.get("revision")
		oldRevision=attrsCache.get("revision") if attrsCache is not None else None
		if (revision or oldRevision is not None) and revision != oldRevision:
			if revision:
				# Translators: Reported when text is revised.
				text = _("revised %s") % revision
			else:
				# Translators: Reported when text is not revised.
				text = _("no revised %s") % oldRevision
			textList.append(text)
	if formatConfig["reportHighlight"]:
		# marked text 
		marked=attrs.get("marked")
		oldMarked=attrsCache.get("marked") if attrsCache is not None else None
		if (marked or oldMarked is not None) and marked!=oldMarked:
			# Translators: Reported when text is marked
			text=(_("marked") if marked
				# Translators: Reported when text is no longer marked
				else _("not marked"))
			textList.append(text)
	if formatConfig["reportEmphasis"]:
		# strong text
		strong=attrs.get("strong")
		oldStrong=attrsCache.get("strong") if attrsCache is not None else None
		if (strong or oldStrong is not None) and strong!=oldStrong:
			# Translators: Reported when text is marked as strong (e.g. bold)
			text=(_("strong") if strong
				# Translators: Reported when text is no longer marked as strong (e.g. bold) 
				else _("not strong"))
			textList.append(text)
		# emphasised text 
		emphasised=attrs.get("emphasised")
		oldEmphasised=attrsCache.get("emphasised") if attrsCache is not None else None
		if (emphasised or oldEmphasised is not None) and emphasised!=oldEmphasised:
			# Translators: Reported when text is marked as emphasised
			text=(_("emphasised") if emphasised
				# Translators: Reported when text is no longer marked as emphasised 
				else _("not emphasised"))
			textList.append(text)
	if  formatConfig["reportFontAttributes"]:
		bold=attrs.get("bold")
		oldBold=attrsCache.get("bold") if attrsCache is not None else None
		if (bold or oldBold is not None) and bold!=oldBold:
			# Translators: Reported when text is bolded.
			text=(_("bold") if bold
				# Translators: Reported when text is not bolded.
				else _("no bold"))
			textList.append(text)
		italic=attrs.get("italic")
		oldItalic=attrsCache.get("italic") if attrsCache is not None else None
		if (italic or oldItalic is not None) and italic!=oldItalic:
			# Translators: Reported when text is italicized.
			text=(_("italic") if italic
				# Translators: Reported when text is not italicized.
				else _("no italic"))
			textList.append(text)
		strikethrough=attrs.get("strikethrough")
		oldStrikethrough=attrsCache.get("strikethrough") if attrsCache is not None else None
		if (strikethrough or oldStrikethrough is not None) and strikethrough!=oldStrikethrough:
			if strikethrough:
				# Translators: Reported when text is formatted with double strikethrough.
				# See http://en.wikipedia.org/wiki/Strikethrough
				text=(_("double strikethrough") if strikethrough=="double"
				# Translators: Reported when text is formatted with strikethrough.
				# See http://en.wikipedia.org/wiki/Strikethrough
				else _("strikethrough"))
			else:
				# Translators: Reported when text is formatted without strikethrough.
				# See http://en.wikipedia.org/wiki/Strikethrough
				text=_("no strikethrough")
			textList.append(text)
		underline=attrs.get("underline")
		oldUnderline=attrsCache.get("underline") if attrsCache is not None else None
		if (underline or oldUnderline is not None) and underline!=oldUnderline:
			# Translators: Reported when text is underlined.
			text=(_("underlined") if underline
				# Translators: Reported when text is not underlined.
				else _("not underlined"))
			textList.append(text)
		hidden = attrs.get("hidden")
		oldHidden = attrsCache.get("hidden") if attrsCache is not None else None
		if (hidden or oldHidden is not None) and hidden != oldHidden:
			text = (
				# Translators: Reported when text is hidden.
				_("hidden")if hidden
				# Translators: Reported when text is not hidden.
				else _("not hidden")
			)
			textList.append(text)
	if formatConfig["reportSuperscriptsAndSubscripts"]:
		textPosition = attrs.get("text-position", TextPosition.UNDEFINED)
		attrs["text-position"] = textPosition
		oldTextPosition = attrsCache.get("text-position") if attrsCache is not None else None
		if (
			textPosition != oldTextPosition
			and (
				textPosition in [TextPosition.SUPERSCRIPT, TextPosition.SUBSCRIPT]
				or (
					textPosition == TextPosition.BASELINE
					and (oldTextPosition is not None and oldTextPosition != TextPosition.UNDEFINED)
				)
			)
		):
			textList.append(textPosition.displayString)
	if formatConfig["reportAlignment"]:
		textAlign=attrs.get("text-align")
		oldTextAlign=attrsCache.get("text-align") if attrsCache is not None else None
		if (textAlign or oldTextAlign is not None) and textAlign!=oldTextAlign:
			textAlign=textAlign.lower() if textAlign else textAlign
			if textAlign=="left":
				# Translators: Reported when text is left-aligned.
				text=_("align left")
			elif textAlign=="center":
				# Translators: Reported when text is centered.
				text=_("align center")
			elif textAlign=="right":
				# Translators: Reported when text is right-aligned.
				text=_("align right")
			elif textAlign=="justify":
				# Translators: Reported when text is justified.
				# See http://en.wikipedia.org/wiki/Typographic_alignment#Justified
				text=_("align justify")
			elif textAlign=="distribute":
				# Translators: Reported when text is justified with character spacing (Japanese etc) 
				# See http://kohei.us/2010/01/21/distributed-text-justification/
				text=_("align distributed")
			else:
				# Translators: Reported when text has reverted to default alignment.
				text=_("align default")
			textList.append(text)
		verticalAlign=attrs.get("vertical-align")
		oldverticalAlign=attrsCache.get("vertical-align") if attrsCache is not None else None
		if (verticalAlign or oldverticalAlign is not None) and verticalAlign!=oldverticalAlign:
			verticalAlign=verticalAlign.lower() if verticalAlign else verticalAlign
			if verticalAlign=="top":
				# Translators: Reported when text is vertically top-aligned.
				text=_("vertical align top")
			elif verticalAlign in("center","middle"):
				# Translators: Reported when text is vertically middle aligned.
				text=_("vertical align middle")
			elif verticalAlign=="bottom":
				# Translators: Reported when text is vertically bottom-aligned.
				text=_("vertical align bottom")
			elif verticalAlign=="baseline":
				# Translators: Reported when text is vertically aligned on the baseline. 
				text=_("vertical align baseline")
			elif verticalAlign=="justify":
				# Translators: Reported when text is vertically justified.
				text=_("vertical align justified")
			elif verticalAlign=="distributed":
				# Translators: Reported when text is vertically justified but with character spacing (For some Asian content). 
				text=_("vertical align distributed") 
			else:
				# Translators: Reported when text has reverted to default vertical alignment.
				text=_("vertical align default")
			textList.append(text)
	if formatConfig["reportParagraphIndentation"]:
		indentLabels={
			'left-indent':(
				# Translators: the label for paragraph format left indent
				_("left indent"),
				# Translators: the message when there is no paragraph format left indent
				_("no left indent"),
			),
			'right-indent':(
				# Translators: the label for paragraph format right indent
				_("right indent"),
				# Translators: the message when there is no paragraph format right indent
				_("no right indent"),
			),
			'hanging-indent':(
				# Translators: the label for paragraph format hanging indent
				_("hanging indent"),
				# Translators: the message when there is no paragraph format hanging indent
				_("no hanging indent"),
			),
			'first-line-indent':(
				# Translators: the label for paragraph format first line indent 
				_("first line indent"),
				# Translators: the message when there is no paragraph format first line indent
				_("no first line indent"),
			),
		}
		for attr,(label,noVal) in indentLabels.items():
			newVal=attrs.get(attr)
			oldVal=attrsCache.get(attr) if attrsCache else None
			if (newVal or oldVal is not None) and newVal!=oldVal:
				if newVal:
					textList.append(u"%s %s"%(label,newVal))
				else:
					textList.append(noVal)
	if formatConfig["reportLineSpacing"]:
		lineSpacing=attrs.get("line-spacing")
		oldLineSpacing=attrsCache.get("line-spacing") if attrsCache is not None else None
		if (lineSpacing or oldLineSpacing is not None) and lineSpacing!=oldLineSpacing:
			# Translators: a type of line spacing (E.g. single line spacing)
			textList.append(_("line spacing %s")%lineSpacing)
	if  formatConfig["reportLinks"]:
		link=attrs.get("link")
		oldLink=attrsCache.get("link") if attrsCache is not None else None
		if (link or oldLink is not None) and link!=oldLink:
			text=_("link") if link else _("out of %s")%_("link")
			textList.append(text)
	if  formatConfig["reportComments"]:
		comment=attrs.get("comment")
		oldComment=attrsCache.get("comment") if attrsCache is not None else None
		if (comment or oldComment is not None) and comment!=oldComment:
			if comment:
				if comment is textInfos.CommentType.DRAFT:
					# Translators: Reported when text contains a draft comment.
					text = _("has draft comment")
				elif comment is textInfos.CommentType.RESOLVED:
					# Translators: Reported when text contains a resolved comment.
					text = _("has resolved comment")
				else:  # generic
					# Translators: Reported when text contains a generic comment.
					text = _("has comment")
				textList.append(text)
			elif extraDetail:
				# Translators: Reported when text no longer contains a comment.
				text=_("out of comment")
				textList.append(text)
	if formatConfig["reportBookmarks"]:
		bookmark = attrs.get("bookmark")
		oldBookmark = attrsCache.get("bookmark") if attrsCache is not None else None
		if (bookmark or oldBookmark is not None) and bookmark != oldBookmark:
			if bookmark:
				# Translators: Reported when text contains a bookmark
				text = _("bookmark")
				textList.append(text)
			elif extraDetail:
				# Translators: Reported when text no longer contains a bookmark
				text = _("out of bookmark")
				textList.append(text)
	if formatConfig["reportSpellingErrors"]:
		invalidSpelling=attrs.get("invalid-spelling")
		oldInvalidSpelling=attrsCache.get("invalid-spelling") if attrsCache is not None else None
		if (invalidSpelling or oldInvalidSpelling is not None) and invalidSpelling!=oldInvalidSpelling:
			if invalidSpelling:
				# Translators: Reported when text contains a spelling error.
				text=_("spelling error")
			elif extraDetail:
				# Translators: Reported when moving out of text containing a spelling error.
				text=_("out of spelling error")
			else:
				text=""
			if text:
				textList.append(text)
		invalidGrammar=attrs.get("invalid-grammar")
		oldInvalidGrammar=attrsCache.get("invalid-grammar") if attrsCache is not None else None
		if (invalidGrammar or oldInvalidGrammar is not None) and invalidGrammar!=oldInvalidGrammar:
			if invalidGrammar:
				# Translators: Reported when text contains a grammar error.
				text=_("grammar error")
			elif extraDetail:
				# Translators: Reported when moving out of text containing a grammar error.
				text=_("out of grammar error")
			else:
				text=""
			if text:
				textList.append(text)
	# The line-prefix formatField attribute contains the text for a bullet or number for a list item, when the bullet or number does not appear in the actual text content.
	# Normally this attribute could be repeated across formatFields within a list item and therefore is not safe to speak when the unit is word or character.
	# However, some implementations (such as MS Word with UIA) do limit its useage to the very first formatField of the list item.
	# Therefore, they also expose a line-prefix_speakAlways attribute to allow its usage for any unit.
	linePrefix_speakAlways=attrs.get('line-prefix_speakAlways',False)
	if linePrefix_speakAlways or unit in (textInfos.UNIT_LINE,textInfos.UNIT_SENTENCE,textInfos.UNIT_PARAGRAPH,textInfos.UNIT_READINGCHUNK):
		linePrefix=attrs.get("line-prefix")
		if linePrefix:
			textList.append(linePrefix)
	if attrsCache is not None:
		attrsCache.clear()
		attrsCache.update(attrs)
	types.logBadSequenceTypes(textList)
	return textList


def getTableInfoSpeech(
		tableInfo: Optional[Dict[str, Any]],
		oldTableInfo: Optional[Dict[str, Any]],
		extraDetail: bool = False
) -> SpeechSequence:
	if tableInfo is None and oldTableInfo is None:
		return []
	if tableInfo is None and oldTableInfo is not None:
		return [
			# Translators: Indicates end of a table.
			_("out of table")
		]
	if not oldTableInfo or tableInfo.get("table-id")!=oldTableInfo.get("table-id"):
		newTable=True
	else:
		newTable=False
	textList=[]
	if newTable:
		columnCount=tableInfo.get("column-count",0)
		rowCount=tableInfo.get("row-count",0)
		# Translators: reports number of columns and rows in a table (example output: table with 3 columns and 5 rows).
		text=_("table with {columnCount} columns and {rowCount} rows").format(columnCount=columnCount,rowCount=rowCount)
		textList.append(text)
	oldColumnNumber=oldTableInfo.get("column-number",0) if oldTableInfo else 0
	columnNumber=tableInfo.get("column-number",0)
	if columnNumber!=oldColumnNumber:
		textList.append(_("column %s")%columnNumber)
	oldRowNumber=oldTableInfo.get("row-number",0) if oldTableInfo else 0
	rowNumber=tableInfo.get("row-number",0)
	if rowNumber!=oldRowNumber:
		textList.append(_("row %s")%rowNumber)
	types.logBadSequenceTypes(textList)
	return textList


#: The singleton _SpeechManager instance used for speech functions.
#: @type: L{manager.SpeechManager}
_manager = manager.SpeechManager()


def clearTypedWordBuffer() -> None:
	"""
	Forgets any word currently being built up with typed characters for speaking. 
	This should be called when the user's context changes such that they could no longer 
	complete the word (such as a focus change or choosing to move the caret).
	"""
	_curWordChars.clear()
