#characterProcessing.py
#A part of NonVisual Desktop Access (NVDA)
#URL: http://www.nvda-project.org/
#Copyright (c) 2010-2011 World Light Information Limited and Hong Kong Blind Union.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import time
import os
import codecs
from logHandler import log

class LocaleDataMap(object):
	"""Allows access to locale-specific data objects, dynamically loading them if needed on request"""

	def __init__(self,localeDataClass):
		"""
		@param localeDataClass: this class will be used to instanciate data objects representing the requested locale.
		""" 
		self._localeDataClass=localeDataClass
		self._dataMap={}

	def fetchLocaleData(self,locale):
		"""
		Fetches a data object for the given locale. 
		This may mean that the data object is first created and sotred if it does not yet exist in the map.
		The locale is also simplified (country is dropped) if the full locale can not be used to instanciate a data object.
		@param locale: the locale of the data object requested
		@type locale: string
		@return: the data object for the given locale
		"""
		localeList=[locale]
		if '_' in locale:
			localeList.append(locale.split('_')[0])
		for l in localeList:
			data=self._dataMap.get(l)
			if data: return data
			try:
				data=self._localeDataClass(l)
			except LookupError:
				data=None
			if not data: continue
			self._dataMap[l]=data
			return data
		raise LookupError(locale)

class CharacterDescriptions(object):
	"""
	Represents a map of characters to one or more descriptions (examples) for that character.
	The data is loaded from a file from the requested locale.
	"""

	def __init__(self,locale):
		"""
		@param locale: The characterDescriptions.dic file will be found by using this locale.
		@type locale: string
		"""
		self._entries = {}
		fileName=os.path.join('locale',locale,'characterDescriptions.dic')
		if not os.path.isfile(fileName): 
			raise LookupError(fileName)
		f = codecs.open(fileName,"r","utf_8_sig",errors="replace")
		for line in f:
			if line.isspace() or line.startswith('#'):
				continue
			line=line.rstrip('\r\n')
			temp=line.split("\t")
			if len(temp) > 1:
				key=temp.pop(0)
				self._entries[key] = temp
			else:
				log.warning("can't parse line '%s'" % line)
		log.debug("Loaded %d entries." % len(self._entries))
		f.close()

	def getCharacterDescription(self, character):
		"""
		Looks up the given character and returns a string containing all the descriptions found.
		"""
		desc=self._entries.get(character)
		if not desc: return None
		return u"\u3002".join(desc)

_charDescLocaleDataMap=LocaleDataMap(CharacterDescriptions)

def getCharacterDescription(locale,character):
	"""
	Finds a description or example for the given character, which makes sence in the given locale.
	@param locale: the locale (language[_COUNTRY]) the description should be for.
	@type locale: string
	@param character: the character  who's description should be retreaved.
	@type character: string
	@return:  the found description for the given character
	@rtype: string
	"""
	l=_charDescLocaleDataMap.fetchLocaleData(locale)
	desc=l.getCharacterDescription(character)
	return desc
 