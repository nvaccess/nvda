#brailleDisplayDrivers/freedomScientific.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2008-2011 Michael Curran <mick@kulgan.net>, James Teh <jamie@jantrid.net>

from ctypes import *
from ctypes.wintypes import *
from collections import OrderedDict
import itertools
import hwPortUtils
import braille
import inputCore
from baseObject import ScriptableObject
from winUser import WNDCLASSEXW, WNDPROC, LRESULT, HCURSOR
from logHandler import log
import brailleInput

#Try to load the fs braille dll
try:
	fsbLib=windll.fsbrldspapi
except:
	fsbLib=None

#Map the needed functions in the fs braille dll
if fsbLib:
	fbOpen=getattr(fsbLib,'_fbOpen@12')
	fbGetCellCount=getattr(fsbLib,'_fbGetCellCount@4')
	fbWrite=getattr(fsbLib,'_fbWrite@16')
	fbClose=getattr(fsbLib,'_fbClose@4')
	fbConfigure=getattr(fsbLib, '_fbConfigure@8')
	fbGetDisplayName=getattr(fsbLib, "_fbGetDisplayName@12")
	fbGetFirmwareVersion=getattr(fsbLib,  "_fbGetFirmwareVersion@12")
	fbBeep=getattr(fsbLib, "_fbBeep@4")

FB_INPUT=1
FB_DISCONNECT=2
FB_EXT_KEY=3

LRESULT=c_long
HCURSOR=c_long

appInstance=windll.kernel32.GetModuleHandleW(None)

nvdaFsBrlWm=windll.user32.RegisterWindowMessageW(u"nvdaFsBrlWm")

inputType_keys=3
inputType_routing=4
inputType_wizWheel=5

# Names of freedom scientific bluetooth devices
bluetoothNames = (
	"F14", "Focus 14 BT",
	"Focus 40 BT",
	"Focus 80 BT",
)

keysPressed=0
extendedKeysPressed=0
@WNDPROC
def nvdaFsBrlWndProc(hwnd,msg,wParam,lParam):
	global keysPressed, extendedKeysPressed
	keysDown=0
	extendedKeysDown=0
	if msg==nvdaFsBrlWm and wParam in (FB_INPUT, FB_EXT_KEY):
		if wParam==FB_INPUT:
			inputType=lParam&0xff
			if inputType==inputType_keys:
				keyBits=lParam>>8
				keysDown=keyBits
				keysPressed |= keyBits
			elif inputType==inputType_routing:
				routingIndex=(lParam>>8)&0xff
				isRoutingPressed=bool((lParam>>16)&0xff)
				isTopRoutingRow=bool((lParam>>24)&0xff)
				if isRoutingPressed:
					gesture=RoutingGesture(routingIndex,isTopRoutingRow)
					try:
						inputCore.manager.executeGesture(gesture)
					except inputCore.NoInputGestureAction:
						pass
			elif inputType==inputType_wizWheel:
				numUnits=(lParam>>8)&0x7
				isRight=bool((lParam>>12)&1)
				isDown=bool((lParam>>11)&1)
				#Right's up and down are rversed, but NVDA does not want this
				if isRight: isDown=not isDown
				for unit in xrange(numUnits):
					gesture=WizWheelGesture(isDown,isRight)
					try:
						inputCore.manager.executeGesture(gesture)
					except inputCore.NoInputGestureAction:
						pass
		elif wParam==FB_EXT_KEY:
			keyBits=lParam>>4
			extendedKeysDown=keyBits
			extendedKeysPressed|=keyBits
		if keysDown==0 and extendedKeysDown==0 and (keysPressed!=0 or extendedKeysPressed!=0):
			gesture=KeyGesture(keysPressed,extendedKeysPressed)
			keysPressed=extendedKeysPressed=0
			try:
				inputCore.manager.executeGesture(gesture)
			except inputCore.NoInputGestureAction:
				pass
		return 0
	else:
		return windll.user32.DefWindowProcW(hwnd,msg,wParam,lParam)

nvdaFsBrlWndCls=WNDCLASSEXW()
nvdaFsBrlWndCls.cbSize=sizeof(nvdaFsBrlWndCls)
nvdaFsBrlWndCls.lpfnWndProc=nvdaFsBrlWndProc
nvdaFsBrlWndCls.hInstance=appInstance
nvdaFsBrlWndCls.lpszClassName=u"nvdaFsBrlWndCls"

