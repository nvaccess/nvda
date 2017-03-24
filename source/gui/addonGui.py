#gui/addonGui.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2012-2017 NV Access Limited, Beqa Gozalishvili, Joseph Lee, Babbage B.V.

"""Add-ons Manager user interface
The Add-ons Manager allows add-ons to be installed, removed, enabled, disabled and perform other tasks.
It also allows add-ons to provide a button to read add-on help files.
"""

import os
import threading
import tempfile
import wx
import core
import languageHandler
import gui
import guiHelper
from logHandler import log
import addonHandler
import globalVars
import queueHandler
import updateCheck

class AddonsDialog(wx.Dialog):
	_instance = None
	def __new__(cls, *args, **kwargs):
		if AddonsDialog._instance is None:
			return super(AddonsDialog, cls).__new__(cls, *args, **kwargs)
		return AddonsDialog._instance

	def __init__(self,parent):
		if AddonsDialog._instance is not None:
			return
		AddonsDialog._instance = self
		# Translators: The title of the Addons Dialog
		super(AddonsDialog,self).__init__(parent,title=_("Add-ons Manager"))
		mainSizer=wx.BoxSizer(wx.VERTICAL)
		settingsSizer=wx.BoxSizer(wx.VERTICAL)
		entriesSizer=wx.BoxSizer(wx.VERTICAL)
		if globalVars.appArgs.disableAddons:
			# Translators: A message in the add-ons manager shown when all add-ons are disabled.
			addonsDisabledLabel=wx.StaticText(self,-1,label=_("All add-ons are currently disabled. To enable add-ons you must restart NVDA."))
			mainSizer.Add(addonsDisabledLabel)
		# Translators: the label for the installed addons list in the addons manager.
		entriesLabel=wx.StaticText(self,-1,label=_("Installed Add-ons"))
		entriesSizer.Add(entriesLabel)
		self.addonsList=wx.ListCtrl(self,-1,style=wx.LC_REPORT|wx.LC_SINGLE_SEL,size=(550,350))
		# Translators: The label for a column in add-ons list used to identify add-on package name (example: package is OCR).
		self.addonsList.InsertColumn(0,_("Package"),width=150)
		# Translators: The label for a column in add-ons list used to identify add-on's running status (example: status is running).
		self.addonsList.InsertColumn(1,_("Status"),width=50)
		# Translators: The label for a column in add-ons list used to identify add-on's version (example: version is 0.3).
		self.addonsList.InsertColumn(2,_("Version"),width=50)
		# Translators: The label for a column in add-ons list used to identify add-on's author (example: author is NV Access).
		self.addonsList.InsertColumn(3,_("Author"),width=300)
		self.addonsList.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.onListItemSelected)
		entriesSizer.Add(self.addonsList,proportion=8)
		settingsSizer.Add(entriesSizer)
		entryButtonsSizer=wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label for a button in Add-ons Manager dialog to show information about the selected add-on.
		self.aboutButton=wx.Button(self,label=_("&About add-on..."))
		self.aboutButton.Disable()
		self.aboutButton.Bind(wx.EVT_BUTTON,self.onAbout)
		entryButtonsSizer.Add(self.aboutButton)
		# Translators: The label for a button in Add-ons Manager dialog to show the help for the selected add-on.
		self.helpButton=wx.Button(self,label=_("Add-on &help"))
		self.helpButton.Disable()
		self.helpButton.Bind(wx.EVT_BUTTON,self.onHelp)
		entryButtonsSizer.Add(self.helpButton)
		# Translators: The label for a button in Add-ons Manager dialog to enable or disable the selected add-on.
		self.enableDisableButton=wx.Button(self,label=_("&Disable add-on"))
		self.enableDisableButton.Disable()
		self.enableDisableButton.Bind(wx.EVT_BUTTON,self.onEnableDisable)
		entryButtonsSizer.Add(self.enableDisableButton)
		# Translators: The label for a button in Add-ons Manager dialog to check for updated versions of installed add-ons.
		self.updateCheckButton=wx.Button(self,label=_("Check for add-on &updates..."))
		self.updateCheckButton.Disable()
		self.updateCheckButton.Bind(wx.EVT_BUTTON,self.onAddonUpdateCheck)
		entryButtonsSizer.Add(self.updateCheckButton)
		# Translators: The label for a button in Add-ons Manager dialog to install an add-on.
		self.addButton=wx.Button(self,label=_("&Install..."))
		self.addButton.Bind(wx.EVT_BUTTON,self.onAddClick)
		entryButtonsSizer.Add(self.addButton)
		# Translators: The label for a button to remove either:
		# Remove the selected add-on in Add-ons Manager dialog.
		# Remove a speech dictionary entry.
		self.removeButton=wx.Button(self,label=_("&Remove"))
		self.removeButton.Disable()
		self.removeButton.Bind(wx.EVT_BUTTON,self.onRemoveClick)
		entryButtonsSizer.Add(self.removeButton)
		# Translators: The label of a button in Add-ons Manager to open the Add-ons website and get more add-ons.
		self.getAddonsButton=wx.Button(self,label=_("&Get add-ons..."))
		self.getAddonsButton.Bind(wx.EVT_BUTTON,self.onGetAddonsClick)
		entryButtonsSizer.Add(self.getAddonsButton)
		settingsSizer.Add(entryButtonsSizer)
		mainSizer.Add(settingsSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)
		# Translators: The label of a button to close the Addons dialog.
		closeButton = wx.Button(self, label=_("&Close"), id=wx.ID_CLOSE)
		closeButton.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
		mainSizer.Add(closeButton,border=20,flag=wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.CENTER|wx.ALIGN_RIGHT)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.EscapeId = wx.ID_CLOSE
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.refreshAddonsList()
		self.addonsList.SetFocus()
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)

	def onAddClick(self,evt):
		# Translators: The message displayed in the dialog that allows you to choose an add-on package for installation.
		fd=wx.FileDialog(self,message=_("Choose Add-on Package File"),
		# Translators: the label for the NVDA add-on package file type in the Choose add-on dialog.
		wildcard=(_("NVDA Add-on Package (*.{ext})")+"|*.{ext}").format(ext=addonHandler.BUNDLE_EXTENSION),
		defaultDir="c:",style=wx.FD_OPEN)
		if fd.ShowModal()!=wx.ID_OK:
			return
		addonPath=fd.GetPath()
		self.installAddon(addonPath)

	def installAddon(self, addonPath, closeAfter=False):
		try:
			try:
				bundle=addonHandler.AddonBundle(addonPath)
			except:
				log.error("Error opening addon bundle from %s"%addonPath,exc_info=True)
				# Translators: The message displayed when an error occurs when opening an add-on package for adding. 
				gui.messageBox(_("Failed to open add-on package file at %s - missing file or invalid file format")%addonPath,
					# Translators: The title of a dialog presented when an error occurs.
					_("Error"),
					wx.OK | wx.ICON_ERROR)
				return
			# Translators: A message asking the user if they really wish to install an addon.
			if gui.messageBox(_("Are you sure you want to install this add-on? Only install add-ons from trusted sources.\nAddon: {summary} {version}\nAuthor: {author}").format(**bundle.manifest),
				# Translators: Title for message asking if the user really wishes to install an Addon.
				_("Add-on Installation"),
				wx.YES|wx.NO|wx.ICON_WARNING)!=wx.YES:
				return
			bundleName=bundle.manifest['name']
			prevAddon=None
			for addon in self.curAddons:
				if not addon.isPendingRemove and bundleName==addon.manifest['name']:
					prevAddon=addon
					break
			if prevAddon:
				# Translators: A message asking if the user wishes to update a previously installed add-on with this one.
				if gui.messageBox(_("A version of this add-on is already installed. Would you like to update it?"),
				# Translators: A title for the dialog  asking if the user wishes to update a previously installed add-on with this one.
				_("Add-on Installation"),
				wx.YES|wx.NO|wx.ICON_WARNING)!=wx.YES:
					return
				prevAddon.requestRemove()
			self._progressDialog = gui.IndeterminateProgressDialog(gui.mainFrame,
			# Translators: The title of the dialog presented while an Addon is being installed.
			_("Installing Add-on"),
			# Translators: The message displayed while an addon is being installed.
			_("Please wait while the add-on is being installed."))
			try:
				gui.ExecAndPump(addonHandler.installAddonBundle,bundle)
			except:
				log.error("Error installing  addon bundle from %s"%addonPath,exc_info=True)
				self.refreshAddonsList()
				self._progressDialog.done()
				self._progressDialog = None
				# Translators: The message displayed when an error occurs when installing an add-on package.
				gui.messageBox(_("Failed to install add-on  from %s")%addonPath,
					# Translators: The title of a dialog presented when an error occurs.
					_("Error"),
					wx.OK | wx.ICON_ERROR)
				return
			else:
				self.refreshAddonsList(activeIndex=-1)
				self._progressDialog.done()
				self._progressDialog = None
		finally:
			if closeAfter:
				# #4460: If we do this immediately, wx seems to drop the WM_QUIT sent if the user chooses to restart.
				# This seems to have something to do with the wx.ProgressDialog.
				# The CallLater seems to work around this.
				wx.CallLater(1, self.Close)

	def onRemoveClick(self,evt):
		index=self.addonsList.GetFirstSelected()
		if index<0: return
		# Translators: Presented when attempting to remove the selected add-on.
		if gui.messageBox(_("Are you sure you wish to remove the selected add-on from NVDA?"),
			# Translators: Title for message asking if the user really wishes to remove the selected Addon.
			_("Remove Add-on"), wx.YES_NO|wx.ICON_WARNING) != wx.YES: return
		addon=self.curAddons[index]
		addon.requestRemove()
		self.refreshAddonsList(activeIndex=index)
		self.addonsList.SetFocus()

	def onAddonUpdateCheck(self,evt):
		# Hide Add-ons Manager window, otherwise the update result dialog will not be shown.
		self.Hide()
		self._progressDialog = gui.IndeterminateProgressDialog(gui.mainFrame,
		# Translators: The title of the dialog presented while checking for add-on updates.
		_("Add-on update check"),
		# Translators: The message displayed while checking for add-on updates.
		_("Checking for add-on updates..."))
		t = threading.Thread(target=self.addonUpdateCheck)
		t.daemon = True
		t.start()

	def addonUpdateCheck(self):
		info = addonHandler.checkForAddonUpdates()
		wx.CallAfter(self._progressDialog.done)
		self._progressDialog = None
		wx.CallAfter(AddonUpdatesDialog, self, info, auto=False)

	def getAddonStatus(self,addon):
		if addon.isPendingInstall:
			# Translators: The status shown for a newly installed addon before NVDA is restarted.
			return _("install")
		elif addon.isPendingRemove:
			# Translators: The status shown for an addon that has been marked as removed, before NVDA has been restarted.
			return _("remove")
		# Need to do this here, as 'isDisabled' overrides other flags.
		elif addon.isPendingDisable:
			# Translators: The status shown for an addon when its disabled.
			return _("disable")
		elif addon.isPendingEnable:
			# Translators: The status shown for an addon when its enabled.
			return _("enable")
		elif globalVars.appArgs.disableAddons or addon.isDisabled:
			# Translators: The status shown for an addon when its currently suspended do to addons being disabled.
			return _("suspended")
		else:
			# Translators: The status shown for an addon when its currently running in NVDA.
			return _("running")

	def refreshAddonsList(self,activeIndex=0):
		self.addonsList.DeleteAllItems()
		self.curAddons=[]
		for addon in addonHandler.getAvailableAddons():
			self.addonsList.Append((addon.manifest['summary'], self.getAddonStatus(addon), addon.manifest['version'], addon.manifest['author']))
			self.curAddons.append(addon)
		# select the given active addon or the first addon if not given
		curAddonsLen=len(self.curAddons)
		if curAddonsLen>0:
			if activeIndex==-1:
				activeIndex=curAddonsLen-1
			elif activeIndex<0 or activeIndex>=curAddonsLen:
				activeIndex=0
			self.addonsList.Select(activeIndex,on=1)
			self.addonsList.SetItemState(activeIndex,wx.LIST_STATE_FOCUSED,wx.LIST_STATE_FOCUSED)
		else:
			self.aboutButton.Disable()
			self.helpButton.Disable()
			self.removeButton.Disable()
			self.updateCheckButton.Disable()

	def _shouldDisable(self, addon):
		return not (addon.isPendingDisable or (addon.isDisabled and not addon.isPendingEnable))

	def onListItemSelected(self, evt):
		index=evt.GetIndex()
		addon=self.curAddons[index] if index>=0 else None
		# #3090: Change toggle button label to indicate action to be taken if clicked.
		if addon is not None:
			# Translators: The label for a button in Add-ons Manager dialog to enable or disable the selected add-on.
			self.enableDisableButton.SetLabel(_("&Enable add-on") if not self._shouldDisable(addon) else _("&Disable add-on"))
		self.aboutButton.Enable(addon is not None and not addon.isPendingRemove)
		self.helpButton.Enable(bool(addon is not None and not addon.isPendingRemove and addon.getDocFilePath()))
		self.enableDisableButton.Enable(addon is not None and not addon.isPendingRemove)
		self.removeButton.Enable(addon is not None and not addon.isPendingRemove)
		self.updateCheckButton.Enable()

	def onClose(self,evt):
		self.Destroy()
		needsRestart = False
		for addon in self.curAddons:
			if (addon.isPendingInstall or addon.isPendingRemove
				or addon.isDisabled and addon.isPendingEnable
				or addon.isRunning and addon.isPendingDisable):
				needsRestart = True
				break
		if needsRestart:
			# Translators: A message asking the user if they wish to restart NVDA as addons have been added, enabled/disabled or removed. 
			if gui.messageBox(_("Changes were made to add-ons. You must restart NVDA for these changes to take effect. Would you like to restart now?"),
			# Translators: Title for message asking if the user wishes to restart NVDA as addons have been added or removed. 
			_("Restart NVDA"),
			wx.YES|wx.NO|wx.ICON_WARNING)==wx.YES:
				core.restart()

	def onAbout(self,evt):
		index=self.addonsList.GetFirstSelected()
		if index<0: return
		manifest=self.curAddons[index].manifest
		# Translators: message shown in the Addon Information dialog. 
		message=_("""{summary} ({name})
Version: {version}
Author: {author}
Description: {description}
""").format(**manifest)
		url=manifest.get('url')
		if url: 
			# Translators: the url part of the About Add-on information
			message+=_("URL: {url}").format(url=url)
		# Translators: title for the Addon Information dialog
		title=_("Add-on Information")
		gui.messageBox(message, title, wx.OK)

	def onHelp(self, evt):
		index = self.addonsList.GetFirstSelected()
		if index < 0:
			return
		path = self.curAddons[index].getDocFilePath()
		os.startfile(path)

	def onEnableDisable(self, evt):
		index=self.addonsList.GetFirstSelected()
		if index<0: return
		addon=self.curAddons[index]
		shouldDisable = self._shouldDisable(addon)
		# Counterintuitive, but makes sense when context is taken into account.
		addon.enable(not shouldDisable)
		self.enableDisableButton.SetLabel(_("&Enable add-on") if shouldDisable else _("&Disable add-on"))
		self.refreshAddonsList(activeIndex=index)

	def onGetAddonsClick(self,evt):
		ADDONS_URL = "http://addons.nvda-project.org"
		os.startfile(ADDONS_URL)

	def __del__(self):
		AddonsDialog._instance = None

	@classmethod
	def handleRemoteAddonInstall(cls, addonPath):
		closeAfter = AddonsDialog._instance is None
		dialog = AddonsDialog(gui.mainFrame)
		dialog.installAddon(addonPath, closeAfter=closeAfter)
		del dialog


