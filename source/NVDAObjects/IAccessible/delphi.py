from NVDAObjects import behaviors
import controlTypes
from . import IAccessible

class TRichView(IAccessible):

	def _get_name(self):
		pass

	def _get_role(self):
		return controlTypes.ROLE_STATICTEXT

class TRichViewEdit(IAccessible):

	def _get_name(self):
		pass

	def _get_role(self):
		return controlTypes.ROLE_EDITABLETEXT

class TGroupBox(IAccessible):

	def _get_role(self):
		return controlTypes.ROLE_GROUPING

class Form(behaviors.Dialog):

	role=controlTypes.ROLE_DIALOG

class TabSheet(behaviors.Dialog):

	role=controlTypes.ROLE_PROPERTYPAGE

class TRxRichEdit(IAccessible):

	def _get_name(self):
		return None
