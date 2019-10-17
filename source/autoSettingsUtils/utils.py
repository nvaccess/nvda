
class UnsupportedConfigParameterError(NotImplementedError):
	"""
	Raised when changing or retrieving a driver setting that is unsupported for the connected device.
	"""

class StringParameterInfo(object):
	"""
	The base class used to represent a value of a string driver setting.
	"""

	def __init__(self, id, displayName):
		"""
		@param id: The unique identifier of the value.
		@type id: str
		@param displayName: The name of the value, visible to the user.
		@type displayName: str
		"""
		self.id = id
		self.displayName = displayName
		# Keep backwards compatibility
		self.ID = id
		self.name = displayName
