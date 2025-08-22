# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020-2025 NV Access Limited, Leonard de Ruijter, Cary-Rowen, Bill Dengler
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""App module for Visual Studio Code."""

import api
import appModuleHandler
import controlTypes
import re
from collections import deque
from logHandler import log
from NVDAObjects.behaviors import EditableTextBase
from NVDAObjects.IAccessible.chromium import Document
from NVDAObjects import NVDAObject, NVDAObjectTextInfo


class VSCodeDocument(Document):
	"""The only content in the root document node of Visual Studio code is the application object.
	Creating a tree interceptor on this object causes a major slow down of Code.
	Therefore, forcefully block tree interceptor creation.
	"""

	_get_treeInterceptorClass = NVDAObject._get_treeInterceptorClass


DIGIT_EXPR = re.compile(r"\d+")


class AppModule(appModuleHandler.AppModule):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._status = None

	@staticmethod
	def _search_for_statusbar(root: NVDAObject) -> NVDAObject | None:
		seen = set()
		t = deque((root,))
		while t:
			obj = t.popleft()
			if obj in seen:
				continue
			seen.add(obj)
			if obj.role == controlTypes.Role.STATUSBAR:
				return obj
			try:
				# IA2 ID often contains "statusbar"
				ia2id = obj.IA2Attributes.get("id")
			except AttributeError:
				ia2id = None
			if ia2id and "statusbar" in ia2id.casefold():
				return obj
			try:
				children = obj.children
			except Exception:
				log.exception(f"Unable to get descendents of {obj}")
				children = ()
			t.extend(children)
		return None

	@staticmethod
	def _looks_like_line_col(text: str) -> bool:
		"""
		Detect two integers separated by something that is NOT a dot,
		to avoid version-like strings.
		"""
		it = DIGIT_EXPR.finditer(text)
		first = next(it, None)
		if first is None:
			return False
		second = next(it, None)
		if second is None:
			return False
		between = text[first.end() : second.start()]
		if "." in between:
			return False
		if not between.strip():
			# Only whitespace or an empty string found,
			# not the line/column number
			return False
		return True

	def _get_statusBar(self) -> NVDAObject:
		cached = self._status
		if cached:
			return cached

		# Fallback: search the current foreground window tree for a STATUSBAR.
		foreground = api.getForegroundObject()
		res = self._search_for_statusbar(foreground)
		if res:
			self._status = res
			return res
		raise NotImplementedError

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if Document in clsList and obj.IA2Attributes.get("tag") == "#document":
			clsList.insert(0, VSCodeDocument)

	def getStatusBarText(self, obj: NVDAObject) -> str:
		parts: list[str] = [
			chunk
			for child in obj.children
			for label in (child.name, child.value)
			if label and (chunk := label.strip())
		]

		if not parts:
			raise NotImplementedError

		pos_idx = next((i for i, e in enumerate(parts) if self._looks_like_line_col(e)), None)
		if pos_idx is not None and pos_idx > 0:
			# Move line and column to the start for speech-friendliness
			parts.insert(0, parts.pop(pos_idx))
		return " ".join(parts)

	def event_NVDAObject_init(self, obj: NVDAObject):
		if isinstance(obj, EditableTextBase):
			obj._supportsSentenceNavigation = False
		# TODO: This is a specific fix for Visual Studio Code.
		# Once the underlying issue is resolved, this workaround can be removed.
		# See issue #15159 for more details.
		if obj.role != controlTypes.Role.EDITABLETEXT and controlTypes.State.EDITABLE not in obj.states:
			obj.TextInfo = NVDAObjectTextInfo
		if obj.role == controlTypes.Role.STATUSBAR:
			self._status = obj
