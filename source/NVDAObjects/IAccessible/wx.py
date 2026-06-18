# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Improvements for wxWidgets objects."""

import api
import eventHandler
import winUser

from . import IAccessible, getNVDAObjectFromEvent
from logHandler import log
import windowUtils
from .. import NVDAObject


def findExtraOverlayClasses(obj: IAccessible, clsList: list[NVDAObject]):
	if obj.name == "wxWebView" and obj.event_objectID == winUser.OBJID_CLIENT:
		clsList.insert(0, WxWebView)


class WxWebView(IAccessible):
	def reportFocus(self):
		# Reporting the wxWebView control gaining focus is redundant since it redirects focus to its inner content.
		pass

	def event_gainFocus(self) -> None:
		super().event_gainFocus()
		firstChild = self.firstChild
		if not firstChild:
			return
		match firstChild.windowClassName:
			case "Shell Embedding":
				# This is an IE webview.
				try:
					obj = getNVDAObjectFromEvent(
						windowUtils.findDescendantWindow(
							firstChild.windowHandle,
							className="Internet Explorer_Server",
						),
						winUser.OBJID_CLIENT,
						winUser.CHILDID_SELF,
					)
					obj.setFocus()
				except LookupError:
					log.warning("Could not find Internet Explorer_Server in wxWebView")
			case "Chrome_WidgetWin_0":
				# This is a Edge WebView2 control.
				# First focus might fail when the inner window is not yet created.
				while not eventHandler.isPendingEvents("gainFocus"):
					# Wait for the window and refocus when it is there.
					try:
						windowUtils.findDescendantWindow(
							firstChild.windowHandle,
							className="Chrome_RenderWidgetHostHWND",
						)
					except LookupError:
						api.processPendingEvents()
						continue
					else:
						# Suppress IAccessible focus event handling for the refocus below.
						# This prevents duplicate or unwanted focus events of the Web View parent control,
						# since we're actually interested in the focus event from the inner document that focus is propagated to.
						self.shouldAllowIAccessibleFocusEvent = False
						self.setFocus()
						break

			case _:
				log.warning(f"Unexpected inner control in wxWebView: {firstChild.windowClassName}")
