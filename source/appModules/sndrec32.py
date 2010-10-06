#appModules/sndrec32.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2010 Peter Vagner <peter.v@datagate.sk>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import _default
import controlTypes

mainWindowButtonNames={
	205:_("Rewind"),
	206:_("Fast forward"),
	207:_("Play"),
	208:_("Stop"),
	209:_("Record")
}

class AppModule(_default.AppModule):

	def event_NVDAObject_init(self, obj):
		if obj.role == controlTypes.ROLE_BUTTON: 
			if obj.windowControlID in mainWindowButtonNames.keys():
				obj.name=mainWindowButtonNames[obj.windowControlID]
