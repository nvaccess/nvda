#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2015 Dinesh Kaushal, NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""unicodeScriptPrep module is used to build unicodeScriptData.py file. This module obtains scripts.txt from unicode.org and builds an array of unicode ranges. 
After  the array is created, it is written to the unicodeScriptData.py module.
To generate the unicodeScriptData.py, just run this script with python."""

import urllib2, re, textwrap

def generateUnicodeScriptData():
	"""build unicodeScriptData.py from scripts.txt"""
	unicodeRange= []
	url = 'http://www.unicode.org/Public/UNIDATA/Scripts.txt'
	scriptDataFile = urllib2.urlopen(url)
	for line in scriptDataFile:
		p = re.findall(r'([0-9A-F]+)(?:\.\.([0-9A-F]+))?\W+(\w+)\s*#\s*(\w+)', line)
		if p:
			a, b, name, cat = p[0]
			unicodeRange.append((int(a, 16), int(b or a, 16), name  ))
	unicodeRange.sort()
	#merge multiple adjacent ranges 
	unicodeRange = normalize(unicodeRange )
	#write the data to unicodeScriptData.txt
	file = open("unicodeScriptData.py","w")
	file.write ('\nscriptCode= [\n%s\n]\n' % ('\n'.join('\t( 0X%x , 0X%x , "%s" ), ' % c for c in unicodeRange) ) )
	file.close()

def normalize(unicodeRanges):
	"""merge adjacent ranges
	@param unicodeRanges: A list of unicode ranges with adjacent ranges that are not merged
	@type unicodeRanges: list
	@return: adjacent unicode ranges that are merged 
	@rtype: list"""
	normalizedRange= []
	lastRecord = unicodeRanges[0] 
	for index in xrange(1, len( unicodeRanges) ) :
		if lastRecord: 
			tempRecord = unicodeRanges[index] 
			if lastRecord[2] == tempRecord[2] and (lastRecord[1] + 1) == tempRecord[0]: 
				lastRecord = lastRecord[0] , tempRecord[1] , tempRecord[2] 
			else:
				normalizedRange.append(lastRecord) 
				lastRecord = tempRecord
	return normalizedRange

generateUnicodeScriptData()