class AddonUpdatesDialog(wx.Dialog):

	def __init__(self,parent, addonUpdateInfo, auto=True):
		# Translators: The title of the add-on updates dialog.
		super(AddonUpdatesDialog,self).__init__(parent,title=_("Add-on Updates"))
		mainSizer=wx.BoxSizer(wx.VERTICAL)
		addonsSizerHelper = guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)
		self.addonUpdateInfo = addonUpdateInfo
		self.auto = auto

		if addonUpdateInfo:
			entriesSizer=wx.BoxSizer(wx.VERTICAL)
			self.addonsList=wx.ListCtrl(self,-1,style=wx.LC_REPORT|wx.LC_SINGLE_SEL,size=(550,350))
			# Translators: The label for a column in add-ons list used to identify add-on package name (example: package is OCR).
			self.addonsList.InsertColumn(0,_("Package"),width=150)
			# Translators: The label for a column in add-ons list used to identify add-on's running status (example: status is running).
			self.addonsList.InsertColumn(1,_("Current version"),width=50)
			# Translators: The label for a column in add-ons list used to identify add-on's version (example: version is 0.3).
			self.addonsList.InsertColumn(2,_("New version"),width=50)
			entriesSizer.Add(self.addonsList,proportion=8)
			for entry in sorted(addonUpdateInfo.keys()):
				addon = addonUpdateInfo[entry]
				self.addonsList.Append((addon['summary'], addon['curVersion'], addon['version']))
			addonsSizerHelper.addItem(entriesSizer)
		else:
			# Translators: Message displayed when no add-on updates are available.
			addonsSizerHelper.addItem(wx.StaticText(self, label=_("No add-on update available.")))

		bHelper = addonsSizerHelper.addDialogDismissButtons(guiHelper.ButtonHelper(wx.HORIZONTAL))
		if addonUpdateInfo:
			# Translators: The label of a button to update add-ons.
			label = _("&Update add-ons")
			updateButton = bHelper.addButton(self, label=label)
			updateButton.Bind(wx.EVT_BUTTON, self.onUpdate)

		# Translators: The label of a button to close a dialog.
		closeButton = bHelper.addButton(self, wx.ID_CLOSE, label=_("&Close"))
		closeButton.Bind(wx.EVT_BUTTON, self.onClose)
		self.Bind(wx.EVT_CLOSE, lambda evt: self.onClose)
		self.EscapeId = wx.ID_CLOSE

		mainSizer.Add(addonsSizerHelper.sizer, border=guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		self.Sizer = mainSizer
		mainSizer.Fit(self)
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)
		wx.CallAfter(self.Show)

	def onUpdate(self, evt):
		self.Destroy()
		# #3208: do not display add-ons manager while updates are in progres.
		# Also, Skip the below step if this is an automatic update check.
		if not self.auto:
			self.Parent.Destroy()
		updateAddonsGenerator(self.addonUpdateInfo.values(), auto=self.auto).next()

	def onClose(self, evt):
		self.Destroy()
		if not self.auto:
			gui.mainFrame.onAddonsManagerCommand(None)


