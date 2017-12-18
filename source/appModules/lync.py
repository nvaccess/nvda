#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017 NV Access Limited

"""appModule for Microsoft Skype for business. """
 
import ui
from NVDAObjects.UIA import UIA
import appModuleHandler

class NetUIRicherLabel(UIA):
	"""A label sometimes found within list items that can fire live region changes, such as for chat messages."""

	def event_liveRegionChange(self):
		# The base liveRegionChange event is not enough as Skype for Business concatinates recent chat messages from the same person within the same minute
		# Therefore, specifically strip out the chat content and only report the most recent part added.
		# The object's name contains the full message (I.e. person: content, timestamp) loosely separated by commas.
		# Example string: "Michael Curran : , , Hello\r\n\r\nThis is a test , 10:45 am."
		# Where person is "Michael Curran", content is "Hello\nThis is a test" and timestamp is "10:45 am" 
		# The object's value just contains the content.
		# Example: "Hello\rThis is a test"
		# We are only interested in person and content
		# Therefore use value (content) to  locate and split off the person from the name (fullText)
		# Normalize the usage of end-of-line characters (name and value seem to expose them differently, which would break comparison)
		content=self.value.replace('\r','\n').strip()
		fullText=self.name.replace('\r\n\r\n','\n')
		contentLines=content.split('\n')
		contentStartIndex=fullText.find(content)
		pretext=fullText[:contentStartIndex]
		# There are some annoying comma characters  after the person's name 
		pretext=pretext.replace(' ,','')
		# If the objects are the same, the person is the same, and the new content is the old content but with more appended, report the appended content
		# Otherwise, report the person and the initial content
		runtimeID=self.UIAElement.getRuntimeId()
		lastRuntimeID,lastPretext,lastContentLines=self.appModule._lastLiveChatMessageData
		contentLinesLen=len(contentLines)
		lastContentLinesLen=len(lastContentLines)
		if runtimeID==lastRuntimeID and pretext==lastPretext and contentLinesLen>lastContentLinesLen and contentLines[:lastContentLinesLen]==lastContentLines:
			message="\n".join(contentLines[lastContentLinesLen:])
		else:
			message=pretext+content
		ui.message(message)
		# Cache the message data for later possible comparisons 
		self.appModule._lastLiveChatMessageData=runtimeID,pretext,contentLines

class AppModule(appModuleHandler.AppModule):

	# data to store the last chat message (runtime ID,person,content lines)
	_lastLiveChatMessageData=[],"",[]

	def chooseNVDAObjectOverlayClasses(self,obj,clsList):
		if isinstance(obj,UIA) and obj.UIAElement.cachedClassName=='NetUIRicherLabel':
			clsList.insert(0,NetUIRicherLabel)
		return clsList

