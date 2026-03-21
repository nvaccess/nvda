# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Hyun W. Ka (KAIST Rehabilitation AI Lab)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""App module for Hancom Office Hangul (HWP) word processor.

Hancom Hangul (한글) is the most widely used word processor in Korea,
especially in government and education. This module provides accessibility
support using two complementary strategies:

1. UIA overlay classes for document role mapping, paragraph handling,
   status bar access, and menu/toolbar interaction.
2. HWP COM Automation API bridge for reading full document text including
   table cell contents, which the UIA tree does not expose.

Key UIA structure:
- Main window: FrameWindowImpl (Window)
- Edit area: HwpMainEditWnd (Edit) with child paragraph nodes
- Status bar: StatusBarImpl (StatusBar) with page/line/column info
- Menus and toolbars: fully labeled in Korean

HWP COM API (HWPFrame.HwpObject):
- Connect via Running Object Table moniker "!HwpObject"
- InitScan(4, 0x0077, 0, 0, 0, 0) + GetText() reads all text including tables
- KeyIndicator() returns current position including table cell address
- HeadCtrl iteration enumerates document controls (tables, sections, etc.)
"""

from __future__ import annotations

import logging
from typing import Optional

import appModuleHandler
import api
import controlTypes
import scriptHandler
import ui
import UIAHandler
from NVDAObjects.UIA import UIA
from NVDAObjects import NVDAObject

log = logging.getLogger(__name__)


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


class HwpComBridge:
	"""Bridge to the HWP COM Automation API (HWPFrame.HwpObject).

	Connects to a running HWP instance via the Running Object Table
	and provides methods to read document content that the UIA tree
	does not expose (e.g. table cell text, full document text).
	"""

	def __init__(self) -> None:
		self._hwp: Optional[object] = None

	def _connect(self) -> Optional[object]:
		if self._hwp is not None:
			return self._hwp
		try:
			import pythoncom
			import win32com.client

			context = pythoncom.CreateBindCtx(0)
			rot = pythoncom.GetRunningObjectTable()
			for moniker in rot.EnumRunning():
				try:
					name = moniker.GetDisplayName(context, None)
					if "HwpObject" in name:
						obj = rot.GetObject(moniker)
						self._hwp = win32com.client.Dispatch(
							obj.QueryInterface(pythoncom.IID_IDispatch),
						)
						return self._hwp
				except Exception:
					continue
		except ImportError:
			log.debugWarning("pywin32 not available for HWP COM bridge")
		except Exception:
			log.debugWarning("Failed to connect to HWP COM object", exc_info=True)
		return None

	def disconnect(self) -> None:
		self._hwp = None

	def getFullText(self, includeTableContents: bool = True) -> str:
		"""Read all text from the document via InitScan/GetText.

		:param includeTableContents: If True, use option=4 to include
			text inside table cells and sub-documents.
		:return: The concatenated document text.
		"""
		hwp = self._connect()
		if not hwp:
			return ""
		option = 4 if includeTableContents else 0
		try:
			hwp.InitScan(option, 0x0077, 0, 0, 0, 0)
			parts: list[str] = []
			for _ in range(10000):
				result = hwp.GetText()
				state = result[0]
				text = result[1] if len(result) > 1 else ""
				if state in (0, 1):
					break
				if text:
					parts.append(text)
			hwp.ReleaseScan()
			return "".join(parts)
		except Exception:
			log.debugWarning("HWP GetText failed", exc_info=True)
			try:
				hwp.ReleaseScan()
			except Exception:
				pass
			return ""

	def getPositionInfo(self) -> Optional[tuple]:
		"""Return KeyIndicator tuple: (visible, page, secPage, section,
		para, line, column, insert, cellAddr).
		"""
		hwp = self._connect()
		if not hwp:
			return None
		try:
			return hwp.KeyIndicator()
		except Exception:
			return None

	def isInTable(self) -> bool:
		hwp = self._connect()
		if not hwp:
			return False
		try:
			return bool(hwp.CellShape)
		except Exception:
			return False

	def getTableCount(self) -> int:
		hwp = self._connect()
		if not hwp:
			return 0
		try:
			ctrl = hwp.HeadCtrl
			count = 0
			while ctrl:
				if ctrl.CtrlID == "tbl":
					count += 1
				ctrl = ctrl.Next
			return count
		except Exception:
			return 0


class AppModule(appModuleHandler.AppModule):
	"""NVDA app module for Hancom Hangul (Hwp.exe)."""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._comBridge = HwpComBridge()

	def terminate(self):
		self._comBridge.disconnect()

	@scriptHandler.script(
		description="한글 문서의 전체 텍스트를 표 내용 포함하여 읽습니다",
		gesture="kb:NVDA+shift+t",
	)
	def script_readFullDocumentText(self, gesture) -> None:
		text = self._comBridge.getFullText(includeTableContents=True)
		if text.strip():
			lineCount = text.count("\n") + 1
			ui.message(f"문서 텍스트 {lineCount}줄. {text[:500]}")
		else:
			ui.message("문서 텍스트를 읽을 수 없습니다")

	@scriptHandler.script(
		description="현재 위치 정보를 읽습니다 (표 셀 주소 포함)",
		gesture="kb:NVDA+shift+p",
	)
	def script_readPositionInfo(self, gesture) -> None:
		info = self._comBridge.getPositionInfo()
		if info:
			page = info[1]
			line = info[5]
			col = info[6]
			cellAddr = info[8] if len(info) > 8 else ""
			msg = f"{page}쪽 {line}줄 {col}칸"
			if cellAddr and ":" in str(cellAddr):
				msg += f" {cellAddr}"
			ui.message(msg)
		else:
			ui.message("위치 정보를 읽을 수 없습니다")

	@scriptHandler.script(
		description="현재 커서가 표 안에 있는지 확인합니다",
		gesture="kb:NVDA+shift+h",
	)
	def script_reportTableInfo(self, gesture) -> None:
		if self._comBridge.isInTable():
			info = self._comBridge.getPositionInfo()
			cellAddr = info[8] if info and len(info) > 8 else ""
			tableCount = self._comBridge.getTableCount()
			msg = f"표 안에 있습니다. 문서 내 표 {tableCount}개."
			if cellAddr:
				msg += f" 현재 셀: {cellAddr}"
			ui.message(msg)
		else:
			ui.message("표 안에 있지 않습니다")

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
