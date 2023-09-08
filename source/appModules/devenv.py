# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2010-2022 NV Access Limited, Soronel Haetir, Babbage B.V., Francisco Del Roio,
# Leonard de Ruijter

import objbase
import comtypes
from locationHelper import RectLTWH
from logHandler import log
import textInfos.offsets

from NVDAObjects.behaviors import EditableText, EditableTextWithoutAutoSelectDetection
from NVDAObjects.window import Window
from comtypes.automation import IDispatch
from NVDAObjects.window import DisplayModelEditableText
from NVDAObjects.IAccessible import IAccessible
from NVDAObjects.UIA import UIA, WpfTextView, UIATextInfo
from enum import IntEnum
import appModuleHandler
import controlTypes
import threading
import UIAHandler


# A few helpful constants
# vsWindowType Enum
class VsWindowType(IntEnum):
	ToolWindow = 15
	Document = 16
	Output = 17


# Scroll bar selector
SB_HORZ = 0
SB_VERT = 1


class AppModule(appModuleHandler.AppModule):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._DTECache = {}
		vsMajor, vsMinor, rest = self.productVersion.split(".", 2)
		self.vsMajor, self.vsMinor = int(vsMajor), int(vsMinor)

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if WpfTextView in clsList:
			clsList.remove(WpfTextView)
			clsList.insert(0, VsWpfTextView)
		# Only use this overlay class if the top level automation object for the IDE can be retrieved,
		# as it will not work otherwise.
		elif obj.windowClassName == "VsTextEditPane" and self.DTE:
			try:
				clsList.remove(DisplayModelEditableText)
			except ValueError:
				pass
			clsList[0:0] = [VsTextEditPane, EditableTextWithoutAutoSelectDetection]
		elif (
			(self.vsMajor == 15 and self.vsMinor >= 3)
			or self.vsMajor >= 16
		):
			if obj.role == controlTypes.Role.TREEVIEWITEM and obj.windowClassName == "LiteTreeView32":
				clsList.insert(0, ObjectsTreeItem)

	def _getDTE(self):
		# Retrieve the top level automation object for the IDE
		bctx = objbase.CreateBindCtx()
		ROT = objbase.GetRunningObjectTable()
		for mon in ROT:
			displayName = mon.GetDisplayName(bctx, None)
			if displayName == f"!VisualStudio.DTE.{self.vsMajor}.0:{self.processID}":
				return comtypes.client.dynamic.Dispatch(ROT.GetObject(mon).QueryInterface(IDispatch))
		else:
			# None found.
			log.debugWarning("No top level automation object found", exc_info=True)
			return None

	def _get_DTE(self):
		thread = threading.get_ident()
		# Return the already fetched instance if there is one.
		DTE = self._DTECache.get(thread)
		if DTE:
			return DTE

		DTE = self._DTECache[thread] = self._getDTE()
		return DTE


class VsWpfTextViewTextInfo(UIATextInfo):

	def _getLineNumberString(self, textRange):
		# Visual Studio exposes line numbers as part of the actual text.
		# We want to store the line number in a format field instead.
		lineNumberRange = textRange.Clone()
		lineNumberRange.MoveEndpointByRange(
			UIAHandler.TextPatternRangeEndpoint_End,
			lineNumberRange,
			UIAHandler.TextPatternRangeEndpoint_Start
		)
		return lineNumberRange.GetText(-1)

	def _getFormatFieldAtRange(self, textRange, formatConfig, ignoreMixedValues=False):
		formatField = super()._getFormatFieldAtRange(textRange, formatConfig, ignoreMixedValues=ignoreMixedValues)
		if not formatField or not formatConfig['reportLineNumber']:
			return formatField
		lineNumberStr = self._getLineNumberString(textRange)
		if lineNumberStr:
			try:
				formatField.field['line-number'] = int(lineNumberStr)
			except ValueError:
				log.debugWarning(
					f"Couldn't parse {lineNumberStr} as integer to report a line number",
					exc_info=True
				)
		return formatField

	def _getTextFromUIARange(self, textRange):
		text = super()._getTextFromUIARange(textRange)
		lineNumberStr = self._getLineNumberString(textRange)
		return text[(0 if not lineNumberStr else len(lineNumberStr)):]


