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
		self.wfile.write(prompt + " ")

	def exit(self):
		self._keepRunning = False

	def handle(self):
		try:
			self.wfile.write("NVDA Remote Python Console\n")
			console = pythonConsole.PythonConsole(outputFunc=self.wfile.write, echoFunc=self.echo, setPromptFunc=self.setPrompt, exitFunc=self.exit)
			console.namespace.update({
				"snap": console.updateNamespaceSnapshotVars,
				"rmSnap": console.removeNamespaceSnapshotVars,
			})

			self._keepRunning = True
			while self._keepRunning:
				line = self.rfile.readline()
				if not line:
					break
				line = line.rstrip("\r\n")
				# Execute in the main thread.
				wx.CallAfter(console.push, line)

		except:
			log.exception("Error handling remote Python console request")

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
