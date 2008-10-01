import appModuleHandler
import speech

class appModule(appModuleHandler.AppModule):

	def event_appGainFocus(self):
		speech.speechMode=speech.speechMode_off

	def event_appLoseFocus(self):
		speech.speechMode=speech.speechMode_talk
