# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Christos Bouronikos
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Tests for detecting and reporting slide changes in a PowerPoint slide show."""

import unittest
from types import SimpleNamespace
from typing import Any
from unittest.mock import Mock, PropertyMock, patch

from appModules import powerpnt


def _object[T](cls: type[T], **attrs: Any) -> T:
	obj = object.__new__(cls)
	obj._propertyCache = {}
	obj.__dict__.update(attrs)
	return obj


class TestSlideShowFocus(unittest.TestCase):
	def setUp(self) -> None:
		self.window = Mock()
		self.interceptor = _object(powerpnt.SlideShowTreeInterceptor, rootNVDAObject=self.window)

	def test_regainingFocusRefreshesTheSlideBeforeReportingIt(self) -> None:
		self.interceptor.hadFocusOnce = True
		self.window.handleSlideChange.return_value = True
		with patch.object(powerpnt.SlideShowTreeInterceptor, "reportNewSlide") as reportNewSlide:
			self.interceptor.event_treeInterceptor_gainFocus()
		self.window.handleSlideChange.assert_called_once_with(report=False)
		reportNewSlide.assert_called_once_with(False, resetSelection=True)

	def test_regainingFocusOnTheSameSlideKeepsTheReadingPosition(self) -> None:
		self.interceptor.hadFocusOnce = True
		self.window.handleSlideChange.return_value = False
		with patch.object(powerpnt.SlideShowTreeInterceptor, "reportNewSlide") as reportNewSlide:
			self.interceptor.event_treeInterceptor_gainFocus()
		reportNewSlide.assert_called_once_with(True, resetSelection=False)

	def test_firstFocusReportsTheSlideFromItsStart(self) -> None:
		self.interceptor.hadFocusOnce = False
		self.window.handleSlideChange.return_value = False
		with patch.object(powerpnt.SlideShowTreeInterceptor, "reportNewSlide") as reportNewSlide:
			self.interceptor.event_treeInterceptor_gainFocus()
		reportNewSlide.assert_called_once_with(False, resetSelection=True)
		self.assertTrue(self.interceptor.hadFocusOnce)

	def _reportNewSlide(self, sayAll: bool, **kwargs: Any) -> Mock:
		info = Mock(isCollapsed=True)
		self.interceptor.makeTextInfo = Mock(return_value=info)
		with (
			patch.object(powerpnt.config, "conf", {"virtualBuffers": {"autoSayAllOnPageLoad": sayAll}}),
			patch.object(
				powerpnt.SlideShowTreeInterceptor, "selection", new_callable=PropertyMock
			) as selection,
			patch.object(powerpnt.braille, "handler") as brailleHandler,
			patch.object(powerpnt.sayAll, "SayAllHandler"),
			patch.object(powerpnt.speech, "speakTextInfo"),
		):
			selection.return_value = info
			self.interceptor.reportNewSlide(**kwargs)
		brailleHandler.handleGainFocus.assert_called_once_with(self.interceptor)
		return info

	def test_newSlideResetsTheCaretAndUpdatesBrailleWithoutSayAll(self) -> None:
		info = self._reportNewSlide(sayAll=False)
		info.updateCaret.assert_called_once_with()

	def test_newSlideResetsTheCaretAndUpdatesBrailleWithSayAll(self) -> None:
		info = self._reportNewSlide(sayAll=True)
		info.updateCaret.assert_called_once_with()

	def test_sameSlideUpdatesBrailleButKeepsTheCaret(self) -> None:
		info = self._reportNewSlide(sayAll=False, suppressSayAll=True, resetSelection=False)
		info.updateCaret.assert_not_called()


class TestSlideChange(unittest.TestCase):
	def setUp(self) -> None:
		self.slide = SimpleNamespace(name="Slide 1")
		self.window = _object(powerpnt.SlideShowWindow, windowHandle=1, notesMode=False)
		patcher = patch.object(powerpnt.SlideShowWindow, "currentSlide", new_callable=PropertyMock)
		self.currentSlide = patcher.start()
		self.currentSlide.return_value = self.slide
		self.addCleanup(patcher.stop)
		patcher = patch.object(powerpnt.SlideShowWindow, "treeInterceptor", new_callable=PropertyMock)
		self.interceptor = patcher.start()
		self.interceptor.return_value = Mock()
		self.addCleanup(patcher.stop)
		patcher = patch.object(powerpnt.SlideShowWindow, "reportFocus")
		self.reportFocus = patcher.start()
		self.addCleanup(patcher.stop)

	def test_newSlideIsReportedOnce(self) -> None:
		self.assertTrue(self.window.handleSlideChange())
		self.assertFalse(self.window.handleSlideChange())
		self.reportFocus.assert_called_once()
		self.interceptor.return_value.reportNewSlide.assert_called_once()

	def test_anotherSlideIsReported(self) -> None:
		self.window.handleSlideChange()
		self.slide.name = "Slide 2"
		self.assertTrue(self.window.handleSlideChange())
		self.assertEqual(self.reportFocus.call_count, 2)

	def test_changeCanBeDetectedWithoutReportingIt(self) -> None:
		self.assertTrue(self.window.handleSlideChange(report=False))
		self.assertFalse(self.window.handleSlideChange(report=False))
		self.reportFocus.assert_not_called()
		self.interceptor.return_value.reportNewSlide.assert_not_called()

	def test_cachedWindowNameIsDiscarded(self) -> None:
		with patch.object(powerpnt.SlideShowWindow, "invalidateCache") as invalidateCache:
			self.window.handleSlideChange()
		invalidateCache.assert_called_once_with()
