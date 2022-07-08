# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2010-2021 NV Access Limited, World Light Information Limited,
# Hong Kong Blind Union, Babbage B.V., Julien Cochuyt
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from enum import IntEnum
import os
import codecs
import collections
import re
from logHandler import log
import globalVars
import config

class LocaleDataMap(object):
	"""Allows access to locale-specific data objects, dynamically loading them if needed on request"""

	def __init__(self,localeDataFactory):
		"""
		@param localeDataFactory: the factory to create data objects for the requested locale.
		""" 
		self._localeDataFactory=localeDataFactory
		self._dataMap={}

	def fetchLocaleData(self,locale,fallback=True):
		"""
		Fetches a data object for the given locale. 
		This may mean that the data object is first created and stored if it does not yet exist in the map.
		The locale is also simplified (country is dropped) if the fallback argument is True and the full locale can not be used to create a data object.
		@param locale: the locale of the data object requested
		@type locale: string
		@param fallback: if true and there is no data for the locale, then the country (if it exists) is stripped and just the language is tried.
		@type fallback: boolean
		@return: the data object for the given locale
		"""
		localeList=[locale]
		if fallback and '_' in locale:
			localeList.append(locale.split('_')[0])
		for l in localeList:
			data=self._dataMap.get(l)
			if data: return data
			try:
				data=self._localeDataFactory(l)
			except LookupError:
				data=None
			if not data: continue
			self._dataMap[l]=data
			return data
		raise LookupError(locale)

	def invalidateLocaleData(self, locale):
		"""Invalidate the data object (if any) for the given locale.
		This will cause a new data object to be created when this locale is next requested.
		@param locale: The locale for which the data object should be invalidated.
		@type locale: str
		"""
		try:
			del self._dataMap[locale]
		except KeyError:
			pass

	def invalidateAllData(self):
		"""Invalidate all data within this locale map.
		This will cause a new data object to be created for every locale that is next requested.
		"""
		self._dataMap.clear()

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
		fileName = os.path.join(globalVars.appDir, 'locale', locale, 'characterDescriptions.dic')
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
		Looks up the given character and returns a list containing all the description strings found.
		"""
		return self._entries.get(character)

_charDescLocaleDataMap=LocaleDataMap(CharacterDescriptions)

def getCharacterDescription(locale,character):
	"""
	Finds a description or examples for the given character, which makes sence in the given locale.
	@param locale: the locale (language[_COUNTRY]) the description should be for.
	@type locale: string
	@param character: the character  who's description should be retreaved.
	@type character: string
	@return:  the found description for the given character
	@rtype: list of strings
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
class SymbolLevel(IntEnum):
	NONE = 0
	SOME = 100
	MOST = 200
	ALL = 300
	CHAR = 1000
	UNCHANGED = -1


SPEECH_SYMBOL_LEVEL_LABELS = {
	# Translators: The level at which the given symbol will be spoken.
	SymbolLevel.NONE: pgettext("symbolLevel", "none"),
	# Translators: The level at which the given symbol will be spoken.
	SymbolLevel.SOME: pgettext("symbolLevel", "some"),
	# Translators: The level at which the given symbol will be spoken.
	SymbolLevel.MOST: pgettext("symbolLevel", "most"),
	# Translators: The level at which the given symbol will be spoken.
	SymbolLevel.ALL: pgettext("symbolLevel", "all"),
	# Translators: The level at which the given symbol will be spoken.
	SymbolLevel.CHAR: pgettext("symbolLevel", "character"),
}
CONFIGURABLE_SPEECH_SYMBOL_LEVELS = (SymbolLevel.NONE, SymbolLevel.SOME, SymbolLevel.MOST, SymbolLevel.ALL)
SPEECH_SYMBOL_LEVELS = CONFIGURABLE_SPEECH_SYMBOL_LEVELS + (SymbolLevel.CHAR,)

# Speech symbol preserve modes
SYMPRES_NEVER = 0
SYMPRES_ALWAYS = 1
SYMPRES_NOREP = 2
SPEECH_SYMBOL_PRESERVE_LABELS = {
	# Translators: An option for when a symbol itself will be sent to the synthesizer.
	# See the "Punctuation/symbol pronunciation" section of the User Guide for details.
	SYMPRES_NEVER: pgettext("symbolPreserve", "never"),
	# Translators: An option for when a symbol itself will be sent to the synthesizer.
	# See the "Punctuation/symbol pronunciation" section of the User Guide for details.
	SYMPRES_ALWAYS: pgettext("symbolPreserve", "always"),
	# Translators: An option for when a symbol itself will be sent to the synthesizer.
	# See the "Punctuation/symbol pronunciation" section of the User Guide for details.
	SYMPRES_NOREP: pgettext("symbolPreserve", "only below symbol's level"),
}
SPEECH_SYMBOL_PRESERVES = (SYMPRES_NEVER, SYMPRES_ALWAYS, SYMPRES_NOREP)

