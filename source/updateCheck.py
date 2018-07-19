#updateCheck.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2012-2018 NV Access Limited, Zahari Yurukov, Babbage B.V.

"""Update checking functionality.
@note: This module may raise C{RuntimeError} on import if update checking for this build is not supported.
"""

import globalVars
import config
if globalVars.appArgs.secure:
	raise RuntimeError("updates disabled in secure mode")
elif config.isAppX:
	raise RuntimeError("updates managed by Windows Store") 
import versionInfo
if not versionInfo.updateVersionType:
	raise RuntimeError("No update version type, update checking not supported")

import winVersion
import os
import inspect
import threading
import time
import cPickle
import urllib
import tempfile
import hashlib
import ctypes.wintypes
import ssl
import wx
import languageHandler
import speech
import braille
import gui
from gui import guiHelper
from addonHandler import getCodeAddon, AddonError
from logHandler import log, isPathExternalToNVDA
import config
import shellapi
import winUser

#: The URL to use for update checks.
CHECK_URL = "https://www.nvaccess.org/nvdaUpdateCheck"
#: The time to wait between checks.
CHECK_INTERVAL = 86400 # 1 day
#: The time to wait before retrying a failed check.
RETRY_INTERVAL = 600 # 10 min
#: The download block size in bytes.
DOWNLOAD_BLOCK_SIZE = 8192 # 8 kb

#: directory to store pending update files
storeUpdatesDir=os.path.join(globalVars.appArgs.configPath, 'updates')
try:
	os.makedirs(storeUpdatesDir)
except OSError:
	if not os.path.isdir(storeUpdatesDir):
		log.debugWarning("Default download path for updates %s could not be created."%storeUpdatesDir)

#: Persistent state information.
#: @type: dict
state = None
_stateFileName = None
#: The single instance of L{AutoUpdateChecker} if automatic update checking is enabled,
#: C{None} if it is disabled.
autoChecker = None

def getQualifiedDriverClassNameForStats(cls):
	""" fetches the name from a given synthDriver or brailleDisplay class, and appends core for in-built code, the add-on name for code from an add-on, or external for code in the NVDA user profile.
	Some examples:
	espeak (core)
	newfon (external)
	eloquence (addon:CodeFactory)
	noBraille (core)
	"""
	name=cls.name
	try:
		addon=getCodeAddon(cls)
	except AddonError:
		addon=None
	if addon:
		return "%s (addon:%s)"%(name,addon.name)
	path=inspect.getsourcefile(cls)
	if isPathExternalToNVDA(path):
		return "%s (external)"%name
	return "%s (core)"%name

def checkForUpdate(auto=False):
	"""Check for an updated version of NVDA.
	This will block, so it generally shouldn't be called from the main thread.
	@param auto: Whether this is an automatic check for updates.
	@type auto: bool
	@return: Information about the update or C{None} if there is no update.
	@rtype: dict
	@raise RuntimeError: If there is an error checking for an update.
	"""
	allowUsageStats=config.conf["update"]['allowUsageStats']
	params = {
		"autoCheck": auto,
		"allowUsageStats":allowUsageStats,
		"version": versionInfo.version,
		"versionType": versionInfo.updateVersionType,
		"osVersion": winVersion.winVersionText,
		"x64": os.environ.get("PROCESSOR_ARCHITEW6432") == "AMD64",
	}
	if auto and allowUsageStats:
		synthDriverClass=speech.getSynth().__class__
		brailleDisplayClass=braille.handler.display.__class__ if braille.handler else None
		# Following are parameters sent purely for stats gathering.
		#  If new parameters are added here, they must be documented in the userGuide for transparency.
		extraParams={
			"language": languageHandler.getLanguage(),
			"installed": config.isInstalledCopy(),
			"synthDriver":getQualifiedDriverClassNameForStats(synthDriverClass) if synthDriverClass else None,
			"brailleDisplay":getQualifiedDriverClassNameForStats(brailleDisplayClass) if brailleDisplayClass else None,
			"outputBrailleTable":config.conf['braille']['translationTable'] if brailleDisplayClass else None,
		}
		params.update(extraParams)
	url = "%s?%s" % (CHECK_URL, urllib.urlencode(params))
	try:
		res = urllib.urlopen(url)
	except IOError as e:
		if isinstance(e.strerror, ssl.SSLError) and e.strerror.reason == "CERTIFICATE_VERIFY_FAILED":
			# #4803: Windows fetches trusted root certificates on demand.
			# Python doesn't trigger this fetch (PythonIssue:20916), so try it ourselves
			_updateWindowsRootCertificates()
			# and then retry the update check.
			res = urllib.urlopen(url)
		else:
			raise
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

