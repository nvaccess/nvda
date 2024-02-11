# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import textInfos
from dataclasses import dataclass
import bisect
import re
from typing import Any, Callable
import config
from config.featureFlagEnums import SentenceReconstructionFlag
import json
import speech


def preprocessNewLines(s: str) -> str:
	stripped = s.rstrip("\r\n")
	n = len(s) - len(stripped)
	return stripped + (" " * n)


def sign(x: int) -> int:
	if x > 0:
		return 1
	elif x < 0:
		return -1
	else:
		return 0


def bisect_right_dict(d: dict[int, int], value: int) -> int:
	keys = list(d.keys())
	values = list(d.values())
	i = bisect.bisect_right(values, value)
	return keys[i]


def getParagraphUnitForTextInfo(info: textInfos.TextInfo):
	from appModules.devenv import VsWpfTextViewTextInfo
	if isinstance(info, VsWpfTextViewTextInfo):
		# TextInfo in Visual Studio doesn't understand UNIT_PARAGRAPH
		return textInfos.UNIT_LINE
	return textInfos.UNIT_PARAGRAPH


def moveParagraph(textInfo: textInfos.TextInfo, direction: int) -> textInfos.TextInfo | None:
	originalTextInfo = textInfo.copy()
	textInfo = textInfo.copy()
	if direction > 0:
		textInfo.collapse(end=True)
	else:
		textInfo.collapse(end=False)
		result = textInfo.move(textInfos.UNIT_CHARACTER, -1)
		if result == 0:
			return None
	textInfo.expand(getParagraphUnitForTextInfo(textInfo))
	if direction > 0 and textInfo.compareEndPoints(originalTextInfo, "startToStart") <= 0:
		return None
	if textInfo.isCollapsed:
		return None
	return textInfo


ExtractStyleFunc = Callable[[textInfos.TextInfo], Any]
StyleCompatibilityFunc = Callable[[Any, Any], bool]


def defaultCompatibilityFunc(style1: Any, style2: Any) -> bool:
	return style1 == style2


def falseCompatibilityFunc(style1: Any, style2: Any) -> bool:
	return False


def emptyStyleFunc(textInfo: textInfos.TextInfo):
	return None


PARAGRAPH_styleFields = frozenset([
	"level",
	"font-family",
	"font-size",
	"color",
	"background-color",
])


def defaultStyleFunc(textInfo: textInfos.TextInfo):
	result = {}
	try:
		result['xOffset'] = textInfo.NVDAObjectAtStart.location[0]
	except Exception:
		pass
	info = textInfo.copy()
	info.collapse()
	code = info.move(textInfos.UNIT_CHARACTER, 1, "end")
	if code != 0:
		fields = info.getTextWithFields()
		formatFields = [
			f
			for f in fields
			if isinstance(f, textInfos.FieldCommand)
			and f.command == "formatChange"
		]
		if len(formatFields) > 0:
			formatField = formatFields[0]
			styleProperties = {k: v for k, v in formatField.field.items() if k in PARAGRAPH_styleFields}
			result = {
				**result,
				**styleProperties,
			}
	return result


def getStyleAndCompatibilityFuncs(
) -> tuple[ExtractStyleFunc, StyleCompatibilityFunc]:
	flag: config.featureFlag.FeatureFlag = config.conf["documentNavigation"]["sentenceReconstruction"]
	match flag.calculated():
		case SentenceReconstructionFlag.NEVER:
			return (emptyStyleFunc, falseCompatibilityFunc)
		case SentenceReconstructionFlag.SAME_STYLE_PARAGRAPHS:
			return (defaultStyleFunc, defaultCompatibilityFunc)
		case SentenceReconstructionFlag.ANY_PARAGRAPHS:
			return (emptyStyleFunc, defaultCompatibilityFunc)
		case _:
			raise RuntimeError(f"Invalid sentence reconstruction flag {flag}")


def getSentenceStopRegex(
		regex: str = None,
		nonBreakingPrefixes: str = None,
) -> re.Pattern:
	regex = regex or config.conf["virtualBuffers"]["textParagraphRegex"]
	if nonBreakingPrefixes is None:
		j = json.loads(config.conf["documentNavigation"]["nonBreakingPrefixRegex"])
		language = speech.getCurrentLanguage()
		nonBreakingPrefixes = j.get(language, "")
	nonBreakingNLBs = "".join(
		f"(?<!{s})"
		for s in nonBreakingPrefixes.split("|")
		if len(s) > 0
	)
	regex = regex.format(nonBreakingRegex=nonBreakingNLBs)
	return re.compile(regex)


class ContextParagraph:
	textInfo: textInfos.TextInfo
	text: str
	pythonicLen: int
	style: Any

	def __init__(
			self,
			textInfo: textInfos.TextInfo,
			extractStyleFunc: ExtractStyleFunc,
	):
		self.textInfo = textInfo
		self.text = preprocessNewLines(textInfo.text)
		self.pythonicLen = len(self.text)
		self.style = extractStyleFunc(textInfo)