class SpeechSymbol(object):
	__slots__ = ("identifier", "pattern", "replacement", "level", "preserve", "displayName")

	def __init__(self, identifier, pattern=None, replacement=None, level=None, preserve=None, displayName=None):
		self.identifier = identifier
		self.pattern = pattern
		self.replacement = replacement
		self.level = level
		self.preserve = preserve
		self.displayName = displayName

	def __repr__(self):
		attrs = []
		for attr in self.__slots__:
			attrs.append("{name}={val!r}".format(
				name=attr, val=getattr(self, attr)))
		return "SpeechSymbol(%s)" % ", ".join(attrs)

class SpeechSymbols(object):
	"""
	Contains raw information about the pronunciation of symbols.
	It does not handle inheritance of data from other sources, processing of text, etc.
	This is all handled by L{SpeechSymbolProcessor}.
	"""

	def __init__(self):
		"""Constructor.
		"""
		self.complexSymbols = collections.OrderedDict()
		self.symbols = collections.OrderedDict()
		self.fileName = None

	def load(self, fileName, allowComplexSymbols=True):
		"""Load symbol information from a file.
		@param fileName: The name of the file from which to load symbol information.
		@type fileName: str
		@param allowComplexSymbols: Whether to allow complex symbols.
		@type allowComplexSymbols: bool
		@raise IOError: If the file cannot be read.
		"""
		self.fileName = fileName
		with codecs.open(fileName, "r", "utf_8_sig", errors="replace") as f:
			handler = None
			for line in f:
				if line.isspace() or line.startswith("#"):
					# Whitespace or comment.
					continue
				line = line.rstrip("\r\n")
				try:
					if line == "complexSymbols:" and allowComplexSymbols:
						handler = self._loadComplexSymbol
					elif line == "symbols:":
						handler = self._loadSymbol
					elif handler:
						# This is a line within a section, so handle it according to which section we're in.
						handler(line)
					else:
						raise ValueError
				except ValueError:
					log.warning(u"Invalid line in file {file}: {line}".format(
						file=fileName, line=line))

	def _loadComplexSymbol(self, line):
		try:
			identifier, pattern = line.split("\t")
		except TypeError:
			raise ValueError
		self.complexSymbols[identifier] = pattern

	def _loadSymbolField(self, input, inputMap=None):
		if input == "-":
			# Default.
			return None
		if not inputMap:
			return input
		try:
			return inputMap[input]
		except KeyError:
			raise ValueError

	IDENTIFIER_ESCAPES_INPUT = {
		"0": "\0",
		"t": "\t",
		"n": "\n",
		"r": "\r",
		"f": "\f",
		"v": "\v",
		"#": "#",
		"\\": "\\",
	}
	IDENTIFIER_ESCAPES_OUTPUT = {v: k for k, v in IDENTIFIER_ESCAPES_INPUT.items()}
	LEVEL_INPUT = {
		"none": SymbolLevel.NONE,
		"some": SymbolLevel.SOME,
		"most": SymbolLevel.MOST,
		"all": SymbolLevel.ALL,
		"char": SymbolLevel.CHAR,
	}
	LEVEL_OUTPUT = {v:k for k, v in LEVEL_INPUT.items()}
	PRESERVE_INPUT = {
		"never": SYMPRES_NEVER,
		"always": SYMPRES_ALWAYS,
		"norep": SYMPRES_NOREP,
	}
	PRESERVE_OUTPUT = {v: k for k, v in PRESERVE_INPUT.items()}

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
			if identifier.startswith("\\") and len(identifier) >= 2:
				identifier = self.IDENTIFIER_ESCAPES_INPUT.get(identifier[1], identifier[1]) + identifier[2:]
			replacement = self._loadSymbolField(next(line))
		except StopIteration:
			# These fields are mandatory.
			raise ValueError
		try:
			level = self._loadSymbolField(next(line), self.LEVEL_INPUT)
			preserve = self._loadSymbolField(next(line), self.PRESERVE_INPUT)
		except StopIteration:
			# These fields are optional. Defaults will be used for unspecified fields.
			pass
		self.symbols[identifier] = SpeechSymbol(identifier, None, replacement, level, preserve, displayName)

	def save(self, fileName=None):
		"""Save symbol information to a file.
		@param fileName: The name of the file to which to save symbol information,
			C{None} to use the file name last passed to L{load} or L{save}.
		@type fileName: str
		@raise IOError: If the file cannot be written.
		@raise ValueError: If C{fileName} is C{None}
			and L{load} or L{save} has not been called.
		"""
		if fileName:
			self.fileName = fileName
		elif self.fileName:
			fileName = self.fileName
		else:
			raise ValueError("No file name")

		with codecs.open(fileName, "w", "utf_8_sig", errors="replace") as f:
			if self.complexSymbols:
				f.write(u"complexSymbols:\r\n")
				for identifier, pattern in self.complexSymbols.items():
					f.write(u"%s\t%s\r\n" % (identifier, pattern))
				f.write(u"\r\n")

			if self.symbols:
				f.write(u"symbols:\r\n")
				for symbol in self.symbols.values():
					f.write(u"%s\r\n" % self._saveSymbol(symbol))

	def _saveSymbolField(self, output, outputMap=None):
		if output is None:
			return "-"
		if not outputMap:
			return output
		try:
			return outputMap[output]
		except KeyError:
			raise ValueError

	def _saveSymbol(self, symbol):
		identifier = symbol.identifier
		try:
			identifier = u"\\%s%s" % (
				self.IDENTIFIER_ESCAPES_OUTPUT[identifier[0]], identifier[1:])
		except KeyError:
			pass
		fields = [identifier,
			self._saveSymbolField(symbol.replacement),
			self._saveSymbolField(symbol.level, self.LEVEL_OUTPUT),
			self._saveSymbolField(symbol.preserve, self.PRESERVE_OUTPUT)
		]
		# Strip optional fields with default values.
		for field in reversed(fields[2:]):
			if field == "-":
				del fields[-1]
			else:
				# This field specifies a value, so no more fields can be stripped.
				break
		if symbol.displayName:
			fields.append("# %s" % symbol.displayName)
		return u"\t".join(fields)

