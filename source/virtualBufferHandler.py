#virtualBuffers/IAccessible.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import gc
import os
import globalVars
from logHandler import log
import winUser
import NVDAObjects
import NVDAObjects.window
import NVDAObjects.IAccessible
import NVDAObjects.IAccessible.MSHTML
import controlTypes
import NVDAObjects.window
import speech
import config
import nvwave
import IAccessibleHandler

runningTable=set()

def getVirtualBuffer(obj):
	for v in runningTable:
		if v.isNVDAObjectInVirtualBuffer(obj):
			return v

def update(obj):
	#If this object already has a virtualBuffer, just return that and don't bother trying to create one
	v=obj.virtualBuffer
	if v:
		return v
	try:
		newClass=obj.virtualBufferClass
	except NotImplementedError:
		return None
	virtualBufferObject=newClass(obj)
	if not virtualBufferObject.isAlive():
		return None
	if hasattr(virtualBufferObject,'loadBuffer'):
		try:
			virtualBufferObject.loadBuffer()
		except:
			log.error("error loading buffer",exc_info=True)
			return None
	runningTable.add(virtualBufferObject)
	log.debug("Adding new virtualBuffer to runningTable: %s"%virtualBufferObject)
	return virtualBufferObject

def cleanup():
	"""Kills off any virtualBuffers that are no longer alive."""
	for v in list(runningTable):
		if not v.isLoading and not v.isAlive():
			killVirtualBuffer(v)

def killVirtualBuffer(virtualBufferObject):
	try:
		runningTable.remove(virtualBufferObject)
	except KeyError:
		return
	if hasattr(virtualBufferObject,'unloadBuffer'):
		virtualBufferObject.unloadBuffer()

def terminate():
	"""Kills any currently running virtualBuffers"""
	for v in list(runningTable):
		killVirtualBuffer(v)

def reportPassThrough(virtualBuffer):
	"""Reports the virtual buffer pass through mode if it has changed.
	@param virtualBuffer: The current virtual buffer.
	@type virtualBuffer: L{virtualBuffers.VirtualBuffer}
	"""
	if virtualBuffer.passThrough != reportPassThrough.last:
		if config.conf["virtualBuffers"]["passThroughAudioIndication"]:
			sound = r"waves\focusMode.wav" if virtualBuffer.passThrough else r"waves\browseMode.wav"
			nvwave.playWaveFile(sound)
		else:
			speech.speakMessage(_("focus mode") if virtualBuffer.passThrough else _("browse mode"))
		reportPassThrough.last = virtualBuffer.passThrough
reportPassThrough.last = False
