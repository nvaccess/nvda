#appModules/klangoplayer.py

import _default
from keyUtils import sendKey

class AppModule(_default.AppModule):

	def script_sayAll(self,keyPress):
		sendKey(([],"extendedinsert"))
		sendKey((["extendedinsert"],"extendeddown"))
	script_sayAll.__doc__ = _("reads from the system caret up to the end of the text, moving the caret as it goes")
