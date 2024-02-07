# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2010-2024 NV Access Limited, Mesar Hameed, Takuya Nishimoto
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
Generates or uses a gettext po file during conversion from markdown to html.
Works as a Python Markdown Extension:
https://python-markdown.github.io/extensions/
"""

import re
import os
from collections.abc import Iterator
from collections import Counter
import polib
from markdown import Extension, Markdown
from markdown.treeprocessors import Treeprocessor


class TranslationExtension(Extension):
	# Magic number, priorities are not well documented.
	# After tables and lists,
	# but before links, images and code spans
	PRIORITY = 25

	def __init__(self, docName: str, potPath: str | None = None, poPath: str | None = None):
		self.potPath = potPath
		self.poPath = poPath
		self.docName = docName
		super().__init__()

	def extendMarkdown(self, md: Markdown):
		processor = TranslationTreeprocessor(md, self.docName, potPath=self.potPath, poPath=self.poPath)
		md.treeprocessors.register(processor, "translation", self.PRIORITY)


class TranslationTreeprocessor(Treeprocessor):

	re_blockAnchor = re.compile(r"^(.*)(\{#.+\})$")

	friendlyTagNames = {
		'p': 'paragraph',
		'ul': 'list',
		'ol': 'list',
		'li': 'list item',
		'table': 'table',
		'tr': 'row',
		'th': 'header cell',
		'td': 'cell',
		'a': 'link',
		'img': 'image',
		'code': 'code span',
		'h1': 'heading level 1',
		'h2': 'heading level 2',
		'h3': 'heading level 3',
		'h4': 'heading level 4',
		'h5': 'heading level 5',
		'h6': 'heading level 6',
	}

	potFile = None
	poFile = None

	def __init__(self, md: Markdown | None, docname: str, potPath: str | None = None, poPath: str | None = None):
		super().__init__(md)
		self.docName = docname
		if potPath:
			if not os.path.exists(potPath):
				print(f"Creating pot file at {potPath}")
				with open(potPath, 'w', encoding='utf-8') as f:
					f.write("#\nmsgid \"\"\nmsgstr \"\"\n")
			else:
				print(f"Loading pot file at {potPath}")
			try:
				self.potFile = polib.pofile(potPath, wrapwidth=0, encoding='utf-8')
			except Exception as e:
				print(f"Error loading / creating pot file: {e}")
				raise
		if poPath:
			if os.path.exists(poPath):
				print(f"Loading po file at {poPath}") 
				try:
					self.poFile = polib.pofile(poPath, encoding='utf-8')
				except Exception as e:
					print(f"Error loading po file: {e}")
					raise
			else:
				print(f"No po file found at {poPath}")
		self.headingPath = []
		self.tagCounters = []
		self.tagPath = []
		self.curHeaderCells = []

	def run(self, root):
		self.tagCounters.append(Counter())
		self.walkTree(root)
		if self.potFile:
			self.potFile.save()

	def addPotEntry(self, text, comment=None, context=None):
		if self.potFile is None:
			return
		newEntry = polib.POEntry(
			msgid=text,
			comment=comment,
			msgctxt=context
		)
		oldEntry = self.potFile.find(st=text, msgctxt=context)
		if oldEntry:
			print(f"Found existing entry for {text}: {oldEntry.msgstr}")
			oldCommentLines = oldEntry.comment.splitlines() if oldEntry.comment else []
			newCommentLines = comment.splitlines() if comment else []
			for newCommentLine in newCommentLines:
				if newCommentLine not in oldCommentLines:
					oldCommentLines.append(newCommentLine)
			oldEntry.comment = "\n".join(oldCommentLines)
		else:
			self.potFile.append(newEntry)

	def lookupPoEntry(self, text, context=None):
		if not self.poFile:
			return
		entry = self.poFile.find(st=text, msgctxt=context)
		if entry and entry.msgstr:
			print(f"Found translation for {context}: {entry.msgstr}")
			return entry.msgstr

	def processText(self, element, str, textOrTail: str):
		content = getattr(element, textOrTail)
		if content is None or content.isspace():
			return
		# Remove line feeds and leading/trailing whitespace
		content = content.strip()
		translatedLines = []
		for line in content.splitlines():
			suffix = ""
			# Strip off any trailing anchres from headings and other block elements.
			m = self.re_blockAnchor .match(line)
			if m:
				line, suffix = m.groups()
			pathString = f" > {self.docName}: "
			pathString += " > ".join(self.headingPath + self.tagPath)
			if textOrTail == 'text':
				tagLabel = self.makeTagLabel(element)
				pathString = " > ".join([pathString, tagLabel])
			self.addPotEntry(line, comment=pathString)
			translatedLine = self.lookupPoEntry(content, context=pathString)
			if not translatedLine:
				translatedLine = line
			translatedLine += suffix
			translatedLines.append(translatedLine)
		setattr(element, textOrTail, "\n".join(translatedLines))

	def getTagNumber(self, element):
		return self.tagCounters[-1][element.tag]

	def makeTagLabel(self, element):
		tagNum = self.getTagNumber(element)
		tagLabel = self.friendlyTagNames.get(element.tag)
		if tagLabel:
			if element.tag in ["table", "ul", "ol"]:
				tagLabel += f" {tagNum}"
			if element.tag == 'td' and self.curHeaderCells:
				header = self.curHeaderCells[tagNum - 1]
				tagLabel += f" ({header})"
		return tagLabel

	def recordHeading(self, element):
		level = int(element.tag[1])
		text = element.text
		text = self.re_blockAnchor.sub(r"\1", text)
		self.headingPath[level-2:] = [text]
		self.tagPath = []
		for counter in self.tagCounters:
			counter.clear()

	def walkTree(self, element):
		# Skip over particular paragraphs not needed in translations.
		if element.tag == 'p' and element.text:
			if element.text == '[TOC]':
				# This is a table of contents, ignore it
				return
			if element.text.startswith('\x02'):
				# This is a comment, ignore it
				return
		if element.tag == "th":
			if element.text in (". {.hideHeaderRow}", "."):
				# This is a header cell that should be hidden, ignore it
				return
		addedTag = False
		tagLabel = self.makeTagLabel(element)
		if not tagLabel:
			for child in element:
				self.walkTree(child)
			return
		self.tagCounters[-1][element.tag] += 1
		if element.tag == 'th':
			self.curHeaderCells.append(element.text)
		self.processText(element, tagLabel, 'text')
		self.processText(element, tagLabel, 'tail')
		if element.tag != "h1":
			self.tagPath.append(tagLabel)
			self.tagCounters.append(Counter())
			addedTag = True
		if element.tag in ["h2", "h3", "h4", "h5", "h6"]:
			self.recordHeading(element)
		for item in element:
			self.walkTree(item)
		if element.tag == 'table':
			self.curHeaderCells.clear()
		if addedTag and len(self.tagPath) > 0:
			self.tagPath.pop()
			self.tagCounters.pop()