@dataclass
class IndexAndOffset:
	paragraphIndex: int
	offset: int


@dataclass
class FindSentenceResult:
	start: IndexAndOffset
	end: IndexAndOffset
	shouldExpandStart: bool
	shouldExpandEnd: bool
	sentenceText: str | None


class SentenceContext:
	SEPARATOR: str = "\n"
	paragraphs: dict[int, ContextParagraph]  # we use dict in order to be able to use negative indices
	minIndex: int  # Smallest value for which paragraphs[minIndex] has been fetched
	maxIndex: int  # Largest value for which paragraphs[maxIndex] has been fetched
	currentPos: IndexAndOffset
	caret: IndexAndOffset
	caretInfo: textInfos.TextInfo
	regex: re.Pattern
	extractStyleFunc: ExtractStyleFunc
	styleCompatibilityFunc: StyleCompatibilityFunc

	def __init__(
			self,
			caretInfo: textInfos.TextInfo,
			regex: re.Pattern = None,
	):
		self.extractStyleFunc, self.styleCompatibilityFunc = getStyleAndCompatibilityFuncs()
		paragraphInfo = caretInfo.copy()
		paragraphInfo.collapse()
		paragraphInfo.expand(getParagraphUnitForTextInfo(paragraphInfo))
		self.paragraphs = {0: ContextParagraph(paragraphInfo, self.extractStyleFunc)}
		preInfo = paragraphInfo.copy()
		preInfo.setEndPoint(caretInfo, "endToEnd")
		self.currentPos = IndexAndOffset(0, len(preInfo.text))
		self.caret = IndexAndOffset(0, len(preInfo.text))
		self.caretInfo = caretInfo
		self.minIndex = self.maxIndex = 0
		if regex is None:
			regex = getSentenceStopRegex()
		self.regex = regex

	def get(self, i: int) -> ContextParagraph:
		try:
			return self.paragraphs[i]
		except KeyError:
			pass
		if i > 0:
			j = i - 1
		else:
			j = i + 1
		anchorParagraph = self.get(j)
		if anchorParagraph is None:
			return None
		newParagraph = moveParagraph(anchorParagraph.textInfo, i - j)
		if newParagraph is None:
			return None
		result = ContextParagraph(newParagraph, self.extractStyleFunc)
		if not self.styleCompatibilityFunc(anchorParagraph .style, result.style):
			return None
		self.paragraphs[i] = result
		self.minIndex = min(self.minIndex, i)
		self.maxIndex = max(self.maxIndex, i)
		return result

	def computeParagraphStartIndices(self) -> list[int]:
		parStartIndices = {self.minIndex: 0}
		for i in range(self.minIndex + 1, self.maxIndex + 2):
			parStartIndices[i] = parStartIndices[i - 1] + self.paragraphs[i - 1].pythonicLen + len(self.SEPARATOR)
		return parStartIndices

	def stringIndexToIndexAndOffset(
			self,
			index: int,
			parStartIndices: list[int],
	) -> IndexAndOffset:
		paragraphIndex: int = bisect_right_dict(parStartIndices, index) - 1
		offset = index - parStartIndices[paragraphIndex]
		return IndexAndOffset(paragraphIndex=paragraphIndex, offset=offset)

	def indexAndOffsetToStringIndex(
			self,
			io: IndexAndOffset,
			parStartIndices: list[int]
	) -> int:
		return parStartIndices[io.paragraphIndex] + io.offset
	
	def indexAndOffsetToTextInfo(
			self,
			io: IndexAndOffset,
	) -> textInfos.TextInfo:
		return self.paragraphs[io.paragraphIndex].textInfo.moveToCodepointOffset(io.offset)

	def FindSentenceResultToTextInfo(
			self,
			fsr: FindSentenceResult | None,
	) -> textInfos.TextInfo:
		if fsr is None:
			return None
		textInfo = self.indexAndOffsetToTextInfo(fsr.start)
		endTextInfo = self.indexAndOffsetToTextInfo(fsr.end)
		textInfo.setEndPoint(endTextInfo, which="endToEnd")
		return textInfo

	def findCurrentSentence(self) -> FindSentenceResult:
		"""
			This function finds current sentence among paragraphs already present in this context.
			This function doesn't expand the context, although within its return value it provides recommendation
			on whether to expand either start or end of context based on whether the resulting sentence touches
			# the corresponding endpoint.
		"""
		text = self.SEPARATOR.join(self.paragraphs[i].text for i in range(self.minIndex, self.maxIndex + 1))

		# parStartIndices Denotes indices in s where new paragraphs start in text.
		# These are pythonic indices of characters within text string.
		parStartIndices = self.computeParagraphStartIndices()
		caretIndex = self.indexAndOffsetToStringIndex(self.currentPos, parStartIndices)
		sentenceBoundaries: list[int] = [m.end() for m in self.regex.finditer(text)]
		# Dedupe list as sometimes there are duplicate matches near the end.
		sentenceBoundaries = sorted(list(set(sentenceBoundaries)))
		if len(sentenceBoundaries) == 0:
			raise RuntimeError("Found no sentence boundaries")
		elif len(sentenceBoundaries) == 1:
			# we must be working with empty context. Return the entire context as a single sentence.
			return FindSentenceResult(
				start=self.stringIndexToIndexAndOffset(0, parStartIndices),
				end=self.stringIndexToIndexAndOffset(len(text), parStartIndices),
				shouldExpandStart=True,
				shouldExpandEnd=True,
				sentenceText="",
			)
		# Use bisection to find indices i and j, such that current sentence is
		# defined by indices sentenceBoundaries[i] ... sentenceBoundaries[j].
		j: int = bisect.bisect_right(sentenceBoundaries, caretIndex)
		if j >= len(sentenceBoundaries):
			# This can happen if the cursor is at the last position of the line or document.
			j -= 1
		i: int = j - 1
		sentenceText = text[sentenceBoundaries[i]:sentenceBoundaries[j]]

		return FindSentenceResult(
			start=self.stringIndexToIndexAndOffset(sentenceBoundaries[i], parStartIndices),
			end=self.stringIndexToIndexAndOffset(sentenceBoundaries[j], parStartIndices),
			shouldExpandStart=sentenceBoundaries[i] == 0,
			shouldExpandEnd=sentenceBoundaries[j] == len(text),
			sentenceText=sentenceText,
		)
	
	def expandCurrentSentence(self, direction: int = 0) -> FindSentenceResult:
		"""
			Expands context if necessary, to make sure, that if sentence spans across multiple paragraphs,
			we capture that sentence completely.
			For example, if we're moving forward (direction==1), then we check if the end of the sentence is
			touching the end of the last paragraph of the context. If it is the case,
			then we expand our context forward, and find current sentence again.
			We repeat this process until we either reach the end of the document, or we reach a paragraph,
			that is incompatible due to different formatting, or until the end of current sentence is
			no longer touching the end of the last paragraph.
		"""
		if direction == 0:
			# Expand both forward and backward
			self.expandCurrentSentence(-1)
			return self.expandCurrentSentence(1)
		MAX_EXPANSION_ATTEMPTS = 1000
		for __ in range(MAX_EXPANSION_ATTEMPTS):
			result = self.findCurrentSentence()
			if (
				(direction > 0 and not result.shouldExpandEnd)
				or (direction < 0 and not result.shouldExpandStart)
			):
				return result
			
			nextParagraph = self.get(self.maxIndex + 1 if direction > 0 else self.minIndex - 1)
			if nextParagraph is None:
				return result

	def moveSentence(self, direction: int) -> textInfos.TextInfo | None:
		"""
			This function either retrieves current sentence when direction = 0, or
			moves to previous/next sentence when direction is not 0.
			Please note that this function can only retrieve immediate previous/immediate next sentences.
		"""
		result = self.expandCurrentSentence(direction)
		if direction == 0:
			textInfo = self.FindSentenceResultToTextInfo(result)
			return textInfo
		elif (
			(direction > 0 and result.shouldExpandEnd)
			or (direction < 0 and result.shouldExpandStart)
		):
			# It is possible that the next paragraph is incompatible, in which case we need to move textInfo there
			# and create a new SentenceContext.
			textInfo = moveParagraph(self.paragraphs[self.maxIndex].textInfo, direction)
			if textInfo is None:
				return None
			textInfo.collapse(end=direction < 0)
			if direction < 0:
				result = textInfo.move(textInfos.UNIT_CHARACTER, -1)
				if result == 0:
					return None
			newContext = SentenceContext(textInfo, self.regex, self.extractStyleFunc, self.styleCompatibilityFunc)
			return self.indexAndOffsetToTextInfo(
				newContext.expandCurrentSentence(direction)
			)
		else:
			# There is likely another sentence available within the same context. Move currentPos to either end
			# or start - 1 in order to retrieve next/previous sentence
			# from this context.
			if direction > 0:
				self.currentPos = result.end
			else:
				# This case is more complicated, since we need to move back 1 character from result.start.
				parStartIndices = self.computeParagraphStartIndices()
				index = self.indexAndOffsetToStringIndex(result.start, parStartIndices)
				if index in parStartIndices:
					# We need to be mindful of extra \n character added between paragraphs.
					# So in this case we skip over fake \n character plus one more real character from the string.
					index -= 2
				else:
					index -= 1
				if index < 0:
					raise RuntimeError("index supposed to stay positive")
				self.currentPos = self.stringIndexToIndexAndOffset(index, parStartIndices)
			return self.FindSentenceResultToTextInfo(self.expandCurrentSentence(direction))
