# -*- coding: UTF-8 -*-
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2017-2018 NV Access Limited, Thomas Stivers
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import gui
import ui
import wx
from logHandler import log
import lxml.html as lh
from lxml import etree

def generateHelp():
	helpFile = gui.getDocFilePath("userGuide.html")
	helpTree = lh.parse(helpFile)
	helpInfo = {}
	helpNames = helpTree.findall('.//a[@name]')
	for name in helpNames:
		helpInfo[name.attrib['name']] = ""
		currentHeadingLevel = int(name.getnext().tag[-1])
		for data in name.itersiblings():
			try:
				if not data.attrib.has_key('name'):
					helpInfo[name.attrib['name']] += etree.tostring(data).replace("&#13;", "")
				elif data.attrib['name'] == name.attrib['name']:
					continue
				elif int(data.getnext().tag[-1]) > currentHeadingLevel:
					continue
				else:
					break
			except(AttributeError): break
	return helpInfo

def showHelp(helpIds, evt):
	"""Display the corresponding section of the user guide when either the Help
	button in an NVDA dialog is pressed or the F1 key is pressed on a
	recognized control.
	"""
	helpInfo = generateHelp()
	# Translators: Message indicating no context sensitive help is available.
	helpMessage = _("No context sensitive help is available here at this time.")
	windowId = evt.GetId()
	windowName = evt.GetEventObject().GetName()
	log.debug("helpIds = %s\nwindowId = %d\nwindowName = %s"%(helpIds, windowId, windowName))
	# if the Help button is pressed or we have no help for a particular control then get help for the entire dialog.
	if windowId == wx.ID_HELP or not windowId in helpIds.keys():
		windowId = evt.GetEventObject().GetTopLevelParent().GetId()
		log.debug("WindowId changed to %d" % windowId)
	if windowId in helpIds.keys():
		helpTitle = _("NVDA Help")
		ui.browseableMessage(helpInfo[helpIds[windowId]], helpTitle, True)
	else:
		log.debug("Help for window id %d not found." % (windowId))
		evt.Skip(True)