_noSymbolLocalesCache = set()
def _getSpeechSymbolsForLocale(locale):
	if locale in _noSymbolLocalesCache:
		raise LookupError
	builtin = SpeechSymbols()
	if config.conf['speech']['includeCLDR']:
		# Try to load CLDR data when processing is on.
		# Load the data before loading other symbols,
		# in order to allow translators to override them.
		try:
			builtin.load(
				os.path.join(globalVars.appDir, "locale", locale, "cldr.dic"),
				allowComplexSymbols=False
			)
		except IOError:
			log.debugWarning("No CLDR data for locale %s" % locale)
	try:
		builtin.load(os.path.join(globalVars.appDir, "locale", locale, "symbols.dic"))
	except IOError:
		_noSymbolLocalesCache.add(locale)
		raise LookupError("No symbol information for locale %s" % locale)
	user = SpeechSymbols()
	try:
		# Don't allow users to specify complex symbols
		# because an error will cause the whole processor to fail.
		user.load(os.path.join(globalVars.appArgs.configPath, "symbols-%s.dic" % locale),
			allowComplexSymbols=False)
	except IOError:
		# An empty user SpeechSymbols is okay.
		pass
	return builtin, user

class SpeechSymbolProcessor(object):
	"""
	Handles processing of symbol pronunciation for a locale.
	Pronunciation information is taken from one or more L{SpeechSymbols} instances.
	"""

	#: Caches symbol data for locales.
	localeSymbols = LocaleDataMap(_getSpeechSymbolsForLocale)

	def __init__(self, locale):
		"""Constructor.
		@param locale: The locale for which symbol pronunciation should be processed.
		@type locale: str
		"""
		self.locale = locale

		# We need to merge symbol data from several sources.
		sources = self.sources = []
		builtin, user = self.localeSymbols.fetchLocaleData(locale,fallback=False)
		self.builtinSources = [builtin]
		self.userSymbols = user
		sources.append(user)
		sources.append(builtin)

		# Always use English as a base.
		if locale != "en":
			# Only the builtin data.
			enBaseSymbols = self.localeSymbols.fetchLocaleData("en")[0]
			sources.append(enBaseSymbols)
			self.builtinSources.append(enBaseSymbols)

		# The computed symbol information from all sources.
		symbols = self.computedSymbols = collections.OrderedDict()
		# An indexable list of complex symbols for use in building/executing the regexp.
		complexSymbolsList = self._computedComplexSymbolsList = []
		# A list of multi-character simple symbols for use in building the regexp.
		multiChars = []
		# A list of single character symbols for use in building the regexp.
		characters = []

		# Add all complex symbols first, as they take priority.
		for source in sources:
			for identifier, pattern in source.complexSymbols.items():
				if identifier in symbols:
					# Already defined.
					continue
				symbol = SpeechSymbol(identifier, pattern)
				symbols[identifier] = symbol
				complexSymbolsList.append(symbol)

		# Supplement the data for complex symbols and add all simple symbols.
		for source in sources:
			for identifier, sourceSymbol in source.symbols.items():
				try:
					symbol = symbols[identifier]
					# We're updating an already existing symbol.
				except KeyError:
					# This is a new simple symbol.
					# (All complex symbols have already been added.)
					symbol = symbols[identifier] = SpeechSymbol(identifier)
					if len(identifier) == 1:
						characters.append(identifier)
					else:
						multiChars.append(identifier)
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
		# As the symbols dictionary changes during iteration, wrap this inside a list call.
		for symbol in list(symbols.values()):
			if symbol.replacement is None:
				# Symbols without a replacement specified are useless.
				log.warning(u"Replacement not defined in locale {locale} for symbol: {symbol}".format(
					symbol=symbol.identifier, locale=self.locale))
				del symbols[symbol.identifier]
				try:
					if len(symbol.identifier) == 1:
						characters.remove(symbol.identifier)
					else:
						multiChars.remove(symbol.identifier)
				except ValueError:
					pass
				try:
					complexSymbolsList.remove(symbol)
				except ValueError:
					pass
				continue
			if symbol.level is None:
				symbol.level = SymbolLevel.ALL
			if symbol.preserve is None:
				symbol.preserve = SYMPRES_NEVER
			if symbol.displayName is None:
				symbol.displayName = symbol.identifier

		# Make characters into a regexp character set.
		characters = "[%s]" % re.escape("".join(characters))
		# The simple symbols must be ordered longest first so that the longer symbols will match.
		multiChars.sort(key=lambda identifier: len(identifier), reverse=True)

		# Build the regexp.
		patterns = [
			# Strip repeated spaces from the end of the line to stop them from being picked up by repeated.
			r"(?P<rstripSpace>  +$)",
			# Repeated characters: more than 3 repeats.
			r"(?P<repeated>(?P<repTmp>%s)(?P=repTmp){3,})" % characters
		]
		# Complex symbols.
		# Each complex symbol has its own named group so we know which symbol matched.
		patterns.extend(
			u"(?P<c{index}>{pattern})".format(index=index, pattern=symbol.pattern)
			for index, symbol in enumerate(complexSymbolsList))
		# Simple symbols.
		# These are all handled in one named group.
		# Because the symbols are just text, we know which symbol matched just by looking at the matched text.
		patterns.append(r"(?P<simple>{multiChars}|{singleChars})".format(
			multiChars="|".join(re.escape(identifier) for identifier in multiChars),
			singleChars=characters
		))
		pattern = "|".join(patterns)
		try:
			self._regexp = re.compile(pattern, re.UNICODE)
		except re.error as e:
			log.error("Invalid complex symbol regular expression in locale %s: %s" % (locale, e))
			raise LookupError

	def _replaceGroups(self, m: re.Match, string: str) -> str:
		"""Replace matching group references (\\1, \\2, ...) with the corresponding matched groups.
		Also replace \\\\ with \\ and reject other escapes, for escaping coherency.
		@param m: The currently-matched group
		@param string: The match replacement string which may contain group references
		"""
		result = ''

		in_escape = False
		for char in string:
			if not in_escape:
				if char == '\\':
					in_escape = True
				else:
					result += char
			else:
				if char == '\\':
					result += '\\'
				elif char >= '0' and char <= '9':
					result += m.group(m.lastindex + ord(char) - ord('0'))
				else:
					log.error("Invalid reference \\%string" % char)
					raise LookupError
				in_escape = False
		if in_escape:
			log.error("Unterminated backslash")
			raise LookupError
		return result

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
				replacement = symbol.replacement
			else:
				# Complex symbol.
				index = int(group[1:])
				symbol = self._computedComplexSymbolsList[index]
				replacement = self._replaceGroups(m, symbol.replacement)

			if symbol.preserve == SYMPRES_ALWAYS or (symbol.preserve == SYMPRES_NOREP and self._level < symbol.level):
				suffix = text
			else:
				suffix = " "
			if self._level >= symbol.level and replacement:
				return u" {repl}{suffix}".format(repl=replacement, suffix=suffix)
			else:
				return suffix

	def processText(self, text, level):
		self._level = level
		return self._regexp.sub(self._regexpRepl, text)

	def updateSymbol(self, newSymbol):
		"""Update information for a symbol if it has changed.
		If there is a change, the changed information will be added to the user's symbol data.
		These changes do not take effect until the symbol processor is reinitialised.
		@param newSymbol: The symbol to update.
		@type newSymbol: L{SpeechSymbol}
		@return: Whether there was a change.
		@rtype: bool
		"""
		identifier = newSymbol.identifier
		try:
			oldSymbol = self.computedSymbols[identifier]
		except KeyError:
			oldSymbol = None
		if oldSymbol is newSymbol:
			return False
		try:
			userSymbol = self.userSymbols.symbols[identifier]
		except KeyError:
			userSymbol = SpeechSymbol(identifier)

		changed = False
		if oldSymbol and newSymbol.pattern != oldSymbol.pattern:
			userSymbol.pattern = newSymbol.pattern
			changed = True
		if not oldSymbol or newSymbol.replacement != oldSymbol.replacement:
			userSymbol.replacement = newSymbol.replacement
			changed = True
		if not oldSymbol or newSymbol.level != oldSymbol.level:
			userSymbol.level = newSymbol.level
			changed = True
		if not oldSymbol or newSymbol.preserve != oldSymbol.preserve:
			userSymbol.preserve = newSymbol.preserve
			changed = True
		if not oldSymbol or newSymbol.displayName != oldSymbol.displayName:
			userSymbol.displayName = newSymbol.displayName
			changed = True

		if not changed:
			return False

		# Do this in case the symbol wasn't in userSymbols before.
		self.userSymbols.symbols[identifier] = userSymbol
		return True

	def deleteSymbol(self, symbol):
		"""Delete a user defined symbol.
		If the symbol does not exist, this method simply does nothing.
		These changes do not take effect until the symbol processor is reinitialised.
		@param symbol: The symbol to delete.
		@type symbol: L{SpeechSymbol}
		"""
		try:
			del self.userSymbols.symbols[symbol.identifier]
		except KeyError:
			pass

	def isBuiltin(self, symbolIdentifier):
		"""Determine whether a symbol is built in.
		@param symbolIdentifier: The identifier of the symbol in question.
		@type symbolIdentifier: str
		@return: C{True} if the symbol is built in,
			C{False} if it was added by the user.
		@rtype: bool
		"""
		return any(symbolIdentifier in source.symbols for source in self.builtinSources)

