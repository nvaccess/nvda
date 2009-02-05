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

	def __init__(self,conn):
		asynchat.async_chat.__init__(self, conn)
		self.set_terminator("konec")

	def collect_incoming_data(self, data):
		self.inputBuf+=data

	def found_terminator(self):
		log.io("Incoming tandem command: %s"%self.inputBuf)
		command = self.inputBuf[0]
		self.inputBuf= self.inputBuf[1:]
		self.processCommand(command,self.inputBuf)
		self.inputBuf = ""

	def processCommand(self,command,data):
		if command == command_keyDown:
			vkCode,scanCode,extended,injected = data.split(" ")
			keyboardHandler.internal_keyDownEvent(vkCode,scanCode,extended,injected)
		elif command == command_keyUp:
			vkCode,scanCode,extended,injected = data.split(" ")
			keyboardHandler.internal_keyUpEvent(vkCode,scanCode,extended,injected)
		elif command == command_closeConnection:
			self.close_when_done()

class ServerSession(Session):
	parent = None

	def __init__(self,conn,parent):
		Session.__init__(self, conn)
		self.parent = parent
		self.parent.clients.append(self)

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
		client = ServerSession(sock, self)

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
