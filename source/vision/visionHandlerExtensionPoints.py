#vision/visionHandlerExtensionPoints.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

from extensionPoints import Action

class EventExtensionPoints:
	post_focusChange = None
	post_foregroundChange = None
	post_caretMove = None
	post_browseModeMove = None
	post_reviewMove = None
	post_mouseMove = None

	def __init__(self):
		self.post_focusChange = Action()
		self.post_foregroundChange = Action()
		self.post_caretMove = Action()
		self.post_browseModeMove = Action()
		self.post_reviewMove = Action()
		self.post_mouseMove = Action()
