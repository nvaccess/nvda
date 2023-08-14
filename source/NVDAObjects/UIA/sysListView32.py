# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2023 NV Access Limited, Leonard de Ruijter
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.


"""Module for native UIA implementations of SysListView32, e.g. in Windows Forms."""

import config
from config.configFlags import ReportTableHeaders
import UIAHandler
from ..behaviors import RowWithFakeNavigation
from . import ListItem, UIA


def findExtraOverlayClasses(obj, clsList):
	UIAControlType = obj.UIAElement.cachedControlType
	if UIAControlType == UIAHandler.UIA.UIA_ListItemControlTypeId:
		clsList.insert(0, SysListViewItem)
	if UIAControlType == UIAHandler.UIA.UIA_ListControlTypeId:
		clsList.insert(0, SysListViewList)


class SysListViewList(UIA):
	...


class SysListViewItem(RowWithFakeNavigation, ListItem):

	def _get_name(self):
		parent = self.parent
		if not isinstance(parent, SysListViewList) or self.childCount == 0:
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
			if name and config.conf['documentFormatting']['reportTableHeaders'] in (
				ReportTableHeaders.ROWS_AND_COLUMNS,
				ReportTableHeaders.COLUMNS,
			) and index > 0:
				columnHeaderItems = e.getCachedPropertyValueEx(
					UIAHandler.UIA.UIA_TableItemColumnHeaderItemsPropertyId,
					True
				)
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

	def _get_rowNumber(self):
		parent = self.parent
		if not isinstance(parent, SysListViewList) or self.childCount == 0:
			return super().rowNumber
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
			return super().rowNumber
		return val + 1
