# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Hyun W. Ka (KAIST Assistive AI Lab)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""App module for Hancom Office Hangul (HWP) word processor.

Hancom Hangul (한글) is the most widely used word processor in Korea,
especially in government and education. This module provides accessibility
support using two complementary strategies:

1. UIA overlay classes for document role mapping, paragraph handling,
   status bar access, and menu/toolbar interaction.
2. HWP COM Automation API bridge with a custom OffsetsTextInfo, enabling
   full NVDA text navigation (character, word, line, paragraph) including
   table cell contents that the UIA tree does not expose.

HWP COM API (HWPFrame.HwpObject):
- Connect via Running Object Table moniker "!HwpObject"
- InitScan(4, 0x0077, 0, 0, 0, 0) + GetText() reads all text including tables
- InitScan(4, 0x0022, 0, 0, 0, 0) reads current line at caret
- KeyIndicator() returns position including table cell address
- GetPos()/SetPos() for caret offset tracking
- HAction.Run("MoveRight"/"MoveLeft"/etc.) for cursor movement
"""

from __future__ import annotations

import logging
import time
from typing import Optional

import appModuleHandler
import api
import controlTypes
import editableText
import scriptHandler
import textInfos
import textInfos.offsets
import ui
import UIAHandler
from NVDAObjects.UIA import UIA
from NVDAObjects import NVDAObject

log = logging.getLogger(__name__)


class HwpComBridge:
	"""Bridge to the HWP COM Automation API (HWPFrame.HwpObject).

	Connects to a running HWP instance via the Running Object Table
	and provides methods to read document content that the UIA tree
	does not expose (e.g. table cell text, full document text).
	"""

	def __init__(self) -> None:
		self._hwp: Optional[object] = None
		self._textCache: Optional[str] = None
		self._textCacheTime: float = 0
		self._TEXT_CACHE_TTL = 2.0

	def _connect(self) -> Optional[object]:
		if self._hwp is not None:
			return self._hwp
		try:
			import pythoncom
			import win32com.client

			# Strategy 1: GetActiveObject (works across security contexts)
			for progId in ("HWPFrame.HwpObject", "Hwp.HwpObject"):
				try:
					self._hwp = win32com.client.GetActiveObject(progId)
					return self._hwp
				except Exception:
					continue

			# Strategy 2: Running Object Table enumeration
			try:
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
			except Exception:
				pass

			# Strategy 3: Direct Dispatch (creates new if needed)
			try:
				self._hwp = win32com.client.Dispatch("HWPFrame.HwpObject")
				return self._hwp
			except Exception:
				pass

		except ImportError:
			log.debugWarning("pywin32 not available for HWP COM bridge")
		except Exception:
			log.debugWarning("Failed to connect to HWP COM object", exc_info=True)
		return None

	def disconnect(self) -> None:
		self._hwp = None
		self.invalidateCache()

	def invalidateCache(self) -> None:
		self._textCache = None
		self._textCacheTime = 0

	def getFullText(self) -> str:
		"""Read all text from the document including table cells.

		Results are cached for a short period to avoid repeated COM calls
		during rapid NVDA text info queries.
		"""
		now = time.time()
		if self._textCache is not None and (now - self._textCacheTime) < self._TEXT_CACHE_TTL:
			return self._textCache
		hwp = self._connect()
		if not hwp:
			return ""
		try:
			hwp.InitScan(4, 0x0077, 0, 0, 0, 0)
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
			self._textCache = "".join(parts)
			self._textCacheTime = now
			return self._textCache
		except Exception:
			log.debugWarning("HWP GetText failed", exc_info=True)
			try:
				hwp.ReleaseScan()
			except Exception:
				pass
			return ""

	def getCurrentLineText(self) -> str:
		"""Read the current line at the caret position."""
		hwp = self._connect()
		if not hwp:
			return ""
		try:
			hwp.InitScan(4, 0x0022, 0, 0, 0, 0)
			parts: list[str] = []
			for _ in range(50):
				result = hwp.GetText()
				if result[0] in (0, 1):
					break
				text = result[1] if len(result) > 1 else ""
				if text:
					parts.append(text)
			hwp.ReleaseScan()
			return "".join(parts).rstrip("\r\n")
		except Exception:
			try:
				hwp.ReleaseScan()
			except Exception:
				pass
			return ""

	def getPositionInfo(self) -> Optional[tuple]:
		"""Return KeyIndicator: (visible, page, secPage, section,
		para, line, column, insert, cellAddr).
		"""
		hwp = self._connect()
		if not hwp:
			return None
		try:
			return hwp.KeyIndicator()
		except Exception:
			return None

	def getCaretLine(self) -> int:
		"""Return 1-based line number of the caret."""
		info = self.getPositionInfo()
		return info[5] if info else 1

	def getCaretColumn(self) -> int:
		"""Return 1-based column number of the caret."""
		info = self.getPositionInfo()
		return info[6] if info else 1

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


_comBridge = HwpComBridge()


class HwpTextInfo(textInfos.offsets.OffsetsTextInfo):
	"""TextInfo for HWP documents backed by the COM Automation API.

	Uses the full document text (from InitScan) as the story text,
	and the current line text (from InitScan range=0x0022) for
	efficient line-level operations. Integrates with NVDA's standard
	text navigation for character, word, line, and paragraph units.
	"""

	def _getStoryText(self) -> str:
		return _comBridge.getFullText()

	def _getStoryLength(self) -> int:
		return len(self._getStoryText())

	def _getCaretOffset(self) -> int:
		"""Map the HWP caret position to a character offset in the story text.

		Uses the current line text to find its position in the full text,
		then adds the column offset within that line.
		"""
		lineText = _comBridge.getCurrentLineText()
		fullText = self._getStoryText()
		if not lineText or not fullText:
			return 0
		lineOffset = fullText.find(lineText)
		if lineOffset < 0:
			return 0
		col = _comBridge.getCaretColumn()
		charOffset = 0
		colCount = 1
		for i, ch in enumerate(lineText):
			if colCount >= col:
				charOffset = i
				break
			colCount += 2 if ord(ch) > 0x7F else 1
		else:
			charOffset = len(lineText)
		return lineOffset + charOffset

	def _setCaretOffset(self, offset: int) -> None:
		pass

	def _getSelectionOffsets(self) -> tuple[int, int]:
		caretOffset = self._getCaretOffset()
		return (caretOffset, caretOffset)

	def _setSelectionOffsets(self, start: int, end: int) -> None:
		pass

	def _getLineOffsets(self, offset: int) -> tuple[int, int]:
		"""Get the start and end offsets of the line containing offset."""
		text = self._getStoryText()
		if not text:
			return (offset, offset + 1)
		lineStart = text.rfind("\n", 0, offset)
		lineStart = lineStart + 1 if lineStart >= 0 else 0
		lineEnd = text.find("\n", offset)
		if lineEnd < 0:
			lineEnd = len(text)
		else:
			lineEnd += 1
		return (lineStart, lineEnd)


class HwpDocumentEdit(editableText.EditableText, UIA):
	"""Overlay class for the main HWP document editing area (HwpMainEditWnd).

	Provides full NVDA text navigation by combining EditableText mixin
	with the HwpTextInfo backed by the COM Automation API bridge.
	"""

	TextInfo = HwpTextInfo
	role = controlTypes.Role.EDITABLETEXT

	def _get_name(self) -> str:
		return ""

	def makeTextInfo(self, position) -> HwpTextInfo:
		return self.TextInfo(self, position)

	def _collectVisibleText(self, rootObj: NVDAObject, maxNodes: int = 80) -> str:
		"""Best-effort UIA fallback when COM is unavailable.

		HWP often exposes current visible text on descendant edit nodes.
		"""
		parts: list[str] = []

		def scoreText(text: str) -> int:
			t = (text or "").strip()
			if not t:
				return -1
			low = t.lower()
			if low == "paragraph":
				return -1
			# Exclude common window title / file-name announcements.
			if low.endswith(" - 한글") or low.endswith(" - hwp"):
				return -1
			if low.endswith(".hwp") or low.endswith(".hwpx"):
				return -1
			score = len(t)
			if "\n" in t:
				score += 40
			if " " in t:
				score += 10
			# Single-token short strings are often labels, not content.
			if (" " not in t) and ("\n" not in t) and len(t) < 20:
				score -= 20
			return score

		visited: set[int] = set()
		stack: list[NVDAObject] = [rootObj]
		while stack and len(visited) < maxNodes:
			obj = stack.pop()
			if not obj:
				continue
			objId = id(obj)
			if objId in visited:
				continue
			visited.add(objId)
			candidates: list[str] = []
			try:
				candidates.append((obj.name or "").strip())
			except Exception:
				pass
			try:
				candidates.append((obj.value or "").strip())
			except Exception:
				pass
			for text in candidates:
				if text and text.lower() != "paragraph" and text not in parts:
					parts.append(text)
			try:
				child = obj.firstChild
			except Exception:
				child = None
			while child:
				stack.append(child)
				try:
					child = child.next
				except Exception:
					child = None
		bestText = ""
		bestScore = -1
		for text in parts:
			s = scoreText(text)
			if s > bestScore:
				bestText = text
				bestScore = s
		return bestText.strip()

	def _reportByUiaFallback(self) -> bool:
		"""Report text from focus tree when COM bridge is unavailable."""
		try:
			focus = api.getFocusObject()
		except Exception:
			focus = None
		try:
			foreground = api.getForegroundObject()
		except Exception:
			foreground = None
		candidates = [self, focus, getattr(focus, "parent", None), foreground]
		for root in candidates:
			text = self._collectVisibleText(root)
			if text:
				ui.message(text[:300])
				return True
		return False

	def _reportCaretByUnit(self, unit: str) -> None:
		"""Fallback speech path for caret navigation keys."""
		_comBridge.invalidateCache()
		try:
			if not _comBridge._connect():
				if self._reportByUiaFallback():
					return
			info = self.makeTextInfo(textInfos.POSITION_CARET)
			info.expand(unit)
			text = info.text.strip("\r\n")
			if text:
				ui.message(text)
			elif unit == textInfos.UNIT_LINE:
				ui.message("빈 줄")
		except Exception:
			self._reportByUiaFallback()

	@scriptHandler.script(gesture="kb:upArrow")
	def script_caretMoveUp(self, gesture) -> None:
		gesture.send()
		self._reportCaretByUnit(textInfos.UNIT_LINE)

	@scriptHandler.script(gesture="kb:downArrow")
	def script_caretMoveDown(self, gesture) -> None:
		gesture.send()
		self._reportCaretByUnit(textInfos.UNIT_LINE)

	@scriptHandler.script(gesture="kb:leftArrow")
	def script_caretMoveLeft(self, gesture) -> None:
		gesture.send()
		self._reportCaretByUnit(textInfos.UNIT_CHARACTER)

	@scriptHandler.script(gesture="kb:rightArrow")
	def script_caretMoveRight(self, gesture) -> None:
		gesture.send()
		self._reportCaretByUnit(textInfos.UNIT_CHARACTER)


class HwpParagraph(UIA):
	"""Overlay class for paragraph elements inside the HWP document."""

	role = controlTypes.Role.PARAGRAPH

	def _get_name(self) -> str:
		return ""


class AppModule(appModuleHandler.AppModule):
	"""NVDA app module for Hancom Hangul (Hwp.exe)."""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def terminate(self):
		_comBridge.disconnect()

	def _reportFocusFallback(self) -> bool:
		"""Fallback for script calls when COM is unavailable."""

		def collectVisibleText(rootObj: NVDAObject, maxNodes: int = 100) -> str:
			parts: list[str] = []

			def scoreText(text: str) -> int:
				t = (text or "").strip()
				if not t:
					return -1
				low = t.lower()
				if low == "paragraph":
					return -1
				if low.endswith(" - 한글") or low.endswith(" - hwp"):
					return -1
				if low.endswith(".hwp") or low.endswith(".hwpx"):
					return -1
				score = len(t)
				if "\n" in t:
					score += 40
				if " " in t:
					score += 10
				if (" " not in t) and ("\n" not in t) and len(t) < 20:
					score -= 20
				return score

			visited: set[int] = set()
			stack: list[NVDAObject] = [rootObj]
			while stack and len(visited) < maxNodes:
				obj = stack.pop()
				if not obj:
					continue
				objId = id(obj)
				if objId in visited:
					continue
				visited.add(objId)
				candidates: list[str] = []
				try:
					candidates.append((obj.name or "").strip())
				except Exception:
					pass
				try:
					candidates.append((obj.value or "").strip())
				except Exception:
					pass
				for text in candidates:
					if text and text.lower() != "paragraph" and text not in parts:
						parts.append(text)
				try:
					child = obj.firstChild
				except Exception:
					child = None
				while child:
					stack.append(child)
					try:
						child = child.next
					except Exception:
						child = None
			bestText = ""
			bestScore = -1
			for text in parts:
				s = scoreText(text)
				if s > bestScore:
					bestText = text
					bestScore = s
			return bestText.strip()

		try:
			focus = api.getFocusObject()
			foreground = api.getForegroundObject()
			candidates = [focus, getattr(focus, "parent", None), foreground]
			for root in candidates:
				text = collectVisibleText(root)
				if text:
					ui.message(text[:300])
					return True
		except Exception:
			pass
		return False

	@scriptHandler.script(
		description="한글 문서의 전체 텍스트를 표 내용 포함하여 읽습니다",
		gesture="kb:NVDA+shift+t",
	)
	def script_readFullDocumentText(self, gesture) -> None:
		try:
			hwp = _comBridge._connect()
			if not hwp:
				if not self._reportFocusFallback():
					ui.message("텍스트를 찾을 수 없습니다")
				return
			text = _comBridge.getFullText()
			if text.strip():
				lineCount = text.count("\n") + 1
				ui.message(f"문서 텍스트 {lineCount}줄. {text[:500]}")
			else:
				ui.message("COM 연결됨, 하지만 텍스트가 비어 있습니다")
		except Exception as e:
			ui.message(f"오류 발생: {e}")

	@scriptHandler.script(
		description="현재 위치 정보를 읽습니다 (표 셀 주소 포함)",
		gesture="kb:NVDA+shift+p",
	)
	def script_readPositionInfo(self, gesture) -> None:
		info = _comBridge.getPositionInfo()
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
		if _comBridge.isInTable():
			info = _comBridge.getPositionInfo()
			cellAddr = info[8] if info and len(info) > 8 else ""
			tableCount = _comBridge.getTableCount()
			msg = f"표 안에 있습니다. 문서 내 표 {tableCount}개."
			if cellAddr:
				msg += f" 현재 셀: {cellAddr}"
			ui.message(msg)
		else:
			ui.message("표 안에 있지 않습니다")

	def event_caret(self, obj: NVDAObject, nextHandler) -> None:
		"""Invalidate text cache on caret movement for fresh reads."""
		_comBridge.invalidateCache()
		nextHandler()

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
			return
		elif (
			obj.windowClassName == "HwpMainEditWnd"
			and obj.UIAElement.cachedControlType == UIAHandler.UIA.UIA_EditControlTypeId
		):
			# Descendant edit nodes inside the main editor should share
			# the same TextInfo path for reliable keyboard reading.
			clsList.insert(0, HwpDocumentEdit)
			return
		elif obj.UIAElement.cachedControlType == UIAHandler.UIA.UIA_EditControlTypeId:
			try:
				name = obj.UIAElement.cachedName or ""
			except Exception:
				name = ""
			if name == "paragraph":
				# Many caret interactions land on the paragraph edit node.
				clsList.insert(0, HwpDocumentEdit)

	def _get_statusBar(self) -> NVDAObject:
		"""Retrieve the HWP status bar via UIA class name lookup."""
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
		if className == "TitleBarImpl":
			try:
				obj.name = api.getForegroundObject().name
			except Exception:
				pass
