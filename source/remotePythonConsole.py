#remotePythonConsole.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2011 NV Access Inc

"""Provides an interactive Python console run inside NVDA which can be accessed via TCP.
To use, call L{initialize} to start the server.
Then, connect to it using TCP port L{PORT}.
The server will only handle one connection at a time.
"""

import threading
import socketserver
import wx
import pythonConsole
from logHandler import log

#: The TCP port on which the server will run.
#: @type: int
PORT = 6832

server = None

class RequestHandler(socketserver.StreamRequestHandler):

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
		# #3126: Remove the default socket timeout.
		# We can't use the class timeout attribute because None means don't set a timeout.
		self.connection.settimeout(None)
		self._keepRunning = True

		try:
			self.wfile.write("NVDA Remote Python Console\n")
			self.console = pythonConsole.PythonConsole(outputFunc=self.wfile.write, setPromptFunc=self.setPrompt, exitFunc=self.exit)
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
	server = socketserver.TCPServer(("", PORT), RequestHandler)
	server.daemon_threads = True
	thread = threading.Thread(
		name=__name__,  # remotePythonConsole
		target=server.serve_forever
	)
	thread.daemon = True
	thread.start()

def terminate():
	global server
	server.shutdown()
	server = None
