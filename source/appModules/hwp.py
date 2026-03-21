# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Hyun W. Ka (KAIST Assistive AI Lab)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""App module for Hancom Office Hangul (HWP) word processor.

Hancom Hangul (한글) is the most widely used word processor in Korea,
especially in government and education. This module provides basic
accessibility support by leveraging the UIA tree exposed by Hwp.exe.

Key UIA structure:
- Main window: FrameWindowImpl (Window)
- Edit area: HwpMainEditWnd (Edit) with child paragraph nodes
- Status bar: StatusBarImpl (StatusBar) with page/line/column info
- Menus and toolbars: fully labeled in Korean

Note: HWP exposes ValuePattern (not TextPattern) on its edit controls.
Paragraph text content is available through the UIA Name property
on grandchild elements of the HwpMainEditWnd control.
"""

import appModuleHandler
import api
import controlTypes
import UIAHandler
from NVDAObjects.UIA import UIA
from NVDAObjects import NVDAObject


class HwpDocumentEdit(UIA):
	"""Overlay class for the main HWP document editing area (HwpMainEditWnd).

	Adjusts the role to DOCUMENT so NVDA treats it as a document rather than
	a plain edit field, consistent with how other word processors are handled.
	"""

	role = controlTypes.Role.DOCUMENT

	def _get_name(self) -> str:
		# Suppress the empty name on the main edit container;
		# actual content is in child paragraph elements.
		return ""


class HwpParagraph(UIA):
	"""Overlay class for paragraph elements inside the HWP document.

	Each paragraph in HWP is exposed as a UIA Edit control with
	name="paragraph". The actual text of each paragraph line is in
	grandchild Edit elements whose Name property holds the text content.
	"""

	role = controlTypes.Role.PARAGRAPH

	def _get_name(self) -> str:
		# The default name "paragraph" is not useful for the user.
		# Return empty so NVDA reads the actual text content instead.
		return ""


class AppModule(appModuleHandler.AppModule):
	"""NVDA app module for Hancom Hangul (Hwp.exe)."""

	def chooseNVDAObjectOverlayClasses(
		self,
		obj: NVDAObject,
		clsList: list[type],
	) -> None:
		if not isinstance(obj, UIA):
			return
		className = obj.UIAElement.cachedClassName or ""
		if className == "HwpMainEditWnd":
			clsList.insert(0, HwpDocumentEdit)
		elif obj.UIAElement.cachedControlType == UIAHandler.UIA.UIA_EditControlTypeId:
			try:
				name = obj.UIAElement.cachedName or ""
			except Exception:
				name = ""
			if name == "paragraph":
				clsList.insert(0, HwpParagraph)

	def _get_statusBar(self) -> NVDAObject:
		"""Retrieve the HWP status bar via UIA class name lookup.

		The status bar (StatusBarImpl) contains children with position info:
		page, section, line, column, character count, input mode, etc.
		"""
		clientObject = UIAHandler.handler.clientObject
		condition = clientObject.createPropertyCondition(
			UIAHandler.UIA_ClassNamePropertyId,
			"StatusBarImpl",
		)
		foreground = api.getForegroundObject()
		if not foreground or not foreground.windowHandle:
			raise NotImplementedError
		rootElement = clientObject.elementFromHandle(foreground.windowHandle)
		statusBarElement = rootElement.findFirst(
			UIAHandler.TreeScope_Descendants,
			condition,
		)
		if not statusBarElement:
			raise NotImplementedError
		statusBarElement = statusBarElement.buildUpdatedCache(
			UIAHandler.handler.baseCacheRequest,
		)
		return UIA(UIAElement=statusBarElement)

	def event_NVDAObject_init(self, obj: NVDAObject) -> None:
		if not isinstance(obj, UIA):
			return
		className = obj.UIAElement.cachedClassName or ""
		# The title bar class exposes a truncated window title;
		# use the full title from the top-level window instead.
		if className == "TitleBarImpl":
			try:
				obj.name = api.getForegroundObject().name
			except Exception:
				pass
