# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2023 NV Access Limited, Leonard de Ruijter
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.


"""Module for native UIA implementations of SysListView32, e.g. in Windows Forms."""

from typing import Dict, List, Optional, Type
from comtypes import COMError
import config
from logHandler import log
from config.configFlags import ReportTableHeaders
import UIAHandler
from .. import NVDAObject
from ..behaviors import RowWithFakeNavigation
from . import ListItem, UIA


def findExtraOverlayClasses(obj: NVDAObject, clsList: List[Type[NVDAObject]]) -> None:
	UIAControlType = obj.UIAElement.cachedControlType
	if UIAControlType == UIAHandler.UIA.UIA_ListControlTypeId:
		clsList.insert(0, SysListViewList)
	elif UIAControlType == UIAHandler.UIA.UIA_ListItemControlTypeId and isinstance(obj.parent, SysListViewList):
		clsList.insert(0, SysListViewItem)
		if obj.parent._getUIACacheablePropertyValue(UIAHandler.UIA.UIA_IsTablePatternAvailablePropertyId):
			clsList.insert(0, RowWithFakeNavigation)


class SysListViewList(UIA):
	...


class SysListViewItem(ListItem):

	def _get_name(self) -> str:
		parent = self.parent
		if not isinstance(parent, SysListViewList) or self.childCount <= 1:
			return super().name
		childrenCacheRequest = UIAHandler.handler.baseCacheRequest.clone()
		childrenCacheRequest.addProperty(UIAHandler.UIA.UIA_NamePropertyId)
		childrenCacheRequest.addProperty(UIAHandler.UIA.UIA_TableItemColumnHeaderItemsPropertyId)
		childrenCacheRequest.TreeScope = UIAHandler.TreeScope_Children
		cachedChildren = self.UIAElement.buildUpdatedCache(childrenCacheRequest).getCachedChildren()
		if not cachedChildren:
			# There are no children
			return super().name
		textList = []
		for index in range(cachedChildren.length):
			e = cachedChildren.getElement(index)
			name = e.cachedName
			columnHeaderTextList = []
			if (
				name
				and config.conf['documentFormatting']['reportTableHeaders'] in (
					ReportTableHeaders.ROWS_AND_COLUMNS,
					ReportTableHeaders.COLUMNS,
				)
				and index > 0
			):
				try:
					columnHeaderItems = e.getCachedPropertyValueEx(
						UIAHandler.UIA.UIA_TableItemColumnHeaderItemsPropertyId,
						False
					)
				except COMError:
					log.debugWarning("Couldn't fetch column header items", exc_info=True)
					columnHeaderItems = None
			else:
				columnHeaderItems = None
			if columnHeaderItems:
				columnHeaderItems = columnHeaderItems.QueryInterface(UIAHandler.IUIAutomationElementArray)
				for innerIndex in range(columnHeaderItems.length):
					columnHeaderItem = columnHeaderItems.getElement(innerIndex)
					columnHeaderTextList.append(columnHeaderItem.currentName)
			columnHeaderText = " ".join(columnHeaderTextList)
			if columnHeaderText:
				text = f"{columnHeaderText} {name}"
			else:
				text = name
			textList.append(text)
		return "; ".join(textList)

	def _get_indexInParent(self) -> Optional[int]:
		parent = self.parent
		if not isinstance(parent, SysListViewList) or self.childCount == 0:
			return super().indexInParent
		childCacheRequest = UIAHandler.handler.baseCacheRequest.clone()
		childCacheRequest.addProperty(UIAHandler.UIA.UIA_GridItemRowPropertyId)
		element = UIAHandler.handler.baseTreeWalker.GetFirstChildElementBuildCache(
			self.UIAElement,
			childCacheRequest
		)
		val = element.getCachedPropertyValueEx(
			UIAHandler.UIA.UIA_GridItemRowPropertyId,
			True
		)
		if val == UIAHandler.handler.reservedNotSupportedValue:
			return super().indexInParent
		return val

	def _get_positionInfo(self) -> Dict[str, int]:
		info = super().positionInfo or {}
		itemIndex = 0
		try:
			itemIndex = self.indexInParent + 1
		except (COMError, NotImplementedError):
			pass
		if itemIndex > 0:
			info['indexInGroup'] = itemIndex
			itemCount = 0
			try:
				itemCount = self.parent.rowCount
			except (COMError, NotImplementedError):
				pass
			if itemCount > 0:
				info['similarItemsInGroup'] = itemCount
		return info
