#appModules/soffice.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2010 Michael Curran <mick@kulgan.net>, James Teh <jamie@jantrid.net>

from comtypes import COMError
import IAccessibleHandler
import appModuleHandler
import controlTypes
import textInfos
import colors
from compoundDocuments import CompoundDocument
from NVDAObjects.JAB import JAB, JABTextInfo
from NVDAObjects.IAccessible import IAccessible, IA2TextTextInfo
from NVDAObjects.behaviors import EditableText
from logHandler import log

def gridCoordStringToNumbers(coordString):
	if not coordString or len(coordString)<2 or ' ' in coordString or coordString[0].isdigit() or not coordString[-1].isdigit(): 
		raise ValueError("bad coord string: %r"%coordString) 
	rowNum=0
	colNum=0
	coordStringRowStartIndex=None
	for index,ch in enumerate(reversed(coordString)):
		if not ch.isdigit():
			coordStringRowStartIndex=len(coordString)-index
			break
	rowNum=int(coordString[coordStringRowStartIndex:])
	for index,ch in enumerate(reversed(coordString[0:coordStringRowStartIndex])):
		colNum+=((ord(ch.upper())-ord('A')+1)*(26**index))
	return rowNum,colNum

class JAB_OOTable(JAB):

	def _get_rowCount(self):
		return 0

	def _get_columnCount(self):
		return 0

class JAB_OOTableCell(JAB):

	role=controlTypes.ROLE_TABLECELL

	def _get_name(self):
		name=super(JAB_OOTableCell,self).name
		if name and name.startswith('Cell') and name[-2].isdigit():
			return None
		return name

	def _get_cellCoordsText(self):
		name=super(JAB_OOTableCell,self).name
		if name and name.startswith('Cell') and name[-2].isdigit():
			return name[5:-1]

	def _get_value(self):
		value=super(JAB_OOTableCell,self).value
		if not value and issubclass(self.TextInfo,JABTextInfo):
			value=self.makeTextInfo(textInfos.POSITION_ALL).text
		return value

	def _get_states(self):
		states=super(JAB_OOTableCell,self).states
		states.discard(controlTypes.STATE_EDITABLE)
		return states

	def _get_rowNumber(self):
		try:
			return gridCoordStringToNumbers(self.cellCoordsText)[0]
		except ValueError:
			return 0

	def _get_columnNumber(self):
		try:
			return gridCoordStringToNumbers(self.cellCoordsText)[1]
		except ValueError:
			return 0

class SymphonyTextInfo(IA2TextTextInfo):

	def _getFormatFieldAndOffsets(self,offset,formatConfig,calculateOffsets=True):
		obj = self.obj
		try:
			startOffset,endOffset,attribsString=obj.IAccessibleTextObject.attributes(offset)
		except COMError:
			log.debugWarning("could not get attributes",exc_info=True)
			return textInfos.FormatField(),(self._startOffset,self._endOffset)
		formatField=textInfos.FormatField()
		if not attribsString and offset>0:
			try:
				attribsString=obj.IAccessibleTextObject.attributes(offset-1)[2]
			except COMError:
				pass
		if attribsString:
			formatField.update(IAccessibleHandler.splitIA2Attribs(attribsString))

		try:
			escapement = int(formatField["CharEscapement"])
			if escapement < 0:
				textPos = "sub"
			elif escapement > 0:
				textPos = "super"
			else:
				textPos = "baseline"
			formatField["text-position"] = textPos
		except KeyError:
			pass
		try:
			formatField["font-name"] = formatField["CharFontName"]
		except KeyError:
			pass
		try:
			formatField["font-size"] = "%spt" % formatField["CharHeight"]
		except KeyError:
			pass
		try:
			formatField["italic"] = formatField["CharPosture"] == "2"
		except KeyError:
			pass
		try:
			formatField["strikethrough"] = formatField["CharStrikeout"] == "1"
		except KeyError:
			pass
		try:
			underline = formatField["CharUnderline"]
			if underline == "10":
				# Symphony doesn't provide for semantic communication of spelling errors, so we have to rely on the WAVE underline type.
				formatField["invalid-spelling"] = True
			else:
				formatField["underline"] = underline != "0"
		except KeyError:
			pass
		try:
			formatField["bold"] = float(formatField["CharWeight"]) > 100
		except KeyError:
			pass
		try:
			color=formatField.pop('CharColor')
		except KeyError:
			color=None
		if color:
			formatField['color']=colors.RGB.fromString(color) 
		try:
			backgroundColor=formatField.pop('CharBackColor')
		except KeyError:
			backgroundColor=None
		if backgroundColor:
			formatField['background-color']=colors.RGB.fromString(backgroundColor)

		# optimisation: Assume a hyperlink occupies a full attribute run.
		try:
			if obj.IAccessibleTextObject.QueryInterface(IAccessibleHandler.IAccessibleHypertext).hyperlinkIndex(offset) != -1:
				formatField["link"] = True
		except COMError:
			pass

		if offset == 0:
			# Only include the list item prefix on the first line of the paragraph.
			numbering = formatField.get("Numbering")
			if numbering:
				formatField["line-prefix"] = numbering.get("NumberingPrefix") or numbering.get("BulletChar")

		if obj.hasFocus:
			# Symphony exposes some information for the caret position as attributes on the document object.
			# optimisation: Use the tree interceptor to get the document.
			try:
				docAttribs = obj.treeInterceptor.rootNVDAObject.IA2Attributes
			except AttributeError:
				# No tree interceptor, so we can't efficiently fetch this info.
				pass
			else:
				try:
					formatField["page-number"] = docAttribs["page-number"]
				except KeyError:
					pass
				try:
					formatField["line-number"] = docAttribs["line-number"]
				except KeyError:
					pass

		return formatField,(startOffset,endOffset)

	def _getLineOffsets(self, offset):
		start, end = super(SymphonyTextInfo, self)._getLineOffsets(offset)
		if offset == 0 and start == 0 and end == 0:
			# HACK: Symphony doesn't expose any characters at all on empty lines, but this means we don't ever fetch the list item prefix in this case.
			# Fake a character so that the list item prefix will be spoken on empty lines.
			return (0, 1)
		return start, end

	def _getStoryLength(self):
		# HACK: Account for the character faked in _getLineOffsets() so that move() will work.
		return max(super(SymphonyTextInfo, self)._getStoryLength(), 1)

