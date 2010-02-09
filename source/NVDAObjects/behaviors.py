#NVDAObjects/behaviors.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2010 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Mix-in classes which provide common behaviour for particular types of controls across different APIs.
"""

import tones
import api
import queueHandler
import controlTypes
import globalVars
import speech
import config
from . import NVDAObject, NVDAObjectTextInfo
import textInfos

class ProgressBar(NVDAObject):

	progressValueCache={} #key is made of "speech" or "beep" and an x,y coordinate, value is the last percentage
 
	def event_valueChange(self):
		pbConf=config.conf["presentation"]["progressBarUpdates"]
		states=self.states
		if pbConf["progressBarOutputMode"]=="off" or controlTypes.STATE_INVISIBLE in states or controlTypes.STATE_OFFSCREEN in states:
			return super(ProgressBar,self).event_valueChange()
		val=self.value
		if val:
			val=val.rstrip('%\x00')
		if not val:
			return super(ProgressBar,self).event_valueChange()
		percentage = min(max(0.0, float(val)), 100.0)
		if not pbConf["reportBackgroundProgressBars"] and not self.isInForeground:
			return
		try:
			left,top,width,height=self.location
		except:
			left=top=width=height=0
		x=left+(width/2)
		y=top+(height/2)
		lastBeepProgressValue=self.progressValueCache.get("beep,%d,%d"%(x,y),None)
		if pbConf["progressBarOutputMode"] in ("beep","both") and (lastBeepProgressValue is None or abs(percentage-lastBeepProgressValue)>=pbConf["beepPercentageInterval"]):
			tones.beep(pbConf["beepMinHZ"]*2**(percentage/25.0),40)
			self.progressValueCache["beep,%d,%d"%(x,y)]=percentage
		lastSpeechProgressValue=self.progressValueCache.get("speech,%d,%d"%(x,y),None)
		if pbConf["progressBarOutputMode"] in ("speak","both") and (lastSpeechProgressValue is None or abs(percentage-lastSpeechProgressValue)>=pbConf["speechPercentageInterval"]):
			queueHandler.queueFunction(queueHandler.eventQueue,speech.speakMessage,_("%d percent")%percentage)
			self.progressValueCache["speech,%d,%d"%(x,y)]=percentage

class Dialog(NVDAObject):
	"""Overrides the description property to obtain dialog text.
	"""

	@classmethod
	def getDialogText(cls,obj):
		"""This classmethod walks through the children of the given object, and collects up and returns any text that seems to be  part of a dialog's message text.
		@param obj: the object who's children you want to collect the text from
		@type obj: L{IAccessible}
		"""
		children=obj.children
		textList=[]
		childCount=len(children)
		for index in xrange(childCount):
			child=children[index]
			childStates=child.states
			childRole=child.role
			#We don't want to handle invisible or unavailable objects
			if controlTypes.STATE_INVISIBLE in childStates or controlTypes.STATE_UNAVAILABLE in childStates: 
				continue
			#For particular objects, we want to descend in to them and get their children's message text
			if childRole in (controlTypes.ROLE_PROPERTYPAGE,controlTypes.ROLE_PANE,controlTypes.ROLE_PANEL,controlTypes.ROLE_WINDOW):
				textList.append(cls.getDialogText(child))
				continue
			# We only want text from certain controls.
			if not (
				 # Static text, labels and links
				 childRole in (controlTypes.ROLE_STATICTEXT,controlTypes.ROLE_LABEL,controlTypes.ROLE_LINK)
				# Read-only, non-multiline edit fields
				or (childRole==controlTypes.ROLE_EDITABLETEXT and controlTypes.STATE_READONLY in childStates and controlTypes.STATE_MULTILINE not in childStates)
			):
				continue
			#We should ignore a text object directly after a grouping object, as it's probably the grouping's description
			if index>0 and children[index-1].role==controlTypes.ROLE_GROUPING:
				continue
			#Like the last one, but a graphic might be before the grouping's description
			if index>1 and children[index-1].role==controlTypes.ROLE_GRAPHIC and children[index-2].role==controlTypes.ROLE_GROUPING:
				continue
			childName=child.name
			#Ignore objects that have another object directly after them with the same name, as this object is probably just a label for that object.
			#However, graphics, static text, separators and Windows are ok.
			if childName and index<(childCount-1) and children[index+1].role not in (controlTypes.ROLE_GRAPHIC,controlTypes.ROLE_STATICTEXT,controlTypes.ROLE_SEPARATOR,controlTypes.ROLE_WINDOW) and children[index+1].name==childName:
				continue
			childText=child.makeTextInfo(textInfos.POSITION_ALL).text
			if not childText or childText.isspace() and child.TextInfo!=NVDAObjectTextInfo:
				childText=child.basicText
			textList.append(childText)
		return " ".join(textList)

	def _get_description(self):
		return self.getDialogText(self)

	value = None
