# -*- coding: UTF-8 -*-
#synthDrivers/sapi5.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2016 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import comtypes.client
from comtypes import COMError
import sapi5

class SynthDriver(sapi5.SynthDriver):

	name="sapiMobile"
	description="Microsoft Speech Mobile"
	testVoiceOnInit=True
	voiceTokenRegKey='HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices'

	@classmethod
	def check(cls):
		try:
			tokens=cls._getVoiceTokens()
		except COMError:
			return False
		return len(tokens)>0

	def __init__(self):
		tokens=self._getVoiceTokens()
		for x in xrange(len(tokens)):
			token=tokens[x]
			try:
				super(SynthDriver,self).__init__(token)
				break
			except COMError:
				continue
		else:
			raise RuntimeError("No available voices")

	@classmethod
	def _getVoiceTokens(cls):
		cat=comtypes.client.CreateObject('sapi.spObjectTokenCategory')
		cat.SetID(cls.voiceTokenRegKey,False)
		return cat.EnumerateTokens()
