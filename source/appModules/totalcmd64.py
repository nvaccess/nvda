#appModules/totalcmd64.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2014 NVDA Contributors
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import totalcmd

class TCList(totalcmd.TCList):

	expectedCounter=3

class AppModule(totalcmd.AppModule):

	tcmdListBoxes = ('LCLListBox',)
	TCList = TCList
	chooseNVDAObjectOverlayClasses = totalcmd.AppModule.chooseNVDAObjectOverlayClasses