def updateAddonsGenerator(addons, auto=True):
	"""Updates one add-on after the other.
	The auto parameter is used to show add-ons manager after all add-ons were updated.
	"""
	if not len(addons):
		if auto:
			wx.CallLater(1, AddonsDialog(gui.mainFrame).Close)
		else:
			gui.mainFrame.onAddonsManagerCommand(None)
		return
	# #3208: Update (download and install) add-ons one after the other.
	addonInfo = addons.pop()
	downloader = AddonUpdateDownloader([addonInfo["urls"]], addonInfo["summary"], addonsToBeUpdated=addons, auto=auto)
	downloader.start()
	yield


class AddonUpdateDownloader(updateCheck.UpdateDownloader):
	"""Same as downloader class for NVDA screen reader updates.
	No hash checking for now, and URL's and temp file paths are different.
	"""

	def __init__(self, urls, addonName, fileHash=None, addonsToBeUpdated=None, auto=True):
		"""Constructor.
		@param urls: URLs to try for the update file.
		@type urls: list of str
		@param addonName: Name of the add-on being downloaded.
		@type addonName: str
		@param fileHash: The SHA-1 hash of the file as a hex string.
		@type fileHash: basestring
		@param addonsToBeUpdated: a list of add-ons that needs updating.
		@type addonsToBeUpdated: list of str
		@param auto: Automatic add-on updates or not.
		@type auto: bool
		"""
		super(AddonUpdateDownloader, self).__init__(urls, fileHash)
		self.urls = urls
		self.addonName = addonName
		self.destPath = tempfile.mktemp(prefix="nvda_addonUpdate-", suffix=".nvda-addon")
		self.fileHash = fileHash
		self.addonsToBeUpdated = addonsToBeUpdated
		self.auto = auto

	def start(self):
		"""Start the download.
		"""
		self._shouldCancel = False
		# Use a timer because timers aren't re-entrant.
		self._guiExecTimer = wx.PyTimer(self._guiExecNotify)
		gui.mainFrame.prePopup()
		# Translators: The title of the dialog displayed while downloading add-on update.
		self._progressDialog = wx.ProgressDialog(_("Downloading Add-on Update"),
			# Translators: The progress message indicating the name of the add-on being downloaded.
			_("Downloading {name}").format(name = self.addonName),
			# PD_AUTO_HIDE is required because ProgressDialog.Update blocks at 100%
			# and waits for the user to press the Close button.
			style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_AUTO_HIDE,
			parent=gui.mainFrame)
		self._progressDialog.Raise()
		t = threading.Thread(target=self._bg)
		t.daemon = True
		t.start()

	def _error(self):
		self._stopped()
		gui.messageBox(
			# Translators: A message indicating that an error occurred while downloading an update to NVDA.
			_("Error downloading update for {name}.").format(name = self.addonName),
			_("Error"),
			wx.OK | wx.ICON_ERROR)
		self.continueUpdatingAddons()

	def _downloadSuccess(self):
		self._stopped()
		try:
			try:
				bundle=addonHandler.AddonBundle(self.destPath.decode("mbcs"))
			except:
				log.error("Error opening addon bundle from %s"%self.destPath,exc_info=True)
				# Translators: The message displayed when an error occurs when trying to update an add-on package due to package problems.
				gui.messageBox(_("Cannot update {name} - missing file or invalid file format").format(name = self.addonName),
					# Translators: The title of a dialog presented when an error occurs.
					_("Error"),
					wx.OK | wx.ICON_ERROR)
				self.continueUpdatingAddons()
				return
			bundleName=bundle.manifest['name']
			# Optimization (future): it is better to remove would-be add-ons all at once instead of doing it each time a bundle is opened.
			for addon in addonHandler.getAvailableAddons():
				if not addon.isPendingRemove and bundleName==addon.manifest['name']:
					addon.requestRemove()
					break
			progressDialog = gui.IndeterminateProgressDialog(gui.mainFrame,
			# Translators: The title of the dialog presented while an Addon is being updated.
			_("Updating {name}").format(name = self.addonName),
			# Translators: The message displayed while an addon is being updated.
			_("Please wait while the add-on is being updated."))
			try:
				gui.ExecAndPump(addonHandler.installAddonBundle,bundle)
			except:
				log.error("Error installing  addon bundle from %s"%self.destPath,exc_info=True)
				progressDialog.done()
				progressDialog.Hide()
				progressDialog.Destroy()
				# Translators: The message displayed when an error occurs when installing an add-on package.
				gui.messageBox(_("Failed to update {name} add-on").format(name = self.addonName),
					# Translators: The title of a dialog presented when an error occurs.
					_("Error"),
					wx.OK | wx.ICON_ERROR)
				self.continueUpdatingAddons()
				return
			else:
				progressDialog.done()
				progressDialog.Hide()
				progressDialog.Destroy()
		finally:
			try:
				os.remove(self.destPath)
			except OSError:
				pass
		self.continueUpdatingAddons()

	def continueUpdatingAddons(self):
		try:
			updateAddonsGenerator(self.addonsToBeUpdated, auto=self.auto).next()
		except StopIteration:
			pass
