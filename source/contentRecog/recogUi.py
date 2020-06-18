#contentRecog/recogUi.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2017 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""User interface for content recognition.
This module provides functionality to capture an image from the screen
for the current navigator object, pass it to a content recognizer for recognition
and present the result to the user so they can read it with cursor keys, etc.
NVDA scripts or GUI call the L{recognizeNavigatorObject} function with the recognizer they wish to use.
"""

import api
import ui
import screenBitmap
import NVDAObjects.window
from NVDAObjects.behaviors import LiveText
import controlTypes
import browseMode
import cursorManager
import eventHandler
import textInfos
from logHandler import log
import queueHandler
import core
from . import RecogImageInfo, BaseContentRecogTextInfo


class RecogResultNVDAObject(cursorManager.CursorManager, LiveText, NVDAObjects.window.Window):
	"""Fake NVDAObject used to present a recognition result in a cursor manager.
	This allows the user to read the result with cursor keys, etc.
	Pressing enter will activate (e.g. click) the text at the cursor.
	Pressing escape dismisses the recognition result.
	"""
	#: How often (in ms) to perform recognition.
	REFRESH_INTERVAL = 1500

	role = controlTypes.Role.DOCUMENT
	# Translators: The title of the document used to present the result of content recognition.
	name = _("Result")
	treeInterceptor = None

	def __init__(self, recognizer=None, imageInfo=None, obj=None):
		self.parent = parent = api.getFocusObject()
		self.recognizer = recognizer
		self.imageInfo = imageInfo
		self.result = None
		super(RecogResultNVDAObject, self).__init__(windowHandle=parent.windowHandle)
		LiveText.initOverlayClass(self)

	def start(self):
		self._recognize(self._onFirstResult)

	def _get_hasFocus(self):
		return self is api.getFocusObject()

	def _recognize(self, onResult):
		if self.result and not self.hasFocus:
			# We've already recognized once, so we did have focus, but we don't any
			# more. This means the user dismissed the recognition result, so we
			# shouldn't recognize again.
			return
		imgInfo = self.imageInfo
		sb = screenBitmap.ScreenBitmap(imgInfo.recogWidth, imgInfo.recogHeight)
		pixels = sb.captureImage(
			imgInfo.screenLeft, imgInfo.screenTop,
			imgInfo.screenWidth, imgInfo.screenHeight
		)
		self.recognizer.recognize(pixels, self.imageInfo, onResult)

	def _onFirstResult(self, result):
		global _activeRecog
		_activeRecog = None
		# This might get called from a background thread, so any UI calls must be queued to the main thread.
		if isinstance(result, Exception):
			log.error("Recognition failed: %s" % result)
			# Translators: Reported when recognition (e.g. OCR) fails.
			queueHandler.queueFunction(
				queueHandler.eventQueue, ui.message, _("Recognition failed")
			)
			return
		self.result = result
		self._selection = self.makeTextInfo(textInfos.POSITION_FIRST)
		# This method queues an event to the main thread.
		self.setFocus()
		if self.recognizer.allowAutoRefresh:
			self._scheduleRecognize()

	def _scheduleRecognize(self):
		core.callLater(self.REFRESH_INTERVAL, self._recognize, self._onResult)

	def _onResult(self, result):
		import tones  # jtd
		tones.beep(1660, 10)  # jtd
		if not self.hasFocus:
			# The user has dismissed the recognition result.
			return
		self.result = result
		# The current selection refers to the old result. We need to refresh that,
		# but try to keep the same cursor position.
		self.selection = self.makeTextInfo(self._selection.bookmark)
		# Tell LiveText that our text has changed.
		self.event_textChange()
		self._scheduleRecognize()

	def makeTextInfo(self, position):
		# Maintain our own fake selection/caret.
		if position == textInfos.POSITION_SELECTION:
			ti = self._selection.copy()
		elif position == textInfos.POSITION_CARET:
			ti = self._selection.copy()
			ti.collapse()
		else:
			ti = self.result.makeTextInfo(self, position)
		return ti

	def setFocus(self):
		ti = self.parent.treeInterceptor
		if isinstance(ti, browseMode.BrowseModeDocumentTreeInterceptor):
			# Normally, when entering browse mode from a descendant (e.g. dialog),
			# we want the cursor to move to the focus (#3145).
			# However, we don't want this for recognition results, as these aren't focusable.
			ti._enteringFromOutside = True
		# This might get called from a background thread and all NVDA events must run in the main thread.
		eventHandler.queueEvent("gainFocus", self)

	def event_gainFocus(self):
		super().event_gainFocus()
		if self.recognizer.allowAutoRefresh:
			# Make LiveText watch for and report new text.
			self.startMonitoring()

	def event_loseFocus(self):
		super().event_loseFocus()
		if self.recognizer.allowAutoRefresh:
			self.stopMonitoring()

	def script_activatePosition(self, gesture):
		try:
			self._selection.activate()
		except NotImplementedError:
			log.debugWarning("Result TextInfo does not implement activate")
	# Translators: Describes a command.
	script_activatePosition.__doc__ = _("Activates the text at the cursor if possible")

	def script_exit(self, gesture):
		self.recognizer.cancel()
		eventHandler.executeEvent("gainFocus", self.parent)
	# Translators: Describes a command.
	script_exit.__doc__ = _("Dismiss the recognition result")

	# The find commands are tricky to support because they pop up dialogs.
	# This moves the focus, so we lose our fake focus.
	# See https://github.com/nvaccess/nvda/pull/7361#issuecomment-314698991
	def script_find(self, gesture):
		# Translators: Reported when a user tries to use a find command when it isn't supported.
		ui.message(_("Not supported in this document"))

	def script_findNext(self, gesture):
		# Translators: Reported when a user tries to use a find command when it isn't supported.
		ui.message(_("Not supported in this document"))

	def script_findPrevious(self, gesture):
		# Translators: Reported when a user tries to use a find command when it isn't supported.
		ui.message(_("Not supported in this document"))

	__gestures = {
		"kb:enter": "activatePosition",
		"kb:space": "activatePosition",
		"kb:escape": "exit",
	}

#: Keeps track of the recognition in progress, if any.
_activeRecog = None
def recognizeNavigatorObject(recognizer):
	"""User interface function to recognize content in the navigator object.
	This should be called from a script or in response to a GUI action.
	@param recognizer: The content recognizer to use.
	@type recognizer: L{contentRecog.ContentRecognizer}
	"""
	global _activeRecog
	if isinstance(api.getFocusObject(), RecogResultNVDAObject):
		# Translators: Reported when content recognition (e.g. OCR) is attempted,
		# but the user is already reading a content recognition result.
		ui.message(_("Already in a content recognition result"))
		return
	nav = api.getNavigatorObject()
	if not recognizer.validateObject(nav):
		return
	# Translators: Reported when content recognition (e.g. OCR) is attempted,
	# but the content is not visible.
	notVisibleMsg = _("Content is not visible")
	try:
		left, top, width, height = nav.location
	except TypeError:
		log.debugWarning("Object returned location %r" % nav.location)
		ui.message(notVisibleMsg)
		return
	if not recognizer.validateCaptureBounds(nav.location):
		return
	try:
		imgInfo = RecogImageInfo.createFromRecognizer(left, top, width, height, recognizer)
	except ValueError:
		ui.message(notVisibleMsg)
		return
	if _activeRecog:
		_activeRecog.recognizer.cancel()
	# Translators: Reporting when content recognition (e.g. OCR) begins.
	ui.message(_("Recognizing"))
	_activeRecog = RecogResultNVDAObject(recognizer=recognizer, imageInfo=imgInfo)
	_activeRecog.start()
