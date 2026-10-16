# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Christos Bouronikos
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Tests for reading audio and video clips in a PowerPoint slide show."""

import unittest
from types import SimpleNamespace
from typing import Any

import controlTypes
from appModules import powerpnt


def _object[T](cls: type[T], **attrs: Any) -> T:
	obj = object.__new__(cls)
	obj._propertyCache = {}
	obj.__dict__.update(attrs)
	return obj


def _media(mediaType: int, alternativeText: str = "") -> SimpleNamespace:
	return SimpleNamespace(
		type=powerpnt.msoMedia,
		mediaType=mediaType,
		hasTextFrame=False,
		hasTable=False,
		alternativeText=alternativeText,
		title="",
		name="Media 3",
	)


class TestMediaText(unittest.TestCase):
	def setUp(self) -> None:
		self.window = _object(powerpnt.SlideShowWindow)

	def test_clipWithoutAlternativeTextIsStillAnnounced(self) -> None:
		for mediaType, role in [
			(powerpnt.ppVideo, controlTypes.Role.VIDEO),
			(powerpnt.ppAudio, controlTypes.Role.AUDIO),
		]:
			with self.subTest(mediaType=mediaType):
				self.assertEqual(list(self.window._getShapeText(_media(mediaType))), [role.displayString])

	def test_alternativeTextFollowsTheType(self) -> None:
		self.assertEqual(
			list(self.window._getShapeText(_media(powerpnt.ppVideo, "Welcome message"))),
			[f"{controlTypes.Role.VIDEO.displayString} Welcome message"],
		)

	def test_unknownMediaTypeKeepsTheGenericLabel(self) -> None:
		self.assertEqual(list(self.window._getShapeText(_media(-2))), [])
		self.assertEqual(list(self.window._getShapeText(_media(-2, "Clip"))), ["Media Clip"])
