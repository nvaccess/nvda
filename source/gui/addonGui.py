#gui/addonGui.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2012-2014 NV Access Limited, Beqa Gozalishvili

import os
import wx
import core
import languageHandler
import gui
from logHandler import log
import addonHandler
import globalVars

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
		self.needsRestart=False
		mainSizer=wx.BoxSizer(wx.VERTICAL)
		settingsSizer=wx.BoxSizer(wx.VERTICAL)
		entriesSizer=wx.BoxSizer(wx.VERTICAL)
		if globalVars.appArgs.disableAddons:
			# Translators: A message in the add-ons manager shown when all add-ons are disabled.
			addonsDisabledLabel=wx.StaticText(self,-1,label=_("All add-ons are now disabled. To enable add-ons you must restart NVDA."))
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
		# Translators: The label for a button in Add-ons Manager dialog to install an add-on.
		self.addButton=wx.Button(self,label=_("&Install..."))
		self.addButton.Bind(wx.EVT_BUTTON,self.OnAddClick)
		entryButtonsSizer.Add(self.addButton)
		# Translators: The label for a button to remove either:
		# Remove the selected add-on in Add-ons Manager dialog.
		# Remove a speech dictionary entry.
		self.removeButton=wx.Button(self,label=_("&Remove"))
		self.removeButton.Disable()
		self.removeButton.Bind(wx.EVT_BUTTON,self.OnRemoveClick)
		entryButtonsSizer.Add(self.removeButton)
		# Translators: The label of a button in Add-ons Manager to open the Add-ons website and get more add-ons.
		self.getAddonsButton=wx.Button(self,label=_("&Get add-ons..."))
		self.getAddonsButton.Bind(wx.EVT_BUTTON,self.OnGetAddonsClick)
		entryButtonsSizer.Add(self.getAddonsButton)
		settingsSizer.Add(entryButtonsSizer)
		mainSizer.Add(settingsSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)
		# Translators: The label of a button to close the Addons dialog.
		closeButton = wx.Button(self, label=_("&Close"), id=wx.ID_CLOSE)
		closeButton.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
		mainSizer.Add(closeButton,border=20,flag=wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.CENTER)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.EscapeId = wx.ID_CLOSE
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.refreshAddonsList()
		self.addonsList.SetFocus()
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)

	def OnAddClick(self,evt):
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
			progressDialog = gui.IndeterminateProgressDialog(gui.mainFrame,
			# Translators: The title of the dialog presented while an Addon is being installed.
			_("Installing Add-on"),
			# Translators: The message displayed while an addon is being installed.
			_("Please wait while the add-on is being installed."))
			try:
				gui.ExecAndPump(addonHandler.installAddonBundle,bundle)
				self.needsRestart=True
			except:
				log.error("Error installing  addon bundle from %s"%addonPath,exc_info=True)
				self.refreshAddonsList()
				progressDialog.done()
				del progressDialog
				# Translators: The message displayed when an error occurs when installing an add-on package.
				gui.messageBox(_("Failed to install add-on  from %s")%addonPath,
					# Translators: The title of a dialog presented when an error occurs.
					_("Error"),
					wx.OK | wx.ICON_ERROR)
				return
			else:
				self.refreshAddonsList(activeIndex=-1)
				progressDialog.done()
				del progressDialog
		finally:
			if closeAfter:
				# #4460: If we do this immediately, wx seems to drop the WM_QUIT sent if the user chooses to restart.
				# This seems to have something to do with the wx.ProgressDialog.
				# The CallLater seems to work around this.
				wx.CallLater(1, self.Close)

	def OnRemoveClick(self,evt):
		index=self.addonsList.GetFirstSelected()
		if index<0: return
		if gui.messageBox(_("Are you sure you wish to remove the selected add-on from NVDA?"), _("Remove Add-on"), wx.YES_NO|wx.ICON_WARNING) != wx.YES: return
		addon=self.curAddons[index]
		addon.requestRemove()
		self.needsRestart=True
		self.refreshAddonsList(activeIndex=index)
		self.addonsList.SetFocus()

	def getAddonStatus(self,addon):
		if addon.isPendingInstall:
			# Translators: The status shown for a newly installed addon before NVDA is restarted.
			return _("install")
		elif addon.isPendingRemove:
			# Translators: The status shown for an addon that has been marked as removed, before NVDA has been restarted.
			return _("remove")
		elif globalVars.appArgs.disableAddons:
			# Translators: The status shown for an addon when its currently suspended do to addons been disabled.
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

	def onListItemSelected(self, evt):
		index=evt.GetIndex()
		addon=self.curAddons[index] if index>=0 else None
		self.aboutButton.Enable(addon is not None and not addon.isPendingRemove)
		self.helpButton.Enable(bool(addon is not None and not addon.isPendingRemove and addon.getDocFilePath()))
		self.removeButton.Enable(addon is not None and not addon.isPendingRemove)

	def onClose(self,evt):
		self.Destroy()
		if self.needsRestart:
			# Translators: A message asking the user if they wish to restart NVDA as addons have been added or removed. 
			if gui.messageBox(_("Add-ons have been added or removed. You must restart NVDA for these changes to take effect. Would you like to restart now?"),
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

	def OnGetAddonsClick(self,evt):
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
