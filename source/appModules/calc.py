import appModuleHandler
import speech

class appModule(appModuleHandler.AppModule):

	def __init__(self,*args,**kwargs):
		super(appModule,self).__init__(*args,**kwargs)
		self._lastValue=None

	def event_NVDAObject_init(self,obj):
		if obj.windowClassName=="Edit" and obj.windowControlID==403:
			obj.name="Display"

	def event_valueChange(self,obj,nextHandler):
		if obj.windowClassName=="Edit" and obj.windowControlID==403:
			text=obj.windowText[0:-1]
			text=text.rstrip()[0:-1]
			if text!=self._lastValue:
				speech.speakText(text)
				self._lastValue=text
		else:
			nextHandler()
