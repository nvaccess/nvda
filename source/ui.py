#ui.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""User interface functionality.
This refers to the user interface presented by the screen reader alone, not the graphical user interface.
See L{gui} for the graphical user interface.
"""

import speech
import braille

def message(text):
	"""Present a message to the user.
	The message will be presented in both speech and braille.
	@param text: The text of the message.
	@type text: str
	"""
	speech.speakMessage(text)
	braille.handler.message(text)
