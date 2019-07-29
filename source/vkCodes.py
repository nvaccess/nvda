#vkCodes.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2007-2010 Michael Curran <mick@kulgan.net>, James Teh <jamie@jantrid.net>

"""Maps between Windows virtual key (vk) codes and NVDA key names.
These names are used when binding keyboard gestures to scripts.
"""

#: Maps vk codes to key names.
#: The dict key is a tuple of (vkCode, extended),
#: where vkCode is the vk code and extended is a bool specifying whether the key is an extended key.
#: If extended is C{None}, the extended state of the key is irrelevant to the mapping;
#: i.e. the name is the same in either case.
#: The dict value is the key name.
#: @type: dict with keys of tuple(int, bool) and values of str
byCode = {
	(0x01, None): "leftMouse",
	(0x02, None): "rightMouse",
	(0x03, None): "break",
	(0x04, None): "middleMouse",
	(0x08, None): "backspace",
	(0x09, None): "tab",
	(0x0C, None): "numpad5",
	(0x0D, False): "enter",
	(0x0D, True): "numpadEnter",
	(0x10, None): "shift",
	(0x11, None): "control",
	(0x12, None): "alt",
	(0x13, None): "pause",
	(0x14, None): "capsLock",
	(0x18, None): "IMEFinalMode",
	(0x1B, None): "escape",
	(0x1C, None): "IMEConvert",
	(0x1D, None): "IMENonconvert",
	(0x1E, None): "IMEAccept",
	(0x1F, None): "IMEModeChange",
	(0x20, None): "space",
	(0x21, True): "pageUp",
	(0x21, False): "numpad9",
	(0x22, True): "pageDown",
	(0x22, False): "numpad3",
	(0x23, True): "end",
	(0x23, False): "numpad1",
	(0x24, True): "home",
	(0x24, False): "numpad7",
	(0x25, True): "leftArrow",
	(0x25, False): "numpad4",
	(0x26, True): "upArrow",
	(0x26, False): "numpad8",
	(0x27, True): "rightArrow",
	(0x27, False): "numpad6",
	(0x28, True): "downArrow",
	(0x28, False): "numpad2",
	(0x29, None): "select",
	(0x2A, None): "print",
	(0x2B, None): "execute",
	(0x2C, None): "printScreen",
	(0x2D, True): "insert",
	(0x2D, False): "numpadInsert",
	(0x2E, True): "delete",
	(0x2E, False): "numpadDelete",
	(0x2F, None): "help",
	(0x5B, None): "leftWindows",
	(0x5C, None): "rightWindows",
	(0x5D, None): "applications",
	(0x5F, None): "sleep",
	(0x60, None): "numLockNumpad0",
	(0x61, None): "numLockNumpad1",
	(0x62, None): "numLockNumpad2",
	(0x63, None): "numLockNumpad3",
	(0x64, None): "numLockNumpad4",
	(0x65, None): "numLockNumpad5",
	(0x66, None): "numLockNumpad6",
	(0x67, None): "numLockNumpad7",
	(0x68, None): "numLockNumpad8",
	(0x69, None): "numLockNumpad9",
	(0x6A, None): "numpadMultiply",
	(0x6B, None): "numpadPlus",
	(0x6C, None): "numpadSeparator",
	(0x6D, None): "numpadMinus",
	(0x6E, None): "numpadDecimal",
	(0x6F, None): "numpadDivide",
	(0x70, None): "f1",
	(0x71, None): "f2",
	(0x72, None): "f3",
	(0x73, None): "f4",
	(0x74, None): "f5",
	(0x75, None): "f6",
	(0x76, None): "f7",
	(0x77, None): "f8",
	(0x78, None): "f9",
	(0x79, None): "f10",
	(0x7A, None): "f11",
	(0x7B, None): "f12",
	(0x7C, None): "f13",
	(0x7D, None): "f14",
	(0x7E, None): "f15",
	(0x7F, None): "f16",
	(0x80, None): "f17",
	(0x81, None): "f18",
	(0x82, None): "f19",
	(0x83, None): "f20",
	(0x84, None): "f21",
	(0x85, None): "f22",
	(0x86, None): "f23",
	(0x87, None): "f24",
	(0x90, None): "numLock",
	(0x91, None): "scrollLock",
	(0xA0, None): "leftShift",
	(0xA1, None): "rightShift",
	(0xA2, None): "leftControl",
	(0xA3, None): "rightControl",
	(0xA4, None): "leftAlt",
	(0xA5, None): "rightAlt",
	(0xA6, None): "browserBack",
	(0xA7, None): "browserForward",
	(0xA8, None): "browserRefresh",
	(0xA9, None): "browserStop",
	(0xAA, None): "browserSearch",
	(0xAB, None): "browserFavorites",
	(0xAC, None): "browserHome",
	(0xAD, None): "volumeMute",
	(0xAE, None): "volumeDown",
	(0xAF, None): "volumeUp",
	(0xB0, None): "mediaNextTrack",
	(0xB1, None): "mediaPrevTrack",
	(0xB2, None): "mediaStop",
	(0xB3, None): "mediaPlayPause",
	(0xB4, None): "launchMail",
	(0xB5, None): "launchMediaPlayer",
	(0xB6, None): "launchApp1",
	(0xB7, None): "launchApp2",
}

#: Maps key names to vk codes.
#: This is the inverse of the L{byCode} map
#: except that names are all lower case to make case insensitive lookup easier.
#: @type: dict with keys of str and values of tuple(int, bool)
byName = dict((name.lower(), code) for code, name in byCode.items())

# Used by SendInput for non-keyboard input to pass Unicode characters as if they were keystrokes.
# The scan code is the Unicode character.
# See https://msdn.microsoft.com/en-us/library/windows/desktop/ms646271(v=vs.85).aspx
VK_PACKET = 0xE7
