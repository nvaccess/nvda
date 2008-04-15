"""Provides an interactive Python console which can be run from within NVDA.
To use, call L{initialize} to create a singleton instance of the console GUI. This can then be accessed externally as L{consoleUI}.
"""

import __builtin__
import code
import sys
import wx
from baseObject import autoPropertyObject
import speech
import queueHandler
import api
import gui

#: The singleton Python console UI instance.
consoleUI = None

class PythonConsole(code.InteractiveConsole, autoPropertyObject):
	"""An interactive Python console which directs output to supplied functions.
	This is necessary for a Python console facilitated by a GUI.
	Input is always received via the L{push} method.
	This console also handles redirection of stdout and stderr and prevents clobbering of the gettext "_" builtin.
	"""

	def __init__(self, outputFunc, echoFunc, setPromptFunc, **kwargs):
		# Can't use super here because stupid code.InteractiveConsole doesn't sub-class object. Grrr!
		code.InteractiveConsole.__init__(self, **kwargs)
		self._output = outputFunc
		self._echo = echoFunc
		self._setPrompt = setPromptFunc
		self.prompt = ">>>"

	def _set_prompt(self, prompt):
		self._prompt = prompt
		self._setPrompt(prompt)

	def _get_prompt(self):
		return self._prompt

	def write(self, data):
		self._output(data)

	def push(self, line):
		self._echo("%s %s\n" % (self.prompt, line))
		# Capture stdout/stderr output as well as code interaction.
		stdout, stderr = sys.stdout, sys.stderr
		sys.stdout = sys.stderr = self
		# Prevent this from messing with the gettext "_" builtin.
		saved_ = __builtin__._
		more = code.InteractiveConsole.push(self, line)
		sys.stdout, sys.stderr = stdout, stderr
		__builtin__._ = saved_
		self.prompt = "..." if more else ">>>"
		return more

class ConsoleUI(wx.Frame):
	"""The NVDA Python console GUI.
	"""

	def __init__(self):
		super(ConsoleUI, self).__init__(None, wx.ID_ANY, _("NVDA Python Console"))
		self.Bind(wx.EVT_CLOSE, self.onClose)
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		self.outputCtrl = wx.TextCtrl(self, wx.ID_ANY, size=(500, 500), style=wx.TE_MULTILINE | wx.TE_READONLY)
		mainSizer.Add(self.outputCtrl, proportion=2, flag=wx.EXPAND)
		inputSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.promptLabel = wx.StaticText(self, wx.ID_ANY)
		inputSizer.Add(self.promptLabel, flag=wx.EXPAND)
		self.inputCtrl = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_DONTWRAP | wx.TE_PROCESS_TAB)
		self.inputCtrl.Bind(wx.EVT_CHAR, self.onInputChar)
		inputSizer.Add(self.inputCtrl, proportion=1, flag=wx.EXPAND)
		mainSizer.Add(inputSizer, proportion=1, flag=wx.EXPAND)
		self.SetSizer(mainSizer)
		mainSizer.Fit(self)

		#: The namespace available to the console. This can be updated externally.
		#: @type: dict
		self.namespace = {}
		self.console = PythonConsole(outputFunc=self.output, echoFunc=self.echo, setPromptFunc=self.setPrompt, locals=self.namespace)
		self.inputHistory = []
		self.inputHistoryPos = 0

		self.inputCtrl.SetFocus()

	def onClose(self, evt):
		self.Hide()

	def output(self, data):
		self.outputCtrl.write(data)
		if data and not data.isspace():
			queueHandler.queueFunction(queueHandler.eventQueue, speech.speakText, data)

	def echo(self, data):
		self.outputCtrl.write(data)

	def setPrompt(self, prompt):
		self.promptLabel.SetLabel(prompt)
		queueHandler.queueFunction(queueHandler.eventQueue, speech.speakText, prompt)

	def execute(self):
		data = self.inputCtrl.GetValue()
		self.console.push(data)
		self.inputHistory.append(data)
		self.inputHistoryPos = len(self.inputHistory)
		self.inputCtrl.ChangeValue("")

	def historyMove(self, movement):
		newIndex = self.inputHistoryPos + movement
		historyLen = len(self.inputHistory)
		if 0 <= newIndex < historyLen:
			self.inputCtrl.ChangeValue(self.inputHistory[newIndex])
		elif newIndex == len(self.inputHistory):
			self.inputCtrl.ChangeValue("")
		else:
			return False
		self.inputHistoryPos = newIndex
		self.inputCtrl.SetInsertionPointEnd()
		return True

	def onInputChar(self, evt):
		key = evt.GetKeyCode()
		if key == wx.WXK_RETURN:
			self.execute()
			return
		elif key in (wx.WXK_UP, wx.WXK_DOWN):
			if self.historyMove(-1 if key == wx.WXK_UP else 1):
				return
		evt.Skip()

	def updateNamespaceSnapshotVars(self):
		"""Update the console namespace with a snapshot of NVDA's current state.
		This creates/updates variables for the current focus, navigator object, etc.
		"""
		self.namespace.update({
			"focus": api.getFocusObject(),
			"focusAnc": api.getFocusAncestors(),
			"fg": api.getForegroundObject(),
			"nav": api.getNavigatorObject(),
			"mouse": api.getMouseObject(),
		})

def initialize():
	"""Initialize the NVDA Python console GUI.
	This creates a singleton instance of the console GUI. This is accessible as L{consoleUI}. This can and should be manipulated externally.
	"""
	global consoleUI
	consoleUI = ConsoleUI()
	gui.topLevelWindows.append(consoleUI)
