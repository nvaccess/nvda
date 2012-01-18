#appModules/sndrec32.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2010 Peter Vagner <peter.v@datagate.sk>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import appModuleHandler
import controlTypes

mainWindowButtonNames={
	# Translators: This is the name of a button in sound recorder.
	205:_("Rewind"),
	# Translators: This is the name of a button in sound recorder.
	206:_("Fast forward"),
	# Translators: This is the name of a button in sound recorder.
	207:_("Play"),
	# Translators: This is the name of a button in sound recorder.
	208:_("Stop"),
	# Translators: This is the name of a button in sound recorder.
	209:_("Record")
}

class AppModule(appModuleHandler.AppModule):

	def event_NVDAObject_init(self, obj):
		if obj.role == controlTypes.ROLE_BUTTON: 
			try:
				obj.name=mainWindowButtonNames[obj.windowControlID]
			except KeyError:
				pass
