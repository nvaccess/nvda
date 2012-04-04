#updateCheck.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2012 NV Access Limited

"""Update checking functionality.
@note: This module may raise C{RuntimeError} on import if update checking for this build is not supported.
"""

import versionInfo
if not versionInfo.updateVersionType:
	raise RuntimeError("No update version type, update checking not supported")

import sys
import os
import threading
import time
import cPickle
import urllib
import tempfile
import wx
import languageHandler
import gui
from logHandler import log
import config
import globalVars
import shellapi

#: The URL to use for update checks.
CHECK_URL = "http://www.nvda-project.org/updateCheck"
#: The time to wait between checks.
CHECK_INTERVAL = 86400 # 1 day
#: The time to wait before retrying a failed check.
RETRY_INTERVAL = 600 # 10 min
#: The download block size in bytes.
DOWNLOAD_BLOCK_SIZE = 8 * 1024 # 8 kb

#: Persistent state information.
#: @type: dict
state = None
_stateFileName = None
#: The single instance of L{AutoUpdateChecker} if automatic update checking is enabled,
#: C{None} if it is disabled.
autoChecker = None

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
		"versionType": versionInfo.updateVersionType,
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

class UpdateChecker(object):
	"""Check for an updated version of NVDA, presenting appropriate user interface.
	The check is performed in the background.
	This class is for manual update checks.
	To use, call L{check} on an instance.
	"""
	AUTO = False

	def check(self):
		"""Check for an update.
		"""
		t = threading.Thread(target=self._bg)
		t.daemon = True
		t.start()

	def _bg(self):
		try:
			info = checkForUpdate(self.AUTO)
		except:
			log.debugWarning("Error checking for update", exc_info=True)
			self._error()
			return
		self._result(info)
		if info:
			state["dontRemindVersion"] = info["version"]
		state["lastCheck"] = time.time()
		saveState()
		if autoChecker:
			autoChecker.setNextCheck()

	def _error(self):
		wx.CallAfter(gui.messageBox,
			# Translators: A message indicating that an error occurred while checking for an update to NVDA.
			_("Error checking for update."),
			# Translators: The title of an error message dialog.
			_("Error"),
			wx.OK | wx.ICON_ERROR)

	def _result(self, info):
		wx.CallAfter(UpdateResultDialog, gui.mainFrame, info, False)

class AutoUpdateChecker(UpdateChecker):
	"""Automatically check for an updated version of NVDA.
	To use, create a single instance and maintain a reference to it.
	Checks will then be performed automatically.
	"""
	AUTO = True

	def __init__(self):
		self._checkTimer = wx.PyTimer(self.check)
		# Set the initial check based on the last check time.
		secs = CHECK_INTERVAL - int(min(time.time() - state["lastCheck"], CHECK_INTERVAL))
		self._checkTimer.Start(secs * 1000, True)

	def setNextCheck(self, isRetry=False):
		self._checkTimer.Stop()
		self._checkTimer.Start((RETRY_INTERVAL if isRetry else CHECK_INTERVAL) * 1000, True)

	def _error(self):
		self.setNextCheck(isRetry=True)

	def _result(self, info):
		if not info:
			return
		if info["version"] == state["dontRemindVersion"]:
			return
		wx.CallAfter(UpdateResultDialog, gui.mainFrame, info, True)

class UpdateResultDialog(wx.Dialog):

	def __init__(self, parent, updateInfo, auto):
		# Translators: The title of the dialog informing the user about an NVDA update.
		super(UpdateResultDialog, self).__init__(parent, title=_("NVDA Update"))
		self.updateInfo = updateInfo
		self.isInstalled = config.isInstalledCopy()
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
			if self.isInstalled:
				# Translators: The label of a button to download and install an NVDA update.
				label = _("Download and &install update")
			else:
				# Translators: The label of a button to download an NVDA update.
				label = _("&Download update")
			item = wx.Button(self, label=label)
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
		self.Hide()
		DonateRequestDialog(gui.mainFrame, self._download)

	def _download(self):
		if self.isInstalled:
			UpdateDownloader((self.updateInfo["launcherUrl"],)).start()
		else:
			os.startfile(self.updateInfo["launcherUrl"])
		self.Destroy()

	def onLaterButton(self, evt):
		state["dontRemindVersion"] = None
		saveState()
		self.Close()

