# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2011-2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Provides an interactive Python console run inside NVDA which can be accessed via TCP.
To use, call `initialize` to start the server.
Then, connect to it using TCP port `PORT`.
The server will only handle one connection at a time.
"""

import socketserver
import threading

import pythonConsole
import wx
from logHandler import log

PORT: int = 6832
"""The TCP port on which the server will run."""

server: socketserver.TCPServer | None = None


class RequestHandler(socketserver.StreamRequestHandler):
	_keepRunning: bool
	_execDoneEvt: threading.Event
	console: pythonConsole.PythonConsole | None

	def setPrompt(self, prompt: str) -> None:
		if not self._keepRunning:
			# We're about to exit, so don't output the prompt.
			return
		self._write(prompt + " ")

	def _write(self, text: str) -> None:
		self.wfile.write(text.encode("utf-8", errors="replace"))

	def exit(self) -> None:
		self._keepRunning = False

	def execute(self, line: str) -> None:
		self.console.push(line)
		# Notify handle() that the line has finished executing.
		self._execDoneEvt.set()

	def handle(self) -> None:
		# #3126: Remove the default socket timeout.
		# We can't use the class timeout attribute because None means don't set a timeout.
		self.connection.settimeout(None)
		self._keepRunning = True

		try:
			self._write("NVDA Remote Python Console\n")
			self.console = pythonConsole.PythonConsole(
				outputFunc=self._write,
				setPromptFunc=self.setPrompt,
				exitFunc=self.exit,
			)
			self.console.namespace.update(
				{
					"snap": self.console.updateNamespaceSnapshotVars,
					"rmSnap": self.console.removeNamespaceSnapshotVars,
				},
			)

			self._execDoneEvt = threading.Event()
			while self._keepRunning:
				rawLine = self.rfile.readline()
				if not rawLine:
					break
				line = rawLine.decode("utf-8", errors="replace").rstrip("\r\n")
				# Execute in the main thread.
				wx.CallAfter(self.execute, line)
				# Wait until the line has finished executing before retrieving the next.
				self._execDoneEvt.wait()
				self._execDoneEvt.clear()

		except:  # noqa: E722
			log.exception("Error handling remote Python console request")
		finally:
			# Clean up the console.
			self.console = None


def initialize() -> None:
	global server
	server = socketserver.TCPServer(("", PORT), RequestHandler)
	server.daemon_threads = True
	thread = threading.Thread(
		name=__name__,  # remotePythonConsole
		target=server.serve_forever,
		daemon=True,
	)
	thread.start()


def terminate() -> None:
	global server
	if server is None:
		return
	server.shutdown()
	server.server_close()
	server = None
