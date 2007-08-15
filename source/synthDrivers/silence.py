import os
import baseObject
import debug

#The 'silent' synth driver
#Used both as a template for all other synth drivers
#And can be used to disable speech in NVDA

#Each synth driver is its own python module containing a 'SynthDriver' class.

class SynthDriver(baseObject.autoPropertyObject):

	hasVoice=False
	hasPitch=False
	hasRate=False
	hasVolume=False
	hasVariant=False
	hasInflection=False

	#A description of the synth
	description=_("No speech,  a template synthesizer")
	#The name must be the original module file name
	name="silence"

	#A method to find out whether this synth is actually supported
	#Return true for yes and False for no
	def check(self):
		return True

	#The method to start the driver
	#Must return True on success and False otherwise 
	def initialize(self):
		return True

	#A method to terminate the driver
	def terminate(self):
		pass

	#A method to speak some given text
	#It must take a string of text, plus two optional parameters: wait and index.
	#wait: if True then this method must block until done speaking
	#index: a bookmark must be set to this value for the text that is given.
	#the lastIndex property should be set to this value at the exact time the synth is speaking the text
	def speakText(self,text,wait=False,index=None):
		pass

	#The property for finding out the last index spoken
	#Each time the synth speaks text related to a index (bookmark) this property must be updated
	#This is used for reading large passages of text where the cursor position must be updated while reading
	#Its safe to return None if there is no index
	def _get_lastIndex(self):
		return None
 
	#A method to shut up the speech quickly
	def cancel(self):
		pass

	#Property to get and set the voice
	#voices are represented to NVDA as a number greater or equal to 1
	def _get_voice(self):
		return 1

	def _set_voice(self,value):
		pass

	#A property to find out the total number of voices
	def _get_voiceCount(self):
		return 1

	#Method to get the name of a given voice number
	def getVoiceName(self,num):
		return "silent voice"

	#Properties to get and set rate, pitch and volume
	#They must accept values between 0 and 100, and be able to report values between 0 and 100

	def _get_rate(self):
		return 0

	def _set_rate(self,value):
		pass

	def _get_pitch(self):
		return 0

	def _set_pitch(self,value):
		pass

	def _get_volume(self):
		return 0

	def _set_volume(self,value):
		pass

	def _get_variant(self):
		return 1

	def _set_variant(self,val):
		pass

	def _get_variantCount(self):
		return 1

	def _get_inflection(self):
		return 0

	def _set_inflection(self,val):
		pass

	def pause(self,switch):
		pass
