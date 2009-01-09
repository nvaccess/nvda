from NVDAObjects.window.akelEdit import AkelEdit
from . import IAccessible

AkelEdit=type("AkelEdit",(AkelEdit,IAccessible),{})
