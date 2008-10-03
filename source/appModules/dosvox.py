import appModuleHandler
import speech

class AppModule(appModuleHandler.AppModule):

	def event_appGainFocus(self):
		speech.speechMode=speech.speechMode_off

	def event_appLoseFocus(self):
		speech.speechMode=speech.speechMode_talk
