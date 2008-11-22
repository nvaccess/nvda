import _default
import speech

class AppModule(_default.AppModule):

	def event_appGainFocus(self):
		speech.speechMode=speech.speechMode_off

	def event_appLoseFocus(self):
		speech.speechMode=speech.speechMode_talk
