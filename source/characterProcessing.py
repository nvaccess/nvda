#characterProcessing.py
#A part of NonVisual Desktop Access (NVDA)
#URL: http://www.nvda-project.org/
#Copyright (c) 2010-2011 World Light Information Limited and Hong Kong Blind Union.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

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
	return %s - %c description"%(locale,character)
 