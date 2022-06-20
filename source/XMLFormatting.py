# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2008-2021 NV Access Limited, Babbage B.V.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import typing
from xml.parsers import expat
import textInfos
import textUtils
from logHandler import log
from textUtils import WCHAR_ENCODING, isLowSurrogate

CommandsT = typing.Union[textInfos.FieldCommand, typing.Optional[str]]
CommandListT = typing.List[CommandsT]


class XMLTextParser(object): 

	def _startElementHandler(self,tagName,attrs):
		if tagName=='unich':
			data=attrs.get('value',None)
			if data is not None:
				try:
					data=chr(int(data))
				except ValueError:
					data = textUtils.REPLACEMENT_CHAR
				self._CharacterDataHandler(data, processBufferedSurrogates=isLowSurrogate(data))
			return
		elif tagName=='control':
			newAttrs=textInfos.ControlField(attrs)
			self._commandList.append(textInfos.FieldCommand("controlStart",newAttrs))
		elif tagName=='text':
			newAttrs=textInfos.FormatField(attrs)
			self._commandList.append(textInfos.FieldCommand("formatChange",newAttrs))
		else:
			raise ValueError("Unknown tag name: %s"%tagName)

		# Normalise attributes common to both field types.
		try:
			newAttrs["_startOfNode"] = newAttrs["_startOfNode"] == "1"
		except KeyError:
			pass
		try:
			newAttrs["_endOfNode"] = newAttrs["_endOfNode"] == "1"
		except KeyError:
			pass

	def _EndElementHandler(self,tagName):
		if tagName=="control":
			self._commandList.append(textInfos.FieldCommand("controlEnd",None))
		elif tagName in ("text","unich"):
			pass
		else:
			raise ValueError("unknown tag name: %s"%tagName)

	def _CharacterDataHandler(self, data: typing.Optional[str], processBufferedSurrogates=False):
		cmdList=self._commandList
		if not isinstance(data, str):
			dataStr = repr(data)
			log.warning(f"unknown type for data: {dataStr}")
		if cmdList and isinstance(cmdList[-1],str):
			cmdList[-1] += data
			if processBufferedSurrogates:
				cmdList[-1] = cmdList[-1].encode(WCHAR_ENCODING, errors="surrogatepass").decode(WCHAR_ENCODING)
		else:
			cmdList.append(data)

	def parse(self, XMLText) -> CommandListT:
		parser = expat.ParserCreate('utf-8')
		parser.StartElementHandler = self._startElementHandler
		parser.EndElementHandler = self._EndElementHandler
		parser.CharacterDataHandler = self._CharacterDataHandler
		self._commandList: XMLTextParser.CommandListT = []
		try:
			parser.Parse(XMLText)
		except Exception:
			log.error("XML: %s" % XMLText, exc_info=True)
		return self._commandList
