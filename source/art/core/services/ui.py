# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""UI service for ART - provides user interface functionality to add-ons."""

import Pyro5.api
import ui
import speech
from logHandler import log
from .base import BaseService


@Pyro5.api.expose
class UIService(BaseService):
	"""Provides UI functionality for add-ons running in ART."""
	
	def __init__(self):
		super().__init__("UIService")
	
	def message(
		self,
		text: str,
		speechPriority: int = None,
		brailleText: str = None
	) -> None:
		"""Present a message to the user via speech and/or braille.
		
		@param text: The text to speak and display in braille.
		@param speechPriority: The speech priority. None uses default.
		@param brailleText: Alternative text for braille. If None, uses text.
		"""
		try:
			# Map None to actual default priority
			if speechPriority is None:
				speechPriority = speech.Spri.MESSAGE
			
			# Call the actual ui.message function
			ui.message(
				text=text,
				speechPriority=speechPriority,
				brailleText=brailleText
			)
			
			log.debug(f"UI message from ART: {text[:50]}...")
			
		except Exception:
			self._log_error("message", f"text={text[:50]}...")
	
	def browseableMessage(
		self,
		message: str,
		title: str = None,
		isHtml: bool = False,
		closeButton: bool = False
	) -> None:
		"""Present a message in a browseable window.
		
		@param message: The message text or HTML content.
		@param title: The window title.
		@param isHtml: Whether the message is HTML.
		@param closeButton: Whether to show only a close button.
		"""
		try:
			# Import here to avoid circular imports
			import ui
			
			ui.browseableMessage(
				message=message,
				title=title,
				isHtml=isHtml,
				closeButton=closeButton
			)
			
			log.debug(f"Browseable message from ART: {title or 'No title'}")
			
		except Exception:
			self._log_error("browseableMessage", f"title={title}")
	
	def reviewMessage(
		self,
		text: str,
		speechPriority: int = None
	) -> None:
		"""Present a message in review mode.
		
		@param text: The text to present.
		@param speechPriority: The speech priority.
		"""
		try:
			# Map None to actual default priority
			if speechPriority is None:
				speechPriority = speech.Spri.MESSAGE
			
			ui.reviewMessage(
				text=text,
				speechPriority=speechPriority
			)
			
			log.debug(f"Review message from ART: {text[:50]}...")
			
		except Exception:
			self._log_error("reviewMessage", f"text={text[:50]}...")
