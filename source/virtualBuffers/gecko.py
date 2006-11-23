from constants import *
import debug
import winUser
import MSAAHandler
import audio
import NVDAObjects
import baseType

NAVRELATION_EMBEDS=0x1009 

class virtualBuffer_gecko(baseType.virtualBuffer):

	def __init__(self,NVDAObject):
		baseType.virtualBuffer.__init__(self,NVDAObject)
		debug.writeMessage("virtualBuffer gecko")
		if not self.NVDAObject.states&STATE_SYSTEM_BUSY:
			self.loadDocument()

	def event_stateChange(self,hwnd,objectID,childID):
		NVDAObject=NVDAObjects.getNVDAObjectByLocator(hwnd,objectID,childID)
		if (NVDAObject.role==ROLE_SYSTEM_DOCUMENT):
			if NVDAObject.states&STATE_SYSTEM_BUSY:
				audio.speakMessage(_("Busy")+"...")
			else:
				self.NVDAObject=NVDAObject
				self.loadDocument()

	def loadDocument(self):
		if winUser.getAncestor(self.NVDAObject.hwnd,GA_ROOT)==winUser.getForegroundWindow():
			audio.cancel()
			audio.speakMessage(_("Loading document")+" "+self.NVDAObject.name+"...")
		self.addNode(self.NVDAObject)
		self.caretPosition=0
		if winUser.getAncestor(self.NVDAObject.hwnd,GA_ROOT)==winUser.getForegroundWindow():
			audio.cancel()
			audio.speakText(self.text)

	def addNode(self,NVDAObject):
		(nodes,text)=self.generateNode(NVDAObject)
		if len(text)>0 and (text[0]=='\n'):
			text=text[1:]
			for num in range(len(nodes)):
				nodes[num][2]-=1
				nodes[num][3]-=1
		self.nodes=nodes
		self.text=text


	def getNodesIndexByUniqueID(self,uniqueID):
		for i in range(len(self.nodes)):
			if self.nodes[i][0]==uniqueID:
				return i
		else:
			return -1

	def getNodesIndexByPosition(self,pos):
		for i in range(len(self.nodes))[::-1]:
			if (pos>=self.nodes[i][2]) and (pos<=self.nodes[i][3]):
				return i
		else:
			return -1

	def getStartTag(self,NVDAObject):
		role=NVDAObject.role
		if role==ROLE_SYSTEM_DOCUMENT:
			return "%s %s\n"%(NVDAObject.typeString,NVDAObject.name)
		if role==ROLE_SYSTEM_STATICTEXT:
			return " %s "%NVDAObject.value
		elif role==ROLE_SYSTEM_LIST:
			return "\n%s wih %s items\n"%(NVDAObject.typeString,NVDAObject.childCount)
		elif role==ROLE_SYSTEM_LISTITEM:
			return "\n*"
		elif role==ROLE_SYSTEM_LINK:
			return " %s %s "%(NVDAObject.typeString,NVDAObject.name)
		elif role in ["h1","h2","h3","h4","h5","h6"]:
			return "\n%s "%NVDAObject.typeString
		elif role==ROLE_SYSTEM_TABLE:
			return "\n%s\n"%NVDAObject.typeString
		elif role in ["tbody","thead","tfoot",ROLE_SYSTEM_CELL]:
			return "\n"
		elif role==ROLE_SYSTEM_GRAPHIC:
			return "%s %s"%(NVDAObject.typeString,NVDAObject.name)
		else:
			return "\nunknown object %s %s"%(NVDAObject.typeString,NVDAObject.name)

	def getEndTag(self,NVDAObject):
		role=NVDAObject.role
		if role==ROLE_SYSTEM_DOCUMENT:
			return "\n%s end"%NVDAObject.typeString
		if role==ROLE_SYSTEM_LIST:
			return "\n%s end\n"%NVDAObject.typeString
		elif role==ROLE_SYSTEM_TABLE:
			return "\n%s end\n"%NVDAObject.typeString
		elif role in ["tbody","thead","tfoot",ROLE_SYSTEM_CELL]:
			return "\n"
		elif role in ["h1","h2","h3","h4","h5","h6"]:
			return "\n"
		else:
			return ""

	def generateNode(self,NVDAObject):
		uniqueID=NVDAObject.childID
		text=""
		nodes=[]
		text+=self.getStartTag(NVDAObject)
		childCount=0
		try:
			child=NVDAObject.firstChild
		except:
			child=None
		while child:
			childCount+=1
			(childNodes,childText)=self.generateNode(child)
			if (len(text)>0) and (len(childText)>0) and (text[-1]=='\n') and (childText[0]=='\n'):
				text=text[:-1]
			for j in range(len(childNodes)):
				childNodes[j][2]+=len(text)
				childNodes[j][3]+=len(text)
			text+=childText
			nodes+=childNodes
			try:
				child=child.next
			except:
				child=None
		text+=self.getEndTag(NVDAObject)
		if (len(text)>0) and (text[0]=='\n'):
			start=1
		else:
			start=0
		nodes.insert(0,[uniqueID,childCount,start,len(text)])
		return (nodes,text)
