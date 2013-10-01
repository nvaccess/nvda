# -*- coding: UTF-8 -*-
#mathPres.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2013 NV Access Limited

import sys
import os
import louis
from NVDAObjects import NVDAObject
import controlTypes
import braille

import latex_access.path
if getattr(sys, "frozen", None):
	# This is a binary build.
	# Fix the latex_access table path.
	def get_path():
		return os.path.join(sys.prefix, "latex_access")
	latex_access.path.get_path = get_path
import latex_access.speech
import latex_access.ueb

class MathNVDAObject(NVDAObject):

	def getArguments(self, count):
		args = []
		child = self.firstChild
		while child:
			if child.role == controlTypes.ROLE_WHITESPACE:
				child = child.next
				continue
			args.append(child)
			if len(args) == count:
				break
			child = child.next
		return args

	def _get__latex(self):
		return makeLatex(self)

	def _get_name(self):
		return latex_access.speech.speech().translate(self._latex)

	def event_becomeNavigatorObject(self):
		super(MathNVDAObject, self).event_becomeNavigatorObject()
		if not braille.handler.enabled:
			return
		del braille.handler.mainBuffer.regions[-1]
		region = braille.Region()
		region.update = lambda: None
		region.brailleCells = [ord(cell) & 255 for cell in louis.translateString(
			[os.path.join(braille.TABLES_DIR, "en-us-comp8.ctb")],
			latex_access.ueb.ueb().translate(self._latex),
			mode=louis.dotsIO)]
		braille.handler.mainBuffer.regions.append(region)
		braille.handler.mainBuffer.update()
		braille.handler.mainBuffer.updateDisplay()

class _LatexMaker(object):

	CT_PREFIX = "prefix"
	CT_INFIX = "infix"
	COMMANDS = {
		controlTypes.ROLE_MATH_FRACTION: (CT_PREFIX, r"\frac", 2),
		controlTypes.ROLE_MATH_SQRT: (CT_PREFIX, r"\sqrt", 1),
		controlTypes.ROLE_MATH_SUPERSCRIPT: (CT_INFIX, "^", 2),
	}
	CHARS = {
		0x2212: u"-", # −
		0xb1: u"\pm", # ±
		0x2062: None, # invisible times
	}

	def __init__(self, obj):
		self.outText = []
		self.addLatex(obj)
		self.outText = "".join(self.outText)

	def out(self, text):
		self.outText.append(text)

	def addLatex(self, obj):
		role = obj.role
		if role == controlTypes.ROLE_WHITESPACE:
			return
		if role == controlTypes.ROLE_STATICTEXT:
			self.out(obj.name.translate(self.CHARS))
			return

		try:
			ct, command, argCount = self.COMMANDS[role]
		except KeyError:
			ct = None

		if ct and argCount > 1:
			args = obj.getArguments(argCount)
			if ct == self.CT_PREFIX:
				self.out(command)
				for arg in args:
					self.out("{")
					self.addLatex(arg)
					self.out("}")
				return
			elif ct == self.CT_INFIX:
				self.addLatex(args[0])
				self.out(command)
				self.out("{")
				self.addLatex(args[1])
				self.out("}")
				return

		if ct == self.CT_PREFIX:
			self.out(command)
			self.out("{")
		child = obj.firstChild
		while child:
			self.addLatex(child)
			child = child.next
		if ct == self.CT_PREFIX:
			self.out("}")

def makeLatex(obj):
	return _LatexMaker(obj).outText