def getPendingUpdate():
	"""Returns the path to the pending update, if any. Returns C{None} otherwise.
	@rtype: str
	"""
	try:
		pendingUpdateFile=state["pendingUpdateFile"]
	except KeyError:
		state["pendingUpdateFile"] = state["pendingUpdateVersion"] = None
		return None
	else:
		if pendingUpdateFile and os.path.isfile(pendingUpdateFile):
			return pendingUpdateFile
		else:
			state["pendingUpdateFile"] = None
	return None

def isPendingUpdate():
	"""Returns whether there is a pending update.
	@rtype: bool
	"""
	return bool(getPendingUpdate())

def executeUpdate(destPath=None):
	if not destPath:
		destPath=getPendingUpdate()
	if not destPath:
		return
	state["pendingUpdateFile"]=None
	state["pendingUpdateVersion"]=None
	saveState()
	if config.isInstalledCopy():
		executeParams = u"--install -m"
	else:
		portablePath = os.getcwdu()
		if os.access(portablePath, os.W_OK):
			executeParams = u'--create-portable --portable-path "{portablePath}" --config-path "{configPath}" -m'.format(
				portablePath=portablePath,
				configPath=os.path.abspath(globalVars.appArgs.configPath)
			)
		else:
			executeParams = u"--launcher"
	# #4475: ensure that the new process shows its first window, by providing SW_SHOWNORMAL
	shellapi.ShellExecute(None, None,
		destPath.decode("mbcs"),
		executeParams,
		None, winUser.SW_SHOWNORMAL)

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
		self._started()
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

	def _started(self):
		self._progressDialog = gui.IndeterminateProgressDialog(gui.mainFrame,
			# Translators: The title of the dialog displayed while manually checking for an NVDA update.
			_("Checking for Update"),
			# Translators: The progress message displayed while manually checking for an NVDA update.
			_("Checking for update"))

	def _error(self):
		wx.CallAfter(self._progressDialog.done)
		self._progressDialog = None
		wx.CallAfter(gui.messageBox,
			# Translators: A message indicating that an error occurred while checking for an update to NVDA.
			_("Error checking for update."),
			# Translators: The title of an error message dialog.
			_("Error"),
			wx.OK | wx.ICON_ERROR)

	def _result(self, info):
		wx.CallAfter(self._progressDialog.done)
		self._progressDialog = None
		wx.CallAfter(UpdateResultDialog, gui.mainFrame, info, False)

