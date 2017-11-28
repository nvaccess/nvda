# -*- coding: UTF-8 -*-
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2017 NV Access Limited, Thomas Stivers
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import gui
import ui
import wx
from logHandler import log
from xml.etree import ElementTree

class Help():

	def __init__(self):
		helpTree = ElementTree.parse(gui.getDocFilePath("userGuide.html"))
		expression = "A[@name]"
		root = helpTree.getroot()

def showHelp(helpIds, evt):
	helpFile = gui.getDocFilePath("userGuide.html")
	# Translators: Message indicating no context sensitive help is available.
	helpMessage = _("No context sensitive help is available here at this time.")
	tag = None
	windowId = evt.GetId()
	# if the Help button is pressed or we have no help for a particular control then get help for the entire dialog.
	if windowId == wx.ID_HELP or not windowId in helpIds.keys():
		windowId = evt.parent.GetId()
	if windowId in helpIds.keys():
		try:
			with open(helpFile) as help:
				lines = help.readlines()
		except:
			evt.Skip()
		iLines = iter(lines)
		while iLines:
			try:
				line = next(iLines)
				if line.startswith("<A NAME=\"%s\"></A>" % (helpIds[windowId])):
					helpMessage = next(iLines)
					tag = helpMessage[:4]
					helpMessage += next(iLines)
				elif tag != None and not line.startswith(tag):
					helpMessage += line
				elif tag != None and (line.startswith(tag) or line.startswith("<H4>")):
					break
			except(StopIteration):
				break
		helpTitle = _("NVDA Help")
		ui.browseableMessage(helpMessage, helpTitle, True)
	else:
		log.debug("Help for window id %d not found." % (windowId))
		evt.Skip()
