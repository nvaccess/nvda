#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2014 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

class HeaderCellInfo(object):
	__slots__=['rowNumber','columnNumber','rowSpan','colSpan','minRowNumber','maxRowNumber','minColumnNumber','maxColumnNumber','name','isRowHeader','isColumnHeader']
	def __init__(self,**kwargs):
		self.minColumnNumber=self.maxColumnNumber=self.minRowNumber=self.maxRowNumber=None
		for  name,value in kwargs.iteritems():
			setattr(self,name,value)

class HeaderCellTracker(object):

	def __init__(self):
		self.infosDict={}
		self.listByRow=[]
		self.listByColumn=[]

	def addHeaderCellInfo(self,**kwargs):
		info=HeaderCellInfo(**kwargs)
		key=(info.rowNumber,info.columnNumber)
		self.infosDict[key]=info
		self.listByRow.append(key)
		self.listByRow.sort(reverse=True)
		self.listByColumn.append(key)
		self.listByColumn.sort(key=lambda k: (k[1],k[0]),reverse=True)

	def removeHeaderCellInfo(self,info):
		key=(info.rowNumber,info.columnNumber)
		self.listByRow.remove(key)
		self.listByColumn.remove(key)
		del self.infosDict[key]

	def getHeaderCellInfoAt(self,rowNumber,columnNumber):
		return self.infosDict.get((rowNumber,columnNumber))

	def iterPossibleHeaderCellInfosFor(self,rowNumber,columnNumber,columnHeader=False):
		for key in (self.listByColumn if columnHeader else self.listByRow):
			info=self.infosDict[key]
			if (info.minColumnNumber and info.minColumnNumber>columnNumber) or (info.maxColumnNumber and info.maxColumnNumber<columnNumber) or (info.minRowNumber and info.minRowNumber>rowNumber) or (info.maxRowNumber and info.maxRowNumber<rowNumber):
				continue
			if (columnHeader and info.isColumnHeader and (info.rowNumber+info.rowSpan-1)<rowNumber and info.columnNumber<=columnNumber) or (not columnHeader and info.isRowHeader and (info.columnNumber+info.colSpan-1)<columnNumber and info.rowNumber<=rowNumber):
				yield info
