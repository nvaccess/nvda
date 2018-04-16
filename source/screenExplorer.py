#screenExplorer.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2012-2018 NV Access Limited, Joseph Lee
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Module which implements various utilities for screen exploration.
This includes touchscreen movement as well as handling coordinate announcement for mouse and objects.
"""

import api
import tones
import controlTypes
import textInfos
import speech
import screenBitmap
import config
import mouseHandler
import wx

def playLocationCoordinates(x, y, screenWidth, screenHeight, screenMinPos=None, detectBrightness=True,blurFactor=0):
	"""Plays a tone indicating the XY-coordinate for the given location. This works for keyboard-based object navigation/focus movement, mouse movement and during touch hover gesture.  
	@param obj: the coordinate for the location and the screen resolution (typically desktopObject.location)
	@type obj: int
	"""
	# Have a fake wx.Point in case min pos is not defined on multiple monitors.
	if screenMinPos is None:
		screenMinPos = wx.Point()
	# Do not play any tone if offscreen.
	if 0 <= x <= screenWidth or 0 <= y <= screenHeight:
		minPitch=config.conf['mouse']['audioCoordinates_minPitch']
		maxPitch=config.conf['mouse']['audioCoordinates_maxPitch']
		curPitch=minPitch+((maxPitch-minPitch)*((screenHeight-y)/float(screenHeight)))
		if detectBrightness:
			startX=min(max(x-blurFactor,0),screenWidth)+screenMinPos.x
			startY=min(max(y-blurFactor,0),screenHeight)+screenMinPos.y
			width=min(blurFactor+1,screenWidth)
			height=min(blurFactor+1,screenHeight)
			grey=screenBitmap.rgbPixelBrightness(mouseHandler.scrBmpObj.captureImage( startX, startY, width, height)[0][0])
			brightness=grey/255.0
			minBrightness=config.conf['mouse']['audioCoordinates_minVolume']
			maxBrightness=config.conf['mouse']['audioCoordinates_maxVolume']
			brightness=(brightness*(maxBrightness-minBrightness))+minBrightness
		else:
			brightness=config.conf['mouse']['audioCoordinates_maxVolume']
		leftVolume=int((85*((screenWidth-float(x))/screenWidth))*brightness)
		rightVolume=int((85*(float(x)/screenWidth))*brightness)
		tones.beep(curPitch,40,left=leftVolume,right=rightVolume)

def playObjectCoordinates(obj):
	"""Plays the audio coordinate for the object.  
	@param obj: the object for which the coordinates should be played
	@type obj: NVDAObjects.NvDAObject
	"""
	l,t,w,h=obj.location
	x = l+(w/2)
	y = t+(h/2)
	screenWidth, screenHeight = api.getDesktopObject().location[-2:]
	try:
		playLocationCoordinates(x, y, screenWidth, screenHeight, detectBrightness=False)
	except AttributeError:
		pass


class ScreenExplorer(object):

	updateReview=False

	def __init__(self):
		self._obj=None
		self._pos=None

	def moveTo(self,x,y,new=False,unit=textInfos.UNIT_LINE):
		obj=api.getDesktopObject().objectFromPoint(x,y)
		prevObj=None
		while obj  and obj.beTransparentToMouse:
			prevObj=obj
			obj=obj.parent
		if not obj or (obj.presentationType!=obj.presType_content and obj.role!=controlTypes.ROLE_PARAGRAPH):
			obj=prevObj
		if not obj:
			return
		hasNewObj=False
		if obj!=self._obj:
			self._obj=obj
			hasNewObj=True
			if self.updateReview:
				api.setNavigatorObject(obj)
		else:
			obj=self._obj
		pos=None
		if obj.treeInterceptor:
			try:
				pos=obj.treeInterceptor.makeTextInfo(obj)
			except LookupError:
				pos=None
			if pos:
				obj=obj.treeInterceptor.rootNVDAObject
				if hasNewObj and self._obj and obj.treeInterceptor is self._obj.treeInterceptor:
					hasNewObj=False 
		if not pos:
			try:
				pos=obj.makeTextInfo(textInfos.Point(x,y))
			except (NotImplementedError,LookupError):
				pass
			if pos: pos.expand(unit)
		if pos and self.updateReview:
			api.setReviewPosition(pos)
		speechCanceled=False
		if hasNewObj:
			speech.cancelSpeech()
			speechCanceled=True
			speech.speakObject(obj)
		if pos  and (new or not self._pos or pos.__class__!=self._pos.__class__ or pos.compareEndPoints(self._pos,"startToStart")!=0 or pos.compareEndPoints(self._pos,"endToEnd")!=0):
				self._pos=pos
				if not speechCanceled:
					speech.cancelSpeech()
				speech.speakTextInfo(pos,reason=controlTypes.REASON_CARET)
