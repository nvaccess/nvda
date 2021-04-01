# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
from braille import BrailleDisplayGesture

driverName = "brailleViewer"


class BrailleViewerGesture_RouteTo(BrailleDisplayGesture):
	source = driverName
	id = "route"

	def __init__(self, argument):
		super().__init__()
		self.routingIndex = argument
		import globalCommands
		self.script = globalCommands.commands.script_braille_routeTo
