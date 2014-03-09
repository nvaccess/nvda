#appModules/totalcmd64.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2014 Marco Zehe
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import totalcmd

class TCList(totalcmd.TCList):

	expectedCounter=3

class AppModule(totalcmd.AppModule):

	tcmdListBoxes = ('LCLListBox',)
	TCList = TCList