class AutoUpdateChecker(UpdateChecker):
	"""Automatically check for an updated version of NVDA.
	To use, create a single instance and maintain a reference to it.
	Checks will then be performed automatically.
	"""
	AUTO = True

	def __init__(self):
		self._checkTimer = gui.NonReEntrantTimer(self.check)
		if config.conf["update"]["startupNotification"] and isPendingUpdate():
			secsTillNext = 0 # Display the update message instantly
		else:
			# Set the initial check based on the last check time.
			# #3260: If the system time is earlier than the last check,
			# treat the last check as being right now (so the next will be tomorrow).
			secsSinceLast = max(time.time() - state["lastCheck"], 0)
			# The maximum time till the next check is CHECK_INTERVAL.
			secsTillNext = CHECK_INTERVAL - int(min(secsSinceLast, CHECK_INTERVAL))
		self._checkTimer.Start(secsTillNext * 1000, True)

	def terminate(self):
		self._checkTimer.Stop()
		self._checkTimer = None

	def setNextCheck(self, isRetry=False):
		# #6127: Timers must be manipulated from the main thread.
		wx.CallAfter(self._checkTimer.Stop)
		wx.CallAfter(self._checkTimer.Start, (RETRY_INTERVAL if isRetry else CHECK_INTERVAL) * 1000, True)

	def _started(self):
		log.info("Performing automatic update check")

	def _error(self):
		self.setNextCheck(isRetry=True)

	def _result(self, info):
		if not info:
			return
		if info["version"]==state["dontRemindVersion"]:
			return
		wx.CallAfter(UpdateResultDialog, gui.mainFrame, info, True)

