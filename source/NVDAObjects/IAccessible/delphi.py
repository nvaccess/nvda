from NVDAObjects import behaviors
import controlTypes
from . import IAccessible

class TRichView(IAccessible):

	def _get_name(self):
		pass

	def _get_role(self):
		return controlTypes.Role.STATICTEXT

class TRichViewEdit(IAccessible):

	def _get_name(self):
		pass

	def _get_role(self):
		return controlTypes.Role.EDITABLETEXT

class TGroupBox(IAccessible):

	def _get_role(self):
		return controlTypes.Role.GROUPING

class Form(behaviors.Dialog):

	role=controlTypes.Role.DIALOG

class TabSheet(behaviors.Dialog):

	role=controlTypes.Role.PROPERTYPAGE

class TRxRichEdit(IAccessible):

	def _get_name(self):
		return None
