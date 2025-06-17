# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU Lesser General Public License.
# See the file COPYING for more details.

"""UI module proxy for add-ons running in ART."""

from typing import Optional

from .base import ServiceProxyMixin


class _UIProxy(ServiceProxyMixin):
	"""Internal proxy class for UI service."""
	_service_env_var = "NVDA_ART_UI_SERVICE_URI"


def message(
	text: str,
	speechPriority: Optional[int] = None,
	brailleText: Optional[str] = None,
) -> None:
	"""Present a message to the user via speech and/or braille.

	This is the most commonly used UI function in add-ons.

	@param text: The text to speak and display in braille.
	@param speechPriority: The speech priority (0-2). None uses default.
	@param brailleText: Alternative text for braille. If None, uses text.
	"""
	_UIProxy._call_service(
		"message",
		text=text,
		speechPriority=speechPriority,
		brailleText=brailleText
	)


def browseableMessage(
	message: str,
	title: Optional[str] = None,
	isHtml: bool = False,
	closeButton: bool = False,
) -> None:
	"""Present a message to the user in a browseable window.

	@param message: The message text or HTML content.
	@param title: The window title. If None, uses default.
	@param isHtml: Whether the message is HTML content.
	@param closeButton: Whether to show only a close button.
	"""
	_UIProxy._call_service(
		"browseableMessage",
		message=message,
		title=title,
		isHtml=isHtml,
		closeButton=closeButton
	)


def reviewMessage(text: str, speechPriority: Optional[int] = None) -> None:
	"""Present a message in review mode.

	@param text: The text to present.
	@param speechPriority: The speech priority.
	"""
	_UIProxy._call_service(
		"reviewMessage",
		text=text,
		speechPriority=speechPriority
	)



# For compatibility with code that might import these
__all__ = ["message", "browseableMessage", "reviewMessage"]
