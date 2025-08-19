# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024, NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import threading
from enum import Enum, auto
from typing import Callable, Iterable

import config
import requests
import wx
from logHandler import log
from requests.exceptions import RequestException
from url_normalize import url_normalize

import gui

from . import guiHelper
from .settingsDialogs import SettingsDialog
from . import nvdaControls

class _ValidationError(ValueError):
	"""Exception raised when validation of an OK response returns False.
	This is only used internally.
	"""


class _SetURLDialog(SettingsDialog):
	class _URLTestStatus(Enum):
		UNTESTED = auto()
		PASSED = auto()
		FAILED = auto()

	_progressDialog: "gui.IndeterminateProgressDialog | None" = None
	_testStatus: _URLTestStatus = _URLTestStatus.UNTESTED

	def __init__(
		self,
		parent: wx.Window,
		title: str,
		configPath: Iterable[str],
		helpId: str | None = None,
		urlTransformer: Callable[[str], str] = lambda url: url,
		responseValidator: Callable[[requests.Response], bool] = lambda response: True,
		*args,
		**kwargs,
	):
		"""Customisable dialog for requesting a URL from the user.

		:param parent: Parent window of this dialog.
		:param title: Title of this dialog.
		:param configPath: Where in the config the URL is to be stored.
		:param helpId: Anchor of the user guide section for this dialog, defaults to None
		:param urlTransformer: Function to transform the given URL into something usable, eg by adding required query parameters. Defaults to the identity function.
		:param responseValidator: Function to check that the response returned when querying the transformed URL is valid.
			The response will always have a status of 200 (OK). Defaults to always returning True.
		:raises ValueError: If no config path is given.
		"""
		if not configPath or len(configPath) < 1:
			raise ValueError("Config path not provided.")
		self.title = title
		self.helpId = helpId
		self._configPath = configPath
		self._urlTransformer = urlTransformer
		self._responseValidator = responseValidator
		super().__init__(parent, *args, **kwargs)

	def makeSettings(self, settingsSizer: wx.Sizer):
		self.SetFont(nvdaControls.FontActions.getFontFromConfig())
		settingsSizerHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		self._urlControl = urlControl = settingsSizerHelper.addLabeledControl(
			# Translators: The label of a text box asking the user for a URL.
			# The purpose of this text box will be explained elsewhere in the user interface.
			_("&URL:"),
			wx.TextCtrl,
			size=(250, -1),
		)
		self.bindHelpEvent("SetURLTextbox", urlControl)
		self._testButton = testButton = wx.Button(
			self,
			# Translators: A button in a dialog which allows the user to test a URL that they have entered.
			label=_("&Test..."),
		)
		self.bindHelpEvent("SetURLTest", testButton)
		urlControlsSizerHelper = guiHelper.BoxSizerHelper(self, sizer=urlControl.GetContainingSizer())
		urlControlsSizerHelper.addItem(testButton)
		testButton.Bind(wx.EVT_BUTTON, self._onTest)
		# We need to bind the text change handler before setting the text of the URL control so that it gets called when we populate the URL control.
		# This allows us to rely on the URL control emitting the text event which will enable the test button, rather than having to doo so manually.
		urlControl.Bind(wx.EVT_TEXT, self._onTextChange)
		self._url = self._getFromConfig()

	def postInit(self):
		# Ensure that focus is on the URL text box.
		self._urlControl.SetFocus()

	def onOk(self, evt: wx.CommandEvent):
		self._normalize()
		if self._url == self._getFromConfig():
			shouldSave = False
		elif self._url and self._testStatus != _SetURLDialog._URLTestStatus.PASSED:
			ret = gui.messageBox(
				_(
					# Translators: Message shown to users when saving a potentially invalid URL to NVDA's settings.
					"The URL you have entered failed the connection test. Are you sure you want to save it anyway?",
				)
				if self._testStatus == _SetURLDialog._URLTestStatus.FAILED
				else _(
					# Translators: Message shown to users when saving an untested URL to NVDA's settings.
					"The URL you have entered has not been tested. Are you sure you want to save it without attempting to connect to it first?",
				),
				# Translators: The title of a dialog.
				_("Warning"),
				wx.YES_NO | wx.CANCEL | wx.CANCEL_DEFAULT | wx.ICON_WARNING,
				self,
			)
			if ret == wx.YES:
				shouldSave = True
			elif ret == wx.NO:
				shouldSave = False
			else:
				return
		else:
			shouldSave = True

		if shouldSave:
			self._saveToConfig()
			# Hack: Update the mirror URL in the parent window before closing.
			# Otherwise, if focus is immediately returned to the mirror URL text control, NVDA will report the old value even though the new one is reflected visually.
			self.Parent._updateCurrentMirrorURL()
		super().onOk(evt)

	def _onTextChange(self, evt: wx.CommandEvent):
		"""Enable the "Test..." button only when there is text in the URL control, and change the URL's test status when the URL changes."""
		value = self._url
		self._testButton.Enable(not (len(value) == 0 or value.isspace()))
		self._testStatus = _SetURLDialog._URLTestStatus.UNTESTED

	def _onTest(self, evt: wx.CommandEvent):
		"""Normalize the URL, start a background thread to test it, and show an indeterminate progress dialog to the user."""
		self._normalize()
		t = threading.Thread(
			name=f"{self.__class__.__module__}.{self._onTest.__qualname__}",
			target=self._bg,
			daemon=True,
		)
		self._progressDialog = gui.IndeterminateProgressDialog(
			self,
			title=self.title,
			# Translators: A message shown to users when connecting to a URL to ensure it is valid.
			message=_("Validating URL..."),
		)
		t.start()

	def _bg(self):
		"""Background URL connection thread."""
		try:
			with requests.get(self._urlTransformer(self._url)) as r:
				r.raise_for_status()
				if not self._responseValidator(r):
					raise _ValidationError
			self._success()
		except (RequestException, _ValidationError) as e:
			log.debug(f"URL check failed: {e}")
			self._failure(e)

	def _success(self):
		"""Notify the user that we successfully connected to their URL."""
		wx.CallAfter(self._progressDialog.done)
		self._progressDialog = None
		self._testStatus = _SetURLDialog._URLTestStatus.PASSED
		wx.CallAfter(
			gui.messageBox,
			# Translators: Message shown to users when testing a given URL has succeeded.
			_("Successfully connected to the given URL."),
			# Translators: The title of a dialog presented when a test succeeds
			_("Success"),
			wx.OK,
		)

	def _failure(self, error: Exception):
		"""Notify the user that testing their URL failed."""
		if isinstance(error, _ValidationError):
			tip = _(
				# Translators: Tip shown to users when testing a given URL has failed because the response was invalid.
				"The response from the server was not recognised. Check the URL is correct before trying again.",
			)
		elif isinstance(error, requests.HTTPError):
			# Translators: Tip shown to users when testing a given URL has failed because the server returned an error.
			tip = _("The server returned an error. Check that the URL is correct before trying again.")
		elif isinstance(error, requests.ConnectionError):
			# Translators: Tip shown to users when testing a given URL has failed because of a network error.
			tip = _("There was a network error. Check that you are connected to the internet and try again.")
		elif isinstance(
			error,
			(
				requests.exceptions.InvalidURL,
				requests.exceptions.MissingSchema,
				requests.exceptions.InvalidSchema,
			),
		):
			# Translators: Tip shown to users when testing a given URL has failed because the URL was invalid.
			tip = _("The URL you have entered is not valid. Check that it is correct and try again.")
		else:
			# Translators: Tip shown to users when testing a given URL has failed for unknown reasons.
			tip = _("Make sure you are connected to the internet and the URL is correct.")
		# Translators: Message shown to users when testing a given URL has failed.
		# {tip} will be replaced with a tip on how to resolve the issue.
		message = _("The URL you have entered failed the connection test. {tip}").format(tip=tip)
		wx.CallAfter(self._progressDialog.done)
		self._progressDialog = None
		self._testStatus = _SetURLDialog._URLTestStatus.FAILED
		wx.CallAfter(
			gui.messageBox,
			message,
			# Translators: The title of a dialog presented when an error occurs.
			"Error",
			wx.OK | wx.ICON_ERROR,
		)

	def _normalize(self):
		"""Normalize the URL in the URL text box."""
		current_url = self._url
		normalized_url = url_normalize(self._url.strip()).rstrip("/")
		if current_url != normalized_url:
			# Only change the value of the textbox if the value has actually changed, as EVT_TEXT will be fired even if the replacement text is identical.
			self._url = normalized_url

	def _getFromConfig(self) -> str:
		"""Get the value pointed to by `configPath` from the config."""
		currentConfigSection = config.conf
		keyIndex = len(self._configPath) - 1
		for index, component in enumerate(self._configPath):
			if index == keyIndex:
				return currentConfigSection[component]
			currentConfigSection = currentConfigSection[component]

	def _saveToConfig(self):
		"""Save the value of `_url` to the config."""
		currentConfigSection = config.conf
		keyIndex = len(self._configPath) - 1
		for index, component in enumerate(self._configPath):
			if index == keyIndex:
				currentConfigSection[component] = self._url
			currentConfigSection = currentConfigSection[component]

	@property
	def _url(self) -> str:
		return self._urlControl.GetValue()

	@_url.setter
	def _url(self, val: str):
		self._urlControl.SetValue(val)
