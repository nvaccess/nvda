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
	for v in list(runningTable):
		if not v.isAlive():
			killVirtualBuffer(v)
	windowClassName=obj.windowClassName
	role=obj.role
	states=obj.states
	#Gecko with IAccessible2 support
	if isinstance(obj,NVDAObjects.IAccessible.IAccessible) and isinstance(obj.IAccessibleObject,IAccessibleHandler.IAccessible2) and windowClassName.startswith('Mozilla') and role==controlTypes.ROLE_DOCUMENT:
		if controlTypes.STATE_READONLY in states and controlTypes.STATE_BUSY not in states and windowClassName=="MozillaContentWindowClass":
			classString="virtualBuffers.gecko_ia2.Gecko_ia2"
		else:
			return
	#Adobe documents with IAccessible
 	elif isinstance(obj,NVDAObjects.IAccessible.IAccessible) and windowClassName=="AVL_AVView" and role in (controlTypes.ROLE_DOCUMENT,controlTypes.ROLE_PAGE) and controlTypes.STATE_READONLY in states:
		classString="virtualBuffers.adobeAcrobat.AdobeAcrobat"
	#MSHTML
 	elif isinstance(obj,NVDAObjects.IAccessible.MSHTML.MSHTML) and obj.IHTMLElement and windowClassName=="Internet Explorer_Server" and obj.IHTMLElement.nodeName.lower() in ("body", "frameset") and not obj.isContentEditable:
		classString="virtualBuffers.MSHTML.MSHTML"
	else:
		return
	modString,classString=os.path.splitext(classString)
	classString=classString[1:]
	log.debug("loading module %s, class %s"%(modString,classString))
	mod=__import__(modString,globals(),locals(),[""])
	log.debug("mod contains %s"%dir(mod))
	newClass=getattr(mod,classString)
	log.debug("virtualBuffers.IAccessible.update: adding %s at %s (%s)"%(newClass,obj.windowHandle,obj.windowClassName))
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
	return virtualBufferObject

def killVirtualBuffer(virtualBufferObject):
	try:
		runningTable.remove(virtualBufferObject)
	except KeyError:
		return
	if hasattr(virtualBufferObject,'unloadBuffer'):
		virtualBufferObject.unloadBuffer()

def cleanupVirtualBuffers():
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
