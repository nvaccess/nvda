#gui/smartDictManager.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os
import wx
import gui
from logHandler import log
import speechDictHandler
from settingsDialogs import DictionaryDialog
from synthDriverHandler  import getListOfAllSynthsAndTheirVoices
from re import escape

class SmartDictMatchesDialog(wx.Dialog):
	def __init__(self,parent,smartDict):
		super(SmartDictMatchesDialog,self).__init__(parent,title=_("dictionary matches"))
		mainSizer=wx.BoxSizer(wx.VERTICAL)
		tree = wx.TreeCtrl(self,id=wx.NewId(), style=wx.TR_HIDE_ROOT)
		synths = getListOfAllSynthsAndTheirVoices()
		treeID=tree.AddRoot(_("Synthesizers"))
		synthAdded=False
		for s in synths:
			for v in s[1]:
				if not smartDict.matches("%s-%s" %(s[0],v)): continue
				if not synthAdded:
					id = tree.AppendItem(treeID,s[0])
					synthAdded = True
				tree.AppendItem(id,v)
			synthAdded=False
		mainSizer.Add(tree)
		buttonSizer=self.CreateButtonSizer(wx.OK)
		mainSizer.Add(buttonSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.BOTTOM)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		tree.SetFocus()

class SmartDictChooseMatchesDialog(wx.Dialog):
	def __init__(self,parent,smartDict):
		super(SmartDictChooseMatchesDialog,self).__init__(parent,title=_("dictionary matches"))
		mainSizer=wx.BoxSizer(wx.VERTICAL)
		self.list = wx.ListBox(self,id=wx.NewId(), style=wx.LB_MULTIPLE, name=_("Choose items"))
		synths = getListOfAllSynthsAndTheirVoices()
		for s in synths:
			rootID = self.list.Append(s[0])
			if smartDict.matches(s[0]): self.list.Select(rootID)
			childID = rootID
			for v in s[1]:
				childID = self.list.Append(v,rootID)
				if smartDict.matches("%s-%s" %(s[0],v)): self.list.Select(childID)
			self.list.SetClientData(rootID,childID)
		mainSizer.Add(self.list)
		buttonSizer=self.CreateButtonSizer(wx.OK|wx.CANCEL)
		mainSizer.Add(buttonSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.BOTTOM)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.list.SetFocus()

	def processSelection(self):
		"""This will process user selection and construct the regular expression."""
		synthChecked = False
		regExpr = []
		for item in self.list.GetSelections():
			#determine whether it is synth or voice
			data = self.list.GetClientData(item)
			isSynth = (data >= item)
			if isSynth: 
				synthChecked = self.list.IsSelected(item)
				if synthChecked: 
					regExpr.append(escape(self.list.GetString(item)))
					continue
			else:
				#ignore voice  if  synth is allready checked
				if synthChecked: continue
			if self.list.IsSelected(item): regExpr.append(escape(self.list.GetString(item)))
		return "(%s)" % "|".join(regExpr)

class SmartDictDialog(wx.Dialog):
	"""For creating|modifying smart dictionary."""
	smartDict = None

	def __init__(self,parent,_title,smartDict):
		super(SmartDictDialog,self).__init__(parent,title=_title)
		self.smartDict = smartDict
		mainSizer=wx.BoxSizer(wx.VERTICAL)
		settingsSizer=wx.BoxSizer(wx.VERTICAL)
		settingsSizer.Add(wx.StaticText(self,-1,label=_("Name")))
		self.nameTextCtrl=wx.TextCtrl(self,wx.NewId())
		self.nameTextCtrl.SetValue(smartDict.name)
		settingsSizer.Add(self.nameTextCtrl)
		settingsSizer.Add(wx.StaticText(self,-1,label=_("Regular expression pattern")))
		self.patternTextCtrl=wx.TextCtrl(self,wx.NewId())
		self.patternTextCtrl.SetValue(smartDict.pattern)
		settingsSizer.Add(self.patternTextCtrl)
		buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
		showMatchesButtonID=wx.NewId()
		showMatchesButton=wx.Button(self,showMatchesButtonID,_("Show &matches..."),wx.DefaultPosition)
		self.Bind(wx.EVT_BUTTON,self.onShowMatchesClick,id=showMatchesButtonID)
		buttonSizer.Add(showMatchesButton,border=20,flag=wx.LEFT|wx.RIGHT|wx.BOTTOM)
		chooseMatchesButtonID=wx.NewId()
		chooseMatchesButton=wx.Button(self,chooseMatchesButtonID,_("&Choose matches..."),wx.DefaultPosition)
		self.Bind(wx.EVT_BUTTON,self.onChooseMatchesClick,id=chooseMatchesButtonID)
		buttonSizer.Add(chooseMatchesButton,border=20,flag=wx.LEFT|wx.RIGHT|wx.BOTTOM)
		mainSizer.Add(buttonSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.BOTTOM)
		mainSizer.Add(settingsSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)
		buttonSizer=self.CreateButtonSizer(wx.OK|wx.CANCEL)
		mainSizer.Add(buttonSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.BOTTOM)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.nameTextCtrl.SetFocus()

	def onShowMatchesClick(self, evt):
		self.smartDict.setPattern(self.patternTextCtrl.GetValue())
		smartDictMatchesDialog =  SmartDictMatchesDialog(self,self.smartDict)
		smartDictMatchesDialog.ShowModal()
		smartDictMatchesDialog.Destroy()

	def onChooseMatchesClick(self, evt):
		self.smartDict.setPattern(self.patternTextCtrl.GetValue())
		smartDictChooseMatchesDialog = SmartDictChooseMatchesDialog(self,self.smartDict)
		if smartDictChooseMatchesDialog.ShowModal():
			self.patternTextCtrl.SetValue(smartDictChooseMatchesDialog.processSelection())
		smartDictChooseMatchesDialog.Destroy()

