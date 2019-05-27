#vision/visionHandlerExtensionPoints.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

from extensionPoints import Action

class VisionHandlerExtensionPoints:
	post_focusChange = None
	post_caretMove = None
	post_reviewMove = None

def __init__(self):
	post_focusChange = Action()
	post_caretMove = Action()
	post_reviewMove = Action()
