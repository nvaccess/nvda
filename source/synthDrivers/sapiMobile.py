# -*- coding: UTF-8 -*-
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2016 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import _winreg
import os
import comtypes.client
from comtypes import COMError
from logHandler import log
import sapi5

class SynthDriver(sapi5.SynthDriver):

	name="sapiMobile"
	description="Microsoft Speech Mobile"
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
		tokens=[]
		for token in cat.EnumerateTokens():
			ID=token.ID
			IDParts=ID.split('\\')
			rootKey=getattr(_winreg,IDParts[0])
			subkey="\\".join(IDParts[1:])
			try:
				hkey=_winreg.OpenKey(rootKey,subkey)
			except WindowsError as e:
				log.debugWarning("Could not open registry key %s, %s"%(ID,e))
				continue
			try:
				langDataPath=_winreg.QueryValueEx(hkey,'langDataPath')
			except WindowsError as e:
				log.debugWarning("Could not open registry value 'langDataPath', %s"%e)
				continue
			if not langDataPath or not isinstance(langDataPath[0],basestring):
				log.debugWarning("Invalid langDataPath value")
				continue
			if not os.path.isfile(os.path.expandvars(langDataPath[0])):
				log.debugWarning("Missing language data file: %s"%langDataPath[0])
				continue
			try:
				voicePath=_winreg.QueryValueEx(hkey,'voicePath')
			except WindowsError as e:
				log.debugWarning("Could not open registry value 'langDataPath', %s"%e)
				continue
			if not voicePath or not isinstance(voicePath[0],basestring):
				log.debugWarning("Invalid voicePath value")
				continue
			if not os.path.isfile(os.path.expandvars(voicePath[0]+'.apm')):
				log.debugWarning("Missing voice file: %s"%voicePath[0]+".apm")
				continue
			tokens.append(token)
		return tokens

