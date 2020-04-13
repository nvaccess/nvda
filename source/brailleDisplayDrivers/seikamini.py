#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2012/20 Ulf Beckmann <beckmann@flusoft.de>
#20/02/10 8:57

# This file represents the braille display driver for
# Seika Mini, a product from Nippon Telesoft
# see www.seika-braille.com for more details
# 09.06.2012
# Dec14/Jan15 add BrilleInput

from typing import Optional, List
from ctypes import *
import time
import wx
import braille
import brailleInput
import inputCore
import hwPortUtils
import winUser 
import os
from logHandler import log

READ_INTERVAL = 50

DOT_1 = 0x1
DOT_2 = 0x2
DOT_3 = 0x4
DOT_4 = 0x8
DOT_5 = 0x10
DOT_6 = 0x20
DOT_7 = 0x40
DOT_8 = 0x80


_keyNames = {
0x000001 : "BACKSPACE",
0x000002 : "SPACE",
0x000004 : "LB",
0x000008 : "RB",
0x000010 : "LJ_CENTER", 
0x000020 : "LJ_LEFT", 
0x000040 : "LJ_RIGHT", 
0x000080 : "LJ_UP",
0x000100 : "LJ_DOWN",
0x000200 : "RJ_CENTER", 
0x000400 : "RJ_LEFT", 
0x000800 : "RJ_RIGHT", 
0x001000 : "RJ_UP", 
0x002000 : "RJ_DOWN"
}

_dotNames = {}
for i in range(1,9):
	key = globals()["DOT_%d" % i]
	_dotNames[key] = "d%d" % i


# try to load the SeikaDevice.dll
# first get the path of the SeikaMini.py
# get the current work directory
# change to this directory
# load the .dll, the SeikaDevice.dll can also load by Pathname + dllname
#      but not the SLABxxx.dll's
# after loading, set the path back to the work path 

BASE_PATH = os.path.dirname(__file__)
DLLNAME = "Seika\\SeikaDevice.dll"
WORK_PATH = os.getcwd()

if not os.path.isfile(BASE_PATH+"\\"+DLLNAME):
	BASE_PATH = "brailleDisplayDrivers"
os.chdir(BASE_PATH)
try:
	seikaDll=cdll.LoadLibrary(DLLNAME)
except:
	seikaDll=None
	log.info("LoadLibrary failed " + DLLNAME)
os.chdir(WORK_PATH)

class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	name = "seikamini"
	description = "Seika Notetaker"

	numCells = 0
	# numBtns = 0

	@classmethod
	def check(cls):
		return bool(seikaDll)

	def seika_errcheck(res, func, args):
		if res != 0:
			raise RuntimeError("seikamini: %s: code %d" % (func.__name__, res))
		return res

	def __init__(self):
		super(BrailleDisplayDriver, self).__init__()
		pint = c_int * 1
		nCells = pint(0)
		nBut = pint(0)
		pN = ""

		# seikaDll.BrailleOpen.errcheck=self.seika_errcheck
		seikaDll.BrailleOpen.restype=c_int
		seikaDll.BrailleOpen.argtype=(c_int,c_int)

		# seikaDll.GetBrailleDisplayInfo.errcheck=self.seika_errcheck
		seikaDll.GetBrailleDisplayInfo.restype=c_int
		seikaDll.GetBrailleDisplayInfo.argtype=(c_void_p,c_void_p)

		# seikaDll.UpdateBrailleDisplay.errcheck=self.seika_errcheck
		seikaDll.UpdateBrailleDisplay.restype=c_int
		seikaDll.UpdateBrailleDisplay.argtype=(POINTER(c_ubyte),c_int)

		# seikaDll.GetBrailleKey.errcheck=self.seika_errcheck
		seikaDll.GetBrailleKey.restype=c_int
		seikaDll.GetBrailleKey.argtype=(c_void_p,c_void_p)

		seikaDll.BrailleClose.restype=c_int

		if seikaDll.BrailleOpen(2,0): # test USB
			seikaDll.GetBrailleDisplayInfo(nCells,nBut)
			log.info("seikamini an USB-HID, Cells {c} Buttons {b}".format(c=nCells[0], b=nBut[0]))
			self.numCells=nCells[0]
			# 
		else: # search the blutooth ports
			for portInfo in sorted(hwPortUtils.listComPorts(onlyAvailable=True), key=lambda item: "bluetoothName" in item):
				port = portInfo["port"]
				hwID = portInfo["hardwareID"]
				if not hwID.startswith(r"BTHENUM"): # Bluetooth Ports
					continue
				bName = ""
				try:
					bName = portInfo["bluetoothName"]
				except KeyError:
					continue
				if not bName.startswith(r"TSM"): # seikamini and then the 4-Digits
					continue

				try:
					pN = port.split("COM")[1]
				except IndexError:
					pN = "0"
				portNum = int(pN,10)
				log.info("seikamini test {c}, {b}".format(c=port, b=bName))
				if seikaDll.BrailleOpen(0,portNum):
					seikaDll.GetBrailleDisplayInfo(nCells,nBut)
					log.info("seikamini via Bluetooth {p} Cells {c} Buttons {b}".format(p=port,c=nCells[0], b=nBut[0]))
					self.numCells=nCells[0]
					# self.numBtns=nBut[0]
					break
			else:
				raise RuntimeError("No MINI-SEIKA display found")
		self._readTimer = wx.PyTimer(self.handleResponses)
		self._readTimer.Start(READ_INTERVAL)

	def terminate(self):
		try:
			super(BrailleDisplayDriver, self).terminate()
			self._readTimer.Stop()
			self._readTimer = None
		finally:
			seikaDll.BrailleClose()

	def display(self, cells: List[int]):
		# cells will already be padded up to numCells.
		cellBytes = bytes(cells)
		seikaDll.UpdateBrailleDisplay(cellBytes,self.numCells)

	def handleResponses(self):
		pint = c_int * 1
		nKey = pint(0)
		nRou = pint(0)
		Key = 0
		Brl = 0
		Rou = 0
		Btn = 0
		keys= set()
		if seikaDll.GetBrailleKey(nKey,nRou):
			Rou = nRou[0]
			Btn = (nKey[0] & 0xff) << 16
			Brl = (nKey[0] >> 8) & 0xff
			Key = (nKey[0] >> 16) & 0xffff
			space = (nKey[0] >> 16) & 0x2
			log.info("GBK Key{c}-Brl{a}-Routing{b}".format(c=Key, b=Rou, a=Brl))
