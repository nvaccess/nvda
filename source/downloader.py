#downloader.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2013 NV Access Limited

"""Utilities for downloading files.
"""

import tempfile
import urllib
import threading
import wx
import gui
from logHandler import log

#: The download block size in bytes.
DOWNLOAD_BLOCK_SIZE = 8192 # 8 kb

class FileDownloader(object):
	"""Download a file, presenting an appropriate user interface.
	The file will be downloaded to a temporary location.
	This class must be subclassed; it cannot be used directly.
	Subclasses must provide L{progressTitle} and L{errorMessage}.
	They will almost certainly want to override L{onSuccess}.
	Once a subclass is instantiated, L{start} should be called to begin the download.
	"""

	#: The suffix for the destination file path.
	#: @type: str
	destSuffix = ""
	#: The title of the download progress dialog.
	#: @type: basestring
	progressTitle = None
	#: The message displayed when the download failed.
	#: @type: basestring
	errorMessage = None

	def __init__(self, urls, parent=None):
		"""Constructor.
		@param urls: URLs to try for the file.
		@type urls: list of str
		@param parent: The parent window for any dialogs.
		@type parent: C{wx.Window}
		"""
		self.urls = urls
		if not parent:
			parent = gui.mainFrame
		self.parent = parent
		#: The path to the downloaded file.
		self.destPath = tempfile.mktemp(prefix="nvda_dl_", suffix=self.destSuffix)

	def start(self):
		"""Start the download.
		"""
		self._shouldCancel = False
		# Use a timer because timers aren't re-entrant.
		self._guiExecTimer = wx.PyTimer(self._guiExecNotify)
		if self.parent is gui.mainFrame:
			gui.mainFrame.prePopup()
		self._progressDialog = wx.ProgressDialog(self.progressTitle,
			# Translators: The progress message indicating that a connection is being established.
			_("Connecting"),
			# PD_AUTO_HIDE is required because ProgressDialog.Update blocks at 100%
			# and waits for the user to press the Close button.
			style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_AUTO_HIDE,
			parent=self.parent)
		self._progressDialog.Raise()
		t = threading.Thread(target=self._bg)
		t.daemon = True
		t.start()

	def _guiExec(self, func, *args):
		self._guiExecFunc = func
		self._guiExecArgs = args
		if not self._guiExecTimer.IsRunning():
			self._guiExecTimer.Start(50, True)

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
			self._guiExec(self._stopped, self.onError)
			return
		if not success:
			try:
				os.remove(self.destPath)
			except OSError:
				pass
			return
		self._guiExec(self._stopped, self.onSuccess)

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
			self._guiExec(self._downloadReport, read, size)
		if read < size:
			raise RuntimeError("Content too short")
		self._guiExec(self._downloadReport, read, size)

	def _downloadReport(self, read, size):
		if self._shouldCancel:
			return
		percent = int(float(read) / size * 100)
		# Translators: The progress message indicating that a download is in progress.
		cont, skip = self._progressDialog.Update(percent, _("Downloading"))
		if not cont:
			self._shouldCancel = True
			self._stopped(self.onCancel)

	def _stopped(self, notifyFunc):
		self._guiExecTimer = None
		self._guiExecFunc = None
		self._guiExecArgs = None
		self._progressDialog.Hide()
		self._progressDialog.Destroy()
		self._progressDialog = None
		if self.parent is gui.mainFrame:
			# Not sure why, but this doesn't work if we call it directly here.
			wx.CallLater(50, gui.mainFrame.postPopup)
		notifyFunc()

	def onError(self):
		"""Called when the download fails.
		Subclasses may override or extend this.
		"""
		gui.messageBox(
			self.errorMessage,
			_("Error"),
			wx.OK | wx.ICON_ERROR, self.parent)

	def onSuccess(self):
		"""Called when the download is successful.
		The base implementation does nothing.
		Subclasses will almost certainly want to override this.
		"""

	def onCancel(self):
		"""Called when the download is cancelled by the user.
		The base implementation does nothing.
		Subclasses may override this.
		Note that the incomplete destination file is deleted separately.
		"""
