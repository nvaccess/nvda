#tests/unit/brailleDisplayProvider.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018 NV Access Limited, Babbage B.V.

"""Provider for fake braille displays, braille display/input gestures and fake initialization of built-in drivers.
"""

import braille
import brailleInput
import inputCore
import brailleDisplayDrivers.noBraille
from contextlib import contextmanager
from baseObject import ScriptableObject

class BrailleDisplayDriver(brailleDisplayDrivers.noBraille.BrailleDisplayDriver):
	"""A dummy braille display driver based on L{brailleDisplayDrivers.noBraille.BrailleDisplayDriver}.
	Its gesture map is based on L{brailleDisplayDrivers.alva.BrailleDisplayDrivers.gestureMap}
	"""
	numCells = 40

	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"kb:control": ("br(noBraille):fakeControl",),
			"kb:alt": ("br(noBraille):fakeAlt",),
			"kb:shift": ("br(noBraille):fakeShift",),
			"kb:escape": ("br(noBraille):fakeEscape",),
			"kb:tab": ("br(noBraille):fakeTab",),
			"kb:upArrow": ("br(noBraille):fakeUp",),
			"kb:downArrow": ("br(noBraille):fakeDown",),
			"kb:leftArrow": ("br(noBraille):fakeLeft",),
			"kb:rightArrow": ("br(noBraille):fakeRight",),
			"kb:enter": ("br(noBraille):fakeEnter",),
			"kb:windows+d": ("br(noBraille):fakeControl+fakeTab",),
			"kb:windows+b": ("br(noBraille):fakeEscape+fakeTab",),
			"kb:windows": ("br(noBraille):fakeAlt+fakeEscape",),
			"kb:alt+tab": ("br(noBraille):fakeAlt+fakeTab",),
			"kb:control+home": ("br(noBraille):fakeShift+fakeUp",),
			"kb:control+end": ("br(noBraille):fakeShift+fakeDown",),
			"kb:home": ("br(noBraille):fakeShift+fakeLeft",),
			"kb:end": ("br(noBraille):fakeShift+fakeRight",),
		}
	})

class InputGesture(braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture):

	def __init__(self, source, model, keys, brailleInput=False):
		super(InputGesture, self).__init__()
		self.source = source
		self.model = model
		self.keyNames = names = []
		dots = 0
		space = False
		for key in keys:
			names.append(key)

			# Braille input
			if brailleInput:
				# Fake input keys look like "fakeInput1" for dot 1
				if key.startswith("fakeInput"):
					if key.endswith("Space"):
						space = True
					else:
						dots |= 1 << int(key[-1])
				else:
					brailleInput = False

	def _get_id(self):
		"""Magic property to allow l{self.keyNames} manipulation after construction."""
		return "+".join(self.keyNames)

def activateDummyDisplayDriver():
	"""Activates the dummy braille display driver."""
	braille.handler.display = BrailleDisplayDriver()
	braille.handler.displaySize = BrailleDisplayDriver.numCells
	braille.handler.enabled = True

@contextmanager
def fakeInitializedDisplayDriver(driver):
	"""A context manager that does the following:
		* It sets the current braille display driver on the braille handler to a built-in driver, without initializing it.
		* It executes a desired piece of code.
		* It resets the braille handler to the dummy driver.
	This context manager should be used to test braille display gesture maps,
	as the scriptHandler only queries the gesture map of the active display.
	Braille output will be ignored.
	"""
	braille.handler.display = driver.__new__(driver)
	if issubclass(driver, ScriptableObject):
		# Initialize the scriptable part of the display driver.
		ScriptableObject.__init__(braille.handler.display)
	# The cell count is unimportant, there just ought to be some cells.
	braille.handler.displaySize = BrailleDisplayDriver.numCells
	braille.handler.display.display = lambda cells: None
	braille.handler.enabled = True
	yield
	activateDummyDisplayDriver()
