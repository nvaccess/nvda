
def paramToPercent(current, min, max):
	"""Convert a raw parameter value to a percentage given the current, minimum and maximum raw values.
	@param current: The current value.
	@type current: int
	@param min: The minimum value.
	@type current: int
	@param max: The maximum value.
	@type max: int
	"""
	return int(round(float(current - min) / (max - min) * 100))


def percentToParam(percent, min, max):
	"""Convert a percentage to a raw parameter value given the current percentage and the minimum and maximum raw parameter values.
	@param percent: The current percentage.
	@type percent: int
	@param min: The minimum raw parameter value.
	@type min: int
	@param max: The maximum raw parameter value.
	@type max: int
	"""
	return int(round(float(percent) / 100 * (max - min) + min))


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
