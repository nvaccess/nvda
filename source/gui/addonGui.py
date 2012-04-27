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
		self.addonsList=wx.ListCtrl(self,-1,style=wx.LC_REPORT|wx.LC_SINGLE_SEL,size=(500,350))
		self.addonsList.InsertColumn(0,_("Package"),width=150)
		self.addonsList.InsertColumn(1,_("Version"),width=50)
		self.addonsList.InsertColumn(2,_("Description"),width=300)
		self.refreshAddonsList()
		entriesSizer.Add(self.addonsList,proportion=8)
		settingsSizer.Add(entriesSizer)
		entryButtonsSizer=wx.BoxSizer(wx.HORIZONTAL)
		addButtonID=wx.NewId()
		addButton=wx.Button(self,addButtonID,_("&Add..."),wx.DefaultPosition)
		self.Bind(wx.EVT_BUTTON,self.OnAddClick,id=addButtonID)
		entryButtonsSizer.Add(addButton)
		removeButtonID=wx.NewId()
		removeButton=wx.Button(self,removeButtonID,_("&Remove"),wx.DefaultPosition)
		self.Bind(wx.EVT_BUTTON,self.OnRemoveClick,id=removeButtonID)
		entryButtonsSizer.Add(removeButton)
		settingsSizer.Add(entryButtonsSizer)
		mainSizer.Add(settingsSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)
		# Translators: The label of a button to continue with the operation.
		closeButton = wx.Button(self, label=_("C&lose"), id=wx.ID_OK)
		closeButton.Bind(wx.EVT_BUTTON, self.onClose)
		mainSizer.Add(closeButton,border=20,flag=wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.CENTER)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.addonsList.SetFocus()

	def OnAddClick(self,evt):
		# Translators: The message displayed in the dialog that allows you to choose an addon bundle for installation.
		fd=wx.FileDialog(self,message=_("Choose Addon bundle file"),wildcard="NVDA Addon Bundle (*.nvda-addon)|*.nvda-addon",defaultDir="c:",style=wx.FD_OPEN)
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
		if gui.messageBox(_("Are you sure you want to install this addon? Only install addons from trusted sources.\nAddon: {description}\nAuthor: {author}").format(**bundle.manifest),
			# Translators: Title for message asking if the user really wishes to install an Addon.
			_("Addon Installation"),
			wx.YES|wx.NO|wx.ICON_WARNING)!=wx.YES:
			return
		bundleName=bundle.manifest['name']
		if any(bundleName==addon.manifest['name'] for addon in self.curAddons):
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
		progressDialog = gui.IndeterminateProgressDialog(gui.mainFrame,
		# Translators: The title of the dialog presented while an Addon is being removed.
		_("Removing Addon"),
		# Translators: The message displayed while an addon is being removed.
		_("Please wait while the addon is being removed."))
		try:
			if addon.isLoaded:
				addon.unload()
			gui.ExecAndPump(addon.removeContents)
			self.needsRestart=True
		except:
			log.error("Failed to remove addon",exc_info=True)
		self.refreshAddonsList()
		progressDialog.done()
		del progressDialog
		self.addonsList.SetFocus()

	def refreshAddonsList(self):
		self.addonsList.DeleteAllItems()
		self.curAddons=[]
		for addon in addonHandler.getAvailableAddons(refresh=True):
			self.addonsList.Append((addon.manifest['description'],addon.manifest['version'],addon.manifest['long_description']))
			self.curAddons.append(addon)

	def onClose(self,evt):
		self.Destroy()
		if self.needsRestart:
			# Translators: A message asking the user if they wish to restart NVDA as addons have been added or removed. 
			if gui.messageBox(_("Addons have been added or removed. You must restart NVDA for these changes to take affect. Would you like to restart now?"),
			# Translators: Title for message asking if the user wishes to restart NVDA as addons have been added or removed. 
			_("Restart NVDA"),
			wx.YES|wx.NO|wx.ICON_WARNING)==wx.YES:
				core.restart()
