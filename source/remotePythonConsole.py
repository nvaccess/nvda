#remotePythonConsole.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2011 NV Access Inc

"""Provides an interactive Python console run inside NVDA which can be accessed via TCP.
"""

import threading
import SocketServer
import wx
import pythonConsole
from logHandler import log

server = None

class RequestHandler(SocketServer.StreamRequestHandler):

	def echo(self, data):
		pass

	def setPrompt(self, prompt):
		if not self._keepRunning:
			# We're about to exit, so don't output the prompt.
			return
		self.wfile.write(prompt + " ")

	def exit(self):
		self._keepRunning = False

	def execute(self, line):
		self.console.push(line)
		# Notify handle() that the line has finished executing.
		self._execDoneEvt.set()

	def handle(self):
		self._keepRunning = True

		try:
			self.wfile.write("NVDA Remote Python Console\n")
			self.console = pythonConsole.PythonConsole(outputFunc=self.wfile.write, echoFunc=self.echo, setPromptFunc=self.setPrompt, exitFunc=self.exit)
			self.console.namespace.update({
				"snap": self.console.updateNamespaceSnapshotVars,
				"rmSnap": self.console.removeNamespaceSnapshotVars,
			})

			self._execDoneEvt = threading.Event()
			while self._keepRunning:
				line = self.rfile.readline()
				if not line:
					break
				line = line.rstrip("\r\n")
				# Execute in the main thread.
				wx.CallAfter(self.execute, line)
				# Wait until the line has finished executing before retrieving the next.
				self._execDoneEvt.wait()
				self._execDoneEvt.clear()

		except:
			log.exception("Error handling remote Python console request")
		finally:
			# Clean up the console.
			self.console = None

def initialize():
	global server
	server = SocketServer.TCPServer(("", 6832), RequestHandler)
	server.daemon_threads = True
	thread = threading.Thread(target=server.serve_forever)
	thread.daemon = True
	thread.start()

def terminate():
	global server
	server.shutdown()
	server = None
