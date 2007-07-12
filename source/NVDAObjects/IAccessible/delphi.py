import controlTypes
import edit

class TRichView(edit.Edit):

	def _get_name(self):
		pass

	def _get_role(self):
		return controlTypes.ROLE_STATICTEXT

[TRichView.bindKey(keyName,scriptName) for keyName,scriptName in [
	("extendedDown","review_nextLine"),
	("extendedUp","review_previousLine"),
	("extendedLeft","review_previousCharacter"),
	("extendedRight","review_nextCharacter"),
	("extendedHome","review_startOfLine"),
	("extendedEnd","review_endOfLine"),
	("control+extendedLeft","review_previousWord"),
	("control+extendedRight","review_nextWord"),
	("control+extendedHome","review_top"),
	("control+extendedEnd","review_bottom"),
]]

class TRichViewEdit(edit.Edit):

	def _get_name(self):
		pass

	def _get_role(self):
		return controlTypes.ROLE_EDITABLETEXT
