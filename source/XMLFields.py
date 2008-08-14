import sgmllib
from xml.parsers import expat

class XMLContextParser(object): 

	def __init__(self):
		self.parser=expat.ParserCreate('utf-8')
		self.parser.StartElementHandler=self._startElementHandler
		#self.parser.EndElementHandler=self._EndElementHandler
		#self.parser.CharacterDataHandler=self._CharacterDataHandler
		self._fieldStack=[]

	def _startElementHandler(self,name,attrs):
		newAttrs={}
		for name,value in attrs.items():
			newAttrs[name.lower()]=value
		self._fieldStack.append(newAttrs)

	def parse(self,XMLContext):
		try:
			self.parser.Parse(XMLContext.encode('utf-8'))
		except:
			log.debugWarning("XML: %s"%XMLContext,exc_info=True)
		return self._fieldStack

class RelativeXMLParser(object):

	def __init__(self):
		self.parser=sgmllib.SGMLParser()
		self.parser.unknown_starttag=self._startElementHandler
		self.parser.unknown_endtag=self._endElementHandler
		self.parser.handle_data=self._characterDataHandler
		self._commandList=[]

	def _startElementHandler(self,tag,attrs):
		newAttrs={}
		for attr in attrs:
			newAttrs[attr[0]]=attr[1]
		attrs=newAttrs
		self._commandList.append(("start",attrs))

	def _endElementHandler(self,tag):
		self._commandList.append(("end",None))

	def _characterDataHandler(self,data):
		self._commandList.append(("text",data))

	def parse(self,relativeXML):
		self.parser.feed(relativeXML)
		return self._commandList
