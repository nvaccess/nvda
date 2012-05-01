import wx
import core
import gui
from logHandler import log
import addonHandler

class AddonsDialog(wx.Dialog):

	def __init__(self,parent):
		# Translators: The title of the Addons Dialog
		super(AddonsDialog,self).__init__(parent,title=_("Addons Manager"))
		self.needsRestart=False
		mainSizer=wx.BoxSizer(wx.VERTICAL)
		settingsSizer=wx.BoxSizer(wx.VERTICAL)
		entriesSizer=wx.BoxSizer(wx.VERTICAL)
		# Translators: the label for the installed addons list in the addons manager.
		entriesLabel=wx.StaticText(self,-1,label=_("&Installed Addons"))
		entriesSizer.Add(entriesLabel)
		self.addonsList=wx.ListCtrl(self,-1,style=wx.LC_REPORT|wx.LC_SINGLE_SEL,size=(550,350))
		self.addonsList.InsertColumn(0,_("Status"),width=50)
		self.addonsList.InsertColumn(1,_("Package"),width=150)
		self.addonsList.InsertColumn(2,_("Version"),width=50)
		self.addonsList.InsertColumn(3,_("Author"),width=300)
		self.addonsList.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.onListItemSelected)
		entriesSizer.Add(self.addonsList,proportion=8)
		settingsSizer.Add(entriesSizer)
		entryButtonsSizer=wx.BoxSizer(wx.HORIZONTAL)
		aboutButtonID=wx.NewId()
		self.aboutButton=wx.Button(self,aboutButtonID,_("&About Addon..."),wx.DefaultPosition)
		self.aboutButton.Disable()
		self.Bind(wx.EVT_BUTTON,self.onAbout,id=aboutButtonID)
		entryButtonsSizer.Add(self.aboutButton)
		addButtonID=wx.NewId()
		self.addButton=wx.Button(self,addButtonID,_("&Add..."),wx.DefaultPosition)
		self.Bind(wx.EVT_BUTTON,self.OnAddClick,id=addButtonID)
		entryButtonsSizer.Add(self.addButton)
		removeButtonID=wx.NewId()
		self.removeButton=wx.Button(self,removeButtonID,_("&Remove"),wx.DefaultPosition)
		self.removeButton.Disable()
		self.Bind(wx.EVT_BUTTON,self.OnRemoveClick,id=removeButtonID)
		entryButtonsSizer.Add(self.removeButton)
		settingsSizer.Add(entryButtonsSizer)
		mainSizer.Add(settingsSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)
		# Translators: The label of a button to continue with the operation.
		closeButton = wx.Button(self, label=_("C&lose"), id=wx.ID_OK)
		closeButton.Bind(wx.EVT_BUTTON, self.onClose)
		mainSizer.Add(closeButton,border=20,flag=wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.CENTER)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.refreshAddonsList()
		self.addonsList.SetFocus()

	def OnAddClick(self,evt):
		# Translators: The message displayed in the dialog that allows you to choose an addon bundle for installation.
		fd=wx.FileDialog(self,message=_("Choose Addon bundle file"),
		# Translators: the label for the nvda adon file type in the Choose addon dialog.
		wildcard=(_("NVDA Addon Bundle (*.{ext})")+"|*.{ext}").format(ext=addonHandler.BUNDLE_EXTENSION),
		defaultDir="c:",style=wx.FD_OPEN)
		if fd.ShowModal()!=wx.ID_OK:
			return
		addonPath=fd.GetPath()
		try:
			bundle=addonHandler.AddonBundle(addonPath)
		except:
			log.error("Error opening addon bundle from %s"%addonPath,exc_info=True)
			# Translators: The message displayed when an error occurs when opening an addon bundle for adding. 
			gui.messageBox(_("Failed to open addon bundle file at %s - missing file or invalid file format")%addonPath,
				# Translators: The title of a dialog presented when an error occurs.
				_("Error"),
				wx.OK | wx.ICON_ERROR)
			return
		# Translators: A message asking the user if they really wish to install an addon.
		if gui.messageBox(_("Are you sure you want to install this addon? Only install addons from trusted sources.\nAddon: {summary} {version}\nAuthor: {author}").format(**bundle.manifest),
			# Translators: Title for message asking if the user really wishes to install an Addon.
			_("Addon Installation"),
			wx.YES|wx.NO|wx.ICON_WARNING)!=wx.YES:
			return
		bundleName=bundle.manifest['name']
		if any(bundleName==addon.manifest['name'] for addon in self.curAddons if not addon.isPendingRemove):
			# Translators: The message displayed when an an addon already seems to be installed. 
			gui.messageBox(_("This addon seems to already be installed. Please remove the existing addon and try again."),
				# Translators: The title of a dialog presented when an error occurs.
				_("Error"),
				wx.OK | wx.ICON_WARNING)
			return
		progressDialog = gui.IndeterminateProgressDialog(gui.mainFrame,
		# Translators: The title of the dialog presented while an Addon is being installed.
		_("Installing Addon"),
		# Translators: The message displayed while an addon is being installed.
		_("Please wait while the addon is being installed."))
		try:
			gui.ExecAndPump(addonHandler.installAddonBundle,bundle)
			self.needsRestart=True
		except:
			log.error("Error installing  addon bundle from %s"%addonPath,exc_info=True)
			self.refreshAddonsList()
			progressDialog.done()
			del progressDialog
			# Translators: The message displayed when an error occurs when installing an addon bundle.
			gui.messageBox(_("Failed to install addon  from %s")%addonPath,
				# Translators: The title of a dialog presented when an error occurs.
				_("Error"),
				wx.OK | wx.ICON_ERROR)
			return
		else:
			self.refreshAddonsList()
			progressDialog.done()
			del progressDialog

	def OnRemoveClick(self,evt):
		index=self.addonsList.GetFirstSelected()
		if index<0: return
		if gui.messageBox(_("Are you sure you wish to remove the selected addon from NVDA?"), _("Remove Addon"), wx.YES_NO|wx.ICON_WARNING) != wx.YES: return
		addon=self.curAddons[index]
		addon.requestRemove()
		self.needsRestart=True
		self.refreshAddonsList()
		self.addonsList.SetFocus()

	def getAddonStatus(self,addon):
		if addon.isPendingInstall:
			# Translators: The status shown for a newly installed addon before NVDA is restarted.
			return _("new")
		elif addon.isPendingRemove:
			# Translators: The status shown for an addon that has been marked as removed, before NVDA has been restarted.
			return _("removed")
		else:
			# Translators: The status shown for an addon when its currently running in NVDA.
			return _("running")

	def refreshAddonsList(self):
		self.addonsList.DeleteAllItems()
		self.curAddons=[]
		for addon in addonHandler.getAvailableAddons(refresh=True):
			self.addonsList.Append((self.getAddonStatus(addon), addon.manifest['summary'],addon.manifest['version'], addon.manifest['author']))
			self.curAddons.append(addon)
		# select the given active addon or the first addon if not given
		if len(self.curAddons)>0:
			activeIndex=0
			self.addonsList.Select(activeIndex,on=1)
			self.addonsList.SetItemState(activeIndex,wx.LIST_STATE_FOCUSED,wx.LIST_STATE_FOCUSED)
		else:
			self.aboutButton.Disable()
			self.removeButton.Disable()

	def onListItemSelected(self, evt):
		index=evt.GetIndex()
		addon=self.curAddons[index] if index>=0 else None
		self.aboutButton.Enable(addon is not None and not addon.isPendingRemove)
		self.removeButton.Enable(addon is not None and not addon.isPendingRemove)

	def onClose(self,evt):
		self.Destroy()
		if self.needsRestart:
			# Translators: A message asking the user if they wish to restart NVDA as addons have been added or removed. 
			if gui.messageBox(_("Addons have been added or removed. You must restart NVDA for these changes to take affect. Would you like to restart now?"),
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
URL: {url}
Description: {description}
""").format(**manifest)
		# Translators: title for the Addon Information dialog
		title=_("Add-on Information")
		gui.messageBox(message, title, wx.OK)
