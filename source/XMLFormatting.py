from xml.parsers import expat
import textInfos
from logHandler import log

class XMLTextParser(object): 

	def __init__(self):
		self.parser=expat.ParserCreate('utf-8')
		self.parser.StartElementHandler=self._startElementHandler
		self.parser.EndElementHandler=self._EndElementHandler
		self.parser.CharacterDataHandler=self._CharacterDataHandler
		self._commandList=[]

	def _startElementHandler(self,tagName,attrs):
		if tagName=='control':
			newAttrs=textInfos.ControlField()
			for name,value in attrs.iteritems():
				newAttrs[name]=value
			self._commandList.append(textInfos.FieldCommand("controlStart",newAttrs))
		elif tagName=='text':
			newAttrs=textInfos.FormatField()
			for name,value in attrs.iteritems():
				newAttrs[name.lower()]=value
			self._commandList.append(textInfos.FieldCommand("formatChange",newAttrs))
		else:
			raise ValueError("Unknown tag name: %s"%tagName)

	def _EndElementHandler(self,tagName):
		if tagName=="control":
			self._commandList.append(textInfos.FieldCommand("controlEnd",None))
		elif tagName=="text":
			pass
		else:
			raise ValueError("unknown tag name: %s"%tagName)

	def _CharacterDataHandler(self,data):
		self._commandList.append(data)

	def parse(self,XMLText):
		try:
			self.parser.Parse(XMLText.encode('utf-8'))
		except:
			log.error("XML: %s"%XMLText,exc_info=True)
		return self._commandList

