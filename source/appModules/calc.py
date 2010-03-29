import _default
import NVDAObjects.IAccessible
import speech

class AppModule(_default.AppModule):

	def event_NVDAObject_init(self,obj):
		windowClassName=obj.windowClassName
		windowControlID=obj.windowControlID
		if windowClassName=="Edit" and windowControlID==403:
			self.overlayCustomNVDAObjectClass(obj,Display,outerMost=True)
		elif windowClassName=="Static" and windowControlID==150:
			self.overlayCustomNVDAObjectClass(obj,Display,outerMost=True)

class Display(NVDAObjects.IAccessible.IAccessible):

	shouldAllowIAccessibleFocusEvent=True

	calcCommandChars=['!','=','@','#']

	calcCommandKeys=[
		"back","escape","ExtendedReturn","Return",
		"f2","f3","f4","f5","f6","f7","f8","f9",
		"l","n","o","p","r","s","t",
	]

	def _get_name(self):
		name=super(Display,self).name
		if not name:
			name=_("Display")
		return name

	def event_typedCharacter(self,ch):
		super(Display,self).event_typedCharacter(ch)
		if ch in self.calcCommandChars:
			speech.speakObjectProperties(self,value=True)

	def script_executeAndRead(self,gesture):
		gesture.send()
		speech.speakObjectProperties(self,value=True)

for k in Display.calcCommandKeys:
	Display.bindKey(k,"executeAndRead")
