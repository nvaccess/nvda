#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2014 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

class HeaderCellInfo(object):
	__slots__=['rowNumber','columnNumber','rowSpan','colSpan','minRowNumber','maxRowNumber','minColumnNumber','maxColumnNumber','name','isRowHeader','isColumnHeader']
	def __init__(self,**kwargs):
		self.rowSpan=self.colSpan=1
		self.minColumnNumber=self.maxColumnNumber=self.minRowNumber=self.maxRowNumber=None
		for  name,value in kwargs.items():
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

	def iterPossibleHeaderCellInfosFor(self,rowNumber,columnNumber,minRowNumber=None,maxRowNumber=None,minColumnNumber=None,maxColumnNumber=None,columnHeader=False):
		for key in self.listByRow: #(self.listByColumn if columnHeader else self.listByRow):
			info=self.infosDict[key]
			if (info.minColumnNumber and info.minColumnNumber>columnNumber) or (info.maxColumnNumber and info.maxColumnNumber<columnNumber) or (info.minRowNumber and info.minRowNumber>rowNumber) or (info.maxRowNumber and info.maxRowNumber<rowNumber):
				# Skipping this possible header as the requested coordinates are outside the header's allowed range
				continue
			if (minColumnNumber and minColumnNumber>info.columnNumber) or (maxColumnNumber and maxColumnNumber<info.columnNumber) or (minRowNumber and minRowNumber>info.rowNumber) or (maxRowNumber and maxRowNumber<info.rowNumber):
				# Skipping this possible header as its coordinates are outside the requested range
				continue
			if (columnHeader and not info.isColumnHeader) or (not columnHeader and not info.isRowHeader):
				# Skipping this possible header as it is the wrong type of header
				continue
			if columnHeader and info.columnNumber<=columnNumber:
				if info.rowNumber<=rowNumber<(info.rowNumber+info.rowSpan):
					# We never want to yield column headers when actually on column headers
					return
				elif (info.rowNumber+info.rowSpan)<=rowNumber:
					# Found a valid column header for these coordinates
					yield info
			if not columnHeader and info.rowNumber<=rowNumber:
				if info.columnNumber<=columnNumber<(info.columnNumber+info.colSpan):
					# We never want to yield row headers when actually on row headers
					return
				elif (info.columnNumber+info.colSpan)<=columnNumber:
					# Found a valid row header for these coordinates
					yield info
