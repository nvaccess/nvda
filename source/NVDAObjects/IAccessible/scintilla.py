from NVDAObjects.window.scintilla import Scintilla
from . import IAccessible

Scintilla=type("Scintilla",(Scintilla,IAccessible),{})