class BrailleDisplayDriver(braille.BrailleDisplayDriver,ScriptableObject):

	name="freedomScientific"
	# Translators: Names of braille displays.
	description=_("Freedom Scientific Focus/PAC Mate series")

	@classmethod
	def check(cls):
		return bool(fsbLib)

	@classmethod
	def getPossiblePorts(cls):
		ports = OrderedDict([cls.AUTOMATIC_PORT, ("USB", "USB",)])
		try:
			cls._getBluetoothPorts().next()
			ports["bluetooth"] = "Bluetooth"
		except StopIteration:
			pass
		return ports

	@classmethod
	def _getBluetoothPorts(cls):
		for p in hwPortUtils.listComPorts():
			try:
				btName = p["bluetoothName"]
			except KeyError:
				continue
			if not any(btName == prefix or btName.startswith(prefix + " ") for prefix in bluetoothNames):
				continue
			yield p["port"].encode("mbcs")

	wizWheelActions=[
		# Translators: The name of a key on a braille display, that scrolls the display to show previous/next part of a long line.
		(_("display scroll"),("globalCommands","GlobalCommands","braille_scrollBack"),("globalCommands","GlobalCommands","braille_scrollForward")),
		# Translators: The name of a key on a braille display, that scrolls the display to show the next/previous line.
		(_("line scroll"),("globalCommands","GlobalCommands","braille_previousLine"),("globalCommands","GlobalCommands","braille_nextLine")),
	]

	def __init__(self, port="auto"):
		self.leftWizWheelActionCycle=itertools.cycle(self.wizWheelActions)
		action=self.leftWizWheelActionCycle.next()
		self.gestureMap.add("br(freedomScientific):leftWizWheelUp",*action[1])
		self.gestureMap.add("br(freedomScientific):leftWizWheelDown",*action[2])
		self.rightWizWheelActionCycle=itertools.cycle(self.wizWheelActions)
		action=self.rightWizWheelActionCycle.next()
		self.gestureMap.add("br(freedomScientific):rightWizWheelUp",*action[1])
		self.gestureMap.add("br(freedomScientific):rightWizWheelDown",*action[2])
		super(BrailleDisplayDriver,self).__init__()
		self._messageWindowClassAtom=windll.user32.RegisterClassExW(byref(nvdaFsBrlWndCls))
		self._messageWindow=windll.user32.CreateWindowExW(0,self._messageWindowClassAtom,u"nvdaFsBrlWndCls window",0,0,0,0,0,None,None,appInstance,None)
		if port == "auto":
			portsToTry = itertools.chain(["USB"], self._getBluetoothPorts())
		elif port == "bluetooth":
			portsToTry = self._getBluetoothPorts()
		else: # USB
			portsToTry = ["USB"]
		fbHandle=-1
		for port in portsToTry:
			fbHandle=fbOpen(port,self._messageWindow,nvdaFsBrlWm)
			if fbHandle!=-1:
				break
		if fbHandle==-1:
			windll.user32.DestroyWindow(self._messageWindow)
			windll.user32.UnregisterClassW(self._messageWindowClassAtom,appInstance)
			raise RuntimeError("No display found")
		self.fbHandle=fbHandle
		self._configureDisplay()
		numCells=self.numCells
		self.gestureMap.add("br(freedomScientific):topRouting1","globalCommands","GlobalCommands","braille_scrollBack")
		self.gestureMap.add("br(freedomScientific):topRouting%d"%numCells,"globalCommands","GlobalCommands","braille_scrollForward")

	def terminate(self):
		super(BrailleDisplayDriver,self).terminate()
		fbClose(self.fbHandle)
		windll.user32.DestroyWindow(self._messageWindow)
		windll.user32.UnregisterClassW(self._messageWindowClassAtom,appInstance)

	def _get_numCells(self):
		return fbGetCellCount(self.fbHandle)

	def display(self,cells):
		cells="".join([chr(x) for x in cells])
		fbWrite(self.fbHandle,0,len(cells),cells)

	def _configureDisplay(self):
		# See what display we are connected to
		displayName= firmwareVersion=""
		buf = create_string_buffer(16)
		if fbGetDisplayName(self.fbHandle, buf, 16):
			displayName=buf.value
		if fbGetFirmwareVersion(self.fbHandle, buf, 16):
			firmwareVersion=buf.value
		if displayName and firmwareVersion and displayName=="Focus" and ord(firmwareVersion[0])>=ord('3'):
			# Focus 2 or later. Make sure extended keys support is enabled.
			log.debug("Activating extended keys on freedom Scientific display. Display name: %s, firmware version: %s.", displayName, firmwareVersion)
			fbConfigure(self.fbHandle, 0x02)

	def script_toggleLeftWizWheelAction(self,gesture):
		action=self.leftWizWheelActionCycle.next()
		self.gestureMap.add("br(freedomScientific):leftWizWheelUp",*action[1],replace=True)
		self.gestureMap.add("br(freedomScientific):leftWizWheelDown",*action[2],replace=True)
		braille.handler.message(action[0])

	def script_toggleRightWizWheelAction(self,gesture):
		action=self.rightWizWheelActionCycle.next()
		self.gestureMap.add("br(freedomScientific):rightWizWheelUp",*action[1],replace=True)
		self.gestureMap.add("br(freedomScientific):rightWizWheelDown",*action[2],replace=True)
		braille.handler.message(action[0])

	__gestures={
		"br(freedomScientific):leftWizWheelPress":"toggleLeftWizWheelAction",
		"br(freedomScientific):rightWizWheelPress":"toggleRightWizWheelAction",
	}

	gestureMap=inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands" : {
			"braille_routeTo":("br(freedomScientific):routing",),
			"braille_scrollBack" : ("br(freedomScientific):leftAdvanceBar", "br(freedomScientific]:leftBumperBarUp","br(freedomScientific):rightBumperBarUp",),
			"braille_scrollForward" : ("br(freedomScientific):rightAdvanceBar","br(freedomScientific):leftBumperBarDown","br(freedomScientific):rightBumperBarDown",),
			"braille_previousLine" : ("br(freedomScientific):leftRockerBarUp", "br(freedomScientific):rightRockerBarUp",),
			"braille_nextLine" : ("br(freedomScientific):leftRockerBarDown", "br(freedomScientific):rightRockerBarDown",),
			"kb:backspace" : ("br(freedomScientific):dot7",),
			"kb:enter" : ("br(freedomScientific):dot8",),
			"kb:shift+tab": ("br(freedomScientific):dot1+dot2+brailleSpaceBar",),
			"kb:tab" : ("br(freedomScientific):dot4+dot5+brailleSpaceBar",),
			"kb:upArrow" : ("br(freedomScientific):dot1+brailleSpaceBar",),
			"kb:downArrow" : ("br(freedomScientific):dot4+brailleSpaceBar",),
			"kb:leftArrow" : ("br(freedomScientific):dot3+brailleSpaceBar",),
			"kb:rightArrow" : ("br(freedomScientific):dot6+brailleSpaceBar",),
			"kb:control+leftArrow" : ("br(freedomScientific):dot2+brailleSpaceBar",),
			"kb:control+rightArrow" : ("br(freedomScientific):dot5+brailleSpaceBar",),
			"kb:home" : ("br(freedomScientific):dot1+dot3+brailleSpaceBar",),
			"kb:control+home" : ("br(freedomScientific):dot1+dot2+dot3+brailleSpaceBar",),
			"kb:end" : ("br(freedomScientific):dot4+dot6+brailleSpaceBar",),
			"kb:control+end" : ("br(freedomScientific):dot4+dot5+dot6+brailleSpaceBar",),
			"kb:alt" : ("br(freedomScientific):dot1+dot3+dot4+brailleSpaceBar",),
			"kb:alt+tab" : ("br(freedomScientific):dot2+dot3+dot4+dot5+brailleSpaceBar",),
			"kb:escape" : ("br(freedomScientific):dot1+dot5+brailleSpaceBar",),
			"kb:windows" : ("br(freedomScientific):dot2+dot4+dot5+dot6+brailleSpaceBar",),
			"kb:windows+d" : ("br(freedomScientific):dot1+dot2+dot3+dot4+dot5+dot6+brailleSpaceBar",),
			"reportCurrentLine" : ("br(freedomScientific):dot1+dot4+brailleSpaceBar",),
			"showGui" :("br(freedomScientific):dot1+dot3+dot4+dot5+brailleSpaceBar",),
			"braille_toggleTether" : ("br(freedomScientific):leftGDFButton+rightGDFButton",),
		}
	})