class UpdateResultDialog(wx.Dialog):

	def __init__(self, parent, updateInfo, auto):
		# Translators: The title of the dialog informing the user about an NVDA update.
		super(UpdateResultDialog, self).__init__(parent, title=_("NVDA Update"))
		self.updateInfo = updateInfo
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)

		if updateInfo:
			self.isInstalled = config.isInstalledCopy()
			if isPendingUpdate() and state["pendingUpdateVersion"] == updateInfo["version"]:
				# Translators: A message indicating that an updated version of NVDA has been downloaded
				# and is pending to be installed.
				message = _("NVDA version {version} has been downloaded and is pending installation.").format(**updateInfo)
			else:
				# Translators: A message indicating that an updated version of NVDA is available.
				# {version} will be replaced with the version; e.g. 2011.3.
				message = _("NVDA version {version} is available.").format(**updateInfo)
		else:
			# Translators: A message indicating that no update to NVDA is available.
			message = _("No update available.")
		sHelper.addItem(wx.StaticText(self, label=message))

		bHelper = sHelper.addDialogDismissButtons(guiHelper.ButtonHelper(wx.HORIZONTAL))
		if updateInfo:
			if isPendingUpdate() and state["pendingUpdateVersion"] == updateInfo["version"]:
				# Translators: The label of a button to install a pending NVDA update.
				# {version} will be replaced with the version; e.g. 2011.3.
				installPendingButton = bHelper.addButton(self, label=_("&Install NVDA {version}").format(**updateInfo))
				installPendingButton.Bind(wx.EVT_BUTTON, self.onInstallButton)
				# Translators: The label of a button to re-download a pending NVDA update.
				label = _("Re-&download update")
			else:
				# Translators: The label of a button to download an NVDA update.
				label = _("&Download update")
			downloadButton = bHelper.addButton(self, label=label)
			downloadButton.Bind(wx.EVT_BUTTON, self.onDownloadButton)

			if auto and (not isPendingUpdate() or state["pendingUpdateVersion"] != updateInfo["version"]):
				# Translators: The label of a button to remind the user later about performing some action.
				remindMeButton = bHelper.addButton(self, label=_("Remind me &later"))
				remindMeButton.Bind(wx.EVT_BUTTON, self.onLaterButton)
				remindMeButton.SetFocus()

		# Translators: The label of a button to close a dialog.
		closeButton = bHelper.addButton(self, wx.ID_CLOSE, label=_("&Close"))
		closeButton.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
		self.Bind(wx.EVT_CLOSE, lambda evt: self.Destroy())
		self.EscapeId = wx.ID_CLOSE

		mainSizer.Add(sHelper.sizer, border=guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		self.Sizer = mainSizer
		mainSizer.Fit(self)
		self.CentreOnScreen()
		self.Show()

	def onInstallButton(self, evt):
		executeUpdate()
		self.Destroy()

	def onDownloadButton(self, evt):
		self.Hide()
		DonateRequestDialog(gui.mainFrame, self._download)

	def _download(self):
		UpdateDownloader(self.updateInfo).start()
		self.Destroy()

	def onLaterButton(self, evt):
		state["dontRemindVersion"] = None
		saveState()
		self.Close()

class UpdateAskInstallDialog(wx.Dialog):

	def __init__(self, parent, destPath, version):
		self.destPath=destPath
		self.version = version
		storeUpdatesDirWritable=os.path.isdir(storeUpdatesDir) and os.access(storeUpdatesDir, os.W_OK)
		# Translators: The title of the dialog asking the user to Install an NVDA update.
		super(UpdateAskInstallDialog, self).__init__(parent, title=_("NVDA Update"))
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)
		
		# Translators: A message indicating that an updated version of NVDA is ready to be installed.
		sHelper.addItem(wx.StaticText(self, label=_("NVDA version {version} is ready to be installed.\n").format(version=version)))

		bHelper = sHelper.addDialogDismissButtons(guiHelper.ButtonHelper(wx.HORIZONTAL))
		# Translators: The label of a button to install an NVDA update.
		installButton = bHelper.addButton(self, wx.ID_OK, label=_("&Install update"))
		installButton.Bind(wx.EVT_BUTTON, self.onInstallButton)
		installButton.SetFocus()
		if storeUpdatesDirWritable:
			# Translators: The label of a button to postpone an NVDA update.
			postponeButton = bHelper.addButton(self, wx.ID_CLOSE, label=_("&Postpone update"))
			postponeButton.Bind(wx.EVT_BUTTON, self.onPostponeButton)

			self.EscapeId = wx.ID_CLOSE
		else:
			self.EscapeId = wx.ID_OK

		mainSizer.Add(sHelper.sizer, border=guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		self.Sizer = mainSizer
		mainSizer.Fit(self)
		self.CentreOnScreen()

	def onInstallButton(self, evt):
		executeUpdate(self.destPath)
		self.EndModal(wx.ID_OK)

	def onPostponeButton(self, evt):
		finalDest=os.path.join(storeUpdatesDir, os.path.basename(self.destPath))
		try:
			os.renames(self.destPath, finalDest)
		except:
			gui.messageBox(
				# Translators: The message when a downloaded update file could not be preserved.
				_("Unable to postpone update."),
				# Translators: The title of the message when a downloaded update file could not be preserved.
				_("Error"),
				wx.OK | wx.ICON_ERROR)
			finalDest=self.destPath
		state["pendingUpdateFile"]=finalDest
		state["pendingUpdateVersion"]=self.version
		# Postponing an update indicates that the user is likely interested in getting a reminder.
		# Therefore, clear the dontRemindVersion.
		state["dontRemindVersion"] = None
		saveState()		
		self.EndModal(wx.ID_CLOSE)

class UpdateDownloader(object):
	"""Download and start installation of an updated version of NVDA, presenting appropriate user interface.
	To use, call L{start} on an instance.
	"""

	def __init__(self, updateInfo):
		"""Constructor.
		@param updateInfo: update information such as possible URLs, version and the SHA-1 hash of the file as a hex string.
		@type updateInfo: dict
		"""
		self.updateInfo = updateInfo
		self.urls = updateInfo["launcherUrl"].split(" ")
		self.version = updateInfo["version"]
		self.fileHash = updateInfo.get("launcherHash")
		self.destPath = tempfile.mktemp(prefix="nvda_update_", suffix=".exe")

	def start(self):
		"""Start the download.
		"""
		self._shouldCancel = False
		# Use a timer because timers aren't re-entrant.
		self._guiExecTimer = gui.NonReEntrantTimer(self._guiExecNotify)
		gui.mainFrame.prePopup()
		# Translators: The title of the dialog displayed while downloading an NVDA update.
		self._progressDialog = wx.ProgressDialog(_("Downloading Update"),
			# Translators: The progress message indicating that a connection is being established.
			_("Connecting"),
			# PD_AUTO_HIDE is required because ProgressDialog.Update blocks at 100%
			# and waits for the user to press the Close button.
			style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_AUTO_HIDE,
			parent=gui.mainFrame)
		self._progressDialog.Raise()
		t = threading.Thread(target=self._bg)
		t.daemon = True
		t.start()

	def _guiExec(self, func, *args):
		self._guiExecFunc = func
		self._guiExecArgs = args
		if not self._guiExecTimer.IsRunning():
			# #6127: Timers must be manipulated from the main thread.
			wx.CallAfter(self._guiExecTimer.Start, 50, True)

	def _guiExecNotify(self):
		self._guiExecFunc(*self._guiExecArgs)

	def _bg(self):
		success=False
		for url in self.urls:
			try:
				self._download(url)
			except:
				log.debugWarning("Error downloading %s" % url, exc_info=True)
			else: #Successfully downloaded or canceled
				if not self._shouldCancel:
					success=True
				break
		else:
			# None of the URLs succeeded.
			self._guiExec(self._error)
			return
		if not success:
			try:
				os.remove(self.destPath)
			except OSError:
				pass
			return
		self._guiExec(self._downloadSuccess)

	def _download(self, url):
		remote = urllib.urlopen(url)
		if remote.code != 200:
			raise RuntimeError("Download failed with code %d" % remote.code)
		# #2352: Some security scanners such as Eset NOD32 HTTP Scanner
		# cause huge read delays while downloading.
		# Therefore, set a higher timeout.
		remote.fp._sock.settimeout(120)
		size = int(remote.headers["content-length"])
		local = file(self.destPath, "wb")
		if self.fileHash:
			hasher = hashlib.sha1()
		self._guiExec(self._downloadReport, 0, size)
		read = 0
		chunk=DOWNLOAD_BLOCK_SIZE
		while True:
			if self._shouldCancel:
				return
			if size -read <chunk:
				chunk =size -read
			block = remote.read(chunk)
			if not block:
				break
			read += len(block)
			if self._shouldCancel:
				return
			local.write(block)
			if self.fileHash:
				hasher.update(block)
			self._guiExec(self._downloadReport, read, size)
		if read < size:
			raise RuntimeError("Content too short")
		if self.fileHash and hasher.hexdigest() != self.fileHash:
			raise RuntimeError("Content has incorrect file hash")
		self._guiExec(self._downloadReport, read, size)

	def _downloadReport(self, read, size):
		if self._shouldCancel:
			return
		percent = int(float(read) / size * 100)
		# Translators: The progress message indicating that a download is in progress.
		cont, skip = self._progressDialog.Update(percent, _("Downloading"))
		if not cont:
			self._shouldCancel = True
			self._stopped()

	def _stopped(self):
		self._guiExecTimer = None
		self._guiExecFunc = None
		self._guiExecArgs = None
		self._progressDialog.Hide()
		self._progressDialog.Destroy()
		self._progressDialog = None
		# Not sure why, but this doesn't work if we call it directly here.
		wx.CallLater(50, gui.mainFrame.postPopup)

	def _error(self):
		self._stopped()
		gui.messageBox(
			# Translators: A message indicating that an error occurred while downloading an update to NVDA.
			_("Error downloading update."),
			_("Error"),
			wx.OK | wx.ICON_ERROR)

	def _downloadSuccess(self):
		self._stopped()
		gui.runScriptModalDialog(UpdateAskInstallDialog(gui.mainFrame, self.destPath, self.version))

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
		# Translators: The label of the button to donate
		# in the "Please Donate" dialog.
		item = self.donateButton = wx.Button(self, label=_("&Donate"))
		item.Bind(wx.EVT_BUTTON, self.onDonate)
		sizer.Add(item)
		# Translators: The label of the button to decline donation
		# in the "Please Donate" dialog.
		item = wx.Button(self, wx.ID_CLOSE, label=_("&Not now"))
		item.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
		sizer.Add(item)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.EscapeId = wx.ID_CLOSE
		mainSizer.Add(sizer, flag=wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, border=20)

		self.Sizer = mainSizer
		mainSizer.Fit(self)
		self.CentreOnScreen()
		self.Show()

	def onDonate(self, evt):
		os.startfile(gui.DONATE_URL)
		# Translators: The label of a button to indicate that the user is finished donating
		# in the "Please Donate" dialog.
		self.donateButton.Label = _("&Done")
		self.donateButton.Bind(wx.EVT_BUTTON, lambda evt: self.Close())

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
		log.debugWarning("Couldn't retrieve update state", exc_info=True)
		# Defaults.
		state = {
			"lastCheck": 0,
			"dontRemindVersion": None,
			"pendingUpdateVersion": None,
			"pendingUpdateFile": None,
		}

	# check the pending version against the current version
	# and make sure that pendingUpdateFile and pendingUpdateVersion are part of the state dictionary.
	if "pendingUpdateVersion" not in state or state["pendingUpdateVersion"] == versionInfo.version:
		state["pendingUpdateFile"] = state["pendingUpdateVersion"] = None
	# remove all update files except the one that is currently pending (if any)
	try:
		for fileName in os.listdir(storeUpdatesDir):
			f=os.path.join(storeUpdatesDir, fileName)
			if f != state["pendingUpdateFile"]:
				os.remove(f)
				log.debug("Update file %s removed"%f)
	except OSError:
		log.warning("Unable to remove old update file %s"%f, exc_info=True)

	if not globalVars.appArgs.launcher and (config.conf["update"]["autoCheck"] or (config.conf["update"]["startupNotification"] and isPendingUpdate())):
		autoChecker = AutoUpdateChecker()

def terminate():
	global state, autoChecker
	state = None
	if autoChecker:
		autoChecker.terminate()
		autoChecker = None

# These structs are only complete enough to achieve what we need.
class CERT_USAGE_MATCH(ctypes.Structure):
	_fields_ = (
		("dwType", ctypes.wintypes.DWORD),
		# CERT_ENHKEY_USAGE struct
		("cUsageIdentifier", ctypes.wintypes.DWORD),
		("rgpszUsageIdentifier", ctypes.c_void_p), # LPSTR *
	)

class CERT_CHAIN_PARA(ctypes.Structure):
	_fields_ = (
		("cbSize", ctypes.wintypes.DWORD),
		("RequestedUsage", CERT_USAGE_MATCH),
		("RequestedIssuancePolicy", CERT_USAGE_MATCH),
		("dwUrlRetrievalTimeout", ctypes.wintypes.DWORD),
		("fCheckRevocationFreshnessTime", ctypes.wintypes.BOOL),
		("dwRevocationFreshnessTime", ctypes.wintypes.DWORD),
		("pftCacheResync", ctypes.c_void_p), # LPFILETIME
		("pStrongSignPara", ctypes.c_void_p), # PCCERT_STRONG_SIGN_PARA
		("dwStrongSignFlags", ctypes.wintypes.DWORD),
	)

def _updateWindowsRootCertificates():
	crypt = ctypes.windll.crypt32
	# Get the server certificate.
	sslCont = ssl._create_unverified_context()
	u = urllib.urlopen("https://www.nvaccess.org/nvdaUpdateCheck", context=sslCont)
	cert = u.fp._sock.getpeercert(True)
	u.close()
	# Convert to a form usable by Windows.
	certCont = crypt.CertCreateCertificateContext(
		0x00000001, # X509_ASN_ENCODING
		cert,
		len(cert))
	# Ask Windows to build a certificate chain, thus triggering a root certificate update.
	chainCont = ctypes.c_void_p()
	crypt.CertGetCertificateChain(None, certCont, None, None,
		ctypes.byref(CERT_CHAIN_PARA(cbSize=ctypes.sizeof(CERT_CHAIN_PARA),
			RequestedUsage=CERT_USAGE_MATCH())),
		0, None,
		ctypes.byref(chainCont))
	crypt.CertFreeCertificateChain(chainCont)
	crypt.CertFreeCertificateContext(certCont)
