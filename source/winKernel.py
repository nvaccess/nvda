#winKernel.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import ctypes
import ctypes.wintypes

kernel32=ctypes.windll.kernel32

#Constants
#Process control
PROCESS_ALL_ACCESS=0x1F0FFF
READ_CONTROL=0x20000
#Console handles
STD_INPUT_HANDLE=-10
STD_OUTPUT_HANDLE=-11
STD_ERROR_HANDLE=-12

class coordType(ctypes.Structure):
	_fields_=[
('x',ctypes.c_short),
('y',ctypes.c_short),
]

class consoleWindowRectType(ctypes.Structure):
	_fields_=[
('left',ctypes.c_short),
('top',ctypes.c_short),
('right',ctypes.c_short),
('bottom',ctypes.c_short),
]

class consoleScreenBufferInfoType(ctypes.Structure):
	_fields_=[
('consoleSize',coordType),
('cursorPosition',coordType),
('attributes',ctypes.c_short),
('windowRect',consoleWindowRectType),
('maxWindowSize',coordType),
]

def attachConsole(processID):
	return kernel32.AttachConsole(processID)

def freeConsole():
	return kernel32.FreeConsole()

def getStdHandle(handleID):
	return kernel32.GetStdHandle(handleID)

def getConsoleProcessList(processList,processCount):
	return kernel32.GetConsoleProcessList(processList,processCount)

def readConsoleOutputCharacter(handle,length,x,y):
	point=coordType()
	point.x=x
	point.y=y
	buf=ctypes.create_unicode_buffer(length)
	kernel32.ReadConsoleOutputCharacterW(handle,buf,length,point,ctypes.byref(ctypes.c_int(0)))
	return buf.value

def getConsoleScreenBufferInfo(handle):
	info=consoleScreenBufferInfoType()
	kernel32.GetConsoleScreenBufferInfo(handle,ctypes.byref(info))
	return info

def openProcess(*args):
	return kernel32.OpenProcess(*args)

def closeHandle(*args):
	return kernel32.CloseHandle(*args)

