import appModuleHandler
import speech

class appModule(appModuleHandler.appModule):

	def event_appGainFocus(self):
		speech.speechMode=speech.speechMode_off

	def event_appLooseFocus(self):
		speech.speechMode=speech.speechMode_talk
