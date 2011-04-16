#characterProcessing.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2010-2011 NV Access Inc, World Light Information Limited, Hong Kong Blind Union
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import time
import os
import codecs
import collections
import re
from logHandler import log

class LocaleDataMap(object):
	"""Allows access to locale-specific data objects, dynamically loading them if needed on request"""

	def __init__(self,localeDataClass):
		"""
		@param localeDataClass: this class will be used to instanciate data objects representing the requested locale.
		""" 
		self._localeDataClass=localeDataClass
		self._dataMap={}

	def fetchLocaleData(self,locale):
		"""
		Fetches a data object for the given locale. 
		This may mean that the data object is first created and sotred if it does not yet exist in the map.
		The locale is also simplified (country is dropped) if the full locale can not be used to instanciate a data object.
		@param locale: the locale of the data object requested
		@type locale: string
		@return: the data object for the given locale
		"""
		localeList=[locale]
		if '_' in locale:
			localeList.append(locale.split('_')[0])
		for l in localeList:
			data=self._dataMap.get(l)
			if data: return data
			try:
				data=self._localeDataClass(l)
			except LookupError:
				data=None
			if not data: continue
			self._dataMap[l]=data
			return data
		raise LookupError(locale)

class CharacterDescriptions(object):
	"""
	Represents a map of characters to one or more descriptions (examples) for that character.
	The data is loaded from a file from the requested locale.
	"""

	def __init__(self,locale):
		"""
		@param locale: The characterDescriptions.dic file will be found by using this locale.
		@type locale: string
		"""
		self._entries = {}
		fileName=os.path.join('locale',locale,'characterDescriptions.dic')
		if not os.path.isfile(fileName): 
			raise LookupError(fileName)
		f = codecs.open(fileName,"r","utf_8_sig",errors="replace")
		for line in f:
			if line.isspace() or line.startswith('#'):
				continue
			line=line.rstrip('\r\n')
			temp=line.split("\t")
			if len(temp) > 1:
				key=temp.pop(0)
				self._entries[key] = temp
			else:
				log.warning("can't parse line '%s'" % line)
		log.debug("Loaded %d entries." % len(self._entries))
		f.close()

	def getCharacterDescription(self, character):
		"""
		Looks up the given character and returns a string containing all the descriptions found.
		"""
		desc=self._entries.get(character)
		if not desc: return None
		return u"\u3002".join(desc)

_charDescLocaleDataMap=LocaleDataMap(CharacterDescriptions)

def getCharacterDescription(locale,character):
	"""
	Finds a description or example for the given character, which makes sence in the given locale.
	@param locale: the locale (language[_COUNTRY]) the description should be for.
	@type locale: string
	@param character: the character  who's description should be retreaved.
	@type character: string
	@return:  the found description for the given character
	@rtype: string
	"""
	try:
		l=_charDescLocaleDataMap.fetchLocaleData(locale)
	except LookupError:
		if not locale.startswith('en'):
			return getCharacterDescription('en',character)
		raise LookupError("en")
	desc=l.getCharacterDescription(character)
	if not desc and not locale.startswith('en'):
		desc=getCharacterDescription('en',character)
	return desc
 
# Speech symbol levels
SYMLVL_NONE = 0
SYMLVL_SOME = 100
SYMLVL_MOST = 200
SYMLVL_ALL = 300
SYMLVL_CHAR = 1000
SPEECH_SYMBOL_LEVELS = {
	"none": SYMLVL_NONE,
	"some": SYMLVL_SOME,
	"most": SYMLVL_MOST,
	"all": SYMLVL_ALL,
	"char": SYMLVL_CHAR,
}
USER_SPEECH_SYMBOL_LEVELS = collections.OrderedDict((
	(SYMLVL_NONE, _("none")),
	(SYMLVL_SOME, _("some")),
	(SYMLVL_MOST, _("most")),
	(SYMLVL_ALL, _("all")),
))

class SpeechSymbol(object):
	__slots__ = ("identifier", "pattern", "replacement", "level", "preserve", "displayName")

	def __init__(self, identifier, pattern=None, replacement=None, level=None, preserve=None, displayName=None):
		self.identifier = identifier
		self.pattern = pattern
		self.replacement = replacement
		self.level = level
		self.preserve = preserve
		self.displayName = displayName