#			log.info("Seika Brl {brl} Key {c} Buttons {b} Route {r}".format(brl=Brl, c=Key, b=Btn, r=Rou))
			if not (Rou or Key or Btn or Brl):
				pass
			if Rou: # Routing key is pressed
				gesture = InputGestureRouting(Rou-1)
				try:
					inputCore.manager.executeGesture(gesture)
				except inputCore.NoInputGestureAction:
					log.debug("No Action for routing command")
					pass

			if Key: # Mini Seika has 2 Top and 4 Front ....
				gesture = InputGesture(keys=Key)
			if Btn: # Mini Seika has no Btn ....
       				gesture = InputGesture(keys=Btn)
			if Brl: # or how to handle Brailleinput?
				gesture = InputGesture(dots=Brl)
			if Key or Btn or Brl:
				try:
					inputCore.manager.executeGesture(gesture)
				except inputCore.NoInputGestureAction:
					log.debug("No Action for keys ")
					pass



	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"braille_routeTo": ("br(seikamini):routing",),
			"braille_scrollBack": ("br(seikamini):LB",),
			"braille_scrollForward": ("br(seikamini):RB",),
			"braille_previousLine": ("br(seikamini):LJ_UP",),
			"braille_nextLine": ("br(seikamini):LJ_DOWN",),
			"braille_toggleTether": ("br(seikamini):LJ_CENTER",),
			"sayAll": ("br(seikamini):SPACE+BACKSPACE",),
			"showGui": ("br(seikamini):RB+LB",),
			"kb:tab": ("br(seikamini):LJ_RIGHT",),
			"kb:shift+tab": ("br(seikamini):LJ_LEFT",),
			"kb:upArrow": ("br(seikamini):RJ_UP",),
			"kb:downArrow": ("br(seikamini):RJ_DOWN",),
			"kb:leftArrow": ("br(seikamini):RJ_LEFT",),
			"kb:rightArrow": ("br(seikamini):RJ_RIGHT",),
			"kb:shift+upArrow": ("br(seikamini):SPACE+RJ_UP",),
			"kb:shift+downArrow": ("br(seikamini):SPACE+RJ_DOWN",),
			"kb:shift+leftArrow": ("br(seikamini):SPACE+RJ_LEFT",),
			"kb:shift+rightArrow": ("br(seikamini):SPACE+RJ_RIGHT",),
			"kb:escape": ("br(seikamini):SPACE+RJ_CENTER",),
			"kb:shift+upArrow": ("br(seikamini):BACKSPACE+RJ_UP",),
			"kb:shift+downArrow": ("br(seikamini):BACKSPACE+RJ_DOWN",),
			"kb:shift+leftArrow": ("br(seikamini):BACKSPACE+RJ_LEFT",),
			"kb:shift+rightArrow": ("br(seikamini):BACKSPACE+RJ_RIGHT",),
			"kb:windows": ("br(seikamini):BACKSPACE+RJ_CENTER",),
			"kb:space": ("br(seikamini):BACKSPACE","br(seikamini):SPACE",),
			"kb:backspace": ("br(seikamini):d7",),
			"kb:pageup": ("br(seikamini):SPACE+LJ_RIGHT",),
			"kb:pagedown": ("br(seikamini):SPACE+LJ_LEFT",),
			"kb:home": ("br(seikamini):SPACE+LJ_UP",),
			"kb:end": ("br(seikamini):SPACE+LJ_DOWN",),
			"kb:control+home": ("br(seikamini):BACKSPACE+LJ_UP",),
			"kb:control+end": ("br(seikamini):BACKSPACE+LJ_DOWN",),
			"kb:enter": ("br(seikamini):RJ_CENTER","br(seikamini):d8"),
		},
	})


class InputGestureRouting(braille.BrailleDisplayGesture):

	source = BrailleDisplayDriver.name
	def __init__(self, index):
		super(InputGestureRouting, self).__init__()
		self.id = "routing"
		self.routingIndex = index

class InputGesture(braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture):
	source = BrailleDisplayDriver.name

	def __init__(self, keys=None, dots=None, space=False, routing=None):
		super(braille.BrailleDisplayGesture, self).__init__()
		# see what thumb keys are pressed:
		names = set()
		if keys is not None:
			names.update(_keyNames[1 << i] for i in range(22)
					if (1 << i) & keys)
		elif dots is not None:
		# now the dots
			self.dots = dots
			if space:
				self.space = space
				names.add(_keyNames[0])
			names.update(_dotNames[1 << i] for i in range(8)
					if (1 << i) & dots)
		elif routing is not None:
			self.routingIndex = routing
			names.add('routing')
		self.id = "+".join(names)
#		log.info("keys {keys}".format(keys=names))