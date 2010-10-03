#appModules/sndrec32.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2010 Peter Vagner <peter.v@datagate.sk>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import _default
import controlTypes

mainWindowButtonNames={
	205:_("Rewind"),
	206:_("Forward"),
	207:_("Play"),
	208:_("Stop"),
	209:_("Record")
}

class AppModule(_default.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.role == controlTypes.ROLE_WINDOW: 
			return
		elif obj.role == controlTypes.ROLE_BUTTON: 
			if obj.windowControlID in mainWindowButtonNames.keys():
				obj.name=mainWindowButtonNames[obj.windowControlID]
