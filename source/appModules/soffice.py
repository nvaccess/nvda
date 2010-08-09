#appModules/soffice.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2010 Michael Curran <mick@kulgan.net>, James Teh <jamie@jantrid.net>

from comtypes import COMError
import IAccessibleHandler
import _default
import controlTypes
import textInfos
from compoundDocuments import CompoundDocument
from NVDAObjects.JAB import JAB
from NVDAObjects.IAccessible import IAccessible, IA2TextTextInfo
from NVDAObjects.behaviors import EditableText
from logHandler import log

class SymphonyTextInfo(IA2TextTextInfo):

	def _getFormatFieldAndOffsets(self,offset,formatConfig,calculateOffsets=True):
		try:
			startOffset,endOffset,attribsString=self.obj.IAccessibleTextObject.attributes(offset)
		except COMError:
			log.debugWarning("could not get attributes",exc_info=True)
			return textInfos.FormatField(),(self._startOffset,self._endOffset)
		formatField=textInfos.FormatField()
		if not attribsString and offset>0:
			try:
				attribsString=self.obj.IAccessibleTextObject.attributes(offset-1)[2]
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

		# optimisation: Assume a hyperlink occupies a full attribute run.
		try:
			self.obj.IAccessibleTextObject.QueryInterface(IAccessibleHandler.IAccessibleHypertext).hyperlinkIndex(offset)
			formatField["link"] = True
		except COMError:
			pass

		if offset == 0:
			# Only include the list item prefix on the first line of the paragraph.
			numbering = formatField.get("Numbering")
			if numbering:
				formatField["line-prefix"] = numbering.get("NumberingPrefix") or numbering.get("BulletChar")

		return formatField,(startOffset,endOffset)

class SymphonyText(IAccessible, EditableText):
	TextInfo = SymphonyTextInfo

	def _get_positionInfo(self):
		level = self.IA2Attributes.get("heading-level")
		if level:
			return {"level": int(level)}
		return super(SymphonyText, self).positionInfo

class AppModule(_default.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if isinstance(obj, IAccessible) and obj.windowClassName in ("SALTMPSUBFRAME", "SALSUBFRAME") and hasattr(obj, "IAccessibleTextObject"):
			clsList.insert(0, SymphonyText)

	def event_NVDAObject_init(self, obj):
		windowClass = obj.windowClassName
		if isinstance(obj, JAB) and windowClass == "SALFRAME":
			# OpenOffice.org has some strange role mappings due to its use of JAB.
			if obj.role == controlTypes.ROLE_CANVAS:
				obj.role = controlTypes.ROLE_DOCUMENT
			elif obj.role == controlTypes.ROLE_LABEL:
				parent = obj.parent
				if parent and parent.role == controlTypes.ROLE_TABLE:
					obj.role = controlTypes.ROLE_TABLECELL

		if windowClass in ("SALTMPSUBFRAME", "SALFRAME") and obj.role == controlTypes.ROLE_DOCUMENT and obj.description:
			# This is a word processor document.
			obj.description = None
			obj.treeInterceptorClass = CompoundDocument
