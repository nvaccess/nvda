#appModules/klangoplayer.py

import _default
from keyUtils import sendKey
import config

class AppModule(_default.AppModule):

	def event_appGainFocus(self):
		self.speakTypedCharacters=config.conf["keyboard"]["speakTypedCharacters"]
		if self.speakTypedCharacters:
			config.conf["keyboard"]["speakTypedCharacters"]=False
		self.speakTypedWords=config.conf["keyboard"]["speakTypedWords"]
		if self.speakTypedWords:
			config.conf["keyboard"]["speakTypedWords"]=False
		self.speakCommandKeys=config.conf["keyboard"]["speakCommandKeys"]
		if self.speakCommandKeys:
			config.conf["keyboard"]["speakCommandKeys"]=False

	def event_appLoseFocus(self):
		config.conf["keyboard"]["speakTypedCharacters"]=self.speakTypedCharacters
		config.conf["keyboard"]["speakTypedWords"]=self.speakTypedWords
		config.conf["keyboard"]["speakCommandKeys"]=self.speakCommandKeys

	def script_sayAll(self,keyPress):
		sendKey(([],"extendedinsert"))
		sendKey((["extendedinsert"],"extendeddown"))
	script_sayAll.__doc__ = _("reads from the system caret up to the end of the text, moving the caret as it goes")
