#NVDAObjects/progressBar.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2009 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import tones
import api
import queueHandler
import controlTypes
import globalVars
import speech
import config
from . import NVDAObject

class ProgressBar(NVDAObject):

	progressValueCache={} #key is made of "speech" or "beep" and an x,y coordinate, value is the last percentage
 
	def event_valueChange(self):
		pbConf=config.conf["presentation"]["progressBarUpdates"]
		if pbConf["progressBarOutputMode"]=="off" or controlTypes.STATE_INVISIBLE in self.states:
			return super(ProgressBar,self).event_valueChange()
		val=self.value
		if val:
			val=val.rstrip('%\x00')
		if not val:
			return super(ProgressBar,self).event_valueChange()
		percentage = min(max(0.0, float(val)), 100.0)
		left,top,width,height=self.location
		x=left+width/2
		y=top+height/2
		screenObj=api.getDesktopObject().objectFromPoint(x,y)
		if not pbConf["reportBackgroundProgressBars"] and self!=screenObj: 
			return
		lastBeepProgressValue=self.progressValueCache.get("beep,%d,%d"%(x,y),None)
		if pbConf["progressBarOutputMode"] in ("beep","both") and (lastBeepProgressValue is None or abs(percentage-lastBeepProgressValue)>=pbConf["beepPercentageInterval"]):
			tones.beep(pbConf["beepMinHZ"]*2**(percentage/25.0),40)
			self.progressValueCache["beep,%d,%d"%(x,y)]=percentage
		lastSpeechProgressValue=self.progressValueCache.get("speech,%d,%d"%(x,y),None)
		if pbConf["progressBarOutputMode"] in ("speak","both") and (lastSpeechProgressValue is None or abs(percentage-lastSpeechProgressValue)>=pbConf["speechPercentageInterval"]):
			queueHandler.queueFunction(queueHandler.eventQueue,speech.speakMessage,_("%d percent")%percentage)
			self.progressValueCache["speech,%d,%d"%(x,y)]=percentage
