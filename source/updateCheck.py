#updateCheck.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2012 NV Access Limited

"""Update checking functionality.
"""

import sys
import os
import threading
import urllib
import wx
import versionInfo
import languageHandler
import gui
from logHandler import log
import config

CHECK_URL = "http://www.nvda-project.org/updateCheck"

# FIXME
state = {
	"lastCheck": 0,
	"dontRemindVersion": None,
}

def checkForUpdate(auto=False):
	"""Check for an updated version of NVDA.
	This will block, so it generally shouldn't be called from the main thread.
	@param auto: Whether this is an automatic check for updates.
	@type auto: bool
	@return: Information about the update or C{None} if there is no update.
	@rtype: dict
	@raise RuntimeError: If there is an error checking for an update.
	"""
	winVer = sys.getwindowsversion()
	params = {
		"autoCheck": auto,
		"version": versionInfo.version,
		"versionType": "stable",
		"osVersion": "{v.major}.{v.minor}.{v.build} {v.service_pack}".format(v=winVer),
		"x64": os.environ.get("PROCESSOR_ARCHITEW6432") == "AMD64",
		"language": languageHandler.getLanguage(),
	}
	res = urllib.urlopen("%s?%s" % (CHECK_URL, urllib.urlencode(params)))
	if res.code != 200:
		raise RuntimeError("Checking for update failed with code %d" % res.code)
	info = {}
	for line in res:
		line = line.rstrip()
		try:
			key, val = line.split(": ", 1)
		except ValueError:
			raise RuntimeError("Error in update check output")
		info[key] = val
	if not info:
		return None
	return info

class CheckForUpdateUi(object):
	"""Check for an updated version of NVDA, presenting appropriate user interface.
	Checks are performed in the background.
	"""

	def __init__(self, auto=False):
		"""Constructor.
		@param auto: Whether this is an automatic check for updates.
		@type auto: bool
		"""
		self.auto = auto
		t = threading.Thread(target=self._bg)
		t.daemon = True
		t.start()

	def _bg(self):
		try:
			info = checkForUpdate(self.auto)
		except:
			if self.auto:
				log.debugWarning("Error checking for update", exc_info=True)
			else:
				log.error("Error checking for update", exc_info=True)
				wx.CallAfter(self._error)
			return
		if not info:
			# No update.
			if  not self.auto:
				wx.CallAfter(self._result, None)
			return
		version = info["version"]
		if self.auto and state["dontRemindVersion"] == version:
			# The user has already been automatically notified about this version.
			return
		state["dontRemindVersion"] = version
		wx.CallAfter(self._result, info)

	def _error(self):
		gui.messageBox(
			# Translators: A message indicating that an error occurred while checking for an update to NVDA.
			_("Error checking for update."),
			# Translators: The title of an error message dialog.
			_("Error"),
			wx.OK | wx.ICON_ERROR)

	def _result(self, info):
		UpdateResultDialog(gui.mainFrame, info, self.auto)

class UpdateResultDialog(wx.Dialog):

	def __init__(self, parent, updateInfo, auto):
		# Translators: The title of the dialog informing the user about an NVDA update.
		super(UpdateResultDialog, self).__init__(parent, title=_("NVDA Update"))
		self.updateInfo = updateInfo
		mainSizer = wx.BoxSizer(wx.VERTICAL)

		if updateInfo:
			# Translators: A message indicating that an updated version of NVDA is available.
			# {version} will be replaced with the version; e.g. 2011.3.
			message = _("NVDA version {version} is available.").format(**updateInfo)
		else:
			# Translators: A message indicating that no update to NVDA is available.
			message = _("No update available.")
		mainSizer.Add(wx.StaticText(self, label=message))

		if updateInfo:
			# Translators: The label of a button to download an NVDA update.
			item = wx.Button(self, label=_("&Download update"))
			item.Bind(wx.EVT_BUTTON, self.onDownloadButton)
			mainSizer.Add(item)

			if auto:
				# Translators: The label of a button to remind the user later about performing some action.
				item = wx.Button(self, label=_("Remind me &later"))
				item.Bind(wx.EVT_BUTTON, self.onLaterButton)
				mainSizer.Add(item)

		# Translators: The label of a button to close a dialog.
		item = wx.Button(self, wx.ID_CLOSE, label=_("&Close"))
		item.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
		mainSizer.Add(item)
		self.Bind(wx.EVT_CLOSE, lambda evt: self.Destroy())
		self.EscapeId = wx.ID_CLOSE

		self.Sizer = mainSizer
		mainSizer.Fit(self)
		self.Show()

	def onDownloadButton(self, evt):
		if config.isInstalledCopy():
			url = self.updateInfo["installerUrl"]
		else:
			url = self.updateInfo["portableUrl"]
		os.startfile(url)
		self.Close()

	def onLaterButton(self, evt):
		state["dontRemindVersion"] = None
		self.Close()
