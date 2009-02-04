import asyncore, asynchat, socket
import globalVars
import keyboardHandler
from logHandler import log

#constants
command_closeConnection = "0"
command_keyDown = "1"
command_keyUp = "2"
serverPort = 2402

#global definitions
server = None
class Session(asynchat.async_chat):
	inputBuf = ""
	parent = None

	def __init__(self,conn,parent):
		asynchat.async_chat.__init__(self, conn)
		self.set_terminator("konec")
		self.parent = parent
		self.parent.clients.append(self)

	def collect_incoming_data(self, data):
		self.inputBuf+=data

	def found_terminator(self):
		log.io("Remote client command: %s"%self.inputBuf)
		command = self.inputBuf[0]
		self.inputBuf= self.inputBuf[1:]
		if command == command_keyDown:
			vkCode,scanCode,extended,injected = self.inputBuf.split(" ")
			keyboardHandler.internal_keyDownEvent(vkCode,scanCode,extended,injected)
		elif command == command_keyUp:
			vkCode,scanCode,extended,injected = self.inputBuf.split(" ")
			keyboardHandler.internal_keyUpEvent(vkCode,scanCode,extended,injected)
		elif command == command_closeConnection:
			self.close_when_done()
		self.inputBuf = ""

	def handle_close(self):
		self.parent.clients.remove(self)
		log.info("disconected tandem client")
		asynchat.async_chat.handle_close(self)

class TandemServer(asynchat.async_chat):
	clients = []

	def __init__(self):
		log.info("Starting tandem server")
		asynchat.async_chat.__init__(self)
		globalVars.tandemServerActive = True
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind(('', 2402))
		self.listen(2)
		log.debug("Listening tandem connections")

	def handle_accept(self):
		sock, addr = self.accept()
		log.info("incoming tandem connection")
		log.debug(addr)
		client = Session(sock, self)

	def sendToAll(self,data):
		for client in self.clients:
			client.push(data)

	def close(self):
		for client in self.clients: client.close_when_done()
		globalVars.tandemServerActive = False
		log.info("Tandem server stopped")

def update():
	asyncore.poll()

def startTandemServer():
	if globalVars.tandemServerActive: return
	global server
	server = TandemServer()

def stopTandemServer():
	global server
	if server is None: return
	server.close()
	server = None