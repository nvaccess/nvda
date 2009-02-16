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

class TFormOptions(IAccessible):

	def _get_role(self):
		return controlTypes.ROLE_DIALOG

class TTabSheet(IAccessible):

	def _get_role(self):
		return controlTypes.ROLE_PROPERTYPAGE

class TRxRichEdit(IAccessible):

	def _get_name(self):
		return None

