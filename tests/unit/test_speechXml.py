#tests/unit/test_speechXml.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017 NV Access Limited

"""Unit tests for the speechXml module.
"""

import unittest
import speechXml
import speech

class TestXmlBalancer(unittest.TestCase):

	def setUp(self):
		self.balancer = speechXml.XmlBalancer()

	def test_text(self):
		xml = self.balancer.generateXml(["<text>"])
		self.assertEqual(xml, "&lt;text&gt;")

	def test_standAloneTag(self):
		xml = self.balancer.generateXml([
			speechXml.StandAloneTagCommand("tag", {"attr": "val"}, "content")
		])
		self.assertEqual(xml, '<tag attr="val">content</tag>')

	def test_standAloneTagNoContent(self):
		xml = self.balancer.generateXml([
			speechXml.StandAloneTagCommand("tag", {"attr": "val"}, None)
		])
		self.assertEqual(xml, '<tag attr="val"/>')

	def test_attrEscaping(self):
		"""Test that attribute values are escaped.
		Depends on behavior tested in test_standAloneTagNoContent.
		"""
		xml = self.balancer.generateXml([
			speechXml.StandAloneTagCommand("tag", {"attr": '"v1"&"v2"'}, None)
		])
		self.assertEqual(xml, '<tag attr="&quot;v1&quot;&amp;&quot;v2&quot;"/>')

	def test_encloseAll(self):
		"""Depends on behavior tested by test_standAloneTag.
		"""
		xml = self.balancer.generateXml([
			speechXml.EncloseAllCommand("encloseAll", {"attr": "val"}),
			speechXml.StandAloneTagCommand("standAlone", {}, "content")
		])
		self.assertEqual(xml, '<encloseAll attr="val"><standAlone>content</standAlone></encloseAll>')

	def test_setAttr(self):
		xml = self.balancer.generateXml([
			speechXml.SetAttrCommand("pitch", "val", 50),
			"text"
		])
		self.assertEqual(xml, '<pitch val="50">text</pitch>')

	def test_delAttrNoSetAttr(self):
		xml = self.balancer.generateXml([
			speechXml.DelAttrCommand("pitch", "val"),
			"text"
		])
		self.assertEqual(xml, 'text')

	def test_setAttrThenDelAttr(self):
		xml = self.balancer.generateXml([
			speechXml.SetAttrCommand("pitch", "val", 50),
			"t1",
			speechXml.DelAttrCommand("pitch", "val"),
			"t2"
		])
		self.assertEqual(xml, '<pitch val="50">t1</pitch>t2')

	def test_setAttrDifferentTags(self):
		"""Tests multiple SetAttrCommands with different tags.
		"""
		xml = self.balancer.generateXml([
			speechXml.SetAttrCommand("pitch", "val", 50),
			speechXml.SetAttrCommand("volume", "val", 60),
			"text"
		])
		self.assertEqual(xml, '<pitch val="50"><volume val="60">text</volume></pitch>')

	def test_setAttrInterspersedText(self):
		"""Tests multiple SetAttrCommands interspersed with text.
		"""
		xml = self.balancer.generateXml([
			speechXml.SetAttrCommand("pitch", "val", 50),
			"t1",
			speechXml.SetAttrCommand("volume", "val", 60),
			"t2"
		])
		self.assertEqual(xml, '<pitch val="50">t1</pitch><pitch val="50"><volume val="60">t2</volume></pitch>')

	def test_setAttrDifferentAttrs(self):
		"""Tests multiple SetAttrCommands with different attributes of the same tag.
		"""
		xml = self.balancer.generateXml([
			speechXml.SetAttrCommand("prosody", "pitch", 50),
			speechXml.SetAttrCommand("prosody", "volume", 60),
			"text"
		])
		self.assertEqual(xml, '<prosody pitch="50" volume="60">text</prosody>')

	def test_delAttrUnbalanced(self):
		"""Tests DelAttrCommand removing an outer tag before an inner tag.
		"""
		xml = self.balancer.generateXml([
			speechXml.SetAttrCommand("pitch", "val", 50),
			speechXml.SetAttrCommand("volume", "val", 60),
			"t1",
			speechXml.DelAttrCommand("pitch", "val"),
			"t2"
		])
		self.assertEqual(xml, '<pitch val="50"><volume val="60">t1</volume></pitch><volume val="60">t2</volume>')

	def test_delSingleAttrOfMultipleAttrs(self):
		"""Tests DelAttrCommand removing a single attribute from a tag which has multiple attributes.
		"""
		xml = self.balancer.generateXml([
			speechXml.SetAttrCommand("prosody", "pitch", 50),
			speechXml.SetAttrCommand("prosody", "volume", 60),
			"t1",
			speechXml.DelAttrCommand("prosody", "pitch"),
			"t2"
		])
		self.assertEqual(xml, '<prosody pitch="50" volume="60">t1</prosody><prosody volume="60">t2</prosody>')

	def test_EncloseText(self):
		"""Depends on behavior tested in test_standAloneTagNoContent.
		"""
		xml = self.balancer.generateXml([
			speechXml.EncloseTextCommand("say-as", {"interpret-as": "characters"}),
			speechXml.StandAloneTagCommand("mark", {"name": "1"}, None),
			"c"
		])
		self.assertEqual(xml, '<mark name="1"/><say-as interpret-as="characters">c</say-as>')

	def test_stopEnclosingText(self):
		"""Depends on behavior tested in test_encloseTag.
		"""
		xml = self.balancer.generateXml([
			speechXml.EncloseTextCommand("say-as", {}),
			"c",
			speechXml.StopEnclosingTextCommand(),
			"t"
		])
		self.assertEqual(xml, '<say-as>c</say-as>t')

class TestSsmlConverter(unittest.TestCase):

	def test_convertComplex(self):
		"""Test converting a complex speech sequence to SSML.
		XML generation is already tested by TestXmlBalancer.
		However, SSML is what callers expect at the end of the day,
		so test converting a complex speech sequence to SSML.
		Depends on behavior tested by TestXmlBalancer.
		"""
		converter = speechXml.SsmlConverter("en_US")
		xml = converter.convertToXml([
			"t1",
			speech.PitchCommand(multiplier=2),
			speech.VolumeCommand(multiplier=2),
			"t2",
			speech.PitchCommand(),
			speech.LangChangeCommand("de_DE"),
			speech.CharacterModeCommand(True),
			speech.IndexCommand(1),
			"c",
			speech.CharacterModeCommand(False),
			speech.PhonemeCommand("phIpa", text="phText")
		])
		self.assertEqual(xml,
			'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">'
			't1'
			'<prosody pitch="200%" volume="200%">t2</prosody>'
			'<prosody volume="200%"><voice xml:lang="de-DE">'
			'<mark name="1"/><say-as interpret-as="characters">c</say-as>'
			'<phoneme alphabet="ipa" ph="phIpa">phText</phoneme>'
			'</voice></prosody></speak>'
		)
