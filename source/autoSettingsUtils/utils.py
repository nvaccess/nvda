
def paramToPercent(current: int, min: int, max: int) -> int:
	"""Convert a raw parameter value to a percentage given the current, minimum and maximum raw values.
	@param current: The current value.
	@type current: int
	@param min: The minimum value.
	@type current: int
	@param max: The maximum value.
	@type max: int
	"""
	return round(float(current - min) / (max - min) * 100)


def percentToParam(percent: int, min: int, max: int) -> int:
	"""Convert a percentage to a raw parameter value given the current percentage and the minimum and maximum raw parameter values.
	@param percent: The current percentage.
	@type percent: int
	@param min: The minimum raw parameter value.
	@type min: int
	@param max: The maximum raw parameter value.
	@type max: int
	"""
	return round(float(percent) / 100 * (max - min) + min)


class UnsupportedConfigParameterError(NotImplementedError):
	"""
	Raised when changing or retrieving a driver setting that is unsupported for the connected device.
	"""

class StringParameterInfo(object):
	"""
	The base class used to represent a value of a string driver setting.
	"""
	id: str
	displayName: str

	def __init__(self, id: str, displayName: str):
		"""
		@param id: The unique identifier of the value.
		@param displayName: The name of the value, visible to the user.
		"""
		self.id = id
		self.displayName = displayName
