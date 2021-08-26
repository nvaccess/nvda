# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2016-2021 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Utilities for converting NVDA speech sequences to XML.
Several synthesizers accept XML, either SSML or their own schemas.
L{SpeechXmlConverter} is the base class for conversion to XML.
You can subclass this to support specific XML schemas.
L{SsmlConverter} is an implementation for conversion to SSML.
"""

from collections import namedtuple, OrderedDict
import re
import speech
import textUtils
from speech.commands import SpeechCommand
from logHandler import log

XML_ESCAPES = {
	0x3C: u"&lt;", # <
	0x3E: u"&gt;", # >
	0x26: u"&amp;", # &
	0x22: u"&quot;", # "
}

# Regular expression to replace invalid XML characters.
# Based on http://stackoverflow.com/a/22273639
def _buildInvalidXmlRegexp():
	# Ranges of invalid characters.
	# Both start and end are inclusive; i.e. they are both themselves considered invalid.
	ranges = ((0x00, 0x08), (0x0B, 0x0C), (0x0E, 0x1F), (0x7F, 0x84), (0x86, 0x9F), (0xFDD0, 0xFDDF), (0xFFFE, 0xFFFF))
	rangeExprs = [u"%s-%s" % (chr(start), chr(end))
		for start, end in ranges]
	leadingSurrogate = u"[\uD800-\uDBFF]"
	trailingSurrogate = u"[\uDC00-\uDFFF]"
	return re.compile((
			# These ranges of characters are invalid.
			u"[{ranges}]"
			# Leading Unicode surrogate is invalid if not followed by trailing surrogate.
			u"|{leading}(?!{trailing})"
			# Trailing surrogate is invalid if not preceded by a leading surrogate.
			u"|(?<!{leading}){trailing}"
		).format(
			ranges="".join(rangeExprs),
			leading=leadingSurrogate,
			trailing=trailingSurrogate))

RE_INVALID_XML_CHARS = _buildInvalidXmlRegexp()
REPLACEMENT_CHAR = textUtils.REPLACEMENT_CHAR

def toXmlLang(nvdaLang):
	"""Convert an NVDA language to an XML language.
	"""
	return nvdaLang.replace("_", "-")

#: An XMLBalancer command to enclose the entire output in a tag.
#: This must be the first command.
EncloseAllCommand = namedtuple("EncloseAllCommand", ("tag", "attrs"))
#: An XMLBalancer command to set a tag attribute to a given value for subsequent output.
#: This attribute will be output with this value until a L{DelAttrCommand}.
SetAttrCommand = namedtuple("SetAttrCommand", ("tag", "attr", "val"))
#: An XmlBalancer command to remove a tag attribute for subsequent output.
#: If the tag has no remaining attributes, it will not be produced henceforth.
DelAttrCommand = namedtuple("DelAttrCommand", ("tag", "attr"))
#: An XmlBalancer command to directly enclose all text henceforth in a tag.
#: That is, the tag must always be the inner most tag.
#: This will occur until a L{StopEnclosingTextCommand}.
EncloseTextCommand = namedtuple("EncloseTextCommand", ("tag", "attrs"))
#: An XMLBalancer command to stop directly enclosing text henceforth in a tag.
StopEnclosingTextCommand = namedtuple("StopEnclosingTextCommand", ())
#: An XmlBalancer command to output a stand-alone tag.
#: That is, it will not enclose subsequent output.
StandAloneTagCommand = namedtuple("StandAloneTagCommand", ("tag", "attrs", "content"))

def _escapeXml(text):
	text = text.translate(XML_ESCAPES)
	text = RE_INVALID_XML_CHARS.sub(REPLACEMENT_CHAR, text)
	return text

class XmlBalancer(object):
	"""Generates balanced XML given a set of commands.
	NVDA speech sequences are linear, but XML is hierarchical, which makes conversion challenging.
	For example, a speech sequence might change the pitch, then change the volume, then reset the pitch to default.
	In XML, resetting to default generally requires closing the tag, but that also requires closing the outer tag.
	This class transparently handles these issues, balancing the XML as appropriate.
	To use, create an instance and call the L{generateXml} method.
	"""

	def __init__(self):
		#: The converted output as it is built.
		self._out = []
		#: A stack of open tags which enclose the entire output.
		self._enclosingAllTags = []
		#: Whether any tags have changed since last time they were output.
		self._tagsChanged = False
		#: A stack of currently open tags (excluding tags which enclose the entire output).
		self._openTags = []
		#: Current tags and their attributes.
		self._tags = OrderedDict()
		#: A tag (and its attributes) which should directly enclose all text henceforth.
		self._tagEnclosingText = (None, None)

	def _text(self, text):
		tag, attrs = self._tagEnclosingText
		if tag:
			self._openTag(tag, attrs)
		self._out.append(_escapeXml(text))
		if tag:
			self._closeTag(tag)

	def _openTag(self, tag, attrs, empty=False):
		self._out.append("<%s" % tag)
		for attr, val in attrs.items():
			self._out.append(' %s="' % attr)
			# Attribute values could be ints, floats etc, not just strings.
			# Therefore coerce the value to a string, as well as escaping xml characters. 
			self._out.append(_escapeXml(str(val)))
			self._out.append('"')
		self._out.append("/>" if empty else ">")

	def _closeTag(self, tag):
		self._out.append("</%s>" % tag)

	def _setAttr(self, tag, attr, val):
		attrs = self._tags.get(tag)
		if not attrs:
			attrs = self._tags[tag] = OrderedDict()
		if attrs.get(attr) != val:
			attrs[attr] = val
			self._tagsChanged = True

	def _delAttr(self, tag, attr):
		attrs = self._tags.get(tag)
		if not attrs:
			return
		if attr not in attrs:
			return
		del attrs[attr]
		if not attrs:
			del self._tags[tag]
		self._tagsChanged = True

	def _outputTags(self):
		if not self._tagsChanged:
			return
		# Just close all open tags and reopen any existing or new ones.
		for tag in reversed(self._openTags):
			self._closeTag(tag)
		del self._openTags[:]
		for tag, attrs in self._tags.items():
			self._openTag(tag, attrs)
			self._openTags.append(tag)
		self._tagsChanged = False

	def generateXml(self, commands):
		"""Generate XML from a sequence of balancer commands and text.
		"""
		for command in commands:
			if isinstance(command, str):
				self._outputTags()
				self._text(command)
			elif isinstance(command, EncloseAllCommand):
				self._openTag(command.tag, command.attrs)
				self._enclosingAllTags.append(command.tag)
			elif isinstance(command, SetAttrCommand):
				self._setAttr(command.tag, command.attr, command.val)
			elif isinstance(command, DelAttrCommand):
				self._delAttr(command.tag, command.attr)
			elif isinstance(command, EncloseTextCommand):
				self._tagEnclosingText = (command.tag, command.attrs)
			elif isinstance(command, StopEnclosingTextCommand):
				self._tagEnclosingText = (None, None)
			elif isinstance(command, StandAloneTagCommand):
				self._outputTags()
				self._openTag(command.tag, command.attrs, empty=not command.content)
				if command.content:
					self._text(command.content)
					self._closeTag(command.tag)
		# Close any open tags.
		for tag in reversed(self._openTags):
			self._closeTag(tag)
		for tag in self._enclosingAllTags:
			self._closeTag(tag)
		return u"".join(self._out)

class SpeechXmlConverter(object):
	"""Base class for conversion of NVDA speech sequences to XML.
	This class converts an NVDA speech sequence into XmlBalancer commands
	which can then be passed to L{XmlBalancer} to produce correct XML.

	The L{generateBalancerCommands} method takes a speech sequence
	and produces corresponding XmlBalancer commands.
	For convenience, callers can call L{convertToXml} with a speech sequence
	to generate XML using L{XmlBalancer}.

	Subclasses implement specific XML schemas by implementing methods which convert each speech command.
	The method for a speech command should be named with the prefix "convert" followed by the command's class name.
	For example, the handler for C{IndexCommand} should be named C{convertIndexCommand}.
	These methods receive the L{SpeechCommand} instance as their only argument.
	They should return an appropriate XmlBalancer command.
	Subclasses may wish to extend L{generateBalancerCommands}
	to produce additional XmlBalancer commands at the start or end;
	e.g. to add an L{EncloseAllCommand} at the start.
	"""

	def generateBalancerCommands(self, speechSequence):
		"""Generate appropriate XmlBalancer commands for a given speech sequence.
		@rtype: generator
		"""
		for item in speechSequence:
			if isinstance(item, str):
				yield item
			elif isinstance(item, SpeechCommand):
				name = type(item).__name__
				# For example: self.convertIndexCommand
				func = getattr(self, "convert%s" % name, None)
				if not func:
					log.debugWarning("Unsupported command: %s" % item)
					return
				command = func(item)
				if command is not None:
					yield command
			else:
				log.error("Unknown speech: %r" % item)

	def convertToXml(self, speechSequence):
		"""Convenience method to convert a speech sequence to XML using L{XmlBalancer}.
		"""
		bal = XmlBalancer()
		balCommands = self.generateBalancerCommands(speechSequence)
		return bal.generateXml(balCommands)

class SsmlConverter(SpeechXmlConverter):
	"""Converts an NVDA speech sequence to SSML.
	"""

	def __init__(self, defaultLanguage):
		self.defaultLanguage = toXmlLang(defaultLanguage)

	def generateBalancerCommands(self, speechSequence):
		attrs = OrderedDict((("version", "1.0"), ("xmlns", "http://www.w3.org/2001/10/synthesis"),
			("xml:lang", self.defaultLanguage)))
		yield EncloseAllCommand("speak", attrs)
		for command in super(SsmlConverter, self).generateBalancerCommands(speechSequence):
			yield command

	def convertIndexCommand(self, command):
		return StandAloneTagCommand("mark", {"name": command.index}, None)

	def convertCharacterModeCommand(self, command):
		if command.state:
			return EncloseTextCommand("say-as", {"interpret-as": "characters"})
		else:
			return StopEnclosingTextCommand()

	def convertLangChangeCommand(self, command):
		lang = command.lang or self.defaultLanguage
		lang = toXmlLang(lang)
		return SetAttrCommand("voice", "xml:lang", lang)

	def convertBreakCommand(self, command):
		return StandAloneTagCommand("break", {"time": "%dms" % command.time}, None)

	def _convertProsody(self, command, attr):
		if command.multiplier == 1:
			# Returning to normal.
			return DelAttrCommand("prosody", attr)
		else:
			return SetAttrCommand("prosody", attr,
				"%d%%" % int(command.multiplier* 100))

	def convertPitchCommand(self, command):
		return self._convertProsody(command, "pitch")
	def convertRateCommand(self, command):
		return self._convertProsody(command, "rate")
	def convertVolumeCommand(self, command):
		return self._convertProsody(command, "volume")

	def convertPhonemeCommand(self, command):
		return StandAloneTagCommand("phoneme", {"alphabet": "ipa", "ph": command.ipa}, command.text)
