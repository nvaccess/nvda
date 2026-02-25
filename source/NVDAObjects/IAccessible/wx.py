# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Leonard de Ruijter
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Improvements for wxWidgets objects."""

import api
import eventHandler
import winUser

from . import IAccessible, getNVDAObjectFromEvent
from logHandler import log
import windowUtils
from .. import NVDAObject


def findExtraOverlayClasses(obj: IAccessible, clsList: list[NVDAObject]):
	if obj.name == "wxWebView":
		clsList.insert(0, WxWebView)


class WxWebView(IAccessible):
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
