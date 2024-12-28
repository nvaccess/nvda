from typing import Any

import braille

from . import callback_manager


class NVDAPatcher(callback_manager.CallbackManager):
	"""Base class to manage patching of braille display changes."""

	def registerSetDisplay(self) -> None:
		braille.displayChanged.register(self.handle_displayChanged)
		braille.displaySizeChanged.register(self.handle_displaySizeChanged)

	def unregisterSetDisplay(self) -> None:
		braille.displaySizeChanged.unregister(self.handle_displaySizeChanged)
		braille.displayChanged.unregister(self.handle_displayChanged)

	def register(self) -> None:
		self.registerSetDisplay()

	def unregister(self) -> None:
		self.unregisterSetDisplay()

	def handle_displayChanged(self, display: Any) -> None:
		self.callCallbacks("set_display", display=display)

	def handle_displaySizeChanged(self, displaySize: Any) -> None:
		self.callCallbacks("set_display", displaySize=displaySize)
