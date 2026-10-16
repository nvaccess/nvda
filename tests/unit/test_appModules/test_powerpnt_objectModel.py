# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Christos Bouronikos
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Tests for choosing the PowerPoint object model of a window."""

import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from appModules import powerpnt


def _appModule(slideShowActive: bool) -> tuple[SimpleNamespace, SimpleNamespace, SimpleNamespace]:
	show = SimpleNamespace(active=slideShowActive)
	editor = SimpleNamespace()
	presentation = SimpleNamespace(
		slideShowWindow=show,
		windows=SimpleNamespace(item=lambda index: editor),
	)
	app = SimpleNamespace(_ppApplicationFromROT=SimpleNamespace(activePresentation=presentation))
	return app, show, editor


class TestObjectModelFromROT(unittest.TestCase):
	def test_activeSlideShowIsAlwaysUsed(self) -> None:
		app, show, _editor = _appModule(slideShowActive=True)
		self.assertIs(powerpnt.AppModule._getPpObjectModelFromROT(app), show)

	def test_inactiveSlideShowIsNotUsedByOtherWindows(self) -> None:
		app, _show, editor = _appModule(slideShowActive=False)
		self.assertIs(powerpnt.AppModule._getPpObjectModelFromROT(app), editor)

	def test_inactiveSlideShowIsUsedByASlideShowWindow(self) -> None:
		app, show, _editor = _appModule(slideShowActive=False)
		self.assertIs(powerpnt.AppModule._getPpObjectModelFromROT(app, slideShow=True), show)

	def test_missingSlideShowFallsBackToTheEditor(self) -> None:
		app, _show, editor = _appModule(slideShowActive=False)
		app._ppApplicationFromROT.activePresentation.slideShowWindow = None
		self.assertIs(powerpnt.AppModule._getPpObjectModelFromROT(app, slideShow=True), editor)


class TestFetchObjectModel(unittest.TestCase):
	def _fetch(self, windowClass: str) -> Mock:
		app = Mock()
		app._getPpObjectModelFromROT.return_value = None
		with patch.object(powerpnt.winUser, "getClassName", return_value=windowClass):
			powerpnt.AppModule._fetchPpObjectModelHelper(app, windowHandle=1)
		return app._getPpObjectModelFromROT

	def test_slideShowWindowAllowsAnInactiveSlideShow(self) -> None:
		getModel = self._fetch("screenClass")
		self.assertTrue(all(call.kwargs["slideShow"] for call in getModel.call_args_list))

	def test_otherWindowsRequireAnActiveSlideShow(self) -> None:
		getModel = self._fetch("mdiClass")
		self.assertFalse(any(call.kwargs["slideShow"] for call in getModel.call_args_list))
