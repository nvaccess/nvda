import braille

class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	"""A dummy braille display driver used to disable braille in NVDA.
	"""
	name = "noBraille"
	description = _("No braille")

	@classmethod
	def check(cls):
		return True