_localeSpeechSymbolProcessors = LocaleDataMap(SpeechSymbolProcessor)


def processSpeechSymbols(locale: str, text: str, level: SymbolLevel):
	"""Process some text, converting symbols according to desired pronunciation.
	@param locale: The locale of the text.
	@param text: The text to process.
	@param level: The symbol level to use.
	"""
	try:
		ss = _localeSpeechSymbolProcessors.fetchLocaleData(locale)
	except LookupError:
		if not locale.startswith("en_"):
			return processSpeechSymbols("en", text, level)
		raise
	return ss.processText(text, level)

def processSpeechSymbol(locale, symbol):
	"""Process a single symbol according to desired pronunciation.
	@param locale: The locale of the symbol.
	@type locale: str
	@param symbol: The symbol.
	@type symbol: str
	"""
	try:
		ss = _localeSpeechSymbolProcessors.fetchLocaleData(locale)
	except LookupError:
		if not locale.startswith("en_"):
			return processSpeechSymbol("en", symbol)
		raise
	try:
		return ss.computedSymbols[symbol].replacement
	except KeyError:
		pass
	return symbol

def clearSpeechSymbols():
	"""Clears the symbol data cached by the locale speech symbol processors.
	This will cause new data to be fetched for the next request to pronounce symbols.
	"""
	SpeechSymbolProcessor.localeSymbols.invalidateAllData()
	_localeSpeechSymbolProcessors.invalidateAllData()

def handlePostConfigProfileSwitch(prevConf=None):
	if not prevConf:
		return
	if prevConf["speech"]["includeCLDR"] is not config.conf["speech"]["includeCLDR"]:
		# Either included or excluded CLDR data, so clear the cache.
		clearSpeechSymbols()

config.post_configProfileSwitch.register(handlePostConfigProfileSwitch)