class UpdateDownloader(object):
	"""Download and start installation of an updated version of NVDA, presenting appropriate user interface.
	To use, call L{start} on an instance.
	"""

	def __init__(self, urls):
		"""Constructor.
		@param urls: URLs to try for the update file.
		@type urls: list of str
		"""
		self.urls = urls
		self.destPath = tempfile.mktemp(prefix="nvda_update_", suffix=".exe")

	def start(self):
		"""Start the download.
		"""
		# Translators: The title of the dialog displayed while downloading an NVDA update.
		self._progressDialog = wx.ProgressDialog(_("Downloading Update"),
			# Translators: The progress message indicating that a connection is being established.
			_("Connecting"),
			style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME, parent=gui.mainFrame)
		self._progressDialog.Raise()
		t = threading.Thread(target=self._bg)
		t.daemon = True
		t.start()

	def _bg(self):
		for url in self.urls:
			try:
				self._download(url)
			except:
				log.debugWarning("Error downloading %s" % url, exc_info=True)
			else:
				break
		else:
			# None of the URLs succeeded.
			wx.CallAfter(self._error)
			return
		wx.CallAfter(self._downloadSuccess)

	def _download(self, url):
		remote = urllib.urlopen(url)
		if remote.code != 200:
			raise RuntimeError("Download failed with code %d" % remote.code)
		size = int(remote.headers["content-length"])
		local = file(self.destPath, "wb")
		wx.CallAfter(self._downloadReport, 0, size)
		read = 0
		while True:
			block = remote.read(DOWNLOAD_BLOCK_SIZE)
			if not block:
				break
			read += len(block)
			local.write(block)
			wx.CallAfter(self._downloadReport, read, size)
		if read < size:
			raise RuntimeError("Content too short")
		wx.CallAfter(self._downloadReport, read, size)

	def _downloadReport(self, read, size):
		percent = int(float(read) / size * 100)
		# Translators: The progress message indicating that a download is in progress.
		self._progressDialog.Update(percent, _("Downloading"))

	def _error(self):
		self._progressDialog.Destroy()

	def _downloadSuccess(self):
		self._progressDialog.Destroy()
		# Translators: The message presented when the update has been successfully downloaded
		# and is about to be installed.
		gui.messageBox(_("Update downloaded. It will now be installed."),
			# Translators: The title of the dialog displayed when the update is about to be installed.
			_("Install Update"))
		state["removeFile"] = self.destPath
		saveState()
		shellapi.ShellExecute(None, None,
			self.destPath.decode("mbcs"),
			u"--install -m",
			None, 0)

class DonateRequestDialog(wx.Dialog):
	# Translators: The message requesting donations from users.
	MESSAGE = _(
		"We need your help in order to continue to improve NVDA.\n"
		"This project relies primarily on donations and grants. By donating, you are helping to fund full time development.\n"
		"If even $10 is donated for every download, we will be able to cover all of the ongoing costs of the project.\n"
		"All donations are received by NV Access, the non-profit organisation which develops NVDA.\n"
		"Thank you for your support."
	)

	def __init__(self, parent, continueFunc):
		# Translators: The title of the dialog requesting donations from users.
		super(DonateRequestDialog, self).__init__(parent, title=_("Please Donate"))
		self._continue = continueFunc

		mainSizer=wx.BoxSizer(wx.VERTICAL)
		item = wx.StaticText(self, label=self.MESSAGE)
		mainSizer.Add(item, border=20, flag=wx.LEFT | wx.RIGHT | wx.TOP)
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label of the button to donate.
		item = wx.Button(self, label=_("&Donate"))
		item.Bind(wx.EVT_BUTTON, lambda evt: os.startfile(gui.DONATE_URL))
		sizer.Add(item)
		item = wx.Button(self, wx.ID_CLOSE, label=_("&Close"))
		item.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
		sizer.Add(item)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.EscapeId = wx.ID_CLOSE
		mainSizer.Add(sizer, flag=wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, border=20)

		self.Sizer = mainSizer
		mainSizer.Fit(self)
		self.Show()

	def onClose(self, evt):
		self.Hide()
		self._continue()
		self.Destroy()

def saveState():
	try:
		cPickle.dump(state, file(_stateFilename, "wb"))
	except:
		log.debugWarning("Error saving state", exc_info=True)

def initialize():
	global state, _stateFilename, autoChecker
	_stateFilename = os.path.join(globalVars.appArgs.configPath, "updateCheckState.pickle")
	try:
		state = cPickle.load(file(_stateFilename, "r"))
	except:
		# Defaults.
		state = {
			"lastCheck": 0,
			"dontRemindVersion": None,
		}

	# If we just updated, remove the updater file.
	try:
		os.remove(state.pop("removeFile"))
		saveState()
	except (KeyError, OSError):
		pass

	if config.conf["update"]["autoCheck"]:
		autoChecker = AutoUpdateChecker()

def terminate():
	global state, autoChecker
	state = None
	autoChecker = None