class SmartDictManagerDialog(wx.Dialog):
	"""shows the list of smart dictionaries and provides manipulating actions"""
	smartDicts = None

	def __init__(self, parent):
		super(SmartDictManagerDialog, self).__init__(parent, wx.ID_ANY, _("Smart Dictionary Manager"))
		self.smartDicts = list(speechDictHandler.smartDicts)
		mainSizer=wx.BoxSizer(wx.VERTICAL)
		#create a list of all dictionaries
		dictListID=wx.NewId()
		self.dictList=wx.ListCtrl(self,dictListID,style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
		entriesSizer=wx.BoxSizer(wx.HORIZONTAL)
		entriesSizer.Add(wx.StaticText(self,-1,label=_("&Smart dictionaries")))
		self.dictList.InsertColumn(0,_("Name"))
		self.dictList.InsertColumn(1,_("Pattern"))
		for smartDict in self.smartDicts:
			self.dictList.Append((smartDict.name, smartDict.pattern))
		entriesSizer.Add(self.dictList)
		buttonsSizer=wx.BoxSizer(wx.VERTICAL)
		createButtonID = wx.NewId()
		createButton=wx.Button(self,createButtonID,_("&Create dictionary..."),wx.DefaultPosition)
		self.Bind(wx.EVT_BUTTON,self.onCreateClick,id=createButtonID)
		buttonsSizer.Add(createButton)
		deleteButtonID=wx.NewId()
		deleteButton=wx.Button(self,deleteButtonID,_("&Delete dictionary"),wx.DefaultPosition)
		self.Bind(wx.EVT_BUTTON,self.onDeleteClick,id=deleteButtonID)
		buttonsSizer.Add(deleteButton)
		changeButtonID=wx.NewId()
		changeButton=wx.Button(self,changeButtonID,_("&Change dictionary properties..."),wx.DefaultPosition)
		self.Bind(wx.EVT_BUTTON,self.onChangeClick,id=changeButtonID)
		buttonsSizer.Add(changeButton)
		editButtonID=wx.NewId()
		editButton=wx.Button(self,editButtonID,_("&Edit dictionary entries..."),wx.DefaultPosition)
		self.Bind(wx.EVT_BUTTON,self.onEditClick,id=editButtonID)
		buttonsSizer.Add(editButton)
		mainSizer.Add(entriesSizer)
		mainSizer.Add(buttonsSizer)
		closeButtonID=wx.NewId()
		closeButton=wx.Button(self,closeButtonID,_("C&lose"),wx.DefaultPosition)
		self.Bind(wx.EVT_BUTTON,self.onCloseClick,id=closeButtonID)
		mainSizer.Add(closeButton,border=20,flag=wx.LEFT|wx.RIGHT|wx.BOTTOM)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.dictList.SetFocus()

	def onEditClick(self, evt):
		i = self.dictList.GetFirstSelected()
		if i <0: return
		dict = self.smartDicts[i]
		dialog = DictionaryDialog(self, dict.fileName, dict)
		dialog.Show()

	def onCreateClick(self, evt):
		smartDict = speechDictHandler.SmartDict()
		smartDictDialog = SmartDictDialog(self, _("New smart dictionary"), smartDict)
		if smartDictDialog.ShowModal()==wx.ID_OK:
			smartDict.setName(smartDictDialog.nameTextCtrl.GetValue())
			smartDict.setPattern(smartDictDialog.patternTextCtrl.GetValue())
			smartDict.save()
			self.smartDicts.append(smartDict)
			self.dictList.Append((smartDict.name, smartDict.pattern))
		smartDictDialog.Destroy()

	def onDeleteClick(self, evt):
		i = self.dictList.GetFirstSelected()
		if i <0: return
		dict = self.smartDicts[i]
		d = wx.MessageDialog(self, _("Are you sure you want to delete dictionary '%s'?" % dict.name), _("Confirm dictionary deletion"), wx.YES|wx.NO|wx.ICON_QUESTION)
		if d.ShowModal() == wx.ID_YES:
			fileName = dict.fileName
			del self.smartDicts[i]
			if os.access(fileName, os.F_OK): os.remove(fileName)
			self.dictList.DeleteItem(i)
		d.Destroy()

	def onChangeClick(self, evt):
		i = self.dictList.GetFirstSelected()
		if i <0: return
		smartDict = self.smartDicts[i]
		oldName = smartDict.name
		smartDictDialog = SmartDictDialog(self, _("Change smart dictionary"), smartDict)
		if smartDictDialog.ShowModal()==wx.ID_OK:
			if oldName != smartDictDialog.nameTextCtrl.GetValue():
				if os.access(smartDict.fileName, os.F_OK): os.remove(smartDict.fileName)
			smartDict.setName(smartDictDialog.nameTextCtrl.GetValue())
			smartDict.setPattern(smartDictDialog.patternTextCtrl.GetValue())
			smartDict.save()
			self.dictList.SetStringItem(i,0,smartDict.name)
			self.dictList.SetStringItem(i,1,smartDict.pattern)
		smartDictDialog.Destroy()

	def onCloseClick(self, evt):
		speechDictHandler.smartDicts = list(self.smartDicts)
		speechDictHandler.reflectVoiceChange()
		self.Destroy()