class InputGesture(braille.BrailleDisplayGesture):
	source = BrailleDisplayDriver.name

class KeyGesture(InputGesture, brailleInput.BrailleInputGesture):

	keyLabels=[
		#Braille keys (byte 1)
		'dot1','dot2','dot3','dot4','dot5','dot6','dot7','dot8',
		#Assorted keys (byte 2)
		'leftWizWheelPress','rightWizWheelPress',
		'leftShiftKey','rightShiftKey',
		'leftAdvanceBar','rightAdvanceBar',
		None,
		'brailleSpaceBar',
		#GDF keys (byte 3)
		'leftGDFButton','rightGDFButton',
		None,
		'leftBumperBarUp','leftBumperBarDown','rightBumperBarUp','rightBumperBarDown',
	]
	extendedKeyLabels = [
	# Rocker bar keys.
	"leftRockerBarUp", "leftRockerBarDown", "rightRockerBarUp", "rightRockerBarDown",
	]

	def __init__(self,keyBits, extendedKeyBits):
		super(KeyGesture,self).__init__()
		keys=[self.keyLabels[num] for num in xrange(24) if (keyBits>>num)&1]
		extendedKeys=[self.extendedKeyLabels[num] for num in xrange(4) if (extendedKeyBits>>num)&1]
		self.id="+".join(set(keys+extendedKeys))
		# Don't say is this a dots gesture if some keys either from dots and space are pressed.
		if not extendedKeyBits and not keyBits & ~(0xff | (1 << 0xf)):
			self.dots = keyBits & 0xff
			# Is space?
			if keyBits & (1 << 0xf):
				self.space = True

class RoutingGesture(InputGesture):

	def __init__(self,routingIndex,topRow=False):
		if topRow:
			self.id="topRouting%d"%(routingIndex+1)
		else:
			self.id="routing"
			self.routingIndex=routingIndex
		super(RoutingGesture,self).__init__()

class WizWheelGesture(InputGesture):

	def __init__(self,isDown,isRight):
		which="right" if isRight else "left"
		direction="Down" if isDown else "Up"
		self.id="%sWizWheel%s"%(which,direction)
		super(WizWheelGesture,self).__init__()