class VsWpfTextView(WpfTextView):
	TextInfo = VsWpfTextViewTextInfo


class VsTextEditPaneTextInfo(textInfos.offsets.OffsetsTextInfo):

	def _get__selectionObject(self):
		window = self.obj._window
		if window.Type == VsWindowType.Document:
			selection = window.Selection
		elif window.Type == VsWindowType.Output:
			selection = window.Object.ActivePane.TextDocument.Selection
		elif window.Type == VsWindowType.ToolWindow:
			selection = window.Object.TextDocument.Selection
		else:
			raise RuntimeError(f"Unknown window type: {window.Kind}")
		self._selectionObject = selection
		return selection

	def _createEditPoint(self):
		return self._selectionObject.ActivePoint.CreateEditPoint()

	def _getCaretOffset(self):
		return self._createEditPoint().AbsoluteCharOffset - 1

	def _setCaretOffset(self, offset):
		self._selectionObject.MoveToAbsoluteOffset(offset + 1)

	def _setSelectionOffsets(self, start, end):
		self._selectionObject.MoveToAbsoluteOffset(start + 1)
		self._selectionObject.MoveToAbsoluteOffset(end + 1, True)

	def _getSelectionOffsets(self):
		caretPos = self._getCaretOffset()
		anchorPos = self._selectionObject.AnchorPoint.CreateEditPoint().AbsoluteCharOffset - 1
		return min(caretPos, anchorPos), max(caretPos, anchorPos)

	def _getTextRange(self, start, end):
		editPointStart = self._createEditPoint()
		editPointStart.MoveToAbsoluteOffset(start + 1)
		return editPointStart.GetText(end - start)

	def _getWordOffsets(self, offset):
		editPointEnd = self._createEditPoint()
		editPointEnd.MoveToAbsoluteOffset(offset + 1)
		editPointEnd.WordRight()
		editPointStart = editPointEnd.CreateEditPoint()
		editPointStart.WordLeft()
		return editPointStart.AbsoluteCharOffset - 1, editPointEnd.AbsoluteCharOffset - 1

	def _getLineOffsets(self, offset):
		editPointStart = self._createEditPoint()
		editPointStart.MoveToAbsoluteOffset(offset + 1)
		editPointStart.StartOfLine()
		editPointEnd = editPointStart.CreateEditPoint()
		editPointEnd.EndOfLine()
		# Offsets are one based and exclusive
		return editPointStart.AbsoluteCharOffset - 1, editPointEnd.AbsoluteCharOffset

	def _getLineNumFromOffset(self, offset):
		editPoint = self._createEditPoint()
		editPoint.MoveToAbsoluteOffset(offset + 1)
		return editPoint.Line

	def _getStoryLength(self):
		editPoint = self._createEditPoint()
		editPoint.EndOfDocument()
		return editPoint.AbsoluteCharOffset - 1


class VsTextEditPane(EditableText, Window):

	def _get_TextInfo(self):
		try:
			if self._window.Type in iter(VsWindowType):
				return VsTextEditPaneTextInfo
			else:
				log.debugWarning(
					f"Retrieved Visual Studio window object, but unknown type: {self._window.Type}"
				)
		except Exception:
			log.debugWarning("Couldn't retrieve Visual Studio window object", exc_info=True)
		return super().TextInfo

	def initOverlayClass(self):
		self._window = self.appModule.DTE.ActiveWindow

	def _get_location(self):
		if not isinstance(self, UIA):
			return RectLTWH(
				self._window.Left,
				self._window.Top,
				self._window.Width,
				self._window.Height
			)
		return super().location

	def event_valueChange(self):
		pass


class ObjectsTreeItem(IAccessible):

	def _get_focusRedirect(self):
		"""
		Returns the correct focused item in the object explorer trees
		"""

		if controlTypes.State.FOCUSED not in self.states:
			# Object explorer tree views have a bad IAccessible implementation.
			# When expanding a primary node and going to secondary node, the
			# focus is placed to the next root node, so we need to redirect
			# it to the real focused widget. Fortunately, the states are
			# still correct and we can detect if this is really focused or not.
			return self.objectWithFocus()

	def _get_positionInfo(self):
		return {
			"level": int(self.IAccessibleObject.accValue(self.IAccessibleChildID))
		}
