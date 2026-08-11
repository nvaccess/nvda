# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 NV Access Limited

"""Unit tests for parsing of virtual buffer XML markup by the XMLFormatting module.

The virtual buffer C++ code sanitizes attribute names when they are added to the buffer
(sanitizeXMLAttribName in nvdaHelper/common/xml.h), because browsers can expose names that
are invalid in XML, e.g. quotes from malformed HTML such as aria-label"foo" (#7173) or
spaces from localised Chrome action names (#6249).
These tests pin the contract that every attribute name that sanitizer can produce is
accepted by the expat parser NVDA parses the markup with.
Note that expat enforces the XML 1.0 fourth edition name rules, which reject many
characters that the fifth edition allows; the sanitizer's allowlist must remain a subset
of what expat accepts.
"""

import string
import unittest
from xml.parsers import expat

import XMLFormatting


#: Characters sanitizeXMLAttribName may leave in an attribute name.
#: Mirrors isValidXMLNameChar in nvdaHelper/common/xml.h.
SANITIZED_NAME_CHARS = string.ascii_letters + string.digits + "-.:_"
#: Characters sanitizeXMLAttribName allows an attribute name to start with.
#: Mirrors the leading character guard in sanitizeXMLAttribName.
SANITIZED_NAME_START_CHARS = string.ascii_letters + "_:"


def _sanitizeXMLAttribName(name: str) -> str:
	"""Python mirror of sanitizeXMLAttribName in nvdaHelper/common/xml.h.
	Used to compute the attribute names the virtual buffer would emit for malformed input.
	"""
	sanitized = "".join(c if c in SANITIZED_NAME_CHARS else "_" for c in name)
	if not sanitized or sanitized[0] not in SANITIZED_NAME_START_CHARS:
		sanitized = "_" + sanitized
	return sanitized


def _parseAttribName(name: str) -> None:
	"""Parse a minimal document using the given attribute name, raising ExpatError on failure."""
	expat.ParserCreate("utf-8").Parse(f'<control {name}=""></control>', True)


class TestSanitizedAttribNamesAcceptedByExpat(unittest.TestCase):
	"""Every name the C++ sanitizer can produce must be accepted by expat."""

	def test_allSanitizedNameCharsInInteriorPosition(self):
		for char in SANITIZED_NAME_CHARS:
			with self.subTest(char=char):
				_parseAttribName(f"a{char}b")

	def test_allSanitizedNameStartChars(self):
		for char in SANITIZED_NAME_START_CHARS:
			with self.subTest(char=char):
				_parseAttribName(f"{char}ab")

	def test_restrictedLeadingCharsRejectedByExpat(self):
		"""Digits, hyphens and periods are valid in names but not as the first character.
		This is why the sanitizer prepends an underscore in those cases.
		"""
		for char in string.digits + "-.":
			with self.subTest(char=char):
				with self.assertRaises(expat.ExpatError):
					_parseAttribName(f"{char}ab")
				# The sanitizer's underscore prefix makes the name acceptable.
				_parseAttribName(f"_{char}ab")

	def test_underscoreAloneIsAValidName(self):
		"""An empty raw name sanitizes to a single underscore."""
		self.assertEqual(_sanitizeXMLAttribName(""), "_")
		_parseAttribName("_")


class TestMalformedAttribNameSanitization(unittest.TestCase):
	"""Known problematic raw names sanitize to names expat accepts."""

	def test_quotesFromMalformedAriaLabel(self):
		"""The name Firefox exposes for aria-label"almenük" with a missing equals sign. (#7173)"""
		sanitized = _sanitizeXMLAttribName('IAccessible2::attribute_label"almen\xfck"')
		self.assertEqual(sanitized, "IAccessible2::attribute_label_almen_k_")
		_parseAttribName(sanitized)

	def test_spacesFromLocalisedChromeActionName(self):
		"""Localised Chrome action names can contain spaces. (#6249)"""
		sanitized = _sanitizeXMLAttribName("IAccessibleAction_fai clic")
		self.assertEqual(sanitized, "IAccessibleAction_fai_clic")
		_parseAttribName(sanitized)

	def test_fourthEditionOnlyCharsReplaced(self):
		"""U+0132 is a valid XML 1.0 fifth edition name character,
		but expat rejects it, so the sanitizer must replace it.
		"""
		with self.assertRaises(expat.ExpatError):
			_parseAttribName("aĲb")
		sanitized = _sanitizeXMLAttribName("aĲb")
		self.assertEqual(sanitized, "a_b")
		_parseAttribName(sanitized)

	def test_validNamesUnchanged(self):
		for name in (
			"IAccessible2::attribute_xml-roles",
			"IAccessibleAction_click",
			"_startOfNode",
			"language",
		):
			with self.subTest(name=name):
				self.assertEqual(_sanitizeXMLAttribName(name), name)
				_parseAttribName(name)


class TestXMLTextParser(unittest.TestCase):
	"""End to end: markup containing sanitized names parses into the expected commands."""

	def test_controlWithSanitizedAttribName(self):
		markup = (
			'<control controlIdentifier_docHandle="1" controlIdentifier_ID="2"'
			' IAccessible2::attribute_label_almen_k_="" IAccessible2::attribute_tag="section"'
			"><text >test</text></control>"
		)
		commands = XMLFormatting.XMLTextParser().parse(markup)
		controlStarts = [
			command for command in commands if getattr(command, "command", None) == "controlStart"
		]
		self.assertEqual(len(controlStarts), 1)
		self.assertEqual(controlStarts[0].field.get("IAccessible2::attribute_tag"), "section")
		self.assertIn("IAccessible2::attribute_label_almen_k_", controlStarts[0].field)
		self.assertIn("test", commands)
