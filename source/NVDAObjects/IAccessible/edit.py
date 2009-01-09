from . import IAccessible
from NVDAObjects.window.edit import *

#Create IAccessible versions of some edit window NVDAObjects using mixins
for cls in (Edit,RichEdit,RichEdit20,RichEdit30,RichEdit50):
	globals()[cls.__name__]=type(cls.__name__,(cls,IAccessible),{})
