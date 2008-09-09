import braille
try:
	import brlapi
except ImportError:
	pass

class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	"""brltty braille display driver.
	"""
	name = "brltty"

	@classmethod
	def check(cls):
		try:
			c = brlapi.Connection()
			del c
			return True
		except:
			pass
		return False

	def __init__(self):
		self._con = brlapi.Connection()
		self._con.enterTtyModeWithPath()

	def __del__(self):
		self._con.leaveTtyMode()
		self._con = None

	def _get_numCells(self):
		return self._con.displaySize[0]

	def display(self, cells):
		self._cells = cells
		self._display()

	def _display(self):
		# The string sent to the display needs to be the length of the display, so pad with zeroes if necessary.
		out = "".join(chr(cell) for cell in self._cells) + "\0" * (self.numCells - len(self._cells))
		self._con.writeDots(out)
