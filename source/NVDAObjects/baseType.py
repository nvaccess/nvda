#NVDAObjects/baseType.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Module that contains the base NVDA object type"""
import autoPropertyType
from keyboardHandler import key, keyName, sendKey
import audio
import globalVars
import api
import config

class NVDAObject(object):
	"""
The baseType NVDA object. All other NVDA objects are based on this one.
@ivar _hashLimit: The limit in size for a hash of this object
@type _hashLimit: int
@ivar _hashPrime: the prime number used in calculating this object's hash
@type _hashPrime: int
@ivar _keyMap: A dictionary that stores key:method  key to script mappings. Do not change this directly, use L{getScript}, L{executeScript}, L{registerScriptKey} or L{registerScriptKeys} instead.
@type _keyMap: dict
@ivar name: The objects name or label. (e.g. the text of a list item, label of a button)
@type name: string
@ivar value: the object's value. (e.g. content of an edit field, percentage on a progresss bar)
@type value: string
@ivar role: The object's chosen role. (NVDA uses the set of IAccessible role constants for roles, however sometimes if there is no suitable role, this can be a string)
@type role: int or string
@ivar typeString: The object's friendly type. (e.g. a link will have a link role, but its typeString may be 'visited link' depending on its states etc). This type can be anything, it is only communicated to the user, never used programatically.
@type typeString: string 
@ivar states: The object's states. (NVDA uses IAccessible state constants for its states, bitwised grouped together)
@type states: int
@ivar allowedPositiveStates: a bitwise group of states that are allowed to be reported when on
@type allowedPositiveStates: int
@ivar allowedNegativeStates: a bitwise group of states that are allowed to be reported when off
@type allowedNegativeStates: int
@ivar description: The object's description. (e.g. Further info to describe the button's action to go with the label) 
@type description: string
@ivar positionString: a description of where the object is in relation to other objects around it. (e.g. a list item might say 2 of 5).
@type positionString: string
@ivar level: the object's level. Example: a tree view item has a level of 5
@type level: int
@ivar contains: a description of the object's content. Example: a tree view item contains '4 items'
@type contains: string
@ivar location: The object's location. (A tuple of left, top, width, depth).
@type location: 4-tuple (int)
@ivar next: gets the next logical NVDA object in the tree
@type next: L{NVDAObject}
@ivar previous: gets the previous logical NVDA object in the tree
@type previous: L{NVDAObject}
@ivar parent: gets the parent NVDA object to this one in the tree 
@type parent: L{NVDAObject}
@ivar firstChild: gets the first child NVDA object to this one in the tree 
@type firstChild: L{NVDAObject}
@ivar children: gets a list of child NVDA objects directly under this one in the tree
@type children: list of L{NVDAObject}
@ivar childCount: The number of child NVDA objects under this one in the tree
@type childCount: int
@ivar speakOnGainFocus: If true, the object will speak when it gains focus, if false it will not.
@type speakOnGainFocus: boolean
@ivar needsFocusState: If true the object will only react to gainFocus events if its focus state is set at the time.
@type needsFocusState: boolean
@ivar speakOnForeground: if true, this object is spoken if it becomes the current foreground object
@type speakOnForeground: boolean
@ivar hasFocus: if true then the object believes it has focus
@type hasFocus: boolean 
@ivar isProtected: if true then this object should be treeted like a password field.
@type isProtected: boolean 
@ivar text_caretOffset: the caret position in this object's text as an offset from 0
@type text_caretOffset: int
@ivar text_reviewOffset: the review cursor's position in the object's text as an offset from 0
@type text_reviewOffset: int
@ivar text_characterCount: the number of characters in this object's text
@type text_characterCount: int
@ivar _text_lastReportedPresentation: a dictionary to store all the last reported attribute values such as font, page number, table position etc.
@type _text_lastReportedPresentation: dict
"""

	__metaclass__=autoPropertyType.autoPropertyType

	allowedPositiveStates=0
	allowedNegativeStates=0

	def __init__(self,*args):
		self._oldValue=None
		self._oldName=None
		self._oldDescription=None
		self._reviewOffset=0
		self._keyMap={}
		self.speakOnGainFocus=True
		self.needsFocusState=True
		self.speakOnForeground=True
		self._text_lastReportedPresentation={}
		self.text_reviewOffset=0
		self._hashLimit=10000000
		self._hashPrime=17

	def __hash__(self):
		l=self._hashLimit
		p=self._hashPrime
		h=0
		h=(h+(hash(self.__class__.__name__)*p))%l
		h=(h+(hash(self.role)*p))%l
		h=(h+(hash(self.description)*p))%l
		h=(h+(hash(self.keyboardShortcut)*p))%l
		location=self.location
		if location and (len(location)==4):
			(left,top,width,height)=location
			h=(h+(hash(left)*p))%l
			h=(h+(hash(top)*p))%l
			h=(h+(hash(width)*p))%l
			h=(h+(hash(height)*p))%l
		return h

	def __eq__(self,other):
		if hash(self)==hash(other):
			return True
		else:
			return False

	def __ne__(self,other):
		if hash(self)!=hash(other):
			return True
		else:
			return False

	def getScript(self,keyPress):
		"""
Returns a script (instance method) if one is assigned to the keyPress given.
@param keyPress: The key you wish to retreave the script for
@type keyPress: key
""" 
		if self._keyMap.has_key(keyPress):
			return self._keyMap[keyPress]

	def executeScript(self,keyPress):
		"""
executes a script (instance method) if one is assigned to the keyPress given.
@param keyPress: The key you wish to execute the script for
@type keyPress: key
""" 
		script=self.getScript(keyPress)
		script(keyPress)

	def registerScriptKey(self,keyPress,func):
		"""
Registers the given script (instance method) along with the given keyPress internally so that this method can be executed by the keyPress.
@param keyPress: The chosen key to link the method with
@type keyPress: key
@param func: The method you want to register
@type func: instance method
"""
		self._keyMap[keyPress]=func

	def registerScriptKeys(self,keyDict):
		"""
Registers a number of methods with their respective keys so that these methods can be later executed by the keys.
@param dict: A dictionary of keyPress:method paires.
@type dict: dictionary
"""
		self._keyMap.update(keyDict)

	def _get_name(self):
		return ""

	def _get_role(self):
		return "NVDA object"

	def _get_typeString(self):
		return _("role %s")%self.role

	def _get_value(self):
		return ""

	def _get_description(self):
		return ""

	def _get_keyboardShortcut(self):
		return ""

	def _get_states(self):
		return 0

	def calculatePositiveStates(self):
		"""
Filters the states property, only allowing certain positive states.
"""
		return self.states&self.allowedPositiveStates

	def calculateNegativeStates(self):
		"""
Filters the states property, only allowing certain positive states.
"""
		return (~self.states)&self.allowedNegativeStates

	def getStateName(self,state,opposite=False):
		"""
Returns a name for a given state. Takes in to account if opposite is true or not.
@param state: IAccessible state constant
@type state: int
@param opposite: True if the state is negative, or false if the state is positive, default is False
@type opposite: boolean
"""
		text=_("state %s")%state
		if opposite:
			text=_("not %s")%text
		return text

	def getStateNames(self,states,opposite=False):
		"""
Returns a string of names for a given bitwise group of states. Takes in to account if opposite is true or not.
@param states: bitwise group of IAccessible state constants
@type state: int
@param opposite: True if the states are negative, or false if the states are positive, default is False
@type opposite: boolean
"""
		return " ".join([self.getStateName(state,opposite) for state in api.createStateList(states)])

	def _get_level(self):
		return ""

	def _get_contains(self):
		return ""

	def _get_location(self):
		return (0,0,0,0)

	def _get_parent(self):
		return None

	def _get_next(self):
		return None

	def _get_previous(self):
		return None

	def _get_firstChild(self):
		return None

	def _get_children(self):
		children=[]
		child=self.firstChild
		while child:
			children.append(child)
			child=child.next
		return children

	def _get_childCount(self):
		return len(self.children)

	def doDefaultAction(self):
		"""
Performs the default action on this object. (e.g. clicks a button)
"""
		pass

	def _get_activeChild(self):
		return None

	def _get_hasFocus(self):
		"""
Returns true of this object has focus, false otherwise.
"""
		return False

	def setFocus(self):
		"""
Tries to force this object to take the focus.
"""
		pass

	def _get_labeledBy(self):
		return None

	def _get_positionString(self):
		return ""

	def _get_isProtected(self):
		return False


	def _get_statusBar(self):
		return None

	def speakObject(self):
		"""
Speaks the properties of this object such as name, typeString,value, description, states, position etc.
"""
		name=self.name
		typeString=self.typeString
		positiveStateNames=self.getStateNames(self.calculatePositiveStates())
		negativeStateNames=self.getStateNames(self.calculateNegativeStates(),opposite=True)
		stateNames="%s %s"%(positiveStateNames,negativeStateNames)
		value=self.value
		description=self.description
		if description==name:
			description=None
		if config.conf["presentation"]["reportKeyboardShortcuts"]:
			keyboardShortcut=self.keyboardShortcut
		else:
			keyboardShortcut=None
		position=self.positionString
		level=self.level
		if isinstance(level,int):
			level=_("level %d")%level 
		contains=self.contains
		audio.speakObjectProperties(name=name,typeString=typeString,stateText=stateNames,value=value,description=description,keyboardShortcut=keyboardShortcut,position=position,level=level,contains=contains)

	def speakDescendantObjects(self,hashList=None):
		if hashList is None:
			hashList=[]
		child=self.firstChild
		while child:
			h=hash(child)
			if h not in hashList:
				hashList.append(h)
				child.speakObject()
				child.speakDescendantObjects(hashList=hashList)
			child=child.next

	def event_gainFocus(self):
		"""
This code is executed if a gain focus event is received by this object.
"""
		if self.speakOnGainFocus and (not self.needsFocusState or (self.needsFocusState and self.hasFocus)):
			api.setNavigatorObject(self)
			if not ((self==api.getForegroundObject()) and self.speakOnForeground):
				self.speakObject()

	def event_foreground(self):
		"""
This method will speak the object if L{speakOnForeground} is true and this object has just become the current foreground object.
"""
		audio.cancel()
		if self.speakOnForeground:
			api.setNavigatorObject(self)
			self.speakObject()

	def _get_text_characterCount(self):
		return len(self.text_getText())

	def text_getText(self,start=None,end=None):
		"""Gets either all the text the object has, or the text from a certain offset, or to a certain offset.
@param start: the start offset
@type start: int
@param end: the end offset
@type end: int
@returns: the text
@rtype: string
"""
		name=self.name
		value=self.value
		description=self.description
		text=""
		if name:
			text+="%s "%name
		if value:
			text+="%s "%value
		if description and description!=name:
			text+="%s"%description
		text=text.rstrip()
		if start is None:
			start=0
		if end is None:
			end=len(text)
		return text[start:end]

	def _get_text_caretOffset(self):
		return 0

	def _set_text_caretOffset(self,offset):
		pass

	def _get_text_reviewOffset(self):
		return self._reviewOffset

	def _set_text_reviewOffset(self,offset):
		self._reviewOffset=offset

	def _get_text_selectionCount(self):
		return 0

	def text_getSelectionOffsets(self,index):
		"""Gets (start,end) tuple of the chosen selection.
@param index: The number of the selection you want
@type index: int
@returns: the start and end offsets of the selection or None if bad selection number
@rtype: 2-tuple
"""
		return None

	def _get_text_lineCount(self):
		return None

	def text_getLineOffsets(self,offset):
		"""Gets the start and end offsets for the line at given offset.
@param offset: the ofset where the line is located
@type offset: int
@returns: start and end offsets
@rtype: 2-tuple
"""
		text=self.text_getText()
		start=offset
		while (text is not None) and (len(text)>=start) and (start>0) and not (text[start-1] in ['\r','\n']): 
  			start-=1
		end=offset+1
		while (end<self.text_characterCount) and (text[end] not in ['\r','\n']):
			end+=1
		if (end<len(text)-1) and (text[end]=='\r') and (text[end+1]=='\n'):
			end+=2
		elif (end<len(text)) and (text[end] in ['\r','\n']):
			end+=1
		return (start,end)

	def text_getNextLineOffsets(self,offset):
		(start,end)=self.text_getLineOffsets(offset)
		if end<self.text_characterCount:
			return self.text_getLineOffsets(end)
		else:
			return None

	def text_getPrevLineOffsets(self,offset):
		(start,end)=self.text_getLineOffsets(offset)
		if start>0:
			return self.text_getLineOffsets(start-1)
		else:
			return None

	def text_getWordOffsets(self,offset):
		"""Gets the start and end offsets for the word at given offset.
@param offset: the ofset where the word is located
@type offset: int
@returns: start and end offsets
@rtype: 2-tuple
"""
		(lineStart,lineEnd)=self.text_getLineOffsets(offset)
		start=offset
		while (start>lineStart) and not self.text_getText(start=start,end=start+1).isspace() and not self.text_getText(start=start-1,end=start).isspace():
			start-=1
 		end=offset+1
		while (end<lineEnd) and not self.text_getText(start=end,end=end+1).isspace():
			end+=1
		return (start,end)

	def text_getNextWordOffsets(self,offset):
		(start,end)=self.text_getWordOffsets(offset)
		while end<self.text_characterCount:
			if not self.text_getText(start=end,end=end+1).isspace():
				return self.text_getWordOffsets(end)
			end+=1
		return None

	def text_getPrevWordOffsets(self,offset):
		(start,end)=self.text_getWordOffsets(offset)
		start-=1
		while start>=0:
			if not self.text_getText(start=start,end=start+1).isspace():
				return self.text_getWordOffsets(start)
			start-=1
		return None

	def text_getSentenceOffsets(self,offset):
		return self.text_getLineOffsets(offset)

	def text_getNextSentenceOffsets(self,offset):
		return self.text_getNextLineOffsets(offset)

	def text_getPrevSentenceOffsets(self,offset):
		return self.text_getPrevLineOffsets(offset)

	def text_getParagraphOffsets(self,offset):
		return self.text_getLineOffsets(offset)

	def text_getNextParagraphOffsets(self,offset):
		return self.text_getNextLineOffsets(offset)

	def text_getPrevParagraphOffsets(self,offset):
		return self.text_getPrevLineOffsets(offset)

	def text_getPageNumber(self,offset):
		return None

	def text_getLineNumber(self,offset):
		return None

	def text_getStyle(self,offset):
		return None

	def text_getAlignment(self,offset):
		return None

	def text_getFontName(self,offset):
		return None

	def text_getFontSize(self,offset):
		return None

	def text_isBold(self,offset):
		return False

	def text_isItalic(self,offset):
		return False

	def text_isUnderline(self,offset):
		return None

	def text_isSubscript(self,offset):
		return False

	def text_isSuperscript(self,offset):
		return False

	def text_getTableRowNumber(self,offset):
		return None

	def text_getTableColumnNumber(self,offset):
		return None

	def text_getTableCellOffsets(self,row,column):
		return None

	def text_getTableRowCount(self,offset):
		return None

	def text_getTableColumnCount(self,offset):
		return None

	def text_inTable(self,offset):
		return None

	def text_getFieldOffsets(self,offset):
		return self.text_getLineOffsets(offset)

	def text_getNextFieldOffsets(self,offset):
		return self.text_getNextLineOffsets(offset)

	def text_getPrevFieldOffsets(self,offset):
		return self.text_getPrevLineOffsets(offset)

	def text_reportNewPresentation(self,offset):
		if config.conf["documentFormatting"]["reportPage"]:
			pageNumber=self.text_getPageNumber(offset)
			lastPageNumber=self._text_lastReportedPresentation.get('pageNumber',None)
			if isinstance(pageNumber,int) and pageNumber!=lastPageNumber:
				audio.speakMessage(_("page %d")%pageNumber)
			self._text_lastReportedPresentation["pageNumber"]=pageNumber
		if config.conf["documentFormatting"]["reportLineNumber"]:
			lineNumber=self.text_getLineNumber(offset)
			lastLineNumber=self._text_lastReportedPresentation.get('lineNumber',None)
			if isinstance(lineNumber,int) and lineNumber!=lastLineNumber:
				audio.speakMessage(_("line %d")%lineNumber)
			self._text_lastReportedPresentation["lineNumber"]=lineNumber
		if config.conf["documentFormatting"]["reportTables"]:
			inTable=self.text_inTable(offset)
			wasInTable=self._text_lastReportedPresentation.get('inTable',None)
			if not inTable and wasInTable:
				audio.speakMessage(_("out of table"))
			elif inTable and not wasInTable:
				rowCount=self.text_getTableRowCount(offset)
				columnCount=self.text_getTableColumnCount(offset)
				audio.speakMessage(_("table with %d columns and %d rows")%(columnCount,rowCount))
			self._text_lastReportedPresentation["inTable"]=inTable
			rowNumber=self.text_getTableRowNumber(offset)
			lastRowNumber=self._text_lastReportedPresentation.get('tableRowNumber',None)
			if isinstance(rowNumber,int) and rowNumber!=lastRowNumber:
				audio.speakMessage(_("row %d")%rowNumber)
			self._text_lastReportedPresentation["tableRowNumber"]=rowNumber
			columnNumber=self.text_getTableColumnNumber(offset)
			lastColumnNumber=self._text_lastReportedPresentation.get('tableColumnNumber',None)
			if isinstance(columnNumber,int) and columnNumber!=lastColumnNumber:
				audio.speakMessage(_("column %d")%columnNumber)
			self._text_lastReportedPresentation["tableColumnNumber"]=columnNumber
		if config.conf["documentFormatting"]["reportStyle"]:
			style=self.text_getStyle(offset)
			lastStyle=self._text_lastReportedPresentation.get('style',None)
			if isinstance(style,basestring) and style!=lastStyle:
				audio.speakMessage(_("style %s")%style)
			self._text_lastReportedPresentation["style"]=style
		if config.conf["documentFormatting"]["reportAlignment"]:
			alignment=self.text_getAlignment(offset)
			lastAlignment=self._text_lastReportedPresentation.get('alignment',None)
			if isinstance(alignment,basestring) and alignment!=lastAlignment:
				audio.speakMessage(_("alignment %s")%alignment)
			self._text_lastReportedPresentation["alignment"]=alignment
		if config.conf["documentFormatting"]["reportFontName"]:
			fontName=self.text_getFontName(offset)
			lastFontName=self._text_lastReportedPresentation.get('fontName',None)
			if isinstance(fontName,basestring) and fontName!=lastFontName:
				audio.speakMessage(_("font name %s")%fontName)
			self._text_lastReportedPresentation["fontName"]=fontName
		if config.conf["documentFormatting"]["reportFontSize"]:
			fontSize=self.text_getFontSize(offset)
			lastFontSize=self._text_lastReportedPresentation.get('fontSize',None)
			if isinstance(fontSize,int) and fontSize!=lastFontSize:
				audio.speakMessage(_("font size %d")%fontSize)
			self._text_lastReportedPresentation["fontSize"]=fontSize
		if config.conf["documentFormatting"]["reportFontAttributes"]:
			isBold=self.text_isBold(offset)
			wasBold=self._text_lastReportedPresentation.get('isBold',None)
			if isinstance(isBold,bool) and isBold and not wasBold:
				audio.speakMessage(_("bold"))
			elif isinstance(isBold,bool) and not isBold and wasBold:
				audio.speakMessage(_("not bold"))
			self._text_lastReportedPresentation["isBold"]=isBold
			isItalic=self.text_isItalic(offset)
			wasItalic=self._text_lastReportedPresentation.get('isItalic',None)
			if isinstance(isItalic,bool) and isItalic and not wasItalic:
				audio.speakMessage(_("italic"))
			elif isinstance(isItalic,bool) and not isItalic and wasItalic:
				audio.speakMessage(_("not italic"))
			self._text_lastReportedPresentation["isItalic"]=isItalic
			isUnderline=self.text_isUnderline(offset)
			wasUnderline=self._text_lastReportedPresentation.get('isUnderline',None)
			if isinstance(isUnderline,bool) and isUnderline and not wasUnderline:
				audio.speakMessage(_("underline"))
			elif isinstance(isUnderline,bool) and not isUnderline and wasUnderline:
				audio.speakMessage(_("not underline"))
			self._text_lastReportedPresentation["isUnderline"]=isUnderline
			isSuperscript=self.text_isSuperscript(offset)
			wasSuperscript=self._text_lastReportedPresentation.get('isSuperscript',None)
			if isinstance(isSuperscript,bool) and isSuperscript and not wasSuperscript:
				audio.speakMessage(_("superscript"))
			elif isinstance(isSuperscript,bool) and not isSuperscript and wasSuperscript:
				audio.speakMessage(_("not superscript"))
			self._text_lastReportedPresentation["isSuperscript"]=isSuperscript
			isSubscript=self.text_isSubscript(offset)
			wasSubscript=self._text_lastReportedPresentation.get('isSubscript',None)
			if isinstance(isSubscript,bool) and isSubscript and not wasSubscript:
				audio.speakMessage(_("superscript"))
			elif isinstance(isSubscript,bool) and not isSubscript and wasSubscript:
				audio.speakMessage(_("not subscript"))
			self._text_lastReportedPresentation["isSubscript"]=isSubscript

	def text_reportPresentation(self,offset):
		style=self.text_getStyle(offset)
		alignment=self.text_getAlignment(offset)
		fontName=self.text_getFontName(offset)
		fontSize=self.text_getFontSize(offset)
		isBold=self.text_isBold(offset)
		isItalic=self.text_isItalic(offset)
		isUnderline=self.text_isUnderline(offset)
		isSuperscript=self.text_isSuperscript(offset)
		isSubscript=self.text_isSubscript(offset)
		if isinstance(style,basestring):
			audio.speakMessage(_("style %s")%style)
		if isinstance(alignment,basestring):
			audio.speakMessage(_("alignment %s")%alignment)
		if isinstance(fontName,basestring):
			audio.speakMessage(_("font name %s")%fontName)
		if isinstance(fontSize,int):
			audio.speakMessage(_("font size %d")%fontSize)
		if isinstance(isBold,bool) and isBold:
			audio.speakMessage(_("bold"))
		if isinstance(isItalic,bool) and isItalic:
			audio.speakMessage(_("italic"))
		if isinstance(isUnderline,bool) and isUnderline:
			audio.speakMessage(_("underline"))
		if isinstance(isSuperscript,bool) and isSuperscript:
			audio.speakMessage(_("superscript"))
		if isinstance(isSubscript,bool) and isSubscript:
			audio.speakMessage(_("subscript"))

	def text_speakLine(self,offset):
		self.text_reportNewPresentation(offset)
		r=self.text_getLineOffsets(offset)
		if r is not None:
			audio.speakText(self.text_getText(r[0],r[1]),index=r[0])

	def text_speakWord(self,offset):
		self.text_reportNewPresentation(offset)
		r=self.text_getWordOffsets(offset)
		if r is not None:
			audio.speakText(self.text_getText(r[0],r[1]),index=r[0])

	def text_speakCharacter(self,offset):
		self.text_reportNewPresentation(offset)
		audio.speakSymbol(self.text_getText(offset,offset+1),index=offset)

	def text_speakSentence(self,offset):
		self.text_reportNewPresentation(offset)
		r=self.text_getSentenceOffsets(offset)
		if r is not None:
			audio.speakText(self.text_getText(r[0],r[1]),index=r[0])

	def text_speakParagraph(self,offset):
		self.text_reportNewPresentation(offset)
		r=self.text_getParagraphOffsets(offset)
		if r is not None:
			audio.speakText(self.text_getText(r[0],r[1]),index=r[0])

	def _get_text_reviewOffsetLimits(self):
		return (0,self.text_characterCount-1)

	def script_text_review_moveToCaret(self,keyPress):
		self.text_reviewOffset=self.text_caretOffset
		self.text_speakLine(self.text_reviewOffset)

	def script_text_review_top(self,keyPress):
		audio.speakMessage(_("top"))
		self.text_reviewOffset=self.text_reviewOffsetLimits[0]
		self.text_speakLine(self.text_reviewOffset)

	def script_text_review_bottom(self,keyPress):
		audio.speakMessage(_("bottom"))
		self.text_reviewOffset=self.text_reviewOffsetLimits[1]
		self.text_speakLine(self.text_reviewOffset)

	def script_text_review_currentLine(self,keyPress):
		self.text_speakLine(self.text_reviewOffset)

	def script_text_review_nextLine(self,keyPress):
		r=self.text_getNextLineOffsets(self.text_reviewOffset)
		limits=self.text_reviewOffsetLimits
		if r is not None and r[0]>=limits[0] and r[0]<=limits[1]:
			self.text_reviewOffset=r[0]
		else:
			audio.speakMessage(_("bottom"))
		self.text_speakLine(self.text_reviewOffset)

	def script_text_review_prevLine(self,keyPress):
		r=self.text_getPrevLineOffsets(self.text_reviewOffset)
		limits=self.text_reviewOffsetLimits
		if r is not None and r[0]>=limits[0] and r[0]<=limits[1]:
			self.text_reviewOffset=r[0]
		else:
			audio.speakMessage(_("top"))
		self.text_speakLine(self.text_reviewOffset)

	def script_text_review_currentWord(self,keyPress):
		self.text_speakWord(self.text_reviewOffset)

	def script_text_review_nextWord(self,keyPress):
		r=self.text_getNextWordOffsets(self.text_reviewOffset)
		limits=self.text_reviewOffsetLimits
		if r is not None and r[0]>=limits[0] and r[0]<=limits[1]:
			self.text_reviewOffset=r[0]
		else:
			audio.speakMessage(_("bottom"))
		self.text_speakWord(self.text_reviewOffset)

	def script_text_review_prevWord(self,keyPress):
		r=self.text_getPrevWordOffsets(self.text_reviewOffset)
		limits=self.text_reviewOffsetLimits
		if r is not None and r[0]>=limits[0] and r[0]<=limits[1]:
			self.text_reviewOffset=r[0]
		else:
			audio.speakMessage(_("top"))
		self.text_speakWord(self.text_reviewOffset)

	def script_text_review_currentCharacter(self,keyPress):
		self.text_speakCharacter(self.text_reviewOffset)

	def script_text_review_nextCharacter(self,keyPress):
		newOffset=self.text_reviewOffset+1
		limits=self.text_reviewOffsetLimits
		if newOffset>=limits[0] and newOffset<=limits[1]:
			self.text_reviewOffset=newOffset
		else:
			audio.speakMessage(_("bottom"))
		self.text_speakCharacter(self.text_reviewOffset)

	def script_text_review_prevCharacter(self,keyPress):
		newOffset=self.text_reviewOffset-1
		limits=self.text_reviewOffsetLimits
		if newOffset>=limits[0] and newOffset<=limits[1]:
			self.text_reviewOffset=newOffset
		else:
			audio.speakMessage(_("top"))
		self.text_speakCharacter(self.text_reviewOffset)

	def script_text_review_startOfLine(self,keyPress):
		r=self.text_getLineOffsets(self.text_reviewOffset)
		self.text_reviewOffset=r[0]
		self.text_speakCharacter(self.text_reviewOffset)

	def script_text_review_endOfLine(self,keyPress):
		r=self.text_getLineOffsets(self.text_reviewOffset)
		self.text_reviewOffset=r[1]-1
		self.text_speakCharacter(self.text_reviewOffset)

	def text_sayAll_generator(self,offset):
		curPos=offset
		chunkOffsetsFunc=self.text_getLineOffsets
		nextChunkOffsetsFunc=self.text_getNextLineOffsets
		lastKeyCount=globalVars.keyCounter
		while (curPos<self.text_characterCount) and (lastKeyCount==globalVars.keyCounter):
			r=chunkOffsetsFunc(curPos)
			if r is None:
				break
			text=self.text_getText(r[0],r[1])
			if text and not text.isspace():
				audio.speakText(text,index=r[0])
			r=nextChunkOffsetsFunc(curPos)
			if r is None:
				break
			curPos=r[0]
			yield

	def event_caret(self):
		self.text_reviewOffset=self.text_caretOffset

	def script_text_moveByLine(self,keyPress):
		"""Moves and then reads the current line"""
		sendKey(keyPress)
		self.text_speakLine(self.text_caretOffset)
		self.text_reviewOffset=self.text_caretOffset

	def script_text_moveByCharacter(self,keyPress):
		"""Moves and reads the current character"""
		sendKey(keyPress)
		self.text_speakCharacter(self.text_caretOffset)
		self.text_reviewOffset=self.text_caretOffset

	def script_text_moveByWord(self,keyPress):
		"""Moves and reads the current word"""
		sendKey(keyPress)
		self.text_speakWord(self.text_caretOffset)
		self.text_reviewOffset=self.text_caretOffset

	def script_text_moveBySentence(self,keyPress):
		"""Moves and then reads the current line"""
		sendKey(keyPress)
		self.text_speakSentence(self.text_caretOffset)
		self.text_reviewOffset=self.text_caretOffset

	def script_text_moveByParagraph(self,keyPress):
		"""Moves and then reads the current line"""
		sendKey(keyPress)
		self.text_speakParagraph(self.text_caretOffset)
		self.text_reviewOffset=self.text_caretOffset

	def script_text_nextParagraph(self,keyPress):
		"""Manually moves to the next paragraph and then speaks it"""
		r=self.text_getNextParagraphOffsets(self.text_caretOffset)
		if r:
			self.text_caretOffset=r[0]
			self.text_speakParagraph(self.text_caretOffset)
		self.text_reviewOffset=self.text_caretOffset

	def script_text_prevParagraph(self,keyPress):
		"""Manually moves to the previous paragraph and then speaks it"""
		r=self.text_getPrevParagraphOffsets(self.text_caretOffset)
		if r:
			self.text_caretOffset=r[0]
			self.text_speakParagraph(self.text_caretOffset)
		self.text_reviewOffset=self.text_caretOffset

	def script_text_changeSelection(self,keyPress):
		"""Moves and reads the current selection"""
		oldSelections=[]
		for selNum in xrange(self.text_selectionCount):
			oldSelections.append(self.text_getSelectionOffsets(selNum))
		sendKey(keyPress)
		newSelections=[]
		for selNum in xrange(self.text_selectionCount):
			newSelections.append(self.text_getSelectionOffsets(selNum))
		if len(oldSelections)>0 and len(newSelections)==0:
			self.text_speakCharacter(self.text_caretOffset)
			audio.speakMessage(_("no selections"))
		elif len(newSelections)>0 and len(oldSelections)==0:
			for selNum in xrange(len(newSelections)):
					audio.speakMessage(_("selected %s")%self.text_getText(newSelections[selNum][0],newSelections[selNum][1]))
		elif len(newSelections)>0 and len(oldSelections)>0:
			for selNum in xrange(max(len(newSelections),len(oldSelections))):
				if selNum<len(oldSelections) and selNum<len(newSelections) and newSelections[selNum][1]>oldSelections[selNum][1]:
   					audio.speakMessage(_("selected %s")%self.text_getText(oldSelections[selNum][1],newSelections[selNum][1]))
				if selNum<len(oldSelections) and selNum<len(newSelections) and newSelections[selNum][0]>oldSelections[selNum][0]:
   					audio.speakMessage(_("selected %s")%self.text_getText(oldSelections[selNum][0],newSelections[selNum][0]))
				if selNum<len(oldSelections) and selNum<len(newSelections) and newSelections[selNum][1]<oldSelections[selNum][1]:
   					audio.speakMessage(_("unselected %s")%self.text_getText(newSelections[selNum][1],oldSelections[selNum][1]))
				if selNum<len(oldSelections) and selNum<len(newSelections) and newSelections[selNum][0]<oldSelections[selNum][0]:
   					audio.speakMessage(_("unselected %s")%self.text_getText(newSelections[selNum][0],oldSelections[selNum][0]))
				if selNum<len(newSelections) and selNum>=len(oldSelections):
   					audio.speakMessage(_("selected %s")%self.text_getText(newSelections[selNum][0],newSelections[selNum][1]))
				if selNum>=len(newSelections) and selNum<len(oldSelections):
   					audio.speakMessage(_("unselected %s")%self.text_getText(oldSelections[selNum][0],oldSelections[selNum][1]))
		self.text_reviewOffset=self.text_caretOffset

	def script_text_delete(self,keyPress):
		"""Deletes the character and reads the new current character"""
		sendKey(keyPress)
		self.text_speakCharacter(self.text_caretOffset)
		self.text_reviewOffset=self.text_caretOffset

	def script_text_backspace(self,keyPress):
		"""Reads the character before the current character and then deletes it"""
		point=self.text_caretOffset
		if point>0:
			delChar=self.text_getText(point-1,point)
			sendKey(keyPress)
			newPoint=self.text_caretOffset
			if newPoint<point:
				audio.speakSymbol(delChar)
		else:
			sendKey(keyPress)
			audio.speakText("")
		self.text_reviewOffset=self.text_caretOffset

	def event_valueChange(self):
		value=self.value
		if self.hasFocus and value!=self._oldValue:
			audio.speakObjectProperties(value=self.value)
			self._oldValue=value

	def event_nameChange(self):
		name=self.name
		if self.hasFocus and name!=self._oldName:
			audio.speakObjectProperties(name=self.name)
			self._oldName=name

	def event_descriptionChange(self):
		description=self.description
		if self.hasFocus and description!=self._oldDescription:
			audio.speakObjectProperties(description=self.description)
			self._oldDescription=description