class SymphonyText(IAccessible, EditableText):
	TextInfo = SymphonyTextInfo

	def _get_positionInfo(self):
		level = self.IA2Attributes.get("heading-level")
		if level:
			return {"level": int(level)}
		return super(SymphonyText, self).positionInfo

class SymphonyTableCell(IAccessible):
	"""Silences particular states, and redundant column/row numbers"""

	TextInfo=SymphonyTextInfo

	def _get_cellCoordsText(self):
		return super(SymphonyTableCell,self).name

	name=None

	def _get_states(self):
		states=super(SymphonyTableCell,self).states
		states.discard(controlTypes.STATE_MULTILINE)
		states.discard(controlTypes.STATE_EDITABLE)
		return states

class SymphonyParagraph(SymphonyText):
	"""Removes redundant information that can be retreaved in other ways."""
	value=None
	description=None

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		role=obj.role
		windowClassName=obj.windowClassName
		if isinstance(obj, IAccessible) and windowClassName in ("SALTMPSUBFRAME", "SALSUBFRAME", "SALFRAME"):
			if role==controlTypes.ROLE_TABLECELL:
				clsList.insert(0, SymphonyTableCell)
			elif hasattr(obj, "IAccessibleTextObject"):
				clsList.insert(0, SymphonyText)
			if role==controlTypes.ROLE_PARAGRAPH:
				clsList.insert(0, SymphonyParagraph)
		if isinstance(obj, JAB) and windowClassName == "SALFRAME":
			if role in (controlTypes.ROLE_PANEL,controlTypes.ROLE_LABEL):
				parent=obj.parent
				if parent and parent.role==controlTypes.ROLE_TABLE:
					clsList.insert(0,JAB_OOTableCell)
			elif role==controlTypes.ROLE_TABLE:
				clsList.insert(0,JAB_OOTable)

	def event_NVDAObject_init(self, obj):
		windowClass = obj.windowClassName
		if isinstance(obj, JAB) and windowClass == "SALFRAME":
			# OpenOffice.org has some strange role mappings due to its use of JAB.
			if obj.role == controlTypes.ROLE_CANVAS:
				obj.role = controlTypes.ROLE_DOCUMENT

		if windowClass in ("SALTMPSUBFRAME", "SALFRAME") and obj.role in (controlTypes.ROLE_DOCUMENT,controlTypes.ROLE_TEXTFRAME) and obj.description:
			# This is a word processor document.
			obj.description = None
			obj.treeInterceptorClass = CompoundDocument