class SpeechSymbols(object):
	"""
	Handles pronunciation of symbols.
	The data is loaded from a file for the requested locale.
	"""

	def __init__(self, locale):
		"""Constructor.
		@param locale: The locale for which to load symbol information.
		@type locale: str
		@raise LookupError: If there is no symbol information for this locale.
		"""
		self.locale = locale

		fileName = os.path.join("locale", locale, "symbols.dic")
		if not os.path.isfile(fileName): 
			raise LookupError("No symbol information for locale %s" % locale)

		self.rawComplexSymbols = collections.OrderedDict()
		self.rawSymbols = []

		# Read data from file.
		with codecs.open(fileName, "r", "utf_8_sig", errors="replace") as f:
			handler = None
			for line in f:
				if line.isspace() or line.startswith("#"):
					# Whitespace or comment.
					continue
				line = line.rstrip("\r\n")
				if line == "complexSymbols:":
					handler = self._loadComplexSymbol
				elif line == "symbols:":
					handler = self._loadSymbol
				elif handler:
					# This is a line within a section, so handle it according to which section we're in.
					try:
						handler(line)
					except ValueError:
						log.warning("Invalid line %r" % line)
				else:
					log.warning("Invalid line %r" % line)

		self.initProcessor()

	def _loadComplexSymbol(self, line):
		try:
			identifier, pattern = line.split("\t")
		except TypeError:
			raise ValueError
		self.rawComplexSymbols[identifier] = pattern

	IDENTIFIER_ESCAPES = {
		"0": "\0",
		"t": "\t",
		"n": "\n",
		"r": "\r",
		"f": "\f",
		"v": "\v",
	}

	def _loadSymbol(self, line):
		line = line.split("\t")
		identifier = replacement = level = preserve = displayName = None
		if line[-1].startswith("#"):
			# Regardless of how many fields there are,
			# if the last field is a comment, it is the display name.
			displayName = line[-1][1:].lstrip()
			del line[-1]
		line = iter(line)
		try:
			identifier = next(line)
			if not identifier:
				# Empty identifier is not allowed.
				raise ValueError
			if len(identifier) == 2 and identifier.startswith("\\"):
				identifier = self.IDENTIFIER_ESCAPES.get(identifier[1], identifier[1])
			replacement = next(line)
			if replacement == "-":
				replacement = None
		except StopIteration:
			# These fields are mandatory.
			raise ValueError
		try:
			level = SPEECH_SYMBOL_LEVELS.get(next(line))
			preserve = next(line)
			if preserve == "always":
				preserve = True
			elif preserve == "never":
				preserve = False
			else:
				preserve = None
		except StopIteration:
			# These fields are optional. Defaults will be used for unspecified fields.
			pass
		self.rawSymbols.append(SpeechSymbol(identifier, None, replacement, level, preserve, displayName))

	def initProcessor(self):
		"""Initialise the symbol processor.
		"""
		# We need to merge symbol data from several sources, starting with this instance.
		sources = [self]
		# Always use English as a base.
		if self.locale != "en":
			sources.append(_speechSymbolsLocaleDataMap.fetchLocaleData("en"))

		# The computed symbol information from all sources.
		symbols = self.computedSymbols = collections.OrderedDict()
		# An indexable list of complex symbols for use in building/executing the regexp.
		complexSymbolsList = self._computedComplexSymbolsList = []
		# A list of simple symbol identifiers for use in building the regexp.
		simpleSymbolIdentifiers = []
		# Single character symbols.
		characters = set()

		# Add all complex symbols first, as they take priority.
		for source in sources:
			for identifier, pattern in source.rawComplexSymbols.iteritems():
				if identifier in symbols:
					# Already defined.
					continue
				symbol = SpeechSymbol(identifier, pattern)
				symbols[identifier] = symbol
				complexSymbolsList.append(symbol)

		# Supplement the data for complex symbols and add all simple symbols.
		for source in sources:
			for sourceSymbol in source.rawSymbols:
				identifier = sourceSymbol.identifier
				try:
					symbol = symbols[identifier]
					# We're updating an already existing symbol.
				except KeyError:
					# This is a new simple symbol.
					# (All complex symbols have already been added.)
					symbol = symbols[identifier] = SpeechSymbol(identifier)
					simpleSymbolIdentifiers.append(identifier)
					if len(identifier) == 1:
						characters.add(identifier)
				# If fields weren't explicitly specified, inherit the value from later sources.
				if symbol.replacement is None:
					symbol.replacement = sourceSymbol.replacement
				if symbol.level is None:
					symbol.level = sourceSymbol.level
				if symbol.preserve is None:
					symbol.preserve = sourceSymbol.preserve
				if symbol.displayName is None:
					symbol.displayName = sourceSymbol.displayName

		# Set defaults for any fields not explicitly set.
		for symbol in symbols.values():
			if symbol.replacement is None:
				# Complex symbols without a replacement specified are useless.
				del symbols[symbol.identifier]
				continue
			if symbol.level is None:
				symbol.level = SYMLVL_ALL
			if symbol.preserve is None:
				symbol.preserve = False
			if symbol.displayName is None:
				symbol.displayName = symbol.identifier

		characters = "".join(characters)

		# Build the regexp.
		patterns = [
			# Strip repeated spaces from the end of the line to stop them from being picked up by repeated.
			r"(?P<rstripSpace>  +$)",
			# Repeated characters: more than 3 repeats.
			r"(?P<repeated>(?P<repTmp>[%s])(?P=repTmp){3,})" % re.escape("".join(characters))
		]
		# Complex symbols.
		# Each complex symbol has its own named group so we know which symbol matched.
		patterns.extend(
			u"(?P<c{index}>{pattern})".format(index=index, pattern=symbol.pattern)
			for index, symbol in enumerate(complexSymbolsList))
		# Simple symbols.
		# These are all handled in one named group.
		# Because the symbols are just text, we know which symbol matched just by looking at the matched text.
		patterns.append(ur"(?P<simple>{})".format(
			"|".join(re.escape(identifier) for identifier in simpleSymbolIdentifiers)
		))
		pattern = "|".join(patterns)
		self._regexp = re.compile(pattern, re.UNICODE)

	def _regexpRepl(self, m):
		group = m.lastgroup

		if group == "rstripSpace":
			return ""

		elif group == "repeated":
			# Repeated character.
			text = m.group()
			symbol = self.computedSymbols[text[0]]
			if self._level >= symbol.level:
				return u" {count} {char} ".format(count=len(text), char=symbol.replacement)
			else:
				return " "

		else:
			# One of the defined symbols.
			text = m.group()
			if group == "simple":
				# Simple symbol.
				symbol = self.computedSymbols[text]
			else:
				# Complex symbol.
				index = int(group[1:])
				symbol = self._computedComplexSymbolsList[index]
			if symbol.preserve:
				suffix = text
			else:
				suffix = " "
			if self._level >= symbol.level and symbol.replacement:
				return u" {repl}{suffix}".format(repl=symbol.replacement, suffix=suffix)
			else:
				return suffix

	def processText(self, text, level):
		self._level = level
		return self._regexp.sub(self._regexpRepl, text)

_speechSymbolsLocaleDataMap = LocaleDataMap(SpeechSymbols)

def processSpeechSymbols(locale, text, level):
	"""Process some text, converting symbols according to desired pronunciation.
	@param locale: The locale of the text.
	@type locale: str
	@param text: The text to process.
	@type text: str
	@param level: The symbol level to use; one of the SYMLVL_* constants.
	"""
	try:
		ss = _speechSymbolsLocaleDataMap.fetchLocaleData(locale)
	except LookupError:
		if not locale.startswith("en"):
			return processSymbols("en", text)
		raise
	return ss.processText(text, level)

def processSpeechSymbol(locale, symbol):
	"""Process a single symbol according to desired pronunciation.
	@param locale: The locale of the symbol.
	@type locale: str
	@param symbol: The symbol.
	@type symbol: str
	"""
	if not symbol:
		return _("blank")
	try:
		ss = _speechSymbolsLocaleDataMap.fetchLocaleData(locale)
	except LookupError:
		if not locale.startswith("en"):
			return processSymbols("en", text)
		raise
	try:
		return ss.computedSymbols[symbol].replacement
	except KeyError:
		pass
	return symbol
