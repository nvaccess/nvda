# -*- coding: UTF-8 -*-
#brailleDisplayDrivers/handyTech.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2008-2011 Felix Grützmacher <felix.gruetzmacher@handytech.de>, James Teh <jamie@jantrid.net>, Bram Duvigneau <bram@bramd.nl>

import _winreg
import comtypes.client
from comtypes import GUID
import braille
from logHandler import log
import speech
import inputCore
import os
from baseObject import ScriptableObject

COM_CLASS = "HtBrailleDriverServer.HtBrailleDriver"
HT_KEYS = {}

constants = None

class Sink(object):

	def __init__(self, server):
		self.server = server
		super(Sink, self).__init__()

	def sayString(self, text):
		speech.speakMessage(text)

	def onKeysPressed(self, keys_arg, routing_pos):
		# keys_arg is VARIANT. Indexing by 0 gives actual value.
		keys = keys_arg[0]
		if constants.KEY_ROUTING in keys:
			gesture = InputGesture(keys, routing_pos -1)
		else:
			gesture = InputGesture(keys)
		try:
			inputCore.manager.executeGesture(gesture)
		except inputCore.NoInputGestureAction:
			pass

class BrailleDisplayDriver(braille.BrailleDisplayDriver, ScriptableObject):
	"""Handy Tech braille display driver.
	"""
	name = "handyTech"
	# Translators: Names of braille displays.
	description = _("Handy Tech braille displays")

	@classmethod
	def check(cls):
		try:
			GUID.from_progid(COM_CLASS)
			return True
		except WindowsError:
			return False

	def __init__(self):
		global constants, HT_KEYS
		super(BrailleDisplayDriver, self).__init__()
		self._server = comtypes.client.CreateObject(COM_CLASS)
		import comtypes.gen.HTBRAILLEDRIVERSERVERLib as constants

		HT_KEYS = {}
		for key, constant in constants.__dict__.items():
			if key.startswith('KEY_'):
				HT_KEYS[constant] = key[4:].lower().replace('_', '')

		# Keep the connection object so it won't become garbage
		self._advise = comtypes.client.GetEvents(self._server, Sink(self._server), constants.IHtBrailleDriverSink)
		self._server.initialize()

	def terminate(self):
		super(BrailleDisplayDriver, self).terminate()
		self._server.terminate()

	def _get_numCells(self):
		return self._server.getCurrentTextLength()[0]

	def display(self, cells):
		self._server.displayText(cells)

	def script_showConfig(self, gesture):
		self._server.startConfigDialog(False)
	script_showConfig.__doc__ = _("Show the Handy Tech driver configuration window.")

	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"braille_scrollBack": ("br(handytech):left", "br(handytech):up"),
			"braille_previousLine": ("br(handytech):b4",),
			"braille_nextLine": ("br(handytech):b5",),
			"braille_scrollForward": ("br(handytech):right", "br(handytech):down"),
			"braille_routeTo": ("br(handytech):routing",),
			"kb:shift+tab": ("br(handytech):esc",),
			"kb:alt": ("br(handytech):b2+b4+b5",),
			"kb:escape": ("br(handytech):b4+b6",),
			"kb:tab": ("br(handytech):enter",),
			"kb:enter": ("br(handytech):esc+enter",),
			"kb:upArrow": ("br(handytech):leftSpace",),
			"kb:downArrow": ("br(handytech):rightSpace",),
			"showGui": ("br(handytech):b2+b4+b5+b6",),
		}
	})

	__gestures = {
		'br(handytech):b4+b8': 'showConfig',
	}

class InputGesture(braille.BrailleDisplayGesture):

	source = BrailleDisplayDriver.name

	def __init__(self, keys, routing_pos=None):
		super(InputGesture, self).__init__()
		self.keys = set(keys)

		self.keyNames = names = set()
		for key in self.keys:
			if key == constants.KEY_ROUTING:
				names.add("routing")
				self.routingIndex = routing_pos
			else:
				try:
					names.add(HT_KEYS[key])
				except KeyError:
					log.debugWarning("Unknown key %d" % key)

		self.id = "+".join(names)
